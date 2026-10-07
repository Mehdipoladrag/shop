export class ApiError extends Error {
  constructor(status, data) {
    super(data?.detail || `Request failed with status ${status}`);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
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

/**
 * JSON request to the backend. The browser sends the session cookie on its
 * own, which is how the shopping cart is tied to the visitor.
 */
export async function request(path, { method = "GET", body, params } = {}) {
  const query = params ? `?${new URLSearchParams(cleanParams(params))}` : "";
  const response = await fetch(`${path}${query}`, {
    method,
    headers: body === undefined ? {} : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  const data = await parseBody(response);
  if (!response.ok) throw new ApiError(response.status, data);
  return data;
}

// Drops empty values so they do not end up as `?color=&brand=` in the URL.
function cleanParams(params) {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== "")
  );
}
