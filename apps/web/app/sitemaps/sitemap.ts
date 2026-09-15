import type { MetadataRoute } from "next";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales, type Locale } from "@/i18n/routing";
import { guideHref, guideSection, guideTopicHref, type GuideKind, type GuideSection } from "@/lib/guides";
import { HREFLANG_DEFAULT, languageAlternates, localeUrl } from "@/lib/seo";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";
import {
  guideSitemapEntries, guideSitemapSummary, guideTopicSitemapEntries, type GuideSitemapSummary,
} from "@/lib/guides.server";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { getCommunityState } from "@/lib/community/server";

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
 * - the per-record community routes -- /pet-friendly/{id}, /community/posts/{id} and
 *   /community/profiles/{handle}. They server-render and are indexable now, but enumerating
 *   them means paging the API from this route on every crawl, which is a separate change
 *   (2026-09-14-sitemap-lists-pet-friendly-places). /pet-friendly links to every place it
 *   lists, so the detail pages are reachable meanwhile.
 * - every member and token route, which carries `noindex`.
 * - an article hub in a language that has nothing published in it. Those pages exist and
 *   answer 200, but with one sentence saying the section is empty; `hub` below lists them
 *   per language instead of per route, and their own `generateMetadata` agrees.
 * - /destinations/osaka/services and /destinations/kyoto/services. The services page accepts
 *   CITIES as well as PUBLIC_DESTINATIONS. Those legacy single-city service views are distinct
 *   from the combined guide, but are not part of this public destination directory.
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
  // The guides are the destination-scoped content; the services pages are an affiliate lodging
  // directory for the same city, so they rank below their own guide rather than beside it.
  ...PUBLIC_DESTINATIONS.map((id) => ({
    path: `/destinations/${id}`,
    priority: 0.7,
    changeFrequency: "weekly" as const,
  })),
  ...PUBLIC_DESTINATIONS.map((id) => ({
    path: `/destinations/${id}/services`,
    priority: 0.4,
    changeFrequency: "monthly" as const,
  })),
];

/**
 * The children of the sitemap index, by id. `static` carries every route below; each
 * `{section}-{locale}` child carries that section's topic hubs and articles in that
 * language. Fixed, not derived from a row count: Next calls `generateSitemaps` during
 * `next build`, where there is no API to ask, so the list has to be knowable without one.
 * A child with nothing published answers an empty file, and the index (`sitemap.xml/route.ts`)
 * leaves it out while the summary can be read.
 */
export const SITEMAP_SECTIONS: readonly GuideSection[] = ["travel", "life"];
export const SITEMAP_CHILDREN: readonly string[] = [
  "static",
  ...SITEMAP_SECTIONS.flatMap((section) => locales.map((locale) => `${section}-${locale}`)),
];

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

/** The section and locale a child id names, or null for `static` and anything unknown. */
export function parseSitemapChild(id: string): { section: GuideSection; locale: Locale } | null {
  for (const section of SITEMAP_SECTIONS) {
    for (const locale of locales) {
      if (id === `${section}-${locale}`) return { section, locale };
    }
  }
  return null;
}

export async function generateSitemaps(): Promise<{ id: string }[]> {
  return SITEMAP_CHILDREN.map((id) => ({ id }));
}

/**
 * One child of the index. Next hands the id from the URL (a promise since Next 16); an id
 * outside `SITEMAP_CHILDREN` never reaches here because Next answers 404 for it, and the
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
 * reciprocal and self-inclusive, and Next does not add the self link.
 *
 * Slugs stay bundled, but indexability depends on the current public switches. One no-store
 * visibility read keeps this list consistent with PublicFeatureGate's metadata: closed or
 * unavailable features are noindex and must not be advertised here. Core pages remain listed
 * if the settings service is unavailable. The canonical origin is still fixed at build time.
 */
async function staticSitemap(): Promise<MetadataRoute.Sitemap> {
  const [visibility, summary, discovery, community] = await Promise.all([
    getSiteVisibility(), guideSitemapSummary(), getDiscoveryStatus(), getCommunityState(),
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

  return SITEMAP_ROUTES.filter(
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
}

/** Whether any of `kinds` has a published row in `locale`, per the summary. */
function publishes(summary: GuideSitemapSummary, kinds: readonly GuideKind[], locale: Locale): boolean {
  return summary.counts.some((row) => kinds.includes(row.kind) && row.locale === locale && row.count > 0);
}

/**
 * One section in one language: its topic hubs, then its articles.
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
async function sectionSitemap({ section, locale }: { section: GuideSection; locale: Locale }): Promise<MetadataRoute.Sitemap> {
  const [topics, guides] = await Promise.all([
    guideTopicSitemapEntries(),
    guideSitemapEntries({ section, locale }),
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
