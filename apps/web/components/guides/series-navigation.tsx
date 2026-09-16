import type { ArticleReference, SeriesNavigation } from "@/lib/guide-series";
import { platformLabel, seriesCopy } from "@/lib/guide-series-copy";
import { guideHref } from "@/lib/guides";

function ArticleLink({ target, locale, prefix }: { target: ArticleReference; locale: string; prefix?: string }) {
  return <a className="inline-flex min-h-11 items-center text-[var(--teal)] underline underline-offset-4" href={`/${locale}${guideHref(target.kind, target.slug)}`}>{prefix ? `${prefix}：` : ""}{target.title}</a>;
}
export function SeriesStart({ series, locale }: { series: SeriesNavigation; locale: string }) {
  const copy = seriesCopy(locale);
  return <div className="space-y-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
    <ArticleLink target={series.hub} locale={locale} prefix={copy.back} />
    {series.current ? <p className="text-sm text-[var(--muted)]">{String(series.current.number).padStart(2, "0")} · {copy[series.current.level as "beginner" | "intermediate" | "advanced"] ?? series.current.level} · {series.current.platforms.map(platformLabel).join(" / ")}</p> : null}
    {series.prerequisites.length ? <div><h2 className="text-sm font-semibold">{copy.prerequisites}</h2>
      <ul>{series.prerequisites.map(target => <li key={target.slug}><ArticleLink target={target} locale={locale} /></li>)}</ul>
    </div> : null}
  </div>;
}
export function SeriesEnd({ series, locale }: { series: SeriesNavigation; locale: string }) {
  const copy = seriesCopy(locale);
  // Previous and next as two columns, each a box a thumb can land on; the way back to the
  // directory sits beneath them rather than between, where it split the pair.
  const box = "rounded-2xl border border-[var(--line)] bg-[var(--paper)] px-4 py-3";
  return <section className="space-y-5 border-t border-[var(--line)] pt-8">
    <nav aria-label={series.hub.title} className="grid gap-3 sm:grid-cols-2">
      <div className={box}>{series.previous ? <ArticleLink target={series.previous} locale={locale} prefix={copy.previous} /> : null}</div>
      <div className={`${box} sm:text-right`}>{series.next ? <ArticleLink target={series.next} locale={locale} prefix={copy.next} /> : null}</div>
    </nav>
    <p><a href={`/${locale}${guideHref(series.hub.kind, series.hub.slug)}`} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{copy.back}</a></p>
    {series.related.length ? <div><h2 className="text-lg font-semibold">{copy.related}</h2><ul>
      {series.related.slice(0, 3).map(target => <li key={target.slug}><ArticleLink target={target} locale={locale} /></li>)}
    </ul></div> : null}
  </section>;
}
