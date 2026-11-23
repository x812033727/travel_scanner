// The copy of the hand-upload link form lives in JSON beside this file, like
// admin-video-delete-messages: the five admin.json files are bound by the duration receipt
// (tools/video/long-form/review.mjs).
import en from "./admin-video-short-link-messages/en.json";
import zhTW from "./admin-video-short-link-messages/zh-TW.json";
import zhCN from "./admin-video-short-link-messages/zh-CN.json";
import ja from "./admin-video-short-link-messages/ja.json";
import ko from "./admin-video-short-link-messages/ko.json";

export type ShortLinkCopy = typeof en;
const catalogs: Record<string, ShortLinkCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function shortLinkCopy(locale: string): ShortLinkCopy {
  return catalogs[locale] ?? en;
}
