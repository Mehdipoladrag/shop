import { useEffect, useId, useRef, useState } from "react";
import { X } from "lucide-react";

const EXIT_MS = 220;
const SCROLL_LOCK_CLASS = "shop-scroll-lock";
const FOCUSABLE = "a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]:not([tabindex='-1'])";

/**
 * Bottom sheet that holds the filters on small screens. It is a modal dialog:
 * focus moves into it and stays there (Tab wraps), Escape and a tap on the dim
 * background close it, the page behind does not scroll, and focus returns to
 * the button that opened it.
 */
export default function FilterSheet({ open, onClose, activeCount, onClear, applyLabel, onApply, children }) {
  const titleId = useId();
  const panelRef = useRef(null);
  const closeRef = useRef(null);
  const applyRef = useRef(null);
  // The handler may change on every render; the open/close effect must not restart because of it.
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;
  // Stay mounted for the length of the exit animation after `open` turns false.
  const [rendered, setRendered] = useState(open);
  if (open && !rendered) setRendered(true);

  useEffect(() => {
    if (open || !rendered) return undefined;
    const timer = setTimeout(() => setRendered(false), EXIT_MS);
    return () => clearTimeout(timer);
  }, [open, rendered]);

  useEffect(() => {
    if (!open) return undefined;
    const root = document.documentElement;
    const opener = document.activeElement;
    root.classList.add(SCROLL_LOCK_CLASS);
    closeRef.current?.focus();

    const handleKey = (event) => {
      if (event.key === "Escape") {
        onCloseRef.current();
        return;
      }
      if (event.key !== "Tab" || !panelRef.current) return;
      const items = [...panelRef.current.querySelectorAll(FOCUSABLE)].filter((item) => item.offsetParent !== null);
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];
      const inside = panelRef.current.contains(document.activeElement);
      if (event.shiftKey && (document.activeElement === first || !inside)) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && (document.activeElement === last || !inside)) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", handleKey);

    return () => {
      document.removeEventListener("keydown", handleKey);
      root.classList.remove(SCROLL_LOCK_CLASS);
      opener?.focus?.();
    };
  }, [open]);

  if (!rendered) return null;

  return (
    <div className={`shop-sheet${open ? "" : " is-closing"}`} data-testid="shop-filter-sheet-root">
      <div className="shop-sheet__overlay" onClick={onClose} data-testid="shop-filter-overlay" />
      <div className="shop-sheet__panel" role="dialog" aria-modal="true" aria-labelledby={titleId} ref={panelRef} data-testid="shop-filter-sheet">
        <div className="shop-sheet__head">
          <h2 className="shop-sheet__title" id={titleId}>
            فیلترها
            {activeCount > 0 && <span className="shop-sheet__count">{activeCount}</span>}
          </h2>
          <button type="button" className="icon-btn" aria-label="بستن فیلترها" onClick={onClose} ref={closeRef} data-testid="shop-filter-close">
            <X size={24} aria-hidden="true" />
          </button>
        </div>
        <div className="shop-sheet__body">{children}</div>
        <div className="shop-sheet__footer">
          <button type="button" className="btn btn--primary" onClick={onApply} ref={applyRef} data-testid="shop-filter-apply">
            {applyLabel}
          </button>
          {activeCount > 0 && (
            <button type="button" className="btn btn--secondary" onClick={() => { onClear(); applyRef.current?.focus(); }} data-testid="shop-filter-sheet-clear">
              پاک کردن همه
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
