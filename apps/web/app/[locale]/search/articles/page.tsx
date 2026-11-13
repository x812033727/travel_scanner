import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { SearchForm } from "@/components/guides/search-form";
import { SearchResults } from "@/components/guides/search-results";
import { SiteHeader } from "@/components/site-header";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import {
  articleSearchHref,
  guideHref,
  guideSearchSorts,
  guideTopicHref,
  isGuideSearchSort,
  isGuideSection,
  type GuideSearchSort,
  type GuideSection,
  type GuideTopic,
} from "@/lib/guides";
import { getGuideSearch, getGuideTopics, getSeriesIndex, getTrendingGuides } from "@/lib/guides.server";

type Params = { locale: Locale };
type Search = { q?: string; section?: string; topic?: string; sort?: string; offset?: string };

const MAX_OFFSET = 200;
const SECTIONS: (GuideSection | null)[] = [null, "travel", "life"];
const TOPIC_SLUG_RE = /^[a-z0-9][a-z0-9-]{0,63}$/;

/** The query parameters, cleaned: an unknown section/topic/sort drops back to the default,
 *  and a garbled or out-of-range offset falls back to the first page. */
function route(search: Search) {
  const q = (search.q ?? "").trim().slice(0, 100);
  const section = isGuideSection(search.section) ? search.section : null;
  const rawTopic = (search.topic ?? "").trim().toLowerCase();
  const topic = TOPIC_SLUG_RE.test(rawTopic) ? rawTopic : null;
  const sort: GuideSearchSort = isGuideSearchSort(search.sort) ? search.sort : "relevance";
  const parsed = Number.parseInt(search.offset ?? "", 10);
  const offset = Number.isFinite(parsed) ? Math.min(Math.max(parsed, 0), MAX_OFFSET) : 0;
  return { q, section, topic, sort, offset };
}

/**
 * The results page. Always `noindex, follow` (docs/seo.md: a search result page is a
 * different ranking of the same articles, and the articles are what rank); `follow` so a
 * crawler that lands here from a shared link still reaches them.
 */
export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return {
    title: t("articleSearchTitle"),
    description: t("articleSearchDescription"),
    robots: { index: false, follow: true },
  };
}

