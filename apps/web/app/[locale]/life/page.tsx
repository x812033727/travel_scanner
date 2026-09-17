import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { HubHero } from "@/components/guides/hub-hero";
import { NewsList } from "@/components/guides/news-list";
import { TopicTiles } from "@/components/guides/topic-tiles";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { NEWS_TOPICS, guideHref, guideListHref, guideTopicHref, newsOrder } from "@/lib/guides";
import { getGuideList, getGuideTopics, getSeriesIndex, hubIsEmpty } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";
import { getGeminiHubReference, getVisibleGeminiSeries, filterGeminiArticleLinks } from "@/lib/gemini-series.server";
import { breadcrumbs, itemList } from "@/lib/structured-data";

type Params = { locale: Locale };
type Search = { topic?: string; cursor?: string };

/** One listing read, shared by the metadata and the body through React's per-request cache:
 *  same arguments, one call to the API. The editor's order (featured, then `display_order`,
 *  then newest): the overview every other article links back to stays on page one however
 *  many batches follow it. */
const listFor = (locale: Locale, search: Search) =>
  getGuideList(locale, { kind: "life", topic: search.topic, cursor: search.cursor, sort: "curated" }, 24);

/** The section opens with its news: the latest twenty stories of the news topic by the day
 *  the news happened (`sort=news`), one line each, with the topic hub as "see all". Not by
 *  publication time -- a batch import publishes a week of stories in the same minute -- and
 *  only dated stories: the topic's evergreen pieces (a sources list, a yearly timeline) are
 *  not news. Only on the plain first page: a `?topic=` or `?cursor=` view is already somewhere
 *  specific, and the news topics' own hubs list all of it.
 *
 *  There are three news topics and the API's `topic` takes one slug, so this reads each of
 *  them and merges on `newsOrder`, the API's own news keyset. Each read asks for the full
 *  limit because one topic may supply every row: crypto and tech start at nothing, and a busy
 *  week in one vertical should not push the others' stories out by an accident of paging. */
const NEWS_LIMIT = 20;

/**
 * The lifestyle section: the same article system as `/guides`, with its own hub, its own
 * topic vocabulary and no kind segment, because `life` is the only kind that lists here.
 */
export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const t = await getTranslations({ locale, namespace: "metadata" });
  const filtered = Boolean(search.topic || search.cursor);
  // Only the unfiltered view asks: a filtered one is `noindex` already, and the extra read
  // would be a second API call per crawl of a URL whose answer cannot change.
  const empty = !filtered && hubIsEmpty(await listFor(locale, search));
  return {
    title: t("lifeTitle"),
    description: t("lifeDescription"),
    // A filtered view is the same collection in a different order. Let the unfiltered
    // section carry the ranking rather than competing with dozens of near-duplicates.
    // An empty section is out for a different reason: the lifestyle section has published
    // nothing in this language yet, so the page is a heading over one sentence. Both stay
    // `follow`, and the first article published here puts it back in the index.
    ...(filtered || empty ? { robots: { index: false, follow: true } } : {}),
    // The topic hub is the page that ranks for a topic; this older `?topic=` URL names it.
    ...(search.topic ? { alternates: { canonical: localeUrl(locale, guideTopicHref("life", search.topic)) } } : {}),
  };
}

/**
 * The lifestyle hub, the same shape as the travel one: what the section is and a search
 * box scoped to it, the topics as tiles, then the listing in the editor's order.
 *
 * The series and tutorial hubs used to sit between the tiles and the listing. They moved
 * to the topic hubs (`renderTopicHub`), where the reader has already said which subject
 * they want -- every series names its topic, so this page was showing all of them to
 * everyone. Neither the tiles nor the header carries a figure any more, for the reason in
 * `HubHero`: the section grows weekly and the number was wrong between deploys.
 */
