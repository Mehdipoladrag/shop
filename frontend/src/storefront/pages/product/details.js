// What the product page reads out of the product API record.

/** Highest user rating (the API stores one decimal; the old page showed "x/10"). */
export const MAX_RATE = 10;
/** The cart accepts 1 to 9 pieces of one product (see the cart API). */
export const MAX_PER_ORDER = 9;
/** Below this many pieces the product is shown as "almost sold out". */
export const LOW_STOCK_LIMIT = 5;

export const stockOf = (product) => Number(product.product_number) || 0;

/** Facts shown as small cards next to the title; only the ones that have a value. */
export function keyFacts(product) {
  const resolution = Number(product.resolution);
  const facts = [
    { key: "color", label: "رنگ", value: product.product_color },
    { key: "os", label: "سیستم‌عامل", value: product.platform_os },
    { key: "technology", label: "فناوری", value: product.technology },
    { key: "capability", label: "قابلیت", value: product.capability },
    { key: "camera", label: "رزولوشن دوربین", value: resolution > 0 ? `${resolution} مگاپیکسل` : "" },
    { key: "bluetooth", label: "بلوتوث", value: product.bluetooth },
  ];
  return facts.filter((fact) => String(fact.value ?? "").trim() !== "");
}

const MAX_KEY_LENGTH = 40;
const URL_PATTERN = /^https?:\/\/\S+$/;

export const isWebAddress = (text) => URL_PATTERN.test(text);

/**
 * Turns the specifications text into table rows. Every line of the form
 * "key: value" is a two-column row; any other line (no colon, or a sentence
 * with a colon far into it) is a full-width row.
 */
export function parseSpecs(text) {
  return String(text ?? "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => {
      const colon = line.indexOf(":");
      if (colon <= 0 || isWebAddress(line)) return { id: index, text: line };
      const key = line.slice(0, colon).trim();
      const value = line.slice(colon + 1).trim();
      if (!key || !value || key.length > MAX_KEY_LENGTH) return { id: index, text: line };
      return { id: index, key, value };
    });
}

/**
 * Paragraphs of the description. The catalog repeats the notice at the end of
 * the description; it has its own alert, so it is left out here unless it is all there is.
 */
export function descriptionParagraphs(description, notice) {
  const paragraphs = String(description ?? "")
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);
  const own = paragraphs.filter((paragraph) => paragraph !== String(notice ?? "").trim());
  return own.length > 0 ? own : paragraphs;
}
