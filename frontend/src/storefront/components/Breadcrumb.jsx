import { Fragment } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, House } from "lucide-react";
import "./Breadcrumb.css";

/** `items` is a list of `{label, to}`; the last item is the current page and has no link. */
export default function Breadcrumb({ items }) {
  return (
    <nav className="breadcrumb" aria-label="مسیر صفحه">
      <ol className="breadcrumb__list">
        <li>
          <Link to="/" aria-label="صفحه اصلی">
            <House size={16} aria-hidden="true" />
          </Link>
        </li>
        {items.map((item, index) => (
          <Fragment key={`${item.label}-${index}`}>
            <li aria-hidden="true">
              <ChevronLeft size={14} />
            </li>
            <li>
              {item.to && index < items.length - 1 ? (
                <Link to={item.to}>{item.label}</Link>
              ) : (
                <span aria-current="page">{item.label}</span>
              )}
            </li>
          </Fragment>
        ))}
      </ol>
    </nav>
  );
}
