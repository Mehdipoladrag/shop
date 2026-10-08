import { Link } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import "./SectionHeader.css";

/** Heading of a page section with an optional "view all" link and extra content (a countdown, for example). */
export default function SectionHeader({ title, subtitle, to, linkLabel = "مشاهده همه", children }) {
  return (
    <header className="section-header">
      <div className="section-header__titles">
        <h2 className="section-header__title">{title}</h2>
        {subtitle && <p className="section-header__subtitle">{subtitle}</p>}
      </div>
      {children}
      {to && (
        <Link to={to} className="section-header__link">
          {linkLabel}
          <ChevronLeft size={18} aria-hidden="true" />
        </Link>
      )}
    </header>
  );
}
