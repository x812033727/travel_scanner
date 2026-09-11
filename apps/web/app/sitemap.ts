import type { MetadataRoute } from "next";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales } from "@/i18n/routing";
import { languageAlternates, localeUrl } from "@/lib/seo";

type SitemapRoute = {
  /** Path after the locale prefix, as `routePathFromRequest` produces it. */
  path: string;
  priority: number;
  changeFrequency: NonNullable<MetadataRoute.Sitemap[number]["changeFrequency"]>;
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
 *   CITIES as well as PUBLIC_DESTINATIONS, so those two resolve, self-canonicalize and duplicate
 *   /destinations/osaka-kyoto/services -- whose guide is the only one of the three that exists.
 *   Listing them would be advertising a duplicate whose parent 404s; the canonical belongs on
 *   the services page itself, which is another task's file.
 */
export const SITEMAP_ROUTES: readonly SitemapRoute[] = [
  { path: "/", priority: 1.0, changeFrequency: "daily" },
  { path: "/hotspots", priority: 0.8, changeFrequency: "daily" },
  { path: "/foods", priority: 0.8, changeFrequency: "daily" },
  { path: "/flights/status", priority: 0.5, changeFrequency: "weekly" },
  { path: "/pricing", priority: 0.5, changeFrequency: "monthly" },
  { path: "/labs/airlines", priority: 0.4, changeFrequency: "weekly" },
  { path: "/destinations", priority: 0.6, changeFrequency: "weekly" },
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
 * No API call: the destination slugs are already in the bundle and a sitemap needs URLs, not
 * names, so it needs neither localization nor network. That is not a preference --
 * `API_INTERNAL_URL` only exists at runtime, this route is prerendered at build time, and the CI
 * web job has no API, so a fetch here would silently bake in an empty sitemap.
 *
 * Prerendered on purpose, and `siteUrl` being fixed at build is not a reason to change that:
 * NEXT_PUBLIC_* is inlined into the server bundle, so a dynamic route would read the same baked
 * value. apps/web/Dockerfile fails the build outright when the arg is missing, so there is no
 * "built without an origin" case to defend against.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  return SITEMAP_ROUTES.flatMap((route) =>
    locales.map((locale) => ({
      url: localeUrl(locale, route.path),
      // No `lastModified`. Google honours it only where it tracks real content change, and
      // nothing here knows when a city guide's places last moved -- that lives behind the API
      // this route deliberately does not call. An omitted field is a missing signal; one that
      // always says "now" teaches Google to distrust the whole file.
      changeFrequency: route.changeFrequency,
      priority: route.priority,
      alternates: { languages: languageAlternates(route.path) },
    })),
  );
}
