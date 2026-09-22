import type { MetadataRoute } from "next";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales, type Locale } from "@/i18n/routing";
import { guideHref, guideSection, guideTopicHref, type GuideKind, type GuideSection } from "@/lib/guides";
import { HREFLANG_DEFAULT, languageAlternates, localeUrl } from "@/lib/seo";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";
import {
  guideSitemapEntries, guideSitemapSummary, guideTopicSitemapEntries, SITEMAP_CHILD_LIMIT, type GuideSitemapSummary,
} from "@/lib/guides.server";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { getCommunityState } from "@/lib/community/server";
import { petPlaceSitemapEntries, type PetPlaceSitemapEntry } from "@/lib/community/public.server";

// Evaluate public switches at request time, not while building without the API.
export const dynamic = "force-dynamic";

type SitemapRoute = {
  /** Path after the locale prefix, as `routePathFromRequest` produces it. */
  path: string;
  priority: number;
  changeFrequency: NonNullable<MetadataRoute.Sitemap[number]["changeFrequency"]>;
  feature?: SiteFeature;
  /** An article hub, listed in a language only while one of these kinds has something
   *  published there. Articles are published one language at a time, so the other four
   *  hubs say "nothing here yet" -- a soft 404 to offer, and nothing to rank. */
  hub?: readonly GuideKind[];
  /** Listed only while the discovery switch is on. Behind it the route has server-rendered
   *  content of its own; in front of it, the fallback link grid, which has nothing to rank. */
  discovery?: true;
  /** Listed only while the community switch is on. With it off every community route renders
   *  the "closed" notice and its own metadata says `noindex`, so advertising it here would
   *  contradict the page. */
  community?: true;
};

/**
 * A route belongs here only once it is genuinely indexable.
 *
 * Deliberately absent:
 * - /about, /privacy, /terms and /contact. `site-information-page.tsx` returns `noindex` until
 *   an administrator publishes the managed document, so listing them now would only accumulate
 *   "Excluded by noindex" in Search Console. They are linked from the footer, so nothing is lost
 *   by waiting for 2026-09-06-legal-content-from-owner.
 * - /explore/collections and the community routes other than /pet-friendly, which are
 *   `noindex` because their content is fetched after hydration and the server sends an empty
 *   shell. /explore no longer sends one -- it is listed below, but only while discovery is on,
 *   since with the switch off it falls back to a grid of links to pages already listed here.
 *   /pet-friendly no longer sends one either and is listed below, behind the community switch.
 * - /community/posts/{id} and /community/profiles/{handle}. They server-render and are
 *   indexable, but there is no public endpoint to enumerate them from -- /community/posts is
 *   the member feed -- so they wait for one. /pet-friendly/{id} has one, the directory's own,
 *   and is listed by `petPlaceSitemap` after these routes rather than among them: it is a
 *   read, not a route.
 * - every member and token route, which carries `noindex`.
 * - an article hub in a language that has nothing published in it. Those pages exist and
 *   answer 200, but with one sentence saying the section is empty; `hub` below lists them
 *   per language instead of per route, and their own `generateMetadata` agrees.
 * - /destinations/{id}/services, every one of them. They carry `noindex` as of 2026-09-22:
 *   the page is one template with the city's name in its title and nothing else, the lodging
 *   arriving from Stay22 after hydration, so 23 of them collected "duplicate, Google chose a
 *   different canonical" in Search Console. The destination page above is the indexable one
 *   and links to its services page, which is how the crawler still reaches it.
 */
export const SITEMAP_ROUTES: readonly SitemapRoute[] = [
  { path: "/", priority: 1.0, changeFrequency: "daily" },
  { path: "/hotspots", priority: 0.8, changeFrequency: "daily", feature: "hotspots" },
  { path: "/foods", priority: 0.8, changeFrequency: "daily" },
  { path: "/flights/status", priority: 0.5, changeFrequency: "weekly", feature: "flight_status" },
  { path: "/pricing", priority: 0.5, changeFrequency: "monthly", feature: "pricing" },
  { path: "/labs/airlines", priority: 0.4, changeFrequency: "weekly", feature: "airline_fares" },
  { path: "/destinations", priority: 0.6, changeFrequency: "weekly" },
  // Ranked below the directories it draws from: the feed reorders their rows, and an entry
  // there is one of them rather than a page of its own.
  { path: "/explore", priority: 0.5, changeFrequency: "daily", discovery: true },
  // Verified pet rules, and the only community route with a server-rendered directory of its
  // own. Ranked with the other directories it sits beside rather than with the feed.
  { path: "/pet-friendly", priority: 0.5, changeFrequency: "weekly", community: true },
  // No `feature`: the guides section is first-party content with no switch behind it, so it
  // is never one of the conditional routes. The two kind hubs resolve through the `[kind]`
  // folder; `/life` is its own folder, because `/guides/life/...` is deliberately a 404.
  { path: "/guides", priority: 0.7, changeFrequency: "daily", hub: ["intel", "howto"] },
  { path: "/guides/intel", priority: 0.7, changeFrequency: "daily", hub: ["intel"] },
  { path: "/guides/howto", priority: 0.6, changeFrequency: "weekly", hub: ["howto"] },
  // Same shape as /guides/howto on purpose: a hub of evergreen articles that are themselves
  // listed as monthly below. Claiming daily for a page that changes when an editor publishes
  // would be the same invented signal the lastmod comment further down warns about.
  { path: "/life", priority: 0.6, changeFrequency: "weekly", hub: ["life"] },
  // The destination-scoped content. Their services pages used to follow them here and no
  // longer do; see the note above.
  ...PUBLIC_DESTINATIONS.map((id) => ({
    path: `/destinations/${id}`,
    priority: 0.7,
    changeFrequency: "weekly" as const,
  })),
];

