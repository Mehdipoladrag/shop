import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// Django routes that the frontend talks to. They are proxied in development
// so the browser sees a single origin and no CORS configuration is needed.
const BACKEND_PATHS = ["/shop", "/accounts", "/admin-panel", "/api", "/media"];

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const backendUrl = env.VITE_BACKEND_URL || "http://127.0.0.1:8001";

  const proxy = Object.fromEntries(
    BACKEND_PATHS.map((path) => [path, { target: backendUrl, changeOrigin: true }])
  );

  return {
    plugins: [react()],
    server: { port: 5173, proxy },
  };
});
