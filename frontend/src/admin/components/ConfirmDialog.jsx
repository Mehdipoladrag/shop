import { useState } from "react";
import Modal from "./Modal";

export default function ConfirmDialog({ title, message, confirmLabel = "حذف", onConfirm, onCancel }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function handleConfirm() {
    setBusy(true);
    setError("");
    try {
      await onConfirm();
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  }

  return (
    <Modal title={title} onClose={onCancel}>
      <p>{message}</p>
      {error && <p className="form-error">{error}</p>}
      <div className="modal__footer">
        <button type="button" className="btn btn--ghost" onClick={onCancel} disabled={busy}>
          انصراف
        </button>
        <button type="button" className="btn btn--danger" onClick={handleConfirm} disabled={busy}>
          {busy ? "در حال انجام…" : confirmLabel}
        </button>
      </div>
    </Modal>
  );
}
