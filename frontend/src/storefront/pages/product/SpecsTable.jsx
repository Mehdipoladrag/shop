import { isWebAddress, keyFacts, parseSpecs } from "./details";

/**
 * Specifications as a zebra table. Lines of the specifications text written as
 * "key: value" become two columns, the other lines span the full width.
 * Without a specifications text the key facts of the product are listed instead.
 */
export default function SpecsTable({ product }) {
  let rows = parseSpecs(product.specifications);
  if (rows.length === 0) rows = keyFacts(product).map((fact) => ({ id: fact.key, key: fact.label, value: fact.value }));

  if (rows.length === 0) {
    return <p className="product-details__empty">مشخصات فنی این محصول ثبت نشده است.</p>;
  }

  return (
    <div className="product-specs">
      <table className="product-specs__table" data-testid="product-specs-table">
        <caption className="visually-hidden">مشخصات فنی {product.product_name}</caption>
        <colgroup>
          <col className="product-specs__key" />
          <col />
        </colgroup>
        <tbody>
          {rows.map((row) =>
            row.key ? (
              <tr key={row.id}>
                <th scope="row">{row.key}</th>
                <td>
                  {isWebAddress(row.value) ? (
                    <a href={row.value} className="ltr" target="_blank" rel="noopener noreferrer">
                      {row.value}
                    </a>
                  ) : (
                    row.value
                  )}
                </td>
              </tr>
            ) : (
              <tr key={row.id} className="is-wide">
                <td colSpan={2}>{row.text}</td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
}
