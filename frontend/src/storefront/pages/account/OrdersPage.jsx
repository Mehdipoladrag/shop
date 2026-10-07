import { Link, useSearchParams } from "react-router-dom";
import { customerApi } from "../../api/endpoints";
import { useApi } from "../../../shared/useApi";
import { formatJalaliDate, formatPrice, toRelativeUrl } from "../../format";
import Pagination from "../../components/Pagination";
import { AsyncContent } from "../../components/States";

const ORDERS_PAGE_SIZE = 10;

export const STATUS_ICONS = {
  pending: "fa-clock",
  completed: "fa-check-circle",
  failed: "fa-times-circle",
};

export function StatusBadge({ order }) {
  return (
    <span className={`status-badge status-badge--${order.status}`}>
      <i className={`fa ${STATUS_ICONS[order.status]}`} aria-hidden="true" /> {order.status_label}
    </span>
  );
}

export default function OrdersPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number(searchParams.get("page")) || 1;
  const state = useApi(() => customerApi.orders(page), [page]);

  return (
    <div className="row">
      <div className="col-lg-12">
        <header className="card-header">
          <h3 className="card-title">
            <span>سفارشات من</span>
          </h3>
        </header>
        <AsyncContent state={state}>
          {({ results, count }) => (
            <>
              {results.length === 0 && (
                <div className="content-section default text-center">
                  <p>هنوز سفارشی ثبت نکرده‌اید.</p>
                  <Link to="/products" className="btn btn-main-masai">
                    رفتن به فروشگاه
                  </Link>
                </div>
              )}
              {results.map((order) => (
                <div className="content-section default" key={order.id}>
                  <div className="row">
                    <div className="col-md-12 col-sm-12 order_delivered_sec">
                      <div className="profile-recent-fav-row">
                        <div className="col-12">
                          <h4 className="profile-recent-fav-name">
                            <StatusBadge order={order} />
                          </h4>
                          <ul>
                            <li>{formatJalaliDate(order.order_date, { withTime: true })}</li>
                            <li>
                              کد سفارش <b>{order.id}</b>
                            </li>
                            <li>
                              مجموع سبد <b>{formatPrice(order.total_cost)} تومان</b>
                            </li>
                          </ul>
                        </div>
                        <div className="col-12">
                          <div className="row">
                            {order.items.map((item) => (
                              <Link to={`/products/${item.product_slug}`} key={item.id}>
                                <img src={toRelativeUrl(item.product_pic)} alt={item.product_name} />
                              </Link>
                            ))}
                          </div>
                        </div>
                        <div className="col-12 text-left">
                          <Link to={`/account/orders/${order.id}`} className="btn btn-main-masai">
                            مشاهده وضعیت سفارش
                          </Link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              <Pagination
                page={page}
                pageCount={Math.ceil(count / ORDERS_PAGE_SIZE)}
                onChange={(target) => setSearchParams({ page: String(target) })}
              />
            </>
          )}
        </AsyncContent>
      </div>
    </div>
  );
}
