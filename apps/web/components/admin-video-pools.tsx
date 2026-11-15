"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { AdminEmptyState, AdminErrorState, AdminFilterBar, AdminSkeleton, AdminStatusPill } from "@/components/admin-ui";
import { Button } from "@/components/community/ui";
import { updateAdminQuery, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { videoPoolsCopy, videoPoolsText } from "@/lib/video-pools-copy";

const SERIES = ["curio", "so-thats-why"] as const;
const VIEWS = ["themes", "published", "expansions"] as const;
const EPISODE_STATUSES = ["published", "unpublished", "all"] as const;
const STATUSES = ["producible", "reserve", "short", "all"] as const;
const DIMS = ["click", "hook", "surprise", "payoff", "share"] as const;
const MIN_SCORES = ["6.5", "7", "7.5", "8"] as const;
type Series = (typeof SERIES)[number];
type Copy = ReturnType<typeof videoPoolsCopy>;
type Verdict = keyof Copy["verdicts"];
export type PoolAudience = {
  score: number; rank: number; of: number; click: number; hook: number; surprise: number; payoff: number; share: number;
  comment: string; reviewed_on: string; rounds: { score: number; comment: string; changes: string; reviewed_on: string }[];
};
export type PoolTheme = {
  id: string; title: string; category: string | null; core_question: string; target_minutes: number; long: boolean; producible: boolean;
  material: { verdict: Exclude<Verdict, "none">; missing: string | null } | null; candidates: number; audience: PoolAudience | null;
};
export type PoolThemeDetail = PoolTheme & {
  chapters: { title: string; seconds: number; new_information: string }[]; boredom_risk: string; drop_if: string; evidence_gaps: string;
};
export type PoolOverview = { series: { key: Series; name: string; revision: string; audience_min: number; themes_sha256: string; counts: Record<keyof Copy["counts"] | "raw_records" | "themes" | "long_themes", number> }[] };
export type PoolThemePage = { items: PoolTheme[]; total: number; page: number; page_size: number; categories: { category: string; count: number }[] };
export type PoolEpisode = {
  key: string; code: string | null; title: string; category: string | null; slugs: string[]; candidate_ids: string[];
  published: boolean; youtube_id: string | null; youtube_url: string | null; youtube_source: "site" | "catalog" | null;
  site_slug: string | null; publish_at: string | null; stage: string | null; dropped: boolean; privacy: string | null;
};
export type PoolEpisodePage = { items: PoolEpisode[]; total: number; published: number; unpublished: number };
export type PoolExpansions = {
  expansions: { batch_id: string; created_on: string | null; scope: string; candidates: number; selected: number; not_added: number; sources: number }[];
  checkpoints: { name: string; revision: string | null; selected: number | null; raw: number | null }[];
};
const PAGE_SIZE = 25;
const oneOf = (values: readonly string[]) => (value: string) => values.includes(value);
const isSeries = oneOf(SERIES);
const isView = oneOf(VIEWS);
const isEpisodeStatus = oneOf(EPISODE_STATUSES);
const isStatus = oneOf(STATUSES);
const isMinScore = oneOf(MIN_SCORES);
const isPage = (value: string) => /^[1-9]\d{0,5}$/.test(value);
const isShort = (value: string) => value.length <= 200;
const selectClass = "min-h-11 min-w-0 max-w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3";

/** Loads one GET at a time for a key and keeps stale answers out after the key changes. */
function useLoad<T>(path: string | null, valid: (value: T) => boolean) {
  const [reload, setReload] = useState(0);
  const key = path ? `${path}#${reload}` : "";
  const [loaded, setLoaded] = useState<{ key: string; data?: T; error?: boolean }>();
  useEffect(() => {
    if (!path) return;
    const controller = new AbortController();
    api<T>(path, { signal: controller.signal }).then((value) => {
      if (controller.signal.aborted) return;
      if (!value || !valid(value)) throw new TypeError("Invalid topic pool data");
      setLoaded({ key, data: value });
    }).catch(() => { if (!controller.signal.aborted) setLoaded({ key, error: true }); });
    return () => controller.abort();
  // eslint-disable-next-line react-hooks/exhaustive-deps -- `valid` is a stable shape check; the key covers the request.
  }, [key, path]);
  return { data: loaded?.key === key ? loaded.data : undefined, error: loaded?.key === key && Boolean(loaded.error), retry: () => setReload((value) => value + 1) };
}

function Score({ audience, copy }: { audience: PoolAudience | null; copy: Copy }) {
  if (!audience) return <span className="text-sm text-[var(--muted)]">{copy.notScored}</span>;
  return <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
    <span className="text-2xl font-black tabular-nums" aria-label={copy.score}>{audience.score.toFixed(2)}</span>
    <span className="text-sm font-semibold">{videoPoolsText(copy.rank, { rank: audience.rank, of: audience.of })}</span>
    <span className="text-xs text-[var(--muted)]">{DIMS.map((dim) => `${copy.dims[dim]} ${audience[dim]}`).join("・")}</span>
  </div>;
}

function ThemeDetail({ series, id, copy }: { series: Series; id: string; copy: Copy }) {
  const { data, error, retry } = useLoad<PoolThemeDetail>(`/admin/video-pools/${series}/themes/${encodeURIComponent(id)}`, (value) => Array.isArray(value.chapters));
  if (error) return <AdminErrorState title={copy.detailError} detail={copy.errorDetail} retry={retry} retryLabel={copy.retry} />;
  if (!data) return <AdminSkeleton label={copy.detailLoading} />;
  const audience = data.audience;
  return <div className="grid min-w-0 gap-5 pt-3">
    <p className="font-semibold">{data.core_question}</p>
    {audience && <section>
      <h4 className="mb-2 font-bold">{copy.history}</h4>
      <ol className="grid gap-2 text-sm">
        {audience.rounds.map((round, index) => <li key={index} className="rounded-xl bg-[var(--paper)] p-3">
          <p>{videoPoolsText(copy.round, { date: round.reviewed_on, score: round.score.toFixed(2), comment: round.comment })}</p>
          <p className="mt-1 text-[var(--muted)]">{videoPoolsText(copy.changed, { changes: round.changes })}</p>
        </li>)}
        <li className="rounded-xl border border-[var(--line)] p-3 font-semibold">{videoPoolsText(copy.latest, { date: audience.reviewed_on, score: audience.score.toFixed(2), comment: audience.comment })}</li>
      </ol>
    </section>}
    {data.material?.missing && <section><h4 className="mb-2 font-bold">{copy.missing}</h4><p className="whitespace-pre-wrap break-words leading-7 [overflow-wrap:anywhere]">{data.material.missing}</p></section>}
    <section>
      <h4 className="mb-2 font-bold">{copy.chapters}</h4>
      <ol className="grid gap-2">
        {data.chapters.map((chapter, index) => <li key={index} className="min-w-0 rounded-xl border border-[var(--line)] p-3">
          <div className="flex flex-wrap items-baseline justify-between gap-2"><span className="font-semibold">{chapter.title}</span><span className="text-xs text-[var(--muted)]">{videoPoolsText(copy.seconds, { seconds: chapter.seconds })}</span></div>
          <p className="mt-1 break-words text-sm leading-6 [overflow-wrap:anywhere]">{chapter.new_information}</p>
        </li>)}
      </ol>
    </section>
    {([["boredom", data.boredom_risk], ["dropIf", data.drop_if], ["gaps", data.evidence_gaps]] as const).map(([label, text]) => <section key={label}>
      <h4 className="mb-2 font-bold">{copy[label]}</h4><p className="whitespace-pre-wrap break-words leading-7 [overflow-wrap:anywhere]">{text}</p>
    </section>)}
  </div>;
}

function Theme({ theme, series, copy }: { theme: PoolTheme; series: Series; copy: Copy }) {
  const [open, setOpen] = useState(false);
  const verdict: Verdict = theme.material?.verdict ?? (theme.producible ? "ready" : "none");
  return <article className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4 sm:p-5">
    <div className="flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
      <span className="font-mono">{theme.id}</span>{theme.category && <span>{theme.category}</span>}
      <span>{videoPoolsText(copy.minutes, { minutes: Math.round(theme.target_minutes * 10) / 10 })}</span>
      <span>{videoPoolsText(copy.candidates, { count: theme.candidates })}</span>
    </div>
    <h3 className="mt-2 break-words text-lg font-bold">{theme.title}</h3>
    <div className="mt-3 flex flex-wrap items-center gap-3">
      <AdminStatusPill status={theme.producible ? "active" : "pending"}>{copy.verdicts[verdict]}</AdminStatusPill>
      <Score audience={theme.audience} copy={copy} />
    </div>
    {theme.audience && <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{theme.audience.comment}</p>}
    <details className="mt-4 text-sm" onToggle={(event) => setOpen((event.target as HTMLDetailsElement).open)}>
      <summary className="min-h-11 cursor-pointer content-center font-bold text-[var(--teal)]">{copy.details}</summary>
      {open && <ThemeDetail series={series} id={theme.id} copy={copy} />}
    </details>
  </article>;
}

function ThemeSearch({ query, copy }: { query: string; copy: Copy }) {
  const [text, setText] = useState(query);
  return <form onSubmit={(event) => { event.preventDefault(); updateAdminQuery({ pool_q: text.trim(), pool_page: "" }); }} className="flex min-w-0 flex-1 flex-wrap items-end gap-2">
    <label className="grid min-w-0 flex-1 gap-1 text-sm font-semibold">{copy.search}
      <input type="search" maxLength={200} value={text} onChange={(event) => setText(event.target.value)} className="min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 font-normal" />
    </label>
    <Button secondary type="submit">{copy.searchButton}</Button>
  </form>;
}

function Themes({ series, copy }: { series: Series; copy: Copy }) {
  const [status] = useAdminQueryValue("pool_status", "producible", isStatus);
  const [category] = useAdminQueryValue("pool_category", "", isShort);
  const [minScore] = useAdminQueryValue("pool_min", "", isMinScore);
  const [query] = useAdminQueryValue("pool_q", "", isShort);
  const [pageValue] = useAdminQueryValue("pool_page", "1", isPage);
  const page = Number(pageValue);
  const params = new URLSearchParams({ status, page: String(page), page_size: String(PAGE_SIZE) });
  if (category) params.set("category", category);
  if (minScore) params.set("min_score", minScore);
  if (query) params.set("q", query);
  const { data, error, retry } = useLoad<PoolThemePage>(`/admin/video-pools/${series}/themes?${params}`, (value) => Array.isArray(value.items) && Number.isInteger(value.total));
  const pages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;
  const set = (values: Record<string, string>) => updateAdminQuery({ ...values, pool_page: "" });
  return <>
    <AdminFilterBar>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.statusLabel}
        <select value={status} onChange={(event) => set({ pool_status: event.target.value === "producible" ? "" : event.target.value, pool_category: "" })} className={selectClass}>
          {STATUSES.map((value) => <option key={value} value={value}>{copy.statuses[value]}</option>)}
        </select>
      </label>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.category}
        <select value={category} onChange={(event) => set({ pool_category: event.target.value })} className={selectClass}>
          <option value="">{copy.allCategories}</option>
          {data?.categories.map((facet) => <option key={facet.category} value={facet.category}>{facet.category} ({facet.count})</option>)}
        </select>
      </label>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.minScore}
        <select value={minScore} onChange={(event) => set({ pool_min: event.target.value })} className={selectClass}>
          <option value="">{copy.anyScore}</option>
          {MIN_SCORES.map((value) => <option key={value} value={value}>≥ {value}</option>)}
        </select>
      </label>
      <ThemeSearch key={query} query={query} copy={copy} />
      {(status !== "producible" || category || minScore || query) && <Button secondary onClick={() => set({ pool_status: "", pool_category: "", pool_min: "", pool_q: "" })}>{copy.clear}</Button>}
    </AdminFilterBar>
    {error ? <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={retry} retryLabel={copy.retry} />
      : !data ? <AdminSkeleton label={copy.loading} />
        : <>
          <p role="status" className="text-sm text-[var(--muted)]">{videoPoolsText(copy.results, { count: data.total })}</p>
          {data.items.length ? <div className="grid min-w-0 gap-3">{data.items.map((theme) => <Theme key={theme.id} theme={theme} series={series} copy={copy} />)}</div>
            : <AdminEmptyState title={copy.empty} detail={copy.emptyDetail} />}
          {pages > 1 && <nav aria-label={copy.pageLabel} className="flex flex-wrap items-center justify-between gap-3">
            <Button secondary disabled={page <= 1} onClick={() => updateAdminQuery({ pool_page: page - 1 === 1 ? "" : String(page - 1) })}>{copy.previous}</Button>
            <span className="text-sm">{videoPoolsText(copy.pagination, { page, pages })}</span>
            <Button secondary disabled={page >= pages} onClick={() => updateAdminQuery({ pool_page: String(page + 1) })}>{copy.next}</Button>
          </nav>}
        </>}
  </>;
}

