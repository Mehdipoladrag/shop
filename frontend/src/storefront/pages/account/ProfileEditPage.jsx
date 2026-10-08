import { useEffect, useState } from "react";
import { Link, useNavigate, useOutletContext } from "react-router-dom";
import { Camera, X } from "lucide-react";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import Avatar from "./Avatar";
import PageHead from "./PageHead";
import SubmitButton from "./SubmitButton";
import "../account.css";

const ACCOUNT_FIELDS = [
  { name: "first_name", label: "نام", autoComplete: "given-name" },
  { name: "last_name", label: "نام خانوادگی", autoComplete: "family-name" },
  { name: "email", label: "ایمیل", type: "email", autoComplete: "email", className: "input account-input-ltr" },
];

// The extra information, in groups drawn as fieldsets.
const PERSONAL_FIELDS = [
  { name: "national_code", label: "کد ملی", inputMode: "numeric", maxLength: 10, className: "input account-input-ltr" },
  { name: "age", label: "سن", type: "number", min: 0, className: "input account-input-ltr" },
  { name: "mobile", label: "شماره همراه", type: "tel", inputMode: "numeric", maxLength: 11, autoComplete: "tel", className: "input account-input-ltr" },
];
const ADDRESS_FIELDS = [
  { name: "city", label: "شهر" },
  { name: "street", label: "خیابان" },
  { name: "zipcode", label: "کد پستی", inputMode: "numeric", maxLength: 10, className: "input account-input-ltr" },
];
const BANK_FIELDS = [
  { name: "card_number", label: "شماره کارت", inputMode: "numeric", maxLength: 16, className: "input account-input-ltr" },
  { name: "iban", label: "شماره شبا", maxLength: 26, className: "input account-input-ltr" },
];

const EDITABLE = [...ACCOUNT_FIELDS, ...PERSONAL_FIELDS, ...ADDRESS_FIELDS, ...BANK_FIELDS, { name: "address" }, { name: "gender" }].map(
  (field) => field.name
);

const toFormValues = (profile) =>
  Object.fromEntries(EDITABLE.map((name) => [name, profile[name] === null || profile[name] === undefined ? "" : String(profile[name])]));

/** Object URL of the chosen picture for the live preview, released when it changes. */
function usePreview(file) {
  const [url, setUrl] = useState("");
  useEffect(() => {
    if (!file) {
      setUrl("");
      return undefined;
    }
    const objectUrl = URL.createObjectURL(file);
    setUrl(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);
  return url;
}

export default function ProfileEditPage() {
  useDocumentTitle("ویرایش اطلاعات");
  const { profile, reloadProfile } = useOutletContext();
  const navigate = useNavigate();
  const flash = useFlash();
  const [values, setValues] = useState(() => toFormValues(profile));
  const [picture, setPicture] = useState(null);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);
  const preview = usePreview(picture);

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
      <FormField
        key={field.name}
        {...field}
        value={values[field.name]}
        onChange={update}
        error={errors[field.name]}
        data-testid={`profile-edit-${field.name}`}
      />
    ));

  return (
    <div className="account-page-body">
      <PageHead title="ویرایش اطلاعات" />
      <form className="account-form" onSubmit={handleSubmit} encType="multipart/form-data" noValidate data-testid="profile-edit-form">
        <FormError message={errors._form} />

        <section className="card card--pad">
          <h2 className="card__title">اطلاعات حساب شخصی</h2>
          <div className="account-picture">
            <Avatar profile={profile} src={preview || undefined} size="xl" testId="profile-edit-avatar-preview" />
            <div className="account-picture__body">
              <p className="account-picture__name">
                نام کاربری: <bdi>{profile.username}</bdi>
              </p>
              <div className="account-picture__actions">
                <label className="btn btn--secondary account-upload">
                  <Camera size={16} aria-hidden="true" />
                  {profile.customer_image || picture ? "تغییر تصویر" : "انتخاب تصویر"}
                  <input
                    type="file"
                    accept="image/*"
                    aria-describedby="profile-edit-picture-hint"
                    data-testid="profile-edit-avatar-input"
                    onChange={(event) => setPicture(event.target.files[0] ?? null)}
                  />
                </label>
                {picture && (
                  <button type="button" className="btn btn--ghost" onClick={() => setPicture(null)} data-testid="profile-edit-avatar-clear">
                    <X size={16} aria-hidden="true" />
                    لغو انتخاب
                  </button>
                )}
              </div>
              {errors.customer_image ? (
                <ul className="errorlist" id="profile-edit-picture-hint">
                  <li>{errors.customer_image}</li>
                </ul>
              ) : (
                <p className="field__hint" id="profile-edit-picture-hint">
                  {picture ? picture.name : "تصویر پروفایل را از دستگاه خود انتخاب کنید."}
                </p>
              )}
            </div>
          </div>
          <div className="account-form__grid">{renderFields(ACCOUNT_FIELDS)}</div>
        </section>

        <section className="card card--pad">
          <h2 className="card__title">اطلاعات تکمیلی</h2>
          <fieldset className="account-fieldset">
            <legend>اطلاعات شخصی</legend>
            <div className="account-form__grid account-form__grid--pairs">
              {renderFields(PERSONAL_FIELDS)}
              <FormField label="جنسیت" error={errors.gender}>
                {(aria) => (
                  <select {...aria} className="select" name="gender" value={values.gender} onChange={update} data-testid="profile-edit-gender">
                    <option value="false">مرد</option>
                    <option value="true">زن</option>
                  </select>
                )}
              </FormField>
            </div>
          </fieldset>
          <fieldset className="account-fieldset">
            <legend>نشانی</legend>
            <FormField label="آدرس" error={errors.address}>
              {(aria) => (
                <textarea
                  {...aria}
                  className="textarea account-textarea"
                  name="address"
                  rows={3}
                  value={values.address}
                  onChange={update}
                  data-testid="profile-edit-address"
                />
              )}
            </FormField>
            <div className="account-form__grid">{renderFields(ADDRESS_FIELDS)}</div>
          </fieldset>
          <fieldset className="account-fieldset">
            <legend>اطلاعات بانکی</legend>
            <div className="account-form__grid account-form__grid--pairs">{renderFields(BANK_FIELDS)}</div>
          </fieldset>
        </section>

        <div className="account-form__actions">
          <SubmitButton className="btn btn--primary btn--lg" loading={saving} loadingText="در حال ذخیره…" data-testid="profile-edit-submit">
            ثبت اطلاعات کاربری
          </SubmitButton>
          <Link to="/account" className="btn btn--secondary btn--lg" data-testid="profile-edit-cancel">
            انصراف
          </Link>
        </div>
      </form>
    </div>
  );
}
