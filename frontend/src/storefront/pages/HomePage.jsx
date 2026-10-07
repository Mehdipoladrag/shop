import { Link } from "react-router-dom";
import { blogApi, catalogApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { staticUrl } from "../config";
import { formatJalaliDate, toRelativeUrl } from "../format";
import Carousel from "../components/Carousel";
import Countdown from "../components/Countdown";
import { ProductItem } from "../components/ProductItem";

const HERO_SLIDES = [
  { image: "banner_img/01/16781944460617.jpg", to: "/products" },
  { image: "banner_img/01/16785213091818.jpg", to: "/products" },
  { image: "banner_img/01/16789575390919.jpg", to: "/categories" },
];

const MINI_LOGOS = [
  ["1.png", "مَسای مارکت"],
  ["2.png", "حراج مَسای"],
  ["3.png", "خرید اقساطی"],
  ["4.png", "مَسای سرویس"],
  ["5.png", "ماه رمضان"],
  ["6.png", "مَسای پلاس"],
  ["7.png", "هدیه خرید"],
  ["8.png", "بیشتر"],
];

const HERO_RESPONSIVE = {
  0: { items: 1, dots: false },
  767: { items: 1, dots: true },
  1200: { items: 1, dots: true },
};

const PRODUCT_RESPONSIVE = {
  0: { items: 2, slideBy: 1 },
  576: { items: 2, slideBy: 1 },
  768: { items: 4, slideBy: 2 },
  992: { items: 5, slideBy: 2 },
  1400: { items: 6, slideBy: 3 },
};

const BLOG_RESPONSIVE = {
  0: { items: 2, slideBy: 1 },
  576: { items: 2, slideBy: 1 },
  768: { items: 3, slideBy: 2 },
  992: { items: 4, slideBy: 2 },
  1400: { items: 4, slideBy: 3 },
};

const BRAND_RESPONSIVE = {
  0: { items: 1 },
  480: { items: 2 },
  600: { items: 3 },
  768: { items: 5 },
  992: { items: 6 },
  1200: { items: 7 },
};

const CAROUSEL_PRODUCT_COUNT = 8;
const HOME_BLOG_COUNT = 6;

// The curved white notch drawn on top of every hero banner by the theme.
function HeroNotch() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="svg_Masai"
      width="231"
      height="75"
      viewBox="0 0 231 75"
      fill="none"
      style={{ float: "right", marginBottom: -100, position: "relative", zIndex: 9, marginTop: 0, marginRight: 30 }}
    >
      <path
        clipRule="evenodd"
        d="M0 0C31.5006 0.949537 50.52 17.872 56.1955 26.4544L55.986 25.8011L82.4924 58.631C99.3032 79.4521 131.038 79.4521 147.849 58.6309L174.356 25.8011L174.146 26.4544C179.822 17.872 198.844 0.949537 230.349 0H0Z"
        fill="#FCFCFC"
        style={{ fill: "#fff" }}
      />
    </svg>
  );
}

function Banner({ image, bordered, className = "col-6 col-lg-3" }) {
  return (
    <div className={className}>
      <div className={`widget-banner card${bordered ? " border_all" : ""}`}>
        <img className="img-fluid" src={staticUrl(`img/banner_img/${image}`)} alt="" />
      </div>
    </div>
  );
}

