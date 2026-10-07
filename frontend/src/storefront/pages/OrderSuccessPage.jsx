import { Link, useParams } from "react-router-dom";
import { staticUrl } from "../config";
import { OrderSteps } from "./CheckoutPage";

export default function OrderSuccessPage() {
  const { id } = useParams();

  return (
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
                کد سفارش: <b>{id}</b>
              </p>
              <Link to={`/account/orders/${id}`} className="btn btn-main-masai">
                مشاهده وضعیت سفارش
              </Link>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
