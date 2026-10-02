import en from "./video-plans-messages/en.json";
import ja from "./video-plans-messages/ja.json";
import ko from "./video-plans-messages/ko.json";
import zhCN from "./video-plans-messages/zh-CN.json";
import zhTW from "./video-plans-messages/zh-TW.json";

export type VideoPlansCopy = typeof en;
const catalogs: Record<string, VideoPlansCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoPlansCopy(locale: string): VideoPlansCopy {
  return catalogs[locale] ?? en;
}

export function videoPlansText(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}
