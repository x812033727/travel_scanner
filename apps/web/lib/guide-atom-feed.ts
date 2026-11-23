import type { Locale } from "@/i18n/routing";
import { guideHref, visibleGuideHero, type GuideSummary } from "@/lib/guides";
import { localeUrl, siteUrl } from "@/lib/seo";

const escapeXml = (value: string): string =>
  value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");

const toIsoTimestamp = (value: string | null | undefined): string | null => {
  if (!value) return null;
  const candidate = /^\d{4}-\d{2}-\d{2}$/.test(value) ? `${value}T00:00:00Z` : value;
  const parsed = new Date(candidate);
  return Number.isNaN(parsed.getTime()) ? null : parsed.toISOString();
};

export type GuideAtomFeedInput = {
  locale: Locale;
  feedPath: string;
  hubPath: string;
  title: string;
  subtitle?: string;
  articles: readonly GuideSummary[];
  fallbackUpdated?: string;
};

/**
 * Builds a valid UTF-8 Atom 1.0 document for a locale news or topic feed.
 * Each entry uses the canonical locale-prefixed article URL as both `<link>` and `<id>`,
 * and includes a Media RSS thumbnail whenever the article carries a real editorial hero.
 */
export function buildGuideAtomFeed(input: GuideAtomFeedInput): string {
  const selfUrl = localeUrl(input.locale, input.feedPath);
  const hubUrl = localeUrl(input.locale, input.hubPath);
  const timestamps = input.articles
    .map((article) => toIsoTimestamp(article.published_at) ?? toIsoTimestamp(article.news_date))
    .filter((stamp): stamp is string => Boolean(stamp));
  const updated = timestamps[0] ?? toIsoTimestamp(input.fallbackUpdated) ?? new Date().toISOString();

  const entries = input.articles.map((article) => {
    const url = localeUrl(input.locale, guideHref(article.kind, article.slug));
    const entryUpdated =
      toIsoTimestamp(article.published_at) ?? toIsoTimestamp(article.news_date) ?? updated;
    const hero = visibleGuideHero(article.hero);
    const thumbnail = hero
      ? `    <media:thumbnail url="${escapeXml(`${siteUrl}${hero.src}`)}" width="${hero.width}" height="${hero.height}"/>`
      : "";
    const categories = (article.topics ?? [])
      .map((topic) => `    <category term="${escapeXml(topic.slug)}" label="${escapeXml(topic.label)}"/>`)
      .join("\n");
    return [
      "  <entry>",
      `    <title>${escapeXml(article.title)}</title>`,
      `    <link href="${escapeXml(url)}"/>`,
      `    <id>${escapeXml(url)}</id>`,
      `    <updated>${entryUpdated}</updated>`,
      `    <published>${entryUpdated}</published>`,
      article.description ? `    <summary>${escapeXml(article.description)}</summary>` : "",
      thumbnail,
      categories,
      "  </entry>",
    ]
      .filter(Boolean)
      .join("\n");
  });

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    `<feed xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xml:lang="${escapeXml(input.locale)}">`,
    `  <title>${escapeXml(input.title)}</title>`,
    input.subtitle ? `  <subtitle>${escapeXml(input.subtitle)}</subtitle>` : "",
    `  <id>${escapeXml(hubUrl)}</id>`,
    `  <link rel="self" type="application/atom+xml" href="${escapeXml(selfUrl)}"/>`,
    `  <link rel="alternate" type="text/html" href="${escapeXml(hubUrl)}"/>`,
    `  <updated>${updated}</updated>`,
    ...entries,
    "</feed>",
    "",
  ]
    .filter((line, index, lines) => line !== "" || index === lines.length - 1)
    .join("\n");
}
