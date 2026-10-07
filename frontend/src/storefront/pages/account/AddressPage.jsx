import { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { customerApi } from "../../api/endpoints";
import { fieldErrors } from "../../api/client";
import FormField, { FormError } from "../../components/FormField";
import { useFlash } from "../../components/Flash";

const FIELDS = [
  { name: "address", label: "آدرس" },
  { name: "city", label: "شهر" },
  { name: "street", label: "خیابان" },
  { name: "zipcode", label: "کد پستی", inputMode: "numeric", maxLength: 10 },
  { name: "mobile", label: "شماره همراه", type: "tel", inputMode: "numeric", maxLength: 11 },
];

const toFormValues = (profile) => Object.fromEntries(FIELDS.map(({ name }) => [name, profile[name] ?? ""]));

export default function AddressPage() {
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

  return (
    <div className="row">
      <div className="col-lg-12">
        <header className="card-header">
          <h3 className="card-title">
            <span>آدرس‌ها</span>
          </h3>
          <div className="text-left">
            <button type="button" className="btn btn-main-masai" onClick={toggleEditing}>
              {editing ? "انصراف" : "ویرایش آدرس"}
            </button>
          </div>
        </header>
        <div className="content-section default">
          {editing ? (
            <form onSubmit={handleSubmit} noValidate>
              <FormError message={errors._form} />
              {FIELDS.map((field) => (
                <FormField key={field.name} {...field} value={values[field.name]} onChange={update} error={errors[field.name]} />
              ))}
              <div className="text--center">
                <button type="submit" className="btn big_btn btn-main-masai" disabled={saving}>
                  {saving ? "در حال ذخیره…" : "ذخیره آدرس"}
                </button>
              </div>
            </form>
          ) : (
            <div className="row">
              <div className="col-md-12 col-sm-12 order_delivered_sec">
                <div className="row">
                  <div className="col-10 col-lg-10 col-md-10">
                    <h4 className="profile-recent-fav-name">
                      <i className="fa fa-map-pin" aria-hidden="true" /> {profile.address || <span>-</span>}
                    </h4>
                    <ul className="order-addres">
                      <li>
                        <i className="fa fa-map colormain" aria-hidden="true" /> {profile.city || "-"}
                      </li>
                      <li>
                        <i className="fa fa-envelope colormain" aria-hidden="true" /> {profile.zipcode || "-"}
                      </li>
                      <li>
                        <i className="fa fa-phone colormain" aria-hidden="true" /> {profile.mobile || "-"}
                      </li>
                      <li>
                        <i className="fa fa-user-large colormain" aria-hidden="true" /> {profile.first_name || "-"}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
