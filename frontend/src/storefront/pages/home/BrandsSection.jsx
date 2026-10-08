import { Link } from "react-router-dom";
import Carousel from "../../components/Carousel";
import SectionHeader from "../../components/SectionHeader";
import { toRelativeUrl } from "../../format";
import { RowSkeleton, SectionError } from "./SectionStates";

/** Brand cards: the logo in grey that turns to colour on hover, or the brand name as text. Each opens that brand's products. */
export default function BrandsSection({ state }) {
  const brands = state.data ?? [];
  const loading = state.loading && !state.data;
  if (!loading && !state.error && brands.length === 0) return null;

  let content;
  if (state.error) {
    content = <SectionError error={state.error} onRetry={state.reload} testId="home-brands-error" />;
  } else if (loading) {
    content = <RowSkeleton variant="brands" count={7} itemClassName="home-skeleton__brand" />;
  } else {
    content = (
      <Carousel variant="brands" label="برندها">
        {brands.map((brand) => (
          <Link to={`/products?brand=${brand.id}`} className="home-brand" key={brand.id} data-testid="home-brand">
            {brand.brand_pic ? (
              <img src={toRelativeUrl(brand.brand_pic)} alt={brand.brand_name} width="160" height="56" loading="lazy" decoding="async" />
            ) : (
              <span className="home-brand__name">{brand.brand_name}</span>
            )}
          </Link>
        ))}
      </Carousel>
    );
  }

  return (
    <section className="section home-brands" data-testid="home-brands">
      <SectionHeader title="محبوب‌ترین برندها" />
      {content}
    </section>
  );
}
