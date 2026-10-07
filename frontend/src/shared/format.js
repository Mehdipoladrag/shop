const PERSIAN_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];

export function toPersianDigits(value) {
  return String(value ?? "").replace(/\d/g, (digit) => PERSIAN_DIGITS[digit]);
}

export function formatNumber(value) {
  const number = Number(value);
  if (Number.isNaN(number)) return toPersianDigits(value);
  return toPersianDigits(number.toLocaleString("en-US"));
}

export function formatPrice(value) {
  return `${formatNumber(Math.round(Number(value) || 0))} تومان`;
}

export function formatDate(isoString) {
  if (!isoString) return "—";
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return "—";
  return toPersianDigits(
    new Intl.DateTimeFormat("fa-IR-u-nu-latn", { dateStyle: "medium" }).format(date)
  );
}