export default async function ArticleSearchPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const { q, section, topic, sort, offset } = route(search);
  const [result, t] = await Promise.all([
    q
      ? getGuideSearch(locale, {
          q,
          section: section ?? undefined,
          ...(topic ? { topic } : {}),
          ...(sort !== "relevance" ? { sort } : {}),
          offset,
        })
      : null,
    getTranslations({ locale, namespace: "common" }),
  ]);
  const showBrowse = !result || (result.available && !result.invalid && result.total === 0 && !result.best_match);
  const [travelTopics, lifeTopics, series, trending] = showBrowse
    ? await Promise.all([
        getGuideTopics(locale, "travel"),
        getGuideTopics(locale, "life"),
        getSeriesIndex(locale),
        getTrendingGuides(locale, section ? { section } : {}, 6),
      ])
    : [[], [], [], { articles: [], next_cursor: null, available: false }];
  const browsable = (topics: GuideTopic[]) => topics.filter((item) => !item.parent && (item.count === undefined || item.count > 0));

  const cardLabels = { intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life") };
  const sectionLabel = (value: GuideSection | null) =>
    value === "travel" ? t("guides.searchSectionTravel") : value === "life" ? t("guides.searchSectionLife") : t("guides.searchSectionAll");
  const sortLabel = (value: GuideSearchSort) =>
    value === "latest" ? t("guides.searchSortLatest") : t("guides.searchSortRelevance");
  const pages = result ? Math.max(1, Math.ceil(Math.min(result.total, MAX_OFFSET + result.limit) / result.limit)) : 1;
  const page = result ? Math.floor(result.offset / result.limit) + 1 : 1;
  const previous = result && result.offset > 0 ? Math.max(0, result.offset - result.limit) : null;

  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <header className="rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-6 shadow-[var(--shadow-sm)] md:p-10">
          <h1 className="text-3xl font-extrabold tracking-tight md:text-5xl">{t("guides.searchTitle")}</h1>
          <p className="mt-3.5 max-w-2xl text-base leading-7 text-[var(--muted)] md:text-lg md:leading-8">{t("guides.searchLead")}</p>

          <SearchForm
            action={`/${locale}/search/articles`}
            q={q}
            section={section}
            topic={topic}
            sort={sort}
            labels={{ label: t("guides.searchLabel"), placeholder: t("guides.searchPlaceholder"), submit: t("guides.searchSubmit") }}
          />
        </header>

        <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
          <nav aria-label={t("guides.searchScope")} className="flex flex-wrap gap-2">
            {SECTIONS.map((value) => (
              <Link
                key={value ?? "all"}
                href={articleSearchHref(q, {
                  section: value,
                  topic: value === section || value === null ? topic : null,
                  sort,
                })}
                aria-current={value === section ? "page" : undefined}
                className={`app-filter-chip ${value === section ? "app-filter-chip-active" : ""}`}
              >
                {sectionLabel(value)}
              </Link>
            ))}
            {topic ? (
              <Link
                href={articleSearchHref(q, { section, sort })}
                className="app-filter-chip app-filter-chip-active"
              >
                #{topic} × {t("guides.searchTopicAll")}
              </Link>
            ) : null}
          </nav>

          {q ? (
            <nav aria-label={t("guides.sortLabel")} className="flex flex-wrap gap-2">
              {guideSearchSorts.map((value) => (
                <Link
                  key={value}
                  href={articleSearchHref(q, { section, topic, sort: value })}
                  aria-current={value === sort ? "page" : undefined}
                  className={`app-filter-chip ${value === sort ? "app-filter-chip-active" : ""}`}
                >
                  {sortLabel(value)}
                </Link>
              ))}
            </nav>
          ) : null}
        </div>

        {result && !result.available ? (
          <p role="alert" className="mt-6 rounded-2xl border border-[var(--line)] p-5 leading-7">{t("guides.searchUnavailable")}</p>
        ) : null}
        {result?.invalid ? (
          <p role="alert" className="mt-6 rounded-2xl border border-[var(--line)] p-5 leading-7">{t("guides.searchInvalid")}</p>
        ) : null}

        {result && result.available && !result.invalid ? (
          <section aria-live="polite" className="mt-8">
            {result.best_match ? (
              <div className="mb-6">
                <h2 className="text-sm font-bold uppercase tracking-wide text-[var(--muted)]">{t("guides.searchBestMatch")}</h2>
                <ul className="mt-3 grid gap-3 sm:grid-cols-2">
                  <GuideCard article={result.best_match} labels={cardLabels} />
                </ul>
              </div>
            ) : null}
            <h2 className="text-xl font-bold tracking-tight">
              {result.total || result.best_match
                ? t("guides.searchResults", { query: q })
                : t("guides.searchNoResults", { query: q })}
            </h2>
            {!result.total && !result.best_match ? (
              <p className="mt-2 leading-7 text-[var(--muted)]">{t("guides.searchTry")}</p>
            ) : null}
            <SearchResults hits={result.results} labels={cardLabels} />
            {result.total > result.limit ? (
              <nav aria-label={t("guides.searchPagination")} className="mt-8 flex flex-wrap items-center gap-4">
                {previous !== null ? (
                  <Link
                    className="inline-flex min-h-11 items-center text-[var(--teal)] underline"
                    href={articleSearchHref(q, { section, topic, sort, offset: previous })}
                  >
                    {t("guides.searchPrev")}
                  </Link>
                ) : null}
                <span className="text-sm text-[var(--muted)]">{t("guides.searchPageOf", { page, pages })}</span>
                {result.next_offset !== null ? (
                  <Link
                    className="inline-flex min-h-11 items-center text-[var(--teal)] underline"
                    href={articleSearchHref(q, { section, topic, sort, offset: result.next_offset })}
                  >
                    {t("guides.searchNext")}
                  </Link>
                ) : null}
              </nav>
            ) : null}
          </section>
        ) : null}

        {!result ? <p className="mt-8 leading-7 text-[var(--muted)]">{t("guides.searchHint")}</p> : null}

        {showBrowse && trending.articles.length ? (
          <section className="mt-10 border-t border-[var(--line)] pt-8" data-testid="search-trending-section">
            <h2 className="text-2xl font-bold tracking-tight">{t("guides.trendingHeading")}</h2>
            <ul className="mt-4 grid gap-4 sm:grid-cols-2">
              {trending.articles.map((article) => (
                <GuideCard key={`${article.kind}:${article.slug}`} article={article} labels={cardLabels} />
              ))}
            </ul>
          </section>
        ) : null}

        {showBrowse && (browsable(travelTopics).length || browsable(lifeTopics).length) ? (
          <section className="mt-12 border-t border-[var(--line)] pt-8">
            <h2 className="text-2xl font-bold tracking-tight">{t("guides.browseTopics")}</h2>
            {([["travel", travelTopics], ["life", lifeTopics]] as const).map(([value, topics]) =>
              browsable(topics).length ? (
                <div key={value} className="mt-4">
                  <h3 className="text-sm font-bold uppercase tracking-wide text-[var(--muted)]">{sectionLabel(value)}</h3>
                  <ul className="mt-2 flex flex-wrap gap-2">
                    {browsable(topics).map((item) => (
                      <li key={item.slug}>
                        <Link className="app-filter-chip" href={guideTopicHref(value, item.slug)}>
                          {item.label}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null,
            )}
          </section>
        ) : null}

        {showBrowse && series.length ? (
          <section className="mt-10">
            <h2 className="text-2xl font-bold tracking-tight">{t("guides.searchBrowseSeries")}</h2>
            <ul className="mt-4 grid gap-3 sm:grid-cols-2">
              {series.map((item) => (
                <li key={item.slug}>
                  <Link
                    className="flex min-h-11 items-center rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 font-semibold text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/50 hover:text-[var(--teal-dark)]"
                    href={guideHref(item.hub.kind, item.hub.slug)}
                  >
                    {item.hub.title}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        ) : null}
      </main>
    </>
  );
}
