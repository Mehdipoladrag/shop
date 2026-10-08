import { Link } from "react-router-dom";
import { toRelativeUrl } from "../../format";
import SectionHeader from "../../components/SectionHeader";
import { BRAND } from "../../../shared/brand";
import { homeCategoryIcon } from "./categoryIcons";
import { SectionError } from "./SectionStates";

const SKELETON_COUNT = 6;

/** Grid of category cards: the category picture on a tinted tile, or its icon when it has none. */
export default function CategoryGrid({ state }) {
  const categories = state.data ?? [];
  const loading = state.loading && !state.data;
  if (!loading && !state.error && categories.length === 0) return null;

  let content;
  if (state.error) {
    content = <SectionError error={state.error} onRetry={state.reload} testId="home-category-grid-error" />;
  } else if (loading) {
    content = (
      <div className="home-catgrid" role="status" aria-label="در حال بارگذاری">
        {Array.from({ length: SKELETON_COUNT }, (_, index) => (
          <span className="skeleton home-catgrid__skeleton" key={index} />
        ))}
      </div>
    );
  } else {
    content = (
      <ul className="home-catgrid">
        {categories.map((category) => {
          const Icon = homeCategoryIcon(category);
          return (
            <li key={category.id}>
              <Link to={`/category/${category.category_slug}`} className="card home-catcard" data-testid="home-category-card">
                <span className="home-catcard__tile">
                  {category.category_pic ? (
                    <img src={toRelativeUrl(category.category_pic)} alt="" width="240" height="240" loading="lazy" decoding="async" />
                  ) : (
                    <Icon size={44} aria-hidden="true" />
                  )}
                </span>
                <span className="home-catcard__name">{category.category_name}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    );
  }

  return (
    <section className="section" data-testid="home-category-grid">
      <SectionHeader title={`دسته‌بندی‌های ${BRAND.name}`} />
      {content}
    </section>
  );
}
