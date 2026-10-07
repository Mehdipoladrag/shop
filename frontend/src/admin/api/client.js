import { tokenStorage } from "./tokenStorage";

export const AUTH_EXPIRED_EVENT = "auth:expired";

export class ApiError extends Error {
  constructor(status, data) {
    super(extractMessage(data) || `Request failed with status ${status}`);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

// DRF returns errors as {detail}, {error}, a list or a {field: [messages]} map.
function extractMessage(data) {
  if (!data) return "";
  if (typeof data === "string") return data;
  if (data.detail) return String(data.detail);
  if (data.error) return String(data.error);
  const firstValue = Array.isArray(data) ? data[0] : Object.values(data)[0];
  return Array.isArray(firstValue) ? String(firstValue[0]) : String(firstValue ?? "");
}

async function parseBody(response) {
  if (response.status === 204) return null;
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function buildOptions(method, body, token) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;

  const options = { method, headers };
  if (body instanceof FormData) {
    // The browser sets the multipart boundary itself.
    options.body = body;
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  return options;
}

// A single in-flight refresh is shared by all requests that hit a 401 at once.
let refreshPromise = null;

async function refreshAccessToken() {
  const refresh = tokenStorage.getRefresh();
  if (!refresh) return null;

  refreshPromise ??= fetch("/api/token/refresh/", {
    ...buildOptions("POST", { refresh }),
  })
    .then(async (response) => {
      if (!response.ok) return null;
      const data = await parseBody(response);
      tokenStorage.setTokens({ access: data.access, refresh: data.refresh });
      return data.access;
    })
    .catch(() => null)
    .finally(() => {
      refreshPromise = null;
    });

  return refreshPromise;
}

/**
 * Sends a request to the backend. Authenticated requests retry once with a
 * refreshed token and signal the app to log out when that fails too.
 */
export async function request(path, { method = "GET", body, auth = true } = {}) {
  let response = await fetch(path, buildOptions(method, body, auth ? tokenStorage.getAccess() : null));

  if (response.status === 401 && auth) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      response = await fetch(path, buildOptions(method, body, newToken));
    }
    if (response.status === 401) {
      tokenStorage.clear();
      window.dispatchEvent(new Event(AUTH_EXPIRED_EVENT));
    }
  }

  const data = await parseBody(response);
  if (!response.ok) throw new ApiError(response.status, data);
  return data;
}
