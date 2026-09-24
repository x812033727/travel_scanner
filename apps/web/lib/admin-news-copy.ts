// The /admin/news copy lives in JSON beside this file, like admin-domains-messages: the
// i18n check refuses new display text written into .ts sources.
import en from "./admin-news-messages/en.json";
import zhTW from "./admin-news-messages/zh-TW.json";
import zhCN from "./admin-news-messages/zh-CN.json";
import ja from "./admin-news-messages/ja.json";
import ko from "./admin-news-messages/ko.json";

export type AdminNewsCopy = typeof en;
const catalogs: Record<string, AdminNewsCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function adminNewsCopy(locale: string): AdminNewsCopy {
  return catalogs[locale] ?? en;
}

// Fills {name} placeholders; the catalog strings are plain text, not ICU messages.
export function fillNewsCopy(template: string, values: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (match, name: string) =>
    name in values ? String(values[name]) : match);
}
