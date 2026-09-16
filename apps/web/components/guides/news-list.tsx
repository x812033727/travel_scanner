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
export function NewsList({ articles, className = "mt-4" }: { articles: readonly GuideSummary[]; className?: string }) {
  if (!articles.length) return null;
  return (
    <ol className={`${className} divide-y divide-[var(--line)] border-y border-[var(--line)]`} data-testid="news-list">
      {articles.map((article) => (
        <li
          key={`${article.kind}:${article.slug}`}
          className="grid gap-x-4 py-1.5 sm:grid-cols-[6.5rem_minmax(0,1fr)] sm:items-baseline"
        >
          {article.news_date ? (
            <time
              dateTime={article.news_date}
              className="pt-1 text-[length:var(--text-meta)] tabular-nums text-[var(--muted)] sm:pt-0"
            >
              {article.news_date}
            </time>
          ) : (
            <span aria-hidden="true" className="hidden sm:block" />
          )}
          <Link
            href={guideHref(article.kind, article.slug)}
            className="inline-flex min-h-11 min-w-0 items-center leading-7 text-[var(--teal)] underline-offset-4 [overflow-wrap:anywhere] hover:underline"
          >
            {article.title}
          </Link>
        </li>
      ))}
    </ol>
  );
}
