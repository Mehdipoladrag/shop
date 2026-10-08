import { Fragment } from "react";
import { Link } from "react-router-dom";
import { CircleAlert, SearchX } from "lucide-react";
import "./States.css";

/** Skeleton shown while a page's data loads, inside the page container. */
export function Loading({ variant = "page" }) {
  return (
    <div className="container loading" role="status" aria-label="در حال بارگذاری">
      <span className="skeleton loading__title" />
      {variant === "grid" ? (
        <div className="product-grid">
          {Array.from({ length: 8 }, (_, index) => (
            <span className="skeleton loading__card" key={index} />
          ))}
        </div>
      ) : (
        <>
          <span className="skeleton loading__block" />
          <span className="skeleton loading__line" />
          <span className="skeleton loading__line loading__line--short" />
        </>
      )}
    </div>
  );
}

/** Centered message with an icon and optional action, used for errors, empty lists and 404. */
export function EmptyState({ icon: Icon = SearchX, title, text, children, tone = "neutral", contained = true, level = 2 }) {
  const Title = `h${level}`;
  const Wrapper = contained ? "div" : Fragment;
  return (
    <Wrapper {...(contained ? { className: "container" } : {})}>
      <div className={`empty-state empty-state--${tone}`}>
        <span className="empty-state__icon">
          <Icon size={36} aria-hidden="true" />
        </span>
        <Title className="empty-state__title">{title}</Title>
        {text && <p className="empty-state__text">{text}</p>}
        {children && <div className="empty-state__actions">{children}</div>}
      </div>
    </Wrapper>
  );
}

export function LoadError({ error, onRetry, contained = true }) {
  return (
    <div role="alert">
      <EmptyState icon={CircleAlert} tone="danger" title="مشکلی پیش آمد" text={error?.message || "خطایی رخ داد."} contained={contained}>
        {onRetry && (
          <button type="button" className="btn btn--primary" onClick={onRetry}>
            تلاش دوباره
          </button>
        )}
      </EmptyState>
    </div>
  );
}

/** Renders the right placeholder for a useApi() state, or the content when ready. */
export function AsyncContent({ state, children, variant }) {
  if (state.loading && !state.data) return <Loading variant={variant} />;
  if (state.error) return <LoadError error={state.error} onRetry={state.reload} />;
  return children(state.data);
}

export function NotFound() {
  return (
    <main className="page">
      <EmptyState level={1} title="صفحه‌ی مورد نظر پیدا نشد." text="ممکن است آدرس را اشتباه وارد کرده باشید یا صفحه حذف شده باشد.">
        <Link to="/" className="btn btn--primary">
          صفحه نخست
        </Link>
        <Link to="/products" className="btn btn--secondary">
          مشاهده محصولات
        </Link>
      </EmptyState>
    </main>
  );
}
