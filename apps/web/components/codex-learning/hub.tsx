"use client";

import { Suspense, useSyncExternalStore } from "react";
import { useSearchParams } from "next/navigation";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { learningCopy } from "@/lib/codex-learning/copy";
import { filterLessons, type LearningEntry } from "@/lib/codex-learning";
import { commandEntries } from "@/lib/codex-learning/commands";
import { emptyFilters, learningFilterUrl, readLearningFilters, type LearningFilters } from "@/lib/codex-learning/filters";
import { depthCopy, learningUnits } from "@/lib/codex-learning/units";

const subscribe = () => () => {};
type HubProps = { entries: LearningEntry[]; locale: Locale; available: boolean };

export function LearningHub(props: HubProps) {
  return <Suspense fallback={<p aria-busy="true">{learningCopy(props.locale).title}</p>}><FilteredHub {...props} /></Suspense>;
}

function FilteredHub({ entries, locale, available }: HubProps) {
  const c = learningCopy(locale);
  const d = depthCopy(locale);
  const units = learningUnits(locale);
  // Prevent a fast first keystroke being lost before React hydrates the server-rendered hub.
  const interactive = useSyncExternalStore(subscribe, () => true, () => false);
  const search = useSearchParams();
  const filters = readLearningFilters(search.toString());
  const { q: query, level, platform, goal, unit } = filters;
  function update(patch: Partial<LearningFilters>, replace = false) {
    const current = readLearningFilters(window.location.search);
    const url = learningFilterUrl(window.location.href, { ...current, ...patch });
    if (replace) window.history.replaceState(null, "", url);
    else window.history.pushState(null, "", url);
  }
  const results = filterLessons(entries, query, level, platform, goal, unit);
  const unpublishedStatus = (entry: LearningEntry) => available ? (entry.ready ? c.unpublished : c.planned) : c.unavailable;
  const field = "mt-1 min-h-11 w-full rounded-lg border border-[var(--line)] bg-[var(--paper)] px-3";
  return <section aria-label={c.title} className="my-8 space-y-6">
    <details className="rounded-xl border border-[var(--line)] p-4">
      <summary className="min-h-11 cursor-pointer font-semibold">{d.order}</summary>
      <div className="grid gap-2 sm:grid-cols-2">{units.map((item) => <button disabled={!interactive} type="button" key={item.id} aria-pressed={unit === item.id} onClick={() => update({ unit: item.id })} className="min-h-11 rounded-lg border border-[var(--line)] p-3 text-left aria-pressed:bg-[var(--paper)]">{item.id} · {item.title}</button>)}</div>
    </details>
    <label className="block font-medium">{c.search}<input disabled={!interactive} maxLength={200} type="search" value={query} onChange={(e) => update({ q: e.target.value }, true)} className={field} /></label>
    <div className="grid gap-3 sm:grid-cols-2">
      {([{ key: "level", label: c.level, options: c.levels }, { key: "platform", label: c.platform, options: c.platforms }, { key: "goal", label: c.goal, options: c.goals }] as const).map(({ key, label, options }) => <label key={key} className="text-sm">{label}<select disabled={!interactive} className={field} value={filters[key]} onChange={(e) => update({ [key]: e.target.value })}><option value="">{c.all}</option>{options.map((text, i) => <option key={i} value={String(i)}>{text}</option>)}</select></label>)}
      <label className="text-sm">{d.unit}<select disabled={!interactive} className={field} value={unit} onChange={(e) => update({ unit: e.target.value })}><option value="">{c.all}</option>{units.map((item) => <option key={item.id} value={item.id}>{item.id} · {item.title}</option>)}</select></label>
    </div>
    <button disabled={!interactive} type="button" className="min-h-11 underline" onClick={() => update(emptyFilters)}>{c.clear}</button>
    {!available && <p role="status">{c.unavailable}</p>}
    <p role="status" aria-live="polite" className="sr-only">{c.filtered}</p>
    {!results.length && <p>{c.empty}</p>}
    <ol className="grid gap-4">
      {results.map((entry) => <li key={entry.slug} className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5">
        <p className="mb-2 text-xs text-[var(--muted)]">{entry.unit} · {c.levels[entry.level]} · {d.read} {entry.minutes} {c.minutes}{entry.operationMinutes && <> · {d.practice} {entry.operationMinutes} {c.minutes}</>}</p>
        <h2 className="text-lg font-semibold">{entry.published ? <Link href={`/life/${entry.slug}`} className="text-[var(--teal)] underline">{entry.title}</Link> : entry.title}</h2>
        <p className="mt-2 leading-7">{entry.description}</p>
        <p className="mt-3 text-sm text-[var(--muted)]">{entry.platforms.map((p) => c.platforms[p]).join(" · ")}</p>
        {entry.published ? <p className="mt-2 text-xs">{c.updated}: {entry.updated}</p> : <p className="mt-2 text-sm">{unpublishedStatus(entry)}</p>}
      </li>)}
    </ol>
    <section aria-label={c.commands} className="border-t border-[var(--line)] pt-6">
      <h2 className="text-xl font-bold">{c.commands}</h2>
      <ul className="mt-3 space-y-3">{commandEntries(locale).filter((item) => {
        const row = entries.find((entry) => entry.id === item.lesson);
        return row && filterLessons([row], "", level, platform, goal, unit).length
          && query.normalize("NFKC").toLowerCase().trim().split(/\s+/).every((term) => `${item.example} ${item.purpose} ${item.surface} ${row.title}`.normalize("NFKC").toLowerCase().includes(term));
      }).map((item) => {
        const row = entries.find((entry) => entry.id === item.lesson)!;
        return <li key={item.example} className="min-w-0 rounded-xl border border-[var(--line)] p-4">
          <p>{item.purpose} · <span className="text-sm text-[var(--muted)]">{item.surface}</span></p>
          <pre className="mt-2 overflow-x-auto text-sm"><code>{item.example}</code></pre>
          {row.published ? <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/life/${row.slug}`}>{row.title}</Link> : <span>{row.title} · {unpublishedStatus(row)}</span>}
        </li>;
      })}</ul>
    </section>
  </section>;
}
