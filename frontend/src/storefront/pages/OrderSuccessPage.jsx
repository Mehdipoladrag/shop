import { Link, useParams } from "react-router-dom";
import { customerApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { useApi } from "../../shared/useApi";
import { formatJalaliDate, formatPrice } from "../format";
import { LoadError, NotFound } from "../components/States";
import { useDocumentTitle } from "../components/useDocumentTitle";
import StatusBadge from "./account/StatusBadge";
import CheckoutSkeleton from "./checkout/CheckoutSkeleton";
import CheckoutSteps from "./checkout/CheckoutSteps";
import "./checkout.css";

/** Large check mark in soft circles, drawn with SVG; the colors come from CSS tokens. */
function SuccessIllustration() {
  return (
    <svg className="checkout-art" viewBox="0 0 160 160" width="160" height="160" aria-hidden="true">
      <circle className="checkout-art__halo" cx="80" cy="80" r="76" />
      <circle className="checkout-art__disc" cx="80" cy="80" r="54" />
      <path className="checkout-art__check" d="M56 82l17 17 33-37" fill="none" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" />
      <circle className="checkout-art__dot checkout-art__dot--coral" cx="22" cy="46" r="5" />
      <circle className="checkout-art__dot checkout-art__dot--navy" cx="142" cy="38" r="4" />
      <circle className="checkout-art__dot checkout-art__dot--navy" cx="132" cy="128" r="6" />
      <circle className="checkout-art__dot checkout-art__dot--coral" cx="30" cy="124" r="3.5" />
      <rect className="checkout-art__dot checkout-art__dot--soft" x="112" y="14" width="9" height="9" rx="2" transform="rotate(20 116 18)" />
      <rect className="checkout-art__dot checkout-art__dot--soft" x="10" y="84" width="8" height="8" rx="2" transform="rotate(-18 14 88)" />
    </svg>
  );
}

export default function OrderSuccessPage() {
  useDocumentTitle("سفارش شما ثبت شد");
  const { id } = useParams();
  // Only an order of the logged in customer may be confirmed; anything else is a 404.
  const state = useApi(() => customerApi.order(id), [id]);

  if (state.error instanceof ApiError && state.error.status === 404) return <NotFound />;
  if (state.loading && !state.data) return <CheckoutSkeleton narrow />;
  if (state.error) {
    return (
      <main className="page checkout-page">
        <LoadError error={state.error} onRetry={state.reload} />
      </main>
    );
  }

  const order = state.data;
  return (
    <main className="page checkout-page" data-testid="order-success">
      <div className="container">
        <CheckoutSteps step={3} complete />
        <section className="card checkout-success">
          <SuccessIllustration />
          <h1 className="checkout-success__title">تبریک، سفارش با موفقیت دریافت شد</h1>
          <p className="checkout-success__text">سفارش شما ثبت شد. وضعیت آن را از حساب کاربری خود پیگیری کنید.</p>

          <dl className="checkout-success__facts">
            <div className="checkout-success__fact checkout-success__fact--id">
              <dt>کد سفارش</dt>
              <dd data-testid="order-success-id">{order.id}</dd>
            </div>
            <div className="checkout-success__fact">
              <dt>تاریخ ثبت</dt>
              <dd>
                <bdi dir="ltr">{formatJalaliDate(order.order_date, { withTime: true })}</bdi>
              </dd>
            </div>
            <div className="checkout-success__fact">
              <dt>مبلغ سفارش</dt>
              <dd>{formatPrice(order.total_cost)} تومان</dd>
            </div>
            <div className="checkout-success__fact">
              <dt>وضعیت</dt>
              <dd>
                <StatusBadge order={order} />
              </dd>
            </div>
          </dl>

          <div className="checkout-success__actions">
            <Link to={`/account/orders/${order.id}`} className="btn btn--primary btn--lg" data-testid="order-success-status-link">
              مشاهده وضعیت سفارش
            </Link>
            <Link to="/products" className="btn btn--secondary btn--lg" data-testid="order-success-shop-link">
              ادامه خرید
            </Link>
          </div>
        </section>
      </div>
    </main>
  );
}