function Published({ series, copy }: { series: Series; copy: Copy }) {
  const [status] = useAdminQueryValue("pool_published", "published", isEpisodeStatus);
  const [query] = useAdminQueryValue("pool_q", "", isShort);
  const params = new URLSearchParams({ status });
  if (query) params.set("q", query);
  const { data, error, retry } = useLoad<PoolEpisodePage>(`/admin/video-pools/${series}/episodes?${params}`, (value) => Array.isArray(value.items) && Number.isInteger(value.total));
  return <>
    <AdminFilterBar>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.publishedLabel}
        <select value={status} onChange={(event) => updateAdminQuery({ pool_published: event.target.value === "published" ? "" : event.target.value })} className={selectClass}>
          {EPISODE_STATUSES.map((value) => <option key={value} value={value}>{copy.publishedStatuses[value]}{data ? ` (${value === "published" ? data.published : value === "unpublished" ? data.unpublished : data.published + data.unpublished})` : ""}</option>)}
        </select>
      </label>
      <ThemeSearch key={query} query={query} copy={{ ...copy, search: copy.episodeSearch }} />
    </AdminFilterBar>
    {error ? <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={retry} retryLabel={copy.retry} />
      : !data ? <AdminSkeleton label={copy.loading} />
        : <>
          <p role="status" className="text-sm text-[var(--muted)]">{videoPoolsText(copy.episodeResults, { count: data.total })}</p>
          {data.items.length ? <div className="grid min-w-0 gap-3">{data.items.map((episode) => <article key={episode.key} className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
            <div className="flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
              {episode.code && <span className="font-mono font-semibold">{episode.code}</span>}
              {episode.category && <span>{episode.category}</span>}
              {episode.candidate_ids.length > 0 && <span>{videoPoolsText(copy.episodeCores, { ids: episode.candidate_ids.join("、") })}</span>}
            </div>
            <h3 className="mt-2 break-words font-bold">{episode.title}</h3>
            <div className="mt-2 flex flex-wrap items-center gap-2 text-sm">
              <AdminStatusPill status={episode.published ? "active" : episode.dropped ? "failed" : "inactive"}>{episode.published ? copy.publishedStatuses.published : episode.dropped ? copy.dropped : copy.publishedStatuses.unpublished}</AdminStatusPill>
              {episode.youtube_id && <a href={episode.youtube_url ?? undefined} target="_blank" rel="noreferrer" className="font-mono font-semibold text-[var(--teal)] underline">{episode.youtube_id}</a>}
              {episode.youtube_source && <span className="text-xs text-[var(--muted)]">{copy.sources[episode.youtube_source]}</span>}
              {episode.privacy && <span className="text-xs text-[var(--muted)]">{videoPoolsText(copy.privacy, { privacy: episode.privacy })}</span>}
              {episode.publish_at && <span className="text-xs text-[var(--muted)]">{videoPoolsText(copy.publishAt, { date: episode.publish_at.slice(0, 10) })}</span>}
              {episode.stage && <span className="text-xs text-[var(--muted)]">{videoPoolsText(copy.stage, { stage: episode.stage })}</span>}
            </div>
            {episode.slugs.length > 0 && <p className="mt-2 break-all font-mono text-xs text-[var(--muted)]">{episode.slugs.join("　")}</p>}
          </article>)}</div>
            : <AdminEmptyState title={copy.episodeEmpty} detail={copy.emptyDetail} />}
        </>}
  </>;
}

