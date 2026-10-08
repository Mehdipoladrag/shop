// Colour dots for the colour filter. Product colours are free text from the
// catalogue, so the dot is looked up by name. These are the colours of the goods
// themselves (not theme colours); an unknown name gets a neutral dot from the CSS.
const COLOR_SWATCHES = {
  مشکی: "#111827",
  سفید: "#ffffff",
  قرمز: "#e03131",
  زرد: "#ffd43b",
  آبی: "#1c7ed6",
  سبز: "#2f9e44",
  نقره‌ای: "#c0c4cc",
  طلایی: "#d4af37",
  هلویی: "#ffcba4",
  گرافیتی: "#41424c",
  خاکستری: "#868e96",
  بنفش: "#7048e8",
  صورتی: "#f783ac",
  نارنجی: "#fd7e14",
  قهوه‌ای: "#8d5524",
};

/** CSS colour for a colour name, or undefined when the name is not known. */
export const swatchColor = (name) => COLOR_SWATCHES[name];
