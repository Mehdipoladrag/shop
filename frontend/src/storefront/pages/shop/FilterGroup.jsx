import { ChevronDown } from "lucide-react";

function GroupSkeleton() {
  return (
    <div className="shop-group__skeleton" role="status" aria-label="در حال بارگذاری" data-testid="shop-group-loading">
      <span className="skeleton" />
      <span className="skeleton" />
      <span className="skeleton" />
    </div>
  );
}

function GroupError({ onRetry }) {
  return (
    <div className="shop-group__error" role="alert">
      <span>بارگذاری این بخش انجام نشد.</span>
      <button type="button" className="link-button" onClick={onRetry}>
        تلاش دوباره
      </button>
    </div>
  );
}

/**
 * One collapsible block of the filter panel. Pass the useApi state the block
 * depends on as `state` and the children as a function of its data: the group
 * then shows its own skeleton and error message.
 */
export default function FilterGroup({ title, state, testId, children }) {
  let body;
  if (state?.error) body = <GroupError onRetry={state.reload} />;
  else if (state && !state.data) body = <GroupSkeleton />;
  else body = typeof children === "function" ? children(state?.data) : children;

  return (
    <details className="shop-group" open data-testid={testId}>
      <summary className="shop-group__summary">
        <span>{title}</span>
        <ChevronDown size={18} aria-hidden="true" />
      </summary>
      <div className="shop-group__body">{body}</div>
    </details>
  );
}
