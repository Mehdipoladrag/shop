import { useState } from "react";
import { contactApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { staticUrl } from "../config";

const ABOUT_TEXT = [
  "قالب مَسای یکی از بهترین قالب های فروشگاهی در ایران است که به صورت یک پکیج کامل عرضه می شود. با استفاده از قالب مَسای می توانید فروشگاه اینترنتی خود را به سادگی راه اندازی کنید.",
  "برای افزایش کیفیت و کارایی قالب، گروه برنامه نویسی گرزک به مرور زمان به بهبود و ارتقاء این قالب متمرکز شده است و همواره سعی در ارائه بهترین خدمات دارد.",
  "استفاده از قالب مَسای به شما این امکان را می دهد که یک فروشگاه عالی خود را طراحی کنید. این قالب شامل ویژگی های متنوعی برای طراحی سایت است.",
];

function InfoCard({ title, children }) {
  return (
    <main className="cart-page default">
      <div className="container">
        <div className="row">
          <div className="contact_us_content col-12 mx-auto">
            <header className="card-header">
              <h3 className="card-title">
                <span>{title}</span>
              </h3>
            </header>
            <div className="account-box contact_us_page">
              <div className="account-box-content">{children}</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

export function AboutPage() {
  return (
    <InfoCard title="درباره ما">
      <div className="form-account">
        <div className="row">
          <div className="col-md-12 col-sm-12">
            <p>
              {ABOUT_TEXT.map((paragraph) => (
                <span key={paragraph}>
                  {paragraph}
                  <br />
                </span>
              ))}
            </p>
          </div>
          <div className="col-md-6 col-sm-12">
            <img src={staticUrl("img/about.png")} alt="" />
          </div>
          <div className="col-md-6 col-sm-12">
            <hr className="hr-text" data-content="در مورد قالب مَسای بیشتر بدانید" />
            <p>{ABOUT_TEXT[1]}</p>
          </div>
          <div className="col-md-6 col-sm-12">
            <hr className="hr-text" data-content="هر آنچه باید در مورد گروه گرزک بدانید" />
            <p>{ABOUT_TEXT[2]}</p>
          </div>
          <div className="col-md-6 col-sm-12">
            <img src={staticUrl("img/about.png")} alt="" />
          </div>
        </div>
      </div>
    </InfoCard>
  );
}

const EMPTY_MESSAGE = { name: "", email: "", phone: "", subject: "", desc: "" };

const CONTACT_FIELDS = [
  { name: "name", label: "نام و نام خانوادگی", type: "text", maxLength: 50 },
  { name: "email", label: "ایمیل", type: "email" },
  { name: "phone", label: "شماره تلفن", type: "tel", maxLength: 20 },
  { name: "subject", label: "موضوع", type: "text", maxLength: 50 },
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

  return (
    <form onSubmit={handleSubmit} noValidate>
      {CONTACT_FIELDS.map((field) => (
        <p key={field.name}>
          <label htmlFor={`contact-${field.name}`}>{field.label}</label>
          <input
            id={`contact-${field.name}`}
            className="input_second input_all"
            name={field.name}
            type={field.type}
            maxLength={field.maxLength}
            placeholder={field.label}
            value={message[field.name]}
            onChange={update}
          />
          {errors[field.name] && <small style={{ color: "var(--color-danger)" }}>{errors[field.name]}</small>}
        </p>
      ))}
      <p>
        <label htmlFor="contact-desc">پیام</label>
        <textarea
          id="contact-desc"
          className="input_second input_all"
          name="desc"
          rows="4"
          placeholder="پیام"
          value={message.desc}
          onChange={update}
        />
        {errors.desc && <small style={{ color: "var(--color-danger)" }}>{errors.desc}</small>}
      </p>
      {errors.form && <p role="alert" style={{ color: "var(--color-danger)" }}>{errors.form}</p>}
      {status === "sent" && <p role="status" style={{ color: "var(--color-primary)" }}>پیام شما ارسال شد. با تشکر!</p>}
      <button type="submit" className="btn big_btn btn-main-masai" disabled={status === "sending"}>
        ارسال پیام
      </button>
    </form>
  );
}

export function ContactPage() {
  return (
    <InfoCard title="تماس با ما">
      <div className="row">
        <div className="col-md-6 col-sm-12">
          <ul>
            <li>
              <i className="fa fa-map colormain" aria-hidden="true" /> ایران، تهران، خیابان طراحان، پلاک 0
            </li>
            <li>
              <i className="fa fa-envelope colormain" aria-hidden="true" /> info@test.ir - sell@test.ir
            </li>
            <li>
              <i className="fa fa-phone colormain" aria-hidden="true" /> 01234567891 - 09198765432
            </li>
          </ul>
        </div>
        <div className="col-md-6 col-sm-12 form_send_re">
          <ContactForm />
        </div>
      </div>
    </InfoCard>
  );
}
