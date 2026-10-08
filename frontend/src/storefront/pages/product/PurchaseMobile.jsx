import { useEffect } from "react";
import { Link } from "react-router-dom";
import Price from "../../components/Price";
import { AddToCart, DealTimer, DeliveryLine, QuantityRow, Reassurance, ViewCartLink } from "./PurchaseParts";

const BAR_BODY_CLASS = "product-has-bar";

/** Phones: everything of the purchase card except the price and the button, which live in the fixed bar. */
export function PurchaseOptions({ product, purchase }) {
  return (
    <section className="product-buy product-buy--options card" aria-label="گزینه‌های خرید" data-testid="product-buy">
      {!purchase.soldOut && <DealTimer product={product} />}
      {!purchase.soldOut && <DeliveryLine product={product} />}
      {!purchase.soldOut && <QuantityRow purchase={purchase} />}
      {purchase.soldOut && (
        <>
          <p className="product-buy__note" data-testid="product-sold-out">
            این محصول در حال حاضر ناموجود است.
          </p>
          <Link to={`/category/${product.category_slug}`} className="btn btn--secondary btn--block" data-testid="product-similar">
            مشاهده محصولات مشابه
          </Link>
        </>
      )}
      <ViewCartLink purchase={purchase} />
      <Reassurance />
    </section>
  );
}

/** Bar fixed to the bottom of the screen on phones with the price and the add button. */
export function PurchaseBar({ product, purchase }) {
  // The page and the footer get room at the bottom, and messages sit above the bar.
  useEffect(() => {
    document.body.classList.add(BAR_BODY_CLASS);
    return () => document.body.classList.remove(BAR_BODY_CLASS);
  }, []);

  return (
    <div className="product-bar" data-testid="product-bar">
      <div className="container product-bar__inner">
        <Price product={product} showBadge={false} />
        <AddToCart product={product} purchase={purchase} compact />
      </div>
    </div>
  );
}
