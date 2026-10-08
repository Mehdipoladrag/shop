import { formatPrice } from "../format";
import "./Price.css";

/**
 * Price block: the final price, and for discounted products the old price
 * struck through next to the discount percentage.
 * `size` is "md" (cards, lists) or "lg" (product page).
 */
export default function Price({ product, size = "md", showBadge = true }) {
  const discounted = Number(product.offer) > 0;
  return (
    <div className={`price price--${size}`}>
      {discounted && (
        <div className="price__old">
          <del>{formatPrice(product.price)}</del>
          {showBadge && <span className="badge badge--discount">{formatPrice(product.offer)}%</span>}
        </div>
      )}
      <div className="price__final">
        <strong>{formatPrice(discounted ? product.final_price : product.price)}</strong>
        <span className="price__unit">تومان</span>
      </div>
    </div>
  );
}
