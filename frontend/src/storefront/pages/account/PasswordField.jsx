import { useState } from "react";
import { Eye, EyeOff, LockKeyhole } from "lucide-react";
import FormField from "../../components/FormField";

/** Password input with a leading lock icon and a show/hide button. */
export default function PasswordField({ label, error, hint, required, testId, ...inputProps }) {
  const [shown, setShown] = useState(false);
  const ToggleIcon = shown ? EyeOff : Eye;

  return (
    <FormField label={label} error={error} hint={hint} required={required} icon={<LockKeyhole size={18} />}>
      {(aria) => (
        <>
          <input
            {...aria}
            {...inputProps}
            type={shown ? "text" : "password"}
            className="input account-input-ltr account-input-ltr--toggle"
            data-testid={testId}
          />
          <button
            type="button"
            className="account-password-toggle"
            aria-label={shown ? "پنهان کردن رمز عبور" : "نمایش رمز عبور"}
            aria-pressed={shown}
            data-testid={testId ? `${testId}-toggle` : undefined}
            onClick={() => setShown((value) => !value)}
          >
            <ToggleIcon size={18} aria-hidden="true" />
          </button>
        </>
      )}
    </FormField>
  );
}