/**
 * The children of the sitemap index, by id. `static` carries every route below and, with
 * the community switch on, the pet-friendly place pages (`petPlaceSitemap`); each
 * `{section}-{locale}` child carries that section's topic hubs and its first
 * `SITEMAP_CHILD_LIMIT` articles in that language, and `{section}-{locale}-{n}` (n ≥ 2)
 * the next slice of its articles, as many slices as the rows need. So a section has no
 * ceiling: the day `life-zh-TW` passes 5,000 rows, `life-zh-TW-2` exists and the index
 * lists it, with no row ever left unadvertised.
 *
 * These eleven are the ids that exist whatever the counts say. The numbered ones are
 * derived from `GET /guides/sitemap/summary` when a crawler asks (`sitemapChildren`): Next
 * calls `generateSitemaps` per request and answers 404 for an id it did not return, and it
 * also calls it during `next build`, where there is no API -- a failed summary read then
 * yields exactly this list. A base child with nothing published answers an empty file
 * rather than a 404, and the index (`sitemap.xml/route.ts`) leaves it out while the summary
 * can be read.
 */
export const SITEMAP_SECTIONS: readonly GuideSection[] = ["travel", "life"];
export const SITEMAP_CHILDREN: readonly string[] = [
  "static",
  ...SITEMAP_SECTIONS.flatMap((section) => locales.map((locale) => `${section}-${locale}`)),
];

/** One section child: which section and language, and which slice of its rows (1-based). */
export type SitemapChild = { section: GuideSection; locale: Locale; page: number };

/** The id `parseSitemapChild` reads back: the base id for the first slice, `-n` after it. */
export function sitemapChildId({ section, locale, page }: SitemapChild): string {
  return page > 1 ? `${section}-${locale}-${page}` : `${section}-${locale}`;
}

/** Rows a section publishes in a locale, per the summary: the sum over the section's kinds. */
function sectionRows(summary: GuideSitemapSummary, { section, locale }: Pick<SitemapChild, "section" | "locale">): number {
  return summary.counts
    .filter((row) => guideSection(row.kind) === section && row.locale === locale)
    .reduce((sum, row) => sum + row.count, 0);
}

/**
 * Every child a crawler may fetch, in `SITEMAP_CHILDREN` order with each section's slices
 * together: the static child, each base child always (so an index read during an outage,
 * which lists every base child, never points at a file that has since vanished), and a
 * numbered child per further `SITEMAP_CHILD_LIMIT` rows the summary reports.
 */
export function sitemapChildren(summary: GuideSitemapSummary): string[] {
  return SITEMAP_CHILDREN.flatMap((id) => {
    const target = parseSitemapChild(id);
    if (!target || !summary.available) return [id];
    const slices = Math.max(1, Math.ceil(sectionRows(summary, target) / SITEMAP_CHILD_LIMIT));
    return Array.from({ length: slices }, (_, index) => sitemapChildId({ ...target, page: index + 1 }));
  });
}

/**
 * The children worth listing in the index: the static one and every slice of a section and
 * locale that publishes something. When the summary cannot be read, every base child --
 * an outage is not an empty section, and a child that then answers with no rows costs one
 * fetch rather than a hidden section.
 */
export function listedSitemapChildren(summary: GuideSitemapSummary): string[] {
  return sitemapChildren(summary).filter((id) => {
    const target = parseSitemapChild(id);
    return !target || !summary.available || sectionRows(summary, target) > 0;
  });
}

/**
 * Where Next serves a child: `/sitemaps/sitemap/<id>.xml`. This module lives one folder down
 * because Next refuses `app/sitemap.ts` next to `app/sitemap.xml/route.ts` as one route
 * declared twice, index or not -- so the index keeps the address and the children take the
 * folder's. The `.xml` matters too: `proxy.ts` skips paths with a dot, so next-intl never
 * tries to locale-prefix a sitemap.
 */
