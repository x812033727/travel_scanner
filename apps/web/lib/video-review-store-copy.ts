import en from "./video-review-store-messages/en.json";
import zhTW from "./video-review-store-messages/zh-TW.json";
import zhCN from "./video-review-store-messages/zh-CN.json";
import ja from "./video-review-store-messages/ja.json";
import ko from "./video-review-store-messages/ko.json";

// The review storage card's copy (components/admin-video-review-store.tsx), kept beside the
// backup card's (video-backup-copy.ts) rather than in messages/*/admin.json.
export type VideoReviewStoreCopy = typeof en;
const catalogs: Record<string, VideoReviewStoreCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoReviewStoreCopy(locale: string): VideoReviewStoreCopy {
  return catalogs[locale] ?? en;
}
