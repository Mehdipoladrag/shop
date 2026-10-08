import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ShoppingCart } from "lucide-react";
import { useCart } from "../cart/CartContext";
import { useFlash } from "../components/Flash";
import { EmptyState, LoadError } from "../components/States";
import { useDocumentTitle } from "../components/useDocumentTitle";
import CartItem from "./cart/CartItem";
import CartSkeleton from "./cart/CartSkeleton";
import CartSteps from "./cart/CartSteps";
import CartSummary from "./cart/CartSummary";
import { UPDATE_FAILED_MESSAGE } from "./cart/constants";
import "./cart.css";

const REMOVED_MESSAGE = "کالا از سبد خرید حذف شد";

/** What the customer saves through discounts: the old price minus the price charged, for every piece. */
function discountSaving(items) {
  return items.reduce((sum, item) => {
    const hasOffer = Number(item.product.offer) > 0;
    return hasOffer ? sum + (Number(item.product.price) - Number(item.unit_price)) * item.product_count : sum;
  }, 0);
}

function CartList({ cart, pending, onChangeCount, onRemove }) {
  return (
    <section className="cart-layout" aria-labelledby="cart-items-title">
      <div>
        <h2 className="visually-hidden" id="cart-items-title">
          کالاهای سبد خرید
        </h2>
        <ul className="cart-list" data-testid="cart-items">
          {cart.items.map((item) => (
            <CartItem
              key={item.product.id}
              item={item}
              pending={pending.has(item.product.id)}
              onChangeCount={onChangeCount}
              onRemove={onRemove}
            />
          ))}
        </ul>
      </div>
      <CartSummary cart={cart} saving={discountSaving(cart.items)} />
    </section>
  );
}

export default function CartPage() {
  useDocumentTitle("سبد خرید");
  const { cart, loaded, reload, setItemCount, removeItem } = useCart();
  const flash = useFlash();
  const [refresh, setRefresh] = useState({ failed: null });
  const [pending, setPending] = useState(() => new Set());

  // The cart is fetched again on every visit, so stock and prices are current and a failed first load can be retried.
  const refreshCart = useCallback(() => {
    setRefresh({ failed: null });
    return reload().catch((error) => setRefresh({ failed: error }));
  }, [reload]);

  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  async function run(productId, action, doneMessage) {
    setPending((current) => new Set(current).add(productId));
    try {
      await action();
      if (doneMessage) flash.show(doneMessage);
    } catch {
      flash.show(UPDATE_FAILED_MESSAGE, "error");
    } finally {
      setPending((current) => {
        const next = new Set(current);
        next.delete(productId);
        return next;
      });
    }
  }

  const changeCount = (productId, count) => run(productId, () => setItemCount(productId, count));
  const remove = (productId) => run(productId, () => removeItem(productId), REMOVED_MESSAGE);

  const hasItems = cart.items.length > 0;

  let body;
  if (!loaded) {
    body = (
      <div className="container">
        <CartSkeleton />
      </div>
    );
  } else if (!hasItems && refresh.failed) {
    body = <LoadError error={refresh.failed} onRetry={refreshCart} />;
  } else if (!hasItems) {
    body = (
      <EmptyState icon={ShoppingCart} title="سبد خرید شما در حال حاضر خالی است." text="محصولات مورد علاقه‌تان را پیدا کنید و به سبد اضافه کنید.">
        <Link to="/products" className="btn btn--primary" data-testid="cart-empty-shop">
          مشاهده محصولات
        </Link>
        <Link to="/" className="btn btn--secondary" data-testid="cart-empty-home">
          صفحه نخست
        </Link>
      </EmptyState>
    );
  } else {
    body = (
      <div className="container">
        <CartList cart={cart} pending={pending} onChangeCount={changeCount} onRemove={remove} />
      </div>
    );
  }

  return (
    <main className="page cart-view" data-testid="cart-page">
      <div className="container">
        <header className="cart-head">
          <h1 className="cart-head__title">
            سبد خرید
            {loaded && hasItems && (
              <span className="badge cart-head__count" data-testid="cart-head-count">
                {cart.total_count} کالا
              </span>
            )}
          </h1>
          {(!loaded || hasItems) && <CartSteps current={1} />}
        </header>
      </div>
      {body}
    </main>
  );
}
