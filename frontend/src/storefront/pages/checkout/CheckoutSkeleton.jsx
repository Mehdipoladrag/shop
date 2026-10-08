import "../checkout.css";

/** Loading placeholder of the checkout and order-confirmation pages. */
export default function CheckoutSkeleton({ narrow = false }) {
  return (
    <main className="page checkout-page" aria-busy="true">
      <div className="container" role="status" aria-label="در حال بارگذاری">
        <span className="skeleton checkout-skeleton__steps" />
        {narrow ? (
          <span className="skeleton checkout-skeleton__success" />
        ) : (
          <div className="checkout-layout">
            <div className="checkout-main">
              <span className="skeleton checkout-skeleton__address" />
              <span className="skeleton checkout-skeleton__items" />
            </div>
            <span className="skeleton checkout-skeleton__total" />
          </div>
        )}
      </div>
    </main>
  );
}
