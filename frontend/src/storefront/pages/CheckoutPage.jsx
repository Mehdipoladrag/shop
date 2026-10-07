import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { checkoutApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { useCart } from "../cart/CartContext";
import { staticUrl } from "../config";
import { formatPrice } from "../format";
import { useFlash } from "../components/Flash";
import { AsyncContent } from "../components/States";

const PAYMENT_PLANS = [
  { id: "pay1", icon: "png-10.png", title: "پرداخت اینترنتی", text: "از طریق کارت های عضو شتاب" },
  { id: "pay2", icon: "png-11.png", title: "پرداخت در محل", text: "با کارت بانکی" },
  { id: "pay3", icon: "png-9.png", title: "خرید اقساطی", text: "با استفاده از مسای پی", disabled: true },
  { id: "pay4", icon: "png-8.png", title: "پرداخت اعتباری", text: "الان بخر بعدا پرداخت کن", disabled: true },
];

export function OrderSteps({ step }) {
  const classFor = (index) => (index <= step ? "active" : undefined);
  return (
    <ul className="order-steps">
      <li className={classFor(0)}>
        <Link to="/cart" className={classFor(0)}>
          <span>سبدخرید</span>
        </Link>
      </li>
      <li className={classFor(1)}>
        <a href="#top" className={step >= 1 ? "active active2" : undefined} onClick={(event) => event.preventDefault()}>
          <span>روش پرداخت</span>
        </a>
      </li>
      <li className={classFor(2)}>
        <a href="#top" className={step >= 2 ? "active active3" : undefined} onClick={(event) => event.preventDefault()}>
          <span>پایان خرید</span>
        </a>
      </li>
    </ul>
  );
}

function EmptyCheckout() {
  return (
    <main className="cart default">
      <div className="container text-center cart_empty">
        <img src={staticUrl("img/empty-cart.png")} alt="" />
        <h6>سبد خرید شما در حال حاضر خالی است.</h6>
        <Link to="/" className="btn btn-main-masai">
          صفحه نخست
        </Link>
      </div>
    </main>
  );
}

function CheckoutContent({ summary }) {
  const navigate = useNavigate();
  const flash = useFlash();
  const { reload: reloadCart } = useCart();
  const [plan, setPlan] = useState(PAYMENT_PLANS[0].id);
  const [placing, setPlacing] = useState(false);
  const { cart, profile_complete: profileComplete } = summary;

  async function handlePay(event) {
    event.preventDefault();
    setPlacing(true);
    try {
      const order = await checkoutApi.placeOrder();
      await reloadCart();
      navigate(`/checkout/success/${order.id}`, { replace: true });
    } catch (error) {
      flash.show(error.message, "error");
      setPlacing(false);
    }
  }

  if (cart.items.length === 0) return <EmptyCheckout />;

  return (
    <main className="cart-page default">
      <div className="container">
        <div className="row">
          <div className="col-12 text-center">
            <OrderSteps step={1} />
          </div>
          <div className="cart-page-content col-xl-12 col-lg-12 col-md-12">
            <header className="card-header">
              <h3 className="card-title">
                <span>انتخاب روش پرداخت</span>
              </h3>
            </header>
            {!profileComplete && (
              <p className="txt_note">
                <i className="fa fa-info" aria-hidden="true" /> آدرس و اطلاعات تحویل شما کامل نیست.{" "}
                <Link to="/account/address">تکمیل آدرس</Link>
              </p>
            )}
            <div className="row cart_details">
              <div className="cart-page-content col-xl-8 col-lg-7 col-md-7">
                <div className="plans">
                  {PAYMENT_PLANS.map((item) => (
                    <label className="plan basic-plan" htmlFor={item.id} key={item.id}>
                      <input
                        type="radio"
                        name="plan"
                        id={item.id}
                        checked={plan === item.id}
                        disabled={item.disabled}
                        onChange={() => setPlan(item.id)}
                      />
                      <div className="plan-content">
                        <img loading="lazy" src={staticUrl(`img/ico/${item.icon}`)} alt="" />
                        <div className="plan-details">
                          <span>{item.title}</span>
                          <p>{item.text}</p>
                        </div>
                      </div>
                    </label>
                  ))}
                </div>
                <p className="txt_note">
                  <i className="fa fa-info" aria-hidden="true" /> پرداخت آنلاین هنوز فعال نشده است؛ سفارش شما ثبت می‌شود و در وضعیت «انتظار» می‌ماند.
                </p>
              </div>
              <div className="cart-page-aside col-xl-4 col-lg-5 col-md-5 divider_details">
                <table className="table table_details">
                  <tbody>
                    <tr>
                      <td>تعداد کالا:</td>
                      <td>{cart.total_count}</td>
                    </tr>
                    <tr>
                      <td>بسته‌بندی و ارسال:</td>
                      <td>وابسته به نوع ارسال</td>
                    </tr>
                    <tr className="all">
                      <td>قیمت قابل پرداخت:</td>
                      <td>
                        {formatPrice(cart.total_price)} <span>تومان</span>
                      </td>
                    </tr>
                    <tr>
                      <td colSpan="2">
                        <button type="button" className="btn btn-main-masai big_btn" disabled={placing} onClick={handlePay}>
                          {placing ? "در حال ثبت سفارش…" : "پرداخت"}
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function CheckoutPage() {
  const state = useApi(checkoutApi.summary);
  return <AsyncContent state={state}>{(summary) => <CheckoutContent summary={summary} />}</AsyncContent>;
}
