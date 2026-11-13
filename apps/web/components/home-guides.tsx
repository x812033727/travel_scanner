import { ArrowRight, Compass, Film, Rss, Search, Soup } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { HomePortalTabs, type HomeGuideBlock } from "@/components/home-portal-tabs";
import { Link } from "@/i18n/navigation";
import { normalizeLocale, type Locale } from "@/i18n/routing";
import { NEWS_TOPICS, guideTopicHref, newsOrder, type GuideSummary } from "@/lib/guides";
import type { SeriesSummary } from "@/lib/guide-series";
import * as guidesServer from "@/lib/guides.server";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";

export type { HomeGuideBlock };

const PER_BLOCK = 4;
const NEWS_PER_TOPIC = 10;
const NEWS_DESK_LIMIT = 11;
const TRENDING_FETCH_LIMIT = 18;
const TRENDING_LIMIT = 6;
const SERIES_LIMIT = 4;

export type HomePortalData = {
  blocks: HomeGuideBlock[];
  news: GuideSummary[];
  trending: GuideSummary[];
  software: GuideSummary[];
  series: SeriesSummary[];
};

const articleKey = (article: Pick<GuideSummary, "kind" | "slug">) => `${article.kind}:${article.slug}`;

/**
 * Reads the portal homepage sections in parallel and deduplicates across them so no article
 * link appears twice on the first screen. A failed read degrades to an empty section, never
 * a thrown page, and optional server helpers are guarded so lightweight unit-test mocks that
 * only stub `getGuideList` continue to work unchanged.
 */
