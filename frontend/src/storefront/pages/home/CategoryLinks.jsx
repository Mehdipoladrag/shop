import { Link } from "react-router-dom";
import { LayoutGrid } from "lucide-react";
import { homeCategoryIcon } from "./categoryIcons";

const SKELETON_COUNT = 7;

/** Round icon shortcuts to every category, plus one to the whole catalog. */
export default function CategoryLinks({ state }) {
  const categories = state.data ?? [];

  if (state.loading && !state.data) {
    return (
      <div className="home-cats" role="status" aria-label="در حال بارگذاری">
        <div className="home-cats__list" data-allow-overflow>
          {Array.from({ length: SKELETON_COUNT }, (_, index) => (
            <div className="home-cats__item" key={index}>
              <span className="skeleton home-cats__circle-skeleton" />
              <span className="skeleton home-cats__label-skeleton" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  // A failed request is reported once, by the category grid further down.
  if (state.error || categories.length === 0) return null;

  return (
    <nav className="home-cats" aria-label="دسته‌بندی‌های محصولات" data-testid="home-categories">
      <ul className="home-cats__list" data-allow-overflow>
        {categories.map((category) => {
          const Icon = homeCategoryIcon(category);
          return (
            <li key={category.id}>
              <Link to={`/category/${category.category_slug}`} className="home-cats__item" data-testid="home-category-link">
                <span className="home-cats__icon">
                  <Icon size={28} aria-hidden="true" />
                </span>
                <span className="home-cats__label">{category.category_name}</span>
              </Link>
            </li>
          );
        })}
        <li>
          <Link to="/products" className="home-cats__item" data-testid="home-all-products-link">
            <span className="home-cats__icon home-cats__icon--all">
              <LayoutGrid size={28} aria-hidden="true" />
            </span>
            <span className="home-cats__label">همه محصولات</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
}
