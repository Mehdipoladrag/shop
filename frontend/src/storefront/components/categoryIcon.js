import { Camera, Gamepad2, Headphones, Laptop, Monitor, Smartphone, Tablet, Tag, Watch } from "lucide-react";

// First matching keyword wins. Categories are free text entered by the shop
// owner, so the icon is chosen from the slug and the name.
const ICON_RULES = [
  [/mobile|phone|گوشی|موبایل/i, Smartphone],
  [/gaming|game|console|کنسول|بازی/i, Gamepad2],
  [/watch|ساعت/i, Watch],
  [/headphone|earphone|audio|هدفون|هندزفری|صوتی/i, Headphones],
  [/camera|دوربین/i, Camera],
  [/tablet|تبلت/i, Tablet],
  [/laptop|notebook|لپ‌تاپ|لپ تاپ|لپتاپ/i, Laptop],
  [/monitor|tv|display|نمایشگر|تلویزیون|مانیتور/i, Monitor],
];

/** Icon component that fits a category; a tag icon when nothing matches. */
export function categoryIcon(category) {
  const text = `${category.category_slug ?? ""} ${category.category_name ?? ""}`;
  return ICON_RULES.find(([pattern]) => pattern.test(text))?.[1] ?? Tag;
}
