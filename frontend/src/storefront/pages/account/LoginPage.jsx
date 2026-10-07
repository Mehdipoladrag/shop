import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { fieldErrors } from "../../api/client";
import { useAuth } from "../../auth/AuthContext";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";

export default function LoginPage() {
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
    <main className="wrapper default">
      <div className="container">
        <div className="row">
          <div className="main-content login_content col-12 col-md-7 col-lg-5 mx-auto">
            <header className="card-header">
              <h3 className="card-title">
                <span>ورود به حساب کاربری</span>
              </h3>
            </header>
            <div className="login_box">
              <form onSubmit={handleSubmit} noValidate>
                <div className="row">
                  <div className="col-md-12 col-sm-12">
                    <FormError message={errors._form} />
                    <FormField
                      label="نام کاربری"
                      name="username"
                      autoComplete="username"
                      placeholder="لطفا نام کاربری را وارد کنید"
                      value={values.username}
                      onChange={update}
                      error={errors.username}
                    />
                    <FormField
                      label="رمزعبور"
                      name="password"
                      type="password"
                      autoComplete="current-password"
                      placeholder="لطفا رمز را وارد کنید"
                      value={values.password}
                      onChange={update}
                      error={errors.password}
                    />
                  </div>
                  <div className="col-12 text--center">
                    <button type="submit" className="btn big_btn btn-main-masai" disabled={submitting}>
                      {submitting ? "در حال ورود…" : "ورود"}
                    </button>
                  </div>
                  <div className="col-12 footer_login_reg text--center">
                    <p>
                      <span>کاربر جدید هستید؟</span> <Link to="/register">ثبت نام</Link>
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
