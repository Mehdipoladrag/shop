import { Minus, Plus } from "lucide-react";
import "./QuantityStepper.css";

/** Minus / number / plus control; `onChange(newValue)` is only called with a value inside min..max. */
export default function QuantityStepper({ value, min = 1, max = 99, onChange, disabled = false, label = "تعداد" }) {
  const change = (next) => {
    if (next >= min && next <= max && next !== value) onChange(next);
  };

  return (
    <div className="stepper" role="group" aria-label={label}>
      <button type="button" className="stepper__button" aria-label="کم کردن" disabled={disabled || value <= min} onClick={() => change(value - 1)}>
        <Minus size={16} aria-hidden="true" />
      </button>
      <output className="stepper__value" aria-live="polite">
        {value}
      </output>
      <button type="button" className="stepper__button" aria-label="زیاد کردن" disabled={disabled || value >= max} onClick={() => change(value + 1)}>
        <Plus size={16} aria-hidden="true" />
      </button>
    </div>
  );
}
