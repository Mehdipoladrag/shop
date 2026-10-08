import { Headphones } from "lucide-react";
import { categoryIcon } from "../../components/categoryIcon";

// The kit matches "phone" before "headphone", so a headphone category would get a smartphone icon.
const HEADPHONE_PATTERN = /headphone|earphone|airpod|هدفون|هندزفری|ایرپاد/i;

/** The kit's category icon, with headphones recognised first. */
export function homeCategoryIcon(category) {
  const text = `${category.category_slug ?? ""} ${category.category_name ?? ""}`;
  return HEADPHONE_PATTERN.test(text) ? Headphones : categoryIcon(category);
}
