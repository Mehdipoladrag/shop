import { Link, useOutletContext } from "react-router-dom";
import { CircleCheck, Info, Pencil } from "lucide-react";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import PageHead from "./PageHead";
import "../account.css";

// "ltr" values (e-mail, numbers) are isolated so they do not reorder inside right-to-left text.
const FIELDS = [
  { name: "first_name", label: "نام" },
  { name: "last_name", label: "نام خانوادگی" },
  { name: "email", label: "پست الکترونیک", ltr: true },
  { name: "mobile", label: "شماره تلفن همراه", ltr: true },
  { name: "zipcode", label: "کد پستی", ltr: true },
  { name: "back_money", label: "روش بازگرداندن پول من" },
  { name: "age", label: "سن" },
  { name: "national_code", label: "کد ملی", ltr: true },
  { name: "card_number", label: "شماره کارت", ltr: true },
  { name: "iban", label: "شماره شبا", ltr: true },
];

// The profile counts as complete once all of these are filled (same list as the server's).
const REQUIRED_FIELDS = [
  { name: "national_code", label: "کد ملی" },
  { name: "address", label: "آدرس" },
  { name: "zipcode", label: "کد پستی" },
  { name: "street", label: "خیابان" },
  { name: "city", label: "شهر" },
  { name: "mobile", label: "شماره همراه" },
  { name: "age", label: "سن" },
  { name: "card_number", label: "شماره کارت" },
  { name: "iban", label: "شماره شبا" },
];

function completeness(profile) {
  const missing = REQUIRED_FIELDS.filter(({ name }) => !profile[name]);
  const percent = profile.is_complete ? 100 : Math.min(99, Math.round(((REQUIRED_FIELDS.length - missing.length) / REQUIRED_FIELDS.length) * 100));
  return { missing, percent };
}

function CompletenessCard({ profile }) {
  const { missing, percent } = completeness(profile);

  if (profile.is_complete) {
    return (
      <section className="account-note account-note--success card" data-testid="profile-completeness">
        <CircleCheck size={22} aria-hidden="true" />
        <p>پروفایل شما کامل است و برای ثبت سفارش آماده‌اید.</p>
      </section>
    );
  }

  return (
    <section className="account-note account-note--warning card" data-testid="profile-completeness">
      <Info size={22} aria-hidden="true" />
      <div className="account-note__body">
        <p>اطلاعات شما کامل نیست. برای تکمیل سفارش‌ها، پروفایل خود را کامل کنید.</p>
        <div className="account-progress">
          <div
            className="account-progress__track"
            role="progressbar"
            aria-label="میزان تکمیل پروفایل"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={percent}
          >
            <span className="account-progress__bar" style={{ width: `${percent}%` }} />
          </div>
          <span className="account-progress__value">{percent}٪</span>
        </div>
        {missing.length > 0 && <p className="account-note__missing">مانده: {missing.map(({ label }) => label).join("، ")}</p>}
      </div>
      <Link to="/account/edit" className="btn btn--primary btn--sm" data-testid="profile-complete-btn">
        تکمیل اطلاعات
      </Link>
    </section>
  );
}

export default function ProfilePage() {
  useDocumentTitle("پروفایل من");
  const { profile } = useOutletContext();

  return (
    <div className="account-page-body">
      <PageHead title="پروفایل من" />
      <CompletenessCard profile={profile} />
      <section className="card card--pad" data-testid="profile-info">
        <div className="account-card-head">
          <h2 className="card__title">مشخصات شما</h2>
          <Link to="/account/edit" className="btn btn--secondary btn--sm" data-testid="profile-edit-link">
            <Pencil size={16} aria-hidden="true" />
            ویرایش
          </Link>
        </div>
        <dl className="account-details">
          {FIELDS.map(({ name, label, ltr }) => {
            const value = profile[name];
            const filled = value !== null && value !== undefined && value !== "";
            return (
              <div className="account-details__row" key={name} data-testid={`profile-field-${name}`}>
                <dt>{label}</dt>
                <dd className={filled ? undefined : "account-details__empty"}>
                  {filled ? ltr ? <bdi dir="ltr">{String(value)}</bdi> : String(value) : "ثبت نشده"}
                </dd>
              </div>
            );
          })}
        </dl>
      </section>
    </div>
  );
}
