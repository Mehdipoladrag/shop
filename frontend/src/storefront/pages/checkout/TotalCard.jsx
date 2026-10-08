import { Link } from "react-router-dom";
import { ArrowLeft, Info } from "lucide-react";
import { formatPrice } from "../../format";
import SubmitButton from "../account/SubmitButton";
import { FormError } from "../../components/FormField";
import "../checkout.css";

/** Sticky total of the order with the button that places it. */
export default function TotalCard({ cart, placing, error, onPlace }) {
  // The price before offers, from the same data the cart page shows.
  const listTotal = cart.items.reduce((sum, item) => sum + Number(item.product.price) * item.product_count, 0);
  const savings = Math.round(listTotal - Number(cart.total_price));

  return (
    <section className="card card--pad checkout-total" aria-labelledby="checkout-total-title" data-testid="checkout-total">
      <h2 className="card__title" id="checkout-total-title">
        خلاصه سفارش
      </h2>
      <dl className="checkout-total__rows">
        <div>
          <dt>تعداد کالا:</dt>
          <dd>{cart.total_count}</dd>
        </div>
        {savings > 0 && (
          <>
            <div>
              <dt>جمع کالاها:</dt>
              <dd>{formatPrice(listTotal)} تومان</dd>
            </div>
            <div className="checkout-total__saving">
              <dt>تخفیف:</dt>
              <dd>{formatPrice(savings)} تومان</dd>
            </div>
          </>
        )}
        <div>
          <dt>بسته‌بندی و ارسال:</dt>
          <dd>وابسته به نوع ارسال</dd>
        </div>
        <div className="checkout-total__final">
          <dt>قیمت قابل پرداخت:</dt>
          <dd data-testid="checkout-total-price">
            {formatPrice(cart.total_price)} <small>تومان</small>
          </dd>
        </div>
      </dl>

      <FormError message={error} />
      <SubmitButton
        type="button"
        className="btn btn--accent btn--lg btn--block"
        loading={placing}
        loadingText="در حال ثبت سفارش…"
        onClick={onPlace}
        data-testid="checkout-submit"
      >
        ثبت سفارش و پرداخت
        <ArrowLeft size={18} aria-hidden="true" />
      </SubmitButton>
      <p className="checkout-total__note">
        <Info size={18} aria-hidden="true" />
        <span>پرداخت آنلاین هنوز فعال نشده است؛ سفارش شما ثبت می‌شود و در وضعیت «انتظار» می‌ماند.</span>
      </p>
      <Link to="/cart" className="btn btn--ghost btn--block">
        بازگشت به سبد خرید
      </Link>
    </section>
  );
}
