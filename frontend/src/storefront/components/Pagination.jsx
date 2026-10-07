const NEIGHBOUR_PAGES = 2;

function visiblePages(current, total) {
  const first = Math.max(1, current - NEIGHBOUR_PAGES);
  const last = Math.min(total, current + NEIGHBOUR_PAGES);
  return Array.from({ length: last - first + 1 }, (_, offset) => first + offset);
}

/** Bootstrap pagination with the same markup as the Django templates. */
export default function Pagination({ page, pageCount, onChange }) {
  if (pageCount <= 1) return null;

  const link = (target, label, { disabled = false, active = false } = {}) => (
    <li className={`page-item${disabled ? " disabled" : ""}${active ? " active" : ""}`} key={label + target}>
      <a
        href={`?page=${target}`}
        className="page-link"
        onClick={(event) => {
          event.preventDefault();
          if (!disabled && !active) onChange(target);
        }}
      >
        {label}
      </a>
    </li>
  );

  return (
    <ul className="pagination">
      {link(page - 1, "«", { disabled: page === 1 })}
      {visiblePages(page, pageCount).map((target) => link(target, String(target), { active: target === page }))}
      {link(page + 1, "»", { disabled: page === pageCount })}
    </ul>
  );
}
