import { Link } from "react-router-dom";
import { BRAND } from "../../shared/brand";
import "./Logo.css";

/** Brand mark and wordmark, drawn in SVG and CSS so it follows the palette. */
export default function Logo({ variant = "color", onClick }) {
  return (
    <Link to="/" className={`logo logo--${variant}`} aria-label={`${BRAND.name}، صفحه اصلی`} onClick={onClick}>
      <svg className="logo__mark" viewBox="0 0 40 40" aria-hidden="true">
        <rect className="logo__mark-bg" width="40" height="40" rx="12" />
        <path
          className="logo__mark-glyph"
          d="M11.5 13h17M20 13v16"
          fill="none"
          strokeWidth="3.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle className="logo__mark-dot" cx="30.5" cy="29" r="3.2" />
      </svg>
      <span className="logo__text">
        <span className="logo__name">{BRAND.name}</span>
        <span className="logo__latin" aria-hidden="true">
          {BRAND.latin}
        </span>
      </span>
    </Link>
  );
}
