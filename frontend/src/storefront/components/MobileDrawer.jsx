import { useEffect, useRef } from "react";
import { NavLink } from "react-router-dom";
import { X } from "lucide-react";
import { DrawerAccountLinks } from "./HeaderMenus";
import { categoryIcon } from "./categoryIcon";
import { NAV_LINKS } from "./Header";
import Logo from "./Logo";
import "./MobileDrawer.css";

/** Slide-in navigation for small screens. `categories` is the list of shop categories. */
export default function MobileDrawer({ open, categories, onClose, onLogout }) {
  const closeRef = useRef(null);

  useEffect(() => {
    document.documentElement.classList.toggle("is-locked", open);
    if (open) closeRef.current?.focus();
    return () => document.documentElement.classList.remove("is-locked");
  }, [open]);

  useEffect(() => {
    if (!open) return undefined;
    const handleKey = (event) => event.key === "Escape" && onClose();
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [open, onClose]);

  return (
    <div className={`drawer${open ? " is-open" : ""}`} aria-hidden={!open}>
      <div className="drawer__overlay" onClick={onClose} />
      <aside className="drawer__panel" role="dialog" aria-modal="true" aria-label="منوی سایت" inert={!open ? "" : undefined}>
        <div className="drawer__head">
          <Logo onClick={onClose} />
          <button type="button" className="icon-btn" aria-label="بستن منو" onClick={onClose} ref={closeRef} data-testid="menu-close">
            <X size={24} aria-hidden="true" />
          </button>
        </div>

        <nav className="drawer__body" aria-label="منوی موبایل">
          <ul className="drawer__links">
            {NAV_LINKS.map((link) => (
              <li key={link.to}>
                <NavLink to={link.to} end={link.end} onClick={onClose}>
                  {link.label}
                </NavLink>
              </li>
            ))}
          </ul>

          {categories.length > 0 && (
            <>
              <h2 className="drawer__heading">دسته‌بندی‌ها</h2>
              <ul className="drawer__links">
                {categories.map((category) => {
                  const Icon = categoryIcon(category);
                  return (
                    <li key={category.id}>
                      <NavLink to={`/category/${category.category_slug}`} onClick={onClose}>
                        <Icon size={20} aria-hidden="true" /> {category.category_name}
                      </NavLink>
                    </li>
                  );
                })}
              </ul>
            </>
          )}

          <h2 className="drawer__heading">حساب کاربری</h2>
          <DrawerAccountLinks onNavigate={onClose} onLogout={onLogout} />
        </nav>
      </aside>
    </div>
  );
}
