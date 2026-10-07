import { Link } from "react-router-dom";

/** Placeholder shown while data loads, laid out inside the page container. */
export function Loading() {
  return (
    <div className="container text-center" style={{ padding: "80px 0", color: "var(--color-primary)" }} role="status">
      در حال بارگذاری…
    </div>
  );
}

export function LoadError({ error, onRetry }) {
  return (
    <div className="container text-center" style={{ padding: "80px 0" }} role="alert">
      <p>{error?.message || "خطایی رخ داد."}</p>
      {onRetry && (
        <button type="button" className="btn btn-main-masai" onClick={onRetry}>
          تلاش دوباره
        </button>
      )}
    </div>
  );
}

/** Renders the right placeholder for a useApi() state, or the content when ready. */
export function AsyncContent({ state, children }) {
  if (state.loading && !state.data) return <Loading />;
  if (state.error) return <LoadError error={state.error} onRetry={state.reload} />;
  return children(state.data);
}

export function NotFound() {
  return (
    <main className="cart default">
      <div className="container text-center cart_empty">
        <h6>صفحه‌ی مورد نظر پیدا نشد.</h6>
        <Link to="/" className="btn btn-main-masai">
          صفحه نخست
        </Link>
      </div>
    </main>
  );
}
