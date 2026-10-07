# Shop admin frontend

React (Vite) admin panel for the Django shop API. Right-to-left, Persian UI,
responsive from phones (drawer menu, tables become cards) to desktops.

## Pages

| Route         | What it does                                           |
| ------------- | ------------------------------------------------------ |
| `/login`      | Admin login (JWT)                                      |
| `/`           | Dashboard: counters and latest orders                  |
| `/categories` | List, create, edit (with image) and delete categories  |
| `/products`   | List and delete products                               |
| `/orders`     | List orders                                            |
| `/users`      | Paginated user list with debounced search              |

## Run it (no Docker)

1. Start the Django backend on port 8001 (see the root README).
2. Install and start the frontend:

```bash
cd frontend
npm install
npm run dev        # http://127.0.0.1:5173
```

The dev server proxies `/shop`, `/accounts`, `/admin-panel`, `/api` and
`/media` to the backend, so no CORS setup is needed. Point it at another
backend with `VITE_BACKEND_URL` (see `.env.example`).

Log in with a user that has `is_staff` or `is_superuser` set.

## Build

```bash
npm run build      # output in dist/
```

## Structure

```
src/
  api/          fetch client with automatic token refresh, endpoint functions
  auth/         AuthContext and ProtectedRoute
  components/   DataTable, Modal, ConfirmDialog, Field, Feedback states
  hooks/        useApi (loading/error state, latest request wins)
  layout/       AdminLayout (topbar, sidebar / mobile drawer)
  pages/        one component per route
  styles/       design tokens, layout and component CSS (light and dark mode)
  utils/        Persian number/date formatting, media URL helper
```
