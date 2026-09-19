import type { Locale } from "@/i18n/routing";
import type { FoodMerchant, MerchantSource } from "@/lib/foods";
import { safeExternalHref } from "@/lib/navigation";
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
 * - `HowTo` for `kind === "howto"`, and an `FAQPage` read out of headings. See the note at the
 *   foot of this file. An `FAQPage` the editor wrote as a `faq` block is a different thing and
 *   has its own builder, `faqPage`, below.
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
    /** The editor's summary block: the answer in two to five sentences. Becomes `abstract`,
     *  and the card that shows it (`#article-summary`) becomes the speakable passage. */
    abstract?: readonly string[] | null;
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
    ...(input.abstract?.length
      ? {
          abstract: input.abstract.join(" "),
          speakable: { "@type": "SpeakableSpecification", cssSelector: ["#article-summary"] },
        }
      : {}),
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
 * The questions an editor wrote as a `faq` block, each with its answer, as the page shows
 * them. Only from that block: a question is a question because the editor said so, never
 * because a heading ends in one (see the note at the foot of this file). Google has shown
 * FAQ rich results only for government and health sites since 2023; the audience for this
 * graph is the answer engines, who read the same `<details>` the reader does.
 */
export function faqPage(
  locale: Locale, path: string, items: readonly { question: string; answer: string }[],
): object | null {
  const questions = items.filter((item) => item.question.trim() && item.answer.trim());
  if (!questions.length) return null;
  return {
    "@context": CONTEXT,
    "@type": "FAQPage",
    "@id": `${localeUrl(locale, path)}#faq`,
    mainEntity: questions.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };
}

/**
 * A glossary entry: the article defines the term its title names, answers to the names in
 * `aliases`, and belongs to the glossary `set` (the hub article of a catalogue-type
 * series). Emitted only for an article the API says is an entry of a set.
 */
export function definedTerm(
  locale: Locale,
  input: { path: string; name: string; description: string; aliases?: readonly string[]; set: Crumb },
): object {
  const aliases = (input.aliases ?? []).map((name) => name.trim()).filter((name) => name && name !== input.name);
  const url = localeUrl(locale, input.path);
  return {
    "@context": CONTEXT,
    "@type": "DefinedTerm",
    "@id": `${url}#term`,
    name: input.name,
    description: input.description,
    url,
    inLanguage: locale,
    ...(aliases.length ? { alternateName: aliases } : {}),
    inDefinedTermSet: { "@type": "DefinedTermSet", name: input.set.name, url: localeUrl(locale, input.set.path) },
  };
}

/** The fields of a merchant card this graph reads; a `FoodMerchant` satisfies it. */
export type MerchantCard = Pick<FoodMerchant, "id" | "name" | "local_name" | "destination_name" | "address"> & {
  sources: readonly Pick<MerchantSource, "title" | "url" | "distinction">[];
};

/** The distinction badges a card can draw, by catalog key, spelled as the card spells them in
 *  the reader's language. Resolved by the caller, so the builder stays free of translation
 *  lookups. */
export type Awards = Readonly<Record<string, string>>;

