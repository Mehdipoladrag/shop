// What the shop listing reads from the URL and sends to the product API.
// The URL is the single source of truth: page, sort order and every filter live there.

export const PAGE_SIZE = 12;

// Each sort option is an `ordering` value of the product API.
export const SORT_OPTIONS = [
  { key: "recommended", ordering: "-product_rate", label: "پیشنهاد خریداران" },
  { key: "newest", ordering: "-create_date", label: "جدیدترین" },
  { key: "cheapest", ordering: "price", label: "ارزان‌ترین" },
  { key: "expensive", ordering: "-price", label: "گران‌ترین" },
  { key: "fastest", ordering: "time_send", label: "سریع‌ترین ارسال" },
];
export const DEFAULT_ORDERING = SORT_OPTIONS[0].ordering;

// URL keys that are filters (the sort order, page and search text are not).
export const FILTER_KEYS = ["brand", "color", "min_price", "max_price", "in_stock", "has_offer"];
export const CLEARED_FILTERS = Object.fromEntries(FILTER_KEYS.map((key) => [key, ""]));

export const splitList = (value) => (value ? value.split(",").filter(Boolean) : []);

/** Adds `item` to a comma separated URL value, or removes it when it is already there. */
export function toggleListValue(current, item) {
  const values = splitList(current);
  const next = values.includes(item) ? values.filter((value) => value !== item) : [...values, item];
  return next.join(",");
}

/** Reads the listing state out of the URL; unknown or broken values fall back to the defaults. */
export function readFilters(searchParams) {
  const page = Math.floor(Number(searchParams.get("page")));
  const ordering = searchParams.get("ordering");
  const brand = searchParams.get("brand") ?? "";
  const color = searchParams.get("color") ?? "";

  return {
    query: (searchParams.get("q") ?? "").trim(),
    page: page >= 1 ? page : 1,
    ordering: SORT_OPTIONS.some((option) => option.ordering === ordering) ? ordering : DEFAULT_ORDERING,
    brand,
    brands: splitList(brand),
    color,
    colors: splitList(color),
    minPrice: searchParams.get("min_price") ?? "",
    maxPrice: searchParams.get("max_price") ?? "",
    inStock: searchParams.get("in_stock") === "1",
    hasOffer: searchParams.get("has_offer") === "1",
  };
}

/** How many filters are switched on (every brand and colour counts, the price range counts once). */
export function countActiveFilters(filters) {
  const price = filters.minPrice || filters.maxPrice ? 1 : 0;
  return filters.brands.length + filters.colors.length + price + Number(filters.inStock) + Number(filters.hasOffer);
}

/** Query parameters of the product API for the current mode and URL. */
export function productQuery(mode, slug, filters) {
  return {
    category: mode === "category" ? slug : undefined,
    search: mode === "search" ? filters.query : undefined,
    page: filters.page,
    page_size: PAGE_SIZE,
    ordering: filters.ordering,
    brand: filters.brand,
    color: filters.color,
    min_price: filters.minPrice,
    max_price: filters.maxPrice,
    in_stock: filters.inStock ? 1 : undefined,
    has_offer: filters.hasOffer ? 1 : undefined,
  };
}

const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩";
const MAX_PRICE_DIGITS = 12;

/** What a visitor typed into a price box, as plain Latin digits (Persian and Arabic digits are accepted). */
export function cleanPriceInput(value) {
  return value
    .replace(/[۰-۹]/g, (digit) => String(PERSIAN_DIGITS.indexOf(digit)))
    .replace(/[٠-٩]/g, (digit) => String(ARABIC_DIGITS.indexOf(digit)))
    .replace(/\D/g, "")
    .slice(0, MAX_PRICE_DIGITS);
}

/** Digits with thousands separators for the price boxes; anything else is shown as it is. */
export function showPriceInput(value) {
  return /^\d+$/.test(value) ? Number(value).toLocaleString("en-US") : value;
}
