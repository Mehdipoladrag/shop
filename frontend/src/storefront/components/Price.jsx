import { formatPrice } from "../format";

/** Price block: struck-through price, discount badge and discounted price. */
export default function Price({ product }) {
  if (!product.offer) {
    return (
      <span>
        {formatPrice(product.price)}
        <span>تومان</span>
      </span>
    );
  }
  return (
    <>
      <del>
        <span>
          {formatPrice(product.price)}
          <span>تومان</span>
        </span>
      </del>
      <span className="discount_badge">{formatPrice(product.offer)}%</span>
      <ins>
        <span>
          {formatPrice(product.final_price)}
          <span>تومان</span>
        </span>
      </ins>
    </>
  );
}
