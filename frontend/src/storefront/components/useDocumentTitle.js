import { useEffect } from "react";
import { BRAND } from "../../shared/brand";

/** Sets the browser tab title to "<title> | <shop name>" while the page is shown. */
export function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} | ${BRAND.name}` : `${BRAND.name} | ${BRAND.tagline}`;
  }, [title]);
}