/**
 * One merchant of the food directory, read off its card on `/foods`.
 *
 * A restaurant is the clearest kind of entity an answer engine meets -- a name, a place, and
 * the sources it was checked against -- and the card already prints all three. Every property
 * here is something the card draws:
 * - `@id` is the card's own anchor, `#merchant-<id>`: the fragment the share button hands out
 *   and `useSharedAnchor` scrolls to.
 * - `alternateName` is the original-script name under the heading, when it differs.
 * - `address` carries the one address line the catalog stores as `streetAddress`, and the
 *   destination the card names beside the pin as `addressLocality`. No country, region or
 *   postcode: the card prints none as such, and the line usually holds them anyway.
 * - `award` is the distinction badge: the first source whose distinction the card has a label
 *   for, which is how the card picks it.
 * - `citation` is the source list under the card, one `CreativeWork` per source, with its `url`
 *   only when the card drew the title as a link -- through `safeExternalHref`, the same test the
 *   card applies, so the graph never names a link the page refused to draw.
 *
 * Deliberately absent, and not oversights:
 * - `aggregateRating` and `review`. Nothing on this site collects a rating: the interest score
 *   is Mokaair's own signal, not a reader's, and rating markup over it would be invented review
 *   markup -- the line `docs/seo.md` draws against Product/Offer markup, drawn again here.
 * - The "Sources checked on" date under the source list. It says when *we* checked the
 *   merchant's sources, which is `lastReviewed`, a WebPage property; a merchant has no page of
 *   its own here, and stamping the date on the list page would claim one review date for a
 *   page that shows twenty. The trap `guideArticle` records for `dateAccessed`, one level up.
 * - `url` and `sameAs` from `official_website_url`. The card draws that link only after a
 *   stricter check than `safeExternalHref` (https only, no credentials, no bare or local hosts)
 *   that lives inside the card's link component, so naming the raw field could name a website
 *   the card refused to draw.
 * - `servesCuisine` from the category chips, which mix cuisines with venue types (a cafe is not
 *   a cuisine), and `geo`, `openingHours`, `telephone`, `priceRange`, `hasMenu`: the card
 *   renders none of them.
 */
export function foodEstablishment(locale: Locale, card: MerchantCard, awards: Awards): object {
  const distinction = card.sources
    .map((source) => source.distinction)
    .find((value): value is string => !!value && Object.hasOwn(awards, value));
  const award = distinction ? awards[distinction] : "";
  const postal = {
    ...(card.address ? { streetAddress: card.address } : {}),
    ...(card.destination_name ? { addressLocality: card.destination_name } : {}),
  };
  return {
    "@context": CONTEXT,
    "@type": "FoodEstablishment",
    "@id": `${localeUrl(locale, "/foods")}#merchant-${card.id}`,
    name: card.name,
    ...(card.local_name && card.local_name !== card.name ? { alternateName: card.local_name } : {}),
    ...(Object.keys(postal).length ? { address: { "@type": "PostalAddress", ...postal } } : {}),
    ...(award ? { award } : {}),
    ...(card.sources.length
      ? { citation: card.sources.map((source) => {
          const url = safeExternalHref(source.url);
          return { "@type": "CreativeWork", name: source.title, ...(url ? { url } : {}) };
        }) }
      : {}),
  };
}

/**
 * The merchants the server-rendered `/foods` drew, one `FoodEstablishment` each.
 *
 * `seed` is the merchant list the page hands `FoodBrowser` as `initialMerchants`, as the API
 * returned it, and the cards on the server-rendered page are that list's `items` and nothing
 * else -- so the graph reads the array the cards read. That is what keeps it honest about the
 * directory's withheld states: a merchant under moderation, without an exact map identity or
 * without a current source never reaches `items` (the API's publication gate filters them in
 * SQL, and the list is fetched `no-store`), and when the seed did not arrive the server rendered
 * no card and the browser fetches the list after hydration -- a list this graph must never run
 * ahead of, so it returns nothing. The `Array.isArray(items)` test is the browser's own.
 */
export function foodEstablishments(locale: Locale, seed: unknown, awards: Awards): object[] {
  const items = typeof seed === "object" && seed !== null ? (seed as { items?: unknown }).items : undefined;
  if (!Array.isArray(items)) return [];
  return (items as MerchantCard[]).map((card) => foodEstablishment(locale, card, awards));
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
 * `FAQPage` derived from headings: only 10 of 498 documents hold two question-heading-and-answer
 * pairs, and the headings that match are section titles (`怎麼去：JR 舞濱、迪士尼度假區線`), not
 * questions. Google has restricted FAQ rich results to health and government sites since 2023,
 * so the upside is machine-readers only -- who are the same audience that discounts a site
 * whose markup does not match its page. That is why `faqPage` above takes only the `faq` block
 * an editor wrote (2026-09-16): the questions on the page and the questions in the graph are
 * then the same list, by construction.
 */
