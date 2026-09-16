import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { ListingEmpty, ListingToolbar } from "@/components/guides/listing-toolbar";
import { SeriesRow } from "@/components/guides/series-row";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import { locales, type Locale } from "@/i18n/routing";
import {
  guideHref, guideTopicHref, isGuideListSort, sectionHubHref, topicLocales, type GuideListSort, type GuideSection, type GuideTopic,
} from "@/lib/guides";
import type { SeriesSummary } from "@/lib/guide-series";
import { getGuideList, getGuideTopicList, getSeriesIndex, hubIsEmpty } from "@/lib/guides.server";
import { HREFLANG_DEFAULT, localeUrl } from "@/lib/seo";
import { breadcrumbs, itemList } from "@/lib/structured-data";

export type TopicHubRoute = { locale: Locale; section: GuideSection; topic: string; cursor?: string; sort?: string };

const PAGE_SIZE = 24;

/** Newest first unless the reader asked for the editor's order: a topic mixes dated
 *  notices with evergreen guides, and the newest is the safer default across both. */
const sortOf = (value?: string): GuideListSort => (isGuideListSort(value) ? value : "latest");

/** One listing read and one vocabulary read, shared by the metadata and the body through
 *  React's per-request cache: same arguments, one call each to the API. */
function reads({ locale, section, topic, cursor, sort }: TopicHubRoute) {
  return Promise.all([
    getGuideTopicList(locale, section),
    getGuideList(locale, { section, topic, cursor, sort: sortOf(sort) }, PAGE_SIZE),
  ]);
}

/**
 * The series and tutorial hubs this topic owns. A registry row names one topic, always a
 * sub-topic, so a parent hub gathers what its children hold -- otherwise the family page a
 * reader lands on first would be the one page that never mentions them.
 *
 * A row whose topic is null, or names a topic this language's vocabulary does not carry,
 * appears nowhere. `test_the_registry_names_hubs_that_exist_and_series_the_api_can_serve`
 * holds every row to a topic in the lifestyle vocabulary, so that is a broken registry
 * rather than a case to render around.
 */
function seriesFor(series: readonly SeriesSummary[], topics: readonly GuideTopic[], route: TopicHubRoute) {
  const owns = (slug: string | null) =>
    slug === route.topic || topics.find((topic) => topic.slug === slug)?.parent === route.topic;
  return series.filter((item) => item.section === route.section && owns(item.topic));
}

/**
 * Resolves the route to a topic, or answers 404. An unknown slug is not a page; an
 * unreachable vocabulary is, and says so with `noindex` rather than claiming the topic is
 * gone -- the hub must survive an API outage the way the section hubs do.
 */
function resolve(topics: GuideTopic[], available: boolean, slug: string): GuideTopic | null {
  const found = topics.find((topic) => topic.slug === slug) ?? null;
  if (available && !found) notFound();
  return found;
}

export async function topicHubMetadata(route: TopicHubRoute): Promise<Metadata> {
  const [vocabulary, list] = await reads(route);
  const topic = resolve(vocabulary.topics, vocabulary.available, route.topic);
  const t = await getTranslations({ locale: route.locale, namespace: "metadata" });
  const label = topic?.label ?? route.topic;
  const path = guideTopicHref(route.section, route.topic);
  // Published-in-this-language decides the index, from the vocabulary's own counts; only when
  // an older API sends none does the listing's emptiness decide, and only a complete answer
  // may say empty (`hubIsEmpty`). A `?cursor=` page is the same collection further down,
  // and a `?sort=` page the same collection reordered.
  const empty = topic?.count !== undefined ? topic.count === 0 : hubIsEmpty(list);
  const noindex = !topic || empty || Boolean(route.cursor) || Boolean(route.sort);
  const published = topic ? topicLocales(topic, locales) : [];
  return {
    title: t("topicHubTitle", { topic: label }),
    description: topic?.description || t("topicHubDescription", { topic: label }),
    alternates: {
      canonical: localeUrl(route.locale, path),
      // Only the languages with something under the topic, for the reason an article page
      // lists only its published translations: hreflang pointing at a `noindex` page is a
      // contradiction. `x-default` belongs to English only while English has the topic.
      ...(published.length
        ? {
            languages: {
              ...Object.fromEntries(published.map((locale) => [locale, localeUrl(locale, path)])),
              ...(published.includes(HREFLANG_DEFAULT) ? { "x-default": localeUrl(HREFLANG_DEFAULT, path) } : {}),
            },
          }
        : {}),
    },
    ...(noindex ? { robots: { index: false, follow: true } } : {}),
  };
}

