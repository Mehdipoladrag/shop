import { useEffect, useRef } from "react";
import { ArrowUpDown } from "lucide-react";
import { SORT_OPTIONS } from "./filterState";

/**
 * Sort options as a row of pills. On small screens the row scrolls sideways,
 * and the chosen pill is kept in view.
 */
export default function SortBar({ ordering, onChange }) {
  const listRef = useRef(null);

  useEffect(() => {
    const list = listRef.current;
    const active = list?.querySelector("[aria-pressed='true']");
    if (!active || list.scrollWidth <= list.clientWidth) return;
    // Scroll the row only (scrollIntoView would also move the page). Works in RTL too.
    const row = list.getBoundingClientRect();
    const pill = active.getBoundingClientRect();
    list.scrollBy({ left: pill.left + pill.width / 2 - (row.left + row.width / 2), behavior: "auto" });
  }, [ordering]);

  return (
    <div className="shop-sort" role="group" aria-label="مرتب‌سازی" data-testid="shop-sort">
      <span className="shop-sort__label" aria-hidden="true">
        <ArrowUpDown size={16} />
        مرتب‌سازی:
      </span>
      <div className="shop-sort__list" ref={listRef}>
        {SORT_OPTIONS.map((option) => {
          const active = option.ordering === ordering;
          return (
            <button
              type="button"
              key={option.key}
              className={`shop-sort__option${active ? " is-active" : ""}`}
              aria-pressed={active}
              onClick={() => !active && onChange(option.ordering)}
              data-testid={`shop-sort-${option.key}`}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
