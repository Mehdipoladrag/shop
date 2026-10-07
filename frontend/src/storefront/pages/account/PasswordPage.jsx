import { useState } from "react";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";

const EMPTY_FORM = { old_password: "", new_password1: "", new_password2: "" };

export default function PasswordPage() {
  const flash = useFlash();
  const [values, setValues] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setErrors({});
    try {
      await customerApi.changePassword(values);
      setValues(EMPTY_FORM);
      flash.show("رمز عبور با موفقیت تغییر کرد");
    } catch (error) {
      setErrors(fieldErrors(error));
    }
    setSaving(false);
  }

  return (
    <div className="main-content login_content">
      <header className="card-header">
        <h3 className="card-title">
          <span>بازنشانی کلمه عبور</span>
        </h3>
      </header>
      <div className="login_box">
        <form onSubmit={handleSubmit} noValidate>
          <FormError message={errors._form} />
          <FormField
            required
            label="رمز عبور قدیمی"
            name="old_password"
            type="password"
            autoComplete="current-password"
            value={values.old_password}
            onChange={update}
            error={errors.old_password}
          />
          <FormField
            required
            label="کلمه عبور جدید"
            name="new_password1"
            type="password"
            autoComplete="new-password"
            placeholder="کلمه عبور حداقل باید ۸ کاراکتر باشد"
            value={values.new_password1}
            onChange={update}
            error={errors.new_password1}
          />
          <FormField
            required
            label="تکرار کلمه عبور"
            name="new_password2"
            type="password"
            autoComplete="new-password"
            placeholder="تکرار کلمه عبور جدید"
            value={values.new_password2}
            onChange={update}
            error={errors.new_password2}
          />
          <div className="text--center">
            <button type="submit" className="btn big_btn btn-main-masai" disabled={saving}>
              {saving ? "در حال ذخیره…" : "بازنشانی کلمه عبور"}
            </button>
          </div>
          <div className="footer_login_reg text--center">
            <p>رمز عبور خود را محافظت کرده و از افشای آن به دیگران خودداری کنید.</p>
          </div>
        </form>
      </div>
    </div>
  );
}
