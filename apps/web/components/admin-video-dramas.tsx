"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { AdminEmptyState, AdminErrorState, AdminFilterBar, AdminSkeleton, AdminStatusPill } from "@/components/admin-ui";
import { Button } from "@/components/community/ui";
import { updateAdminQuery, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { videoDramasCopy, videoDramasText } from "@/lib/video-dramas-copy";

type Copy = ReturnType<typeof videoDramasCopy>;
type DocKind = keyof Copy["docs"];
const VIEWS = ["episodes", "documents"] as const;
const DOC_KINDS: DocKind[] = ["brief", "script", "storyboard", "review"];
export type DramaEpisode = { slug: string; number: number; variant: string | null; title: string; target_minutes: number | number[] | null; docs: { kind: DocKind; bytes: number }[] };
export type DramaSeries = {
  key: string; name: string; content_sha256: string;
  counts: { episodes: number } & Record<DocKind, number>;
  episodes: DramaEpisode[];
  documents: { id: string; path: string; title: string; bytes: number }[];
};
export type DramaIndex = { schema_version: number; status: string; series: DramaSeries[] };
export type DramaEpisodeDetail = { series: string; slug: string; title: string; docs: { kind: DocKind; markdown: string }[] };
export type DramaDocument = { series: string; id: string; path: string; title: string; markdown: string };
const isView = (value: string) => (VIEWS as readonly string[]).includes(value);
const isKey = (value: string) => /^[a-z0-9-]{1,40}$/.test(value);
const isQuery = (value: string) => value.length <= 100;
const selectClass = "min-h-11 min-w-0 max-w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3";
const textClass = "max-h-[40rem] overflow-y-auto whitespace-pre-wrap break-words rounded-xl bg-[var(--paper)] p-3 text-sm leading-7 [overflow-wrap:anywhere]";

function useLoad<T>(path: string | null, valid: (value: T) => boolean) {
  const [reload, setReload] = useState(0);
  const key = path ? `${path}#${reload}` : "";
  const [loaded, setLoaded] = useState<{ key: string; data?: T; error?: boolean }>();
  useEffect(() => {
    if (!path) return;
    const controller = new AbortController();
    api<T>(path, { signal: controller.signal }).then((value) => {
      if (controller.signal.aborted) return;
      if (!value || !valid(value)) throw new TypeError("Invalid drama script data");
      setLoaded({ key, data: value });
    }).catch(() => { if (!controller.signal.aborted) setLoaded({ key, error: true }); });
    return () => controller.abort();
  // eslint-disable-next-line react-hooks/exhaustive-deps -- `valid` is a stable shape check; the key covers the request.
  }, [key, path]);
  return { data: loaded?.key === key ? loaded.data : undefined, error: loaded?.key === key && Boolean(loaded.error), retry: () => setReload((value) => value + 1) };
}

const minutesText = (value: DramaEpisode["target_minutes"]) => value === null ? null : Array.isArray(value) ? value.join("–") : String(value);

function EpisodeText({ series, slug, copy }: { series: string; slug: string; copy: Copy }) {
  const { data, error, retry } = useLoad<DramaEpisodeDetail>(`/admin/video-dramas/${series}/episodes/${slug}`, (value) => Array.isArray(value.docs));
  const [kind, setKind] = useState<DocKind | null>(null);
  if (error) return <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={retry} retryLabel={copy.retry} />;
  if (!data) return <AdminSkeleton label={copy.loading} />;
  const shown = data.docs.find((doc) => doc.kind === kind) ?? data.docs.find((doc) => doc.kind === "script") ?? data.docs[0];
  return <div className="grid min-w-0 gap-3 pt-3">
    <div role="tablist" aria-label={copy.viewLabel} className="flex flex-wrap gap-2">
      {data.docs.map((doc) => <Button key={doc.kind} secondary={doc.kind !== shown?.kind} role="tab" aria-selected={doc.kind === shown?.kind} onClick={() => setKind(doc.kind)}>{copy.docs[doc.kind]}</Button>)}
    </div>
    {shown && <div role="tabpanel" className={textClass}>{shown.markdown}</div>}
  </div>;
}

function Episode({ series, episode, copy }: { series: string; episode: DramaEpisode; copy: Copy }) {
  const [open, setOpen] = useState(false);
  const minutes = minutesText(episode.target_minutes);
  return <article className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <div className="flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
      <span className="font-semibold">{videoDramasText(copy.episode, { number: episode.number })}</span>
      {episode.variant && <AdminStatusPill status="queued">{copy.variants[episode.variant as keyof Copy["variants"]] ?? episode.variant}</AdminStatusPill>}
      <span className="font-mono">{episode.slug}</span>
      {minutes && <span>{videoDramasText(copy.minutes, { minutes })}</span>}
    </div>
    <h3 className="mt-2 break-words font-bold">{episode.title}</h3>
    <div className="mt-2 flex flex-wrap gap-2">{DOC_KINDS.map((kind) => <AdminStatusPill key={kind} status={episode.docs.some((doc) => doc.kind === kind) ? "active" : "inactive"}>{copy.docs[kind]}</AdminStatusPill>)}</div>
    <details className="mt-3 text-sm" onToggle={(event) => setOpen((event.target as HTMLDetailsElement).open)}>
      <summary className="min-h-11 cursor-pointer content-center font-bold text-[var(--teal)]">{open ? copy.close : copy.open}</summary>
      {open && <EpisodeText series={series} slug={episode.slug} copy={copy} />}
    </details>
  </article>;
}

function Document({ series, document, copy }: { series: string; document: DramaSeries["documents"][number]; copy: Copy }) {
  const [open, setOpen] = useState(false);
  return <article className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <h3 className="break-words font-bold">{document.title}</h3>
    <p className="mt-1 break-all font-mono text-xs text-[var(--muted)]">{videoDramasText(copy.documentPath, { path: document.path })}</p>
    <details className="mt-3 text-sm" onToggle={(event) => setOpen((event.target as HTMLDetailsElement).open)}>
      <summary className="min-h-11 cursor-pointer content-center font-bold text-[var(--teal)]">{open ? copy.close : copy.open}</summary>
      {open && <DocumentText series={series} id={document.id} copy={copy} />}
    </details>
  </article>;
}

function DocumentText({ series, id, copy }: { series: string; id: string; copy: Copy }) {
  const { data, error, retry } = useLoad<DramaDocument>(`/admin/video-dramas/${series}/documents/${id}`, (value) => typeof value.markdown === "string");
  if (error) return <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={retry} retryLabel={copy.retry} />;
  if (!data) return <AdminSkeleton label={copy.loading} />;
  return <div className={`mt-3 ${textClass}`}>{data.markdown}</div>;
}

/** Authored AI drama text packaged with the API image: episodes and series documents, read-only. */
export function AdminVideoDramas() {
  const copy = videoDramasCopy(useLocale());
  const index = useLoad<DramaIndex>("/admin/video-dramas", (value) => Array.isArray(value.series));
  const [seriesValue] = useAdminQueryValue("script_series", "", isKey);
  const [view] = useAdminQueryValue("script_view", "episodes", isView);
  const [query] = useAdminQueryValue("script_q", "", isQuery);
  const [text, setText] = useState(query);
  if (index.error) return <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={index.retry} retryLabel={copy.retry} />;
  if (!index.data) return <AdminSkeleton label={copy.loading} />;
  const series = index.data.series.find((item) => item.key === seriesValue) ?? index.data.series[0];
  const needle = query.trim().toLowerCase();
  const episodes = series.episodes.filter((episode) => !needle || episode.title.toLowerCase().includes(needle) || episode.slug.includes(needle) || String(episode.number) === needle);
  return <section aria-label={copy.title} className="grid min-w-0 gap-4">
    <header>
      <h2 className="text-xl font-black">{copy.title}</h2>
      <p className="mt-2 max-w-3xl text-sm leading-7 text-[var(--muted)]">{copy.description}</p>
      <p className="mt-1 text-sm text-[var(--muted)]">{copy.readOnly}</p>
    </header>
    <AdminFilterBar>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.seriesLabel}
        <select value={series.key} onChange={(event) => updateAdminQuery({ script_series: event.target.value, script_q: "" })} className={selectClass}>
          {index.data.series.map((item) => <option key={item.key} value={item.key}>{item.name} ({item.counts.episodes})</option>)}
        </select>
      </label>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.viewLabel}
        <select value={view} onChange={(event) => updateAdminQuery({ script_view: event.target.value === "episodes" ? "" : event.target.value })} className={selectClass}>
          {VIEWS.map((value) => <option key={value} value={value}>{copy.views[value]}</option>)}
        </select>
      </label>
      {view === "episodes" && <form onSubmit={(event) => { event.preventDefault(); updateAdminQuery({ script_q: text.trim() }); }} className="flex min-w-0 flex-1 flex-wrap items-end gap-2">
        <label className="grid min-w-0 flex-1 gap-1 text-sm font-semibold">{copy.search}
          <input type="search" maxLength={100} value={text} onChange={(event) => setText(event.target.value)} className="min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 font-normal" />
        </label>
        <Button secondary type="submit">{copy.search}</Button>
      </form>}
    </AdminFilterBar>
    <p className="text-sm font-semibold">{videoDramasText(copy.counts, series.counts)}</p>
    {view === "episodes" ? <>
      <p role="status" className="text-sm text-[var(--muted)]">{videoDramasText(copy.results, { count: episodes.length })}</p>
      {episodes.length ? <div className="grid min-w-0 gap-3">{episodes.map((episode) => <Episode key={episode.slug} series={series.key} episode={episode} copy={copy} />)}</div>
        : <AdminEmptyState title={copy.empty} detail={copy.emptyDetail} />}
    </> : <div className="grid min-w-0 gap-3">{series.documents.map((document) => <Document key={document.id} series={series.key} document={document} copy={copy} />)}</div>}
  </section>;
}
