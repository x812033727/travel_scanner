import type { Locale } from "@/i18n/routing";
import type { GuideKind } from "@/lib/guides";

export const ARTICLE_OG_WIDTH = 1200;
export const ARTICLE_OG_HEIGHT = 630;

/**
 * Relative path of the dynamically rendered 1200x630 editorial social/Discover preview card for
 * an article that has no real editorial photography of its own.
 *
 * Placed under `/og/.../card.png` rather than `/api/...` so:
 * - `robots.ts` (`disallow: ["/api/"]`) never blocks Googlebot-Image or social scrapers;
 * - `proxy.ts`'s `.png` matcher skips locale redirection and middleware overhead;
 * - crawlers receive a canonical `.png` URL without query parameters.
 */
export function articleOgImagePath(locale: Locale, kind: GuideKind, slug: string): string {
  return `/og/${locale}/${kind}/${slug}/card.png`;
}

const NON_LATIN_SCRIPT = /[^\u0000-\u024F\u2000-\u206F]/;

export function hasNonLatinScript(text: string): boolean {
  return NON_LATIN_SCRIPT.test(text);
}

const FONT_FAMILY_BY_LOCALE: Record<Locale, string> = {
  en: "Noto Sans",
  "zh-TW": "Noto Sans TC",
  "zh-CN": "Noto Sans SC",
  ja: "Noto Sans JP",
  ko: "Noto Sans KR",
};

const FONT_CACHE_MAX = 64;
const fontCache = new Map<string, ArrayBuffer>();

// Classic Safari UA so Google Fonts CSS serves a TrueType URL (Satori does not decode WOFF2).
const GOOGLE_FONT_TTF_UA =
  "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1";

/**
 * Fetch a subsetted Bold TrueType font covering only the characters actually printed on the card.
 * Returns null on timeout or network failure so the route can fall back to the static brand PNG
 * instead of rendering broken tofu glyphs.
 */
export async function loadSubsetFont(locale: Locale, text: string): Promise<{ name: string; data: ArrayBuffer } | null> {
  const family = FONT_FAMILY_BY_LOCALE[locale] ?? FONT_FAMILY_BY_LOCALE["zh-TW"];
  const uniqueChars = Array.from(new Set(text.replace(/\s+/g, " ").trim())).sort().join("");
  if (!uniqueChars) return null;
  const cacheKey = `${family}:${uniqueChars}`;
  const cached = fontCache.get(cacheKey);
  if (cached) return { name: family, data: cached };

  try {
    const cssUrl = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(family)}:wght@700&text=${encodeURIComponent(uniqueChars)}`;
    const cssResponse = await fetch(cssUrl, {
      headers: { "User-Agent": GOOGLE_FONT_TTF_UA },
      signal: AbortSignal.timeout(2000),
    });
    if (!cssResponse.ok) return null;
    const css = await cssResponse.text();
    const match = css.match(/src:\s*url\(([^)]+)\)\s*format\(['"](?:truetype|opentype)['"]\)/i)
      ?? css.match(/src:\s*url\((https?:\/\/[^)]+)\)/i);
    if (!match?.[1]) return null;
    const fontUrl = match[1].replace(/^['"]|['"]$/g, "");
    const fontResponse = await fetch(fontUrl, { signal: AbortSignal.timeout(2000) });
    if (!fontResponse.ok) return null;
    const data = await fontResponse.arrayBuffer();
    if (data.byteLength === 0) return null;
    if (fontCache.size >= FONT_CACHE_MAX) {
      const oldest = fontCache.keys().next().value;
      if (oldest !== undefined) fontCache.delete(oldest);
    }
    fontCache.set(cacheKey, data);
    return { name: family, data };
  } catch {
    return null;
  }
}

export function clampCardText(value: string, maxChars: number): string {
  const cleaned = value.replace(/\s+/g, " ").trim();
  if (cleaned.length <= maxChars) return cleaned;
  return `${cleaned.slice(0, maxChars - 1).trimEnd()}…`;
}

export function headlineFontSize(title: string): number {
  const weightedLength = Array.from(title).reduce((sum, ch) => sum + (NON_LATIN_SCRIPT.test(ch) ? 1.65 : 1), 0);
  if (weightedLength <= 34) return 60;
  if (weightedLength <= 56) return 50;
  return 42;
}
