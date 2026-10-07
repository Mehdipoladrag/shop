import { Link } from "react-router-dom";
import { staticUrl } from "../config";

const SERVICES = [
  ["png-4.png", "ضمانت اصل بودن"],
  ["png-1.png", "پرداخت در محل"],
  ["png-2.png", "ارسال سریع"],
  ["png-5.png", "فرصت 7 روزه استرداد"],
  ["png-3.png", "پشتیبانی تلفنی"],
  ["png-7.png", "هدیه نقدی"],
];

function FooterWidget({ title, children }) {
  return (
    <div className="col-12 col-md-6 col-lg-3">
      <div className="widget-menu widget card">
        <div className="card-header">
          <h3 className="card-title">{title}</h3>
        </div>
        {children}
      </div>
    </div>
  );
}

function scrollToTop(event) {
  event.preventDefault();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

export default function Footer() {
  return (
    <footer className="main-footer default">
      <div className="back-to-top">
        <a href="#top" onClick={scrollToTop}>
          <span className="icon">
            <i className="fa fa-chevron-up" />
          </span>
          <span>بازگشت بالا</span>
        </a>
      </div>
      <div className="servicesbg">
        <div className="footer-services container space-10">
          <div className="row">
            {SERVICES.map(([icon, label]) => (
              <div className="service-item col-2 contact-box text-center" key={icon}>
                <img src={staticUrl(`img/ico/${icon}`)} className="width-40" alt="" />
                <span className="title-1 light-black">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="container-fluid space-30 bg-map">
        <div className="footer-widgets container">
          <div className="row">
            <FooterWidget title="درباره ما">
              <p className="about_footer">
                قالب مَسای یک پکیج کامل ایرانی با هدف بی نهایت قالب HTML و WordPress و به روز رسانی همیشگی است، که
                تمام ویژگی های لازم طراحی سایت را در نظر میگیرد
              </p>
            </FooterWidget>
            <FooterWidget title="خدمات مشتریان">
              <ul className="footer-menu">
                {["ارسال فوری", "پشتیبانی سریع", "بازگشت وجه", "بسته بندی کالا"].map((label) => (
                  <li key={label}>
                    <a href="#top" onClick={(event) => event.preventDefault()}>
                      {label}
                    </a>
                  </li>
                ))}
              </ul>
            </FooterWidget>
            <FooterWidget title="با مَسای شاپ">
              <ul className="footer-menu">
                <li>
                  <a href="#top" onClick={(event) => event.preventDefault()}>
                    تامین کالا همکار
                  </a>
                </li>
                <li>
                  <a href="#top" onClick={(event) => event.preventDefault()}>
                    تخفیف سازمانی
                  </a>
                </li>
                <li>
                  <Link to="/contact">تماس با ما</Link>
                </li>
                <li>
                  <Link to="/about">درباره ما</Link>
                </li>
              </ul>
            </FooterWidget>
            <FooterWidget title="مجوزات">
              <div className="License_img">
                <a href="#top" onClick={(event) => event.preventDefault()}>
                  <img src={staticUrl("img/License_2.png")} alt="" />
                </a>
                <a href="#top" onClick={(event) => event.preventDefault()}>
                  <img src={staticUrl("img/License_1.png")} alt="" />
                </a>
              </div>
            </FooterWidget>
          </div>
        </div>
      </div>
      <div className="copyright">
        <div className="container">
          <p>
            این وب سایت به وسیله <a href="#top" onClick={(event) => event.preventDefault()}>مهدی پولادرگ</a> پشتیبانی میشود.
          </p>
        </div>
      </div>
    </footer>
  );
}
