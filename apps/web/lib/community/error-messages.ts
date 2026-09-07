import en from "@/messages/en/community.json";
import ja from "@/messages/ja/community.json";
import ko from "@/messages/ko/community.json";
import zhCN from "@/messages/zh-CN/community.json";
import zhTW from "@/messages/zh-TW/community.json";
import type { Locale } from "@/i18n/routing";

const catalogs: Record<Locale, Record<string, string>> = {
  en: en.errors, ja: ja.errors, ko: ko.errors, "zh-CN": zhCN.errors, "zh-TW": zhTW.errors,
};

/** Also used by existing travel tools, outside the community's ErrorNotice. */
export function communityProblemMessage(code: unknown, locale: Locale): string | undefined {
  if (typeof code !== "string" || (!code.startsWith("community_") && !code.startsWith("pet_"))) return undefined;
  const catalog = catalogs[locale];
  return Object.hasOwn(catalog, code) ? catalog[code] : undefined;
}
