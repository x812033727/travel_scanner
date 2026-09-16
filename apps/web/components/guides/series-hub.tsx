"use client";

import { useSyncExternalStore } from "react";
import { filterSeries, readSeriesFilters, type GuideSeries, type SeriesFilters } from "@/lib/guide-series";
import { platformLabel, seriesCopy } from "@/lib/guide-series-copy";
import { guideHref } from "@/lib/guides";

function subscribe(listener: () => void) {
  window.addEventListener("popstate", listener);
  window.addEventListener("guide-series-filter", listener);
  return () => {
    window.removeEventListener("popstate", listener);
    window.removeEventListener("guide-series-filter", listener);
  };
}
const snapshot = () => window.location.search;
const serverSnapshot = () => "";

export function SeriesHub({ series }: { series: GuideSeries }) {
  // Keep the complete published directory visible in the server HTML, including with
  // JavaScript disabled. Enhance it with URL filters after hydration, without suspending
  // the catalogue behind a client-only fallback.
  const search = useSyncExternalStore(subscribe, snapshot, serverSnapshot);
  const filters = readSeriesFilters(new URLSearchParams(search));
  const copy = seriesCopy(series.locale);
  const entries = filterSeries(series, filters);
  const selectedPath = series.paths.find(path => path.id === filters.path);
  const groups = selectedPath ? [{ id: "path", title: selectedPath.title, entries }]
    : series.groups.map(group => ({ ...group, entries: entries.filter(entry => entry.group === group.id) }));
  function change(key: keyof SeriesFilters, value: string) {
    const url = new URL(window.location.href);
    if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
    window.history.replaceState(null, "", url.pathname + url.search + url.hash);
    window.dispatchEvent(new Event("guide-series-filter"));
  }
  function clear() {
    window.history.replaceState(null, "", window.location.pathname);
    window.dispatchEvent(new Event("guide-series-filter"));
  }
  const control = "min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 py-2";
  return <section className="min-w-0 space-y-7" aria-label={copy.hub}>
    <div className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5">
      <h2 className="text-xl font-semibold">{copy.paths}</h2>
      <div className="mt-3 flex flex-wrap gap-2">
        {series.paths.map(path => <button key={path.id} type="button" aria-pressed={filters.path === path.id}
          onClick={() => change("path", filters.path === path.id ? "" : path.id)}
          className="min-h-11 rounded-full border border-[var(--line)] px-4 text-sm aria-pressed:bg-[var(--teal)] aria-pressed:text-white">{path.title}</button>)}
      </div>
    </div>
    <div className="grid gap-4 sm:grid-cols-3">
      <label className="grid gap-2 sm:col-span-3">{copy.search}
        <input type="search" maxLength={200} className={control} value={filters.q} onChange={event => change("q", event.target.value)} />
      </label>
      <label className="grid gap-2">{copy.group}<select aria-label={copy.group} className={control} value={filters.group} onChange={e => change("group", e.target.value)}>
        <option value="">{copy.all}</option>{series.groups.map(group => <option key={group.id} value={group.id}>{group.title}</option>)}
      </select></label>
      <label className="grid gap-2">{copy.level}<select aria-label={copy.level} className={control} value={filters.level} onChange={e => change("level", e.target.value)}>
        <option value="">{copy.all}</option>{(["beginner", "intermediate", "advanced"] as const).map(level => <option key={level} value={level}>{copy[level]}</option>)}
      </select></label>
      <label className="grid gap-2">{copy.platform}<select aria-label={copy.platform} className={control} value={filters.platform} onChange={e => change("platform", e.target.value)}>
        <option value="">{copy.all}</option>{Array.from(new Set(series.entries.flatMap(entry => entry.platforms))).map(platform => <option key={platform} value={platform}>{platformLabel(platform)}</option>)}
      </select></label>
    </div>
    <div className="flex flex-wrap items-center justify-between gap-3">
      <p role="status" aria-live="polite" className="sr-only">{copy.filtered}</p>
      <button type="button" onClick={clear} className="min-h-11 rounded-xl border border-[var(--line)] px-4">{copy.clear}</button>
    </div>
    {!entries.length ? <p className="rounded-2xl border border-[var(--line)] p-6">{copy.empty}</p> : null}
    {groups.filter(group => group.entries.length > 0).map(group => <section key={group.id} className="space-y-3">
      <h2 className="text-xl font-bold">{group.id !== "path" ? `${group.id}．` : ""}{group.title}</h2>
      <ol className="grid gap-3 sm:grid-cols-2">
        {group.entries.map(entry => <li key={entry.slug} className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-5">
          <a href={`/${series.locale}${guideHref(entry.kind, entry.slug)}`} className="block text-lg font-semibold text-[var(--teal)] underline-offset-4 hover:underline">
            {entry.title}
          </a>
          <p className="mt-2 text-sm leading-7 text-[var(--muted)]">{entry.description.includes("。") ? `${entry.description.split("。")[0]}。` : entry.description}</p>
          <p className="mt-3 text-xs leading-6">{copy[entry.level as "beginner" | "intermediate" | "advanced"] ?? entry.level} · {entry.minutes} {copy.minutes}</p>
          <ul className="mt-2 flex flex-wrap gap-2">{entry.platforms.map(platform => <li key={platform} className="rounded-full bg-[var(--paper)] px-2 py-1 text-xs">{platformLabel(platform)}</li>)}</ul>
        </li>)}
      </ol>
    </section>)}
  </section>;
}
