import en from "./video-pools-messages/en.json";
import ja from "./video-pools-messages/ja.json";
import ko from "./video-pools-messages/ko.json";
import zhCN from "./video-pools-messages/zh-CN.json";
import zhTW from "./video-pools-messages/zh-TW.json";

export type VideoPoolsCopy = typeof en;
const catalogs: Record<string, VideoPoolsCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoPoolsCopy(locale: string): VideoPoolsCopy {
  return catalogs[locale] ?? en;
}

export function videoPoolsText(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}
