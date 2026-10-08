import { X } from "lucide-react";
import { formatPrice } from "../../format";
import { toggleListValue } from "./filterState";

/** Text of the price chip: "از X تا Y تومان", or one side only. */
function priceLabel(minPrice, maxPrice) {
  const from = minPrice ? `از ${formatPrice(minPrice)}` : "";
  const to = maxPrice ? `تا ${formatPrice(maxPrice)}` : "";
  return `قیمت: ${[from, to].filter(Boolean).join(" ")} تومان`;
}

/** Chips for every filter that is switched on, each removable, plus "clear all". */
export default function ActiveFilters({ filters, brands, onChange, onClear }) {
  const chips = [];

  filters.brands.forEach((id) => {
    const name = brands.data?.find((brand) => String(brand.id) === id)?.brand_name;
    // While the brand list loads its names are unknown; the chip appears once they are.
    if (name || brands.data || brands.error) {
      chips.push({ key: `brand:${id}`, label: `برند: ${name ?? "ناشناخته"}`, remove: { brand: toggleListValue(filters.brand, id) } });
    }
  });
  filters.colors.forEach((color) => {
    chips.push({ key: `color:${color}`, label: `رنگ: ${color}`, remove: { color: toggleListValue(filters.color, color) } });
  });
  if (filters.minPrice || filters.maxPrice) {
    chips.push({ key: "price", label: priceLabel(filters.minPrice, filters.maxPrice), remove: { min_price: "", max_price: "" } });
  }
  if (filters.inStock) chips.push({ key: "in_stock", label: "فقط کالاهای موجود", remove: { in_stock: "" } });
  if (filters.hasOffer) chips.push({ key: "has_offer", label: "فقط تخفیف‌دار", remove: { has_offer: "" } });

  if (chips.length === 0) return null;

  return (
    <div className="shop-active" role="group" aria-label="فیلترهای فعال" data-testid="shop-active-filters">
      <button type="button" className="link-button shop-active__clear" onClick={onClear} data-testid="shop-clear-all">
        پاک کردن همه
      </button>
      {chips.map((chip) => (
        <button
          type="button"
          className="shop-chip"
          key={chip.key}
          aria-label={`حذف فیلتر ${chip.label}`}
          onClick={() => onChange(chip.remove)}
          data-testid="shop-active-filter"
          data-filter={chip.key}
        >
          <span>{chip.label}</span>
          <X size={14} aria-hidden="true" />
        </button>
      ))}
    </div>
  );
}
