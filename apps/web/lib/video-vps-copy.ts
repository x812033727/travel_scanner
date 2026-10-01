import en from "./video-vps-messages/en.json";
import zhTW from "./video-vps-messages/zh-TW.json";
import zhCN from "./video-vps-messages/zh-CN.json";
import ja from "./video-vps-messages/ja.json";
import ko from "./video-vps-messages/ko.json";

export type VideoVpsCopy = typeof en;
const catalogs: Record<string, VideoVpsCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoVpsCopy(locale: string): VideoVpsCopy {
  return catalogs[locale] ?? en;
}
