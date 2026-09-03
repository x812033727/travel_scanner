export const HOTSPOT_CATEGORY_CODES = [
  "culture",
  "food",
  "nature",
  "beach",
  "family",
  "viewpoint",
  "shopping",
  "nightlife",
] as const;

export type HotspotCategoryCode = (typeof HOTSPOT_CATEGORY_CODES)[number];

export function isHotspotCategoryCode(value: string): value is HotspotCategoryCode {
  return (HOTSPOT_CATEGORY_CODES as readonly string[]).includes(value);
}
