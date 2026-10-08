import { useCallback, useEffect, useId, useMemo, useRef, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { SlidersHorizontal } from "lucide-react";
import { useApi } from "../../shared/useApi";
import { catalogApi } from "../api/endpoints";
import Breadcrumb from "../components/Breadcrumb";
import Pagination from "../components/Pagination";
import ProductCard from "../components/ProductCard";
import { EmptyState, LoadError } from "../components/States";
import { useDocumentTitle } from "../components/useDocumentTitle";
import ActiveFilters from "./shop/ActiveFilters";
import FilterPanel from "./shop/FilterPanel";
import FilterSheet from "./shop/FilterSheet";
import ResultsSkeleton from "./shop/ResultsSkeleton";
import SortBar from "./shop/SortBar";
import { CLEARED_FILTERS, PAGE_SIZE, countActiveFilters, productQuery, readFilters } from "./shop/filterState";
import { useMediaQuery } from "./shop/useMediaQuery";
import { useStickyOffset } from "./shop/useStickyOffset";
import "./shop.css";

// From this width the filters sit in a sticky sidebar; below it they open from a button.
const SIDEBAR_QUERY = "(min-width: 992px)";
const PRICE_ORDER_ERROR = "حداقل قیمت نباید از حداکثر بیشتر باشد.";

function formatCount(value) {
  return Number(value).toLocaleString("en-US");
}

/** Nothing matched: offer the way out that fits what the visitor did. */
function EmptyResults({ mode, hasFilters, query, onClear }) {
  let text = "چند لحظه بعد دوباره سر بزنید یا دسته‌بندی دیگری را ببینید.";
  if (hasFilters) text = "فیلترها را کم کنید یا بازه قیمت را بازتر کنید.";
  else if (mode === "search") {
    text = (
      <>
        نتیجه‌ای برای «<bdi>{query}</bdi>» پیدا نشد. عبارت دیگری را جستجو کنید.
      </>
    );
  }

  return (
    <div data-testid="shop-empty">
      <EmptyState title="محصولی با این مشخصات پیدا نشد" text={text}>
        {hasFilters && (
          <button type="button" className="btn btn--primary" onClick={onClear} data-testid="shop-empty-clear">
            پاک کردن فیلترها
          </button>
        )}
        <Link to={mode === "all" ? "/" : "/products"} className={`btn ${hasFilters ? "btn--secondary" : "btn--primary"}`} data-testid="shop-empty-link">
          {mode === "all" ? "صفحه نخست" : "مشاهده همه محصولات"}
        </Link>
      </EmptyState>
    </div>
  );
}

/**
 * Product listing used by four routes: all products, one category and search
 * results (`mode` is "all", "category" or "search"). Page, sort order and every
 * filter live in the URL, so each view can be shared and back/forward work.
 */
export default function ShopPage({ mode }) {
  const { slug } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const filters = useMemo(() => readFilters(searchParams), [searchParams]);
  const sidebar = useMediaQuery(SIDEBAR_QUERY);
  const resultsTitleId = useId();

  const rootRef = useRef(null);
  const resultsRef = useRef(null);
  useStickyOffset(rootRef);

  const categories = useApi(catalogApi.categories);
  const brands = useApi(catalogApi.brands);
  const options = useApi(catalogApi.productFilters);
  const products = useApi(
    () => catalogApi.products(productQuery(mode, slug, filters)),
    [mode, slug, filters.query, filters.page, filters.ordering, filters.brand, filters.color, filters.minPrice, filters.maxPrice, filters.inStock, filters.hasOffer]
  );

  // Changing a filter or the sort order always returns to the first page.
  const update = useCallback(
    (changes, { keepPage = false } = {}) => {
      setSearchParams((previous) => {
        const next = new URLSearchParams(previous);
        Object.entries(changes).forEach(([key, value]) => {
          if (value === "" || value === undefined || value === null) next.delete(key);
          else next.set(key, value);
        });
        if (!keepPage) next.delete("page");
        return next;
      });
    },
    [setSearchParams]
  );
  const clearFilters = useCallback(() => update(CLEARED_FILTERS), [update]);

  // A removed chip or button takes keyboard focus with it; the results region keeps it on the page.
  const focusResults = () => resultsRef.current?.focus({ preventScroll: true });
  const removeFilter = (changes) => {
    update(changes);
    focusResults();
  };
  const clearFromPage = () => {
    clearFilters();
    focusResults();
  };

  // The price inputs are a draft until "apply"; they follow the URL when it changes (clear, back, forward).
  const [priceDraft, setPriceDraft] = useState({ min: filters.minPrice, max: filters.maxPrice });
  const [priceError, setPriceError] = useState("");
  useEffect(() => {
    setPriceDraft({ min: filters.minPrice, max: filters.maxPrice });
    setPriceError("");
  }, [filters.minPrice, filters.maxPrice]);

  const changePriceDraft = (field, value) => {
    setPriceDraft((draft) => ({ ...draft, [field]: value }));
    setPriceError("");
  };

  /** Writes the price draft to the URL; false when the range is wrong. */
  const applyPrice = () => {
    const min = priceDraft.min.trim();
    const max = priceDraft.max.trim();
    if (min && max && Number(min) > Number(max)) {
      setPriceError(PRICE_ORDER_ERROR);
      return false;
    }
    if (min !== filters.minPrice || max !== filters.maxPrice) update({ min_price: min, max_price: max });
    return true;
  };

  // Filters of the small-screen sheet apply as soon as they are touched; the button only closes it.
  const [sheetOpen, setSheetOpen] = useState(false);
  const closeSheet = useCallback(() => setSheetOpen(false), []);
  useEffect(() => {
    if (sidebar) setSheetOpen(false);
  }, [sidebar]);

  const goToPage = (target) => {
    update({ page: String(target) }, { keepPage: true });
    resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const categoryName = categories.data?.find((category) => category.category_slug === slug)?.category_name;
  let title = "همه محصولات";
  if (mode === "search") title = filters.query ? `نتایج جستجو برای «${filters.query}»` : "جستجوی محصولات";
  else if (mode === "category") title = categoryName ?? (categories.data ? "دسته‌بندی پیدا نشد" : categories.error ? "دسته‌بندی" : null);
  useDocumentTitle(title ?? "دسته‌بندی");

  const breadcrumb =
    mode === "all"
      ? [{ label: "فروشگاه" }]
      : [{ label: "فروشگاه", to: "/products" }, { label: mode === "search" ? "جستجو" : title ?? "دسته‌بندی" }];

  const activeCount = countActiveFilters(filters);
  const count = products.data?.count;
  const pageCount = Math.ceil((count ?? 0) / PAGE_SIZE);
  const refreshing = products.loading && Boolean(products.data);
  const pageMissing = products.error?.status === 404 && filters.page > 1;

  let applyLabel = "نمایش کالاها";
  if (count === 0) applyLabel = "بستن";
  else if (count > 0 && !refreshing) applyLabel = `نمایش ${formatCount(count)} کالا`;

  const panel = (
    <FilterPanel
      mode={mode}
      slug={slug}
      filters={filters}
      categories={categories}
      brands={brands}
      options={options}
      price={{ ...priceDraft, error: priceError }}
      onChange={update}
      onPriceChange={changePriceDraft}
      onPriceApply={applyPrice}
      onNavigate={closeSheet}
    />
  );

  let body;
  if (products.error) {
    body = pageMissing ? (
      <div data-testid="shop-page-missing">
        <EmptyState title="این صفحه وجود ندارد" text="تعداد صفحه‌های نتایج کمتر است. از اولین صفحه شروع کنید.">
          <button type="button" className="btn btn--primary" onClick={() => update({ page: "" }, { keepPage: true })} data-testid="shop-first-page">
            رفتن به صفحه اول
          </button>
        </EmptyState>
      </div>
    ) : (
      <div data-testid="shop-error">
        <LoadError error={products.error} onRetry={products.reload} />
      </div>
    );
  } else if (!products.data) {
    body = <ResultsSkeleton />;
  } else if (products.data.results.length === 0) {
    body = <EmptyResults mode={mode} hasFilters={activeCount > 0} query={filters.query} onClear={clearFromPage} />;
  } else {
    body = (
      <>
        <ul className="product-grid shop-grid" data-testid="shop-grid">
          {products.data.results.map((product) => (
            <li className="shop-grid__item" key={product.id} data-testid="shop-product">
              <ProductCard product={product} />
            </li>
          ))}
        </ul>
        <div data-testid="shop-pagination">
          <Pagination page={filters.page} pageCount={pageCount} onChange={goToPage} />
        </div>
      </>
    );
  }

  return (
    <main className="page shop" data-testid="shop-page" ref={rootRef}>
      <div className="container">
        <Breadcrumb items={breadcrumb} />

        <header className="shop-head">
          <h1 className="shop-head__title" data-testid="shop-title">
            {mode === "search" && filters.query ? (
              <>
                نتایج جستجو برای «<bdi>{filters.query}</bdi>»
              </>
            ) : (
              title ?? <span className="skeleton shop-head__title-skeleton" role="status" aria-label="در حال بارگذاری" />
            )}
          </h1>
          <p className="shop-head__count" role="status" data-testid="shop-result-count">
            {products.data ? (
              <>
                <strong>{formatCount(count)}</strong> کالا
              </>
            ) : (
              !products.error && <span className="skeleton shop-head__count-skeleton" />
            )}
          </p>
        </header>

        <div className="shop-layout">
          {sidebar && (
            <aside className="shop-sidebar card" aria-labelledby={`${resultsTitleId}-filters`} data-testid="shop-filters">
              <div className="shop-sidebar__head">
                <h2 className="shop-sidebar__title" id={`${resultsTitleId}-filters`}>
                  <SlidersHorizontal size={18} aria-hidden="true" />
                  فیلترها
                </h2>
              </div>
              {panel}
            </aside>
          )}

          <section className="shop-results" aria-labelledby={resultsTitleId} tabIndex={-1} ref={resultsRef} data-testid="shop-results">
            <h2 className="visually-hidden" id={resultsTitleId}>
              فهرست محصولات
            </h2>

            <div className="shop-toolbar">
              {!sidebar && (
                <button type="button" className="btn btn--secondary shop-toolbar__filters" aria-haspopup="dialog" onClick={() => setSheetOpen(true)} data-testid="shop-filter-open">
                  <SlidersHorizontal size={18} aria-hidden="true" />
                  فیلترها
                  {activeCount > 0 && <span className="shop-toolbar__badge">{activeCount}</span>}
                </button>
              )}
              <SortBar ordering={filters.ordering} onChange={(ordering) => update({ ordering })} />
            </div>

            <ActiveFilters filters={filters} brands={brands} onChange={removeFilter} onClear={clearFromPage} />

            <div className={`shop-results__body${refreshing ? " is-refreshing" : ""}`} aria-busy={refreshing} data-testid="shop-results-body">
              {refreshing && <span className="shop-progress" role="status" aria-label="در حال بارگذاری" data-testid="shop-progress" />}
              {body}
            </div>
          </section>
        </div>
      </div>

      {!sidebar && (
        <FilterSheet open={sheetOpen} onClose={closeSheet} activeCount={activeCount} onClear={clearFilters} applyLabel={applyLabel} onApply={() => applyPrice() && closeSheet()}>
          {panel}
        </FilterSheet>
      )}
    </main>
  );
}
