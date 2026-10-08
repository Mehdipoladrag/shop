import { useId } from "react";

/**
 * Label, input and error message of one form row.
 *
 * Pass the input's props (name, type, value, onChange ...) directly, or a
 * render function as `children` to draw another control (select, file input);
 * it receives the id and aria props the control needs. `icon` (a lucide
 * element) is drawn inside the input on the starting side.
 */
export default function FormField({ label, error, hint, type = "text", required, icon, children, ...inputProps }) {
  const id = useId();
  const messageId = `${id}-message`;
  const aria = { id, "aria-invalid": Boolean(error), "aria-describedby": error || hint ? messageId : undefined };

  const control = children ? (
    children(aria)
  ) : (
    <input type={type} className="input" {...aria} {...inputProps} />
  );

  return (
    <div className="field">
      <label className="field__label" htmlFor={id}>
        {label}
        {required && <span className="required-mark"> *</span>}
      </label>
      {icon ? (
        <div className="input-group">
          <span className="input-group__icon" aria-hidden="true">
            {icon}
          </span>
          {control}
        </div>
      ) : (
        control
      )}
      {error ? (
        <ul className="errorlist" id={messageId}>
          <li>{error}</li>
        </ul>
      ) : (
        hint && (
          <span className="field__hint" id={messageId}>
            {hint}
          </span>
        )
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
