# Shop frontend (React + Vite)

One Vite project with two right-to-left, responsive apps for the Django shop:

| App          | URL      | What it is                                                         |
| ------------ | -------- | ------------------------------------------------------------------ |
| Storefront   | `/`      | The customer site, rebuilt in React with the existing Masai design |
| Admin panel  | `/panel` | Dashboard and management pages for staff                           |

## Storefront

It uses the theme's own stylesheets, fonts and images, served by Django under
`/static/assets`, with the same class names and markup as the Django templates,
so it looks like the current site. The jQuery behaviour (Owl carousels, countdown,
slide-in mobile menu, tabs) is reimplemented in React.

| Route                       | Page                                               |
| --------------------------- | -------------------------------------------------- |
| `/`                         | Home: hero slider, offers, best rated, categories, brands, blog |
| `/products`, `/categories`  | Shop listing with filters, sorting, pagination     |
| `/category/:slug`           | Products of one category                           |
| `/search?q=`                | Search results                                     |
| `/products/:slug`           | Product page with gallery, tabs and add to cart    |
| `/cart`                     | Cart (stored in the Django session)                |
| `/blog`, `/blog/:slug`      | Blog list and post                                 |
| `/about`, `/contact`        | Info pages; the contact form posts to the API      |
| `/login`, `/register`       | Customer login and registration                    |
| `/account`                  | Profile; `/account/edit` (with picture), `/account/password`, `/account/address` |
| `/account/orders`           | Orders; `/account/orders/:id` status, `/account/orders/current` the latest |
| `/checkout`                 | Checkout; `/checkout/success/:id` confirmation     |

Filters, sort order and page are kept in the URL (`?brand=1&color=...&ordering=price`).

Login uses the Django session cookie. Every change (login, registration, cart,
profile, checkout) sends the CSRF token from the `csrftoken` cookie in the
`X-CSRFToken` header; `src/storefront/api/client.js` does this and retries once
when the token has gone stale. Online payment is not connected yet: an order is
stored with a `pending` transaction.

Data comes from the public API under `/shop/api/v1/public/` (categories, brands,
products, filters, cart, checkout, blog, contact, session) and the customer API under
`/accounts/api/v1/customer/` (register, login, logout, profile, password, address, orders).

## Admin panel

Log in with a user that has `is_staff` or `is_superuser`.

| Route         | Page                                                   |
| ------------- | ------------------------------------------------------ |
| `/panel/login`      | Admin login (JWT, refreshed automatically)       |
| `/panel`            | Dashboard: counters and latest orders            |
| `/panel/categories` | List, create, edit (with image) and delete       |
| `/panel/products`   | List and delete                                  |
| `/panel/orders`     | List                                             |
| `/panel/users`      | Paginated list with debounced search             |

## Run it (no Docker)

1. Start the Django backend on port 8001 (see the root README).
2. Install and start the frontend:

```bash
cd frontend
npm install
npm run dev        # http://127.0.0.1:5173  (admin: http://127.0.0.1:5173/panel)
```

The dev server proxies `/shop/api`, `/accounts/api`, `/admin-panel/api`,
`/blog/api`, `/api`, `/media` and `/static` to the backend, so the browser sees a
single origin: no CORS setup, and the session cookie used by the cart works.
`VITE_BACKEND_URL` (see `.env.example`) sets the backend address.

## Build

```bash
npm run build      # output in dist/ (index.html and panel/index.html)
```

Serve `dist/` from the same origin as Django, with `/` and `/panel/` falling back
to their `index.html`.

## Structure

```
index.html            storefront entry (theme stylesheets from /static)
panel/index.html      admin entry
src/
  shared/             Persian formatting helpers, useApi hook
  storefront/
    api/              fetch client and endpoint functions
    cart/             cart context (session cart)    session/  login state
    components/       Layout, Header, Footer, Carousel, Countdown, ProductItem ...
    pages/            one component per route
  admin/              the admin app (api, auth, components, layout, pages, styles)
```
