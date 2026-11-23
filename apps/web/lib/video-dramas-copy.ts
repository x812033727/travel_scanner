import en from "./video-dramas-messages/en.json";
import ja from "./video-dramas-messages/ja.json";
import ko from "./video-dramas-messages/ko.json";
import zhCN from "./video-dramas-messages/zh-CN.json";
import zhTW from "./video-dramas-messages/zh-TW.json";

export type VideoDramasCopy = typeof en;
const catalogs: Record<string, VideoDramasCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoDramasCopy(locale: string): VideoDramasCopy {
  return catalogs[locale] ?? en;
}

export function videoDramasText(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => String(values[key] ?? match));
}
