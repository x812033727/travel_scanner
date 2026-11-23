import { locales, type Locale } from "@/i18n/routing";
import { NEWS_TOPICS, guideHref, type GuideSummary } from "@/lib/guides";
import { getGuideList } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";

/** Google News sitemaps cover only stories published in the last 48 hours and cap at 1,000 URLs. */
export const NEWS_WINDOW_MS = 48 * 60 * 60 * 1000;
const CLOCK_SKEW_MS = 5 * 60 * 1000;
const MAX_NEWS_URLS = 1_000;
const PER_TOPIC_LIMIT = 30;
const INTEL_LIMIT = 20;

const PUBLICATION_NAME = "Mokaair";

/** Google News language codes follow ISO 639 except Chinese (`zh-cn` and `zh-tw`). */
export function newsLanguageCode(locale: Locale): string {
  if (locale === "zh-TW") return "zh-tw";
  if (locale === "zh-CN") return "zh-cn";
  return locale;
}

const escapeXml = (value: string) =>
  value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");

function parseIsoTimestamp(value: string): { ms: number; iso: string } | null {
  const date = new Date(value);
  const ms = date.getTime();
  if (Number.isNaN(ms)) return null;
  return { ms, iso: date.toISOString() };
}

function isTimelyNewsItem(article: GuideSummary): boolean {
  if (article.kind === "intel") return true;
  if (article.news_date) return true;
  return article.topics.some((topic) => NEWS_TOPICS.includes(topic.slug));
}

export type NewsSitemapEntry = {
  locale: Locale;
  url: string;
  title: string;
  publishedAtIso: string;
  publishedMs: number;
};

export function renderNewsSitemapXml(entries: readonly NewsSitemapEntry[]): string {
  const body = entries.map((item) => [
    "  <url>",
    `    <loc>${escapeXml(item.url)}</loc>`,
    "    <news:news>",
    "      <news:publication>",
    `        <news:name>${escapeXml(PUBLICATION_NAME)}</news:name>`,
    `        <news:language>${newsLanguageCode(item.locale)}</news:language>`,
    "      </news:publication>",
    `      <news:publication_date>${item.publishedAtIso}</news:publication_date>`,
    `      <news:title>${escapeXml(item.title)}</news:title>`,
    "    </news:news>",
    "  </url>",
  ].join("\n"));

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">',
    ...body,
    "</urlset>",
    "",
  ].join("\n");
}

export async function loadRecentNewsSitemap(
  nowMs: number = Date.now(),
): Promise<{ available: boolean; entries: NewsSitemapEntry[] }> {
  const tasks = locales.flatMap((locale) => [
    ...NEWS_TOPICS.map(async (topic) => ({
      locale,
      result: await getGuideList(locale, { section: "life", topic, sort: "latest" }, PER_TOPIC_LIMIT),
    })),
    (async () => ({
      locale,
      result: await getGuideList(locale, { kind: "intel", sort: "latest" }, INTEL_LIMIT),
    }))(),
  ]);

  const responses = await Promise.all(tasks);
  if (responses.some(({ result }) => !result.available)) {
    return { available: false, entries: [] };
  }

  const seen = new Set<string>();
  const entries: NewsSitemapEntry[] = [];

  for (const { locale, result } of responses) {
    for (const article of result.articles) {
      if (!isTimelyNewsItem(article)) continue;
      const parsed = parseIsoTimestamp(article.published_at);
      if (!parsed) continue;
      const ageMs = nowMs - parsed.ms;
      if (ageMs < -CLOCK_SKEW_MS || ageMs > NEWS_WINDOW_MS) continue;
      const key = `${locale}:${article.kind}:${article.slug}`;
      if (seen.has(key)) continue;
      seen.add(key);
      entries.push({
        locale,
        url: localeUrl(locale, guideHref(article.kind, article.slug)),
        title: article.title,
        publishedAtIso: parsed.iso,
        publishedMs: parsed.ms,
      });
    }
  }

  entries.sort((a, b) => b.publishedMs - a.publishedMs || a.url.localeCompare(b.url));
  return { available: true, entries: entries.slice(0, MAX_NEWS_URLS) };
}
