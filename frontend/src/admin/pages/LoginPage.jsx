import { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { ApiError } from "../api/client";

function describeLoginError(error) {
  if (error instanceof ApiError && error.status === 401) {
    return "نام کاربری یا گذرواژه نادرست است، یا این کاربر دسترسی مدیریتی ندارد.";
  }
  return "ارتباط با سرور برقرار نشد. دوباره تلاش کنید.";
}

export default function LoginPage() {
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const redirectTo = location.state?.from || "/";
  if (isAuthenticated) return <Navigate to={redirectTo} replace />;

  const updateField = (event) => setForm({ ...form, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await login(form.username.trim(), form.password);
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(describeLoginError(err));
      setSubmitting(false);
    }
  }

  return (
    <div className="login">
      <form className="login__card" onSubmit={handleSubmit}>
        <h1>ورود به پنل مدیریت</h1>
        <div className="field">
          <label htmlFor="username">نام کاربری</label>
          <input id="username" name="username" autoComplete="username" required value={form.username} onChange={updateField} />
        </div>
        <div className="field">
          <label htmlFor="password">گذرواژه</label>
          <input id="password" name="password" type="password" autoComplete="current-password" required value={form.password} onChange={updateField} />
        </div>
        {error && <p className="form-error" role="alert">{error}</p>}
        <button type="submit" className="btn btn--primary btn--block" disabled={submitting}>
          {submitting ? "در حال ورود…" : "ورود"}
        </button>
      </form>
    </div>
  );
}
