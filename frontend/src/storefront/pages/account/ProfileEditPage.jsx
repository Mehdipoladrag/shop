import { useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";

const ACCOUNT_FIELDS = [
  { name: "first_name", label: "نام", autoComplete: "given-name" },
  { name: "last_name", label: "نام خانوادگی", autoComplete: "family-name" },
  { name: "email", label: "ایمیل", type: "email", autoComplete: "email" },
];

const PROFILE_FIELDS = [
  { name: "national_code", label: "کد ملی", inputMode: "numeric", maxLength: 10 },
  { name: "address", label: "آدرس" },
  { name: "zipcode", label: "کد پستی", inputMode: "numeric", maxLength: 10 },
  { name: "street", label: "خیابان" },
  { name: "city", label: "شهر" },
  { name: "mobile", label: "شماره همراه", type: "tel", inputMode: "numeric", maxLength: 11, autoComplete: "tel" },
  { name: "age", label: "سن", type: "number", min: 0 },
  { name: "card_number", label: "شماره کارت", inputMode: "numeric", maxLength: 16 },
  { name: "iban", label: "شماره شبا", maxLength: 26 },
];

const EDITABLE = [...ACCOUNT_FIELDS, ...PROFILE_FIELDS, { name: "gender" }].map((field) => field.name);

const toFormValues = (profile) =>
  Object.fromEntries(EDITABLE.map((name) => [name, profile[name] === null || profile[name] === undefined ? "" : String(profile[name])]));

export default function ProfileEditPage() {
  const { profile, reloadProfile } = useOutletContext();
  const navigate = useNavigate();
  const flash = useFlash();
  const [values, setValues] = useState(() => toFormValues(profile));
  const [picture, setPicture] = useState(null);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setErrors({});

    const formData = new FormData();
    Object.entries(values).forEach(([name, value]) => formData.append(name, value));
    if (picture) formData.append("customer_image", picture);

    try {
      await customerApi.updateProfile(formData);
      await reloadProfile();
      flash.show("اطلاعات شما با موفقیت ذخیره شد");
      navigate("/account");
    } catch (error) {
      setErrors(fieldErrors(error));
      setSaving(false);
    }
  }

  const renderFields = (fields) =>
    fields.map((field) => (
      <FormField key={field.name} {...field} value={values[field.name]} onChange={update} error={errors[field.name]} />
    ));

  return (
    <form className="main-content login_content" onSubmit={handleSubmit} encType="multipart/form-data" noValidate>
      <div className="row">
        <div className="col-lg-6 col-md-6">
          <header className="card-header">
            <h3 className="card-title">
              <span>اطلاعات حساب شخصی</span>
            </h3>
          </header>
          <div className="login_box">
            <div className="form-field">
              <span className="title">نام کاربری :</span> <span dir="ltr">{profile.username}</span>
            </div>
            {renderFields(ACCOUNT_FIELDS)}
          </div>
        </div>
        <div className="col-lg-6 col-md-6">
          <header className="card-header">
            <h3 className="card-title">
              <span>اطلاعات تکمیلی</span>
            </h3>
          </header>
          <div className="login_box">
            <div className="row">
              <div className="col-md-12 col-sm-12">
                <FormError message={errors._form} />
                {renderFields(PROFILE_FIELDS.slice(0, 6))}
                {renderFields(PROFILE_FIELDS.slice(6))}
                <FormField label="جنسیت" error={errors.gender}>
                  {(aria) => (
                    <select {...aria} className="input_second input_all" name="gender" value={values.gender} onChange={update}>
                      <option value="false">مرد</option>
                      <option value="true">زن</option>
                    </select>
                  )}
                </FormField>
                <FormField label="تصویر مشتری" error={errors.customer_image}>
                  {(aria) => (
                    <input
                      {...aria}
                      type="file"
                      accept="image/*"
                      className="input_second input_all"
                      onChange={(event) => setPicture(event.target.files[0] ?? null)}
                    />
                  )}
                </FormField>
              </div>
              <div className="col-12 text--center">
                <button type="submit" className="btn big_btn btn-main-masai" disabled={saving}>
                  {saving ? "در حال ذخیره…" : "ثبت اطلاعات کاربری"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
  );
}
