import type { MetadataRoute } from "next";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales } from "@/i18n/routing";
import { guideHref } from "@/lib/guides";
import { languageAlternates, localeUrl } from "@/lib/seo";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";
import { guideSitemapEntries } from "@/lib/guides.server";
import { getSiteVisibility } from "@/lib/site-visibility.server";

// Evaluate public switches at request time, not while building without the API.
export const dynamic = "force-dynamic";

type SitemapRoute = {
  /** Path after the locale prefix, as `routePathFromRequest` produces it. */
  path: string;
  priority: number;
  changeFrequency: NonNullable<MetadataRoute.Sitemap[number]["changeFrequency"]>;
  feature?: SiteFeature;
};

/**
 * A route belongs here only once it is genuinely indexable.
 *
 * Deliberately absent:
 * - /about, /privacy, /terms and /contact. `site-information-page.tsx` returns `noindex` until
 *   an administrator publishes the managed document, so listing them now would only accumulate
 *   "Excluded by noindex" in Search Console. They are linked from the footer, so nothing is lost
 *   by waiting for 2026-09-06-legal-content-from-owner.
 * - /explore, /explore/collections, /pet-friendly and the community routes, which are `noindex`
 *   because their content is fetched after hydration and the server sends an empty shell.
 * - every member and token route, which carries `noindex`.
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
  // No `feature`: the guides section is first-party content with no switch behind it, so it
  // is never one of the conditional routes. The two kind hubs resolve through the `[kind]`
  // folder; `/life` is its own folder, because `/guides/life/...` is deliberately a 404.
  { path: "/guides", priority: 0.7, changeFrequency: "daily" },
  { path: "/guides/intel", priority: 0.7, changeFrequency: "daily" },
  { path: "/guides/howto", priority: 0.6, changeFrequency: "weekly" },
  // Same shape as /guides/howto on purpose: a hub of evergreen articles that are themselves
  // listed as monthly below. Claiming daily for a page that changes when an editor publishes
  // would be the same invented signal the lastmod comment further down warns about.
  { path: "/life", priority: 0.6, changeFrequency: "weekly" },
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
 * One entry per locale per route, each carrying the full alternate set. Google wants those
 * reciprocal and self-inclusive, and Next does not add the self link.
 *
 * Slugs stay bundled, but indexability depends on the current public switches. One no-store
 * visibility read keeps this list consistent with PublicFeatureGate's metadata: closed or
 * unavailable features are noindex and must not be advertised here. Core pages remain listed
 * if the settings service is unavailable. The canonical origin is still fixed at build time.
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [visibility, guides] = await Promise.all([getSiteVisibility(), guideSitemapEntries()]);
  const routes = SITEMAP_ROUTES.filter(
    (route) => !route.feature || featureEnabled(visibility, route.feature),
  ).flatMap((route) =>
    locales.map((locale) => ({
      url: localeUrl(locale, route.path),
      // No `lastModified` on these. Google honours it only where it tracks real content
      // change, and nothing here knows when a city guide's places last moved -- that lives
      // behind the API this route deliberately does not call for them. An omitted field is a
      // missing signal; one that always says "now" teaches Google to distrust the whole file.
      changeFrequency: route.changeFrequency,
      priority: route.priority,
      alternates: { languages: languageAlternates(route.path) },
    })),
  );

  /**
   * Guide articles, appended after the static routes so their exact order stays testable.
   *
   * Two things here deliberately differ from every route above, and both follow from the
   * section publishing one locale at a time:
   *
   * - `lastModified` is real. The comment above is true of a city guide and false of an
   *   article: the API returns the actual publication date, and for a dated notice that
   *   signal is the point.
   * - The alternates carry only the locales an article is genuinely published in, never the
   *   full five. Advertising a translation nobody wrote is the one thing per-locale
   *   publication exists to prevent, and the article page's own hreflang agrees with this.
   */
  // The API's unique keys on the article and its locale already rule a repeated row out. Keeping
  // the guard here makes "no duplicate URL" a property of this file rather than an assumption
  // about the query behind it -- and keeps the test of that name able to fail.
  const listed = new Set<string>();
  const articles = guides.flatMap((entry) => {
    const path = guideHref(entry.kind, entry.slug);
    const url = localeUrl(entry.locale, path);
    if (listed.has(url)) return [];
    listed.add(url);
    return [{
      url,
      changeFrequency: (entry.kind === "intel" ? "daily" : "monthly") as NonNullable<
        MetadataRoute.Sitemap[number]["changeFrequency"]
      >,
      priority: 0.5,
      lastModified: new Date(entry.published_at),
      alternates: {
        languages: {
          ...Object.fromEntries(entry.locales.map((locale) => [locale, localeUrl(locale, path)])),
          ...(entry.locales.includes("en") ? { "x-default": localeUrl("en", path) } : {}),
        },
      },
    }];
  });

  return [...routes, ...articles];
}
