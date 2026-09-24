import type { Metadata, ResolvingMetadata } from "next";
import { permanentRedirect } from "next/navigation";
import { getTranslations } from "next-intl/server";
import type { ReactNode } from "react";
import { SeriesHub } from "./series-hub";
import { LearningHub } from "@/components/codex-learning/hub";
import { HUB_SLUG, learningEntries } from "@/lib/codex-learning";
import { depthCopy } from "@/lib/codex-learning/units";
import { seriesCopy } from "@/lib/guide-series-copy";
import { getGeminiHubReference, getVisibleGeminiSeries, isGeminiSeriesPage, projectGeminiArticle } from "@/lib/gemini-series.server";
import { GuideArticle, type GuideArticleLabels } from "@/components/guides/article";
import type { GuideCardLabels } from "@/components/guides/card";
import { Breadcrumb } from "@/components/guides/breadcrumb";
import { Backlinks, RelatedGrid } from "@/components/guides/related-grid";
import { TravelCrosslinks, type TravelCrosslinksLabels } from "@/components/guides/travel-crosslinks";
import { SiteHeader } from "@/components/site-header";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { citiesForCountry, countryKeys, destinationSeeds, type CatalogTranslator } from "@/lib/destinations";
import { contentBlockLink } from "@/lib/content-blocks";
import { guideAffiliateDestination } from "@/lib/guide-affiliate";
import { splitArticleExtras, guideTopicHref, guideSection,
  guideHeadings, guideHref, guideListHref, readingMinutes,
  type GuideArticleState, type GuideKind, type GuideSummary, type PublishedGuide,
} from "@/lib/guides";
import { getAdsenseSlot } from "@/lib/adsense.server";
import { getGuideTopics, getGuideArticle, getGuideList, getGuideSeries } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";
import { faqPage, definedTerm, breadcrumbs, guideArticle, type Crumb } from "@/lib/structured-data";

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

/**
 * A slug is lowercase, and one article has one URL. An inbound link that capitalised it
 * (`/guides/howto/Narita-To-Tokyo`) is sent to the canonical address for good rather than
 * answered with the "temporarily unavailable" notice the loader's identity guard would
 * otherwise produce: the article is live, only the address was wrong. `guideHref` builds
 * the locale-less path; the `Link`-less redirect needs the locale on it.
 */
function canonicalSlugOrRedirect({ locale, kind, slug }: GuideArticleRoute): void {
  const canonical = slug.toLowerCase();
  if (canonical !== slug) permanentRedirect(`/${locale}${guideHref(kind, canonical)}`);
}

