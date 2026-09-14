import { cache } from "react";
import { isArticleReference, isGuideSeries, isSeriesNavigation, type GuideSeries } from "./guide-series";
import {
  isGuidePartnerLink,
  isGuideSummary,
  isPublishedGuide,
  isGuideKind,
  isGuideSection,
  type GuideArticleState,
  type GuideKind,
  type GuideList,
  type GuideSection,
  type GuideTopic,
} from "./guides";
import { defaultLocale, locales, type Locale } from "@/i18n/routing";
import { publicServerHeaders } from "@/lib/public-server-fetch";

/**
 * Server-to-server reads of the guides API.
 *
 * Guides are moderated content an owner can withdraw, so these are `no-store`, as
 * `docs/seo.md` requires of moderated listings: a five-minute window in which a retracted
 * fare notice stays live is exactly the failure the API's publication gate exists to
 * prevent. React `cache` still dedupes within a single render, so `generateMetadata` and
 * the page body agree without caching anything across requests.
 */

function apiBase() {
  return (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
}

async function fetchJson(path: string, locale: string): Promise<unknown | null> {
  try {
    const response = await fetch(`${apiBase()}/api/v1${path}`, {
      cache: "no-store",
      signal: AbortSignal.timeout(3000),
      headers: await publicServerHeaders(locale),
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // Each caller decides what a miss means: a list degrades to empty, an article refuses
    // to render a blank document and says it is unavailable.
    return null;
  }
}

export type GuideFilters = {
  kind?: GuideKind;
  /** Which public section to list. The API treats `section` and `kind` as an intersection,
   *  so `{ section: "life", kind: "intel" }` is an empty list, never an unfiltered one. */
  section?: GuideSection;
  destination?: string;
  topic?: string;
  cursor?: string;
};

function query(locale: string, filters: GuideFilters, limit: number): string {
  const params = new URLSearchParams({ locale, limit: String(limit) });
  if (filters.kind) params.set("kind", filters.kind);
  if (filters.section) params.set("section", filters.section);
  if (filters.destination) params.set("destination", filters.destination);
  if (filters.topic) params.set("topic", filters.topic);
  if (filters.cursor) params.set("cursor", filters.cursor);
  return params.toString();
}

/**
 * A listing, plus whether the API actually answered it.
 *
 * The body of a hub reads the same either way -- "nothing published here yet" -- but the
 * indexing rule does not. `available: false` means the read failed or was malformed, and an
 * empty `articles` then says nothing about whether the section is empty; a hub must stay
 * indexable through an API outage rather than noindex every language at once.
 */
export type GuideListResult = GuideList & { available: boolean };

export async function loadGuideList(
  locale: Locale, filters: GuideFilters = {}, limit = 12,
): Promise<GuideListResult> {
  const row = await fetchJson(`/guides?${query(locale, filters, limit)}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.articles)) return { articles: [], next_cursor: null, available: false };
  return {
    articles: body.articles.filter(isGuideSummary),
    next_cursor: typeof body.next_cursor === "string" ? body.next_cursor : null,
    available: true,
  };
}

/**
 * Whether a hub is known to have nothing to show, which is the only case that may be
 * `noindex`. Every listing behind the hub has to have answered: `/guides` covers two kinds,
 * and one failed read there would otherwise hide a language that does have articles.
 *
 * A hub called empty here is still `follow`. The page keeps the header, the section links and
 * the language switcher, and they remain the crawler's way into the languages that do
 * publish. Only the empty page itself stays out of the index.
 */
export function hubIsEmpty(...lists: GuideListResult[]): boolean {
  return lists.every((list) => list.available && list.articles.length === 0);
}

/**
 * The topic vocabulary of one section. `section` is required rather than defaulted: a page
 * that forgot to pass it would silently render every topic of both sections as its filter
 * chips. A catalogue served by an older API carries no `section` on its rows; those rows are
 * kept, because the server already filtered them.
 */
export async function loadGuideTopics(locale: Locale, section: GuideSection): Promise<GuideTopic[]> {
  const params = new URLSearchParams({ locale, section });
  const row = await fetchJson(`/guides/topics?${params.toString()}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.topics)) return [];
  return body.topics.filter((topic): topic is GuideTopic => {
    const entry = topic as Record<string, unknown> | null;
    return !!entry && typeof entry.slug === "string" && typeof entry.label === "string"
      && (entry.section === undefined || isGuideSection(entry.section));
  });
}

export async function loadGuideArticle(
  kind: GuideKind, slug: string, locale: Locale,
): Promise<GuideArticleState> {
  const unavailable: GuideArticleState = {
    slug, kind, locale, status: "unavailable", destination_id: null, destination_label: null,
    topics: [], valid_until: null, expired: false, document: null, published_locales: [],
  };
  const row = await fetchJson(
    `/guides/${kind}/${encodeURIComponent(slug)}?locale=${encodeURIComponent(locale)}`, locale,
  );
  const body = row as Record<string, unknown> | null;
  // `body.kind !== kind` is the one-article-one-URL insurance: the API looks an article up
  // by slug, so a response for a `life` article must never render under `/guides/howto/…`
  // (or the reverse) if a route ever forwards the wrong kind.
  if (!body || body.slug !== slug || body.locale !== locale || !isGuideKind(body.kind) || body.kind !== kind) {
    return unavailable;
  }
  const published = Array.isArray(body.published_locales)
    ? body.published_locales.filter((value): value is Locale => locales.includes(value as Locale))
    : [];
  const shared = {
    slug, kind, locale,
    destination_id: typeof body.destination_id === "string" ? body.destination_id : null,
    destination_label: typeof body.destination_label === "string" ? body.destination_label : null,
    topics: Array.isArray(body.topics) ? (body.topics as GuideTopic[]) : [],
    valid_until: typeof body.valid_until === "string" ? body.valid_until : null,
    expired: body.expired === true,
    published_locales: published,
  };
  if (body.status === "unpublished") return { ...shared, status: "unpublished", document: null };
  // A published status with an unreadable document is a fault, not an empty article. Saying
  // "unavailable" keeps the page out of the index instead of publishing a blank one.
  if (body.status !== "published" || !isPublishedGuide(body.document)) return unavailable;
  // A malformed entry costs only its own link, never the article: the block it belongs to
  // finds no match and draws nothing.
  const partnerLinks = Array.isArray(body.partner_links) ? body.partner_links.filter(isGuidePartnerLink) : [];
  return { ...shared, status: "published", document: body.document, partner_links: partnerLinks,
    article_links: Array.isArray(body.article_links) ? body.article_links.filter(isArticleReference) : [],
    series: isSeriesNavigation(body.series) ? body.series : null,
  };
}

export async function loadGuideSeries(slug: string, locale: Locale): Promise<GuideSeries | null> {
  const row = await fetchJson(`/guides/series/${encodeURIComponent(slug)}?locale=${encodeURIComponent(locale)}`, locale);
  return isGuideSeries(row) && row.slug === slug && row.locale === locale ? row : null;
}
export const getGuideSeries = cache(loadGuideSeries);

/** One published translation of one article, for the sitemap. */
export type GuideSitemapEntry = {
  kind: GuideKind;
  slug: string;
  locale: Locale;
  published_at: string;
  /** When the current public version went live -- the honest `lastmod`. Absent when the API
   *  predates it or sent something unparseable, in which case the sitemap falls back to
   *  `published_at` rather than dropping the row. */
  modified_at?: string;
  /** Every locale this article is published in, so its alternates can be reciprocal. */
  locales: Locale[];
};

/** Google's per-file limit is 50,000 URLs; this is a far lower self-imposed bound that keeps
 *  one slow response from dominating the sitemap. The API applies the same cap. */
export const SITEMAP_GUIDE_ENTRY_LIMIT = 1000;

/** The slug grammar the API enforces on write (`SLUG_PATTERN`, apps/api/app/guides/schemas.py). */
const SITEMAP_SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/**
 * The enumeration, plus whether it is the complete publication picture.
 *
 * `complete` is what lets the sitemap leave a section hub out of a language with nothing
 * published in it. A failed read returns no entries, and a response at the cap returns the
 * newest slice of them; in both cases "this language has no articles of this kind" is
 * unknowable, so the hubs stay listed for every language.
 */
export type GuideSitemapResult = { entries: GuideSitemapEntry[]; complete: boolean };

/**
 * Publication-aware enumeration for `app/sitemap.ts`.
 *
 * Returns no entries on any failure. The sitemap must degrade to its static list rather than
 * disappear: an empty sitemap tells Google the site has no pages, which is far worse than
 * one missing section.
 */
export async function guideSitemapEntries(): Promise<GuideSitemapResult> {
  const row = await fetchJson("/guides/sitemap", defaultLocale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.entries)) return { entries: [], complete: false };

  const byArticle = new Map<string, Locale[]>();
  const rows: Array<Omit<GuideSitemapEntry, "locales">> = [];
  for (const value of body.entries) {
    const entry = value as Record<string, unknown> | null;
    if (!entry || typeof entry.slug !== "string" || typeof entry.published_at !== "string") continue;
    if (!isGuideKind(entry.kind) || !locales.includes(entry.locale as Locale)) continue;
    // Neither of these is reachable through today's API, which validates the slug on write and
    // types published_at as a datetime. They are here because either one costs the whole file
    // rather than one URL. Next interpolates the URL into <loc> and into every alternate's href
    // with no escaping (next/dist/build/webpack/loaders/metadata/resolve-route-data.js), so a
    // slug holding `&` or `<` makes the document unparseable; and a date that does not parse
    // becomes an Invalid Date, which is truthy and is a Date, so the same serialiser calls
    // toISOString() on it and throws -- a 500 on /sitemap.xml rather than a missing entry.
    if (!SITEMAP_SLUG.test(entry.slug)) continue;
    if (!Number.isFinite(Date.parse(entry.published_at))) continue;
    const locale = entry.locale as Locale;
    const key = `${entry.kind}:${entry.slug}`;
    byArticle.set(key, [...(byArticle.get(key) ?? []), locale]);
    // Same guard as published_at, but a bad value here costs only the lastmod, never the URL.
    const modified = typeof entry.modified_at === "string" && Number.isFinite(Date.parse(entry.modified_at))
      ? { modified_at: entry.modified_at } : {};
    rows.push({ kind: entry.kind, slug: entry.slug, locale, published_at: entry.published_at, ...modified });
  }

  return {
    entries: rows.slice(0, SITEMAP_GUIDE_ENTRY_LIMIT).map((entry) => ({
      ...entry,
      // Ordered by the site's own locale list rather than the API's row order, so two runs
      // cannot produce differently ordered alternates for the same article.
      locales: locales.filter((value) => byArticle.get(`${entry.kind}:${entry.slug}`)?.includes(value)),
    })),
    // A response that filled the cap may have left rows behind, including the only article of
    // some kind in some language. Dropped rows are always the oldest, and a hub is exactly as
    // absent for one missing article as for a thousand.
    complete: rows.length <= SITEMAP_GUIDE_ENTRY_LIMIT,
  };
}

export const getGuideList = cache(loadGuideList);
export const getGuideTopics = cache(loadGuideTopics);
export const getGuideArticle = cache(loadGuideArticle);
