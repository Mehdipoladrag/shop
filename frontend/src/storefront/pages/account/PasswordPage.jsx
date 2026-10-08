import { useState } from "react";
import { ShieldCheck } from "lucide-react";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import PageHead from "./PageHead";
import PasswordField from "./PasswordField";
import SubmitButton from "./SubmitButton";
import "../account.css";

const EMPTY_FORM = { old_password: "", new_password1: "", new_password2: "" };

export default function PasswordPage() {
  useDocumentTitle("امنیت و تغییر رمز");
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
    <div className="account-page-body">
      <PageHead title="امنیت و تغییر رمز" />
      <div className="account-password">
        <form className="card card--pad account-form" onSubmit={handleSubmit} noValidate data-testid="password-form">
          <h2 className="card__title">بازنشانی کلمه عبور</h2>
          <FormError message={errors._form} />
          <PasswordField
            required
            label="رمز عبور قدیمی"
            name="old_password"
            autoComplete="current-password"
            value={values.old_password}
            onChange={update}
            error={errors.old_password}
            testId="password-old"
          />
          <PasswordField
            required
            label="کلمه عبور جدید"
            name="new_password1"
            autoComplete="new-password"
            hint="کلمه عبور حداقل باید ۸ کاراکتر باشد"
            value={values.new_password1}
            onChange={update}
            error={errors.new_password1}
            testId="password-new1"
          />
          <PasswordField
            required
            label="تکرار کلمه عبور"
            name="new_password2"
            autoComplete="new-password"
            hint="کلمه عبور جدید را دوباره وارد کنید"
            value={values.new_password2}
            onChange={update}
            error={errors.new_password2}
            testId="password-new2"
          />
          <div className="account-form__actions">
            <SubmitButton className="btn btn--primary" loading={saving} loadingText="در حال ذخیره…" data-testid="password-submit">
              بازنشانی کلمه عبور
            </SubmitButton>
          </div>
        </form>
        <aside className="account-tip card card--pad">
          <span className="account-tip__icon">
            <ShieldCheck size={22} aria-hidden="true" />
          </span>
          <p>رمز عبور خود را محافظت کرده و از افشای آن به دیگران خودداری کنید.</p>
        </aside>
      </div>
    </div>
  );
}
