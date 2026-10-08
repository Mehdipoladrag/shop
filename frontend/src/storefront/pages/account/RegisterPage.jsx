import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { AtSign, Check, Mail, User } from "lucide-react";
import { BRAND } from "../../../shared/brand";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import { useAuth } from "../../auth/AuthContext";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import AuthShell from "./AuthShell";
import PasswordField from "./PasswordField";
import SubmitButton from "./SubmitButton";
import "../account.css";

const EMPTY_FORM = { username: "", email: "", first_name: "", last_name: "", password1: "", password2: "" };

const TERMS_ERROR = "برای ثبت نام باید شرایط و قوانین را بپذیرید.";

export default function RegisterPage() {
  useDocumentTitle("ثبت نام");
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const flash = useFlash();
  const [values, setValues] = useState(EMPTY_FORM);
  const [agreed, setAgreed] = useState(false);
  const [errors, setErrors] = useState({});
  const [termsError, setTermsError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (isAuthenticated) return <Navigate to="/account" replace />;

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    if (!agreed) {
      setErrors({});
      setTermsError(TERMS_ERROR);
      return;
    }
    setSubmitting(true);
    setErrors({});
    setTermsError("");
    try {
      await customerApi.register({ ...values, username: values.username.trim() });
      flash.show("حساب کاربری با موفقیت ساخته شد");
      navigate("/login", { replace: true });
    } catch (error) {
      setErrors(fieldErrors(error));
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      testId="register-page"
      title="ایجاد حساب کاربری"
      subtitle="چند ثانیه وقت بگذارید و حساب خود را بسازید."
      lead={`به ${BRAND.name} بپیوندید`}
      footer={
        <>
          <span>قبلا ثبت نام کرده اید؟</span>{" "}
          <Link to="/login" data-testid="register-login-link">
            ورود
          </Link>
        </>
      }
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate data-testid="register-form">
        {errors._form && (
          <div data-testid="register-error">
            <FormError message={errors._form} />
          </div>
        )}
        <FormField
          label="نام کاربری"
          name="username"
          icon={<AtSign size={18} />}
          className="input account-input-ltr"
          autoComplete="username"
          placeholder="@ali"
          hint="نام کاربری باید با @ شروع شود."
          value={values.username}
          onChange={update}
          error={errors.username}
          data-testid="register-username"
        />
        <FormField
          label="ایمیل"
          name="email"
          type="email"
          icon={<Mail size={18} />}
          className="input account-input-ltr"
          autoComplete="email"
          placeholder="name@example.com"
          value={values.email}
          onChange={update}
          error={errors.email}
          data-testid="register-email"
        />
        <div className="auth-form__row">
          <FormField
            label="نام"
            name="first_name"
            icon={<User size={18} />}
            autoComplete="given-name"
            placeholder="نام"
            value={values.first_name}
            onChange={update}
            error={errors.first_name}
            data-testid="register-first-name"
          />
          <FormField
            label="نام خانوادگی"
            name="last_name"
            icon={<User size={18} />}
            autoComplete="family-name"
            placeholder="نام خانوادگی"
            value={values.last_name}
            onChange={update}
            error={errors.last_name}
            data-testid="register-last-name"
          />
        </div>
        <PasswordField
          label="رمزعبور"
          name="password1"
          autoComplete="new-password"
          placeholder="حداقل ۸ کاراکتر"
          value={values.password1}
          onChange={update}
          error={errors.password1}
          testId="register-password1"
        />
        <PasswordField
          label="تکرار رمز عبور"
          name="password2"
          autoComplete="new-password"
          placeholder="رمز را دوباره وارد کنید"
          value={values.password2}
          onChange={update}
          error={errors.password2}
          testId="register-password2"
        />
        <label className="check auth-terms">
          <input
            type="checkbox"
            id="agree"
            checked={agreed}
            aria-invalid={Boolean(termsError)}
            data-testid="register-terms"
            onChange={(event) => setAgreed(event.target.checked)}
          />
          <span className="auth-terms__box" aria-hidden="true">
            <Check size={14} strokeWidth={3} />
          </span>
          <span>تمامی شرایط و قوانین استفاده از سرویس‌های سایت {BRAND.name} را به دقت مطالعه کرده‌ام و می‌پذیرم</span>
        </label>
        {termsError && (
          <div data-testid="register-terms-error">
            <FormError message={termsError} />
          </div>
        )}
        <SubmitButton
          className="btn btn--primary btn--lg btn--block"
          loading={submitting}
          loadingText="در حال ثبت…"
          data-testid="register-submit"
        >
          عضویت
        </SubmitButton>
      </form>
    </AuthShell>
  );
}
