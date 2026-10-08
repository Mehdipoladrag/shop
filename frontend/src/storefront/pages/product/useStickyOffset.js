import { useLayoutEffect } from "react";

const HEADER_SELECTOR = ".site-header";
const GAP_PX = 16;

/**
 * Publishes the height of the sticky site header plus a gap as the custom
 * property `name` on `ref`'s element, so a sticky card sits just below the
 * header whatever its height is at this width.
 */
export function useStickyOffset(ref, name) {
  useLayoutEffect(() => {
    const target = ref.current;
    const header = document.querySelector(HEADER_SELECTOR);
    if (!target || !header) return undefined;

    const apply = () => target.style.setProperty(name, `${Math.ceil(header.getBoundingClientRect().height) + GAP_PX}px`);
    apply();
    const observer = new ResizeObserver(apply);
    observer.observe(header);
    return () => observer.disconnect();
  }, [ref, name]);
}
