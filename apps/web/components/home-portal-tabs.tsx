"use client";

import { ArrowRight, ArrowUpRight, Flame, Layers, Newspaper, Rss } from "lucide-react";
import { useState } from "react";
import { GuideCard, type GuideCardLabels } from "@/components/guides/card";
import { GuideImage } from "@/components/guides/guide-image";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, guideTopicHref, visibleGuideHero, type GuideSummary } from "@/lib/guides";
import type { SeriesSummary } from "@/lib/guide-series";

export type HomeGuideBlock = {
  key: "travel" | "tech" | "money";
  href: string;
  articles: GuideSummary[];
};

export type PortalTabId = "all" | "news" | "ai" | "software" | "travel" | "money";

export type HomePortalTabsLabels = {
  cardLabels: GuideCardLabels;
  blockTitles: Record<HomeGuideBlock["key"] | "software", string>;
  seeAll: string;
  tabsLabel: string;
  tabAll: string;
  tabNews: string;
  tabAi: string;
  tabSoftware: string;
  tabTravel: string;
  tabMoney: string;
  featuredLeadBadge: string;
  newsDeskTitle: string;
  newsDeskLead: string;
  newsDeskRss: string;
  trendingTitle: string;
  trendingLead: string;
  seriesTitle: string;
};

export function HomePortalTabs({
  locale,
  blocks,
  news,
  trending,
  software,
  series,
  labels,
}: {
  locale: Locale;
  blocks: HomeGuideBlock[];
  news: GuideSummary[];
  trending: GuideSummary[];
  software: GuideSummary[];
  series: SeriesSummary[];
  labels: HomePortalTabsLabels;
}) {
  const [activeTab, setActiveTab] = useState<PortalTabId>("all");

  const nonEmptyBlocks = blocks.filter((block) => block.articles.length > 0);
  const hasTech = nonEmptyBlocks.some((block) => block.key === "tech");
  const hasTravel = nonEmptyBlocks.some((block) => block.key === "travel");
  const hasMoney = nonEmptyBlocks.some((block) => block.key === "money");

  const availableTabs: Array<{ id: PortalTabId; label: string }> = [
    { id: "all", label: labels.tabAll },
    ...(news.length > 0 ? [{ id: "news" as const, label: labels.tabNews }] : []),
    ...(hasTech ? [{ id: "ai" as const, label: labels.tabAi }] : []),
    ...(software.length > 0 ? [{ id: "software" as const, label: labels.tabSoftware }] : []),
    ...(hasTravel ? [{ id: "travel" as const, label: labels.tabTravel }] : []),
    ...(hasMoney ? [{ id: "money" as const, label: labels.tabMoney }] : []),
  ];

  const currentTab = availableTabs.some((tab) => tab.id === activeTab) ? activeTab : "all";
  const showNewsDesk = (currentTab === "all" || currentTab === "news") && news.length > 0;
  const showSideRail = currentTab === "all" && (trending.length > 0 || series.length > 0);
  const showSoftware = (currentTab === "all" || currentTab === "software") && software.length > 0;

  const visibleBlocks = nonEmptyBlocks.filter((block) => {
    if (currentTab === "all") return true;
    if (currentTab === "ai") return block.key === "tech";
    if (currentTab === "travel") return block.key === "travel";
    if (currentTab === "money") return block.key === "money";
    return false;
  });

  const leadStory = news[0] ?? null;
  const leadHero = visibleGuideHero(leadStory?.hero);
  const deskStories = news.slice(1, 11);
  const subLeads = deskStories.length >= 2 ? deskStories.slice(0, 2) : [];
  const wireStories = deskStories.length >= 2 ? deskStories.slice(2) : deskStories;

  return (
    <div className="mt-5 space-y-8 sm:mt-6 sm:space-y-9">
      {availableTabs.length >= 3 ? (
        <div
          role="group"
          aria-label={labels.tabsLabel}
          data-testid="portal-tabs"
          className="portal-scroll-strip flex items-center gap-2 border-b border-[var(--line)] pb-3.5 sm:flex-wrap sm:overflow-visible"
        >
          {availableTabs.map((tab) => {
            const active = currentTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                aria-pressed={active}
                onClick={() => setActiveTab(tab.id)}
                className={`inline-flex min-h-11 shrink-0 snap-start items-center gap-1.5 whitespace-nowrap rounded-full px-4 py-2 text-sm font-semibold transition-all ${
                  active
                    ? "border border-[var(--teal)] bg-[var(--teal-fill)] text-[var(--primary-text)] shadow-[var(--shadow-sm)]"
                    : "border border-[var(--line)] bg-[var(--surface)] text-[var(--ink)] hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/50 hover:text-[var(--teal-dark)]"
                }`}
              >
                {active ? <span aria-hidden className="h-1.5 w-1.5 rounded-full bg-current opacity-90" /> : null}
                {tab.label}
              </button>
            );
          })}
        </div>
      ) : null}

      {showNewsDesk || showSideRail ? (
        <div
          className={`grid gap-5 sm:gap-6 ${
            showNewsDesk && showSideRail ? "lg:grid-cols-[minmax(0,1.68fr)_minmax(19rem,1fr)] lg:items-start" : ""
          }`}
        >
          {showNewsDesk && leadStory ? (
            <div
              data-testid="portal-news-desk"
              className="min-w-0 rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-sm)] sm:p-5 md:p-6"
            >
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] pb-3.5">
                <div className="min-w-0">
                  <h3 className="flex items-center gap-2.5 text-lg font-extrabold tracking-tight sm:text-xl">
                    <span className="inline-grid h-8 w-8 shrink-0 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal-dark)]">
                      <Newspaper size={17} aria-hidden />
                    </span>
                    {labels.newsDeskTitle}
                  </h3>
                  <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{labels.newsDeskLead}</p>
                </div>
                <div className="flex flex-wrap items-center gap-2 text-sm font-semibold">
                  <a
                    href={`/${locale}/life/feed.xml`}
                    className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/75 px-3.5 text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
                  >
                    <Rss size={15} className="text-[var(--coral)]" aria-hidden />
                    {labels.newsDeskRss}
                  </a>
                  <Link
                    href="/life"
                    className="inline-flex min-h-11 items-center gap-1 rounded-full px-3 text-[var(--teal)] transition-colors hover:bg-[var(--teal-soft)]"
                  >
                    {labels.seeAll}
                    <ArrowRight size={15} className="shrink-0" aria-hidden />
                  </Link>
                </div>
              </div>

              <article
                data-testid="portal-hero"
                className={`group relative mt-4 rounded-2xl border border-[color-mix(in_srgb,var(--teal)_42%,var(--line))] bg-[color-mix(in_srgb,var(--teal-soft)_38%,var(--surface))] p-4 shadow-[var(--shadow-sm)] transition-all duration-200 hover:border-[var(--teal)] hover:shadow-[var(--shadow-md)] sm:p-5 ${
                  leadHero
                    ? "md:grid md:grid-cols-[1.08fr_1.2fr] md:items-center md:gap-5"
                    : "border-l-4 border-l-[var(--teal)]"
                }`}
              >
                {leadHero ? (
                  <div className="mb-3.5 overflow-hidden rounded-xl bg-[var(--paper)] ring-1 ring-black/5 md:mb-0">
                    <GuideImage
                      src={leadHero.src}
                      alt={leadHero.alt}
                      width={leadHero.width}
                      height={leadHero.height}
                      loading="eager"
                      fetchPriority="high"
                      decoding="async"
                      className="aspect-video w-full object-cover transition-transform duration-300 group-hover:scale-[1.02]"
                    />
                  </div>
                ) : null}
                <div className="min-w-0">
                  <p className="flex flex-wrap items-center gap-2 text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">
                    <span className="rounded-full bg-[var(--teal-fill)] px-2.5 py-0.5 text-[var(--primary-text)]">
                      {labels.featuredLeadBadge}
                    </span>
                    {leadStory.news_date ? (
                      <time dateTime={leadStory.news_date} className="font-mono tabular-nums">
                        {leadStory.news_date}
                      </time>
                    ) : null}
                    {leadStory.topics[0] ? (
                      <span className="rounded-full border border-[var(--line)] bg-[var(--surface)] px-2 py-0.5 text-[var(--ink)]">
                        {leadStory.topics[0].label}
                      </span>
                    ) : null}
                  </p>
                  <h4 className="mt-2.5 text-lg font-extrabold leading-[1.36] tracking-tight sm:text-xl md:text-2xl md:leading-snug">
                    <Link
                      href={guideHref(leadStory.kind, leadStory.slug)}
                      className="text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
                    >
                      {leadStory.title}
                    </Link>
                  </h4>
                  <p className="mt-2 line-clamp-2 text-sm leading-6 text-[var(--muted)] sm:line-clamp-3">
                    {leadStory.description}
                  </p>
                </div>
              </article>

              {subLeads.length > 0 ? (
                <div className="mt-3.5 grid gap-3 sm:mt-4 sm:grid-cols-2 sm:gap-3.5">
                  {subLeads.map((story) => {
                    const storyHero = visibleGuideHero(story.hero);
                    return (
                      <article
                        key={story.slug}
                        className="portal-card-surface group relative flex items-start gap-3.5 rounded-2xl p-3.5 sm:flex-col sm:items-stretch sm:justify-between sm:p-4"
                      >
                        {storyHero ? (
                          <div className="w-24 shrink-0 overflow-hidden rounded-xl bg-[var(--paper)] ring-1 ring-black/5 sm:mb-3 sm:w-full">
                            <GuideImage
                              src={storyHero.src}
                              alt={storyHero.alt}
                              width={storyHero.width}
                              height={storyHero.height}
                              loading="lazy"
                              decoding="async"
                              className="aspect-[4/3] w-full object-cover transition-transform duration-300 group-hover:scale-[1.03] sm:aspect-video"
                            />
                          </div>
                        ) : null}
                        <div className="min-w-0 flex-1">
                          <p className="flex flex-wrap items-center gap-1.5 text-[length:var(--text-xs)] text-[var(--muted)] sm:gap-2">
                            {story.news_date ? (
                              <time dateTime={story.news_date} className="font-mono font-semibold tabular-nums">
                                {story.news_date}
                              </time>
                            ) : null}
                            {story.topics[0] ? (
                              <span className="rounded-full bg-[var(--teal-soft)] px-2 py-0.5 font-semibold text-[var(--teal-dark)]">
                                {story.topics[0].label}
                              </span>
                            ) : null}
                          </p>
                          <h4 className="mt-1.5 text-[0.96875rem] font-bold leading-6 tracking-tight sm:mt-2 sm:text-base">
                            <Link
                              href={guideHref(story.kind, story.slug)}
                              className="text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
                            >
                              {story.title}
                            </Link>
                          </h4>
                          <p className="mt-1.5 hidden text-sm leading-6 text-[var(--muted)] sm:block">
                            <span className="line-clamp-2">{story.description}</span>
                          </p>
                        </div>
                      </article>
                    );
                  })}
                </div>
              ) : null}

              {wireStories.length > 0 ? (
                <ul className="mt-4 divide-y divide-[var(--line)] border-t border-[var(--line)] pt-1">
                  {wireStories.map((story) => (
                    <li
                      key={story.slug}
                      className="group relative -mx-2 flex flex-col gap-1 rounded-xl px-2 py-3 transition-colors hover:bg-[var(--paper)]/75 sm:flex-row sm:items-baseline sm:justify-between sm:gap-3 sm:py-2.5"
                    >
                      <div className="flex min-w-0 flex-col gap-1 sm:flex-row sm:items-baseline sm:gap-3">
                        <div className="flex shrink-0 items-center gap-2 text-[length:var(--text-xs)] text-[var(--muted)]">
                          {story.news_date ? (
                            <time dateTime={story.news_date} className="font-mono font-medium tabular-nums">
                              {story.news_date}
                            </time>
                          ) : null}
                          {story.topics[0] ? (
                            <span className="rounded-full border border-[var(--line)] bg-[var(--paper)] px-2 py-0.5 font-medium text-[var(--ink)]">
                              {story.topics[0].label}
                            </span>
                          ) : null}
                        </div>
                        <Link
                          href={guideHref(story.kind, story.slug)}
                          className="min-w-0 text-[0.96875rem] font-semibold leading-6 text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline sm:text-base"
                        >
                          {story.title}
                        </Link>
                      </div>
                      <ArrowUpRight
                        size={15}
                        aria-hidden
                        className="hidden shrink-0 text-[var(--muted)] opacity-0 transition-all group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-[var(--teal)] group-hover:opacity-100 sm:block"
                      />
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
          ) : null}

          {showSideRail ? (
            <aside className="min-w-0 space-y-5 lg:sticky lg:top-24">
              {trending.length > 0 ? (
                <section
                  aria-labelledby="portal-trending-heading"
                  data-testid="portal-trending"
                  className="rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-sm)] sm:p-5"
                >
                  <div className="border-b border-[var(--line)] pb-3">
                    <h3 id="portal-trending-heading" className="flex items-center gap-2 text-lg font-extrabold tracking-tight">
                      <span className="inline-grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-[var(--coral-soft)] text-[var(--coral)]">
                        <Flame size={16} aria-hidden />
                      </span>
                      {labels.trendingTitle}
                    </h3>
                    <p className="mt-1 text-[length:var(--text-xs)] leading-5 text-[var(--muted)]">{labels.trendingLead}</p>
                  </div>
                  <ol className="mt-2 divide-y divide-[var(--line)]">
                    {trending.map((article, index) => {
                      const rankClass = index === 0
                        ? "bg-[var(--teal-fill)] text-[var(--primary-text)] shadow-[var(--shadow-sm)]"
                        : index < 3
                          ? "bg-[var(--coral-soft)] text-[var(--coral)]"
                          : "border border-[var(--line)] bg-[var(--paper)] text-[var(--muted)]";
                      return (
                        <li
                          key={`${article.kind}:${article.slug}`}
                          className="group relative -mx-2 flex items-start gap-3 rounded-xl px-2 py-2.5 transition-colors hover:bg-[var(--paper)]/70"
                        >
                          <span
                            aria-hidden
                            className={`mt-0.5 inline-grid h-7 w-7 shrink-0 place-items-center rounded-lg font-mono text-[length:var(--text-xs)] font-extrabold tabular-nums ${rankClass}`}
                          >
                            {String(index + 1).padStart(2, "0")}
                          </span>
                          <div className="min-w-0">
                            <Link
                              href={guideHref(article.kind, article.slug)}
                              className="text-sm font-bold leading-6 text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
                            >
                              {article.title}
                            </Link>
                            <p className="mt-0.5 text-[length:var(--text-xs)] text-[var(--muted)]">
                              {article.topics[0]?.label ?? labels.cardLabels[article.kind]}
                            </p>
                          </div>
                        </li>
                      );
                    })}
                  </ol>
                </section>
              ) : null}

              {series.length > 0 ? (
                <section
                  aria-labelledby="portal-series-heading"
                  data-testid="portal-series"
                  className="rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-sm)] sm:p-5"
                >
                  <h3 id="portal-series-heading" className="flex items-center gap-2 text-lg font-extrabold tracking-tight">
                    <span className="inline-grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-[var(--teal-soft)] text-[var(--teal-dark)]">
                      <Layers size={16} aria-hidden />
                    </span>
                    {labels.seriesTitle}
                  </h3>
                  <ul className="mt-3.5 space-y-2">
                    {series.map((item) => (
                      <li key={item.slug}>
                        <Link
                          href={guideHref(item.hub.kind, item.hub.slug)}
                          className="flex min-h-11 items-center justify-between gap-2 rounded-xl border border-[var(--line)] bg-[var(--paper)]/55 px-3.5 py-2.5 text-sm font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/50 hover:text-[var(--teal-dark)]"
                        >
                          <span className="min-w-0">{item.hub.title}</span>
                          <ArrowUpRight size={15} className="shrink-0 text-[var(--teal)]" aria-hidden />
                        </Link>
                      </li>
                    ))}
                  </ul>
                </section>
              ) : null}
            </aside>
          ) : null}
        </div>
      ) : null}

      {showSoftware ? (
        <div data-testid="portal-software" className="min-w-0">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] pb-2.5">
            <h3 className="portal-section-heading text-xl font-extrabold tracking-tight">
              {labels.blockTitles.software}
            </h3>
            <Link
              href={guideTopicHref("life", "software")}
              className="inline-flex min-h-11 items-center gap-1 rounded-full px-3 text-sm font-semibold text-[var(--teal)] transition-colors hover:bg-[var(--teal-soft)]"
            >
              {labels.seeAll}
              <ArrowRight size={15} className="shrink-0" aria-hidden />
            </Link>
          </div>
          {currentTab === "all" ? (
            <ul className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {software.slice(0, 4).map((article) => (
                <GuideCard key={article.slug} article={article} labels={labels.cardLabels} />
              ))}
            </ul>
          ) : (
            <ul className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {software.map((article, index) => (
                <GuideCard
                  key={article.slug}
                  article={article}
                  labels={labels.cardLabels}
                  variant={index === 0 && software.length >= 3 ? "featured" : "default"}
                />
              ))}
            </ul>
          )}
        </div>
      ) : null}

      {visibleBlocks.length > 0 ? (
        <div className={`grid gap-6 ${currentTab === "all" ? "lg:grid-cols-3" : ""}`}>
          {visibleBlocks.map((block) => {
            const shownArticles = currentTab === "all" ? block.articles.slice(0, 4) : block.articles;
            return (
              <div key={block.key} className="min-w-0" data-testid={`home-guides-${block.key}`}>
                <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] pb-2.5">
                  <h3 className="portal-section-heading text-xl font-extrabold tracking-tight">
                    {labels.blockTitles[block.key]}
                  </h3>
                  <Link
                    href={block.href}
                    className="inline-flex min-h-11 items-center gap-1 rounded-full px-3 text-sm font-semibold text-[var(--teal)] transition-colors hover:bg-[var(--teal-soft)]"
                  >
                    {labels.seeAll}
                    <ArrowRight size={15} className="shrink-0" aria-hidden />
                  </Link>
                </div>
                {currentTab === "all" ? (
                  <ul className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
                    {shownArticles.map((article) => (
                      <GuideCard key={article.slug} article={article} labels={labels.cardLabels} variant="compact" />
                    ))}
                  </ul>
                ) : (
                  <ul className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {shownArticles.map((article, index) => (
                      <GuideCard
                        key={article.slug}
                        article={article}
                        labels={labels.cardLabels}
                        variant={index === 0 && shownArticles.length >= 3 ? "featured" : "default"}
                      />
                    ))}
                  </ul>
                )}
              </div>
            );
          })}
        </div>
      ) : null}

      {currentTab !== "all" && currentTab !== "news" ? (() => {
        const categorySeries = series.filter((item) => {
          if (currentTab === "travel") return item.section === "travel";
          if (currentTab === "ai") {
            return item.section === "life" && (
              item.topic?.startsWith("ai")
              || item.slug === "claude-code"
              || item.slug === "codex"
              || item.slug === "gemini"
            );
          }
          if (currentTab === "software") return item.section === "life" && item.topic === "software";
          if (currentTab === "money") return item.section === "life" && item.topic === "finance";
          return false;
        });
        if (!categorySeries.length) return null;
        return (
          <section
            aria-label={labels.seriesTitle}
            data-testid="portal-category-series"
            className="rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]"
          >
            <h3 className="flex items-center gap-2 text-lg font-extrabold tracking-tight">
              <span className="inline-grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-[var(--teal-soft)] text-[var(--teal-dark)]">
                <Layers size={16} aria-hidden />
              </span>
              {labels.seriesTitle}
            </h3>
            <ul className="mt-3.5 grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
              {categorySeries.map((item) => (
                <li key={item.slug}>
                  <Link
                    href={guideHref(item.hub.kind, item.hub.slug)}
                    className="flex min-h-11 items-center justify-between gap-2 rounded-xl border border-[var(--line)] bg-[var(--paper)]/55 px-3.5 py-2.5 text-sm font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/50 hover:text-[var(--teal-dark)]"
                  >
                    <span className="min-w-0">{item.hub.title}</span>
                    <ArrowUpRight size={15} className="shrink-0 text-[var(--teal)]" aria-hidden />
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        );
      })() : null}
    </div>
  );
}
