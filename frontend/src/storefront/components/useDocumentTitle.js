import { useEffect } from "react";

const SITE_NAME = "مَسای شاپ";

/** Sets the browser tab title to "<title> | مَسای شاپ" while the page is shown. */
export function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} | ${SITE_NAME}` : `${SITE_NAME} | فروشگاه اینترنتی کالای دیجیتال`;
  }, [title]);
}
