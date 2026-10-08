# Storefront design guide

The storefront (`src/storefront`) draws everything itself: colors come from
`src/shared/palette.css`, type from `src/shared/fonts.css`, and the shared
look from `src/storefront/styles` and `src/storefront/components`. It does not
use any file from Django's `/static` folder. A live preview of the kit is at
`/design-kit` in development.

## Principles

- **Calm and confident.** Navy is the brand color and dominates (header,
  primary buttons, prices, headings). Coral is an accent used sparingly:
  discount badges, the cart counter, one highlight per page. Never use coral
  for body text; use `--coral-700` when coral text is needed.
- **Soft surfaces.** Page background `--color-bg`, content on white cards
  (`.card`, radius 16, 1px `--color-line` border, tinted shadow). Group things
  with space before reaching for a border.
- **Spacing on a 4px scale** (`--space-*`), sections separated by
  `.section` (fluid 2 to 3.5rem). Never hard-code random pixel values.
- **Typography.** `--fs-*` scale, headings 700, body line-height 1.85 for
  readable Persian. Nothing below 12px. Numbers are written with Latin digits
  (`formatPrice`); the font draws them as Persian digits.
- **Right-to-left first.** Use logical properties (`margin-inline-start`,
  `inset-inline-end`, `padding-inline`, `text-align: start`). Arrows that mean
  "forward" point left, "back" point right.
- **Mobile first.** Breakpoints 640, 768, 992, 1200. At 320 px and 390 px there
  must be no horizontal scroll; tap targets are at least 44 px.
- **Accessible.** Text contrast at least 4.5:1, visible focus (global
  `:focus-visible`), every input has a label, icon-only buttons have an
  `aria-label`, one `h1` per page and no skipped heading levels, informative
  images have `alt` (decorative ones `alt=""`).
- **Every async view has three states:** loading (skeleton), error (retry),
  empty (illustration icon, one sentence, one action). Use `AsyncContent`,
  `LoadError` and `EmptyState`.
- **Motion is subtle** (180 ms ease, no bouncing) and respects
  `prefers-reduced-motion` (handled globally).
- **Icons** come from `lucide-react` (`size` 18 to 24, `aria-hidden="true"`).
- **Persian copy is short and friendly.** No English filler text.

## Building blocks

| Need | Use |
| --- | --- |
| Page wrapper | `<main className="page"><div className="container">…` |
| Section | `<section className="section">` + `<SectionHeader title to>` |
| Card | `.card`, `.card--pad`, `.card__title` |
| Buttons | `.btn` + `--primary` `--accent` `--secondary` `--ghost` `--danger`, `--sm` `--lg` `--block`; `.icon-btn` |
| Forms | `<FormField label error hint icon>` (+ `.input` `.select` `.textarea`), `<FormError>` |
| Product | `<ProductCard product>` inside `.product-grid` or `<Carousel variant="cards">` |
| Price | `<Price product size="md|lg">` |
| Rating, stepper | `<Rating value>`, `<QuantityStepper value max onChange>` |
| Carousel | `<Carousel variant="cards|posts|brands|hero" autoplay dots label>` |
| Lists | `<Pagination page pageCount onChange>`, `<Breadcrumb items>` |
| States | `<AsyncContent state variant>`, `<EmptyState icon title text>`, `<LoadError>`, `<NotFound>` |
| Feedback | `useFlash().show(text, "success" | "error")`, `.badge`, `.status-badge--*` |
| Long text | `.prose` |
| Countdown | `<Countdown tone="dark|light">` |
| Category icon | `categoryIcon(category)` (lucide icon for a category) |

Page-specific styles live next to the page (`pages/home.css`, …) and use only
tokens (`var(--…)`); a class is prefixed with its page or component name
(`.home-hero__title`) so nothing leaks.

## Test hooks

End-to-end tests find elements by `data-testid` and visible text, not by CSS
classes. Keep the existing flash messages and error texts word for word.
