import { MapPin, PackageCheck, ShieldCheck } from "lucide-react";
import Logo from "../../components/Logo";

const BENEFITS = [
  { icon: PackageCheck, text: "پیگیری سفارش‌ها از حساب کاربری" },
  { icon: MapPin, text: "ذخیره آدرس برای ثبت سریع‌تر سفارش" },
  { icon: ShieldCheck, text: "مدیریت اطلاعات حساب و رمز عبور" },
];

/**
 * Frame of the login and registration pages: a brand panel with benefits next
 * to the form on desktop, only the form with a small brand header on phones.
 * The page's single h1 is the form title.
 */
export default function AuthShell({ title, subtitle, lead, footer, testId, children }) {
  return (
    <main className="page auth-page">
      <div className="container">
        <div className="auth-card card" data-testid={testId}>
          <aside className="auth-brand">
            <Logo variant="light" />
            <p className="auth-brand__lead">{lead}</p>
            <ul className="auth-brand__list">
              {BENEFITS.map(({ icon: Icon, text }) => (
                <li key={text}>
                  <span className="auth-brand__icon">
                    <Icon size={20} aria-hidden="true" />
                  </span>
                  {text}
                </li>
              ))}
            </ul>
          </aside>
          <section className="auth-panel">
            <div className="auth-panel__brand">
              <Logo />
            </div>
            <h1 className="auth-panel__title">{title}</h1>
            {subtitle && <p className="auth-panel__subtitle">{subtitle}</p>}
            {children}
            <p className="auth-panel__footer">{footer}</p>
          </section>
        </div>
      </div>
    </main>
  );
}
