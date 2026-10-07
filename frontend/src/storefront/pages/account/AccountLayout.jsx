import { NavLink, Outlet, useLocation } from "react-router-dom";
import { customerApi } from "../../api/endpoints";
import { useApi } from "../../../shared/useApi";
import { toRelativeUrl } from "../../format";
import { AsyncContent } from "../../components/States";

const MENU = [
  { to: "/account/orders", label: "لیست سفارشات من", icon: "fa-cart-arrow-down" },
  { to: "/account/address", label: "آدرس ها", icon: "fa-map" },
  { to: "/account", label: "پروفایل", icon: "fa-user-large", end: true },
  { to: "/account/edit", label: "ویرایش اطلاعات", icon: "fa-pencil" },
  { to: "/account/password", label: "امنیت و تغییر رمز", icon: "fa-shield" },
];

function ProfileCard({ profile }) {
  return (
    <div className="profile-card-1">
      <div className="img">{profile.customer_image && <img src={toRelativeUrl(profile.customer_image)} alt="" />}</div>
      <div className="mid-section">
        <div className="name">
          {/* Usernames start with "@", which would jump to the end in right-to-left text. */}
          <bdi>{profile.username}</bdi>
        </div>
        <div className="description">
          <a href="#top" className="btn btn-main-masai" onClick={(event) => event.preventDefault()}>
            افزایش موجودی
          </a>
          <a href="#top" className="btn btn-second-masai" onClick={(event) => event.preventDefault()}>
            مسای کلاب
          </a>
        </div>
        <div className="line" />
        <div className="stats">
          <div className="stat">
            {profile.orders_count}
            <div className="subtext">سفارش‌ها</div>
          </div>
          <div className="stat">
            {profile.completed_orders_count}
            <div className="subtext">تحویل داده</div>
          </div>
        </div>
      </div>
    </div>
  );
}

/** Frame of the customer area: the page on one side, profile card and menu on the other. */
export default function AccountLayout() {
  const { pathname } = useLocation();
  const state = useApi(customerApi.profile);
  const listing = pathname.startsWith("/account/orders") || pathname === "/account/address";

  return (
    <main className={`${listing ? "order-delivered" : "profile-user-page"} default space-top-30`}>
      <div className="container">
        <AsyncContent state={state}>
          {(profile) => (
            <div className="row">
              <div className="col-xl-9 col-lg-8 col-md-12 order-2">
                <Outlet context={{ profile, reloadProfile: state.reload }} />
              </div>
              <div className="profile-page-aside col-xl-3 col-lg-4 col-md-6 center-section order-1">
                <ProfileCard profile={profile} />
                <div className="profile-menu">
                  <ul className="profile-menu-items">
                    {MENU.map((item) => (
                      <li key={item.to}>
                        <NavLink to={item.to} end={item.end} className="dropdown-item">
                          <i className={`fa ${item.icon} colormain`} aria-hidden="true" /> {item.label}
                        </NavLink>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </AsyncContent>
      </div>
    </main>
  );
}