export function sitemapChildPath(id: string): string {
  return `/sitemaps/sitemap/${id}.xml`;
}

/** The section, locale and slice a child id names, or null for `static` and anything
 *  unknown -- including a numbered spelling `sitemapChildId` never produces (`-1`, `-02`). */
export function parseSitemapChild(id: string): SitemapChild | null {
  for (const section of SITEMAP_SECTIONS) {
    for (const locale of locales) {
      const base = `${section}-${locale}`;
      if (id === base) return { section, locale, page: 1 };
      if (id.startsWith(`${base}-`)) {
        const suffix = id.slice(base.length + 1);
        return /^(?:[2-9]|[1-9]\d+)$/.test(suffix) ? { section, locale, page: Number(suffix) } : null;
      }
    }
  }
  return null;
}

export async function generateSitemaps(): Promise<{ id: string }[]> {
  return sitemapChildren(await guideSitemapSummary()).map((id) => ({ id }));
}

/**
 * One child of the index. Next hands the id from the URL (a promise since Next 16); an id
 * outside `generateSitemaps` never reaches here because Next answers 404 for it, and the
 * empty array is only insurance against that changing.
 */
export default async function sitemap({ id }: { id: Promise<string> }): Promise<MetadataRoute.Sitemap> {
  const child = await id;
  if (child === "static") return staticSitemap();
  const target = parseSitemapChild(child);
  return target ? sectionSitemap(target) : [];
}

/** A hub advertises only the languages it is listed in, for the reason an article does:
 *  hreflang pointing at a page this file just decided not to index is a contradiction, and
 *  x-default belongs to English only while English has the section. */
const hubAlternates = (available: readonly Locale[], path: string): Record<string, string> => ({
  ...Object.fromEntries(available.map((locale) => [locale, localeUrl(locale, path)])),
  ...(available.includes(HREFLANG_DEFAULT) ? { "x-default": localeUrl(HREFLANG_DEFAULT, path) } : {}),
});

/**
 * One entry per locale per route, each carrying the full alternate set. Google wants those
 * reciprocal and self-inclusive, and Next does not add the self link. The pet-friendly place
 * pages follow the routes (`petPlaceSitemap`).
 *
 * Slugs stay bundled, but indexability depends on the current public switches. One no-store
 * visibility read keeps this list consistent with PublicFeatureGate's metadata: closed or
 * unavailable features are noindex and must not be advertised here. Core pages remain listed
 * if the settings service is unavailable. The canonical origin is still fixed at build time.
 */
async function staticSitemap(): Promise<MetadataRoute.Sitemap> {
  // The place enumeration starts alongside the switch reads rather than after them: it is the
  // one read here that pages, and it gates on the same request-scoped community state itself,
  // so a closed community costs it nothing.
  const [visibility, summary, discovery, community, places] = await Promise.all([
    getSiteVisibility(), guideSitemapSummary(), getDiscoveryStatus(), getCommunityState(), petPlaceSitemapEntries(),
  ]);
  const communityOpen = community.status === "ready" && community.flags.enabled;

  /**
   * Which languages each hub has something to show, from the same summary the index reads,
   * so a hub can never be listed while every article under it is absent from its child.
   *
   * Only an answer that arrived may remove anything. A failed read leaves every hub listed
   * for every language, which is the behaviour before this filter existed.
   */
  const hubLocales = (route: SitemapRoute): readonly Locale[] =>
    !route.hub || !summary.available
      ? locales
      : locales.filter((locale) => publishes(summary, route.hub!, locale));

  const routes = SITEMAP_ROUTES.filter(
    (route) => (!route.feature || featureEnabled(visibility, route.feature))
      && (!route.discovery || discovery.enabled)
      && (!route.community || communityOpen),
  ).flatMap((route) => {
    const available = hubLocales(route);
    const languages = available.length === locales.length
      ? languageAlternates(route.path)
      : hubAlternates(available, route.path);
    return available.map((locale) => ({
      url: localeUrl(locale, route.path),
      // No `lastModified` on these. Google honours it only where it tracks real content
      // change, and nothing here knows when a city guide's places last moved -- that lives
      // behind the API this route deliberately does not call for them. An omitted field is a
      // missing signal; one that always says "now" teaches Google to distrust the whole file.
      changeFrequency: route.changeFrequency,
      priority: route.priority,
      alternates: { languages },
    }));
  });
  // With the switch off there are no place pages, whatever a read that raced the switch
  // returned: this child and /pet-friendly itself must always agree.
  return [...routes, ...petPlaceSitemap(communityOpen ? places.entries : [])];
}

