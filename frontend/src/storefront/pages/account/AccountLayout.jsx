import { useEffect, useRef } from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { LockKeyhole, MapPin, PackageSearch, UserPen, UserRound } from "lucide-react";
import { customerApi } from "../../api/endpoints";
import { useApi } from "../../../shared/useApi";
import Breadcrumb from "../../components/Breadcrumb";
import { LoadError } from "../../components/States";
import Avatar from "./Avatar";
import { AccountSkeleton } from "./AccountSkeleton";
import "../account.css";

const MENU = [
  { to: "/account", label: "پروفایل", icon: UserRound, end: true, testId: "profile" },
  { to: "/account/orders", label: "لیست سفارشات من", icon: PackageSearch, testId: "orders" },
  { to: "/account/address", label: "آدرس ها", icon: MapPin, testId: "address" },
  { to: "/account/edit", label: "ویرایش اطلاعات", icon: UserPen, testId: "edit" },
  { to: "/account/password", label: "امنیت و تغییر رمز", icon: LockKeyhole, testId: "password" },
];

function ProfileCard({ profile }) {
  const fullName = `${profile.first_name ?? ""} ${profile.last_name ?? ""}`.trim();
  return (
    <section className="account-profile card" aria-label="مشخصات شما" data-testid="account-profile-card">
      <Avatar profile={profile} size="lg" testId="account-avatar" />
      <div className="account-profile__id">
        {fullName && <p className="account-profile__name">{fullName}</p>}
        {/* Usernames start with "@", which would jump to the end in right-to-left text. */}
        <p className="account-profile__username">
          <bdi data-testid="account-username">{profile.username}</bdi>
        </p>
      </div>
      <dl className="account-profile__stats">
        <div className="account-profile__stat">
          <dt>سفارش‌ها</dt>
          <dd data-testid="account-stat-orders">{profile.orders_count}</dd>
        </div>
        <div className="account-profile__stat">
          <dt>تکمیل‌شده</dt>
          <dd data-testid="account-stat-completed">{profile.completed_orders_count}</dd>
        </div>
      </dl>
    </section>
  );
}

/** Sidebar menu on desktop, a row of scrollable pills on phones. */
function AccountMenu({ pathname }) {
  const listRef = useRef(null);

  // On phones the row scrolls sideways: keep the current page's pill in view.
  useEffect(() => {
    const list = listRef.current;
    const active = list?.querySelector('[aria-current="page"]');
    if (list && active && list.scrollWidth > list.clientWidth) {
      active.scrollIntoView({ inline: "center", block: "nearest" });
    }
  }, [pathname]);

  return (
    <nav className="account-menu" aria-label="منوی حساب کاربری" data-testid="account-menu">
      <ul className="account-menu__list" ref={listRef} data-allow-overflow>
        {MENU.map(({ to, label, icon: Icon, end, testId }) => (
          <li key={to}>
            <NavLink to={to} end={end} className="account-menu__link" data-testid={`account-menu-${testId}`}>
              <Icon size={20} aria-hidden="true" />
              <span>{label}</span>
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}

function breadcrumbFor(pathname) {
  const current = MENU.find((item) => !item.end && pathname.startsWith(item.to));
  const root = { label: "حساب کاربری", to: "/account" };
  return current ? [root, { label: current.label }] : [{ label: root.label }];
}

/** Frame of the customer area: profile card and menu on one side, the page on the other. */
export default function AccountLayout() {
  const { pathname } = useLocation();
  const state = useApi(customerApi.profile);
  const profile = state.data;

  return (
    <main className="page account-page" data-testid="account-layout">
      <div className="container">
        <Breadcrumb items={breadcrumbFor(pathname)} />
        {state.loading && !profile ? (
          <AccountSkeleton />
        ) : state.error ? (
          <LoadError error={state.error} onRetry={state.reload} />
        ) : (
          <div className="account-layout">
            <aside className="account-aside">
              <ProfileCard profile={profile} />
              <AccountMenu pathname={pathname} />
            </aside>
            <div className="account-main">
              <Outlet context={{ profile, reloadProfile: state.reload }} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
