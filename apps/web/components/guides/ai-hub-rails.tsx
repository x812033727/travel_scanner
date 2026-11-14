import { GuideCard } from "@/components/guides/card";
import { NewsList } from "@/components/guides/news-list";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideTopicHref, type GuideSummary, type GuideTopic } from "@/lib/guides";
import { getGuideList } from "@/lib/guides.server";

/**
 * The AI hub's first screen, laid out by what the reader came to do rather than by tool:
 * pick a plan, compare the assistants, get work done, make images and video, write code,
 * and earn with it. Each rail is one sub-topic -- its label, its description and its four
 * picks in the editor's order -- with a link to that sub-topic's own hub.
 *
 * The rails are sub-topics so the vocabulary keeps naming them in every language, and a
 * sub-topic with nothing published in this language is simply left out, as the chips do.
 */
export const AI_HUB_RAILS = ["ai-plans", "ai-chat", "ai-work", "ai-create", "ai-coding", "ai-income"] as const;
export const AI_HUB_NEWS = "ai-news";
const PER_RAIL = 4;
const NEWS_ROWS = 6;

export type AiHubRail = { topic: GuideTopic; articles: GuideSummary[] };

export async function loadAiHubRails(locale: Locale, topics: readonly GuideTopic[]) {
  const known = (slug: string) => topics.find((topic) => topic.slug === slug && (topic.count === undefined || topic.count > 0));
  const wanted = AI_HUB_RAILS.flatMap((slug) => {
    const topic = known(slug);
    return topic ? [topic] : [];
  });
  const news = known(AI_HUB_NEWS);
  const [lists, newsList] = await Promise.all([
    Promise.all(wanted.map((topic) => getGuideList(locale, { kind: "life", topic: topic.slug, sort: "curated" }, PER_RAIL))),
    news ? getGuideList(locale, { kind: "life", topic: news.slug, sort: "news" }, NEWS_ROWS) : Promise.resolve(null),
  ]);
  return {
    rails: wanted.map((topic, index) => ({ topic, articles: lists[index].articles })).filter((rail) => rail.articles.length),
    news: news && newsList?.articles.length ? { topic: news, articles: newsList.articles } : null,
  };
}

export function AiHubRails({ rails, news, labels }: {
  rails: readonly AiHubRail[];
  news: AiHubRail | null;
  labels: { heading: string; seeAll: string; cards: { intel: string; howto: string; life: string } };
}) {
  if (!rails.length && !news) return null;
  return (
    <section aria-labelledby="ai-hub-rails" className="mt-10" data-testid="ai-hub-rails">
      <h2 id="ai-hub-rails" className="portal-section-heading text-2xl font-extrabold tracking-tight">{labels.heading}</h2>
      <nav aria-label={labels.heading} className="portal-scroll-strip mt-4 flex items-center gap-2 sm:flex-wrap sm:overflow-visible">
        {[...(news ? [news] : []), ...rails].map((rail) => (
          <a
            key={rail.topic.slug}
            href={`#rail-${rail.topic.slug}`}
            className="inline-flex min-h-11 shrink-0 snap-start items-center whitespace-nowrap rounded-full border border-[var(--line)] bg-[var(--surface)] px-4 text-sm font-semibold text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
          >
            {rail.topic.label}
          </a>
        ))}
      </nav>
      {news ? (
        <Rail rail={news} seeAll={labels.seeAll}>
          <NewsList articles={news.articles} className="mt-4" />
        </Rail>
      ) : null}
      {rails.map((rail) => (
        <Rail key={rail.topic.slug} rail={rail} seeAll={labels.seeAll}>
          <ul className="mt-4 grid gap-4 sm:grid-cols-2">
            {rail.articles.map((article) => (
              <GuideCard key={`${article.kind}:${article.slug}`} article={article} labels={labels.cards} />
            ))}
          </ul>
        </Rail>
      ))}
    </section>
  );
}

function Rail({ rail, seeAll, children }: { rail: AiHubRail; seeAll: string; children: React.ReactNode }) {
  const id = `rail-${rail.topic.slug}`;
  return (
    <section id={id} aria-labelledby={`${id}-title`} className="mt-10 scroll-mt-24">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] pb-2.5">
        <h3 id={`${id}-title`} className="portal-section-heading text-xl font-extrabold tracking-tight">{rail.topic.label}</h3>
        <Link
          href={guideTopicHref("life", rail.topic.slug)}
          className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] bg-[var(--surface)] px-4 text-sm font-semibold text-[var(--teal)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]"
        >
          {seeAll}
        </Link>
      </div>
      {rail.topic.description ? <p className="mt-2.5 max-w-2xl leading-7 text-[var(--muted)]">{rail.topic.description}</p> : null}
      {children}
    </section>
  );
}
