import { useId } from "react";

export default function Field({ label, error, children }) {
  const id = useId();
  return (
    <div className={`field${error ? " field--invalid" : ""}`}>
      <label htmlFor={id}>{label}</label>
      {children(id)}
      {error && <small className="field__error">{error}</small>}
    </div>
  );
}
