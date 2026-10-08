import { Link } from "react-router-dom";
import { Check } from "lucide-react";
import "../checkout.css";

const STEPS = ["سبد خرید", "تأیید و پرداخت", "پایان خرید"];

/**
 * Progress of the purchase. `step` is the current step (1 to 3); with
 * `complete` every step, the last one included, is shown as finished.
 */
export default function CheckoutSteps({ step, complete = false }) {
  return (
    <ol className="checkout-steps" aria-label="مراحل خرید" data-testid="checkout-steps">
      {STEPS.map((label, index) => {
        const number = index + 1;
        const state = complete || number < step ? "done" : number === step ? "current" : "upcoming";
        const marker = state === "done" ? <Check size={16} aria-hidden="true" /> : number;
        return (
          <li
            key={label}
            className={`checkout-steps__item checkout-steps__item--${state}`}
            aria-current={state === "current" ? "step" : undefined}
          >
            {number === 1 && !complete ? (
              <Link to="/cart" className="checkout-steps__link">
                <span className="checkout-steps__marker">{marker}</span>
                <span className="checkout-steps__label">{label}</span>
              </Link>
            ) : (
              <span className="checkout-steps__link">
                <span className="checkout-steps__marker">{marker}</span>
                <span className="checkout-steps__label">{label}</span>
              </span>
            )}
          </li>
        );
      })}
    </ol>
  );
}
