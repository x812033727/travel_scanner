import type { Metadata, ResolvingMetadata } from "next";
import { getTranslations } from "next-intl/server";
import type { ReactNode } from "react";
import { SeriesHub } from "./series-hub";
import { seriesCopy } from "@/lib/guide-series-copy";
import { GuideArticle, type GuideArticleLabels } from "@/components/guides/article";
import type { GuideCardLabels } from "@/components/guides/card";
import { TravelCrosslinks, type TravelCrosslinksLabels } from "@/components/guides/travel-crosslinks";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { citiesForCountry, countryKeys, destinationSeeds, type CatalogTranslator } from "@/lib/destinations";
import { guideAffiliateDestination } from "@/lib/guide-affiliate";
import {
  guideHeadings, guideHref, guideListHref, readingMinutes,
  type GuideArticleState, type GuideKind, type GuideSummary, type PublishedGuide,
} from "@/lib/guides";
import { getAdsenseSlot } from "@/lib/adsense.server";
import { getGuideArticle, getGuideList, getGuideSeries } from "@/lib/guides.server";
import { localeUrl, siteUrl } from "@/lib/seo";
import { breadcrumbs, type Crumb } from "@/lib/structured-data";

/**
 * The one article page, shared by `/guides/[kind]/[slug]` and `/life/[slug]`.
 *
 * Next forbids extra named exports from a `page.tsx`, so the metadata and the screen live
 * here and each route is a thin shell that fixes the kind. Everything section-specific --
 * the breadcrumb trail, the listing to return to, the crosslinks under a lifestyle article --
 * keys off `kind`, never off the URL, and the loader refuses a body whose kind differs from
 * the route's, so one article can only ever render at one address.
 */
export type GuideArticleRoute = { locale: Locale; kind: GuideKind; slug: string };

type Translate = (key: string, values?: Record<string, string | number>) => string;

/** How many related articles end a travel article; past three it stops being a pick. */
export const RELATED_ARTICLE_LIMIT = 3;

/** The listing an article belongs to: the heading readers return to, and its URL. */
function listingOf(kind: GuideKind, t: Translate): Crumb {
  const name = kind === "life"
    ? t("guides.lifeHubTitle")
    : kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle");
  return { name, path: guideListHref(kind) };
}

export async function guideArticleMetadata(
  { locale, kind, slug }: GuideArticleRoute, parent?: ResolvingMetadata,
): Promise<Metadata> {
  const [state, t] = await Promise.all([
    getGuideArticle(kind, slug, locale),
    getTranslations({ locale, namespace: "common" }),
  ]);
  const path = guideHref(kind, slug);
  if (state.status !== "published" || !state.document) {
    return {
      title: t("guides.unavailableTitle"),
      description: t(state.status === "unpublished" ? "guides.notTranslated" : "guides.unavailable"),
      robots: { index: false },
      alternates: { canonical: localeUrl(locale, path) },
    };
  }
  // Each locale publishes independently, so the root layout's all-five alternate set would
  // advertise translations that do not exist. Declare only the ones actually published.
  const languages = Object.fromEntries(state.published_locales.map((value) => [value, localeUrl(value, path)]));
  return {
    title: state.document.title,
    description: state.document.description,
    alternates: {
      canonical: localeUrl(locale, path),
      languages: {
        ...languages,
        ...(state.published_locales.includes("en") ? { "x-default": localeUrl("en", path) } : {}),
      },
    },
    ...(await socialCard(state.document, parent)),
  };
}

/**
 * The share card, only when the article has a hero to put on it.
 *
 * Next replaces a whole top-level metadata key rather than merging inside it, so naming
 * `openGraph` here would silently drop the layout's locale and alternate locales. They are
 * read back from the parent and restated; the image path is relative, and the layout's
 * `metadataBase` makes it absolute the same way it does for `/og.png`. Without a hero the
 * keys are left alone and the site card inherits.
 */
async function socialCard(
  document: PublishedGuide, parent?: ResolvingMetadata,
): Promise<Pick<Metadata, "openGraph" | "twitter">> {
  const hero = document.hero;
  if (!hero) return {};
  const inherited = parent ? (await parent).openGraph : null;
  return {
    openGraph: {
      ...(inherited?.siteName ? { siteName: inherited.siteName } : {}),
      ...(inherited?.locale ? { locale: inherited.locale } : {}),
      ...(inherited?.alternateLocale ? { alternateLocale: inherited.alternateLocale } : {}),
      type: "article",
      publishedTime: document.published_at,
      modifiedTime: document.modified_at ?? document.published_at,
      images: [{ url: hero.src, width: hero.width, height: hero.height, alt: hero.alt }],
    },
    twitter: { card: "summary_large_image", images: [hero.src] },
  };
}

