// The backend returns absolute media URLs built from its own host. Keeping
// only the path makes images load through whichever origin serves the app.
export function toRelativeMediaUrl(url) {
  if (!url) return "";
  try {
    return new URL(url, window.location.origin).pathname;
  } catch {
    return url;
  }
}
