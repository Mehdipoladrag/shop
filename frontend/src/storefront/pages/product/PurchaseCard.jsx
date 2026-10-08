import { useRef } from "react";
import Price from "../../components/Price";
import { AddToCart, DealTimer, DeliveryLine, QuantityRow, Reassurance } from "./PurchaseParts";
import { useStickyOffset } from "./useStickyOffset";

/** The purchase card of tablets and desktops: price, discount timer, delivery, quantity and the add button. */
export default function PurchaseCard({ product, purchase }) {
  const ref = useRef(null);
  useStickyOffset(ref, "--product-sticky-top");

  return (
    <aside className="product-buy card" ref={ref} aria-label="خرید محصول" data-testid="product-buy">
      <Price product={product} size="lg" />
      {!purchase.soldOut && <DealTimer product={product} />}
      {!purchase.soldOut && <DeliveryLine product={product} />}
      {!purchase.soldOut && <QuantityRow purchase={purchase} />}
      <AddToCart product={product} purchase={purchase} />
      <Reassurance />
    </aside>
  );
}
