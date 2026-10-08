import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowUp, Check, Headphones, RotateCcw, ShieldCheck, Truck, Wallet } from "lucide-react";
import Logo from "./Logo";
import "./Footer.css";

const BENEFITS = [
  { icon: ShieldCheck, title: "ضمانت اصل بودن کالا", text: "تمام محصولات اورجینال هستند" },
  { icon: Truck, title: "ارسال سریع", text: "ارسال به سراسر کشور" },
  { icon: Wallet, title: "پرداخت در محل", text: "پس از دریافت کالا پرداخت کنید" },
  { icon: RotateCcw, title: "۷ روز فرصت بازگشت", text: "بازگشت کالا بدون دردسر" },
  { icon: Headphones, title: "پشتیبانی تلفنی", text: "پاسخگوی سوال‌های شما" },
];

const QUICK_LINKS = [
  { to: "/products", label: "فروشگاه" },
  { to: "/blog", label: "وبلاگ" },
  { to: "/cart", label: "سبد خرید" },
  { to: "/account", label: "حساب کاربری" },
  { to: "/contact", label: "تماس با ما" },
  { to: "/about", label: "درباره ما" },
];

const CUSTOMER_SERVICES = ["ارسال فوری", "پشتیبانی سریع", "بازگشت وجه", "بسته‌بندی ایمن کالا"];

const SHOW_TOP_BUTTON_PX = 600;

function BackToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handle = () => setVisible(window.scrollY > SHOW_TOP_BUTTON_PX);
    handle();
    window.addEventListener("scroll", handle, { passive: true });
    return () => window.removeEventListener("scroll", handle);
  }, []);

  return (
    <button
      type="button"
      className={`back-to-top${visible ? " is-visible" : ""}`}
      aria-label="بازگشت به بالای صفحه"
      tabIndex={visible ? 0 : -1}
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
    >
      <ArrowUp size={22} aria-hidden="true" />
    </button>
  );
}

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <ul className="benefits">
          {BENEFITS.map(({ icon: Icon, title, text }) => (
            <li className="benefits__item" key={title}>
              <span className="benefits__icon">
                <Icon size={26} aria-hidden="true" />
              </span>
              <div>
                <strong>{title}</strong>
                <span>{text}</span>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div className="site-footer__main">
        <div className="container site-footer__grid">
          <section className="site-footer__about">
            <Logo variant="light" />
            <p>
              مَسای شاپ فروشگاه اینترنتی کالای دیجیتال است؛ گوشی، تبلت، لوازم جانبی و کنسول بازی با ضمانت اصالت، قیمت منصفانه و ارسال سریع.
            </p>
          </section>

          <nav aria-label="دسترسی سریع">
            <h2 className="site-footer__heading">دسترسی سریع</h2>
            <ul className="site-footer__list">
              {QUICK_LINKS.map((link) => (
                <li key={link.to}>
                  <Link to={link.to}>{link.label}</Link>
                </li>
              ))}
            </ul>
          </nav>

          <section>
            <h2 className="site-footer__heading">خدمات مشتریان</h2>
            <ul className="site-footer__list site-footer__list--checks">
              {CUSTOMER_SERVICES.map((label) => (
                <li key={label}>
                  <Check size={16} aria-hidden="true" /> {label}
                </li>
              ))}
            </ul>
          </section>
        </div>

        <div className="site-footer__bottom">
          <div className="container site-footer__bottom-inner">
            <p>این وب‌سایت به وسیله مهدی پولادرگ پشتیبانی می‌شود.</p>
          </div>
        </div>
      </div>

      <BackToTop />
    </footer>
  );
}
