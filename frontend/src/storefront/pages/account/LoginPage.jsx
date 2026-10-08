import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { User } from "lucide-react";
import { BRAND } from "../../../shared/brand";
import { fieldErrors } from "../../api/client";
import { useAuth } from "../../auth/AuthContext";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import AuthShell from "./AuthShell";
import PasswordField from "./PasswordField";
import SubmitButton from "./SubmitButton";
import "../account.css";

export default function LoginPage() {
  useDocumentTitle("ورود");
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const flash = useFlash();
  const [values, setValues] = useState({ username: "", password: "" });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  // After logging in, return to the page that asked for it (the cart's checkout, for example).
  const redirectTo = location.state?.from || "/";
  if (isAuthenticated) return <Navigate to={redirectTo} replace />;

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setErrors({});
    try {
      await login(values.username.trim(), values.password);
      flash.show("با موفقیت وارد شدید");
      navigate(redirectTo, { replace: true });
    } catch (error) {
      setErrors(fieldErrors(error));
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      testId="login-page"
      title="ورود به حساب کاربری"
      subtitle={location.state?.from ? "برای ادامه، وارد حساب کاربری خود شوید." : "نام کاربری و رمز عبور خود را وارد کنید."}
      lead={`خوش آمدید به ${BRAND.name}`}
      footer={
        <>
          <span>کاربر جدید هستید؟</span>{" "}
          <Link to="/register" data-testid="login-register-link">
            ثبت نام
          </Link>
        </>
      }
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate data-testid="login-form">
        {errors._form && (
          <div data-testid="login-error">
            <FormError message={errors._form} />
          </div>
        )}
        <FormField
          label="نام کاربری"
          name="username"
          icon={<User size={18} />}
          className="input account-input-ltr"
          autoComplete="username"
          placeholder="لطفا نام کاربری را وارد کنید"
          value={values.username}
          onChange={update}
          error={errors.username}
          data-testid="login-username"
        />
        <PasswordField
          label="رمزعبور"
          name="password"
          autoComplete="current-password"
          placeholder="لطفا رمز را وارد کنید"
          value={values.password}
          onChange={update}
          error={errors.password}
          testId="login-password"
        />
        <SubmitButton
          className="btn btn--primary btn--lg btn--block"
          loading={submitting}
          loadingText="در حال ورود…"
          data-testid="login-submit"
        >
          ورود
        </SubmitButton>
      </form>
    </AuthShell>
  );
}