export default async function LifeHubPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const showNews = !search.topic && !search.cursor;
  const [rawList, rawNews, topics, registry, t, nav] = await Promise.all([
    listFor(locale, search),
    showNews
      ? Promise.all(NEWS_TOPICS.map((topic) => getGuideList(locale, { kind: "life", topic, sort: "news" }, NEWS_LIMIT)))
      : Promise.resolve(null),
    getGuideTopics(locale, "life"),
    getSeriesIndex(locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const listing = guideListHref("life", search.topic);
  // A `?cursor=` the API refused (minted under the old order, or hand-edited) must not
  // render as a 200 saying nothing is published; the first page is the honest answer.
  if (search.cursor && !rawList.available) redirect(listing);

  // The Gemini series is projected by the web from its own catalogue, and its lessons show
  // in the listing only while the hub is published here -- which is exactly when the
  // registry lists it, so the registry row is the publication signal.
  const geminiReference = getGeminiHubReference(locale);
  const geminiSeries = getVisibleGeminiSeries({
    locale, hubPublished: Boolean(geminiReference) && registry.some((item) => item.source === "web-gemini"),
  });
  const list = { ...rawList, articles: geminiReference ? filterGeminiArticleLinks(rawList.articles, geminiSeries) : rawList.articles };
  // One row per story even if two topics carry the same article: a pack may hold both
  // ``crypto`` and ``ai-news``, and it appears in each topic's read.
  const newsBySlug = new Map(
    (rawNews ?? []).flatMap((result) =>
      (geminiReference ? filterGeminiArticleLinks(result.articles, geminiSeries) : result.articles)
        .filter((article) => Boolean(article.news_date))
        .map((article) => [article.slug, article] as const),
    ),
  );
  const news = [...newsBySlug.values()].sort(newsOrder).slice(0, NEWS_LIMIT);
  // "See all" names the topics that actually have something, in ``NEWS_TOPICS`` order, with
  // each topic's own label from the vocabulary this page already reads -- no new strings, and
  // while only one vertical publishes it renders as the single link it was before.
  const newsHubs = NEWS_TOPICS.flatMap((slug) => {
    const topic = topics.find((item) => item.slug === slug);
    return topic && news.some((article) => article.topics?.some((option) => option.slug === slug))
      ? [{ slug, label: topic.label }]
      : [];
  });

  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life"),
  };
  const next = `${listing}${listing.includes("?") ? "&" : "?"}cursor=`;

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [
            { name: nav("home"), path: "/" },
            { name: t("guides.lifeHubTitle"), path: "/life" },
          ]),
          itemList(locale, list.articles.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <HubHero
          title={t("guides.lifeHubTitle")}
          intro={t("guides.lifeHubIntro")}
          section="life"
          action={`/${locale}/search/articles`}
          labels={{ label: t("guides.searchLabel"), placeholder: t("guides.searchPlaceholder"), submit: t("guides.searchSubmit") }}
        />

        {news.length ? (
          <section className="mt-10" aria-labelledby="life-news-heading" data-testid="life-news">
            <div className="flex flex-wrap items-baseline justify-between gap-3">
              <h2 id="life-news-heading" className="text-2xl font-bold tracking-tight">{t("guides.latestNews")}</h2>
              <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1">
                {newsHubs.map((hub) => (
                  <Link
                    key={hub.slug}
                    className="inline-flex min-h-11 items-center text-[var(--teal)] underline"
                    href={guideTopicHref("life", hub.slug)}
                  >
                    {newsHubs.length === 1 ? t("guides.seeAll") : hub.label}
                  </Link>
                ))}
              </div>
            </div>
            <NewsList articles={news} />
          </section>
        ) : null}

        <TopicTiles
          section="life"
          topics={topics}
          active={search.topic ?? null}
          labels={{ heading: t("guides.browseTopics"), more: t("guides.subtopicsMore") }}
        />

        <section className="mt-10" aria-labelledby="life-listing-heading">
          <h2 id="life-listing-heading" className="text-2xl font-bold tracking-tight">{t("guides.allArticles")}</h2>
          {list.articles.length ? (
            <ul className="mt-4 grid gap-3 sm:grid-cols-2">
              {list.articles.map((article) => (
                <GuideCard key={article.slug} article={article} labels={cardLabels} />
              ))}
            </ul>
          ) : (
            <p className="mt-4 leading-7 text-[var(--muted)]">{t("guides.empty")}</p>
          )}

          {list.next_cursor ? (
            <p className="mt-8">
              <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`${next}${encodeURIComponent(list.next_cursor)}`}>
                {t("guides.more")}
              </Link>
            </p>
          ) : null}
        </section>
      </main>
    </>
  );
}