export async function guideArticleMetadata(
  { locale, kind, slug }: GuideArticleRoute, parent?: ResolvingMetadata,
): Promise<Metadata> {
  canonicalSlugOrRedirect({ locale, kind, slug });
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
  canonicalSlugOrRedirect({ locale, kind, slug });
  const [rawState, t, nav, ts] = await Promise.all([
    getGuideArticle(kind, slug, locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
    getTranslations({ locale, namespace: "travelServices" }),
  ]);
  const hubReference = getGeminiHubReference(locale);
  const belongsToGemini = rawState.status === "published" && Boolean(rawState.document) && isGeminiSeriesPage(slug, locale, kind);
  const geminiHub = belongsToGemini && hubReference ? (slug === hubReference.slug ? rawState : await getGuideArticle("life", hubReference.slug, locale)) : null;
  const geminiSeries = belongsToGemini ? getVisibleGeminiSeries({ locale, hubPublished: geminiHub?.status === "published" && Boolean(geminiHub.document) }) : null;
  const state = projectGeminiArticle(rawState, geminiSeries);
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
  // What to read next comes from the API's ranked list when it has one (the editor's picks,
  // then the nearest neighbours); a lesson's own related lessons are already listed by the
  // series navigation just above and are not repeated. A lifestyle article keeps the travel
  // handover after it; a travel article's list replaces the same-city cards it used to end
  // with, which an API without the list still supplies.
  const seriesRelated = (state.series?.related ?? []).map((item) => item.slug);
  const grid = state.related?.length
    ? <RelatedGrid heading={t("guides.relatedSameTopic")} items={state.related} kindLabels={kindLabels} exclude={seriesRelated} />
    : null;
  const cited = state.backlinks?.length ? <Backlinks heading={t("guides.citedBy")} items={state.backlinks} /> : null;
  const handover = kind === "life"
    ? await travelCrosslinks(locale, state.destination_id, {
      relatedTravel: t("guides.relatedTravel"),
      relatedDestinations: t("guides.relatedDestinations"),
      card,
    })
    : grid ? null : await relatedTravel(locale, state, {
      relatedTravel: t("guides.related"),
      relatedDestinations: t("guides.relatedDestinations"),
      card,
    });
  const related = grid || cited || handover ? <>{grid}{cited}{handover}</> : null;
  // Travel articles sit under the guides hub and then their kind; a lifestyle article sits
  // directly under `/life`, which is both its hub and its only listing. Then the article's
  // first topic: its parent hub and its own hub for a sub-topic, its own hub otherwise. The
  // vocabulary read is what names a parent (the state carries only the parent's slug); when
  // it is unavailable the topic still gets its crumb, its parent does not.
  const trail: Crumb[] = kind === "life"
    ? [{ name: nav("home"), path: "/" }, listing]
    : [{ name: nav("home"), path: "/" }, { name: t("guides.hubTitle"), path: "/guides" }, listing];
  const section = guideSection(kind);
  const topic = state.topics[0];
  if (topic) {
    const vocabulary = await getGuideTopics(locale, section);
    const parentSlug = topic.parent ?? vocabulary.find((item) => item.slug === topic.slug)?.parent ?? null;
    const parent = parentSlug ? vocabulary.find((item) => item.slug === parentSlug) ?? null : null;
    if (parent) trail.push({ name: parent.label, path: guideTopicHref(section, parent.slug) });
    trail.push({ name: topic.label, path: guideTopicHref(section, topic.slug) });
  }
  const extras = splitArticleExtras(state.document.blocks);
  const labels: GuideArticleLabels = {
    ...kindLabels,
    updated: t("guides.updated"),
    sources: t("guides.sources"), checkedOn: t("guides.checkedOn"),
    destination: t("guides.destination"),
    contents: state.series?.current ? seriesCopy(locale).contents : t("guides.contents"),
    adLabel: t("guides.adLabel"),
    disclosure: ts("disclosure"),
    partnerDisclosure: t("guides.partnerDisclosure"),
    partner: { badge: t("guides.partnerBadge"), newTab: ts("newTab") },
    blocks: {
      imageCredit: t("guides.imageCredit"), imageDescription: t("guides.imageDescriptionToggle"),
      tip: t("guides.calloutTip"), warning: t("guides.calloutWarning"), info: t("guides.calloutInfo"),
    },
    term: { card: t("guides.termCard"), readMore: t("guides.termReadMore") },
    summary: t("guides.summary"),
    faq: t("guides.faq"),
    support: { text: t("guides.supportText"), action: t("guides.supportAction"), newTab: ts("newTab") },
  };
  const hero = state.document.hero;
  const copy = seriesCopy(locale);
  labels.blocks.code = copy;
  const isCodexHub = kind === "life" && slug === HUB_SLUG;
  const isHub = isCodexHub || Boolean(state.series && !state.series.current && state.series.hub.slug === slug);
  const series = isHub ? await getGuideSeries(isCodexHub ? "codex" : state.series!.slug, locale) : null;
  if (state.series?.current) trail.push({ name: state.series.hub.title, path: guideHref(state.series.hub.kind, state.series.hub.slug) });
  const headings = guideHeadings(state.document.blocks);
  const seriesDirectory = isCodexHub
    ? <LearningHub locale={locale} entries={learningEntries(locale, series?.entries ?? [])} available={Boolean(series)} />
    : isHub ? series ? <SeriesHub series={series} />
    : <div role="alert"><p>{copy.unavailable}</p><a href={`/${locale}${guideHref(kind, slug)}`} className="inline-flex min-h-11 items-center underline">{copy.retry}</a></div> : null;

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [...trail, { name: state.document.title, path: guideHref(kind, slug) }]),
          // The editor's questions, and the glossary entry, as their own graphs: each is
          // present exactly when the page shows the thing it describes.
          extras.faq ? faqPage(locale, guideHref(kind, slug), extras.faq.items) : null,
          state.term_set
            ? definedTerm(locale, {
              path: guideHref(kind, slug),
              name: state.document.title,
              description: state.document.description,
              aliases: state.aliases,
              set: { name: state.term_set.title, path: guideHref(state.term_set.kind, state.term_set.slug) },
            })
            : null,
          // Honest because this page renders every part of it: the headline, the body, the
          // publication date, the topic chips, the reading time, and the source list with the
          // date each entry was checked. `guideArticle` records what is deliberately left out.
          guideArticle(locale, {
            path: guideHref(kind, slug),
            title: state.document.title,
            description: state.document.description,
            publishedAt: state.document.published_at,
            modifiedAt: state.document.modified_at,
            hero,
            section: listingOf(kind, t).name,
            keywords: state.topics.map((topic) => topic.label),
            // Only an id with a destination page behind it. Every id in the corpus has one
            // today, but the graph may not be the thing that finds out when one stops.
            destination: state.destination_id && state.destination_label
              && (PUBLIC_DESTINATIONS as readonly string[]).includes(state.destination_id)
              ? { name: state.destination_label, path: `/destinations/${state.destination_id}` }
              : null,
            // Through the same sanitizer the source list below is drawn with, so the graph can
            // never name a source the page itself refused to link.
            references: state.document.sources.flatMap((source) => {
              const href = contentBlockLink(source.url);
              return href ? [{ title: source.title, url: href, checkedOn: source.checked_on }] : [];
            }),
            minutes: readingMinutes(state.document),
            abstract: extras.summary?.items ?? null,
            collection: isHub,
            entries: series?.entries.map((item) => ({ name: item.title, path: guideHref(item.kind, item.slug) })),
          }),
        ]}
      />
      <main className={`mx-auto px-5 py-10 md:py-14 ${state.series ? "max-w-6xl" : "max-w-3xl"}`}>
        <Breadcrumb trail={trail} current={state.document.title} label={t("guides.breadcrumb")} />
        <div className={state.series?.current ? "grid min-w-0 gap-8 lg:grid-cols-[minmax(0,1fr)_15rem]" : ""}>
        <div className="min-w-0">
        <GuideArticle
          geminiSeries={geminiSeries}
          state={{ ...state, document: state.document }}
          related={related}
          readingTime={t("guides.readingTime", { minutes: state.series?.current?.minutes ?? readingMinutes(state.document) })
            + (state.series?.current?.operation_minutes ? ` · ${depthCopy(locale).practice} ${state.series.current.operation_minutes} ${copy.minutes}` : "")}
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
