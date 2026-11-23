import { ArrowRight, Compass, Film, Rss, Search, Soup } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { HomePortalTabs, type HomeGuideBlock } from "@/components/home-portal-tabs";
import { Link } from "@/i18n/navigation";
import { normalizeLocale, type Locale } from "@/i18n/routing";
import { NEWS_TOPICS, guideTopicHref, newsOrder, type GuideSummary } from "@/lib/guides";
import type { SeriesSummary } from "@/lib/guide-series";
import * as guidesServer from "@/lib/guides.server";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { navGroups, navItemLabelKey } from "@/lib/nav-links";

export type { HomeGuideBlock };

const OVERVIEW_PER_BLOCK = 4;
const FETCH_PER_BLOCK = 8;
const NEWS_DESK_LIMIT = 11;
const TRENDING_FETCH_LIMIT = 18;
const TRENDING_LIMIT = 6;
const SERIES_LIMIT = 6;

export type HomePortalData = {
  blocks: HomeGuideBlock[];
  news: GuideSummary[];
  newsTopics: string[];
  trending: GuideSummary[];
  software: GuideSummary[];
  series: SeriesSummary[];
};

const articleKey = (article: Pick<GuideSummary, "kind" | "slug">) => `${article.kind}:${article.slug}`;

async function safeTrendingGuides(locale: Locale): Promise<GuideSummary[]> {
  try {
    if (typeof guidesServer.getTrendingGuides !== "function") return [];
    const result = await guidesServer.getTrendingGuides(locale, {}, TRENDING_FETCH_LIMIT);
    return Array.isArray(result?.articles) ? result.articles : [];
  } catch {
    return [];
  }
}

async function safeSeriesIndex(locale: Locale): Promise<SeriesSummary[]> {
  try {
    if (typeof guidesServer.getSeriesIndex !== "function") return [];
    const result = await guidesServer.getSeriesIndex(locale);
    return Array.isArray(result) ? result : [];
  } catch {
    return [];
  }
}

/**
 * Read each news channel up to the full desk size. A busy channel can supply every
 * headline, while a quieter channel still gets a direct link to its own archive.
 */
export async function loadHomeGuides(locale: Locale): Promise<HomePortalData> {
  const [tech, travel, money, rawNews, rawSoftware, rawTrendingArticles, rawSeries] = await Promise.all([
    guidesServer.getGuideList(locale, { kind: "life", topic: "ai", sort: "curated" }, FETCH_PER_BLOCK),
    guidesServer.getGuideList(locale, { kind: "howto", sort: "curated" }, FETCH_PER_BLOCK),
    guidesServer.getGuideList(locale, { kind: "life", topic: "finance", sort: "curated" }, FETCH_PER_BLOCK),
    Promise.all(
      NEWS_TOPICS.map((topic) =>
        guidesServer.getGuideList(locale, { kind: "life", topic, sort: "news" }, NEWS_DESK_LIMIT),
      ),
    ),
    guidesServer.getGuideList(locale, { kind: "life", topic: "software", sort: "curated" }, FETCH_PER_BLOCK),
    safeTrendingGuides(locale),
    safeSeriesIndex(locale),
  ]);

  const blocks: HomeGuideBlock[] = [
    { key: "tech", href: guideTopicHref("life", "ai"), articles: tech.articles },
    { key: "travel", href: "/guides", articles: travel.articles },
    { key: "money", href: guideTopicHref("life", "finance"), articles: money.articles },
  ];

  const newsTopics = NEWS_TOPICS.filter((_, index) => rawNews[index].articles.some((article) => article.news_date));
  const newsByKey = new Map<string, GuideSummary>();
  for (const group of rawNews) {
    for (const item of group.articles) {
      const key = articleKey(item);
      if (item.news_date && !newsByKey.has(key)) {
        newsByKey.set(key, item);
      }
    }
  }
  const news = [...newsByKey.values()].sort(newsOrder).slice(0, NEWS_DESK_LIMIT);
  return { blocks, news, newsTopics, trending: rawTrendingArticles, software: rawSoftware.articles, series: rawSeries };
}

/**
 * Mokaair's portal entrance: site identity, quick trip-comparison link, inline article search,
 * quick links to hotspots/foods/videos/Atom feed, and interactive category/news/trending views.
 *
 * Sits before and outside `DiscoveryHomeGate` so crawlers and readers get the full editorial
 * portal on initial server render regardless of discovery mode.
 */
