import { Link } from "react-router-dom";
import { useCart } from "../cart/CartContext";
import { toRelativeUrl } from "../format";
import Price from "./Price";

/** Quick "add to cart" icon used on product cards. */
function AddToCartIcon({ product }) {
  const { addItem } = useCart();
  return (
    <span
      className="search_prod_btn"
      role="button"
      tabIndex={0}
      aria-label={`افزودن ${product.product_name} به سبد خرید`}
      onClick={() => addItem(product.id, 1)}
      onKeyDown={(event) => event.key === "Enter" && addItem(product.id, 1)}
    >
      <i className="fa fa fa-cart-arrow-down search_icon_cart" aria-hidden="true" />
    </span>
  );
}

/** Card used inside the product carousels of the home page. */
export function ProductItem({ product }) {
  const productUrl = `/products/${product.slug}`;
  return (
    <div className="item">
      <Link to={productUrl}>
        <img src={toRelativeUrl(product.pic)} className="img-fluid" alt={product.product_name} />
      </Link>
      <h2 className="product_title">
        <Link to={productUrl}>{product.product_name}</Link>
      </h2>
      <div className="price">
        <Price product={product} />
      </div>
      <div className="product-seller-details product-seller-details-item-grid">
        <span className="search_prod_icon">
          <Link to={productUrl} aria-label="مشاهده محصول">
            <i className="fa fa-search search_icon_search" aria-hidden="true" />
          </Link>
          <i className="fa fa-heart search_icon_like" aria-hidden="true" />
        </span>
        <AddToCartIcon product={product} />
      </div>
    </div>
  );
}

/** Card used in the shop listing grid. */
export function ProductBox({ product }) {
  const productUrl = `/products/${product.slug}`;
  return (
    <div className="col-xl-4 col-lg-4 col-md-6 col-12 list_search_p">
      <div className="product-box">
        <div className="product-seller-details product-seller-details-item-grid">
          <span className="search_prod_icon">
            <Link to={productUrl} aria-label="مشاهده محصول">
              <i className="fa fa-search search_icon_search" aria-hidden="true" />
            </Link>
            <i className="fa fa-heart search_icon_like" aria-hidden="true" />
          </span>
          <AddToCartIcon product={product} />
        </div>
        <Link className="product-box-img" to={productUrl}>
          <img src={toRelativeUrl(product.pic)} alt={product.product_name} />
        </Link>
        <div className="product-box-content">
          <div className="product-box-content-row">
            <div className="product_title">
              <Link to={productUrl}>{product.product_name}</Link>
            </div>
          </div>
          <div className="product-box-row product_price_search">
            <div className="price">
              <Price product={product} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
