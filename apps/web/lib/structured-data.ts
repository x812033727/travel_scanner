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

/** The brand as a nested node. No `@context`: a node inside another graph inherits the
 *  enclosing one, and repeating it is noise a validator has to look past. */
function brand(): object {
  return {
    "@type": "Organization",
    name: BRAND,
    url: siteUrl,
    logo: `${siteUrl}/brand/mokaair-monogram.png`,
  };
}

export function organization(): object {
  return { "@context": CONTEXT, ...brand() };
}

export function webSite(locale: Locale, searchEnabled = true): object {
  return {
    "@context": CONTEXT,
    "@type": "WebSite",
    name: BRAND,
    url: localeUrl(locale, "/"),
    inLanguage: locale,
    // /hotspots really does take `q` and filter on it, so this is a search endpoint a reader can
    // land on, not a shape invented to earn a sitelinks search box.
    ...(searchEnabled ? { potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${localeUrl(locale, "/hotspots")}?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    } } : {}),
  };
}

export type Crumb = { name: string; path: string };

/** The trail a reader walked, in order, starting at the locale home page. */
export function breadcrumbs(locale: Locale, trail: readonly Crumb[]): object | null {
  if (!trail.length) return null;
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

/** A list whose entries have their own pages. Entries without a URL are left unmarked: a
 *  ListItem a crawler cannot follow is not worth describing. */
export function itemList(locale: Locale, items: readonly Crumb[]): object | null {
  if (!items.length) return null;
  return {
    "@context": CONTEXT,
    "@type": "ItemList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      url: localeUrl(locale, item.path),
    })),
  };
}

export function touristDestination(
  locale: Locale,
  input: {
    name: string;
    path: string;
    description: string;
    country: string;
    alternateName?: readonly string[];
    center?: { latitude: number; longitude: number } | null;
  },
): object {
  const alternateName = (input.alternateName ?? []).filter((value) => value && value !== input.name);
  return {
    "@context": CONTEXT,
    "@type": "TouristDestination",
    name: input.name,
    url: localeUrl(locale, input.path),
    // No `inLanguage`: TouristDestination derives from Place, and inLanguage is a CreativeWork
    // property. Validators flag it as unexpected. It is correct on WebSite above.
    ...(input.description ? { description: input.description } : {}),
    ...(alternateName.length ? { alternateName } : {}),
    ...(input.country ? { containedInPlace: { "@type": "Country", name: input.country } } : {}),
    ...(input.center
      ? { geo: { "@type": "GeoCoordinates", latitude: input.center.latitude, longitude: input.center.longitude } }
      : {}),
  };
}

/** One entry of an article's source list: what was read, where, and when it was checked. */
export type Reference = { title: string; url: string; checkedOn?: string | null };

/**
 * A published guide, intel notice or lifestyle article.
 *
 * This graph used to be an object literal inside `guides/article-page.tsx` -- the only one on
 * the site built outside this file, and so the only one with no test. It had drifted to the
 * six fields someone typed once, while the page below it rendered four more the graph never
 * mentioned: the dated source list, the topic chips, the destination the article is about,
 * and the reading time. Everything added here is read off that same rendered page.
 *
 * `citation` is the reason this exists. Every published document carries its sources -- the
 * page prints them with the date each was checked -- and an answer engine deciding whether to
 * repeat a fare or a train time is deciding on exactly that provenance. Passing them through
 * `contentBlockLink` at the call site, as the renderer does, keeps the graph from naming a
 * source the page itself refused to draw.
 *
 * Deliberately absent, and not oversights:
 * - `dateAccessed` on a citation. It is not a schema.org property; `checked_on` says when *we*
 *   read the source, which is `lastReviewed` on the WebPage below, not a claim about theirs.
 * - `lastReviewed` / `reviewedBy` on the article itself. Both are WebPage properties, so they
 *   belong on `mainEntityOfPage` -- the same trap `touristDestination` records for `inLanguage`.
 * - `author` as a Person. No document carries a byline; the only `author` in the content schema
 *   is a photographer's credit. An Organization author is accurate and is accepted.
 * - `expires`, from an intel notice's `valid_until`. schema.org reads it as "stop serving this",
 *   and the product deliberately keeps an expired notice online and its URL working -- the
 *   article renderer states that rule as "no expiry banner, no date it applied until". Publishing
 *   the withheld date to ask an answer engine to stop citing the page is both dishonest and the
 *   opposite of what this graph is for.
 * - `HowTo` for `kind === "howto"`, and `FAQPage` anywhere. See the note at the foot of this file.
 */
