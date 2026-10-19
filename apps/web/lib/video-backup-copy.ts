import en from "./video-backup-messages/en.json";
import zhTW from "./video-backup-messages/zh-TW.json";
import zhCN from "./video-backup-messages/zh-CN.json";
import ja from "./video-backup-messages/ja.json";
import ko from "./video-backup-messages/ko.json";

export type VideoBackupCopy = typeof en;
const catalogs: Record<string, VideoBackupCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function videoBackupCopy(locale: string): VideoBackupCopy {
  return catalogs[locale] ?? en;
}

/** A catalog sentence with its {names} filled in. */
export function fill(text: string, values: Record<string, string | number>): string {
  return text.replace(/\{(\w+)\}/g, (whole, name: string) => (name in values ? String(values[name]) : whole));
}
