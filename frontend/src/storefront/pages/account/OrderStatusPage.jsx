import { Link, useParams } from "react-router-dom";
import { customerApi } from "../../api/endpoints";
import { ApiError } from "../../api/client";
import { useApi } from "../../../shared/useApi";
import { formatJalaliDate, formatPrice, toRelativeUrl } from "../../format";
import { AsyncContent } from "../../components/States";
import { StatusBadge } from "./OrdersPage";

const CURRENT = "current";

export default function OrderStatusPage() {
  const { id } = useParams();
  // `current` is the most recent order of the customer.
  const state = useApi(() => (id === CURRENT ? customerApi.latestOrder() : customerApi.order(id)), [id]);

  if (state.error instanceof ApiError && state.error.status === 404) {
    return (
      <div className="content-section default text-center">
        <p>{id === CURRENT ? "هنوز سفارشی ثبت نکرده‌اید." : "این سفارش پیدا نشد."}</p>
        <Link to="/account/orders" className="btn btn-main-masai">
          لیست سفارشات
        </Link>
      </div>
    );
  }

  return (
    <div className="row">
      <div className="col-lg-12">
        <header className="card-header">
          <h3 className="card-title">
            <span>وضعیت سفارش</span>
          </h3>
        </header>
        <AsyncContent state={state}>
          {(order) => (
            <div className="content-section default">
              <div className="row">
                <div className="col-12 order_delivered_sec">
                  <h4 className="profile-recent-fav-name">
                    <StatusBadge order={order} />
                  </h4>
                  <ul>
                    <li>
                      کد سفارش <b>{order.id}</b>
                    </li>
                    <li>{formatJalaliDate(order.order_date, { withTime: true })}</li>
                    <li>
                      مجموع سبد <b>{formatPrice(order.total_cost)} تومان</b>
                    </li>
                  </ul>
                </div>
                <div className="col-12">
                  <div className="table-responsive default">
                    <table className="table">
                      <thead>
                        <tr>
                          <th scope="col">محصول</th>
                          <th scope="col">قیمت واحد</th>
                          <th scope="col">تعداد</th>
                          <th scope="col">قیمت نهایی</th>
                        </tr>
                      </thead>
                      <tbody>
                        {order.items.map((item) => (
                          <tr className="cart_item" key={item.id}>
                            <td>
                              <img src={toRelativeUrl(item.product_pic)} alt="" />
                              <h3 className="cart_title">
                                {item.product_slug ? <Link to={`/products/${item.product_slug}`}>{item.product_name}</Link> : "محصول حذف شده"}
                              </h3>
                            </td>
                            <td>{formatPrice(item.discounted_price ?? item.product_price)} تومان</td>
                            <td>{item.product_count}</td>
                            <td className="price_alltd">{formatPrice(item.product_cost)} تومان</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
                <div className="col-12 text-left">
                  <Link to="/account/orders" className="btn btn-second-masai">
                    بازگشت به لیست سفارشات
                  </Link>
                </div>
              </div>
            </div>
          )}
        </AsyncContent>
      </div>
    </div>
  );
}
