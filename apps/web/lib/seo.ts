import type { Metadata } from "next";
import { locales, type Locale } from "@/i18n/routing";

/**
 * One place to build public URLs.
 *
 * The layout used to publish a fixed `canonical: ${siteUrl}/${locale}`. Next merges metadata
 * shallowly from parent to child and `alternates` is a top-level field, so a page that does not
 * set its own inherits that one verbatim — and only the destination services page ever did.
 * Every other page under /[locale]/* was telling search engines it was the locale home page.
 *
 * Nothing here reads `next/headers`: the sitemap route, the page-level helpers and the unit
 * tests all need these builders, and only the layout has a request to read the path from.
 */

export const siteUrl = (process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000").replace(/\/$/, "");

/** The version to hand a reader whose language we do not carry. Not the unprefixed path: that
 *  would resolve through `localeDetection`, and a redirect is not an answer to give a crawler. */
export const HREFLANG_DEFAULT: Locale = "en";

/**
 * `/zh-TW/foods?city=tokyo` -> `/foods`. `/en` -> `/`. Anything without a known locale prefix,
 * and anything missing, falls back to `/` so the canonical degrades to the locale home page
 * rather than inventing a path that may not exist in every language.
 *
 * Dropping the query is deliberate. `/hotspots?destination_id=tokyo` and `/explore?content=…`
 * are filtered views of one document, not separate ones.
 */
export function routePathFromRequest(value: string | null | undefined): string {
  const pathname = (value || "").split("?")[0].split("#")[0];
  if (!pathname.startsWith("/")) return "/";
  const [, first, ...rest] = pathname.split("/");
  if (!(locales as readonly string[]).includes(first)) return "/";
  const suffix = rest.join("/").replace(/\/+$/, "");
  return suffix ? `/${suffix}` : "/";
}

/** `("en", "/")` -> `https://host/en`, with no trailing slash to canonicalize against. */
export function localeUrl(locale: Locale, path: string): string {
  return `${siteUrl}/${locale}${path === "/" ? "" : path}`;
}

/** All five translations plus x-default. Google wants the set reciprocal and self-inclusive,
 *  and Next does not add the self link, so every locale is listed including the current one. */
export function languageAlternates(path: string): Record<string, string> {
  return {
    ...Object.fromEntries(locales.map((value) => [value, localeUrl(value, path)])),
    "x-default": localeUrl(HREFLANG_DEFAULT, path),
  };
}

export function alternatesFor(locale: Locale, path: string): Metadata["alternates"] {
  return { canonical: localeUrl(locale, path), languages: languageAlternates(path) };
}

/**
 * Page-level metadata with the canonical, the alternates and an Open Graph block that agrees
 * with this page's own title rather than the site-wide one.
 *
 * Callers pass the resolved strings rather than a message key on purpose:
 * `app/[locale]/metadata.test.ts` reads page sources for a literal `title: t("someKey")`, so the
 * key has to stay visible at the call site.
 */
export function pageMetadata(input: {
  locale: Locale;
  path: string;
  title: string;
  description: string;
  images?: string[];
  type?: "website" | "article";
  robots?: Metadata["robots"];
}): Metadata {
  const { locale, path, title, description, images = ["/og.png"], type = "website", robots } = input;
  return {
    title,
    description,
    alternates: alternatesFor(locale, path),
    openGraph: {
      title,
      description,
      url: localeUrl(locale, path),
      images,
      locale: locale.replace("-", "_"),
      alternateLocale: locales.filter((value) => value !== locale).map((value) => value.replace("-", "_")),
      type,
    },
    twitter: { card: "summary_large_image", title, description, images },
    ...(robots ? { robots } : {}),
  };
}