function Expansions({ series, copy }: { series: Series; copy: Copy }) {
  const { data, error, retry } = useLoad<PoolExpansions>(`/admin/video-pools/${series}/expansions`, (value) => Array.isArray(value.expansions) && Array.isArray(value.checkpoints));
  if (error) return <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={retry} retryLabel={copy.retry} />;
  if (!data) return <AdminSkeleton label={copy.loading} />;
  return <div className="grid min-w-0 gap-6">
    <section>
      <h3 className="mb-3 text-lg font-bold">{copy.batches}</h3>
      <ol className="grid gap-2">
        {data.expansions.map((batch) => <li key={batch.batch_id} className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1"><span className="font-mono text-sm font-semibold">{batch.batch_id}</span><span className="text-xs text-[var(--muted)]">{batch.created_on ?? copy.noDate}</span></div>
          <p className="mt-1 text-sm font-semibold">{videoPoolsText(copy.batchCounts, { candidates: batch.candidates, selected: batch.selected, not_added: batch.not_added, sources: batch.sources })}</p>
          {batch.scope && <details className="mt-2 text-sm"><summary className="cursor-pointer text-[var(--teal)]">{batch.scope.slice(0, 60)}{batch.scope.length > 60 ? "…" : ""}</summary><p className="mt-2 whitespace-pre-wrap break-words leading-6 [overflow-wrap:anywhere]">{batch.scope}</p></details>}
        </li>)}
      </ol>
    </section>
    {data.checkpoints.length > 0 && <section>
      <h3 className="mb-3 text-lg font-bold">{copy.checkpoints}</h3>
      <ul className="grid gap-1 text-sm">{data.checkpoints.map((point) => <li key={point.name}>{videoPoolsText(copy.checkpoint, { name: point.name, selected: point.selected ?? "—", raw: point.raw ?? "—" })}</li>)}</ul>
    </section>}
  </div>;
}

