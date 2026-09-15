import type { GeminiSeriesCopy } from "@/lib/gemini-series-copy";
import { visibleGeminiHref, visibleGeminiNavigation, type VisibleGeminiSeries } from "@/lib/gemini-series-projection";

const link = "inline-flex min-h-11 min-w-0 items-center text-[var(--teal)] underline underline-offset-4 [overflow-wrap:anywhere]";

export function GeminiNavigation({ series, number, position, copy }: { series: VisibleGeminiSeries; number: number; position: "top" | "bottom"; copy: GeminiSeriesCopy }) {
  const navigation = visibleGeminiNavigation(series, number);
  if (!navigation) return null;
  const { current, previous, next, related, prerequisites } = navigation;
  const group = series.groups.find(entry => entry.id === current.group);
  return <nav aria-label={position === "top" ? copy.navigation : copy.continue} className="min-w-0 space-y-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 [overflow-wrap:anywhere]">
    <a href={visibleGeminiHref(series, series.hubSlug)} className={link}>{copy.back}</a>
    <p className="text-sm text-[var(--muted)]">{group?.title} · {copy.position.replace("{number}", String(current.number)).replace("{total}", String(series.articles.length))}</p>
    {position === "top" && prerequisites.length ? <div><p className="font-semibold">{copy.prerequisites}</p><ul>{prerequisites.map(entry => <li key={entry.slug}><a className={link} href={visibleGeminiHref(series, entry.slug)}>{entry.title}</a></li>)}</ul></div> : null}
    {position === "bottom" ? <>
      <div className="grid min-w-0 gap-3 sm:grid-cols-2">
        {previous ? <a className={link} rel="prev" href={visibleGeminiHref(series, previous.slug)}>{copy.previous}{previous.title}</a> : <span />}
        {next ? <a className={link} rel="next" href={visibleGeminiHref(series, next.slug)}>{copy.next}{next.title}</a> : null}
      </div>
      <p className="font-semibold">{copy.related}</p>
      <ul>{related.map(entry => <li key={entry.slug}><a href={visibleGeminiHref(series, entry.slug)} className={link}>{entry.title}</a></li>)}</ul>
    </> : null}
  </nav>;
}
