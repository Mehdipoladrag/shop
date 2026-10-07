import { useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { catalogApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { toRelativeUrl } from "../format";
import { ProductBox } from "../components/ProductItem";
import Pagination from "../components/Pagination";
import { Loading, LoadError } from "../components/States";

const PAGE_SIZE = 12;
const CATEGORY_TILE_LIMIT = 12;

// Each tab of the listing is a sort order of the product API.
const SORT_TABS = [
  { ordering: "-product_rate", label: "پیشنهاد خریداران" },
  { ordering: "-create_date", label: "جدیدترین" },
  { ordering: "price", label: "ارزان‌ترین" },
  { ordering: "-price", label: "گران‌ترین" },
  { ordering: "time_send", label: "سریع‌ترین ارسال" },
];
const DEFAULT_ORDERING = SORT_TABS[0].ordering;

// Swatch colors for the usual Persian color names; unknown names get a neutral grey.
const COLOR_SWATCHES = {
  مشکی: "#000",
  سفید: "#fff",
  قرمز: "#ff0000",
  زرد: "#ffd800",
  آبی: "#0000ff",
  سبز: "#28a745",
  نقره‌ای: "#c0c0c0",
  طلایی: "#d4af37",
};
const FALLBACK_SWATCH = "#999";

const splitList = (value) => (value ? value.split(",") : []);

/** Toggles `item` in a comma separated URL value. */
function toggleListValue(current, item) {
  const values = splitList(current);
  const next = values.includes(item) ? values.filter((value) => value !== item) : [...values, item];
  return next.join(",");
}

function CategoryTiles({ categories }) {
  return (
    <div className="col-12 hidden-xs">
      <div className="brand-slider card border_all">
        <header className="card-header">
          <h3 className="card-title">
            <span>دسته بندی ها</span>
          </h3>
        </header>
        <div className="row">
          <div className="col-12">
            <div className="row">
              {categories.slice(0, CATEGORY_TILE_LIMIT).map((category) => (
                <div className="col-6 col-md-2 contact-bigicon" key={category.id}>
                  <Link to={`/category/${category.category_slug}`}>
                    <img className="img-responsive imgpad" src={toRelativeUrl(category.category_pic)} alt="" />
                    <b className="title-3 light-black">{category.category_name}</b>
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function FilterBox({ title, children }) {
  return (
    <div className="box">
      <header className="card-header">
        <h3 className="card-title">
          <span className="space-right-10">{title}</span>
        </h3>
      </header>
      <div className="box-content">{children}</div>
    </div>
  );
}

function CheckboxRow({ id, label, checked, onChange, swatch }) {
  return (
    <div className="form-account-agree">
      <label className="checkbox-form checkbox-primary">
        <input type="checkbox" id={id} checked={checked} onChange={onChange} />
        <span className="checkbox-check" />
      </label>
      <label htmlFor={id}>{label}</label>
      {swatch && <span className="color_pro_sel" style={{ backgroundColor: swatch }} />}
    </div>
  );
}

function PriceFilter({ range, minPrice, maxPrice, onApply }) {
  const [min, setMin] = useState(minPrice);
  const [max, setMax] = useState(maxPrice);

  // Keep the inputs in sync when the URL changes (for example "clear filters").
  useEffect(() => {
    setMin(minPrice);
    setMax(maxPrice);
  }, [minPrice, maxPrice]);

  function handleSubmit(event) {
    event.preventDefault();
    onApply(min, max);
  }

  return (
    <form className="box-content space-15" onSubmit={handleSubmit}>
      <input
        type="number"
        min="0"
        className="input_second input_all"
        placeholder={`از ${Math.round(range.min_price)} تومان`}
        aria-label="حداقل قیمت"
        value={min}
        onChange={(event) => setMin(event.target.value)}
      />
      <input
        type="number"
        min="0"
        className="input_second input_all"
        style={{ marginTop: 8 }}
        placeholder={`تا ${Math.round(range.max_price)} تومان`}
        aria-label="حداکثر قیمت"
        value={max}
        onChange={(event) => setMax(event.target.value)}
      />
      <button type="submit" className="btn btn-main-masai" style={{ marginTop: 8 }}>
        اعمال
      </button>
    </form>
  );
}

/**
 * Product listing used by three routes: all products, one category and search
 * results. Filters, sort order and page live in the URL, so every view can be
 * shared and the back button works.
 */
export default function ShopPage({ mode }) {
  const { slug } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const query = searchParams.get("q") ?? "";
  const page = Number(searchParams.get("page")) || 1;
  const ordering = searchParams.get("ordering") || DEFAULT_ORDERING;
  const brandIds = searchParams.get("brand") ?? "";
  const colors = searchParams.get("color") ?? "";
  const minPrice = searchParams.get("min_price") ?? "";
  const maxPrice = searchParams.get("max_price") ?? "";
  const inStock = searchParams.get("in_stock") === "1";

  const categories = useApi(catalogApi.categories);
  const brands = useApi(catalogApi.brands);
  const filters = useApi(catalogApi.productFilters);

  const products = useApi(
    () =>
      catalogApi.products({
        category: mode === "category" ? slug : undefined,
        search: mode === "search" ? query : undefined,
        page,
        page_size: PAGE_SIZE,
        ordering,
        brand: brandIds,
        color: colors,
        min_price: minPrice,
        max_price: maxPrice,
        in_stock: inStock ? 1 : undefined,
      }),
    [mode, slug, query, page, ordering, brandIds, colors, minPrice, maxPrice, inStock]
  );

  // Changing a filter or the sort order always returns to the first page.
  function updateParams(changes, { keepPage = false } = {}) {
    const next = new URLSearchParams(searchParams);
    Object.entries(changes).forEach(([key, value]) => {
      if (value === "" || value === undefined || value === null) next.delete(key);
      else next.set(key, value);
    });
    if (!keepPage) next.delete("page");
    setSearchParams(next);
  }

  const categoryName = categories.data?.find((category) => category.category_slug === slug)?.category_name;
  const heading =
    mode === "search" ? `نتایج جستجو برای «${query}»` : mode === "category" ? categoryName : null;
  const pageCount = Math.ceil((products.data?.count ?? 0) / PAGE_SIZE);

  return (
    <main className="search-page default space-top-30">
      <div className="container">
        <div className="row">
          {mode !== "search" && categories.data && <CategoryTiles categories={categories.data} />}

          <aside className="sidebar-page col-12 col-sm-12 col-md-4 col-lg-3">
            {filters.data?.colors.length > 0 && (
              <FilterBox title="رنگ">
                {filters.data.colors.map((color) => (
                  <CheckboxRow
                    key={color}
                    id={`color-${color}`}
                    label={color}
                    swatch={COLOR_SWATCHES[color] ?? FALLBACK_SWATCH}
                    checked={splitList(colors).includes(color)}
                    onChange={() => updateParams({ color: toggleListValue(colors, color) })}
                  />
                ))}
              </FilterBox>
            )}

            {filters.data && (
              <div className="box">
                <header className="card-header">
                  <h3 className="card-title">
                    <span className="space-right-10">قیمت</span>
                  </h3>
                </header>
                <PriceFilter
                  range={filters.data}
                  minPrice={minPrice}
                  maxPrice={maxPrice}
                  onApply={(min, max) => updateParams({ min_price: min, max_price: max })}
                />
              </div>
            )}

            {brands.data?.length > 0 && (
              <FilterBox title="لیست برند ها">
                {brands.data.map((brand) => (
                  <CheckboxRow
                    key={brand.id}
                    id={`brand-${brand.id}`}
                    label={brand.brand_name}
                    checked={splitList(brandIds).includes(String(brand.id))}
                    onChange={() => updateParams({ brand: toggleListValue(brandIds, String(brand.id)) })}
                  />
                ))}
              </FilterBox>
            )}

            <div className="box">
              <div className="box-content">
                <CheckboxRow
                  id="in-stock"
                  label="موجود در انبار مسای"
                  checked={inStock}
                  onChange={() => updateParams({ in_stock: inStock ? "" : "1" })}
                />
              </div>
            </div>
          </aside>

          <div className="col-12 col-sm-12 col-md-8 col-lg-9">
            <div className="listing default">
              {heading && (
                <header className="card-header">
                  <h3 className="card-title">
                    <span>{heading}</span>
                  </h3>
                </header>
              )}
              <div className="listing-header default marg_all0">
                <ul className="Search_list nav nav-tabs" role="tablist">
                  {SORT_TABS.map((tab) => (
                    <li key={tab.ordering}>
                      <a
                        href={`?ordering=${tab.ordering}`}
                        className={ordering === tab.ordering ? "active" : ""}
                        role="tab"
                        aria-selected={ordering === tab.ordering}
                        onClick={(event) => {
                          event.preventDefault();
                          updateParams({ ordering: tab.ordering });
                        }}
                      >
                        {tab.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="tab-content default text-center">
                <div className="tab-pane active" role="tabpanel">
                  {products.loading && !products.data && <Loading />}
                  {products.error && <LoadError error={products.error} onRetry={products.reload} />}
                  {products.data && (
                    <div className="row listing-items">
                      {products.data.results.map((product) => (
                        <ProductBox product={product} key={product.id} />
                      ))}
                      {products.data.results.length === 0 && (
                        <p className="col-12" style={{ padding: "60px 0", color: "#46A9AE" }}>
                          محصولی با این مشخصات پیدا نشد.
                        </p>
                      )}
                    </div>
                  )}
                </div>
              </div>

              <div className="row">
                <div className="col-sm-9 padding-right">
                  <Pagination
                    page={page}
                    pageCount={pageCount}
                    onChange={(target) => updateParams({ page: String(target) }, { keepPage: true })}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
