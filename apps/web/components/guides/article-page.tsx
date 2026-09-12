import type { Metadata, ResolvingMetadata } from "next";
import { getTranslations } from "next-intl/server";
import type { ReactNode } from "react";
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
  guideHref, guideListHref, readingMinutes,
  type GuideArticleState, type GuideKind, type GuideSummary, type PublishedGuide,
} from "@/lib/guides";
import { getGuideArticle, getGuideList } from "@/lib/guides.server";
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

  const kindLabels = { intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life") };
  const card: GuideCardLabels = {
    ...kindLabels, expired: t("guides.expired"),
    validUntil: t("guides.validUntil"), published: t("guides.published"),
  };
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
    published: t("guides.published"), updated: t("guides.updated"),
    expiredNotice: t("guides.expiredNotice"), validUntil: t("guides.validUntil"),
    sources: t("guides.sources"), checkedOn: t("guides.checkedOn"),
    destination: t("guides.destination"), otherLanguages: t("guides.otherLanguages"),
    contents: t("guides.contents"),
    disclosure: ts("disclosure"),
    blocks: {
      imageCredit: t("guides.imageCredit"),
      tip: t("guides.calloutTip"), warning: t("guides.calloutWarning"), info: t("guides.calloutInfo"),
    },
  };
  const hero = state.document.hero;

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
            "@type": "Article",
            headline: state.document.title,
            description: state.document.description,
            inLanguage: locale,
            datePublished: state.document.published_at,
            dateModified: state.document.modified_at ?? state.document.published_at,
            ...(hero ? { image: `${siteUrl}${hero.src}` } : {}),
            mainEntityOfPage: localeUrl(locale, guideHref(kind, slug)),
            author: { "@type": "Organization", name: "Mokaair" },
            publisher: { "@type": "Organization", name: "Mokaair" },
          },
        ]}
      />
      <main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
        <GuideArticle
          state={{ ...state, document: state.document }}
          related={related}
          readingTime={t("guides.readingTime", { minutes: readingMinutes(state.document) })}
          labels={labels}
        />
        <p className="mt-10">
          <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={listing.path}>
            {listing.name}
          </Link>
        </p>
      </main>
    </>
  );
}
