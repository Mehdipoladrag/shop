/** Placeholder with the layout of the product page while the product loads. */
export default function ProductSkeleton() {
  return (
    <main className="page product-view" data-testid="product-skeleton">
      <div className="container" role="status" aria-label="در حال بارگذاری">
        <span className="skeleton product-skeleton__crumbs" />
        <div className="product-layout">
          <span className="skeleton product-skeleton__media" />
          <div className="product-skeleton__info">
            <span className="skeleton product-skeleton__line product-skeleton__line--short" />
            <span className="skeleton product-skeleton__title" />
            <span className="skeleton product-skeleton__line" />
            <span className="skeleton product-skeleton__line product-skeleton__line--medium" />
            <div className="product-skeleton__facts">
              {Array.from({ length: 4 }, (_, index) => (
                <span className="skeleton product-skeleton__fact" key={index} />
              ))}
            </div>
          </div>
          <span className="skeleton product-skeleton__buy" />
        </div>
      </div>
    </main>
  );
}
