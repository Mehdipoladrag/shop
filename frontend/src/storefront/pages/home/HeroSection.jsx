import { Link } from "react-router-dom";
import { ArrowLeft, PackageOpen, Sparkles } from "lucide-react";
import { BRAND } from "../../../shared/brand";
import Carousel from "../../components/Carousel";
import { formatPrice, toRelativeUrl } from "../../format";

const SLIDE_TONES = 3;

/** The shop's "T" mark drawn large, used when there is no product to show. */
function BrandMark() {
  return (
    <svg className="home-hero__mark" viewBox="0 0 40 40" aria-hidden="true">
      <rect className="home-hero__mark-bg" width="40" height="40" rx="12" />
      <path
        className="home-hero__mark-glyph"
        d="M11.5 13h17M20 13v16"
        fill="none"
        strokeWidth="3.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle className="home-hero__mark-dot" cx="30.5" cy="29" r="3.2" />
    </svg>
  );
}

function ProductSlide({ product, index }) {
  const url = `/products/${product.slug}`;
  return (
    <article className={`home-hero__slide home-hero__slide--${index % SLIDE_TONES}`} data-testid="home-hero-slide">
      <div className="home-hero__content">
        <span className="home-hero__kicker">
          <Sparkles size={16} aria-hidden="true" />
          پیشنهاد ویژه
        </span>
        <h2 className="home-hero__title">
          <Link to={url}>{product.product_name}</Link>
        </h2>
        {product.mini_description && <p className="home-hero__text">{product.mini_description}</p>}
        <div className="home-hero__buy">
          <div className="home-hero__price">
            <div className="home-hero__old">
              <del>{formatPrice(product.price)}</del>
              <span className="badge badge--discount">{Number(product.offer)}%</span>
            </div>
            <div className="home-hero__final">
              <strong>{formatPrice(product.final_price)}</strong>
              <span>تومان</span>
            </div>
          </div>
          <Link to={url} className="btn btn--accent btn--lg home-hero__cta" data-testid="home-hero-cta">
            مشاهده و خرید
            <ArrowLeft size={20} aria-hidden="true" />
          </Link>
        </div>
      </div>

      <div className="home-hero__art">
        <span className="home-hero__plate">
          {product.pic ? (
            <img src={toRelativeUrl(product.pic)} alt="" width="320" height="320" decoding="async" />
          ) : (
            <PackageOpen className="home-hero__fallback-icon" size={72} aria-hidden="true" />
          )}
        </span>
      </div>
    </article>
  );
}

function BrandSlide() {
  return (
    <article className="home-hero__slide home-hero__slide--0" data-testid="home-hero-slide">
      <div className="home-hero__content">
        <span className="home-hero__kicker">
          <Sparkles size={16} aria-hidden="true" />
          {BRAND.tagline}
        </span>
        <h2 className="home-hero__title">{BRAND.name}</h2>
        <p className="home-hero__text">گوشی، تبلت، لوازم جانبی و کنسول بازی را از یک‌جا ببینید و بخرید.</p>
        <div className="home-hero__buy">
          <Link to="/products" className="btn btn--accent btn--lg home-hero__cta" data-testid="home-hero-cta">
            مشاهده محصولات
            <ArrowLeft size={20} aria-hidden="true" />
          </Link>
        </div>
      </div>

      <div className="home-hero__art" aria-hidden="true">
        <span className="home-hero__plate">
          <BrandMark />
        </span>
      </div>
    </article>
  );
}

function HeroSkeleton() {
  return <div className="skeleton home-hero__skeleton" role="status" aria-label="در حال بارگذاری" data-testid="home-hero-loading" />;
}

/**
 * Top banner: one slide per product with a big discount, or a single brand
 * slide when the shop has no offers (or they could not be loaded).
 */
export default function HeroSection({ products, loading }) {
  return (
    <div className="home-hero" data-testid="home-hero">
      {loading ? (
        <HeroSkeleton />
      ) : (
        <Carousel variant="hero" autoplay dots label="پیشنهادهای ویژه">
          {products.length > 0
            ? products.map((product, index) => <ProductSlide product={product} index={index} key={product.id} />)
            : [<BrandSlide key="brand" />]}
        </Carousel>
      )}
    </div>
  );
}
