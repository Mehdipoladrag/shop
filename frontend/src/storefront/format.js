// The existing Django site prints prices with Latin digits and thousands
// separators (`{{ price|intcomma }}`), so the React site does the same.
export function formatPrice(value) {
  return Math.round(Number(value) || 0).toLocaleString("en-US");
}

/**
 * Jalali (Persian calendar) date as yy/mm/dd, optionally followed by the
 * time, matching the `to_jalali:'%y/%m/%d | %H:%M:%S'` filter of the site.
 */
export function formatJalaliDate(isoString, { withTime = false } = {}) {
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return "";

  const formatter = new Intl.DateTimeFormat("en-US-u-ca-persian-nu-latn", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
  });
  const parts = Object.fromEntries(formatter.formatToParts(date).map(({ type, value }) => [type, value]));

  const day = `${parts.year.slice(-2)}/${parts.month}/${parts.day}`;
  return withTime ? `${day} | ${parts.hour}:${parts.minute}:${parts.second}` : day;
}

// Shortens text to a number of words, like Django's `truncatewords`.
export function truncateWords(text, wordCount) {
  const words = String(text ?? "").split(/\s+/).filter(Boolean);
  return words.length > wordCount ? `${words.slice(0, wordCount).join(" ")}…` : words.join(" ");
}

// Media URLs come back absolute from the API; keep only the path so images
// load through whichever origin serves the site.
export function toRelativeUrl(url) {
  if (!url) return "";
  try {
    return new URL(url, window.location.origin).pathname;
  } catch {
    return url;
  }
}
