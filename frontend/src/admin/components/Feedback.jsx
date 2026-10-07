export function Spinner({ label = "در حال بارگذاری…" }) {
  return (
    <div className="feedback" role="status">
      <span className="spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}

export function ErrorState({ error, onRetry }) {
  return (
    <div className="feedback feedback--error" role="alert">
      <p>{error?.message || "خطایی رخ داد."}</p>
      {onRetry && (
        <button type="button" className="btn btn--ghost" onClick={onRetry}>
          تلاش دوباره
        </button>
      )}
    </div>
  );
}

export function EmptyState({ text = "موردی برای نمایش وجود ندارد." }) {
  return <div className="feedback feedback--empty">{text}</div>;
}

// Renders the right placeholder for a useApi() state, or the content when ready.
export function AsyncContent({ state, children }) {
  if (state.loading && !state.data) return <Spinner />;
  if (state.error) return <ErrorState error={state.error} onRetry={state.reload} />;
  return children(state.data);
}
