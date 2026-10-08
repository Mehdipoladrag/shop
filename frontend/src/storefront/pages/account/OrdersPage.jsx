import { Link, useSearchParams } from "react-router-dom";
import { CalendarDays, ChevronLeft, PackageOpen } from "lucide-react";
import { customerApi } from "../../api/endpoints";
import { useApi } from "../../../shared/useApi";
import { formatJalaliDate, formatPrice, toRelativeUrl } from "../../format";
import Pagination from "../../components/Pagination";
import { EmptyState, LoadError } from "../../components/States";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import { CardsSkeleton } from "./AccountSkeleton";
import PageHead from "./PageHead";
import StatusBadge from "./StatusBadge";
import "../account.css";

const ORDERS_PAGE_SIZE = 10;
const MAX_THUMBNAILS = 4;

function OrderCard({ order }) {
  // Items whose product was deleted have no page to link to, so they get no thumbnail.
  const linkable = order.items.filter((item) => item.product_slug);
  const shown = linkable.slice(0, MAX_THUMBNAILS);
  const hidden = linkable.length - shown.length;
  const unitCount = order.items.reduce((sum, item) => sum + Number(item.product_count || 0), 0);

  return (
    <article className="account-order card" data-testid="order-card" data-order-id={order.id}>
      <header className="account-order__head">
        <div className="account-order__meta">
          <h2 className="account-order__title">
            کد سفارش <bdi data-testid="order-card-id">{order.id}</bdi>
          </h2>
          <span className="account-order__date">
            <CalendarDays size={16} aria-hidden="true" />
            <bdi dir="ltr">{formatJalaliDate(order.order_date, { withTime: true })}</bdi>
          </span>
        </div>
        <StatusBadge order={order} testId="order-card-status" />
      </header>

      <div className="account-order__body">
        {linkable.length > 0 && (
          <ul className="account-order__thumbs">
            {shown.map((item) => (
              <li key={item.id}>
                <Link to={`/products/${item.product_slug}`} className="account-order__thumb">
                  <img src={toRelativeUrl(item.product_pic)} alt={item.product_name} width="56" height="56" loading="lazy" />
                </Link>
              </li>
            ))}
            {hidden > 0 && (
              <li className="account-order__more" aria-label={`و ${hidden} کالای دیگر`}>
                <span aria-hidden="true">+{hidden}</span>
              </li>
            )}
          </ul>
        )}
        <dl className="account-order__facts">
          <div>
            <dt>تعداد کالا</dt>
            <dd>{unitCount}</dd>
          </div>
          <div>
            <dt>مجموع سبد</dt>
            <dd className="account-order__total">
              {formatPrice(order.total_cost)} <small>تومان</small>
            </dd>
          </div>
        </dl>
        <Link to={`/account/orders/${order.id}`} className="btn btn--secondary btn--sm account-order__link" data-testid="order-card-link">
          مشاهده وضعیت سفارش
          <ChevronLeft size={16} aria-hidden="true" />
        </Link>
      </div>
    </article>
  );
}

export default function OrdersPage() {
  useDocumentTitle("سفارشات من");
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number(searchParams.get("page")) || 1;
  const state = useApi(() => customerApi.orders(page), [page]);

  let content;
  if (state.loading && !state.data) {
    content = <CardsSkeleton count={3} height="account-skeleton__order" />;
  } else if (state.error) {
    content = <LoadError error={state.error} onRetry={state.reload} />;
  } else if (state.data.results.length === 0) {
    content = (
      <div data-testid="orders-empty">
        <EmptyState icon={PackageOpen} title="هنوز سفارشی ثبت نکرده‌اید." text="بعد از ثبت اولین سفارش، آن را اینجا پیگیری می‌کنید.">
          <Link to="/products" className="btn btn--primary">
            رفتن به فروشگاه
          </Link>
        </EmptyState>
      </div>
    );
  } else {
    const { results, count } = state.data;
    content = (
      <>
        <div className="account-cards" data-testid="orders-list">
          {results.map((order) => (
            <OrderCard order={order} key={order.id} />
          ))}
        </div>
        <Pagination page={page} pageCount={Math.ceil(count / ORDERS_PAGE_SIZE)} onChange={(target) => setSearchParams({ page: String(target) })} />
      </>
    );
  }

  return (
    <div className="account-page-body">
      <PageHead title="سفارشات من" />
      {content}
    </div>
  );
}
