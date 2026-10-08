import { useLayoutEffect } from "react";

const HEADER_SELECTOR = ".site-header";
const GAP_PX = 16;

/**
 * Publishes `--shop-sticky-top` (the height of the sticky site header plus a
 * gap) on `ref`'s element, so the sticky filter panel and the scroll targets of
 * the listing sit just below the header, whatever its height is at this width.
 */
export function useStickyOffset(ref) {
  useLayoutEffect(() => {
    const target = ref.current;
    const header = document.querySelector(HEADER_SELECTOR);
    if (!target || !header) return undefined;

    const apply = () => target.style.setProperty("--shop-sticky-top", `${Math.ceil(header.getBoundingClientRect().height) + GAP_PX}px`);
    apply();
    const observer = new ResizeObserver(apply);
    observer.observe(header);
    return () => observer.disconnect();
  }, [ref]);
}