/**
 * The destinations a lifestyle article hands the reader on to. A destination the editor
 * chose points at one country, so the reader gets that country's cities; without one, the
 * first city of every country, so the row spans the catalogue. The renderer caps the count.
 */
function crosslinkCities(destinationId: string | null, tc: CatalogTranslator): { id: string; name: string }[] {
  const catalogId = guideAffiliateDestination(destinationId);
  const country = destinationSeeds.find((seed) => seed.id === catalogId)?.country;
  const cities = country
    ? citiesForCountry(country, tc)
    : countryKeys.flatMap((key) => citiesForCountry(key, tc).slice(0, 1));
  return cities.map(({ id, name }) => ({ id, name }));
}

async function travelCrosslinks(
  locale: Locale, destinationId: string | null, labels: TravelCrosslinksLabels,
): Promise<ReactNode> {
  // The same `search.catalog` translator the home page hands to `citiesForCountry`, so a
  // city is named here exactly as it is on the destination rail.
  const [travel, tc] = await Promise.all([
    getGuideList(locale, { section: "travel" }, 3),
    getTranslations({ locale, namespace: "search.catalog" }),
  ]);
  return <TravelCrosslinks articles={travel.articles} cities={crosslinkCities(destinationId, tc)} labels={labels} />;
}

/**
 * What ends a travel article: up to three other travel articles about the same destination,
 * topped up from the article's first topic when the city has too few. Never the article
 * itself, never a lifestyle article, and nothing at all when there is nothing to show.
 */
async function relatedTravel(
  locale: Locale, state: GuideArticleState, labels: TravelCrosslinksLabels,
): Promise<ReactNode> {
  const own = `${state.kind}:${state.slug}`;
  const key = (article: GuideSummary) => `${article.kind}:${article.slug}`;
  const picks: GuideSummary[] = [];
  const take = (articles: GuideSummary[]) => {
    for (const article of articles) {
      if (key(article) !== own && !picks.some((pick) => key(pick) === key(article))) picks.push(article);
    }
  };
  if (state.destination_id) {
    take((await getGuideList(locale, { section: "travel", destination: state.destination_id }, RELATED_ARTICLE_LIMIT + 1)).articles);
  }
  if (picks.length < RELATED_ARTICLE_LIMIT && state.topics[0]) {
    take((await getGuideList(locale, { section: "travel", topic: state.topics[0].slug }, RELATED_ARTICLE_LIMIT + 1)).articles);
  }
  const shown = picks.slice(0, RELATED_ARTICLE_LIMIT);
  return shown.length ? <TravelCrosslinks articles={shown} cities={[]} labels={labels} /> : null;
}

