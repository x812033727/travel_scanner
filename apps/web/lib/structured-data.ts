import type { Locale } from "@/i18n/routing";
import { localeUrl, siteUrl } from "@/lib/seo";

/**
 * schema.org graphs, as plain data.
 *
 * Pure functions on purpose: no `headers()`, no fetching, no translation lookups. Callers pass
 * text they have already resolved, which keeps these testable and keeps a page from paying for a
 * second round trip just to describe what it already rendered.
 *
 * Nothing here describes something the page does not show. An `ItemList` whose entries have no
 * URLs, or an `FAQPage` without a question on the page, is markup a crawler cannot act on and
 * Search Console can flag -- so those wait until there is something real to point at.
 */

const CONTEXT = "https://schema.org";
const BRAND = "Mokaair";

export function organization(): object {
  return {
    "@context": CONTEXT,
    "@type": "Organization",
    name: BRAND,
    url: siteUrl,
    logo: `${siteUrl}/brand/mokaair-monogram.png`,
  };
}

export function webSite(locale: Locale): object {
  return {
    "@context": CONTEXT,
    "@type": "WebSite",
    name: BRAND,
    url: localeUrl(locale, "/"),
    inLanguage: locale,
    // /hotspots really does take `q` and filter on it, so this is a search endpoint a reader can
    // land on, not a shape invented to earn a sitelinks search box.
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${localeUrl(locale, "/hotspots")}?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  };
}

export type Crumb = { name: string; path: string };

/** The trail a reader walked, in order, starting at the locale home page. */
export function breadcrumbs(locale: Locale, trail: readonly Crumb[]): object {
  return {
    "@context": CONTEXT,
    "@type": "BreadcrumbList",
    itemListElement: trail.map((crumb, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: crumb.name,
      item: localeUrl(locale, crumb.path),
    })),
  };
}
