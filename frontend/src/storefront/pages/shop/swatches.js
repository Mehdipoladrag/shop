// Colour dots for the colour filter. Product colours are free text from the
// catalogue, so the dot is looked up by name. These are the colours of the goods
// themselves (not theme colours); an unknown name gets a neutral dot from the CSS.
const COLOR_SWATCHES = {
  مشکی: "#111827",
  سفید: "#ffffff",
  قرمز: "#e03131",
  زرد: "#ffd43b",
  آبی: "#1c7ed6",
  "آبی آسمانی": "#74c0fc",
  "آبی روشن": "#a5d8ff",
  "آبی سرمه‌ای": "#1b2a5c",
  "آبی نقره‌ای": "#a9b8cf",
  "آبی کبالتی": "#0047ab",
  سبز: "#2f9e44",
  سبزآبی: "#12b5a6",
  "نقره‌ای": "#c0c4cc",
  طلایی: "#d4af37",
  هلویی: "#ffcba4",
  گرافیتی: "#41424c",
  خاکستری: "#868e96",
  بنفش: "#7048e8",
  یاسی: "#c9b6e8",
  صورتی: "#f783ac",
  نارنجی: "#fd7e14",
  "قهوه‌ای": "#8d5524",
  کرم: "#f2e8cf",
  "تیتانیوم آبی": "#4f6b8c",
  "تیتانیوم خاکستری": "#8d9096",
  "تیتانیوم سفید": "#e8e6e1",
  "تیتانیوم شنی": "#b8a58c",
  "تیتانیوم طبیعی": "#a89f91",
  "تیتانیوم مشکی": "#2b2d31",
};

/** CSS colour for a colour name, or undefined when the name is not known. */
export const swatchColor = (name) => COLOR_SWATCHES[name];