export function guideArticle(
  locale: Locale,
  input: {
    path: string;
    title: string;
    description: string;
    publishedAt: string;
    /** Moves on republication where `publishedAt` does not; absent on an older API. */
    modifiedAt?: string | null;
    hero?: { src: string; width: number; height: number } | null;
    /** The listing the reader returns to, named as the breadcrumb names it. */
    section: string;
    /** Topic labels, as the chips under the article spell them -- not their slugs, which
     *  say nothing to a crawler. */
    keywords?: readonly string[];
    /** The place the article is about, when it has one. 319 of 398 articles do not. */
    destination?: Crumb | null;
    references?: readonly Reference[];
    minutes?: number;
    /** A series hub describes a collection rather than an article. */
    collection?: boolean;
    /** The hub's members, when the series listing resolved. */
    entries?: readonly Crumb[] | null;
  },
): object {
  const url = localeUrl(locale, input.path);
  const keywords = (input.keywords ?? []).filter(Boolean);
  const references = input.references ?? [];
  // ISO `YYYY-MM-DD` sorts lexicographically, so the newest check is a plain string max and
  // needs no Date parsing. `checked_on` is nullable in the schema even though nothing currently
  // omits it, so the nulls are dropped rather than compared.
  const checked = references.map((row) => row.checkedOn).filter((value): value is string => !!value);
  const lastReviewed = checked.length ? checked.reduce((left, right) => (right > left ? right : left)) : null;
  return {
    "@context": CONTEXT,
    "@type": input.collection ? "CollectionPage" : "Article",
    headline: input.title,
    name: input.title,
    description: input.description,
    url,
    inLanguage: locale,
    datePublished: input.publishedAt,
    dateModified: input.modifiedAt ?? input.publishedAt,
    ...(input.hero
      ? { image: { "@type": "ImageObject", url: `${siteUrl}${input.hero.src}`, width: input.hero.width, height: input.hero.height } }
      : {}),
    articleSection: input.section,
    // `keywords` takes Text, so the labels are joined rather than listed.
    ...(keywords.length ? { keywords: keywords.join(", ") } : {}),
    ...(input.destination
      ? { about: { "@type": "TouristDestination", name: input.destination.name, url: localeUrl(locale, input.destination.path) } }
      : {}),
    ...(input.minutes ? { timeRequired: `PT${input.minutes}M` } : {}),
    isAccessibleForFree: true,
    ...(references.length
      ? { citation: references.map((row) => ({ "@type": "CreativeWork", name: row.title, url: row.url })) }
      : {}),
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": url,
      ...(lastReviewed ? { lastReviewed } : {}),
      reviewedBy: brand(),
    },
    author: brand(),
    publisher: brand(),
    ...(input.entries?.length
      ? { mainEntity: {
          "@type": "ItemList",
          itemListElement: input.entries.map((entry, index) => ({
            "@type": "ListItem", position: index + 1, name: entry.name, url: localeUrl(locale, entry.path),
          })),
        } }
      : {}),
  };
}

/**
 * Two graphs this corpus looks like it should carry and must not.
 *
 * `HowTo`, for the 106 `howto` articles: only 20 of them hold an ordered list at all, and those
 * are itineraries rather than procedures -- clocked departures a reader may join at any point.
 * One is the inverse of a procedure: `taoyuan-airport-departure-guide` enumerates who is barred
 * from e-Gate, which as `HowToStep` instructs the reader to obtain an exit ban. `ordered: true`
 * in these packs means "numbered for reading". A step list needs an author to declare one.
 *
 * `FAQPage`: only 10 of 498 documents hold two question-heading-and-answer pairs, and the
 * headings that match are section titles (`怎麼去：JR 舞濱、迪士尼度假區線`), not questions.
 * Google has restricted FAQ rich results to health and government sites since 2023, so the
 * upside is machine-readers only -- who are the same audience that discounts a site whose
 * markup does not match its page.
 */
