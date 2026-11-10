import { GuideCard, type GuideCardLabels } from "./card";
import { NewsDesk } from "./news-desk";
import { NewsList } from "./news-list";
import { type GuideSummary, type GuideTopic } from "@/lib/guides";
import { LIFE_NEWS_PREVIEW, lifeDiscoveryCopy } from "@/lib/life-discovery";

export function LifeReadingJumps({ locale, news, knowledge }: { locale: string; news: boolean; knowledge: boolean }) {
  if (!news && !knowledge) return null;
  const copy = lifeDiscoveryCopy(locale);
  return <nav aria-label={copy.jumpLabel} className="mt-6 flex flex-wrap gap-3" data-testid="life-reading-jumps">
    {news ? <a className="inline-flex min-h-11 items-center rounded-full bg-[var(--teal)] px-5 py-2 font-semibold text-white underline-offset-4 hover:underline" href="#life-news">{copy.jumpNews}</a> : null}
    {knowledge ? <a className="inline-flex min-h-11 items-center rounded-full border border-[var(--teal)] px-5 py-2 font-semibold text-[var(--teal)] underline-offset-4 hover:underline" href="#life-knowledge">{copy.jumpKnowledge}</a> : null}
  </nav>;
}

/** The hub still holds all twenty stories in their original order. Native details remains
 * operable without hydration or JavaScript, and only the first list has a lead story. */
export function LifeNewsPreview({ articles, topics, topicsLabel, locale }: {
  articles: readonly GuideSummary[]; topics: readonly GuideTopic[]; topicsLabel: string; locale: string;
}) {
  const rest = articles.slice(LIFE_NEWS_PREVIEW);
  const copy = lifeDiscoveryCopy(locale);
  return <>
    <NewsDesk articles={articles.slice(0, LIFE_NEWS_PREVIEW)} topics={topics} topicsLabel={topicsLabel} />
    {rest.length ? <details className="mt-5 rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 sm:px-5" data-testid="life-more-news">
      <summary className="min-h-14 cursor-pointer py-4 font-semibold text-[var(--teal)]">{copy.moreNews.replace("{count}", String(rest.length))}</summary>
      <NewsList articles={rest} start={LIFE_NEWS_PREVIEW + 1} titleTag="h3" className="min-w-0" />
    </details> : null}
  </>;
}

export function LifeKnowledge({ articles, labels, locale }: {
  articles: readonly GuideSummary[]; labels: GuideCardLabels; locale: string;
}) {
  if (!articles.length) return null;
  const copy = lifeDiscoveryCopy(locale);
  return <section id="life-knowledge" aria-labelledby="life-knowledge-heading" className="mt-10 scroll-mt-36" data-testid="life-knowledge">
    <h2 id="life-knowledge-heading" className="text-2xl font-bold tracking-tight">{copy.knowledgeTitle}</h2>
    <p className="mt-2 max-w-2xl leading-7 text-[var(--muted)]">{copy.knowledgeIntro}</p>
    <ul className="mt-4 grid gap-3 md:grid-cols-3">
      {articles.map((article) => <GuideCard key={`${article.kind}:${article.slug}`} article={article} variant="compact"
        labels={{ ...labels, life: article.topics.find((topic) => topic.parent)?.label ?? article.topics[0]?.label ?? copy.knowledgeLabel }} />)}
    </ul>
  </section>;
}
