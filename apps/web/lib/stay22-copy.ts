import en from "./stay22-messages/en.json";
import zhTW from "./stay22-messages/zh-TW.json";
import zhCN from "./stay22-messages/zh-CN.json";
import ja from "./stay22-messages/ja.json";
import ko from "./stay22-messages/ko.json";

// Feature-scoped catalogs follow itinerary-copy.ts while shared namespaces are owned elsewhere.
export type Stay22Copy = Record<keyof typeof en, string>;
const catalogs: Record<string, Stay22Copy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
export function stay22Copy(locale: string): Stay22Copy { return catalogs[locale] || en; }
export function stay22Text(text: string, values: Record<string, string | number>) {
  return text.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}
