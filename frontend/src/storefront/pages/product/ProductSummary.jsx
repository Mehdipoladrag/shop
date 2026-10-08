import { Ban, Bluetooth, Camera, Check, Cpu, Palette, Smartphone, Sparkles, TriangleAlert } from "lucide-react";
import Rating from "../../components/Rating";
import { keyFacts, LOW_STOCK_LIMIT, MAX_RATE, stockOf } from "./details";

const FACT_ICONS = {
  color: Palette,
  os: Smartphone,
  technology: Cpu,
  capability: Sparkles,
  camera: Camera,
  bluetooth: Bluetooth,
};

/** Stock status as a small colored chip: in stock, only a few left, or sold out. */
export function StockChip({ product }) {
  const stock = stockOf(product);
  if (stock <= 0) {
    return (
      <span className="badge badge--danger product-summary__stock" data-testid="product-stock">
        <Ban size={14} aria-hidden="true" />
        ناموجود
      </span>
    );
  }
  if (stock <= LOW_STOCK_LIMIT) {
    return (
      <span className="badge badge--warning product-summary__stock" data-testid="product-stock">
        <TriangleAlert size={14} aria-hidden="true" />
        تنها {stock} عدد باقی مانده
      </span>
    );
  }
  return (
    <span className="badge badge--success product-summary__stock" data-testid="product-stock">
      <Check size={14} aria-hidden="true" />
      موجود
    </span>
  );
}

/** Brand, title, rating, stock chip, short description and the key facts. */
export default function ProductSummary({ product }) {
  const facts = keyFacts(product);
  const rated = Number(product.product_rate) > 0;

  return (
    <div className="product-summary" data-testid="product-summary">
      {product.brand && (
        <p className="product-summary__brand" data-testid="product-brand" dir="auto">
          {product.brand}
        </p>
      )}
      <h1 className="product-summary__title" data-testid="product-title">
        {product.product_name}
      </h1>

      <div className="product-summary__meta">
        {rated && (
          <span className="product-summary__rate" data-testid="product-rating">
            <Rating value={product.product_rate} />
            <span>امتیاز کاربران از {MAX_RATE}</span>
          </span>
        )}
        <StockChip product={product} />
      </div>

      {product.mini_description && <p className="product-summary__lead">{product.mini_description}</p>}

      {facts.length > 0 && (
        <dl className="product-summary__facts" data-testid="product-facts">
          {facts.map((fact) => {
            const Icon = FACT_ICONS[fact.key];
            return (
              <div className="product-fact" key={fact.key} data-testid={`product-fact-${fact.key}`}>
                <dt>
                  <Icon size={16} aria-hidden="true" />
                  {fact.label}
                </dt>
                <dd>{fact.value}</dd>
              </div>
            );
          })}
        </dl>
      )}
    </div>
  );
}
