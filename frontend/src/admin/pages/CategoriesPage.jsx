import { useState } from "react";
import { categoryApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { useApi } from "../../shared/useApi";
import { AsyncContent } from "../components/Feedback";
import PageHeader from "../components/PageHeader";
import DataTable from "../components/DataTable";
import Modal from "../components/Modal";
import ConfirmDialog from "../components/ConfirmDialog";
import Field from "../components/Field";
import { toPersianDigits } from "../../shared/format";
import { toRelativeMediaUrl } from "../../shared/media";

const EMPTY_FORM = { category_name: "", category_code: "", category_slug: "" };

function CategoryForm({ category, onSaved, onCancel }) {
  const isEditing = Boolean(category);
  const [values, setValues] = useState(
    isEditing
      ? {
          category_name: category.category_name,
          category_code: String(category.category_code),
          category_slug: category.category_slug,
        }
      : EMPTY_FORM
  );
  const [picture, setPicture] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [saving, setSaving] = useState(false);

  const updateValue = (event) => setValues({ ...values, [event.target.name]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setFieldErrors({});
    setFormError("");

    const formData = new FormData();
    Object.entries(values).forEach(([name, value]) => formData.append(name, value));
    if (picture) formData.append("category_pic", picture);

    try {
      if (isEditing) await categoryApi.update(category.id, formData);
      else await categoryApi.create(formData);
      onSaved();
    } catch (error) {
      // DRF reports validation problems per field; anything else is shown as a general error.
      if (error instanceof ApiError && error.status === 400 && typeof error.data === "object") {
        const errors = Object.fromEntries(
          Object.entries(error.data).map(([field, messages]) => [field, [].concat(messages)[0]])
        );
        setFieldErrors(errors);
      } else {
        setFormError(error.message);
      }
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <Field label="نام دسته‌بندی" error={fieldErrors.category_name}>
        {(id) => <input id={id} name="category_name" required maxLength={50} value={values.category_name} onChange={updateValue} />}
      </Field>
      <Field label="کد دسته‌بندی" error={fieldErrors.category_code}>
        {(id) => <input id={id} name="category_code" type="number" required value={values.category_code} onChange={updateValue} />}
      </Field>
      <Field label="نشانی (slug)" error={fieldErrors.category_slug}>
        {(id) => <input id={id} name="category_slug" required dir="ltr" value={values.category_slug} onChange={updateValue} />}
      </Field>
      <Field label={isEditing ? "تصویر جدید (اختیاری)" : "تصویر"} error={fieldErrors.category_pic}>
        {(id) => (
          <input id={id} type="file" accept="image/*" required={!isEditing} onChange={(event) => setPicture(event.target.files[0] ?? null)} />
        )}
      </Field>
      {formError && <p className="form-error" role="alert">{formError}</p>}
      <div className="modal__footer">
        <button type="button" className="btn btn--ghost" onClick={onCancel} disabled={saving}>
          انصراف
        </button>
        <button type="submit" className="btn btn--primary" disabled={saving}>
          {saving ? "در حال ذخیره…" : "ذخیره"}
        </button>
      </div>
    </form>
  );
}

export default function CategoriesPage() {
  const state = useApi(categoryApi.list);
  // `dialog` is null, {type: "form", category?} or {type: "delete", category}.
  const [dialog, setDialog] = useState(null);

  const closeDialog = () => setDialog(null);

  function handleSaved() {
    closeDialog();
    state.reload();
  }

  async function handleDelete(category) {
    await categoryApi.remove(category.id);
    closeDialog();
    state.reload();
  }

  const columns = [
    {
      key: "category_pic",
      header: "تصویر",
      render: (category) => <img className="thumb" src={toRelativeMediaUrl(category.category_pic)} alt={category.category_name} loading="lazy" />,
    },
    { key: "category_name", header: "نام" },
    { key: "category_code", header: "کد", render: (category) => toPersianDigits(category.category_code) },
    { key: "category_slug", header: "نشانی", render: (category) => <span dir="ltr">{category.category_slug}</span> },
  ];

  return (
    <>
      <PageHeader title="دسته‌بندی‌ها">
        <button type="button" className="btn btn--primary" onClick={() => setDialog({ type: "form" })}>
          + دسته‌بندی جدید
        </button>
      </PageHeader>

      <AsyncContent state={state}>
        {(categories) => (
          <DataTable
            columns={columns}
            rows={categories}
            getRowKey={(category) => category.id}
            emptyText="هنوز دسته‌بندی‌ای ثبت نشده است."
            renderActions={(category) => (
              <>
                <button type="button" className="btn btn--ghost" onClick={() => setDialog({ type: "form", category })}>
                  ویرایش
                </button>
                <button type="button" className="btn btn--danger-ghost" onClick={() => setDialog({ type: "delete", category })}>
                  حذف
                </button>
              </>
            )}
          />
        )}
      </AsyncContent>

      {dialog?.type === "form" && (
        <Modal title={dialog.category ? "ویرایش دسته‌بندی" : "دسته‌بندی جدید"} onClose={closeDialog}>
          <CategoryForm category={dialog.category} onSaved={handleSaved} onCancel={closeDialog} />
        </Modal>
      )}
      {dialog?.type === "delete" && (
        <ConfirmDialog
          title="حذف دسته‌بندی"
          message={`دسته‌بندی «${dialog.category.category_name}» حذف شود؟ این کار قابل بازگشت نیست.`}
          onConfirm={() => handleDelete(dialog.category)}
          onCancel={closeDialog}
        />
      )}
    </>
  );
}
