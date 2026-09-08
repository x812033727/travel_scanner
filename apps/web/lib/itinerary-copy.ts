import en from "./itinerary-messages/en.json";
import zhTW from "./itinerary-messages/zh-TW.json";
import zhCN from "./itinerary-messages/zh-CN.json";
import ja from "./itinerary-messages/ja.json";
import ko from "./itinerary-messages/ko.json";

// Feature-scoped catalogs avoid the concurrently edited shared namespaces.
// TypeScript checks keys; the ordering suite checks interpolation parity.
export type ItineraryCopy = Record<keyof typeof en, string>;
const catalogs: Record<string, ItineraryCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
export function itineraryCopy(locale: string): ItineraryCopy {
  return catalogs[locale] || en;
}
export function itineraryText(text: string, values: Record<string, string | number>) {
  return text.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}
