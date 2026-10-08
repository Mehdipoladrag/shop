// Registers the IRANYekan family when its (licensed) web fonts were added to
// src/shared/fonts/iranyekan. Vite bundles whatever it finds there, so a
// missing font never causes a failed request.
const fontFiles = import.meta.glob("./fonts/iranyekan/*.woff2", { eager: true, query: "?url", import: "default" });

const WEIGHT_BY_NAME = { light: 300, regular: 400, medium: 500, bold: 700 };

function fontFaceRule(path, url) {
  const fileName = path.split("/").pop().toLowerCase();
  const weight = Object.entries(WEIGHT_BY_NAME).find(([name]) => fileName.includes(name))?.[1];
  if (!weight) return "";
  return `@font-face{font-family:"IRANYekan";font-style:normal;font-weight:${weight};font-display:swap;src:url("${url}") format("woff2");}`;
}

export function installFonts() {
  const rules = Object.entries(fontFiles)
    .map(([path, url]) => fontFaceRule(path, url))
    .join("");
  if (!rules) return;

  const style = document.createElement("style");
  style.dataset.font = "iranyekan";
  style.textContent = rules;
  document.head.appendChild(style);
}
