import { ChevronLeft, ChevronRight } from "lucide-react";
import "./Pagination.css";

const NEIGHBOUR_PAGES = 1;

/** Page numbers to show: first, last, the current one with its neighbours, and "…" gaps. */
function visiblePages(current, total) {
  const wanted = new Set([1, total]);
  for (let page = current - NEIGHBOUR_PAGES; page <= current + NEIGHBOUR_PAGES; page += 1) {
    if (page >= 1 && page <= total) wanted.add(page);
  }
  const sorted = [...wanted].sort((a, b) => a - b);
  return sorted.flatMap((page, index) => (index > 0 && page - sorted[index - 1] > 1 ? ["gap", page] : [page]));
}

/** Page navigation; `onChange(page)` is called with the page number to show. */
export default function Pagination({ page, pageCount, onChange }) {
  if (pageCount <= 1) return null;

  const go = (event, target) => {
    event.preventDefault();
    if (target >= 1 && target <= pageCount && target !== page) onChange(target);
  };

  return (
    <nav className="pagination" aria-label="صفحه‌بندی">
      <ul className="pagination__list">
        <li>
          <a href={`?page=${page - 1}`} className="pagination__link" aria-label="صفحه قبل" aria-disabled={page === 1} onClick={(event) => go(event, page - 1)}>
            <ChevronRight size={18} aria-hidden="true" />
          </a>
        </li>
        {visiblePages(page, pageCount).map((entry, index) =>
          entry === "gap" ? (
            <li key={`gap-${index}`} className="pagination__gap" aria-hidden="true">
              …
            </li>
          ) : (
            <li key={entry}>
              <a
                href={`?page=${entry}`}
                className={`pagination__link${entry === page ? " is-active" : ""}`}
                aria-current={entry === page ? "page" : undefined}
                onClick={(event) => go(event, entry)}
              >
                {entry}
              </a>
            </li>
          )
        )}
        <li>
          <a href={`?page=${page + 1}`} className="pagination__link" aria-label="صفحه بعد" aria-disabled={page === pageCount} onClick={(event) => go(event, page + 1)}>
            <ChevronLeft size={18} aria-hidden="true" />
          </a>
        </li>
      </ul>
    </nav>
  );
}
