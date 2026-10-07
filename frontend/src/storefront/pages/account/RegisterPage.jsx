import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import { useAuth } from "../../auth/AuthContext";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";

const EMPTY_FORM = { username: "", email: "", first_name: "", last_name: "", password1: "", password2: "" };

const FIELDS = [
  { name: "username", label: "نام کاربری", placeholder: "لطفا نام کاربری مورد نظر خود را وارد کنید (با @ شروع شود)", autoComplete: "username" },
  { name: "email", label: "ایمیل", type: "email", placeholder: "لطفا ایمیل خود را وارد کنید", autoComplete: "email" },
  { name: "first_name", label: "نام", placeholder: "لطفا نام را وارد کنید", autoComplete: "given-name" },
  { name: "last_name", label: "نام خانوادگی", placeholder: "لطفا نام خانوادگی را وارد کنید", autoComplete: "family-name" },
  { name: "password1", label: "رمزعبور", type: "password", placeholder: "لطفا رمز عبور را وارد کنید (حداقل ۸ کاراکتر)", autoComplete: "new-password" },
  { name: "password2", label: "تکرار رمز عبور", type: "password", placeholder: "لطفا رمز را دوباره وارد کنید", autoComplete: "new-password" },
];

export default function RegisterPage() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const flash = useFlash();
  const [values, setValues] = useState(EMPTY_FORM);
  const [agreed, setAgreed] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  if (isAuthenticated) return <Navigate to="/account" replace />;

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    if (!agreed) {
      setErrors({ _form: "برای ثبت نام باید شرایط و قوانین را بپذیرید." });
      return;
    }
    setSubmitting(true);
    setErrors({});
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
    <main className="wrapper default">
      <div className="container">
        <div className="row">
          <div className="main-content login_content col-12 col-md-7 col-lg-5 mx-auto">
            <header className="card-header">
              <h3 className="card-title">
                <span>ایجاد حساب کاربری</span>
              </h3>
            </header>
            <div className="login_box">
              <form onSubmit={handleSubmit} noValidate>
                <div className="row">
                  <div className="col-md-12 col-sm-12">
                    <FormError message={errors._form} />
                    {FIELDS.map((field) => (
                      <FormField
                        key={field.name}
                        {...field}
                        value={values[field.name]}
                        onChange={update}
                        error={errors[field.name]}
                      />
                    ))}
                  </div>
                  <div className="col-12">
                    <div className="form-account-agree">
                      <label className="checkbox-form checkbox-primary">
                        <input type="checkbox" id="agree" checked={agreed} onChange={(event) => setAgreed(event.target.checked)} />
                        <span className="checkbox-check" />
                      </label>
                      <label htmlFor="agree">تمامی شرایط و قوانین استفاده از سرویس‌های سایت مَسای را به دقت مطالعه کرده‌ام و می‌پذیرم</label>
                    </div>
                  </div>
                  <div className="col-12 text--center">
                    <button type="submit" className="btn big_btn btn-main-masai" disabled={submitting}>
                      {submitting ? "در حال ثبت…" : "عضویت"}
                    </button>
                  </div>
                  <div className="col-12 footer_login_reg text--center">
                    <p>
                      <span>قبلا ثبت نام کرده اید؟</span> <Link to="/login">ورود</Link>
                    </p>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