/** The packaged topic pools: producible themes with audience scores, and how each pool grew. Read-only. */
export function AdminVideoPools() {
  const copy = videoPoolsCopy(useLocale());
  const [seriesValue] = useAdminQueryValue("pool_series", "curio", isSeries);
  const series = seriesValue as Series;
  const [view] = useAdminQueryValue("pool_view", "themes", isView);
  const overview = useLoad<PoolOverview>("/admin/video-pools", (value) => Array.isArray(value.series));
  const current = overview.data?.series.find((entry) => entry.key === series);
  return <section aria-label={copy.title} className="grid min-w-0 gap-4">
    <header>
      <h2 className="text-xl font-black">{copy.title}</h2>
      <p className="mt-2 max-w-3xl text-sm leading-7 text-[var(--muted)]">{copy.description}</p>
      <p className="mt-1 text-sm text-[var(--muted)]">{copy.readOnly}</p>
    </header>
    <AdminFilterBar>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.seriesLabel}
        <select value={series} onChange={(event) => updateAdminQuery({ pool_series: event.target.value === "curio" ? "" : event.target.value, pool_status: "", pool_category: "", pool_min: "", pool_q: "", pool_page: "" })} className={selectClass}>
          {SERIES.map((value) => <option key={value} value={value}>{copy.series[value]}</option>)}
        </select>
      </label>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.viewLabel}
        <select value={view} onChange={(event) => updateAdminQuery({ pool_view: event.target.value === "themes" ? "" : event.target.value })} className={selectClass}>
          {VIEWS.map((value) => <option key={value} value={value}>{copy.views[value]}</option>)}
        </select>
      </label>
    </AdminFilterBar>
    {overview.error ? <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={overview.retry} retryLabel={copy.retry} />
      : current && <div className="grid gap-2">
        <dl className="grid grid-cols-2 gap-2 sm:grid-cols-5">
          {(Object.keys(copy.counts) as (keyof Copy["counts"])[]).map((name) => <div key={name} className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-3">
            <dt className="text-xs text-[var(--muted)]">{copy.counts[name]}</dt><dd className="text-xl font-black tabular-nums">{current.counts[name].toLocaleString()}</dd>
          </div>)}
        </dl>
        <p className="text-xs text-[var(--muted)]">{videoPoolsText(copy.revision, { revision: current.revision })}</p>
        <p className="text-sm">{videoPoolsText(copy.minimum, { min: current.audience_min })}</p>
      </div>}
    {view === "themes" ? <Themes key={series} series={series} copy={copy} /> : view === "published" ? <Published key={series} series={series} copy={copy} /> : <Expansions key={series} series={series} copy={copy} />}
  </section>;
}
