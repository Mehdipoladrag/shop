import { useId, useRef, useState } from "react";
import { Info } from "lucide-react";
import SpecsTable from "./SpecsTable";
import { descriptionParagraphs } from "./details";

const TABS = [
  { id: "description", label: "توضیحات" },
  { id: "specs", label: "مشخصات فنی" },
];

/** Description and specifications as an accessible tab list, followed by the product notice. */
export default function ProductTabs({ product }) {
  const baseId = useId();
  const [active, setActive] = useState(TABS[0].id);
  const tabRefs = useRef({});
  const paragraphs = descriptionParagraphs(product.product_description, product.notice);
  const notice = String(product.notice ?? "").trim();

  // Arrow keys follow what is on screen: in right-to-left text the left arrow goes to the next tab.
  function handleKeyDown(event) {
    const rtl = getComputedStyle(event.currentTarget).direction === "rtl";
    const index = TABS.findIndex((tab) => tab.id === active);
    let next;
    if (event.key === "ArrowRight") next = rtl ? index - 1 : index + 1;
    else if (event.key === "ArrowLeft") next = rtl ? index + 1 : index - 1;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = TABS.length - 1;
    else return;

    event.preventDefault();
    const target = TABS[(next + TABS.length) % TABS.length];
    setActive(target.id);
    tabRefs.current[target.id]?.focus();
  }

  return (
    <section className="section product-details" aria-labelledby={`${baseId}-heading`} data-testid="product-details">
      <h2 className="visually-hidden" id={`${baseId}-heading`}>
        اطلاعات تکمیلی محصول
      </h2>
      <div className="product-details__card card">
        <div className="product-details__tabs" role="tablist" aria-label="اطلاعات محصول" onKeyDown={handleKeyDown}>
          {TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              role="tab"
              id={`${baseId}-tab-${tab.id}`}
              className={`product-details__tab${active === tab.id ? " is-active" : ""}`}
              aria-selected={active === tab.id}
              aria-controls={`${baseId}-panel-${tab.id}`}
              tabIndex={active === tab.id ? 0 : -1}
              ref={(node) => {
                tabRefs.current[tab.id] = node;
              }}
              onClick={() => setActive(tab.id)}
              data-testid={`product-tab-${tab.id}`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div
          role="tabpanel"
          id={`${baseId}-panel-description`}
          aria-labelledby={`${baseId}-tab-description`}
          className="product-details__panel"
          tabIndex={0}
          hidden={active !== "description"}
          data-testid="product-panel-description"
        >
          {paragraphs.length > 0 ? (
            <div className="prose product-details__prose">
              {paragraphs.map((paragraph, index) => (
                <p key={index}>{paragraph}</p>
              ))}
            </div>
          ) : (
            <p className="product-details__empty">توضیحاتی برای این محصول ثبت نشده است.</p>
          )}
        </div>

        <div
          role="tabpanel"
          id={`${baseId}-panel-specs`}
          aria-labelledby={`${baseId}-tab-specs`}
          className="product-details__panel"
          tabIndex={0}
          hidden={active !== "specs"}
          data-testid="product-panel-specs"
        >
          <SpecsTable product={product} />
        </div>
      </div>

      {notice && (
        <div className="product-notice" role="note" data-testid="product-notice">
          <Info size={20} aria-hidden="true" />
          <p>{notice}</p>
        </div>
      )}
    </section>
  );
}
