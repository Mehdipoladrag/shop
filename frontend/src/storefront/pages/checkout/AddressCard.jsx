import { Link } from "react-router-dom";
import { MapPin, TriangleAlert } from "lucide-react";
import "../checkout.css";

/**
 * Delivery address of the order. `profile` is the customer's saved address
 * (null while it loads or when it could not be loaded); `complete` comes from
 * the checkout summary and decides between the address and the warning.
 */
export default function AddressCard({ complete, profile, loading }) {
  const name = `${profile?.first_name ?? ""} ${profile?.last_name ?? ""}`.trim();

  return (
    <section className="card card--pad checkout-address" aria-labelledby="checkout-address-title" data-testid="checkout-address">
      <div className="checkout-card-head">
        <h2 className="card__title" id="checkout-address-title">
          <MapPin size={20} aria-hidden="true" />
          آدرس تحویل
        </h2>
        {complete && (
          <Link to="/account/address" className="btn btn--ghost btn--sm" data-testid="checkout-address-edit">
            ویرایش
          </Link>
        )}
      </div>

      {!complete ? (
        <div className="checkout-warning" data-testid="checkout-address-warning">
          <TriangleAlert size={22} aria-hidden="true" />
          <p>آدرس و اطلاعات تحویل شما کامل نیست.</p>
          <Link to="/account/address" className="btn btn--primary btn--sm" data-testid="checkout-address-link">
            تکمیل آدرس
          </Link>
        </div>
      ) : profile ? (
        <div className="checkout-address__body">
          {name && <p className="checkout-address__name">{name}</p>}
          <p>{profile.address}</p>
          <ul className="checkout-address__meta">
            {profile.city && <li>{profile.city}</li>}
            {profile.street && <li>{profile.street}</li>}
            {profile.zipcode && (
              <li>
                کد پستی: <bdi dir="ltr">{profile.zipcode}</bdi>
              </li>
            )}
            {profile.mobile && (
              <li>
                موبایل: <bdi dir="ltr">{profile.mobile}</bdi>
              </li>
            )}
          </ul>
        </div>
      ) : loading ? (
        <div role="status" aria-label="در حال بارگذاری آدرس">
          <span className="skeleton checkout-address__skeleton" />
        </div>
      ) : (
        <p className="text-muted">آدرس تحویل شما ثبت شده است.</p>
      )}
    </section>
  );
}
