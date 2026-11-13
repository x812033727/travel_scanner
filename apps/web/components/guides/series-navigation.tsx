import type { ArticleReference, SeriesNavigation } from "@/lib/guide-series";
import { platformLabel, seriesCopy } from "@/lib/guide-series-copy";
import { guideHref } from "@/lib/guides";

function ArticleLink({ target, locale, prefix }: { target: ArticleReference; locale: string; prefix?: string }) {
  return <a className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline underline-offset-4 hover:text-[var(--teal-dark)]" href={`/${locale}${guideHref(target.kind, target.slug)}`}>{prefix ? `${prefix}：` : ""}{target.title}</a>;
}
export function SeriesStart({ series, locale }: { series: SeriesNavigation; locale: string }) {
  const copy = seriesCopy(locale);
  return <div className="portal-hero-shell space-y-2 rounded-2xl p-4 sm:p-5">
    <ArticleLink target={series.hub} locale={locale} prefix={copy.back} />
    {series.current ? <p className="text-sm font-medium text-[var(--muted)]">{copy[series.current.level as "beginner" | "intermediate" | "advanced"] ?? series.current.level} · {series.current.platforms.map(platformLabel).join(" / ")}</p> : null}
    {series.prerequisites.length ? <div><h2 className="text-sm font-semibold">{copy.prerequisites}</h2>
      <ul>{series.prerequisites.map(target => <li key={target.slug}><ArticleLink target={target} locale={locale} /></li>)}</ul>
    </div> : null}
  </div>;
}
export function SeriesEnd({ series, locale }: { series: SeriesNavigation; locale: string }) {
  const copy = seriesCopy(locale);
  // Previous and next as two columns, each a box a thumb can land on; the way back to the
  // directory sits beneath them rather than between, where it split the pair.
  const activeBox = "portal-card-surface rounded-2xl px-4 py-3.5";
  const emptyBox = "hidden sm:block";
  return <section className="space-y-5 border-t border-[var(--line)] pt-8">
    <nav aria-label={series.hub.title} className="grid gap-3.5 sm:grid-cols-2">
      <div className={series.previous ? activeBox : emptyBox}>{series.previous ? <ArticleLink target={series.previous} locale={locale} prefix={copy.previous} /> : null}</div>
      <div className={series.next ? `${activeBox} sm:text-right` : emptyBox}>{series.next ? <ArticleLink target={series.next} locale={locale} prefix={copy.next} /> : null}</div>
    </nav>
    <p><a href={`/${locale}${guideHref(series.hub.kind, series.hub.slug)}`} className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] bg-[var(--surface)] px-4 text-sm font-semibold text-[var(--teal)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]">{copy.back}</a></p>
    {series.related.length ? <div><h2 className="portal-section-heading text-lg font-bold tracking-tight">{copy.related}</h2><ul className="mt-2">
      {series.related.slice(0, 3).map(target => <li key={target.slug}><ArticleLink target={target} locale={locale} /></li>)}
    </ul></div> : null}
  </section>;
}
