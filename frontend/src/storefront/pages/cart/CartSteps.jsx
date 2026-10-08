import { Check } from "lucide-react";
import { CART_STEPS } from "./constants";

/** Progress through the order: cart, details and payment, done. `current` is the 1-based active step. */
export default function CartSteps({ current = 1 }) {
  return (
    <ol className="cart-steps" aria-label="مراحل خرید" data-testid="cart-steps">
      {CART_STEPS.map((label, index) => {
        const number = index + 1;
        const state = number < current ? "done" : number === current ? "current" : "todo";
        return (
          <li className={`cart-steps__item is-${state}`} key={label} aria-current={state === "current" ? "step" : undefined}>
            <span className="cart-steps__mark" aria-hidden="true">
              {state === "done" ? <Check size={16} /> : number}
            </span>
            <span className="cart-steps__label">{label}</span>
          </li>
        );
      })}
    </ol>
  );
}
