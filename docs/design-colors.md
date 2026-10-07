# Colors of the frontend

## Where the colors are defined

| What                                   | File                                                        |
| -------------------------------------- | ----------------------------------------------------------- |
| Navy scale, semantic names, focus ring | `shop/static/assets/css/palette.css`                        |
| Theme rules (buttons, header, footer…) | `shop/static/assets/css/main.css`, `style.css`, `main_ui.css` use `var(--navy-*)` |
| React-only styles                      | `frontend/src/storefront/styles/app.css` (semantic names)   |
| Admin panel                            | `frontend/src/admin/styles/base.css` (`--primary` = `--navy-700`) |

To re-theme the site change the `--navy-*` (and matching `--navy-*-rgb`) values in
`palette.css`. Contrast on white: navy-500 5.6:1, navy-600 8.2:1, navy-700 11.1:1.

## Colors that do not come from CSS

These raster images are mostly teal (the old brand color) and are **not** affected
by the palette. Replace them with navy versions to finish the re-theme.

| Group | Files (under `shop/static/assets/img/`) |
| ----- | ---------------------------------------- |
| Logo and icons | `logo.png`, `favicon.png` |
| Top strip and banners | `banner_img/bg_top.jpg`, `banner_img/img-3.jpg` … `img-9.jpg`, `banner_img/01/*.jpg`, `banner_img/02/*.jpg` |
| Section titles | `shegeft_1.png`, `seller_1.png` |
| Shortcut icons on the home page | `Masai/minilogo/1.png` … `8.png` |
| Payment method icons | `ico/png-8.png` … `png-11.png` |
| Licence badges | `License_1.png`, `License_2.png` |
| Illustrations | `empty-cart.png`, `successful-cart.png`, `about.png` (partly) |
| Footer background | `map.png` |

Product, category, brand and blog pictures are uploaded content (`media/`) and keep
their own colors.

## Colors that stay as they are

Status colors keep their usual meaning: success green, warning amber, danger red
(see `--color-success`, `--color-warning`, `--color-danger`). Neutral greys of the
theme were left alone except the ones that failed the AA contrast check (old
prices, small captions, disabled pagination).
