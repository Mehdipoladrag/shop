import { EmptyState } from "./Feedback";

/**
 * Table that turns into a stack of cards on narrow screens. Each cell carries
 * its column header as `data-label`, which the stylesheet shows on mobile.
 */
export default function DataTable({ columns, rows, getRowKey, renderActions, emptyText }) {
  if (rows.length === 0) return <EmptyState text={emptyText} />;

  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>{column.header}</th>
            ))}
            {renderActions && <th aria-label="عملیات" />}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={getRowKey(row)}>
              {columns.map((column) => (
                <td key={column.key} data-label={column.header}>
                  {column.render ? column.render(row) : row[column.key]}
                </td>
              ))}
              {renderActions && (
                <td className="data-table__actions" data-label="عملیات">
                  {renderActions(row)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
