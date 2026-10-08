/** Placeholder with the layout of the cart while it loads. */
export default function CartSkeleton() {
  return (
    <div className="cart-layout" role="status" aria-label="در حال بارگذاری" data-testid="cart-skeleton">
      <div className="cart-skeleton__list">
        {Array.from({ length: 3 }, (_, index) => (
          <span className="skeleton cart-skeleton__item" key={index} />
        ))}
      </div>
      <span className="skeleton cart-skeleton__summary" />
    </div>
  );
}
