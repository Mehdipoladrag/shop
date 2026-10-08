import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { ChevronDown, ClipboardList, LayoutGrid, LogIn, LogOut, ShoppingCart, User, UserPlus } from "lucide-react";
import { useAuth } from "../auth/AuthContext";
import { useCart } from "../cart/CartContext";
import { formatPrice, toRelativeUrl } from "../format";
import { categoryIcon } from "./categoryIcon";
import { useDismiss } from "./useDismiss";

const MINI_CART_ITEMS = 3;

/** A button that opens a floating panel; closes on outside click, Escape and navigation. */
function Popover({ label, trigger, panelClassName = "", className = "", children, testId }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const { pathname } = useLocation();
  const close = useCallback(() => setOpen(false), []);

  useDismiss(ref, open, close);
  useEffect(close, [pathname, close]);

  return (
    <div className={`popover ${className}`} ref={ref}>
      <button
        type="button"
        className="popover__trigger"
        aria-expanded={open}
        aria-haspopup="true"
        aria-label={label}
        data-testid={testId}
        onClick={() => setOpen(!open)}
      >
        {trigger}
      </button>
      {open && <div className={`popover__panel ${panelClassName}`}>{typeof children === "function" ? children(close) : children}</div>}
    </div>
  );
}

export function CategoryMenu({ categories }) {
  return (
    <Popover
      label="دسته‌بندی‌ها"
      className="popover--nav"
      panelClassName="popover__panel--categories"
      trigger={
        <>
          <LayoutGrid size={18} aria-hidden="true" />
          <span>دسته‌بندی‌ها</span>
          <ChevronDown size={16} aria-hidden="true" />
        </>
      }
    >
      {(close) => (
        <ul className="category-menu">
          {categories.map((category) => {
            const Icon = categoryIcon(category);
            return (
              <li key={category.id}>
                <Link to={`/category/${category.category_slug}`} onClick={close}>
                  <span className="category-menu__icon">
                    <Icon size={20} aria-hidden="true" />
                  </span>
                  {category.category_name}
                </Link>
              </li>
            );
          })}
          <li className="category-menu__all">
            <Link to="/products" onClick={close}>
              مشاهده همه محصولات
            </Link>
          </li>
        </ul>
      )}
    </Popover>
  );
}

export function AccountMenu({ onLogout }) {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return (
      <Link to="/login" className="header-action header-action--wide" data-testid="login-link">
        <LogIn size={22} aria-hidden="true" />
        <span>ورود | ثبت‌نام</span>
      </Link>
    );
  }

  return (
    <Popover
      label="حساب کاربری"
      className="popover--account"
      panelClassName="popover__panel--account"
      testId="account-menu"
      trigger={
        <>
          <User size={22} aria-hidden="true" />
          <span className="header-action__label">حساب من</span>
          <ChevronDown size={16} aria-hidden="true" />
        </>
      }
    >
      {(close) => (
        <div className="account-menu">
          <div className="account-menu__name">
            <bdi>{user?.first_name || user?.username}</bdi>
          </div>
          <Link to="/account" onClick={close} data-testid="account-link">
            <User size={18} aria-hidden="true" /> پروفایل
          </Link>
          <Link to="/account/orders" onClick={close}>
            <ClipboardList size={18} aria-hidden="true" /> سفارش‌های من
          </Link>
          <button type="button" className="account-menu__logout" data-testid="logout-button" onClick={() => { close(); onLogout(); }}>
            <LogOut size={18} aria-hidden="true" /> خروج
          </button>
        </div>
      )}
    </Popover>
  );
}

export function CartMenu() {
  const { cart } = useCart();
  const items = cart.items ?? [];
  const extra = items.length - MINI_CART_ITEMS;

  return (
    <Popover
      label={`سبد خرید، ${cart.total_count} کالا`}
      className="popover--cart"
      panelClassName="popover__panel--cart"
      testId="cart-menu"
      trigger={
        <>
          <span className="header-action__icon">
            <ShoppingCart size={22} aria-hidden="true" />
            {cart.total_count > 0 && <span className="header-action__count" data-testid="cart-count">{cart.total_count}</span>}
          </span>
          <span className="header-action__label">سبد خرید</span>
        </>
      }
    >
      {(close) => (
        <div className="mini-cart">
          {items.length === 0 ? (
            <div className="mini-cart__empty">
              <ShoppingCart size={34} aria-hidden="true" />
              <p>سبد خرید شما خالی است</p>
              <Link to="/products" className="btn btn--secondary btn--sm" onClick={close}>
                مشاهده محصولات
              </Link>
            </div>
          ) : (
            <>
              <ul className="mini-cart__list">
                {items.slice(0, MINI_CART_ITEMS).map((item) => (
                  <li key={item.product.id}>
                    <img src={toRelativeUrl(item.product.pic)} alt="" width="56" height="56" />
                    <div>
                      <Link to={`/products/${item.product.slug}`} onClick={close}>
                        {item.product.product_name}
                      </Link>
                      <span>
                        {item.product_count} × {formatPrice(item.unit_price)} تومان
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
              {extra > 0 && <p className="mini-cart__more">و {extra} کالای دیگر</p>}
              <div className="mini-cart__total">
                <span>جمع کل</span>
                <strong>{formatPrice(cart.total_price)} تومان</strong>
              </div>
              <div className="mini-cart__actions">
                <Link to="/cart" className="btn btn--secondary btn--sm" onClick={close}>
                  مشاهده سبد
                </Link>
                <Link to="/checkout" className="btn btn--primary btn--sm" onClick={close}>
                  ثبت سفارش
                </Link>
              </div>
            </>
          )}
        </div>
      )}
    </Popover>
  );
}

/** Account links for the mobile drawer, which shows them as a list instead of a popover. */
export function DrawerAccountLinks({ onNavigate, onLogout }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? (
    <ul className="drawer__links drawer__links--account">
      <li>
        <Link to="/account" onClick={onNavigate} data-testid="drawer-account-link">
          <User size={20} aria-hidden="true" /> پروفایل
        </Link>
      </li>
      <li>
        <Link to="/account/orders" onClick={onNavigate}>
          <ClipboardList size={20} aria-hidden="true" /> سفارش‌های من
        </Link>
      </li>
      <li>
        <button type="button" onClick={onLogout} data-testid="drawer-logout-button">
          <LogOut size={20} aria-hidden="true" /> خروج
        </button>
      </li>
    </ul>
  ) : (
    <ul className="drawer__links drawer__links--account">
      <li>
        <Link to="/login" onClick={onNavigate} data-testid="drawer-login-link">
          <LogIn size={20} aria-hidden="true" /> ورود
        </Link>
      </li>
      <li>
        <Link to="/register" onClick={onNavigate}>
          <UserPlus size={20} aria-hidden="true" /> ثبت‌نام
        </Link>
      </li>
    </ul>
  );
}
