import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { ReactNode } from "react";
import { GuideArticle } from "@/components/guides/article";
import { TravelCrosslinks, type TravelCrosslinksLabels } from "@/components/guides/travel-crosslinks";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { citiesForCountry, countryKeys, destinationSeeds, type CatalogTranslator } from "@/lib/destinations";
import { guideAffiliateDestination } from "@/lib/guide-affiliate";
import { guideHref, guideListHref, type GuideKind } from "@/lib/guides";
import { getGuideArticle, getGuideList } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";
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

type Translate = (key: string) => string;

/** The listing an article belongs to: the heading readers return to, and its URL. */
function listingOf(kind: GuideKind, t: Translate): Crumb {
  const name = kind === "life"
    ? t("guides.lifeHubTitle")
    : kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle");
  return { name, path: guideListHref(kind) };
}

export async function guideArticleMetadata({ locale, kind, slug }: GuideArticleRoute): Promise<Metadata> {
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

export async function renderGuideArticle({ locale, kind, slug }: GuideArticleRoute) {
  const [state, t, nav] = await Promise.all([
    getGuideArticle(kind, slug, locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
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
  const related = kind === "life"
    ? await travelCrosslinks(locale, state.destination_id, {
      relatedTravel: t("guides.relatedTravel"),
      relatedDestinations: t("guides.relatedDestinations"),
      card: {
        ...kindLabels, expired: t("guides.expired"),
        validUntil: t("guides.validUntil"), published: t("guides.published"),
      },
    })
    : null;
  // Travel articles sit under the guides hub and then their kind; a lifestyle article sits
  // directly under `/life`, which is both its hub and its only listing.
  const trail: Crumb[] = kind === "life"
    ? [{ name: nav("home"), path: "/" }, listing]
    : [{ name: nav("home"), path: "/" }, { name: t("guides.hubTitle"), path: "/guides" }, listing];

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [...trail, { name: state.document.title, path: guideHref(kind, slug) }]),
          // Honest because this page renders the article it describes: a real headline, a
          // real body and a real publication date. No image is claimed; there is none.
          {
            "@context": "https://schema.org",
            "@type": "Article",
            headline: state.document.title,
            description: state.document.description,
            inLanguage: locale,
            datePublished: state.document.published_at,
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
          labels={{
            ...kindLabels,
            published: t("guides.published"), updated: t("guides.updated"),
            expiredNotice: t("guides.expiredNotice"), validUntil: t("guides.validUntil"),
            sources: t("guides.sources"), checkedOn: t("guides.checkedOn"),
            destination: t("guides.destination"), otherLanguages: t("guides.otherLanguages"),
          }}
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
