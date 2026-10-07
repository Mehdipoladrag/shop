import { Link, useParams } from "react-router-dom";
import { customerApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { useApi } from "../../shared/useApi";
import { staticUrl } from "../config";
import { AsyncContent, NotFound } from "../components/States";
import { OrderSteps } from "./CheckoutPage";

export default function OrderSuccessPage() {
  const { id } = useParams();
  // Only an order of the logged in customer may be confirmed; anything else is a 404.
  const state = useApi(() => customerApi.order(id), [id]);

  if (state.error instanceof ApiError && state.error.status === 404) return <NotFound />;

  return (
    <AsyncContent state={state}>
      {(order) => (
        <main className="cart-page default">
          <div className="container">
            <div className="row">
              <div className="col-12 text-center">
                <OrderSteps step={2} />
              </div>
              <div className="cart default">
                <div className="container text-center cart_empty">
                  <img src={staticUrl("img/successful-cart.png")} alt="" />
                  <h6>تبریک، سفارش با موفقیت دریافت شد</h6>
                  <p>این اطمینان را به شما می‌دهیم که بزودی محصول خریداری شده شما را ارسال خواهیم کرد.</p>
                  <p>
                    کد سفارش: <b>{order.id}</b>
                  </p>
                  <Link to={`/account/orders/${order.id}`} className="btn btn-main-masai">
                    مشاهده وضعیت سفارش
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </main>
      )}
    </AsyncContent>
  );
}
