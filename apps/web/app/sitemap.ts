import type { MetadataRoute } from "next";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales, type Locale } from "@/i18n/routing";
import { guideHref, type GuideKind } from "@/lib/guides";
import { guideSitemapEntries, type GuideSitemapEntry } from "@/lib/guides.server";
import { HREFLANG_DEFAULT, languageAlternates, localeUrl } from "@/lib/seo";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";
import { getSiteVisibility } from "@/lib/site-visibility.server";

// Evaluate public switches and published guides at request time, not while building without the API.
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
 * - /guides/{kind}/{slug}. Which articles exist, and in which languages, is only known at request
 *   time, so `sitemap()` appends them from the guides API after these routes.
 */
export const SITEMAP_ROUTES: readonly SitemapRoute[] = [
  { path: "/", priority: 1.0, changeFrequency: "daily" },
  { path: "/hotspots", priority: 0.8, changeFrequency: "daily", feature: "hotspots" },
  { path: "/foods", priority: 0.8, changeFrequency: "daily" },
  { path: "/flights/status", priority: 0.5, changeFrequency: "weekly", feature: "flight_status" },
  { path: "/pricing", priority: 0.5, changeFrequency: "monthly", feature: "pricing" },
  { path: "/labs/airlines", priority: 0.4, changeFrequency: "weekly", feature: "airline_fares" },
  { path: "/destinations", priority: 0.6, changeFrequency: "weekly" },
  // First-party editorial content with no switch behind it. Intel is the time-sensitive half, so
  // its list, and the hub that leads with it, change daily.
  { path: "/guides", priority: 0.6, changeFrequency: "daily" },
  { path: "/guides/intel", priority: 0.6, changeFrequency: "daily" },
  { path: "/guides/howto", priority: 0.6, changeFrequency: "weekly" },
  // The city guides are the destination-scoped content; the services pages are an affiliate lodging
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

/** Hints for article entries. Intel is revised or withdrawn as fares and rules change; a how-to
 *  stays true for longer. */
const GUIDE_ARTICLE_HINTS: Record<GuideKind, Pick<SitemapRoute, "priority" | "changeFrequency">> = {
  intel: { priority: 0.5, changeFrequency: "weekly" },
  howto: { priority: 0.5, changeFrequency: "monthly" },
};

/** Only the translations that exist, plus `x-default` when English is one of them: the set the
 *  article page declares in its head. Advertising a missing translation would send Google to a
 *  `noindex` "not translated" page. */
function publishedAlternates(path: string, translations: readonly Locale[]): Record<string, string> {
  const languages: Record<string, string> = Object.fromEntries(translations.map((locale) => [locale, localeUrl(locale, path)]));
  if (translations.includes(HREFLANG_DEFAULT)) languages["x-default"] = localeUrl(HREFLANG_DEFAULT, path);
  return languages;
}

/**
 * One entry per published translation, in the API's newest-first order. Unlike the static routes
 * these carry `lastModified`, because the guides API returns each translation's real publication
 * date rather than a guess.
 */
function guideArticleEntries(rows: readonly GuideSitemapEntry[]): MetadataRoute.Sitemap {
  const translations = new Map<string, Set<Locale>>();
  for (const row of rows) {
    const path = guideHref(row.kind, row.slug);
    translations.set(path, (translations.get(path) ?? new Set<Locale>()).add(row.locale));
  }
  // The API's unique keys already rule out a repeated row; this makes "no duplicate URL" a
  // property of the sitemap instead of an assumption about the query behind it.
  const listed = new Set<string>();
  return rows.flatMap((row) => {
    const path = guideHref(row.kind, row.slug);
    const url = localeUrl(row.locale, path);
    if (listed.has(url)) return [];
    listed.add(url);
    const published = locales.filter((locale) => translations.get(path)?.has(locale));
    return [{
      url,
      lastModified: new Date(row.published_at),
      ...GUIDE_ARTICLE_HINTS[row.kind],
      alternates: { languages: publishedAlternates(path, published) },
    }];
  });
}

/**
 * One entry per locale per static route, each carrying the full alternate set. Google wants those
 * reciprocal and self-inclusive, and Next does not add the self link. Guide articles follow, one
 * entry per published translation, each carrying only its own article's translations.
 *
 * Slugs stay bundled, but indexability depends on the current public switches. One no-store
 * visibility read keeps this list consistent with PublicFeatureGate's metadata: closed or
 * unavailable features are noindex and must not be advertised here. Core pages remain listed
 * if the settings service is unavailable. The canonical origin is still fixed at build time.
 *
 * The articles come from one no-store read of the guides API, made alongside the visibility read.
 * When it fails the loader answers `[]`, so an outage leaves exactly the static list rather than
 * an error or an empty file.
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [visibility, guides] = await Promise.all([getSiteVisibility(), guideSitemapEntries()]);
  const staticEntries = SITEMAP_ROUTES.filter((route) => !route.feature || featureEnabled(visibility, route.feature)).flatMap((route) =>
    locales.map((locale) => ({
      url: localeUrl(locale, route.path),
      // No `lastModified` here. Google honours it only where it tracks real content change, and
      // nothing here knows when a city guide's places last moved -- that lives behind the hotspot
      // and merchant APIs this route does not call. An omitted field is a missing signal; one that
      // always says "now" teaches Google to distrust the whole file. Guide articles, which do have
      // a real date, are the one exception (`guideArticleEntries`).
      changeFrequency: route.changeFrequency,
      priority: route.priority,
      alternates: { languages: languageAlternates(route.path) },
    })),
  );
  // Articles strictly after the static routes, so the static part reads the same with or without them.
  return [...staticEntries, ...guideArticleEntries(guides)];
}
