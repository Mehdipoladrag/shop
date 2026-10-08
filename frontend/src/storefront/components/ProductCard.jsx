import { useState } from "react";
import { Link } from "react-router-dom";
import { Check, ShoppingCart } from "lucide-react";
import { useCart } from "../cart/CartContext";
import { toRelativeUrl } from "../format";
import { useFlash } from "./Flash";
import Price from "./Price";
import Rating from "./Rating";
import "./ProductCard.css";

const LOW_STOCK_LIMIT = 5;
const ADDED_FEEDBACK_MS = 1600;

/** Product tile used by every listing: the shop grid, home carousels and related products. */
export default function ProductCard({ product }) {
  const { addItem } = useCart();
  const flash = useFlash();
  const [state, setState] = useState("idle");
  const url = `/products/${product.slug}`;
  const stock = Number(product.product_number);
  const soldOut = stock <= 0;
  const discounted = Number(product.offer) > 0;

  async function handleAdd() {
    if (state !== "idle") return;
    setState("busy");
    try {
      await addItem(product.id, 1);
      flash.show("به سبد خرید اضافه شد");
      setState("added");
      setTimeout(() => setState("idle"), ADDED_FEEDBACK_MS);
    } catch (error) {
      flash.show(error.message, "error");
      setState("idle");
    }
  }

  return (
    <article className={`product-card${soldOut ? " is-sold-out" : ""}`}>
      <Link to={url} className="product-card__media" tabIndex={-1} aria-hidden="true">
        <img src={toRelativeUrl(product.pic)} alt="" loading="lazy" decoding="async" width="320" height="320" />
        {discounted && <span className="badge badge--discount product-card__badge">{Number(product.offer)}%</span>}
        {soldOut && <span className="product-card__sold-out">ناموجود</span>}
      </Link>

      <div className="product-card__body">
        <span className="product-card__brand">{product.brand}</span>
        <h3 className="product-card__title">
          <Link to={url}>{product.product_name}</Link>
        </h3>
        <div className="product-card__meta">
          <Rating value={product.product_rate} />
          {!soldOut && stock <= LOW_STOCK_LIMIT && <span className="product-card__low-stock">فقط {stock} عدد باقی مانده</span>}
        </div>

        <div className="product-card__footer">
          <Price product={product} showBadge={false} />
          <button
            type="button"
            className={`product-card__add${state === "added" ? " is-added" : ""}`}
            aria-label={`افزودن ${product.product_name} به سبد خرید`}
            disabled={soldOut || state === "busy"}
            onClick={handleAdd}
          >
            {state === "added" ? <Check size={20} aria-hidden="true" /> : <ShoppingCart size={20} aria-hidden="true" />}
          </button>
        </div>
      </div>
    </article>
  );
}
