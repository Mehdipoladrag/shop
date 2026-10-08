import { CircleAlert, RefreshCw } from "lucide-react";

/**
 * Compact error box for one section of the home page. The kit's LoadError is a
 * full-page card with its own container, which would double the page gutters
 * inside a section.
 */
export function SectionError({ error, onRetry, testId }) {
  return (
    <div className="home-error" role="alert" data-testid={testId}>
      <span className="home-error__icon">
        <CircleAlert size={24} aria-hidden="true" />
      </span>
      <div className="home-error__text">
        <strong>مشکلی پیش آمد</strong>
        <span>{error?.message || "خطایی رخ داد."}</span>
      </div>
      {onRetry && (
        <button type="button" className="btn btn--secondary btn--sm" onClick={onRetry} data-testid={`${testId}-retry`}>
          <RefreshCw size={16} aria-hidden="true" />
          تلاش دوباره
        </button>
      )}
    </div>
  );
}

/**
 * Skeleton row that reuses the carousel's own sizing classes, so the
 * placeholders take exactly the room the real items will.
 */
export function RowSkeleton({ variant = "cards", count = 6, itemClassName = "" }) {
  return (
    <div className={`carousel carousel--${variant} home-skeleton`} role="status" aria-label="در حال بارگذاری">
      <div className="carousel__track">
        {Array.from({ length: count }, (_, index) => (
          <div className="carousel__item" key={index}>
            <span className={`skeleton ${itemClassName}`} />
          </div>
        ))}
      </div>
    </div>
  );
}
