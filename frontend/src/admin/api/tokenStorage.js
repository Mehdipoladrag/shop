// The access token key matches the one used by the Django-rendered admin
// pages, so a login in either place is valid in both.
const ACCESS_KEY = "jwtToken";
const REFRESH_KEY = "jwtRefreshToken";

function safeGet(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSet(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // Storage can be unavailable (private mode); the session then lasts one page load.
  }
}

function safeRemove(key) {
  try {
    localStorage.removeItem(key);
  } catch {
    // Nothing to clean up when storage is unavailable.
  }
}

export const tokenStorage = {
  getAccess: () => safeGet(ACCESS_KEY),
  getRefresh: () => safeGet(REFRESH_KEY),
  setTokens({ access, refresh }) {
    if (access) safeSet(ACCESS_KEY, access);
    if (refresh) safeSet(REFRESH_KEY, refresh);
  },
  clear() {
    safeRemove(ACCESS_KEY);
    safeRemove(REFRESH_KEY);
  },
};
