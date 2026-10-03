import { defineRouting } from "next-intl/routing";

export const locales = ["en", "ja", "ko", "zh-TW", "zh-CN"] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = "zh-TW";
export const localeCookieName = "travel_locale";

/**
 * The attributes of every write of the locale cookie: next-intl's middleware and client
 * navigation (through `routing` below), the login proxy, the OAuth callback, and the two writes
 * in the browser after sign-in (`localeCookieString`). `Secure` follows the session cookie's
 * rule, production only, so a development server over plain HTTP keeps its cookies. It is left
 * out rather than set to `false` because next-intl's browser writer prints a boolean
 * attribute's name whatever its value.
 */
export function localeCookieAttributes() {
  return {
    path: "/",
    maxAge: 60 * 60 * 24 * 365,
    sameSite: "lax" as const,
    ...(process.env.NODE_ENV === "production" ? { secure: true } : {}),
  };
}

/** The same cookie as a `document.cookie` assignment. */
export function localeCookieString(locale: Locale): string {
  const { path, maxAge, sameSite, secure } = localeCookieAttributes();
  return `${localeCookieName}=${locale}; path=${path}; max-age=${maxAge}; samesite=${sameSite}${secure ? "; secure" : ""}`;
}

export const routing = defineRouting({
  locales,
  defaultLocale,
  localePrefix: "always",
  localeCookie: { name: localeCookieName, ...localeCookieAttributes() },
  localeDetection: true,
  // The middleware's `Link` header would list all five locales with an unprefixed x-default
  // on every page, contradicting page metadata that names only published languages and
  // points x-default at English. Page metadata and the sitemap are the only alternate sets.
  alternateLinks: false,
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
