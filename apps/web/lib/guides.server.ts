import { cache } from "react";
import {
  isArticleReference, isGuideSeries, isSeriesNavigation, isSeriesSummary,
  type GuideSeries, type SeriesSummary,
} from "./guide-series";
import {
  isDestinationFacet,
  isGuidePartnerLink,
  isGuideSummary,
  isGuideTopic,
  isPublishedGuide,
  isGuideKind,
  isGuideSearchResult,
  topicLocales,
  type DestinationFacet,
  type GuideSearchResult,
  type GuideArticleState,
  type GuideKind,
  type GuideList,
  type GuideListSort,
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

type Answer = { ok: boolean; status: number; body: unknown };

/** One read, with the status kept: a caller that has to tell "the API refused the input"
 *  (422) from "the API is down" reads this; every other caller reads `fetchJson`. */
async function fetchJsonWithStatus(path: string, locale: string): Promise<Answer | null> {
  try {
    const response = await fetch(`${apiBase()}/api/v1${path}`, {
      cache: "no-store",
      signal: AbortSignal.timeout(3000),
      headers: await publicServerHeaders(locale),
    });
    const body: unknown = await response.json().catch(() => null);
    return { ok: response.ok, status: response.status, body };
  } catch {
    // Each caller decides what a miss means: a list degrades to empty, an article refuses
    // to render a blank document and says it is unavailable.
    return null;
  }
}

async function fetchJson(path: string, locale: string): Promise<unknown | null> {
  const answer = await fetchJsonWithStatus(path, locale);
  return answer && answer.ok ? answer.body : null;
}

export type GuideFilters = {
  kind?: GuideKind;
  /** Which public section to list. The API treats `section` and `kind` as an intersection,
   *  so `{ section: "life", kind: "intel" }` is an empty list, never an unfiltered one. */
  section?: GuideSection;
  destination?: string;
  /** A catalog country in URL form (`japan`, `south-korea`); the API maps it to its cities. */
  country?: string;
  /** A topic slug. A parent topic lists its sub-topics' articles too. */
  topic?: string;
  cursor?: string;
  /** Left unset, the parameter is not sent and the API's default (`latest`) applies. A
   *  cursor minted under one order is refused (422) under the other, which `loadGuideList`
   *  reports as `available: false`; the page then sends the reader to its first page. */
  sort?: GuideListSort;
};

function query(locale: string, filters: GuideFilters, limit: number): string {
  const params = new URLSearchParams({ locale, limit: String(limit) });
  if (filters.kind) params.set("kind", filters.kind);
  if (filters.section) params.set("section", filters.section);
  if (filters.destination) params.set("destination", filters.destination);
  if (filters.country) params.set("country", filters.country);
  if (filters.topic) params.set("topic", filters.topic);
  if (filters.cursor) params.set("cursor", filters.cursor);
  if (filters.sort) params.set("sort", filters.sort);
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
export type GuideTopicListResult = { topics: GuideTopic[]; available: boolean };

/**
 * The vocabulary plus whether the API answered, for the one caller that needs to tell an
 * unknown topic (a 404) from an unreachable vocabulary (a page that must not claim the topic
 * is gone). Listing pages keep using `loadGuideTopics`, for which an outage is an empty chip
 * row either way.
 */
export async function loadGuideTopicList(locale: Locale, section: GuideSection): Promise<GuideTopicListResult> {
  const params = new URLSearchParams({ locale, section });
  const row = await fetchJson(`/guides/topics?${params.toString()}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.topics)) return { topics: [], available: false };
  return { topics: body.topics.filter(isGuideTopic), available: true };
}

export async function loadGuideTopics(locale: Locale, section: GuideSection): Promise<GuideTopic[]> {
  return (await loadGuideTopicList(locale, section)).topics;
}

/** Every series hub published in `locale`, in the API's registry order; empty on any failure. */
export async function loadSeriesIndex(locale: Locale): Promise<SeriesSummary[]> {
  const row = await fetchJson(`/guides/series?locale=${encodeURIComponent(locale)}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.series)) return [];
  return body.series.filter(isSeriesSummary);
}

export type GuideSearchFilters = {
  q: string;
  section?: GuideSection;
  kind?: GuideKind;
  topic?: string;
  destination?: string;
  country?: string;
  offset?: number;
};

/** A search answer, plus how it failed when it did: `invalid` is the API refusing the
 *  query (nothing searchable in it), `available: false` is the API not answering at all.
 *  The page words the two differently, because only one of them is the reader's to fix. */
export type GuideSearchState = GuideSearchResult & { available: boolean; invalid: boolean };

export const SEARCH_PAGE_SIZE = 10;

function emptySearch(q: string, offset: number, limit: number, state: Pick<GuideSearchState, "available" | "invalid">): GuideSearchState {
  return { query: q, total: 0, offset, limit, results: [], best_match: null, next_offset: null, ...state };
}

export async function loadGuideSearch(
  locale: Locale, filters: GuideSearchFilters, limit = SEARCH_PAGE_SIZE,
): Promise<GuideSearchState> {
  const offset = Math.max(0, filters.offset ?? 0);
  const params = new URLSearchParams({ locale, q: filters.q, limit: String(limit), offset: String(offset) });
  if (filters.section) params.set("section", filters.section);
  if (filters.kind) params.set("kind", filters.kind);
  if (filters.topic) params.set("topic", filters.topic);
  if (filters.destination) params.set("destination", filters.destination);
  if (filters.country) params.set("country", filters.country);
  const answer = await fetchJsonWithStatus(`/guides/search?${params.toString()}`, locale);
  if (!answer) return emptySearch(filters.q, offset, limit, { available: false, invalid: false });
  if (answer.status === 422) return emptySearch(filters.q, offset, limit, { available: true, invalid: true });
  if (!answer.ok || !isGuideSearchResult(answer.body)) {
    return emptySearch(filters.q, offset, limit, { available: false, invalid: false });
  }
  return { ...answer.body, best_match: answer.body.best_match ?? null, next_offset: answer.body.next_offset ?? null, available: true, invalid: false };
}

export type DestinationFacetResult = { destinations: DestinationFacet[]; available: boolean };

/** The destinations with a published article in `locale`, with their country and count. */
export async function loadDestinationFacets(
  locale: Locale, section?: GuideSection,
): Promise<DestinationFacetResult> {
  const params = new URLSearchParams({ locale });
  if (section) params.set("section", section);
  const row = await fetchJson(`/guides/destinations?${params.toString()}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.destinations)) return { destinations: [], available: false };
  return { destinations: body.destinations.filter(isDestinationFacet), available: true };
}

/** One topic hub per section topic, with the locales that publish something under it. */
export type GuideTopicSitemapEntry = { section: GuideSection; slug: string; locales: Locale[] };

/**
 * Publication-aware enumeration of the topic hubs for `app/sitemap.ts`: a hub is listed in a
 * language only while that language has an article under the topic, which is the same rule
 * the hub's own `generateMetadata` applies. Two reads, one per section vocabulary; a failed
 * read lists nothing for that section rather than every hub in every language.
 */
export async function guideTopicSitemapEntries(): Promise<GuideTopicSitemapEntry[]> {
  const sections: GuideSection[] = ["travel", "life"];
  const results = await Promise.all(sections.map((section) => loadGuideTopicList(defaultLocale, section)));
  return sections.flatMap((section, index) => results[index].topics
    .map((topic) => ({ section, slug: topic.slug, locales: topicLocales(topic, locales) }))
    .filter((entry) => entry.locales.length > 0));
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
  const references = (value: unknown) => (Array.isArray(value) ? value.filter(isArticleReference) : []);
  return { ...shared, status: "published", document: body.document, partner_links: partnerLinks,
    article_links: references(body.article_links),
    series: isSeriesNavigation(body.series) ? body.series : null,
    related: references(body.related),
    backlinks: references(body.backlinks),
    aliases: Array.isArray(body.aliases) ? body.aliases.filter((name): name is string => typeof name === "string") : [],
    term_set: isArticleReference(body.term_set) ? body.term_set : null,
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

/**
 * The most rows one child sitemap carries: not a ceiling on the section, a slice of it. A
 * section and locale with more rows than this is served as numbered children
 * (`app/sitemaps/sitemap.ts`), the n-th starting `(n - 1) × SITEMAP_CHILD_LIMIT` rows down
 * the API's total order, so nothing is ever left unadvertised. Google's per-file limit is
 * 50,000 URLs; 5,000 keeps each file quick to serve and to fetch, read in pages of
 * `SITEMAP_PAGE_SIZE` (the API's page maximum) so a child needs a handful of calls.
 */
export const SITEMAP_CHILD_LIMIT = 5000;
export const SITEMAP_PAGE_SIZE = 1000;

/** The slug grammar the API enforces on write (`SLUG_PATTERN`, apps/api/app/guides/schemas.py). */
const SITEMAP_SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/**
 * The enumeration, plus whether it is the complete publication picture.
 *
 * `complete` is false after a failed page. A failed first page returns no entries at all; a
 * failed later page keeps the rows already read, because a child with most of its articles
 * beats a child with none -- but either way the caller must not read an absence here as
 * "not published". A slice that filled `SITEMAP_CHILD_LIMIT` is complete: the rows after it
 * belong to the next numbered child, not to this one.
 */
export type GuideSitemapResult = { entries: GuideSitemapEntry[]; complete: boolean };

/** Which child's rows to enumerate: one section, one locale, and how many rows down the
 *  API's order the child starts (the n-th child of a section starts at
 *  `(n - 1) × SITEMAP_CHILD_LIMIT`). Empty means every row from the top. */
export type GuideSitemapFilters = { section?: GuideSection; locale?: Locale; offset?: number };

/**
 * Publication-aware enumeration for `app/sitemaps/sitemap.ts`, following `next_cursor`
 * until the API says the page was the last one or the child's slice is full.
 *
 * Returns no entries on a failed first page. The sitemap must degrade to its static child
 * rather than disappear: an empty sitemap tells Google the site has no pages, which is far
 * worse than one missing section.
 */
export async function guideSitemapEntries(filters: GuideSitemapFilters = {}): Promise<GuideSitemapResult> {
  const rows: Array<Omit<GuideSitemapEntry, "locales"> & { apiLocales?: Locale[] }> = [];
  const byArticle = new Map<string, Locale[]>();
  let cursor: string | null = null;
  let complete = true;
  do {
    const params = new URLSearchParams({ limit: String(SITEMAP_PAGE_SIZE) });
    if (filters.section) params.set("section", filters.section);
    if (filters.locale) params.set("locale", filters.locale);
    // The offset enters the order once; every later page continues from the cursor.
    if (!cursor && filters.offset) params.set("offset", String(filters.offset));
    if (cursor) params.set("cursor", cursor);
    const row: unknown = await fetchJson(`/guides/sitemap?${params.toString()}`, defaultLocale);
    const body = row as Record<string, unknown> | null;
    if (!body || !Array.isArray(body.entries)) {
      // A failed page: keep what earlier pages gave, and say the picture is not whole.
      complete = false;
      break;
    }
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
      // toISOString() on it and throws -- a 500 on the child rather than a missing entry.
      if (!SITEMAP_SLUG.test(entry.slug)) continue;
      if (!Number.isFinite(Date.parse(entry.published_at))) continue;
      const locale = entry.locale as Locale;
      const key = `${entry.kind}:${entry.slug}`;
      byArticle.set(key, [...(byArticle.get(key) ?? []), locale]);
      // Same guard as published_at, but a bad value here costs only the lastmod, never the URL.
      const modified = typeof entry.modified_at === "string" && Number.isFinite(Date.parse(entry.modified_at))
        ? { modified_at: entry.modified_at } : {};
      // The API names every locale the article is published in; a child that holds one locale
      // could not learn the others from its own rows. An older API sends none, and then the
      // rows this read saw are the best picture there is.
      const apiLocales = Array.isArray(entry.locales)
        && entry.locales.every((item) => locales.includes(item as Locale)) && entry.locales.includes(locale)
        ? { apiLocales: entry.locales as Locale[] } : {};
      rows.push({ kind: entry.kind, slug: entry.slug, locale, published_at: entry.published_at, ...modified, ...apiLocales });
    }
    cursor = typeof body.next_cursor === "string" && body.next_cursor ? body.next_cursor : null;
    // A full slice is this child's whole share; the rows after it are the next child's.
    if (rows.length >= SITEMAP_CHILD_LIMIT) break;
  } while (cursor);

  return {
    entries: rows.slice(0, SITEMAP_CHILD_LIMIT).map(({ apiLocales, ...entry }) => ({
      ...entry,
      // Ordered by the site's own locale list rather than the API's row order, so two runs
      // cannot produce differently ordered alternates for the same article.
      locales: locales.filter((value) => (apiLocales ?? byArticle.get(`${entry.kind}:${entry.slug}`))?.includes(value)),
    })),
    complete,
  };
}

/** Published rows per kind and locale, from `GET /guides/sitemap/summary`. */
export type GuideSitemapCount = { kind: GuideKind; locale: Locale; count: number };
export type GuideSitemapSummary = { counts: GuideSitemapCount[]; available: boolean };

/**
 * What the sitemap index and the section hubs decide from: which kinds publish in which
 * locales. `available: false` is a failed read, and only a read that answered may leave a
 * hub or a child out -- an outage must keep every hub listed in every language, which is the
 * behaviour before this read existed.
 */
export async function guideSitemapSummary(): Promise<GuideSitemapSummary> {
  const row = await fetchJson("/guides/sitemap/summary", defaultLocale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.counts)) return { counts: [], available: false };
  const counts = body.counts.filter((value): value is GuideSitemapCount => {
    const entry = value as Record<string, unknown> | null;
    return !!entry && isGuideKind(entry.kind) && locales.includes(entry.locale as Locale)
      && Number.isInteger(entry.count) && Number(entry.count) >= 0;
  });
  return { counts, available: true };
}


export const getGuideList = cache(loadGuideList);
export const getGuideTopics = cache(loadGuideTopics);
export const getGuideTopicList = cache(loadGuideTopicList);
export const getGuideArticle = cache(loadGuideArticle);
export const getSeriesIndex = cache(loadSeriesIndex);
export const getDestinationFacets = cache(loadDestinationFacets);
export const getGuideSearch = cache(loadGuideSearch);
