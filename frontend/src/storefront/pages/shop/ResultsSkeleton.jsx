import { PAGE_SIZE } from "./filterState";

/** Placeholder product cards with the same proportions as the real ones. */
export default function ResultsSkeleton() {
  return (
    <div className="product-grid shop-grid" role="status" aria-label="در حال بارگذاری" data-testid="shop-skeleton">
      {Array.from({ length: PAGE_SIZE }, (_, index) => (
        <div className="shop-skeleton-card" key={index}>
          <span className="skeleton shop-skeleton-card__media" />
          <span className="skeleton shop-skeleton-card__line shop-skeleton-card__line--short" />
          <span className="skeleton shop-skeleton-card__line" />
          <span className="skeleton shop-skeleton-card__line" />
          <span className="skeleton shop-skeleton-card__price" />
        </div>
      ))}
    </div>
  );
}
