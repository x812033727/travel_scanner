import { cache } from "react";
import { isSitePageDocument, sitePageLocales, type PublishedSitePage, type SitePageLocale, type SitePagePublicState, type SitePageSlug } from "./site-pages";

// Public legal-page labels and empty/error states cannot become an alternate
// publication channel through general UI-text overrides. Never fall back a locale.
export async function getSitePageCopy(locale: string): Promise<typeof import("../messages/en/admin.json")["sitePages"]> {
  if (!sitePageLocales.includes(locale as SitePageLocale)) throw new Error("Unsupported site-page locale");
  return (await import(`../messages/${locale}/admin.json`)).default.sitePages;
}

export async function loadSitePage(slug: SitePageSlug, locale: string): Promise<SitePagePublicState> {
  const unavailable: SitePagePublicState = { slug, locale, status: "unavailable", document: null };
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/site-pages/${slug}?locale=${encodeURIComponent(locale)}`, {
      cache: "no-store", headers: { Accept: "application/json" }, signal: AbortSignal.timeout(3000),
    });
    if (!response.ok) return unavailable;
    const row = await response.json();
    if (row.slug !== slug || row.locale !== locale) return unavailable;
    if (row.status === "unpublished" && row.document === null) return { slug, locale, status: "unpublished", document: null };
    if (row.status !== "published" || !isSitePageDocument(row.document)
      || typeof row.document.version !== "number" || typeof row.document.published_at !== "string") return unavailable;
    return { slug, locale, status: "published", document: row.document as PublishedSitePage };
  } catch { return unavailable; }
}

// React cache is per request: metadata and body agree without caching a policy across requests.
export const getSitePage = cache(loadSitePage);