export function HomeGuides({
  blocks,
  news = [],
  newsTopics = [],
  trending = [],
  software = [],
  series = [],
  hotspotsEnabled = true,
  flightSearchEnabled = true,
  videosEnabled = true,
}: {
  blocks: HomeGuideBlock[];
  news?: GuideSummary[];
  newsTopics?: string[];
  trending?: GuideSummary[];
  software?: GuideSummary[];
  series?: SeriesSummary[];
  hotspotsEnabled?: boolean;
  flightSearchEnabled?: boolean;
  videosEnabled?: boolean;
}) {
  const rawLocale = useLocale();
  const locale = normalizeLocale(rawLocale);
  const t = useTranslations("search.homeGuides");
  const common = useTranslations("common");
  const nav = useTranslations("navigation");
  const flow = getFrontendFlowCopy(rawLocale);
  const cardLabels = {
    intel: common("guides.intel"),
    howto: common("guides.howto"),
    life: common("guides.life"),
  };
  const populatedHrefs = new Set(newsTopics.map((slug) => guideTopicHref("life", slug)));
  const newsChannels = navGroups.flatMap((group) =>
    group.items.filter((item) => populatedHrefs.has(item.href)).map((item) => ({
      href: item.href, label: nav(navItemLabelKey(group.key, item.key)),
    })),
  );

  // The overview gives dated headlines first choice. Category tabs keep the editor's
  // complete selection, including stories already visible in the overview's news desk.
  const shown = new Set(news.map(articleKey));
  function takeUnseen(articles: GuideSummary[], limit: number): GuideSummary[] {
    const picks: GuideSummary[] = [];
    for (const article of articles) {
      const key = articleKey(article);
      if (shown.has(key)) continue;
      shown.add(key);
      picks.push(article);
      if (picks.length === limit) break;
    }
    return picks;
  }
  const overviewBlocks = blocks.map((block) => ({ ...block, articles: takeUnseen(block.articles, OVERVIEW_PER_BLOCK) }))
    .filter((block) => block.articles.length > 0);
  const overviewSoftware = takeUnseen(software, OVERVIEW_PER_BLOCK);
  const trendingPicks = takeUnseen(trending, TRENDING_LIMIT);
  const seriesPicks = series.filter((item) => !shown.has(articleKey(item.hub))).slice(0, SERIES_LIMIT);

  return (
    <section aria-labelledby="home-guides-title" className="mx-auto max-w-6xl px-4 pb-12 pt-4 sm:px-5 md:px-8 md:pt-7">
      <div className="flex flex-wrap items-start justify-between gap-3 sm:items-center sm:gap-4">
        <div className="min-w-0">
          <span className="inline-flex items-center gap-2 rounded-full border border-[color-mix(in_srgb,var(--teal)_28%,var(--line))] bg-[var(--teal-soft)] px-3 py-1 text-[length:var(--text-xs)] font-extrabold uppercase tracking-wider text-[var(--teal-dark)]">
            <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-[var(--teal)]" />
            {t("eyebrow")}
          </span>
          <h1
            id="home-guides-title"
            className="mt-2.5 text-[1.45rem] font-extrabold leading-[1.28] tracking-tight sm:text-3xl md:text-[2.15rem] md:leading-[1.22]"
          >
            {t("title")}
          </h1>
        </div>
        {flightSearchEnabled ? (
          <Link
            href="/search/new"
            className="inline-flex min-h-11 items-center gap-2 rounded-full border border-[var(--teal)] bg-[var(--surface)] px-4 py-2 text-sm font-semibold text-[var(--teal)] shadow-[var(--shadow-sm)] transition-all hover:-translate-y-0.5 hover:bg-[var(--teal-soft)]"
          >
            {flow.searchTrips}<ArrowRight size={17} className="shrink-0" aria-hidden />
          </Link>
        ) : null}
      </div>
      <p className="mt-2.5 max-w-3xl text-sm leading-6 text-[var(--muted)] sm:mt-3 sm:text-base sm:leading-7">
        {t("intro")}
      </p>

      <div
        data-testid="portal-toolbar"
        className="portal-hero-shell mt-4 flex flex-col gap-3 rounded-2xl p-3.5 sm:mt-5 md:flex-row md:items-center md:justify-between md:p-4"
      >
        <form
          role="search"
          method="get"
          action={`/${locale}/search/articles`}
          className="flex min-w-0 flex-1 flex-wrap items-center gap-2 sm:flex-nowrap"
        >
          <label className="sr-only" htmlFor="home-portal-search-q">{t("searchButton")}</label>
          <div className="relative min-w-0 flex-1 basis-44">
            <Search
              size={17}
              aria-hidden
              className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-[var(--muted)]"
            />
            <input
              id="home-portal-search-q"
              type="search"
              name="q"
              placeholder={t("searchPlaceholder")}
              maxLength={100}
              autoComplete="off"
              required
              style={{ paddingInlineStart: "2.45rem" }}
              className="app-field min-h-11 w-full min-w-0 bg-[var(--surface)] pr-3 focus-visible:border-[var(--teal)] focus-visible:outline-none lg:pr-14"
            />
            <kbd
              aria-hidden="true"
              className="pointer-events-none absolute right-3 top-1/2 hidden -translate-y-1/2 rounded-md border border-[var(--line)] bg-[var(--paper)] px-1.5 py-0.5 font-mono text-[length:var(--text-xs)] font-semibold text-[var(--muted)] lg:inline-block"
            >
              ⌘K
            </kbd>
          </div>
          <button type="submit" className="app-primary-button min-h-11 grow justify-center px-4 min-[420px]:grow-0">
            <Search size={16} aria-hidden />
            {t("searchButton")}
          </button>
        </form>
        <div className="portal-scroll-strip flex items-center gap-2 text-[length:var(--text-xs)] font-semibold md:flex-wrap md:overflow-visible">
          {hotspotsEnabled ? (
            <Link
              href="/hotspots"
              className="inline-flex min-h-11 shrink-0 snap-start items-center gap-1.5 whitespace-nowrap rounded-full border border-[var(--line)] bg-[var(--surface)] px-3.5 text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
            >
              <Compass size={15} className="text-[var(--teal)]" aria-hidden />
              {t("quickHotspotsShort")}
            </Link>
          ) : null}
          <Link
            href="/foods"
            className="inline-flex min-h-11 shrink-0 snap-start items-center gap-1.5 whitespace-nowrap rounded-full border border-[var(--line)] bg-[var(--surface)] px-3.5 text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
          >
            <Soup size={15} className="text-[var(--coral)]" aria-hidden />
            {t("quickFoodsShort")}
          </Link>
          {videosEnabled ? (
            <Link
              href="/videos"
              className="inline-flex min-h-11 shrink-0 snap-start items-center gap-1.5 whitespace-nowrap rounded-full border border-[var(--line)] bg-[var(--surface)] px-3.5 text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
            >
              <Film size={15} className="text-[var(--teal)]" aria-hidden />
              {t("quickVideosShort")}
            </Link>
          ) : null}
          {news.length === 0 ? (
            <a
              href={`/${locale}/life/feed.xml`}
              className="inline-flex min-h-11 shrink-0 snap-start items-center gap-1.5 whitespace-nowrap rounded-full border border-[var(--line)] bg-[var(--surface)] px-3.5 text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
            >
              <Rss size={15} className="text-[var(--coral)]" aria-hidden />
              {t("newsDeskRss")}
            </a>
          ) : null}
        </div>
      </div>

      <HomePortalTabs
        locale={locale}
        blocks={blocks}
        news={news}
        newsChannels={newsChannels}
        overviewBlocks={overviewBlocks}
        overviewSoftware={overviewSoftware}
        trending={trendingPicks}
        software={software}
        series={seriesPicks}
        labels={{
          cardLabels,
          blockTitles: {
            travel: t("travel"),
            tech: t("tech"),
            money: t("money"),
            software: t("software"),
          },
          seeAll: t("seeAll"),
          tabsLabel: t("tabsLabel"),
          tabAll: t("tabAll"),
          tabNews: t("tabNews"),
          tabAi: t("tabAi"),
          tabSoftware: t("tabSoftware"),
          tabTravel: t("tabTravel"),
          tabMoney: t("tabMoney"),
          featuredLeadBadge: t("featuredLeadBadge"),
          newsDeskTitle: t("newsDeskTitle"),
          newsDeskLead: t("newsDeskLead"),
          newsDeskRss: t("newsDeskRss"),
          trendingTitle: t("trendingTitle"),
          trendingLead: t("trendingLead"),
          seriesTitle: t("seriesTitle"),
        }}
      />
    </section>
  );
}
