import { useId } from "react";

/**
 * Label, input and error message of one form row, laid out like the
 * `{{ form.as_p }}` rows of the Django forms (`input_second input_all`).
 */
export default function FormField({ label, error, type = "text", required, children, ...inputProps }) {
  const id = useId();
  const describedBy = error ? `${id}-error` : undefined;

  return (
    <div className="form-field">
      <label htmlFor={id}>
        {required && <span className="required-mark">*</span>} {label}
      </label>
      {children ? (
        children({ id, "aria-invalid": Boolean(error), "aria-describedby": describedBy })
      ) : (
        <input
          id={id}
          type={type}
          className="input_second input_all"
          aria-invalid={Boolean(error)}
          aria-describedby={describedBy}
          {...inputProps}
        />
      )}
      {error && (
        <ul className="errorlist" id={`${id}-error`}>
          <li>{error}</li>
        </ul>
      )}
    </div>
  );
}

/** Error that belongs to the whole form. */
export function FormError({ message }) {
  if (!message) return null;
  return (
    <ul className="errorlist errorlist--form" role="alert">
      <li>{message}</li>
    </ul>
  );
}
