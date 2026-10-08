import { useEffect, useRef, useState } from "react";
import { useCart } from "../../cart/CartContext";
import { useFlash } from "../../components/Flash";
import { MAX_PER_ORDER, stockOf } from "./details";

const ADDED_FEEDBACK_MS = 1600;
export const ADDED_MESSAGE = "به سبد خرید اضافه شد";
export const ADD_FAILED_MESSAGE = "افزودن به سبد انجام نشد. دوباره تلاش کنید.";

/**
 * State of the purchase area of one product: the chosen quantity (never more
 * than the stock or the cart limit) and the add-to-cart request.
 * `status` is "idle", "saving", "added" (for a moment after success) or "error".
 * With `flashOnError` the failure is also shown as a message at the bottom of the screen.
 */
export default function usePurchase(product, { flashOnError = false } = {}) {
  const { addItem } = useCart();
  const flash = useFlash();
  const stock = stockOf(product);
  const soldOut = stock <= 0;
  const maxQuantity = Math.max(1, Math.min(stock, MAX_PER_ORDER));

  const [quantity, setQuantity] = useState(1);
  const [status, setStatus] = useState("idle");
  const [hasAdded, setHasAdded] = useState(false);
  const timer = useRef(0);

  useEffect(() => () => clearTimeout(timer.current), []);

  async function add() {
    if (soldOut || status === "saving") return;
    setStatus("saving");
    try {
      await addItem(product.id, quantity);
      flash.show(ADDED_MESSAGE);
      setStatus("added");
      setHasAdded(true);
      clearTimeout(timer.current);
      timer.current = setTimeout(() => setStatus("idle"), ADDED_FEEDBACK_MS);
    } catch {
      setStatus("error");
      if (flashOnError) flash.show(ADD_FAILED_MESSAGE, "error");
    }
  }

  return { stock, soldOut, maxQuantity, quantity, setQuantity, status, hasAdded, add };
}
