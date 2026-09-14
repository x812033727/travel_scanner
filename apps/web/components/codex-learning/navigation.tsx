import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { HUB_SLUG, type LearningEntry } from "@/lib/codex-learning";
import { learningCopy } from "@/lib/codex-learning/copy";
import { depthCopy } from "@/lib/codex-learning/units";

export function LearningNavigation({ slug, locale, entries, hubPublished, compact = false }: {
  slug: string; locale: Locale; entries: LearningEntry[]; hubPublished: boolean; compact?: boolean;
}) {
  const c = learningCopy(locale);
  const d = depthCopy(locale);
  const current = entries.find((row) => row.slug === slug);
  if (!current) return null;
  const route = entries.filter((row) => row.unit === current.unit).sort((a, b) => a.order - b.order);
  const position = route.findIndex((row) => row.slug === slug);
  const previous = position > 0 ? route[position - 1] : null;
  const next = position >= 0 ? route[position + 1] : null;
  const related = entries.filter((row) => current.related.includes(row.id) && row.published);
  const prerequisites = current.prerequisites.map((id) => entries.find((row) => row.id === id)).filter((row): row is LearningEntry => Boolean(row));
  const entryLabel = (row: LearningEntry, prefix = "") => row.published
    ? <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/life/${row.slug}`}>{prefix}{row.title}</Link>
    : <span className="inline-flex min-h-11 items-center">{prefix}{row.title} · {row.ready ? c.unpublished : c.planned}</span>;
  return <nav aria-label={compact ? c.back : c.related} className="my-6 space-y-3 rounded-xl border border-[var(--line)] p-4">
    {hubPublished && <Link href={`/life/${HUB_SLUG}`} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">← {c.back}</Link>}
    {!compact && <>
      <div className="flex flex-wrap justify-between gap-3">{previous && entryLabel(previous, `${c.previous}: `)}{next && entryLabel(next, `${c.next}: `)}</div>
      {prerequisites.length > 0 && <><p className="font-semibold">{d.prerequisites}</p><ul>{prerequisites.map((row) => <li key={row.slug}>{entryLabel(row)}</li>)}</ul></>}
      {related.length > 0 && <><p className="font-semibold">{c.related}</p><ul>{related.map((row) => <li key={row.slug}><Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/life/${row.slug}`}>{row.title}</Link></li>)}</ul></>}
    </>}
  </nav>;
}
