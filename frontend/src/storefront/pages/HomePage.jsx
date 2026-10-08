import { useMemo } from "react";
import { BRAND } from "../../shared/brand";
import { useApi } from "../../shared/useApi";
import { blogApi, catalogApi } from "../api/endpoints";
import { useDocumentTitle } from "../components/useDocumentTitle";
import BlogSection from "./home/BlogSection";
import BrandsSection from "./home/BrandsSection";
import CategoryGrid from "./home/CategoryGrid";
import CategoryLinks from "./home/CategoryLinks";
import CtaBand from "./home/CtaBand";
import HeroSection from "./home/HeroSection";
import ProductSection from "./home/ProductSection";
import PromoBanners from "./home/PromoBanners";
import "./home.css";

const CAROUSEL_PRODUCT_COUNT = 10;
const HOME_BLOG_COUNT = 6;
const HERO_SLIDE_COUNT = 3;
// The API cannot sort by discount, so ask for the most offers one page allows and sort them here.
const OFFER_POOL_SIZE = 48;

/** The products with the biggest discount that can still be bought, best first. */
function pickHeroProducts(products) {
  return products
    .filter((product) => Number(product.offer) > 0 && Number(product.product_number) > 0)
    .sort((a, b) => Number(b.offer) - Number(a.offer) || Number(b.product_rate) - Number(a.product_rate))
    .slice(0, HERO_SLIDE_COUNT);
}

export default function HomePage() {
  useDocumentTitle();

  const offers = useApi(() => catalogApi.products({ has_offer: 1, page_size: OFFER_POOL_SIZE }));
  const topRated = useApi(() => catalogApi.products({ ordering: "-product_rate", page_size: CAROUSEL_PRODUCT_COUNT }));
  const categories = useApi(catalogApi.categories);
  const brands = useApi(catalogApi.brands);
  const posts = useApi(() => blogApi.posts({ page_size: HOME_BLOG_COUNT }));

  const offerProducts = offers.data?.results;
  const heroProducts = useMemo(() => pickHeroProducts(offerProducts ?? []), [offerProducts]);
  const offerLoading = offers.loading && !offers.data;
  const topRatedLoading = topRated.loading && !topRated.data;

  return (
    <main className="page" data-testid="home-page">
      <h1 className="visually-hidden">
        {BRAND.name}، {BRAND.tagline}
      </h1>

      <div className="container">
        <HeroSection products={heroProducts} loading={offerLoading} />
        <CategoryLinks state={categories} />
        <PromoBanners />

        <ProductSection
          testId="home-offers"
          title="پیشنهاد شگفت‌انگیز"
          subtitle="تخفیف‌های امروز"
          to="/products?has_offer=1"
          products={(offerProducts ?? []).slice(0, CAROUSEL_PRODUCT_COUNT)}
          loading={offerLoading}
          error={offers.error}
          onRetry={offers.reload}
          countdown
        />
        <ProductSection
          testId="home-top-rated"
          title="پرامتیازترین‌ها"
          subtitle="بر اساس امتیاز خریداران"
          to="/products?ordering=-product_rate"
          products={topRated.data?.results ?? []}
          loading={topRatedLoading}
          error={topRated.error}
          onRetry={topRated.reload}
        />

        <CtaBand />
        <CategoryGrid state={categories} />
        <BrandsSection state={brands} />
        <BlogSection state={posts} />
      </div>
    </main>
  );
}
