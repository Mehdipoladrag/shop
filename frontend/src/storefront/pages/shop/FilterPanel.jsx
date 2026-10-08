import { Link } from "react-router-dom";
import { LayoutGrid } from "lucide-react";
import FormField from "../../components/FormField";
import { formatPrice } from "../../format";
import FilterGroup from "./FilterGroup";
import { shopCategoryIcon } from "./categoryIcon";
import { cleanPriceInput, showPriceInput, toggleListValue } from "./filterState";
import { swatchColor } from "./swatches";

function SwitchRow({ label, checked, onChange, testId }) {
  return (
    <label className="shop-switch">
      <span>{label}</span>
      <input type="checkbox" role="switch" className="shop-switch__input" checked={checked} onChange={onChange} data-testid={testId} />
    </label>
  );
}

function CategoryLinks({ categories, mode, slug, onNavigate }) {
  return (
    <ul className="shop-cats">
      <li>
        <Link
          to="/products"
          className={`shop-cat${mode === "all" ? " is-active" : ""}`}
          aria-current={mode === "all" ? "page" : undefined}
          onClick={onNavigate}
          data-testid="shop-filter-category-all"
        >
          <LayoutGrid size={18} aria-hidden="true" />
          <span>همه محصولات</span>
        </Link>
      </li>
      {categories.map((category) => {
        const Icon = shopCategoryIcon(category);
        const active = mode === "category" && category.category_slug === slug;
        return (
          <li key={category.id}>
            <Link
              to={`/category/${category.category_slug}`}
              className={`shop-cat${active ? " is-active" : ""}`}
              aria-current={active ? "page" : undefined}
              onClick={onNavigate}
              data-testid={`shop-filter-category-${category.category_slug}`}
            >
              <Icon size={18} aria-hidden="true" />
              <span>{category.category_name}</span>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

function PriceForm({ range, price, onPriceChange, onPriceApply }) {
  const hasRange = range && Number(range.max_price) > 0;
  return (
    <form
      className="shop-price"
      onSubmit={(event) => {
        event.preventDefault();
        onPriceApply();
      }}
      data-testid="shop-filter-price"
    >
      <div className="shop-price__fields">
        <FormField
          label="حداقل قیمت"
          inputMode="numeric"
          autoComplete="off"
          placeholder={hasRange ? formatPrice(range.min_price) : "0"}
          value={showPriceInput(price.min)}
          onChange={(event) => onPriceChange("min", cleanPriceInput(event.target.value))}
          aria-invalid={Boolean(price.error)}
          data-testid="shop-filter-min-price"
        />
        <FormField
          label="حداکثر قیمت"
          inputMode="numeric"
          autoComplete="off"
          placeholder={hasRange ? formatPrice(range.max_price) : "0"}
          value={showPriceInput(price.max)}
          onChange={(event) => onPriceChange("max", cleanPriceInput(event.target.value))}
          aria-invalid={Boolean(price.error)}
          data-testid="shop-filter-max-price"
        />
      </div>
      {price.error ? (
        <p className="shop-price__error" role="alert">
          {price.error}
        </p>
      ) : (
        hasRange && (
          <p className="shop-price__range">
            قیمت کالاها از {formatPrice(range.min_price)} تا {formatPrice(range.max_price)} تومان است.
          </p>
        )
      )}
      <button type="submit" className="btn btn--secondary btn--sm btn--block" data-testid="shop-filter-price-apply">
        اعمال
      </button>
    </form>
  );
}

/**
 * Every filter of the shop listing. It is drawn once: in the sticky sidebar on
 * wide screens and inside the bottom sheet on small ones. All changes go
 * through `onChange(urlChanges)`, so the URL stays the source of truth.
 */
export default function FilterPanel({ mode, slug, filters, categories, brands, options, price, onChange, onPriceChange, onPriceApply, onNavigate }) {
  const colors = options.data?.colors ?? [];
  const showCategories = mode !== "search" && (categories.error || !categories.data || categories.data.length > 0);
  const showBrands = brands.error || !brands.data || brands.data.length > 0;
  const showColors = options.error || !options.data || colors.length > 0;

  return (
    <div className="shop-panel" data-testid="shop-filter-panel">
      <div className="shop-panel__quick">
        <SwitchRow
          label="فقط کالاهای موجود"
          checked={filters.inStock}
          onChange={() => onChange({ in_stock: filters.inStock ? "" : "1" })}
          testId="shop-filter-in-stock"
        />
        <SwitchRow
          label="فقط تخفیف‌دار"
          checked={filters.hasOffer}
          onChange={() => onChange({ has_offer: filters.hasOffer ? "" : "1" })}
          testId="shop-filter-has-offer"
        />
      </div>

      {showCategories && (
        <FilterGroup title="دسته‌بندی" state={categories} testId="shop-filter-categories">
          {(list) => <CategoryLinks categories={list} mode={mode} slug={slug} onNavigate={onNavigate} />}
        </FilterGroup>
      )}

      {showBrands && (
        <FilterGroup title="برند" state={brands} testId="shop-filter-brands">
          {(list) => (
            <ul className="shop-options">
              {list.map((brand) => (
                <li key={brand.id}>
                  <label className="check shop-option">
                    <input
                      type="checkbox"
                      checked={filters.brands.includes(String(brand.id))}
                      onChange={() => onChange({ brand: toggleListValue(filters.brand, String(brand.id)) })}
                      data-testid={`shop-filter-brand-${brand.id}`}
                    />
                    <span>{brand.brand_name}</span>
                  </label>
                </li>
              ))}
            </ul>
          )}
        </FilterGroup>
      )}

      {showColors && (
        <FilterGroup title="رنگ" state={options} testId="shop-filter-colors">
          {(data) => (
            <ul className="shop-swatches">
              {data.colors.map((color) => (
                <li key={color}>
                  <label className="shop-swatch" style={{ "--swatch": swatchColor(color) }}>
                    <input
                      type="checkbox"
                      className="shop-swatch__input"
                      checked={filters.colors.includes(color)}
                      onChange={() => onChange({ color: toggleListValue(filters.color, color) })}
                      data-testid={`shop-filter-color-${color}`}
                    />
                    <span className="shop-swatch__chip">
                      <span className="shop-swatch__dot" aria-hidden="true" />
                      {color}
                    </span>
                  </label>
                </li>
              ))}
            </ul>
          )}
        </FilterGroup>
      )}

      <FilterGroup title="بازه قیمت" testId="shop-filter-price-group">
        <PriceForm range={options.data} price={price} onPriceChange={onPriceChange} onPriceApply={onPriceApply} />
      </FilterGroup>
    </div>
  );
}
