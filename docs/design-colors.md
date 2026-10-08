# Colors of the frontend

The storefront and the admin panel draw everything with CSS, SVG and icons, so
every color on screen comes from one file.

## Where the colors are defined

| What | File |
| ---- | ---- |
| Navy scale, coral accent, status colors, focus ring | `frontend/src/shared/palette.css` |
| Surfaces, text, lines, shadows and the other design tokens | `frontend/src/storefront/styles/tokens.css` |
| Admin panel (`--primary` = `--navy-700`) | `frontend/src/admin/styles/base.css` |

To re-theme the site change the `--navy-*` (and the matching `--navy-*-rgb`)
values in `palette.css`; the coral accent is `--coral-*`.

| Role | Token | Notes |
| ---- | ----- | ----- |
| Brand, primary buttons, prices | `--navy-700` (`#1f3a6e`) | 11.1:1 on white |
| Headings, footer | `--navy-900` / `--navy-950` | |
| Links | `--navy-600` | 8.2:1 on white |
| Discount badges, cart counter | `--coral-500` (`#ff6b4a`) | fill color: put `--navy-950` text on it (6.5:1) |
| Coral text or coral button with white text | `--coral-700` (`#c93f1f`) | 5.0:1 on white |
| Muted text | `--color-muted` (`#566686`) | 5.8:1 on white |

All text colors pass WCAG AA (4.5:1). `frontend/DESIGN.md` explains how the
colors are used.

## Colors that do not come from CSS

Product, category, brand and blog pictures are uploaded content (`media/`) and
keep their own colors. Everything else (logo, banners, icons, illustrations) is
drawn in code and follows the palette.

## Colors that stay as they are

Status colors keep their usual meaning: success green, warning amber, danger red
(`--color-success`, `--color-warning`, `--color-danger`).
