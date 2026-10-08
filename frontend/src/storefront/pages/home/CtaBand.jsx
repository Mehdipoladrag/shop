import { Link } from "react-router-dom";
import { ArrowLeft, Headphones, Smartphone, Tablet } from "lucide-react";

/** Wide call to action with a button to the whole catalog. */
export default function CtaBand() {
  return (
    <section className="section" aria-labelledby="home-cta-title">
      <div className="home-cta" data-testid="home-cta-band">
        <div className="home-cta__content">
          <h2 className="home-cta__title" id="home-cta-title">
            جدیدترین گوشی‌ها، تبلت‌ها و ایرپادها
          </h2>
          <p className="home-cta__text">همه محصولات را یک‌جا ببینید و بر اساس دسته، برند و قیمت پیدا کنید.</p>
          <Link to="/products" className="btn btn--accent btn--lg home-cta__button" data-testid="home-cta-link">
            مشاهده محصولات
            <ArrowLeft size={20} aria-hidden="true" />
          </Link>
        </div>

        <div className="home-cta__art" aria-hidden="true">
          <span className="home-cta__tile home-cta__tile--phone">
            <Smartphone size={56} strokeWidth={1.5} />
          </span>
          <span className="home-cta__tile home-cta__tile--tablet">
            <Tablet size={72} strokeWidth={1.5} />
          </span>
          <span className="home-cta__tile home-cta__tile--audio">
            <Headphones size={56} strokeWidth={1.5} />
          </span>
        </div>
      </div>
    </section>
  );
}
