import { useEffect, useState } from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { BRAND } from "../../shared/brand";

const NAV_ITEMS = [
  { to: "/", label: "داشبورد", end: true },
  { to: "/categories", label: "دسته‌بندی‌ها" },
  { to: "/products", label: "محصولات" },
  { to: "/orders", label: "سفارش‌ها" },
  { to: "/users", label: "کاربران" },
];

export default function AdminLayout() {
  const { logout } = useAuth();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  // Close the mobile drawer after navigating.
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  return (
    <div className={`shell${menuOpen ? " shell--menu-open" : ""}`}>
      <header className="topbar">
        <button
          type="button"
          className="icon-btn topbar__menu"
          aria-label="باز و بسته کردن منو"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          ☰
        </button>
        <span className="topbar__brand">{`پنل مدیریت ${BRAND.name}`}</span>
        <button type="button" className="btn btn--ghost topbar__logout" onClick={logout}>
          خروج
        </button>
      </header>

      <aside className="sidebar" aria-label="منوی اصلی">
        <nav>
          {NAV_ITEMS.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end} className="sidebar__link">
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="scrim" onClick={() => setMenuOpen(false)} aria-hidden="true" />

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
