import { Link, useParams } from "react-router-dom";
import { ArrowRight, CalendarDays, Check, Clock, PackageSearch, X } from "lucide-react";
import { customerApi } from "../../api/endpoints";
import { ApiError } from "../../api/client";
import { useApi } from "../../../shared/useApi";
import { formatJalaliDate, formatPrice, toRelativeUrl } from "../../format";
import { EmptyState, LoadError } from "../../components/States";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import { CardsSkeleton } from "./AccountSkeleton";
import PageHead from "./PageHead";
import StatusBadge from "./StatusBadge";
import "../account.css";

const CURRENT = "current";

/** The three steps of an order: placed, waiting for payment, then completed or failed. */
function timelineSteps(status) {
  return [
    { key: "placed", label: "ثبت سفارش", state: "done", icon: Check },
    { key: "pending", label: "انتظار", state: status === "pending" ? "current" : "done", icon: Clock },
    status === "failed"
      ? { key: "failed", label: "ناموفق", state: "failed", icon: X }
      : { key: "completed", label: "تکمیل شده", state: status === "completed" ? "done" : "upcoming", icon: Check },
  ];
}

function Timeline({ status }) {
  return (
    <ol className="account-timeline" aria-label="مراحل سفارش" data-testid="order-status-timeline">
      {timelineSteps(status).map(({ key, label, state, icon: Icon }) => (
        <li
          key={key}
          className={`account-timeline__step account-timeline__step--${state}`}
          aria-current={state === "current" || state === "failed" ? "step" : undefined}
          data-step={key}
        >
          <span className="account-timeline__marker">{state !== "upcoming" && <Icon size={18} aria-hidden="true" />}</span>
          <span className="account-timeline__label">{label}</span>
        </li>
      ))}
    </ol>
  );
}

function OrderDetails({ order }) {
  const unitPrice = (item) => Number(item.discounted_price ?? item.product_price);
  const listTotal = order.items.reduce((sum, item) => sum + Number(item.product_price) * item.product_count, 0);
  const savings = Math.round(listTotal - Number(order.total_cost));
  const unitCount = order.items.reduce((sum, item) => sum + Number(item.product_count || 0), 0);

  return (
    <>
      <section className="card card--pad account-summary" aria-label="خلاصه سفارش">
        <div className="account-summary__top">
          <div className="account-summary__ids">
            <p className="account-summary__number">
              کد سفارش <bdi data-testid="order-status-id">{order.id}</bdi>
            </p>
            <span className="account-order__date">
              <CalendarDays size={16} aria-hidden="true" />
              <bdi dir="ltr" data-testid="order-status-date">
                {formatJalaliDate(order.order_date, { withTime: true })}
              </bdi>
            </span>
          </div>
          <StatusBadge order={order} testId="order-status-badge" />
        </div>
        <Timeline status={order.status} />
      </section>

      <section className="card card--pad" aria-labelledby="order-items-title">
        <h2 className="card__title" id="order-items-title">
          کالاهای سفارش
        </h2>
        <ul className="account-lines" data-testid="order-status-items">
          {order.items.map((item) => {
            const discounted = unitPrice(item) < Number(item.product_price);
            return (
              <li className="account-line" key={item.id} data-testid="order-status-item">
                <img className="account-line__pic" src={toRelativeUrl(item.product_pic)} alt="" width="64" height="64" loading="lazy" />
                <div className="account-line__info">
                  {item.product_slug ? (
                    <Link to={`/products/${item.product_slug}`} className="account-line__name">
                      {item.product_name}
                    </Link>
                  ) : (
                    <span className="account-line__name account-line__name--gone">محصول حذف شده</span>
                  )}
                  <p className="account-line__meta">
                    {item.product_count} × {formatPrice(unitPrice(item))} تومان
                    {discounted && <del>{formatPrice(item.product_price)}</del>}
                  </p>
                </div>
                <p className="account-line__total">
                  {formatPrice(item.product_cost)} <small>تومان</small>
                </p>
              </li>
            );
          })}
        </ul>
        <dl className="account-totals" data-testid="order-status-totals">
          <div>
            <dt>تعداد کالا</dt>
            <dd>{unitCount}</dd>
          </div>
          {savings > 0 && (
            <>
              <div>
                <dt>جمع کالاها</dt>
                <dd>{formatPrice(listTotal)} تومان</dd>
              </div>
              <div className="account-totals__saving">
                <dt>تخفیف</dt>
                <dd>{formatPrice(savings)} تومان</dd>
              </div>
            </>
          )}
          <div className="account-totals__final">
            <dt>مجموع سبد</dt>
            <dd data-testid="order-status-total">
              {formatPrice(order.total_cost)} <small>تومان</small>
            </dd>
          </div>
        </dl>
      </section>
    </>
  );
}

export default function OrderStatusPage() {
  useDocumentTitle("وضعیت سفارش");
  const { id } = useParams();
  // `current` is the most recent order of the customer.
  const state = useApi(() => (id === CURRENT ? customerApi.latestOrder() : customerApi.order(id)), [id]);

  let content;
  if (state.loading && !state.data) {
    content = <CardsSkeleton count={2} height="account-skeleton__order" />;
  } else if (state.error instanceof ApiError && state.error.status === 404) {
    content = (
      <div data-testid="order-status-empty">
        <EmptyState icon={PackageSearch} title={id === CURRENT ? "هنوز سفارشی ثبت نکرده‌اید." : "این سفارش پیدا نشد."}>
          <Link to="/account/orders" className="btn btn--primary">
            لیست سفارشات
          </Link>
          {id === CURRENT && (
            <Link to="/products" className="btn btn--secondary">
              رفتن به فروشگاه
            </Link>
          )}
        </EmptyState>
      </div>
    );
  } else if (state.error) {
    content = <LoadError error={state.error} onRetry={state.reload} />;
  } else {
    content = <OrderDetails order={state.data} />;
  }

  return (
    <div className="account-page-body" data-testid="order-status-page">
      <PageHead title="وضعیت سفارش">
        <Link to="/account/orders" className="btn btn--secondary" data-testid="order-status-back">
          <ArrowRight size={18} aria-hidden="true" />
          بازگشت به لیست سفارشات
        </Link>
      </PageHead>
      {content}
    </div>
  );
}
