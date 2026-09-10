import type { MetadataRoute } from "next";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales } from "@/i18n/routing";
import { languageAlternates, localeUrl } from "@/lib/seo";

/**
 * Rendered per request rather than prerendered. `siteUrl` comes from NEXT_PUBLIC_SITE_URL, which
 * docker-compose.prod.yml supplies as a build arg *and* at runtime -- but only the runtime one is
 * mandatory (`:?set NEXT_PUBLIC_SITE_URL`). Baking the origin in at build time means a build that
 * missed the arg ships a sitemap full of localhost URLs, and Google rejects a sitemap whose entries
 * are on another host, so the failure is both total and silent. Regenerating this costs nothing.
 */
export const dynamic = "force-dynamic";

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
 */
export const SITEMAP_ROUTES: readonly SitemapRoute[] = [
  { path: "/", priority: 1.0, changeFrequency: "daily" },
  { path: "/hotspots", priority: 0.8, changeFrequency: "daily" },
  { path: "/foods", priority: 0.8, changeFrequency: "daily" },
  { path: "/flights/status", priority: 0.5, changeFrequency: "weekly" },
  { path: "/pricing", priority: 0.5, changeFrequency: "monthly" },
  { path: "/labs/airlines", priority: 0.4, changeFrequency: "weekly" },
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
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return SITEMAP_ROUTES.flatMap((route) =>
    locales.map((locale) => ({
      url: localeUrl(locale, route.path),
      lastModified,
      changeFrequency: route.changeFrequency,
      priority: route.priority,
      alternates: { languages: languageAlternates(route.path) },
    })),
  );
}
