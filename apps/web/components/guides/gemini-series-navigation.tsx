import { geminiCopy as copy, geminiSeries, seriesArticle, seriesHref, type SeriesArticle } from "@/lib/gemini-series";

const link = "inline-flex min-h-11 items-center text-[var(--teal)] underline underline-offset-4";

export function SeriesNavigation({ article, position }: { article: SeriesArticle; position: "top" | "bottom" }) {
  const group = geminiSeries.groups.find((entry) => entry.id === article.group);
  const previous = seriesArticle(article.number - 1);
  const next = seriesArticle(article.number + 1);
  const related = article.related.map(seriesArticle).filter((entry) => entry !== undefined);
  const prerequisites = article.prerequisites.map(seriesArticle).filter((entry): entry is SeriesArticle => entry !== undefined && entry.number !== article.number);
  return <nav aria-label={position === "top" ? copy.navigation : copy.continue} className="space-y-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
    <a href={seriesHref(geminiSeries.hubSlug)} className={link}>{copy.back}</a>
    <p className="text-sm text-[var(--muted)]">{group?.title} · {copy.position.replace("{number}", String(article.number)).replace("{total}", String(geminiSeries.articles.length))}</p>
    {position === "top" && prerequisites.length ? <div><p className="font-semibold">{copy.prerequisites}</p><ul>{prerequisites.map((entry) => <li key={entry.slug}><a className={link} href={seriesHref(entry.slug)}>{entry.title}</a></li>)}</ul></div> : null}
    {position === "bottom" ? <>
      <div className="grid gap-3 sm:grid-cols-2">
        {previous ? <a className={link} rel="prev" href={seriesHref(previous.slug)}>{copy.previous}{previous.title}</a> : <span />}
        {next ? <a className={link} rel="next" href={seriesHref(next.slug)}>{copy.next}{next.title}</a> : null}
      </div>
      <p className="font-semibold">{copy.related}</p>
      <ul>{related.map((entry) => <li key={entry.slug}><a href={seriesHref(entry.slug)} className={link}>{entry.title}</a></li>)}</ul>
    </> : null}
  </nav>;
}
