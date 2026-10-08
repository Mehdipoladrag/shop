import { Link } from "react-router-dom";
import "./Logo.css";

/** Brand mark and wordmark, drawn in SVG and CSS so it follows the palette. */
export default function Logo({ variant = "color", onClick }) {
  return (
    <Link to="/" className={`logo logo--${variant}`} aria-label="مَسای شاپ، صفحه اصلی" onClick={onClick}>
      <svg className="logo__mark" viewBox="0 0 40 40" aria-hidden="true">
        <rect className="logo__mark-bg" width="40" height="40" rx="12" />
        <path
          className="logo__mark-glyph"
          d="M10.5 28.5V15c0-.9 1.1-1.3 1.7-.7l7.8 7.7 7.8-7.7c.6-.6 1.7-.2 1.7.7v13.5"
          fill="none"
          strokeWidth="3.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle className="logo__mark-dot" cx="30.5" cy="10.5" r="3.2" />
      </svg>
      <span className="logo__text">
        <span className="logo__name">مَسای</span>
        <span className="logo__latin" aria-hidden="true">
          MASAI SHOP
        </span>
      </span>
    </Link>
  );
}
