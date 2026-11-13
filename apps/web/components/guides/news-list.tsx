import { Link } from "@/i18n/navigation";
import { guideHref, type GuideSummary } from "@/lib/guides";

/**
 * News as a list, one story per line: the day the news happened, then the title as a link.
 * No hero, no description, no badge -- a reader scanning news wants what happened and when,
 * and a column of dates is what makes "newest first" visible at a glance.
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
  showTopic = false,
  showDescription = false,
}: {
  articles: readonly GuideSummary[];
  className?: string;
  showTopic?: boolean;
  showDescription?: boolean;
}) {
  if (!articles.length) return null;
  return (
    <ol
      className={`${className} divide-y divide-[var(--line)] rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-1.5 shadow-[var(--shadow-sm)]`}
      data-testid="news-list"
    >
      {articles.map((article) => (
        <li
          key={`${article.kind}:${article.slug}`}
          className="-mx-2 grid gap-x-4 rounded-xl px-2 py-1.5 transition-colors hover:bg-[var(--paper)]/75 sm:grid-cols-[7rem_minmax(0,1fr)] sm:items-baseline"
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
                className="inline-flex min-h-11 min-w-0 items-center font-medium leading-7 text-[var(--ink)] underline-offset-4 [overflow-wrap:anywhere] hover:text-[var(--teal)] hover:underline"
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
