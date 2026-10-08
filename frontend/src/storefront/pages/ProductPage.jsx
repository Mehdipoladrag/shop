import { useParams } from "react-router-dom";
import { catalogApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { useApi } from "../../shared/useApi";
import Breadcrumb from "../components/Breadcrumb";
import Carousel from "../components/Carousel";
import ProductCard from "../components/ProductCard";
import SectionHeader from "../components/SectionHeader";
import { LoadError, NotFound } from "../components/States";
import { useDocumentTitle } from "../components/useDocumentTitle";
import Gallery from "./product/Gallery";
import ProductSkeleton from "./product/ProductSkeleton";
import ProductSummary from "./product/ProductSummary";
import ProductTabs from "./product/ProductTabs";
import PurchaseCard from "./product/PurchaseCard";
import { PurchaseBar, PurchaseOptions } from "./product/PurchaseMobile";
import usePurchase from "./product/usePurchase";
import { useMediaQuery } from "./product/useMediaQuery";
import "./product.css";

// Phones get the purchase bar fixed to the bottom of the screen.
const PHONE_QUERY = "(max-width: 767px)";

function ProductDetail({ product, related }) {
  const phone = useMediaQuery(PHONE_QUERY);
  const purchase = usePurchase(product, { flashOnError: phone });
  const crumbs = [
    { label: product.category, to: `/category/${product.category_slug}` },
    { label: product.product_name },
  ];

  return (
    <main className="page product-view" data-testid="product-page">
      <div className="container">
        <Breadcrumb items={crumbs} />

        <article className="product-layout">
          <Gallery product={product} />
          <ProductSummary product={product} />
          {phone ? <PurchaseOptions product={product} purchase={purchase} /> : <PurchaseCard product={product} purchase={purchase} />}
        </article>

        <ProductTabs product={product} />

        {related.length > 0 && (
          <section className="section product-related" data-testid="product-related">
            <SectionHeader title="محصولات مرتبط" />
            <Carousel variant="cards" label="محصولات مرتبط">
              {related.map((item) => (
                <ProductCard product={item} key={item.id} />
              ))}
            </Carousel>
          </section>
        )}
      </div>

      {phone && <PurchaseBar product={product} purchase={purchase} />}
    </main>
  );
}

export default function ProductPage() {
  const { slug } = useParams();
  const state = useApi(() => catalogApi.product(slug).then((data) => ({ ...data, requestedSlug: slug })), [slug]);
  const notFound = state.error instanceof ApiError && state.error.status === 404;
  // While the next product loads the previous one is still in `state.data`; it must not stay on screen.
  const current = state.data?.requestedSlug === slug ? state.data : null;

  useDocumentTitle(current ? current.product.product_name : notFound ? "محصول پیدا نشد" : "محصول");

  if (notFound) {
    // The kit's NotFound has no h1 of its own, and every page needs exactly one.
    return (
      <>
        <h1 className="visually-hidden">محصول پیدا نشد</h1>
        <NotFound />
      </>
    );
  }
  if (state.error) {
    return (
      <main className="page">
        <LoadError error={state.error} onRetry={state.reload} />
      </main>
    );
  }
  if (!current) return <ProductSkeleton />;

  // `key` gives every product its own quantity, picture and tab state.
  return <ProductDetail key={current.product.id} product={current.product} related={current.related} />;
}
