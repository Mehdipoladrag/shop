import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { catalogApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { useCart } from "../cart/CartContext";
import { toRelativeUrl } from "../format";
import Carousel from "../components/Carousel";
import Countdown from "../components/Countdown";
import Price from "../components/Price";
import { ProductItem } from "../components/ProductItem";
import { AsyncContent, NotFound } from "../components/States";
import { ApiError } from "../api/client";

const QUANTITY_OPTIONS = Array.from({ length: 9 }, (_, index) => index + 1);
const MAX_RATE = 10;

const RELATED_RESPONSIVE = {
  0: { items: 2, slideBy: 1 },
  768: { items: 4, slideBy: 2 },
  992: { items: 4, slideBy: 2 },
};

function SpecList({ product }) {
  return (
    <>
      <li className="list-group-item">رنگ: {product.product_color}</li>
      <li className="list-group-item">بلوتوث: {product.bluetooth}</li>
      <li className="list-group-item">رزولوشن عکس : {product.resolution} مگاپیکسل</li>
      <li className="list-group-item">
        امتیاز کاربران : {product.product_rate}/{MAX_RATE}
      </li>
      <li className="list-group-item">قابلیت : {product.capability}</li>
      <li className="list-group-item">سیستم عامل : {product.platform_os}</li>
      <li className="list-group-item">فناوری : {product.technology}</li>
    </>
  );
}

function Gallery({ product }) {
  const [activeImage, setActiveImage] = useState(0);
  const images = product.images.map(toRelativeUrl);
  const [favorite, setFavorite] = useState(false);

  // Switching to another product shows its first picture again.
  useEffect(() => setActiveImage(0), [product.id]);

  return (
    <div className="product-gallery default">
      <img className="main_img_gallery" src={images[activeImage]} alt={product.product_name} />
      {images.length > 1 && (
        <section className="testimonial py-3">
          <div className="row gallery">
            {images.map((image, position) => (
              <div className="col-4 col-md-3 pd" key={image}>
                <a
                  href={image}
                  onClick={(event) => {
                    event.preventDefault();
                    setActiveImage(position);
                  }}
                >
                  <img src={image} className="img-thumb" alt={`${product.product_name} ${position + 1}`} />
                </a>
              </div>
            ))}
          </div>
        </section>
      )}
      <ul className="gallery-options">
        <li>
          <button
            type="button"
            className={`add-favorites favorites2 favorites_heart${favorite ? " favorites" : ""}`}
            aria-label="افزودن به علاقه‌مندی‌ها"
            onClick={() => setFavorite(!favorite)}
          >
            <i className="fa fa-heart" />
          </button>
        </li>
      </ul>
    </div>
  );
}

function AddToCart({ product }) {
  const { addItem } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [status, setStatus] = useState("idle");

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("saving");
    try {
      await addItem(product.id, quantity);
      setStatus("added");
    } catch {
      setStatus("error");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="tedad">
        <p>
          <label htmlFor="product-quantity">تعداد: </label>{" "}
          <select id="product-quantity" value={quantity} onChange={(event) => setQuantity(Number(event.target.value))}>
            {QUANTITY_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </p>
      </div>
      <button type="submit" className="btn big_btn btn-main-masai" disabled={status === "saving"}>
        افزودن به سبد خرید
      </button>
      {status === "added" && (
        <p className="txt_note" role="status">
          به سبد خرید اضافه شد. <Link to="/cart">مشاهده سبد</Link>
        </p>
      )}
      {status === "error" && <p className="txt_note" role="alert">افزودن به سبد انجام نشد. دوباره تلاش کنید.</p>}
    </form>
  );
}

function ProductDetail({ product, related }) {
  const [tab, setTab] = useState("desc");

  return (
    <main className="single-product default">
      <div className="container">
        <div className="row">
          <div className="col-12">
            <nav>
              <ul className="breadcrumb">
                <Link to="/">
                  <li>
                    <i className="fa fa-home" aria-hidden="true" />
                  </li>
                </Link>
                <li>
                  <Link to={`/category/${product.category_slug}`}>
                    <span>{product.category}</span>
                  </Link>
                </li>
                <li>
                  <span>{product.brand}</span>
                </li>
                <li>
                  <span>{product.product_name}</span>
                </li>
              </ul>
            </nav>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <article className="product">
              <div className="row product_main_details">
                <div className="col-lg-5 col-md-6 col-sm-12">
                  <Gallery product={product} />
                </div>
                <div className="col-lg-7 col-md-6 col-sm-12">
                  <div className="product-title">
                    <h1>{product.product_name}</h1>
                  </div>
                  <hr className="hr-text" data-content={product.mini_description} />
                  <div className="row">
                    <div className="col-6">
                      <ul className="list-group space-15">
                        <li className="list-group-item">رنگ: {product.product_color}</li>
                        <li className="list-group-item">بلوتوث: {product.bluetooth}</li>
                        <li className="list-group-item">رزولوشن عکس : {product.resolution} مگاپیکسل</li>
                        <li className="list-group-item">
                          امتیاز کاربران : {product.product_rate}/{MAX_RATE}
                        </li>
                      </ul>
                    </div>
                    <div className="col-6">
                      <ul className="list-group space-15">
                        <li className="list-group-item">قابلیت : {product.capability}</li>
                        <li className="list-group-item">سیستم عامل : {product.platform_os}</li>
                        <li className="list-group-item">فناوری : {product.technology}</li>
                        <li className="list-group-item">
                          موجودی : {product.product_number > 0 ? `${product.product_number} عدد` : "ناموجود"}
                        </li>
                      </ul>
                    </div>
                    <div className="col-lg-12 col-md-12 col-sm-12 product_main_pr">
                      <div className="time_pr">
                        <div className="row">
                          <div className="col-12 upda">
                            <b>
                              <i className="fa fa-calendar" aria-hidden="true" /> زمان ارسال محصول :{" "}
                            </b>
                            {product.time_send} روز
                          </div>
                          <div className="col-12 col-lg-6 col-md-6">
                            {product.offer > 0 && (
                              <>
                                <p>زمان باقی مانده </p>
                                <Countdown />
                              </>
                            )}
                          </div>
                          <div className="col-12 col-lg-6 col-md-6 border_left">
                            <div className="price space-15">
                              <Price product={product} />
                            </div>
                            <div className="col-12 timer-title text--center">
                              {product.product_number > 0 ? (
                                <AddToCart product={product} />
                              ) : (
                                <p className="txt_note">این محصول در حال حاضر ناموجود است.</p>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    {product.notice && (
                      <div className="col-12">
                        <p className="txt_note">
                          <i className="fa fa-info" aria-hidden="true" /> {product.notice}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>

      <div className="container">
        <div className="row">
          <div className="col-12 default no-padding bg_single_product">
            <div className="product-tabs default">
              <div className="box-tabs default">
                <ul className="nav" role="tablist">
                  {[
                    ["desc", "توضیحات تکمیلی"],
                    ["params", "مشخصات محصول"],
                  ].map(([key, label]) => (
                    <li className="box-tabs-tab" key={key}>
                      <a
                        href={`#${key}`}
                        className={tab === key ? "active" : ""}
                        role="tab"
                        aria-selected={tab === key}
                        onClick={(event) => {
                          event.preventDefault();
                          setTab(key);
                        }}
                      >
                        {label}
                      </a>
                    </li>
                  ))}
                </ul>
                <div className="card-body default">
                  <div className="tab-content">
                    {tab === "desc" ? (
                      <div className="tab-pane active" role="tabpanel">
                        <header className="card-header">
                          <h3 className="card-title">
                            <span>بررسی تخصصی {product.product_name}</span>
                          </h3>
                        </header>
                        <div className="parent-expert default">
                          <div className="content-expert">
                            <p style={{ whiteSpace: "pre-line" }}>{product.product_description}</p>
                            <p style={{ whiteSpace: "pre-line" }}>{product.specifications}</p>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="tab-pane active params" role="tabpanel">
                        <header className="card-header">
                          <h3 className="card-title">
                            <span>مشخصات {product.product_name}</span>
                          </h3>
                        </header>
                        <div className="col-12">
                          <ul className="list-group">
                            <SpecList product={product} />
                          </ul>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {related.length > 0 && (
          <div className="row">
            <div className="col-12">
              <div className="widget widget-product card border_all bglight">
                <header className="card-header">
                  <h3 className="card-title">
                    <span>محصولات مرتبط</span>
                  </h3>
                </header>
                <Carousel className="product-carousel" responsive={RELATED_RESPONSIVE} margin={10} nav>
                  {related.map((item) => (
                    <ProductItem product={item} key={item.id} />
                  ))}
                </Carousel>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

export default function ProductPage() {
  const { slug } = useParams();
  const state = useApi(() => catalogApi.product(slug), [slug]);

  if (state.error instanceof ApiError && state.error.status === 404) return <NotFound />;

  return (
    <AsyncContent state={state}>
      {({ product, related }) => <ProductDetail product={product} related={related} />}
    </AsyncContent>
  );
}
