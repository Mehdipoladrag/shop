# IRANYekan

IRANYekan is a licensed font, so its files are **not** part of this repository.
Buy or download it from the producer (https://fontiran.com) and drop the
`woff2` files here, using exactly these names:

| File                             | Weight  |
| -------------------------------- | ------- |
| `iranyekanweblightfanum.woff2`   | 300     |
| `iranyekanwebregularfanum.woff2` | 400     |
| `iranyekanwebmediumfanum.woff2`  | 500     |
| `iranyekanwebboldfanum.woff2`    | 700     |

Nothing else has to change: `src/shared/fonts.js` finds the files at build
time, bundles them and registers the `IRANYekan` family. Until they exist the
site uses Vazirmatn (SIL Open Font License), so every page stays readable.
