import { useRef } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Check, Truck } from "lucide-react";
import { formatPrice } from "../../format";
import { useStickyOffset } from "../product/useStickyOffset";
import { FREE_SHIPPING_THRESHOLD } from "./constants";

/** Progress toward free shipping, or the confirmation that the order already has it. */
function ShippingProgress({ total }) {
  const remaining = Math.max(0, FREE_SHIPPING_THRESHOLD - total);
  const percent = Math.min(100, Math.round((total / FREE_SHIPPING_THRESHOLD) * 100));
  const free = remaining === 0;

  return (
    <div className={`cart-shipping${free ? " is-free" : ""}`} data-testid="cart-shipping">
      <p className="cart-shipping__text">
        {free ? <Check size={18} aria-hidden="true" /> : <Truck size={18} aria-hidden="true" />}
        {free ? (
          <span>ارسال سفارش شما رایگان است.</span>
        ) : (
          <span>
            با <strong>{formatPrice(remaining)} تومان</strong> خرید بیشتر، ارسال رایگان می‌شود.
          </span>
        )}
      </p>
      <div
        className="cart-shipping__bar"
        role="progressbar"
        aria-label="پیشرفت تا ارسال رایگان"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={percent}
      >
        <span className="cart-shipping__fill" style={{ inlineSize: `${percent}%` }} />
      </div>
      <p className="cart-shipping__note">ارسال رایگان برای سفارش‌های بالای {formatPrice(FREE_SHIPPING_THRESHOLD)} تومان</p>
    </div>
  );
}

/** Totals of the cart with the way on to the checkout. */
export default function CartSummary({ cart, saving }) {
  const total = Number(cart.total_price) || 0;
  const free = total >= FREE_SHIPPING_THRESHOLD;
  const ref = useRef(null);
  useStickyOffset(ref, "--cart-sticky-top");

  return (
    <aside className="cart-summary card" ref={ref} aria-labelledby="cart-summary-title" data-testid="cart-summary">
      <h2 className="cart-summary__title" id="cart-summary-title">
        خلاصه سفارش
      </h2>

      <ShippingProgress total={total} />

      <dl className="cart-summary__rows">
        <div className="cart-summary__row">
          <dt>تعداد کالا</dt>
          <dd data-testid="cart-count">{cart.total_count}</dd>
        </div>
        {saving > 0 && (
          <div className="cart-summary__row cart-summary__row--saving">
            <dt>سود شما از تخفیف</dt>
            <dd data-testid="cart-saving">{formatPrice(saving)} تومان</dd>
          </div>
        )}
        <div className="cart-summary__row">
          <dt>بسته‌بندی و ارسال</dt>
          <dd>{free ? "رایگان" : "وابسته به نوع ارسال"}</dd>
        </div>
        <div className="cart-summary__row cart-summary__row--total">
          <dt>قیمت قابل پرداخت</dt>
          <dd data-testid="cart-total">
            <strong>{formatPrice(total)}</strong>
            <span>تومان</span>
          </dd>
        </div>
      </dl>

      <Link to="/checkout" className="btn btn--primary btn--lg btn--block" data-testid="cart-checkout">
        ادامه و ثبت سفارش
        <ArrowLeft size={20} aria-hidden="true" />
      </Link>
      <Link to="/products" className="btn btn--secondary btn--block" data-testid="cart-continue-shopping">
        ادامه خرید
      </Link>

      <p className="cart-summary__note">
        افزودن کالا به سبد خرید به معنی رزرو آن نیست؛ با توجه به محدودیت موجودی، سبد خود را ثبت و خرید را نهایی کنید.
      </p>
    </aside>
  );
}
