import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useCart } from "../cart/CartContext";
import { useSession } from "../session/SessionContext";
import { djangoUrl, staticUrl } from "../config";
import { formatPrice } from "../format";

const SCROLL_SHRINK_PX = 60;
const MOBILE_HEADER_HEIGHT_PX = 60;

const NAV_LINKS = [
  { to: "/products", label: "فروشگاه", icon: "fa-shop" },
  { to: "/categories", label: "دسته بندی محصولات", icon: "fa-list-alt" },
  { to: "/blog", label: "وبلاگ ها", icon: "fa-newspaper" },
  { to: "/contact", label: "تماس با ما", icon: "fa-phone" },
  { to: "/about", label: "درباره ما", icon: "fa-address-card" },
];

function useScrolledPast(thresholdPx) {
  const [scrolled, setScrolled] = useState(window.scrollY > thresholdPx);
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > thresholdPx);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [thresholdPx]);
  return scrolled;
}

function SearchForm({ className, onSearch }) {
  const [query, setQuery] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(query.trim());
  }

  return (
    <form className={className} onSubmit={handleSubmit}>
      <input type="text" name="q" placeholder="جستجو ..." value={query} onChange={(event) => setQuery(event.target.value)} />
      <button type="submit">
        <img src={staticUrl("img/search.png")} alt="جستجو" />
      </button>
    </form>
  );
}

export function MobileHeader({ menuOpen, onToggleMenu, onNavigate, onSearch }) {
  const session = useSession();
  const scrolled = useScrolledPast(SCROLL_SHRINK_PX);

  return (
    <nav
      className="navbar direction-ltr fixed-top header-responsive"
      style={scrolled ? { height: MOBILE_HEADER_HEIGHT_PX } : undefined}
    >
      <div className="container">
        <div className="navbar-translate">
          <button
            className={`navbar-toggler navbar-toggler-right${menuOpen ? " toggled" : ""}`}
            type="button"
            aria-expanded={menuOpen}
            aria-label="Toggle navigation"
            onClick={onToggleMenu}
          >
            <span className="navbar-toggler-bar bar1" />
            <span className="navbar-toggler-bar bar2" />
            <span className="navbar-toggler-bar bar3" />
          </button>
          <div className="search-nav default" style={scrolled ? { opacity: 0, visibility: "hidden" } : undefined}>
            <SearchForm onSearch={onSearch} />
            <ul>
              {session.is_authenticated ? (
                <>
                  <li>
                    <a href={djangoUrl("/accounts/profile/")}>
                      <i className="fa-regular fa-user colormain" aria-hidden="true" />
                    </a>
                  </li>
                  <li>
                    <a href={djangoUrl("/accounts/logout/")} className="list__link">
                      <i className="fa fa-sign-out icon-icon icon-color-1" aria-hidden="true" />
                    </a>
                  </li>
                </>
              ) : (
                <li>
                  <a href={djangoUrl("/accounts/login/")}>
                    <i className="fa fa-sign-in colormain" aria-hidden="true" />
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>
        <div className="collapse navbar-collapse justify-content-end" id="navigation">
          <div className="logo-nav-res default text-center">
            <Link to="/" onClick={onNavigate}>
              <img src={staticUrl("img/logo.png")} alt="مسای شاپ" />
            </Link>
          </div>
          <ul className="navbar-nav default">
            {NAV_LINKS.map((link) => (
              <li key={link.to}>
                <Link to={link.to} onClick={onNavigate}>
                  {link.label}
                </Link>
              </li>
            ))}
            {!session.is_authenticated && (
              <li>
                <a href={djangoUrl("/accounts/register/")}>ثبت نام</a>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

function CartDropdown() {
  const { cart } = useCart();
  const [open, setOpen] = useState(false);

  return (
    <div className={`cart dropdown masai_dropdown${open ? " show" : ""}`}>
      <span className="divider" />
      <a
        href="/cart"
        className="dropdown-toggle iconhead"
        aria-expanded={open}
        onClick={(event) => {
          event.preventDefault();
          setOpen(!open);
        }}
      >
        <i className="fa fa-cart-arrow-down font-20" aria-hidden="true" />
      </a>
      <div className={`dropdown-menu${open ? " show" : ""}`}>
        <div className="m_cart-header">
          <div className="m_cart-total">
            {cart.total_count > 0
              ? `${cart.total_count} کالا — ${formatPrice(cart.total_price)} تومان`
              : "سبد خرید شما خالی است"}
          </div>
        </div>
        <div className="btn_cart">
          <Link to="/cart" className="btn btn_sabad" onClick={() => setOpen(false)}>
            مشاهده سبد
          </Link>
          <a href={djangoUrl("/shop/payment/checkout/")} className="btn btn_pardakht btn-main-masai">
            پرداخت
          </a>
        </div>
      </div>
    </div>
  );
}

export function PcHeader({ onSearch }) {
  const session = useSession();

  return (
    <header className="Masai-header default">
      <div className="container-fluid">
        <div className="row">
          <div className="col-lg-2 col-md-3 col-sm-4 col-5">
            <div className="logo-area default">
              <Link to="/">
                <img src={staticUrl("img/logo.png")} alt="مسای شاپ" />
              </Link>
            </div>
          </div>
          <div className="col-lg-8 col-md-5 col-sm-8 col-7">
            <div className="search-area default">
              <SearchForm className="search" onSearch={onSearch} />
            </div>
          </div>
          <div className="col-md-2 col-sm-12">
            <div className="user_head">
              {session.is_authenticated ? (
                <a href={djangoUrl("/accounts/profile/")} className="iconhead">
                  <i className="fa fa-user icon-icon icon-color-1" aria-hidden="true">
                    <span>پروفایل </span>
                  </i>
                </a>
              ) : (
                <a href={djangoUrl("/accounts/login/")} className="iconhead">
                  <i className="fa fa-sign-in font-20" aria-hidden="true" />
                </a>
              )}
            </div>
            <CartDropdown />
          </div>
        </div>
      </div>
      <nav className="nav_header">
        <ul className="nav__ullist">
          <li className="list_style">
            <i className="fa fa-home icon-icon" aria-hidden="true" />
            <Link to="/" className="list__link">
              صفحه اصلی
            </Link>
          </li>
          {NAV_LINKS.map((link) => (
            <li className="list_style" key={link.to}>
              <i
                className={`fa ${link.icon} icon-icon`}
                style={link.icon === "fa-address-card" ? { color: "#46A9AE" } : undefined}
                aria-hidden="true"
              />
              <Link to={link.to} className="list__link">
                {link.label}
              </Link>
            </li>
          ))}
          <ul className="nav_header-2">
            <li className="list_style">
              {session.is_authenticated ? (
                <a href={djangoUrl("/accounts/logout/")} className="list__link">
                  <i className="fa fa-sign-out icon-icon icon-color-1" aria-hidden="true">
                    <span>خروج</span>
                  </i>
                </a>
              ) : (
                <a href={djangoUrl("/accounts/register/")} className="list__link">
                  <i className="fa fa-user-plus icon-icon icon-color-1" aria-hidden="true" />
                </a>
              )}
            </li>
          </ul>
        </ul>
      </nav>
    </header>
  );
}

export function TopBanner() {
  return (
    <div className="top-section fullscreen-container">
      <img src={staticUrl("img/banner_img/bg_top.jpg")} className="h-100" alt="" />
    </div>
  );
}
