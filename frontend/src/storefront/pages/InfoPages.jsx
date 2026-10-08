import { useState } from "react";
import { Link } from "react-router-dom";
import { ClipboardList, Clock, Headphones, Mail, MessageSquare, Phone, ShieldCheck, Tag, Truck, User } from "lucide-react";
import { contactApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { BRAND } from "../../shared/brand";
import Breadcrumb from "../components/Breadcrumb";
import FormField, { FormError } from "../components/FormField";
import Logo from "../components/Logo";
import { useDocumentTitle } from "../components/useDocumentTitle";
import "./content.css";

const VALUES = [
  { icon: ShieldCheck, title: "ضمانت اصالت", text: "همه‌ی کالاها اورجینال و با ضمانت اصالت و سلامت فیزیکی عرضه می‌شوند." },
  { icon: Truck, title: "ارسال سریع", text: "سفارش شما با بسته‌بندی ایمن آماده‌ی ارسال می‌شود و تا درِ خانه می‌آید." },
  { icon: Headphones, title: "پشتیبانی همراه شما", text: "پیش از خرید و بعد از آن، پرسش‌هایتان را می‌شنویم و پاسخ می‌دهیم." },
];

export function AboutPage() {
  useDocumentTitle("درباره ما");

  return (
    <main className="page">
      <div className="container">
        <Breadcrumb items={[{ label: "درباره ما" }]} />

        <section className="about-hero">
          <div className="about-hero__logo">
            <Logo variant="light" />
          </div>
          <h1>درباره‌ی {BRAND.name}</h1>
          <p>
            {BRAND.name} فروشگاه اینترنتی کالای دیجیتال است؛ جایی برای خرید گوشی، تبلت، هدفون و لوازم جانبی با قیمت شفاف و خیال راحت.
          </p>
          <div className="about-hero__actions">
            <Link to="/products" className="btn btn--accent btn--lg">
              مشاهده محصولات
            </Link>
            <Link to="/contact" className="btn btn--lg about-hero__secondary">
              تماس با ما
            </Link>
          </div>
        </section>

        <section className="section" aria-label="ارزش‌های ما">
          <ul className="values">
            {VALUES.map(({ icon: Icon, title, text }) => (
              <li className="value-card card" key={title}>
                <span className="value-card__icon">
                  <Icon size={28} aria-hidden="true" />
                </span>
                <h2>{title}</h2>
                <p>{text}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="section story card card--pad">
          <h2>هدف ما</h2>
          <div className="prose">
            <p>
              خرید کالای دیجیتال باید ساده، شفاف و قابل‌اعتماد باشد. در {BRAND.name} تلاش می‌کنیم مشخصات هر محصول، قیمت و زمان
              ارسال را روشن و بدون ابهام نشان دهیم تا بتوانید با اطمینان انتخاب کنید.
            </p>
            <p>
              اگر در انتخاب کالا یا پیگیری سفارش به کمک نیاز دارید، از بخش تماس با ما پیام بدهید؛ پیام شما را می‌خوانیم و پاسخ
              می‌دهیم.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}

const EMPTY_MESSAGE = { name: "", email: "", phone: "", subject: "", desc: "" };

const CONTACT_FIELDS = [
  { name: "name", label: "نام و نام خانوادگی", type: "text", maxLength: 50, icon: User, autoComplete: "name" },
  { name: "email", label: "ایمیل", type: "email", icon: Mail, autoComplete: "email" },
  { name: "phone", label: "شماره تلفن", type: "tel", maxLength: 20, icon: Phone, autoComplete: "tel" },
  { name: "subject", label: "موضوع", type: "text", maxLength: 50, icon: Tag },
];

function ContactForm() {
  const [message, setMessage] = useState(EMPTY_MESSAGE);
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState("idle");

  const update = (event) => setMessage({ ...message, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("sending");
    setErrors({});
    try {
      await contactApi.send(message);
      setMessage(EMPTY_MESSAGE);
      setStatus("sent");
    } catch (error) {
      if (error instanceof ApiError && error.status === 400) {
        setErrors(Object.fromEntries(Object.entries(error.data).map(([field, text]) => [field, [].concat(text)[0]])));
      } else if (error instanceof ApiError && error.status === 429) {
        setErrors({ form: "تعداد پیام‌های ارسالی بیش از حد مجاز است. بعداً دوباره تلاش کنید." });
      } else {
        setErrors({ form: "ارسال پیام انجام نشد. دوباره تلاش کنید." });
      }
      setStatus("idle");
    }
  }

  if (status === "sent") {
    return (
      <div className="contact-sent" role="status" data-testid="contact-success">
        <h2>پیام شما ارسال شد. با تشکر!</h2>
        <p>پیام شما به دست ما رسید و در اسرع وقت بررسی می‌شود.</p>
        <button type="button" className="btn btn--secondary" onClick={() => setStatus("idle")}>
          ارسال پیام جدید
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate data-testid="contact-form">
      <FormError message={errors.form} />
      {CONTACT_FIELDS.map(({ icon: Icon, ...field }) => (
        <FormField
          key={field.name}
          {...field}
          icon={<Icon size={18} />}
          value={message[field.name]}
          onChange={update}
          error={errors[field.name]}
        />
      ))}
      <FormField label="پیام" error={errors.desc}>
        {(aria) => (
          <textarea {...aria} className="textarea" name="desc" rows="5" placeholder="پیام خود را بنویسید" value={message.desc} onChange={update} />
        )}
      </FormField>
      <button type="submit" className="btn btn--primary btn--lg btn--block" disabled={status === "sending"} data-testid="contact-submit">
        {status === "sending" ? "در حال ارسال…" : "ارسال پیام"}
      </button>
    </form>
  );
}

export function ContactPage() {
  useDocumentTitle("تماس با ما");

  return (
    <main className="page">
      <div className="container">
        <Breadcrumb items={[{ label: "تماس با ما" }]} />
        <header className="blog-header">
          <h1>تماس با ما</h1>
          <p>سؤال، پیشنهاد یا مشکلی دارید؟ پیامتان را بنویسید.</p>
        </header>

        <div className="contact-layout">
          <section className="card card--pad contact-form-card" aria-label="فرم تماس">
            <ContactForm />
          </section>

          <aside className="contact-info" aria-label="اطلاعات تماس">
            <div className="card card--pad contact-info__item">
              <span className="contact-info__icon">
                <Clock size={22} aria-hidden="true" />
              </span>
              <div>
                <h2>پاسخگویی</h2>
                <p>پیام‌های شما را در ساعات کاری می‌خوانیم و به‌زودی پاسخ می‌دهیم.</p>
              </div>
            </div>
            <div className="card card--pad contact-info__item">
              <span className="contact-info__icon">
                <ClipboardList size={22} aria-hidden="true" />
              </span>
              <div>
                <h2>پیگیری سفارش</h2>
                <p>
                  وضعیت سفارش‌هایتان را در بخش <Link to="/account/orders">سفارش‌های من</Link> ببینید.
                </p>
              </div>
            </div>
            <div className="card card--pad contact-info__item">
              <span className="contact-info__icon">
                <MessageSquare size={22} aria-hidden="true" />
              </span>
              <div>
                <h2>حریم خصوصی</h2>
                <p>اطلاعاتی که می‌نویسید فقط برای پاسخ دادن به پیام شما استفاده می‌شود.</p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
