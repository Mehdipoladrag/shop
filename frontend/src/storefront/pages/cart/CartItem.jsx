import { Link } from "react-router-dom";
import { Trash2 } from "lucide-react";
import Price from "../../components/Price";
import QuantityStepper from "../../components/QuantityStepper";
import { formatPrice, toRelativeUrl } from "../../format";
import { MAX_PER_ORDER } from "../product/details";

const PICTURE_SIZE = 112;

/** One product of the cart: picture, details, unit price, quantity, line total and the remove button. */
export default function CartItem({ item, pending, onChangeCount, onRemove }) {
  const { product } = item;
  const stock = Number(product.product_number) || 0;
  // Never below what is already in the cart, so the stepper never shows an impossible state.
  const maxCount = Math.max(item.product_count, Math.min(stock, MAX_PER_ORDER));
  const url = `/products/${product.slug}`;
  const unitProduct = { ...product, final_price: item.unit_price };
  const details = [
    product.brand && { label: "برند", value: product.brand },
    item.product_color && { label: "رنگ", value: item.product_color },
  ].filter(Boolean);

  return (
    <li
      className={`cart-item${pending ? " is-pending" : ""}`}
      aria-busy={pending}
      data-testid="cart-item"
      data-product-id={product.id}
    >
      <Link to={url} className="cart-item__media" tabIndex={-1}>
        <img src={toRelativeUrl(product.pic)} alt={product.product_name} width={PICTURE_SIZE} height={PICTURE_SIZE} loading="lazy" decoding="async" />
      </Link>

      <div className="cart-item__info">
        <h3 className="cart-item__title">
          <Link to={url} data-testid="cart-item-link">
            {product.product_name}
          </Link>
        </h3>
        {details.length > 0 && (
          <ul className="cart-item__details">
            {details.map((detail) => (
              <li key={detail.label}>
                <span>{detail.label}</span>
                <strong dir="auto">{detail.value}</strong>
              </li>
            ))}
          </ul>
        )}
        <div className="cart-item__unit" data-testid="cart-item-unit-price">
          <span className="cart-item__caption">قیمت واحد</span>
          <Price product={unitProduct} showBadge={false} />
        </div>
      </div>

      <div className="cart-item__quantity" data-testid="cart-item-quantity">
        <QuantityStepper
          value={item.product_count}
          max={maxCount}
          disabled={pending}
          label={`تعداد ${product.product_name}`}
          onChange={(count) => onChangeCount(product.id, count)}
        />
        {stock > 0 && stock < MAX_PER_ORDER && item.product_count >= stock && <span className="cart-item__limit">حداکثر موجودی</span>}
      </div>

      <p className="cart-item__total" data-testid="cart-item-total">
        <span className="cart-item__caption">جمع</span>
        <span className="cart-item__amount">
          <strong>{formatPrice(item.total_price)}</strong>
          <span>تومان</span>
        </span>
      </p>

      <button
        type="button"
        className="icon-btn cart-item__remove"
        aria-label={`حذف ${product.product_name} از سبد`}
        disabled={pending}
        onClick={() => onRemove(product.id)}
        data-testid="cart-item-remove"
      >
        <Trash2 size={20} aria-hidden="true" />
      </button>
    </li>
  );
}
