/** Loading placeholder of the whole account area (profile card, menu and a page). */
export function AccountSkeleton() {
  return (
    <div className="account-layout" role="status" aria-label="در حال بارگذاری" data-testid="account-skeleton">
      <div className="account-aside">
        <span className="skeleton account-skeleton__profile" />
        <span className="skeleton account-skeleton__menu" />
      </div>
      <div className="account-main">
        <span className="skeleton account-skeleton__title" />
        <span className="skeleton account-skeleton__card" />
        <span className="skeleton account-skeleton__card" />
      </div>
    </div>
  );
}

/** Placeholder for a list of cards inside the account page (orders, order details). */
export function CardsSkeleton({ count = 3, height = "account-skeleton__card" }) {
  return (
    <div className="account-cards" role="status" aria-label="در حال بارگذاری">
      {Array.from({ length: count }, (_, index) => (
        <span className={`skeleton ${height}`} key={index} />
      ))}
    </div>
  );
}
