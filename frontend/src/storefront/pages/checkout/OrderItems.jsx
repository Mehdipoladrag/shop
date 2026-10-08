import { Link } from "react-router-dom";
import { formatPrice, toRelativeUrl } from "../../format";
import "../checkout.css";

/** Items of the cart as they will be ordered. */
export default function OrderItems({ items, totalCount }) {
  return (
    <section className="card card--pad" aria-labelledby="checkout-items-title" data-testid="checkout-items">
      <div className="checkout-card-head">
        <h2 className="card__title" id="checkout-items-title">
          کالاهای سفارش <span className="badge">{totalCount}</span>
        </h2>
        <Link to="/cart" className="btn btn--ghost btn--sm" data-testid="checkout-cart-link">
          ویرایش سبد
        </Link>
      </div>
      <ul className="checkout-lines">
        {items.map((item) => {
          const { product } = item;
          const discounted = Number(product.offer) > 0;
          return (
            <li className="checkout-line" key={`${product.id}-${item.product_color}`} data-testid="checkout-item">
              <div className="checkout-line__pic">
                <img src={toRelativeUrl(product.pic)} alt="" width="72" height="72" loading="lazy" />
              </div>
              <div className="checkout-line__info">
                <Link to={`/products/${product.slug}`} className="checkout-line__name">
                  {product.product_name}
                </Link>
                <p className="checkout-line__meta">
                  {item.product_color && <span>رنگ: {item.product_color}</span>}
                  <span>تعداد: {item.product_count}</span>
                </p>
                <p className="checkout-line__unit">
                  {discounted && <del>{formatPrice(product.price)}</del>}
                  <span>{formatPrice(item.unit_price)} تومان</span>
                </p>
              </div>
              <p className="checkout-line__total">
                {formatPrice(item.total_price)} <small>تومان</small>
              </p>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
