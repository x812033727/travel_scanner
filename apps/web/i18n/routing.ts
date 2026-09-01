import { defineRouting } from "next-intl/routing";

export const locales = ["en", "ja", "ko", "zh-TW", "zh-CN"] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = "zh-TW";
export const localeCookieName = "travel_locale";

export const routing = defineRouting({
  locales,
  defaultLocale,
  localePrefix: "always",
  localeCookie: {
    name: localeCookieName,
    maxAge: 60 * 60 * 24 * 365,
    sameSite: "lax",
  },
  localeDetection: true,
});

export function isLocale(value: unknown): value is Locale {
  return typeof value === "string" && locales.includes(value as Locale);
}

export function normalizeLocale(value: string | null | undefined): Locale {
  if (!value) return defaultLocale;
  const normalized = value.trim().replace("_", "-");
  if (isLocale(normalized)) return normalized;
  const lower = normalized.toLowerCase();
  if (lower.startsWith("ja")) return "ja";
  if (lower.startsWith("ko")) return "ko";
  if (lower.startsWith("en")) return "en";
  if (/^zh-(cn|sg|hans)/.test(lower) || lower === "zh-hans") return "zh-CN";
  if (lower.startsWith("zh")) return "zh-TW";
  return defaultLocale;
}

export const localeLabels: Record<Locale, string> = {
  en: "English",
  ja: "日本語",
  ko: "한국어",
  "zh-TW": "繁體中文",
  "zh-CN": "简体中文",
};
