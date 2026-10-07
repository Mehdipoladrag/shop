import { resolve } from "node:path";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// Backend routes the frontend talks to. They are proxied in development so
// the browser sees a single origin: no CORS setup, and the Django session
// cookie (used by the shopping cart) works as is. `/static` serves the
// existing storefront stylesheets, fonts and images straight from Django.
const BACKEND_PATHS = [
  "/shop/api",
  "/accounts/api",
  "/admin-panel/api",
  "/blog/api",
  "/api",
  "/media",
  "/static",
];

const ADMIN_BASE = "/panel";

// Serves the admin app's index.html for any /panel/... route in dev, the
// same way a history-API fallback does for a single-page app.
function adminFallback() {
  return {
    name: "admin-spa-fallback",
    configureServer(server) {
      server.middlewares.use((request, _response, next) => {
        const [path] = request.url.split("?");
        const isAdminRoute = path === ADMIN_BASE || path.startsWith(`${ADMIN_BASE}/`);
        const isAsset = path.includes(".") || path.includes("/@") || path.includes("/node_modules/");
        if (isAdminRoute && !isAsset) request.url = `${ADMIN_BASE}/index.html`;
        next();
      });
    },
  };
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const backendUrl = env.VITE_BACKEND_URL || "http://127.0.0.1:8001";

  const proxy = Object.fromEntries(
    BACKEND_PATHS.map((path) => [path, { target: backendUrl, changeOrigin: true }])
  );

  return {
    plugins: [react(), adminFallback()],
    server: { port: 5173, proxy },
    build: {
      rollupOptions: {
        input: {
          storefront: resolve(import.meta.dirname, "index.html"),
          admin: resolve(import.meta.dirname, "panel/index.html"),
        },
      },
    },
  };
});
