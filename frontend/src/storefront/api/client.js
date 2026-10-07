export const SESSION_EXPIRED_EVENT = "customer:session-expired";

const CSRF_URL = "/accounts/api/v1/customer/csrf/";
// Requests that need a logged in customer; a 403 on them means the session is gone.
const SESSION_PATHS = ["/accounts/api/v1/customer/", "/shop/api/v1/public/checkout/"];
const LOGIN_PATHS = ["/accounts/api/v1/customer/login/", "/accounts/api/v1/customer/register/"];
const CSRF_COOKIE = "csrftoken";
const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);

// DRF answers in English for authentication, permission and throttling errors.
const STATUS_MESSAGES = {
  401: "برای ادامه وارد حساب کاربری خود شوید.",
  403: "برای ادامه وارد حساب کاربری خود شوید.",
  429: "تعداد تلاش‌های شما بیش از حد مجاز است. کمی بعد دوباره امتحان کنید.",
  409: "درخواست قبلی شما هنوز در حال انجام است. چند لحظه صبر کنید.",
};
const NETWORK_ERROR_MESSAGE = "ارتباط با سرور برقرار نشد. اینترنت خود را بررسی کنید.";
const GENERIC_ERROR_MESSAGE = "خطایی رخ داد. دوباره تلاش کنید.";
// What DRF answers (with status 403) when the session no longer identifies a user.
const NOT_AUTHENTICATED_DETAIL = "Authentication credentials were not provided.";

const CSRF_MESSAGE = "اعتبار درخواست منقضی شده است. صفحه را دوباره بارگذاری کنید.";

// A 403 is "log in first" only when the server says so; a CSRF rejection has its own message.
function messageFor(status, data) {
  const detail = typeof data?.detail === "string" ? data.detail : "";
  if (status === 403 && detail.startsWith("CSRF Failed")) return CSRF_MESSAGE;
  if (status === 403 && detail && detail !== NOT_AUTHENTICATED_DETAIL) return detail;
  return STATUS_MESSAGES[status] ?? firstMessage(data) ?? GENERIC_ERROR_MESSAGE;
}

export class ApiError extends Error {
  constructor(status, data) {
    super(messageFor(status, data));
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

function firstMessage(data) {
  if (!data || typeof data !== "object") return null;
  if (typeof data.detail === "string") return data.detail;
  const first = Object.values(data)[0];
  return [].concat(first)[0] ?? null;
}

/**
 * Field errors of a DRF response as `{field: message}`. Errors that belong to
 * no single field (wrong login, for example) are under `_form`.
 */
export function fieldErrors(error) {
  if (!(error instanceof ApiError) || error.status !== 400 || typeof error.data !== "object") {
    return { _form: error.message };
  }
  const errors = {};
  Object.entries(error.data).forEach(([field, messages]) => {
    const key = field === "non_field_errors" || field === "detail" ? "_form" : field;
    errors[key] = [].concat(messages)[0];
  });
  return errors;
}

function readCookie(name) {
  const match = document.cookie.split("; ").find((cookie) => cookie.startsWith(`${name}=`));
  return match ? decodeURIComponent(match.split("=")[1]) : "";
}

// The CSRF cookie is set by a harmless GET; it also changes after login.
async function csrfToken({ refresh = false } = {}) {
  if (refresh || !readCookie(CSRF_COOKIE)) await fetch(CSRF_URL);
  return readCookie(CSRF_COOKIE);
}

async function parseBody(response) {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function send(path, method, body, { refreshCsrf = false } = {}) {
  try {
    const headers = {};
    if (!SAFE_METHODS.has(method)) headers["X-CSRFToken"] = await csrfToken({ refresh: refreshCsrf });

    let payload;
    if (body instanceof FormData) {
      payload = body; // the browser sets the multipart boundary
    } else if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      payload = JSON.stringify(body);
    }
    return await fetch(path, { method, headers, body: payload });
  } catch {
    // fetch only rejects when the request could not be made at all.
    throw new ApiError(0, { detail: NETWORK_ERROR_MESSAGE });
  }
}

/**
 * JSON request to the backend. The browser sends the session cookie on its
 * own; unsafe methods also carry the CSRF token. A request rejected because
 * the token went stale is retried once with a fresh one.
 */
export async function request(path, { method = "GET", body, params } = {}) {
  const url = `${path}${params ? `?${new URLSearchParams(cleanParams(params))}` : ""}`;

  let response = await send(url, method, body);
  if (response.status === 403 && !SAFE_METHODS.has(method) && (await isCsrfFailure(response))) {
    response = await send(url, method, body, { refreshCsrf: true });
  }

  const data = await parseBody(response);
  if (!response.ok) {
    // The server no longer knows this customer (session expired or ended elsewhere).
    const sessionGone =
      response.status === 403 &&
      data?.detail === NOT_AUTHENTICATED_DETAIL &&
      SESSION_PATHS.some((prefix) => path.startsWith(prefix)) &&
      !LOGIN_PATHS.includes(path);
    if (sessionGone) {
      window.dispatchEvent(new Event(SESSION_EXPIRED_EVENT));
    }
    throw new ApiError(response.status, data);
  }
  return data;
}

// Only a CSRF rejection is worth retrying; a 403 for a missing login is final.
async function isCsrfFailure(response) {
  const data = await parseBody(response.clone());
  const detail = typeof data?.detail === "string" ? data.detail : "";
  // Ours comes from the CSRF middleware, "CSRF Failed" from DRF's session authentication.
  return detail.includes("اعتبار درخواست") || detail.startsWith("CSRF Failed");
}

// Drops empty values so they do not end up as `?color=&brand=` in the URL.
function cleanParams(params) {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== "")
  );
}
