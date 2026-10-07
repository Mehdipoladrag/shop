# IRANYekan font files

IRANYekan is a licensed font and its files are **not** included in this repository.
Get the web fonts from the producer (https://fontiran.com) under a license that
fits this project, then place them in this folder with these names:

| Weight  | Files (any of the three; woff2 is tried first)                  |
| ------- | ---------------------------------------------------------------- |
| 300     | `iranyekanweblightfanum.woff2` / `.woff` / `.ttf`                |
| 400     | `iranyekanwebregularfanum.woff2` / `.woff` / `.ttf`              |
| 500     | `iranyekanwebmediumfanum.woff2` / `.woff` / `.ttf`               |
| 700     | `iranyekanwebboldfanum.woff2` / `.woff` / `.ttf`                 |

The "FaNum" variant shows Persian digits, like the Vazir font used before.

`../../css/fonts.css` already declares these faces and sets `--font-main` for the
whole storefront and the admin panel. Until the files exist the browser falls back
to Vazir (`../vazir/vazir-fd-wl.ttf`).

Once IRANYekan works you can delete `../vazir/` and the "Vazir FD" block in
`fonts.css`, and the Vazir files in `frontend/public/panel-fonts/` together with
their `@font-face` rules in `frontend/src/admin/styles/base.css`.

Do not commit the font files to a public repository unless the license allows
redistribution.