export async function renderGuideArticle({ locale, kind, slug }: GuideArticleRoute) {
  const [state, t, nav, ts] = await Promise.all([
    getGuideArticle(kind, slug, locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
    getTranslations({ locale, namespace: "travelServices" }),
  ]);
  const listing = listingOf(kind, t);

  if (state.status !== "published" || !state.document) {
    const others = state.published_locales.filter((value) => value !== locale);
    return (
      <>
        <SiteHeader />
        <main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
          <h1 className="text-3xl font-bold">{t("guides.unavailableTitle")}</h1>
          <p role={state.status === "unavailable" ? "alert" : "status"} className="mt-5 leading-8 text-[var(--muted)]">
            {t(state.status === "unpublished" ? "guides.notTranslated" : "guides.unavailable")}
          </p>
          {others.length ? (
            <ul className="mt-5 flex flex-wrap gap-3">
              {others.map((value) => (
                <li key={value}>
                  <a className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/${value}${guideHref(kind, slug)}`} hrefLang={value}>
                    {localeLabels[value]}
                  </a>
                </li>
              ))}
            </ul>
          ) : null}
          <p className="mt-6">
            <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={listing.path}>
              {listing.name}
            </Link>
          </p>
        </main>
      </>
    );
  }

  // Read only past the guard above: an unavailable or untranslated article is a "no content"
  // screen, which the programme policies forbid carrying ads, so it never even asks.
  const adsense = await getAdsenseSlot();
  const kindLabels = { intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life") };
  // A card is labelled by its section and nothing else, so the kind labels are the whole set.
  const card: GuideCardLabels = kindLabels;
  const related = kind === "life"
    ? await travelCrosslinks(locale, state.destination_id, {
      relatedTravel: t("guides.relatedTravel"),
      relatedDestinations: t("guides.relatedDestinations"),
      card,
    })
    : await relatedTravel(locale, state, {
      relatedTravel: t("guides.related"),
      relatedDestinations: t("guides.relatedDestinations"),
      card,
    });
  // Travel articles sit under the guides hub and then their kind; a lifestyle article sits
  // directly under `/life`, which is both its hub and its only listing.
  const trail: Crumb[] = kind === "life"
    ? [{ name: nav("home"), path: "/" }, listing]
    : [{ name: nav("home"), path: "/" }, { name: t("guides.hubTitle"), path: "/guides" }, listing];
  const labels: GuideArticleLabels = {
    ...kindLabels,
    updated: t("guides.updated"),
    sources: t("guides.sources"), checkedOn: t("guides.checkedOn"),
    destination: t("guides.destination"), otherLanguages: t("guides.otherLanguages"),
    contents: state.series?.current ? seriesCopy(locale).contents : t("guides.contents"),
    adLabel: t("guides.adLabel"),
    disclosure: ts("disclosure"),
    partnerDisclosure: t("guides.partnerDisclosure"),
    partner: { badge: t("guides.partnerBadge"), newTab: ts("newTab") },
    blocks: {
      imageCredit: t("guides.imageCredit"),
      tip: t("guides.calloutTip"), warning: t("guides.calloutWarning"), info: t("guides.calloutInfo"),
    },
  };
  const hero = state.document.hero;
  const copy = seriesCopy(locale);
  labels.blocks.code = copy;
  const isHub = Boolean(state.series && !state.series.current && state.series.hub.slug === slug);
  const series = isHub && state.series ? await getGuideSeries(state.series.slug, locale) : null;
  if (state.series?.current) trail.push({ name: state.series.hub.title, path: guideHref(state.series.hub.kind, state.series.hub.slug) });
  const headings = guideHeadings(state.document.blocks);
  const seriesDirectory = isHub ? series ? <SeriesHub series={series} />
    : <div role="alert"><p>{copy.unavailable}</p><a href={`/${locale}${guideHref(kind, slug)}`} className="inline-flex min-h-11 items-center underline">{copy.retry}</a></div> : null;

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [...trail, { name: state.document.title, path: guideHref(kind, slug) }]),
          // Honest because this page renders the article it describes: a real headline, a
          // real body, a real publication date, and an image only when the article has one.
          {
            "@context": "https://schema.org",
            "@type": isHub ? "CollectionPage" : "Article",
            headline: state.document.title,
            description: state.document.description,
            inLanguage: locale,
            datePublished: state.document.published_at,
            dateModified: state.document.modified_at ?? state.document.published_at,
            ...(hero ? { image: `${siteUrl}${hero.src}` } : {}),
            mainEntityOfPage: localeUrl(locale, guideHref(kind, slug)),
            author: { "@type": "Organization", name: "Mokaair" },
            publisher: { "@type": "Organization", name: "Mokaair" },
            ...(series ? { mainEntity: { "@type": "ItemList", itemListElement: series.entries.map((entry, index) => ({
              "@type": "ListItem", position: index + 1, name: entry.title, url: localeUrl(locale, guideHref(entry.kind, entry.slug)),
            })) } } : {}),
          },
        ]}
      />
      <main className={`mx-auto px-5 py-10 md:py-14 ${state.series ? "max-w-6xl" : "max-w-3xl"}`}>
        {state.series ? <nav aria-label="Breadcrumb" className="mb-6 text-sm leading-7 text-[var(--muted)]"><ol className="flex flex-wrap gap-2">
          {trail.filter(crumb => crumb.path !== "/").map(crumb => <li key={crumb.path}><Link className="underline" href={crumb.path}>{crumb.name}</Link><span aria-hidden="true"> / </span></li>)}
          <li aria-current="page">{state.document.title}</li>
        </ol></nav> : null}
        <div className={state.series?.current ? "grid min-w-0 gap-8 lg:grid-cols-[minmax(0,1fr)_15rem]" : ""}>
        <div className="min-w-0">
        <GuideArticle
          state={{ ...state, document: state.document }}
          related={related}
          readingTime={t("guides.readingTime", { minutes: readingMinutes(state.document) })}
          labels={labels}
          adsense={adsense}
          seriesHub={seriesDirectory}
        />
        </div>
        {state.series?.current ? <aside className="hidden lg:block"><nav aria-label={labels.contents} className="sticky top-24 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
          <a href={`/${locale}${guideHref(state.series.hub.kind, state.series.hub.slug)}`} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{copy.back}</a>
          <h2 className="mt-2 font-semibold">{labels.contents}</h2><ol className="mt-3 space-y-2 text-sm leading-6">{headings.map(heading => <li key={heading.id}><a href={`#${heading.id}`} className="underline">{heading.text}</a></li>)}</ol>
        </nav></aside> : null}
        </div>
        <p className="mt-10">
          <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={listing.path}>
            {listing.name}
          </Link>
        </p>
      </main>
    </>
  );
}
