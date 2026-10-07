// Address of the Django site. Pages that are still rendered by Django (login,
// registration, profile, checkout) are linked through it.
const backendUrl = import.meta.env.VITE_BACKEND_URL ?? "http://127.0.0.1:8001";

export const djangoUrl = (path) => `${backendUrl.replace(/\/$/, "")}${path}`;

// Static assets (images, icons) come from Django's static files.
export const staticUrl = (path) => `/static/assets/${path}`;
