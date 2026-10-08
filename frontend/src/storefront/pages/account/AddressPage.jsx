import { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { MapPin, MapPinOff, Pencil, X } from "lucide-react";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";
import { EmptyState } from "../../components/States";
import { useDocumentTitle } from "../../components/useDocumentTitle";
import PageHead from "./PageHead";
import SubmitButton from "./SubmitButton";
import "../account.css";

const FIELDS = [
  { name: "city", label: "شهر" },
  { name: "street", label: "خیابان" },
  { name: "zipcode", label: "کد پستی", inputMode: "numeric", maxLength: 10, className: "input account-input-ltr" },
  { name: "mobile", label: "شماره همراه", type: "tel", inputMode: "numeric", maxLength: 11, className: "input account-input-ltr" },
];

const ALL_NAMES = ["address", ...FIELDS.map(({ name }) => name)];
const toFormValues = (profile) => Object.fromEntries(ALL_NAMES.map((name) => [name, profile[name] ?? ""]));

function Detail({ label, value, ltr, wide }) {
  return (
    <div className={`account-details__row${wide ? " account-details__row--wide" : ""}`}>
      <dt>{label}</dt>
      <dd className={value ? undefined : "account-details__empty"}>{value ? ltr ? <bdi dir="ltr">{value}</bdi> : value : "ثبت نشده"}</dd>
    </div>
  );
}

export default function AddressPage() {
  useDocumentTitle("آدرس‌ها");
  const { profile, reloadProfile } = useOutletContext();
  const flash = useFlash();
  const [editing, setEditing] = useState(false);
  const [values, setValues] = useState(() => toFormValues(profile));
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  // Leaving the form discards edits that were not saved.
  function toggleEditing() {
    setValues(toFormValues(profile));
    setErrors({});
    setEditing(!editing);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setErrors({});
    try {
      await customerApi.updateAddress(values);
      await reloadProfile();
      flash.show("آدرس شما ذخیره شد");
      setEditing(false);
    } catch (error) {
      setErrors(fieldErrors(error));
    }
    setSaving(false);
  }

  const hasAddress = ALL_NAMES.some((name) => profile[name]);
  const recipient = `${profile.first_name ?? ""} ${profile.last_name ?? ""}`.trim();

  return (
    <div className="account-page-body">
      <PageHead title="آدرس‌ها">
        <button type="button" className="btn btn--secondary" onClick={toggleEditing} data-testid="address-edit-toggle">
          {editing ? <X size={18} aria-hidden="true" /> : <Pencil size={18} aria-hidden="true" />}
          {editing ? "انصراف" : "ویرایش آدرس"}
        </button>
      </PageHead>

      {editing ? (
        <form className="card card--pad account-form" onSubmit={handleSubmit} noValidate data-testid="address-form">
          <h2 className="card__title">ویرایش آدرس تحویل</h2>
          <FormError message={errors._form} />
          <FormField label="آدرس" error={errors.address}>
            {(aria) => (
              <textarea
                {...aria}
                className="textarea account-textarea"
                name="address"
                rows={3}
                value={values.address}
                onChange={update}
                data-testid="address-input-address"
              />
            )}
          </FormField>
          <div className="account-form__grid">
            {FIELDS.map((field) => (
              <FormField
                key={field.name}
                {...field}
                value={values[field.name]}
                onChange={update}
                error={errors[field.name]}
                data-testid={`address-input-${field.name}`}
              />
            ))}
          </div>
          <div className="account-form__actions">
            <SubmitButton className="btn btn--primary" loading={saving} loadingText="در حال ذخیره…" data-testid="address-save">
              ذخیره آدرس
            </SubmitButton>
            <button type="button" className="btn btn--secondary" onClick={toggleEditing} data-testid="address-cancel">
              انصراف
            </button>
          </div>
        </form>
      ) : hasAddress ? (
        <section className="card card--pad account-address" data-testid="address-card">
          <span className="account-address__icon">
            <MapPin size={22} aria-hidden="true" />
          </span>
          <div className="account-address__body">
            <h2 className="card__title">آدرس تحویل سفارش</h2>
            <dl className="account-details">
              <Detail label="آدرس" value={profile.address} wide />
              <Detail label="شهر" value={profile.city} />
              <Detail label="خیابان" value={profile.street} />
              <Detail label="کد پستی" value={profile.zipcode} ltr />
              <Detail label="شماره همراه" value={profile.mobile} ltr />
              <Detail label="تحویل‌گیرنده" value={recipient} />
            </dl>
          </div>
        </section>
      ) : (
        <div data-testid="address-empty">
          <EmptyState icon={MapPinOff} title="هنوز آدرسی ثبت نکرده‌اید." text="آدرس تحویل را ثبت کنید تا ثبت سفارش سریع‌تر شود.">
            <button type="button" className="btn btn--primary" onClick={toggleEditing}>
              ثبت آدرس
            </button>
          </EmptyState>
        </div>
      )}
    </div>
  );
}
