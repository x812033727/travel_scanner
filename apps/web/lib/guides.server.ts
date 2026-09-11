import { cache } from "react";
import {
  isGuideSummary,
  isPublishedGuide,
  isGuideKind,
  type GuideArticleState,
  type GuideKind,
  type GuideList,
  type GuideTopic,
} from "./guides";
import { defaultLocale, locales, type Locale } from "@/i18n/routing";

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
      headers: { Accept: "application/json", "X-Travel-Locale": locale },
    });
    if (!response.ok) return null;
    return (await response.json()) as unknown;
  } catch {
    // Each caller decides what a miss means: a list degrades to empty, an article refuses
    // to render a blank document and says it is unavailable.
    return null;
  }
}

export type GuideFilters = { kind?: GuideKind; destination?: string; topic?: string; cursor?: string };

function query(locale: string, filters: GuideFilters, limit: number): string {
  const params = new URLSearchParams({ locale, limit: String(limit) });
  if (filters.kind) params.set("kind", filters.kind);
  if (filters.destination) params.set("destination", filters.destination);
  if (filters.topic) params.set("topic", filters.topic);
  if (filters.cursor) params.set("cursor", filters.cursor);
  return params.toString();
}

export async function loadGuideList(
  locale: Locale, filters: GuideFilters = {}, limit = 12,
): Promise<GuideList> {
  const row = await fetchJson(`/guides?${query(locale, filters, limit)}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.articles)) return { articles: [], next_cursor: null };
  return {
    articles: body.articles.filter(isGuideSummary),
    next_cursor: typeof body.next_cursor === "string" ? body.next_cursor : null,
  };
}

export async function loadGuideTopics(locale: Locale): Promise<GuideTopic[]> {
  const row = await fetchJson(`/guides/topics?locale=${encodeURIComponent(locale)}`, locale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.topics)) return [];
  return body.topics.filter((topic): topic is GuideTopic => {
    const entry = topic as Record<string, unknown> | null;
    return !!entry && typeof entry.slug === "string" && typeof entry.label === "string";
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
  if (!body || body.slug !== slug || body.locale !== locale || !isGuideKind(body.kind)) {
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
  return { ...shared, status: "published", document: body.document };
}

/** One published translation of one article, for the sitemap. */
export type GuideSitemapEntry = {
  kind: GuideKind;
  slug: string;
  locale: Locale;
  published_at: string;
  /** Every locale this article is published in, so its alternates can be reciprocal. */
  locales: Locale[];
};

/** Google's per-file limit is 50,000 URLs; this is a far lower self-imposed bound that keeps
 *  one slow response from dominating the sitemap. The API applies the same cap. */
export const SITEMAP_GUIDE_ENTRY_LIMIT = 1000;

/**
 * Publication-aware enumeration for `app/sitemap.ts`.
 *
 * Returns `[]` on any failure. The sitemap must degrade to its static list rather than
 * disappear: an empty sitemap tells Google the site has no pages, which is far worse than
 * one missing section.
 */
export async function guideSitemapEntries(): Promise<GuideSitemapEntry[]> {
  const row = await fetchJson("/guides/sitemap", defaultLocale);
  const body = row as Record<string, unknown> | null;
  if (!body || !Array.isArray(body.entries)) return [];

  const byArticle = new Map<string, Locale[]>();
  const rows: Array<{ kind: GuideKind; slug: string; locale: Locale; published_at: string }> = [];
  for (const value of body.entries) {
    const entry = value as Record<string, unknown> | null;
    if (!entry || typeof entry.slug !== "string" || typeof entry.published_at !== "string") continue;
    if (!isGuideKind(entry.kind) || !locales.includes(entry.locale as Locale)) continue;
    const locale = entry.locale as Locale;
    const key = `${entry.kind}:${entry.slug}`;
    byArticle.set(key, [...(byArticle.get(key) ?? []), locale]);
    rows.push({ kind: entry.kind, slug: entry.slug, locale, published_at: entry.published_at });
  }

  return rows.slice(0, SITEMAP_GUIDE_ENTRY_LIMIT).map((entry) => ({
    ...entry,
    // Ordered by the site's own locale list rather than the API's row order, so two runs
    // cannot produce differently ordered alternates for the same article.
    locales: locales.filter((value) => byArticle.get(`${entry.kind}:${entry.slug}`)?.includes(value)),
  }));
}

export const getGuideList = cache(loadGuideList);
export const getGuideTopics = cache(loadGuideTopics);
export const getGuideArticle = cache(loadGuideArticle);
