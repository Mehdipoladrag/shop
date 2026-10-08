import { Loader2 } from "lucide-react";

/** Primary button with a spinner and its own text while a request is running. */
export default function SubmitButton({ loading, loadingText, children, className = "btn btn--primary", ...props }) {
  return (
    <button type="submit" className={className} disabled={loading} aria-busy={loading || undefined} {...props}>
      {loading && <Loader2 size={18} className="account-spin" aria-hidden="true" />}
      {loading ? loadingText : children}
    </button>
  );
}
