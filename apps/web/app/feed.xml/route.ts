import { NextResponse } from "next/server";
import { getGuideList } from "@/lib/guides.server";
import { guideHref, guideSections, type GuideSummary } from "@/lib/guides";
import { FEED_PATH, localeUrl, siteUrl } from "@/lib/seo";
import { defaultLocale } from "@/i18n/routing";

/**
 * `/feed.xml` -- an Atom feed of the newest articles, for discovery rather than for readers.
 *
 * The sitemap already lists every article with its own `lastmod`, and that is what decides
 * what gets *re-crawled*. What it is poor at is announcing that something new exists: it is
 * one index over eleven children totalling ~1,800 URLs, and a crawler has to walk it to find
 * the handful of rows that changed. A feed is the opposite shape -- short, newest-first, and
 * cheap to poll -- which is why Google's own guidance is to publish both and submit the feed
 * alongside the sitemap. Bing and the feed readers that carry a story onwards read the same
 * file.
 *
 * Deliberately one locale. Nearly every article is written in zh-TW first and translated
 * later if at all (1,036 of 1,720 locale rows at the time of writing), so a single feed
 * mixing five languages would bury the thing it exists to announce. Per-locale feeds are a
 * later addition if the translated sections ever fill out; the shape here does not stop them.
 *
 * Not in the sitemap and not in `robots.ts`'s `Sitemap:` line: a feed is not a sitemap, and
 * listing it as one would put its URL into the coverage report as a page. It is advertised
 * the way feeds are, with `<link rel="alternate">` in the document head, and submitted to
 * Search Console by hand.
 */
export const dynamic = "force-dynamic";

/** Enough to cover a publishing batch without turning the feed into a second sitemap. */
const FEED_SIZE = 30;

/** Escapes text and attribute values alike, so one helper cannot be used in the wrong place. */
const escape = (value: string) =>
  value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const iso = (value: string) => {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
};

function entry(article: GuideSummary): string {
  const url = localeUrl(defaultLocale, guideHref(article.kind, article.slug));
  const updated = iso(article.published_at) ?? new Date().toISOString();
  return [
    "  <entry>",
    `    <title>${escape(article.title)}</title>`,
    `    <link href="${escape(url)}"/>`,
    // The URL is the identifier: slugs are unique per kind and never reused.
    `    <id>${escape(url)}</id>`,
    `    <updated>${updated}</updated>`,
    `    <published>${updated}</published>`,
    article.description ? `    <summary>${escape(article.description)}</summary>` : "",
    "  </entry>",
  ].filter(Boolean).join("\n");
}

export async function GET(): Promise<NextResponse> {
  // Both public sections, then merged: asking without a section would rely on the API's
  // unfiltered default, and `section` and `kind` intersect there in ways a feed should not
  // depend on. Each list is already newest-first.
  const lists = await Promise.all(
    guideSections.map((section) => getGuideList(defaultLocale, { section, sort: "latest" }, FEED_SIZE)),
  );

  if (lists.some((list) => !list.available)) {
    // A read failed, so "no new articles" is not something this handler knows. Answering 200
    // with an empty feed would say it anyway, and a poller would believe it until the next
    // fetch -- the same mistake as serving `noindex` on a page whose state could not be read.
    return new NextResponse("feed temporarily unavailable", {
      status: 503,
      headers: { "Retry-After": "600", "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  const articles = lists
    .flatMap((list) => list.articles)
    .sort((a, b) => (iso(b.published_at) ?? "").localeCompare(iso(a.published_at) ?? ""))
    .slice(0, FEED_SIZE);

  const updated = articles.length
    ? iso(articles[0].published_at) ?? new Date().toISOString()
    : new Date().toISOString();

  const body = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<feed xmlns="http://www.w3.org/2005/Atom">',
    "  <title>Mokaair</title>",
    `  <id>${escape(`${siteUrl}/`)}</id>`,
    `  <link rel="self" href="${escape(`${siteUrl}${FEED_PATH}`)}"/>`,
    `  <link href="${escape(localeUrl(defaultLocale, "/"))}"/>`,
    `  <updated>${updated}</updated>`,
    ...articles.map(entry),
    "</feed>",
    "",
  ].join("\n");

  return new NextResponse(body, {
    headers: {
      "Content-Type": "application/atom+xml; charset=utf-8",
      // Same freshness as the sitemap: the point of this file is that a new article shows up
      // in it the moment it publishes.
      "Cache-Control": "max-age=0, must-revalidate",
    },
  });
}
