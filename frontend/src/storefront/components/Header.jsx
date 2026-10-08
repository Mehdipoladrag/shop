import { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Menu, Truck } from "lucide-react";
import { catalogApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { AccountMenu, CartMenu, CategoryMenu } from "./HeaderMenus";
import Logo from "./Logo";
import SearchForm from "./SearchForm";
import "./Header.css";

const SCROLLED_PX = 8;

export const NAV_LINKS = [
  { to: "/", label: "صفحه اصلی", end: true },
  { to: "/products", label: "فروشگاه" },
  { to: "/blog", label: "وبلاگ" },
  { to: "/contact", label: "تماس با ما" },
  { to: "/about", label: "درباره ما" },
];

function useScrolled() {
  const [scrolled, setScrolled] = useState(window.scrollY > SCROLLED_PX);
  useEffect(() => {
    const handle = () => setScrolled(window.scrollY > SCROLLED_PX);
    window.addEventListener("scroll", handle, { passive: true });
    return () => window.removeEventListener("scroll", handle);
  }, []);
  return scrolled;
}

/** Thin announcement strip above the header. */
function PromoBar() {
  return (
    <div className="promo-bar">
      <div className="container promo-bar__inner">
        <Truck size={16} aria-hidden="true" />
        <span>ارسال رایگان برای سفارش‌های بالای ۱ میلیون و ۴۰۰ هزار تومان</span>
      </div>
    </div>
  );
}

/** Promo strip, sticky header with search, account and cart, and the desktop navigation. */
export default function Header({ onSearch, onLogout, onOpenMenu }) {
  const scrolled = useScrolled();
  const categories = useApi(catalogApi.categories);

  return (
    <>
      <PromoBar />
      <header className={`site-header${scrolled ? " is-scrolled" : ""}`}>
        <div className="container site-header__main">
          <button type="button" className="icon-btn site-header__menu" aria-label="باز کردن منو" onClick={onOpenMenu} data-testid="menu-button">
            <Menu size={26} aria-hidden="true" />
          </button>
          <Logo />
          <SearchForm onSearch={onSearch} className="site-header__search" />
          <div className="site-header__actions">
            <AccountMenu onLogout={onLogout} />
            <CartMenu />
          </div>
        </div>

        <nav className="site-nav" aria-label="منوی اصلی">
          <div className="container site-nav__inner">
            {(categories.data ?? []).length > 0 && <CategoryMenu categories={categories.data} />}
            <ul className="site-nav__links">
              {NAV_LINKS.map((link) => (
                <li key={link.to}>
                  <NavLink to={link.to} end={link.end}>
                    {link.label}
                  </NavLink>
                </li>
              ))}
            </ul>
            <Link to="/products?has_offer=1" className="site-nav__offers">
              تخفیف‌های ویژه
            </Link>
          </div>
        </nav>
      </header>
    </>
  );
}
