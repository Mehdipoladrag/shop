import { Link } from "react-router-dom";
import { Ban, Check, LoaderCircle, RotateCcw, ShieldCheck, ShoppingCart, Timer, Truck } from "lucide-react";
import Countdown from "../../components/Countdown";
import QuantityStepper from "../../components/QuantityStepper";
import { ADD_FAILED_MESSAGE } from "./usePurchase";
import { MAX_PER_ORDER } from "./details";

/** Countdown to the end of the discount; renders nothing for products without an offer. */
export function DealTimer({ product }) {
  if (!(Number(product.offer) > 0)) return null;
  return (
    <div className="product-buy__deal" data-testid="product-countdown">
      <p className="product-buy__deal-title">
        <Timer size={18} aria-hidden="true" />
        پایان تخفیف
      </p>
      <Countdown tone="dark" />
    </div>
  );
}

export function DeliveryLine({ product }) {
  const days = Number(product.time_send);
  if (!(days > 0)) return null;
  return (
    <p className="product-buy__delivery" data-testid="product-delivery">
      <Truck size={20} aria-hidden="true" />
      <span>
        زمان ارسال: <strong>{days} روز</strong>
      </span>
    </p>
  );
}

export function QuantityRow({ purchase }) {
  const { quantity, setQuantity, maxQuantity, stock } = purchase;
  return (
    <div className="product-buy__quantity" data-testid="product-quantity">
      <span className="product-buy__quantity-label" aria-hidden="true">
        تعداد
      </span>
      <QuantityStepper value={quantity} max={maxQuantity} onChange={setQuantity} />
      {stock < MAX_PER_ORDER && <span className="product-buy__quantity-hint">حداکثر {stock} عدد</span>}
    </div>
  );
}

export function Reassurance() {
  return (
    <ul className="product-buy__promises" data-testid="product-promises">
      <li>
        <ShieldCheck size={20} aria-hidden="true" />
        ضمانت اصالت کالا
      </li>
      <li>
        <RotateCcw size={20} aria-hidden="true" />7 روز فرصت بازگشت
      </li>
    </ul>
  );
}

/** "View cart" shortcut that appears after the product was added at least once. */
export function ViewCartLink({ purchase }) {
  if (!purchase.hasAdded) return null;
  return (
    <Link to="/cart" className="product-buy__cart-link" data-testid="product-view-cart">
      مشاهده سبد خرید
    </Link>
  );
}

/**
 * The big add-to-cart button with its loading and success states, or the
 * disabled "ناموجود" button for a sold out product. `compact` is the button of the
 * bar fixed to the bottom of small screens (no extra lines under it).
 */
export function AddToCart({ product, purchase, compact = false }) {
  const { soldOut, status, add } = purchase;

  if (soldOut) {
    return (
      <div className="product-buy__add">
        <button type="button" className="btn btn--secondary btn--lg btn--block product-buy__button is-sold-out" disabled data-testid="product-add-to-cart">
          <Ban size={20} aria-hidden="true" />
          ناموجود
        </button>
        {!compact && (
          <>
            <p className="product-buy__note" data-testid="product-sold-out">
              این محصول در حال حاضر ناموجود است.
            </p>
            <Link to={`/category/${product.category_slug}`} className="btn btn--secondary btn--block" data-testid="product-similar">
              مشاهده محصولات مشابه
            </Link>
          </>
        )}
      </div>
    );
  }

  const saving = status === "saving";
  const added = status === "added";
  let icon = <ShoppingCart size={20} aria-hidden="true" />;
  let label = "افزودن به سبد خرید";
  if (saving) {
    icon = <LoaderCircle size={20} className="product-buy__spinner" aria-hidden="true" />;
    label = "در حال افزودن...";
  } else if (added) {
    icon = <Check size={20} aria-hidden="true" />;
    label = "افزوده شد";
  }

  return (
    <div className="product-buy__add">
      <button
        type="button"
        className={`btn btn--accent btn--lg btn--block product-buy__button${added ? " is-added" : ""}`}
        disabled={saving}
        aria-busy={saving}
        onClick={add}
        data-testid="product-add-to-cart"
      >
        {icon}
        <span>{label}</span>
      </button>
      {!compact && status === "error" && (
        <p className="product-buy__error" role="alert" data-testid="product-add-error">
          {ADD_FAILED_MESSAGE}
        </p>
      )}
      {!compact && <ViewCartLink purchase={purchase} />}
    </div>
  );
}
