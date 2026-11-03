import en from "./youtube-reports-messages/en.json";
import zhTW from "./youtube-reports-messages/zh-TW.json";
import zhCN from "./youtube-reports-messages/zh-CN.json";
import ja from "./youtube-reports-messages/ja.json";
import ko from "./youtube-reports-messages/ko.json";

// The channel reports line's words on the YouTube card (docs/videos/YOUTUBE-REPORTS.md). They live
// here rather than in messages/<locale>/admin.json for the reason runpod-copy.ts gives: those five
// files are bound by SHA-256 in docs/videos/long-form/review.json.
export type YoutubeReportsCopy = typeof en;
const catalogs: Record<string, YoutubeReportsCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function youtubeReportsCopy(locale: string): YoutubeReportsCopy {
  return catalogs[locale] ?? en;
}

/** A sentence with its {name} placeholders filled in. */
export function fill(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (whole, name: string) => (name in values ? String(values[name]) : whole));
}
