import { Star } from "lucide-react";
import "./Rating.css";

/** Star icon followed by the numeric rating. */
export default function Rating({ value, className = "" }) {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) return null;
  return (
    <span className={`rating ${className}`} title={`امتیاز کاربران: ${number}`}>
      <Star size={15} fill="currentColor" aria-hidden="true" />
      <span>{number.toLocaleString("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}</span>
    </span>
  );
}