export async function loadHomeGuides(locale: Locale): Promise<HomePortalData> {
  const [tech, travel, money, rawNews, rawSoftware, rawTrending, rawSeries] = await Promise.all([
    guidesServer.getGuideList(locale, { kind: "life", topic: "ai", sort: "curated" }, PER_BLOCK),
    guidesServer.getGuideList(locale, { kind: "howto", sort: "curated" }, PER_BLOCK),
    guidesServer.getGuideList(locale, { kind: "life", topic: "finance", sort: "curated" }, PER_BLOCK),
    Promise.all(
      NEWS_TOPICS.map((topic) =>
        guidesServer.getGuideList(locale, { kind: "life", topic, sort: "news" }, NEWS_PER_TOPIC),
      ),
    ),
    guidesServer.getGuideList(locale, { kind: "life", topic: "software", sort: "curated" }, PER_BLOCK),
    typeof guidesServer.getTrendingGuides === "function"
      ? guidesServer.getTrendingGuides(locale, {}, TRENDING_FETCH_LIMIT)
      : Promise.resolve({ articles: [], next_cursor: null, available: false }),
    typeof guidesServer.getSeriesIndex === "function"
      ? guidesServer.getSeriesIndex(locale)
      : Promise.resolve([]),
  ]);

  const blocks: HomeGuideBlock[] = [
    { key: "tech", href: guideTopicHref("life", "ai"), articles: tech.articles },
    { key: "travel", href: "/guides", articles: travel.articles },
    { key: "money", href: guideTopicHref("life", "finance"), articles: money.articles },
  ];

  const shown = new Set<string>(blocks.flatMap((block) => block.articles.map(articleKey)));

  const newsByKey = new Map<string, GuideSummary>();
  for (const group of rawNews) {
    for (const item of group.articles) {
      const key = articleKey(item);
      if (item.news_date && !shown.has(key) && !newsByKey.has(key)) {
        newsByKey.set(key, item);
      }
    }
  }
  const news = [...newsByKey.values()].sort(newsOrder).slice(0, NEWS_DESK_LIMIT);
  for (const item of news) shown.add(articleKey(item));

  const software: GuideSummary[] = [];
  for (const item of rawSoftware.articles) {
    const key = articleKey(item);
    if (!shown.has(key) && software.length < PER_BLOCK) {
      shown.add(key);
      software.push(item);
    }
  }

  const trending: GuideSummary[] = [];
  for (const item of rawTrending.articles) {
    const key = articleKey(item);
    if (!shown.has(key) && trending.length < TRENDING_LIMIT) {
      shown.add(key);
      trending.push(item);
    }
  }

  const series = rawSeries
    .filter((item) => !shown.has(`${item.hub.kind}:${item.hub.slug}`))
    .slice(0, SERIES_LIMIT);

  return { blocks, news, trending, software, series };
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
  trending = [],
  software = [],
  series = [],
  hotspotsEnabled = true,
}: {
  blocks: HomeGuideBlock[];
  news?: GuideSummary[];
  trending?: GuideSummary[];
  software?: GuideSummary[];
  series?: SeriesSummary[];
  hotspotsEnabled?: boolean;
}) {
  const rawLocale = useLocale();
  const locale = normalizeLocale(rawLocale);
  const t = useTranslations("search.homeGuides");
  const common = useTranslations("common");
  const flow = getFrontendFlowCopy(rawLocale);
  const cardLabels = {
    intel: common("guides.intel"),
    howto: common("guides.howto"),
    life: common("guides.life"),
  };

  return (
    <section aria-labelledby="home-guides-title" className="mx-auto max-w-6xl px-5 pb-12 pt-5 md:px-8 md:pt-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="min-w-0">
          <p className="inline-flex items-center gap-2 rounded-full bg-[var(--teal-soft)] px-3 py-1 text-[length:var(--text-xs)] font-extrabold uppercase tracking-wider text-[var(--teal-dark)]">
            {t("eyebrow")}
          </p>
          <h2
            id="home-guides-title"
            className="mt-2 text-2xl font-extrabold tracking-tight md:text-[2.1rem] md:leading-tight"
          >
            {t("title")}
          </h2>
        </div>
        <Link
          href="/search/new"
          className="inline-flex min-h-11 items-center gap-2 rounded-full border border-[var(--teal)] bg-[var(--surface)] px-4 py-2 text-sm font-semibold text-[var(--teal)] shadow-[var(--shadow-sm)] transition-all hover:-translate-y-0.5 hover:bg-[var(--teal-soft)]"
        >
          {flow.searchTrips}<ArrowRight size={17} className="shrink-0" aria-hidden />
        </Link>
      </div>
      <p className="mt-3 max-w-3xl text-base leading-7 text-[var(--muted)]">{t("intro")}</p>

      <div
        data-testid="portal-toolbar"
        className="mt-5 flex flex-col gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3 shadow-[var(--shadow-sm)] md:flex-row md:items-center md:justify-between md:p-4"
      >
        <form
          role="search"
          method="get"
          action={`/${locale}/search/articles`}
          className="flex min-w-0 flex-1 items-center gap-2"
        >
          <label className="sr-only" htmlFor="home-portal-search-q">{t("searchButton")}</label>
          <input
            id="home-portal-search-q"
            type="search"
            name="q"
            placeholder={t("searchPlaceholder")}
            maxLength={100}
            autoComplete="off"
            required
            className="app-field min-h-11 min-w-0 flex-1 focus-visible:border-[var(--teal)] focus-visible:outline-none"
          />
          <button type="submit" className="app-primary-button min-h-11 shrink-0 px-4">
            <Search size={16} aria-hidden />
            {t("searchButton")}
          </button>
        </form>
        <div className="flex flex-wrap items-center gap-2 text-[length:var(--text-xs)] font-semibold">
          {hotspotsEnabled ? (
            <Link
              href="/hotspots"
              className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/70 px-3.5 text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
            >
              <Compass size={15} aria-hidden />
              {t("quickHotspotsShort")}
            </Link>
          ) : null}
          <Link
            href="/foods"
            className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/70 px-3.5 text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
          >
            <Soup size={15} aria-hidden />
            {t("quickFoodsShort")}
          </Link>
          <Link
            href="/videos"
            className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/70 px-3.5 text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
          >
            <Film size={15} aria-hidden />
            {t("quickVideosShort")}
          </Link>
          {news.length === 0 ? (
            <a
              href={`/${locale}/life/feed.xml`}
              className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/70 px-3.5 text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
            >
              <Rss size={15} aria-hidden />
              {t("newsDeskRss")}
            </a>
          ) : null}
        </div>
      </div>

      <HomePortalTabs
        locale={locale}
        blocks={blocks}
        news={news}
        trending={trending}
        software={software}
        series={series}
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
