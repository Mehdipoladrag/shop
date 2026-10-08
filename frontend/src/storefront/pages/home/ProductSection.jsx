import Carousel from "../../components/Carousel";
import Countdown from "../../components/Countdown";
import ProductCard from "../../components/ProductCard";
import SectionHeader from "../../components/SectionHeader";
import { RowSkeleton, SectionError } from "./SectionStates";

/**
 * A titled carousel of product cards. While the products load it shows
 * skeleton cards, when they fail a retry box, and with no products it renders
 * nothing at all.
 */
export default function ProductSection({ testId, title, subtitle, to, products, loading, error, onRetry, countdown = false }) {
  if (!loading && !error && products.length === 0) return null;

  let content;
  if (error) {
    content = <SectionError error={error} onRetry={onRetry} testId={`${testId}-error`} />;
  } else if (loading) {
    content = <RowSkeleton variant="cards" count={6} itemClassName="home-skeleton__product" />;
  } else {
    content = (
      <Carousel variant="cards" label={title}>
        {products.map((product) => (
          <ProductCard product={product} key={product.id} />
        ))}
      </Carousel>
    );
  }

  return (
    <section className="section" data-testid={testId}>
      <SectionHeader title={title} subtitle={subtitle} to={to}>
        {countdown && !error && (
          <div className="home-countdown" data-testid={`${testId}-countdown`}>
            <Countdown tone="dark" />
          </div>
        )}
      </SectionHeader>
      {content}
    </section>
  );
}
