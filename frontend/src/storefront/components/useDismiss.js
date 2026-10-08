import { useEffect } from "react";

/** Calls `close` when the user presses Escape or clicks outside `ref` while `open` is true. */
export function useDismiss(ref, open, close) {
  useEffect(() => {
    if (!open) return undefined;
    const handlePointer = (event) => {
      if (!ref.current?.contains(event.target)) close();
    };
    const handleKey = (event) => {
      if (event.key === "Escape") close();
    };
    document.addEventListener("pointerdown", handlePointer);
    document.addEventListener("keydown", handleKey);
    return () => {
      document.removeEventListener("pointerdown", handlePointer);
      document.removeEventListener("keydown", handleKey);
    };
  }, [open, close, ref]);
}