function ProductWidget({ titleImage, products, id, countdown }) {
  return (
    <div className="row">
      <div className="col-12">
        <div className={`widget widget-product card border_all bglight${countdown ? " pad_time_prod" : ""}`} id={id}>
          <header className="card-header">
            <h3 className="card-title">
              <span>
                <img src={staticUrl(`img/${titleImage}`)} alt="" />
              </span>
            </h3>
            {countdown && <Countdown />}
          </header>
          <Carousel className="product-carousel" responsive={PRODUCT_RESPONSIVE} margin={10} nav>
            {products.map((product) => (
              <ProductItem product={product} key={product.id} />
            ))}
          </Carousel>
          <Link to="/products" className="view_more">
            مشاهده بیشتر
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  const offers = useApi(() => catalogApi.products({ has_offer: 1, page_size: CAROUSEL_PRODUCT_COUNT }));
  const topRated = useApi(() => catalogApi.products({ ordering: "-product_rate", page_size: CAROUSEL_PRODUCT_COUNT }));
  const categories = useApi(catalogApi.categories);
  const brands = useApi(catalogApi.brands);
  const posts = useApi(() => blogApi.posts({ page_size: HOME_BLOG_COUNT }));

  return (
    <main className="main default space-top-10">
      <div className="container-fluid">
        <Carousel
          className="slider_main"
          responsive={HERO_RESPONSIVE}
          nav
          dots
          loop
          autoplay
          navText={[
            <div className="nav-btn prev-slide" key="prev">
              <i className="fa fa-chevron-right" />
            </div>,
            <div className="nav-btn next-slide" key="next">
              <i className="fa fa-chevron-left" />
            </div>,
          ]}
        >
          {HERO_SLIDES.map((slide) => (
            <div className="item" key={slide.image}>
              <HeroNotch />
              <Link to={slide.to}>
                <img src={staticUrl(`img/${slide.image}`)} className="img-fluid imgslider" alt="" />
              </Link>
            </div>
          ))}
        </Carousel>
      </div>

      <div className="container space-top-50">
        <div className="row space-bottom-30">
          {[MINI_LOGOS.slice(0, 4), MINI_LOGOS.slice(4)].map((group) => (
            <div className="col-sm-6" key={group[0][0]}>
              <div className="row">
                {group.map(([icon, label]) => (
                  <div className="col-3 contact-miniicon text-center" key={icon}>
                    <div className="space-5">
                      <img src={staticUrl(`img/Masai/minilogo/${icon}`)} className="minilogo_w" alt="" />
                      <b className="title-3 light-black">{label}</b>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="row">
          <div className="col-12">
            <div className="row banner-ads">
              <div className="col-12">
                <div className="row">
                  <Banner image="img-3.jpg" bordered />
                  <Banner image="img-4.jpg" />
                  <Banner image="img-5.jpg" bordered />
                  <Banner image="img-6.jpg" />
                </div>
              </div>
            </div>
          </div>

          <div className="col-12">
            <ProductWidget id="shegeft_1" titleImage="shegeft_1.png" products={offers.data?.results ?? []} countdown />
            <div className="row banner-ads">
              <div className="col-12">
                <div className="row">
                  <Banner image="img-7.jpg" bordered className="col-12 col-lg-6" />
                  <Banner image="img-8.jpg" className="col-12 col-lg-6" />
                </div>
              </div>
            </div>
            <ProductWidget titleImage="seller_1.png" products={topRated.data?.results ?? []} />
          </div>
        </div>

        <div className="row banner-ads">
          <div className="col-12">
            <div className="row">
              <div className="col-12">
                <div className="widget widget-banner card border_all">
                  <img className="img-fluid" src={staticUrl("img/banner_img/img-9.jpg")} alt="" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <div className="brand-slider card border_all bglight">
              <header className="card-header">
                <h3 className="card-title">
                  <span>دسته بندی های مَسای</span>
                </h3>
              </header>
              <div className="row">
                <div className="col-12">
                  <div className="row">
                    {(categories.data ?? []).map((category) => (
                      <div className="col-6 col-md-2 contact-bigicon" key={category.id}>
                        <Link to={`/category/${category.category_slug}`}>
                          {category.category_pic && (
                            <img
                              className="img-responsive imgpad"
                              src={toRelativeUrl(category.category_pic)}
                              alt={category.category_name}
                            />
                          )}
                          <b className="title-3 light-black">{category.category_name}</b>
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-12">
            <div className="brand-slider card border_all bglight">
              <header className="card-header">
                <h3 className="card-title">
                  <span>محبوب‌ترین برندها</span>
                </h3>
              </header>
              <Carousel responsive={BRAND_RESPONSIVE} loop autoplay autoplayTimeout={3000}>
                {(brands.data ?? []).map((brand) => (
                  <div className="item borderitem" key={brand.id}>
                    {brand.brand_pic && <img src={toRelativeUrl(brand.brand_pic)} alt={brand.brand_name} />}
                  </div>
                ))}
              </Carousel>
            </div>
          </div>
        </div>
      </div>

      <div className="container-fluid bgGray blog-box-footer">
        <div className="container">
          <div className="col-12">
            <div className="widget-blog border_all">
              <header className="card-header">
                <h3 className="card-title">
                  <span>مَسای مگ</span>
                </h3>
              </header>
              <Carousel className="Blog-carousel" responsive={BLOG_RESPONSIVE} margin={10} nav>
                {(posts.data?.results ?? []).map((post) => (
                  <div className="item" key={post.id}>
                    <Link to={`/blog/${post.slug}`}>
                      <img src={toRelativeUrl(post.blog_image)} className="img-fluid" alt={post.blog_name} />
                    </Link>
                    <Link to={`/blog/${post.slug}`}>
                      <h2 className="Blog_title">{post.blog_name}</h2>
                    </Link>
                    <div className="Blog_list">
                      <span className="Blog_author">
                        <i className="fa fa-user" /> {post.author}
                      </span>
                      <span className="Blog_Date">
                        <i className="fa fa-calendar" /> {formatJalaliDate(post.create_date)}
                      </span>
                    </div>
                  </div>
                ))}
              </Carousel>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
