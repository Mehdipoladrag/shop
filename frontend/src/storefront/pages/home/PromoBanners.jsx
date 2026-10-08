import { Link } from "react-router-dom";
import { ArrowLeft, BadgePercent, PackagePlus, Trophy } from "lucide-react";

// `ordering` values are the ones the products API accepts (see ALLOWED_ORDERINGS in the backend).
const PROMOS = [
  {
    id: "offers",
    to: "/products?has_offer=1",
    title: "تخفیف‌های ویژه",
    text: "همه کالاهای تخفیف‌دار را یک‌جا ببینید.",
    icon: BadgePercent,
  },
  {
    id: "newest",
    to: "/products?ordering=-create_date",
    title: "جدیدترین‌ها",
    text: "تازه‌ترین کالاهایی که به فروشگاه آمده‌اند.",
    icon: PackagePlus,
  },
  {
    id: "popular",
    to: "/products?ordering=-product_rate",
    title: "محبوب‌ترین‌ها",
    text: "کالاهای پرامتیاز از نگاه خریداران.",
    icon: Trophy,
  },
];

/** Three shortcut banners drawn with CSS and one big icon each; no pictures. */
export default function PromoBanners() {
  return (
    <section className="section" aria-labelledby="home-promos-title">
      <h2 className="visually-hidden" id="home-promos-title">
        میان‌برهای فروشگاه
      </h2>
      <div className="home-promos">
        {PROMOS.map(({ id, to, title, text, icon: Icon }) => (
          <Link to={to} className={`home-promo home-promo--${id}`} key={id} data-testid={`home-promo-${id}`}>
            <span className="home-promo__body">
              <h3 className="home-promo__title">{title}</h3>
              <span className="home-promo__text">{text}</span>
              <span className="home-promo__more">
                مشاهده
                <span className="home-promo__arrow">
                  <ArrowLeft size={16} aria-hidden="true" />
                </span>
              </span>
            </span>
            <span className="home-promo__art" aria-hidden="true">
              <Icon size={56} strokeWidth={1.5} />
            </span>
          </Link>
        ))}
      </div>
    </section>
  );
}
