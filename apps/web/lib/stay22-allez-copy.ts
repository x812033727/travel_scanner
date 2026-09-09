import en from "./stay22-allez-messages/en.json";
import zhTW from "./stay22-allez-messages/zh-TW.json";
import zhCN from "./stay22-allez-messages/zh-CN.json";
import ja from "./stay22-allez-messages/ja.json";
import ko from "./stay22-allez-messages/ko.json";

export type Stay22AllezCopy = Record<keyof typeof en, string>;
const catalogs: Record<string, Stay22AllezCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
export function stay22AllezCopy(locale: string): Stay22AllezCopy { return catalogs[locale] || en; }

export function stay22AllezText(text: string, values: Record<string, string | number>) {
  return text.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}
