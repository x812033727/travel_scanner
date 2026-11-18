import { Link } from "@/i18n/navigation";
import { guideHref, visibleGuideHero, type GuideSummary } from "@/lib/guides";
import { GuideImage } from "./guide-image";

function LeadRow({ article, heading: Heading, showTopic }: {
  article: GuideSummary;
  heading: "h3" | "h4";
  showTopic: boolean;
}) {
  const hero = visibleGuideHero(article.hero);
  return (
    <li className="py-2">
      <Link href={guideHref(article.kind, article.slug)} aria-label={article.title}
        className={`group grid min-w-0 gap-3 rounded-xl bg-[var(--teal-soft)] p-4 text-[var(--ink)] outline-offset-2 [overflow-wrap:anywhere] sm:p-5 ${hero ? "sm:grid-cols-[minmax(0,1fr)_11rem] sm:items-center" : ""}`}>
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2 text-sm font-semibold text-[var(--teal-dark)]">
            <time dateTime={article.news_date ?? undefined} className="tabular-nums">{article.news_date}</time>
            {showTopic && article.topics[0] ? <span>{article.topics[0].label}</span> : null}
          </div>
          <Heading className="mt-1 text-xl font-extrabold leading-snug tracking-tight underline-offset-4 group-hover:underline group-focus-visible:underline sm:text-2xl">
            {article.title}
          </Heading>
          {article.description ? (
            <p className="mt-2 line-clamp-3 text-sm leading-6 text-[var(--ink)]">{article.description}</p>
          ) : null}
        </div>
        {hero ? (
          <GuideImage src={hero.src} alt="" width={hero.width} height={hero.height} loading="lazy" decoding="async"
            className="aspect-video w-full rounded-lg object-contain" />
        ) : null}
      </Link>
    </li>
  );
}

/**
 * A compact chronological wire. A section can give its first dated story a headline and
 * summary, while keeping the remaining rows short enough to scan on a phone.
 *
 * The date is `news_date`, never the publication or update time: stories are imported in
 * batches, so a whole week publishes in the same minute and corrections move `updated_at`.
 * A row without one (a news topic's evergreen piece, such as a sources list) keeps its line
 * with an empty date column; the API already sorts those after the dated stories.
 *
 * The rows are in the order given. The list is an `<ol>` because that order means something,
 * but it prints no numbers: a position in a list that grows every day is not worth reading.
 */
export function NewsList({
  articles,
  className = "mt-4",
  leadHeading,
  showTopic = false,
  showDescription = false,
}: {
  articles: readonly GuideSummary[];
  className?: string;
  leadHeading?: "h3" | "h4";
  showTopic?: boolean;
  showDescription?: boolean;
}) {
  if (!articles.length) return null;
  return (
    <ol
      className={`${className} divide-y divide-[var(--line)] rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-1.5 shadow-[var(--shadow-sm)]`}
      data-testid="news-list"
    >
      {articles.map((article, index) => leadHeading && index === 0 && article.news_date ? (
        <LeadRow key={`${article.kind}:${article.slug}`} article={article} heading={leadHeading} showTopic={showTopic} />
      ) : (
        <li
          key={`${article.kind}:${article.slug}`}
          className="group relative -mx-2 grid gap-x-4 rounded-xl px-2 py-1.5 transition-colors hover:bg-[var(--paper)]/75 sm:grid-cols-[7rem_minmax(0,1fr)] sm:items-baseline"
        >
          {article.news_date ? (
            <time
              dateTime={article.news_date}
              className="pt-1 font-mono text-[length:var(--text-meta)] font-medium tabular-nums text-[var(--muted)] sm:pt-0"
            >
              {article.news_date}
            </time>
          ) : (
            <span aria-hidden="true" className="hidden sm:block" />
          )}
          <div className="min-w-0">
            <div className="flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
              {showTopic && article.topics[0] ? (
                <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[length:var(--text-xs)] font-semibold text-[var(--teal-dark)]">
                  {article.topics[0].label}
                </span>
              ) : null}
              <Link
                href={guideHref(article.kind, article.slug)}
                className="inline-flex min-h-11 min-w-0 items-center font-medium leading-7 text-[var(--ink)] underline-offset-4 [overflow-wrap:anywhere] after:absolute after:inset-0 group-hover:text-[var(--teal)] group-hover:underline focus-visible:underline"
              >
                {article.title}
              </Link>
            </div>
            {showDescription && article.description ? (
              <p className="mb-1.5 line-clamp-2 text-sm leading-6 text-[var(--muted)]">{article.description}</p>
            ) : null}
          </div>
        </li>
      ))}
    </ol>
  );
}