/**
 * One entry per locale per published place, after the routes and in this child rather than
 * one of their own: the section children are cut by guide section and language and the index
 * lists them from the guide summary, whereas what decides whether a place page exists is the
 * community switch this child already reads. At the enumeration's cap that is 1,000 places,
 * five rows each -- a tenth of Google's per-file limit. A child of their own is the day the
 * count needs it.
 *
 * Like the routes, each carries the full reciprocal alternate set: the page renders in every
 * locale from the one record (`names[locale] || name`), and the layout's own hreflang says
 * the same five plus x-default. Unlike them it may carry `lastModified`, from the one real
 * date a place has -- when its rules were last verified -- and only when the API sent one: a
 * place without it gets no date rather than "now".
 */
function petPlaceSitemap(places: readonly PetPlaceSitemapEntry[]): MetadataRoute.Sitemap {
  // The cursor walks (created_at, id), so a repeat is not expected; ruling one out here keeps
  // "each place once" a property of this file, as the section children do for articles.
  const listed = new Set<string>();
  return places.flatMap((place) => {
    if (listed.has(place.id)) return [];
    listed.add(place.id);
    const path = `/pet-friendly/${place.id}`;
    const languages = languageAlternates(path);
    return locales.map((locale) => ({
      url: localeUrl(locale, path),
      // Rules are re-verified and visits approved on the cadence of an evergreen article, not
      // a feed; the directory above them is weekly because its membership moves.
      changeFrequency: "monthly" as const,
      priority: 0.5,
      ...(place.verified_at ? { lastModified: new Date(place.verified_at) } : {}),
      alternates: { languages },
    }));
  });
}

/** Whether any of `kinds` has a published row in `locale`, per the summary. */
function publishes(summary: GuideSitemapSummary, kinds: readonly GuideKind[], locale: Locale): boolean {
  return summary.counts.some((row) => kinds.includes(row.kind) && row.locale === locale && row.count > 0);
}

/**
 * One section in one language: its topic hubs, then its articles -- or, for a numbered
 * child, the next `SITEMAP_CHILD_LIMIT` of its articles and no hubs, which the first child
 * already carries.
 *
 * Two things here deliberately differ from the static child, and both follow from the
 * section publishing one locale at a time:
 *
 * - `lastModified` is real on an article. It is false of a city guide and true here: the API
 *   returns when the version readers see went live (falling back to the first publication
 *   for an older API), and for a corrected notice that signal is the point.
 * - The alternates carry only the locales an article is genuinely published in, never the
 *   full five. Advertising a translation nobody wrote is the one thing per-locale
 *   publication exists to prevent, and the article page's own hreflang agrees with this.
 *   The API names those locales on every row, which is what lets a child that holds one
 *   language still point at the others.
 */
async function sectionSitemap({ section, locale, page }: SitemapChild): Promise<MetadataRoute.Sitemap> {
  const [topics, guides] = await Promise.all([
    page === 1 ? guideTopicSitemapEntries() : Promise.resolve([]),
    guideSitemapEntries({ section, locale, offset: (page - 1) * SITEMAP_CHILD_LIMIT }),
  ]);

  /**
   * Topic hubs first. Like an article hub, a topic hub is listed in a language only while
   * that language has something under the topic, and like the static routes it carries no
   * `lastModified`: the API knows when an article changed, not when a collection did. Its
   * alternates are the languages it is listed in, wherever those children live.
   */
  const topicHubs = topics
    .filter((entry) => entry.section === section && entry.locales.includes(locale))
    .map((entry) => {
      const path = guideTopicHref(entry.section, entry.slug);
      return {
        url: localeUrl(locale, path),
        changeFrequency: "weekly" as const,
        priority: 0.6,
        alternates: { languages: hubAlternates(entry.locales, path) },
      };
    });

  // The API's unique keys on the article and its locale already rule a repeated row out, and
  // the filters keep another section's or language's row out. Keeping both guards here makes
  // "this child holds only its own URLs, once" a property of this file rather than an
  // assumption about the query behind it -- and keeps the tests of that name able to fail.
  const listed = new Set<string>();
  const articles = guides.entries.flatMap((entry) => {
    if (guideSection(entry.kind) !== section || entry.locale !== locale) return [];
    const path = guideHref(entry.kind, entry.slug);
    const url = localeUrl(locale, path);
    if (listed.has(url)) return [];
    listed.add(url);
    return [{
      url,
      changeFrequency: (entry.kind === "intel" ? "daily" : "monthly") as NonNullable<
        MetadataRoute.Sitemap[number]["changeFrequency"]
      >,
      priority: 0.5,
      lastModified: new Date(entry.modified_at ?? entry.published_at),
      alternates: {
        languages: {
          ...Object.fromEntries(entry.locales.map((item) => [item, localeUrl(item, path)])),
          ...(entry.locales.includes("en") ? { "x-default": localeUrl("en", path) } : {}),
        },
      },
    }];
  });

  return [...topicHubs, ...articles];
}
