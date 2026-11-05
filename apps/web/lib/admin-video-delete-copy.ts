// The copy of a dropped video's delete dialog lives in JSON beside this file, like
// admin-news-messages: the i18n check refuses new display text written into .ts sources, and the
// five admin.json files are bound by the duration receipt (tools/video/long-form/review.mjs).
import en from "./admin-video-delete-messages/en.json";
import zhTW from "./admin-video-delete-messages/zh-TW.json";
import zhCN from "./admin-video-delete-messages/zh-CN.json";
import ja from "./admin-video-delete-messages/ja.json";
import ko from "./admin-video-delete-messages/ko.json";

export type VideoDeleteCopy = typeof en;
const catalogs: Record<string, VideoDeleteCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoDeleteCopy(locale: string): VideoDeleteCopy {
  return catalogs[locale] ?? en;
}