export async function renderTopicHub(route: TopicHubRoute) {
  const { locale, section } = route;
  const [[vocabulary, list], registry, t, nav] = await Promise.all([
    reads(route),
    getSeriesIndex(locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);
  const topic = resolve(vocabulary.topics, vocabulary.available, route.topic);
  const parent = topic?.parent ? vocabulary.topics.find((item) => item.slug === topic.parent) ?? null : null;
  const label = topic?.label ?? route.topic;
  const sectionTitle = section === "life" ? t("guides.lifeHubTitle") : t("guides.hubTitle");
  const sectionLead = section === "life" ? t("guides.lifeHubIntro") : t("guides.hubIntro");
  const lead = topic?.description || parent?.description || sectionLead;
  const path = guideTopicHref(section, route.topic);
  const cardLabels = { intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life") };
  const toolbarLabels = {
    allTopics: t("guides.allTopics"), topicsLabel: t("guides.topicsLabel"), subtopics: t("guides.subtopics"),
    moreChips: t("guides.moreChips"), fewerChips: t("guides.fewerChips"),
    sortLabel: t("guides.sortLabel"), sortCurated: t("guides.sortCurated"), sortLatest: t("guides.sortLatest"),
  };
  const searchLabels = { label: t("guides.searchLabel"), placeholder: t("guides.searchPlaceholder"), submit: t("guides.searchSubmit") };
  const sort = sortOf(route.sort);
  // The hub's own address is its default order; the other order rides on `?sort=`.
  const view = (value: GuideListSort) => (value === "latest" ? path : `${path}?sort=${value}`);
  const next = `${view(sort)}${sort === "latest" ? "?" : "&"}cursor=`;
  const trail = [
    { name: nav("home"), path: "/" },
    { name: sectionTitle, path: sectionHubHref(section) },
    ...(parent ? [{ name: parent.label, path: guideTopicHref(section, parent.slug) }] : []),
    { name: label, path },
  ];

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, trail),
          itemList(locale, list.articles.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <nav aria-label={t("guides.breadcrumb")} className="text-[length:var(--text-meta)] text-[var(--muted)]">
          <ol className="flex flex-wrap items-center gap-1">
            {trail.slice(0, -1).map((crumb) => (
              <li key={crumb.path} className="flex items-center gap-1">
                <Link className="inline-flex min-h-11 items-center underline underline-offset-4" href={crumb.path}>{crumb.name}</Link>
                <span aria-hidden>›</span>
              </li>
            ))}
            <li aria-current="page" className="inline-flex min-h-11 items-center">{label}</li>
          </ol>
        </nav>
        <h1 className="text-4xl font-bold tracking-tight">{label}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{lead}</p>

        {!vocabulary.available ? (
          <p className="mt-6 leading-7 text-[var(--muted)]">{t("guides.topicUnavailable")}</p>
        ) : null}

        <SeriesRow
          series={seriesFor(registry, vocabulary.topics, route)}
          labels={{ heading: t("guides.seriesRow"), lead: t("guides.seriesLead") }}
        />

        <ListingToolbar
          section={section}
          topics={vocabulary.topics}
          active={route.topic}
          allHref={sectionHubHref(section)}
          sort={{ current: sort, hrefs: { curated: view("curated"), latest: view("latest") } }}
          labels={toolbarLabels}
        />

        {list.articles.length ? (
          <ul className="mt-6 grid gap-3 sm:grid-cols-2">
            {list.articles.map((article) => (
              <GuideCard key={`${article.kind}:${article.slug}`} article={article} labels={cardLabels} />
            ))}
          </ul>
        ) : (
          <ListingEmpty
            section={section}
            action={`/${locale}/search/articles`}
            labels={{ ...searchLabels, empty: t("guides.empty"), hint: t("guides.emptyHint") }}
          />
        )}

        {list.next_cursor ? (
          <p className="mt-8">
            <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`${next}${encodeURIComponent(list.next_cursor)}`}>
              {t("guides.more")}
            </Link>
          </p>
        ) : null}
      </main>
    </>
  );
}
