"use client";

import { ArrowLeft, BookOpen } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { control, list, type ProjectSummary, record, text, useRefresh, useWhen } from "@/components/admin-video-review-card";
import { DiscussionThread, docSubject } from "@/components/admin-video-thread";
import { Button } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The drama tab of /admin/videos (docs/videos/SERIES.md): a long series is planned document by
// document (the setting book, the whole-series outline, each chapter's detailed outline), each
// approved here, and made episode by episode; every episode is a video of its own with the usual
// review cards, reached from the episode table. A one-off episode (docs/videos/DRAMA-FLOW.md,
// section 2) is a series of one episode whose only document is its story bible; the form files one
// and the list shows them apart. Every document carries a discussion thread (section 3).
type SeriesStatus = "setting" | "outline" | "active" | "paused" | "finished";
type SeriesKind = "series" | "one-off";
type DocKind = "setting" | "outline" | "chapter" | "bible";
type DocStatus = "generating" | "review" | "approved" | "rejected";
type EpisodeStatus = "planned" | "ready" | "queued" | "started" | "done" | "skipped";
export type SeriesDoc = {
  id: string; kind: DocKind; chapter_number: number; version: number; body_md: string; body_json: Record<string, unknown>; status: DocStatus; note: string | null;
  decided_at: string | null; created_at: string;
  // The owner's lines on this document's thread the model has not answered; absent from an older API.
  unanswered?: number;
};
type SeriesEpisode = {
  number: number; chapter_number: number; title: string; logline: string; beats: Record<string, unknown>; status: EpisodeStatus; slug: string | null;
  recap: string | null; started_at: string | null; finished_at: string | null; video: ProjectSummary | null;
};
type SeriesSummary = {
  id: string; slug: string; title: string; premise: string; aspects: string[]; tone: string; style_preset: string; target_minutes: number;
  planned_episodes: number; episodes_per_chapter: number; chapters: number; open_ended: boolean; status: SeriesStatus; note: string | null;
  requested_chapter: number | null; force_next: boolean; episodes_done: number; episodes_started: number; episodes_ready: number; docs_pending: number;
  media_usd: number; clip_seconds: number; created_at: string; updated_at: string;
  // Both absent from an API older than one-offs and threads: a series then, with nothing waiting.
  kind?: SeriesKind; messages_pending?: number;
};
export type Series = SeriesSummary & { docs: SeriesDoc[]; episodes: SeriesEpisode[] };
type RequestStatus = "queued" | "started" | "done" | "cancelled";
type DramaRequest = {
  id: string; premise: string; title: string | null; source_guide: string | null; style_preset: string; target_minutes: number;
  note: string | null; status: RequestStatus; slug: string | null; created_at: string; started_at: string | null; finished_at: string | null; cancelled_at: string | null;
  // The one-off series the request became; a request from before one-offs were series has none.
  series_slug?: string | null; episode_number?: number | null;
};

export const SERIES_SLUG = /^[a-z0-9][a-z0-9-]{1,39}$/;
// The drama part of the settings tab, where the route is switched on (docs/videos/DRAMA-FLOW.md, section 1).
const DRAMA_SETTINGS = "/admin/videos?tab=settings&section=drama";
const ASPECTS = ["world", "bonds", "structure", "mood"] as const;
const TONES = ["dual-male-leads-subtext", "dual-male-leads-explicit", "hetero-leads", "no-romance"] as const;
const PRESETS = ["cinematic-3d", "anime-2d", "ink-wash", "custom"] as const;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
const seriesTone: Record<SeriesStatus, string> = { setting: "pending", outline: "pending", active: "active", paused: "inactive", finished: "inactive" };
const docTone: Record<DocStatus, string> = { generating: "running", review: "pending", approved: "active", rejected: "failed" };
const episodeTone: Record<EpisodeStatus, string> = { planned: "inactive", ready: "queued", queued: "queued", started: "active", done: "ok", skipped: "inactive" };
const requestTone: Record<RequestStatus, string> = { queued: "pending", started: "active", done: "inactive", cancelled: "inactive" };
const message = (problem: unknown) => (problem instanceof Error ? problem.message : "");
// The status pill's key: a one-off waiting on its first document (the server starts it at "setting",
// apps/api/app/video_automation/series.py create_one_off) waits for a story bible, not a setting book.
const statusKey = (series: SeriesSummary) => (series.kind === "one-off" && series.status === "setting" ? "bible" : series.status);
const docPath = (slug: string, doc: SeriesDoc) => `/admin/video-automation/series/${slug}/docs/${doc.kind}${doc.kind === "chapter" ? `/${doc.chapter_number}` : ""}`;

/** Start a series: the premise and the shape; the worker plans the setting book from it. */
function NewSeriesForm({ onCreated }: { onCreated: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const [slug, setSlug] = useState("");
  const [title, setTitle] = useState("");
  const [premise, setPremise] = useState("");
  const [aspects, setAspects] = useState<string[]>([...ASPECTS]);
  const [tone, setTone] = useState<(typeof TONES)[number]>("dual-male-leads-subtext");
  const [preset, setPreset] = useState<(typeof PRESETS)[number]>("cinematic-3d");
  const [minutes, setMinutes] = useState(3);
  const [planned, setPlanned] = useState(100);
  const [perChapter, setPerChapter] = useState(10);
  const [openEnded, setOpenEnded] = useState(true);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const slugOk = SERIES_SLUG.test(slug.trim());
  const create = async () => {
    setBusy(true);
    setError("");
    try {
      const created = await api<Series>("/admin/video-automation/series", {
        method: "POST",
        body: JSON.stringify({ slug: slug.trim(), title: title.trim(), premise: premise.trim(), aspects, tone, style_preset: preset, target_minutes: minutes, planned_episodes: planned, episodes_per_chapter: perChapter, open_ended: openEnded, note: note.trim() || undefined }),
      });
      onCreated(created.slug);
    } catch (problem) {
      setError(t("createError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("newSeries")}</summary>
    <form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); void create(); }} aria-label={t("newSeries")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("newSeriesHelp")} <Link href={DRAMA_SETTINGS} className="font-semibold text-[var(--teal)] underline">{t("openDramaSettings")}</Link></p>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("fields.title")}<input className={control} value={title} disabled={busy} maxLength={200} onChange={(event) => setTitle(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.slug")}<input className={control} value={slug} disabled={busy} placeholder={t("slugPlaceholder")} aria-invalid={Boolean(slug) && !slugOk} onChange={(event) => setSlug(event.target.value)} /></label>
      </div>
      <label className="grid gap-2 text-sm font-semibold">{t("fields.premise")}
        <textarea className={control} rows={4} value={premise} disabled={busy} maxLength={4000} placeholder={t("premisePlaceholder")} onChange={(event) => setPremise(event.target.value)} />
      </label>
      <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("fields.aspects")}</legend>
        <div className="grid gap-2 md:grid-cols-2">{ASPECTS.map((aspect) => <label key={aspect} className="flex min-h-11 items-center gap-2 text-sm"><input type="checkbox" checked={aspects.includes(aspect)} disabled={busy} onChange={(event) => setAspects(event.target.checked ? [...aspects, aspect] : aspects.filter((each) => each !== aspect))} />{t(`aspects.${aspect}`)}</label>)}</div>
      </fieldset>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("fields.tone")}
          <select className={control} value={tone} disabled={busy} onChange={(event) => setTone(event.target.value as (typeof TONES)[number])}>{TONES.map((each) => <option key={each} value={each}>{t(`tones.${each}`)}</option>)}</select>
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.stylePreset")}
          <select className={control} value={preset} disabled={busy} onChange={(event) => setPreset(event.target.value as (typeof PRESETS)[number])}>{PRESETS.map((each) => <option key={each} value={each}>{t(`presets.${each}`)}</option>)}</select>
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.targetMinutes")}<input className={control} type="number" min={1} max={8} value={minutes} disabled={busy} onChange={(event) => setMinutes(Number(event.target.value))} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.plannedEpisodes")}<input className={control} type="number" min={1} max={500} value={planned} disabled={busy} onChange={(event) => setPlanned(Number(event.target.value))} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.episodesPerChapter")}<input className={control} type="number" min={4} max={20} value={perChapter} disabled={busy} onChange={(event) => setPerChapter(Number(event.target.value))} /></label>
        <label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={openEnded} disabled={busy} onChange={(event) => setOpenEnded(event.target.checked)} />{t("fields.openEnded")}</label>
      </div>
      <label className="grid gap-2 text-sm font-semibold">{t("fields.note")}<textarea className={control} rows={2} value={note} disabled={busy} maxLength={2000} placeholder={t("notePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button type="submit" disabled={busy || !title.trim() || !premise.trim() || !slugOk || aspects.length === 0}>{busy ? t("saving") : t("create")}</Button></div>
    </form>
  </details>;
}

/**
 * A one-off episode: a premise (or an article to adapt), a style and a length. The server files it
 * as a series of one episode and answers with that series' slug, which the caller opens; an older
 * server answers without one and the request stays in the queue below.
 */
function NewDramaForm({ onFiled }: { onFiled: (seriesSlug: string | null) => void }) {
  const t = useTranslations("admin.videoReviews");
  const [premise, setPremise] = useState("");
  const [title, setTitle] = useState("");
  const [guide, setGuide] = useState("");
  const [preset, setPreset] = useState<(typeof PRESETS)[number]>("cinematic-3d");
  const [minutes, setMinutes] = useState(3);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const guideOk = !guide.trim() || GUIDE_SLUG.test(guide.trim());
  const file = async () => {
    setBusy(true);
    setError("");
    try {
      const filed = await api<DramaRequest>("/admin/video-automation/drama-requests", {
        method: "POST",
        body: JSON.stringify({ premise: premise.trim(), title: title.trim() || undefined, source_guide: guide.trim() || undefined, style_preset: preset, target_minutes: minutes, note: note.trim() || undefined }),
      });
      setPremise(""); setTitle(""); setGuide(""); setNote("");
      onFiled(filed?.series_slug ?? null);
    } catch (problem) {
      setError(t("newDramaError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("newDrama")}</summary>
    <form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); void file(); }} aria-label={t("newDrama")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("newDramaHelp")} <Link href={DRAMA_SETTINGS} className="font-semibold text-[var(--teal)] underline">{t("openDramaSettings")}</Link></p>
      <label className="grid gap-2 text-sm font-semibold">{t("premise")}
        <textarea className={control} rows={4} value={premise} disabled={busy} maxLength={4000} placeholder={t("premisePlaceholder")} onChange={(event) => setPremise(event.target.value)} />
      </label>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("workingTitle")}<input className={control} value={title} disabled={busy} maxLength={200} onChange={(event) => setTitle(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("sourceGuide")}<input className={control} value={guide} disabled={busy} placeholder={t("sourceGuidePlaceholder")} aria-invalid={!guideOk} onChange={(event) => setGuide(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("stylePreset")}
          <select className={control} value={preset} disabled={busy} onChange={(event) => setPreset(event.target.value as (typeof PRESETS)[number])}>
            {PRESETS.map((each) => <option key={each} value={each}>{t(`presets.${each}`)}</option>)}
          </select>
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("targetMinutes")}<input className={control} type="number" min={1} max={8} value={minutes} disabled={busy} onChange={(event) => setMinutes(Number(event.target.value))} /></label>
      </div>
      <label className="grid gap-2 text-sm font-semibold">{t("requestNote")}<textarea className={control} rows={2} value={note} disabled={busy} maxLength={2000} placeholder={t("requestNotePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button type="submit" disabled={busy || !premise.trim() || !guideOk || minutes < 1 || minutes > 8}>{busy ? t("saving") : t("fileRequest")}</Button></div>
    </form>
  </details>;
}

/** What the owner asked for as one-off episodes and where each stands; a queued one can be withdrawn. */
function DramaQueue({ requests, canManage, onChanged, onOpen }: { requests: DramaRequest[]; canManage: boolean; onChanged: () => void; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const cancel = async (request: DramaRequest) => {
    if (!window.confirm(t("cancelConfirm"))) return;
    setBusy(request.id);
    setError("");
    try {
      await api(`/admin/video-automation/drama-requests/${request.id}`, { method: "DELETE" });
      onChanged();
    } catch (problem) {
      setError(t("cancelError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  if (!requests.length) return null;
  return <section className="grid gap-3" aria-label={t("queue")}>
    <h3 className="text-lg font-bold">{t("queue")}</h3>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <ul className="grid gap-3">{requests.map((request) => <li key={request.id} className="grid gap-2 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
      <span className="flex flex-wrap items-center gap-3">
        <AdminStatusPill status={requestTone[request.status]}>{t(`requestStatuses.${request.status}`)}</AdminStatusPill>
        <span className="font-bold">{request.title || request.premise.slice(0, 40)}</span>
        <span className="text-sm text-[var(--muted)]">{t(`presets.${request.style_preset}`)} · {t("minutes", { minutes: request.target_minutes })} · {t("filedAt", { time: when(request.created_at) })}</span>
      </span>
      <span className="whitespace-pre-wrap text-sm leading-6">{request.premise}</span>
      {request.source_guide && <span className="text-sm text-[var(--muted)]">{t("adaptsArticle", { slug: request.source_guide })}</span>}
      {request.note && <span className="text-sm text-[var(--muted)]">{t("requestNote")}: {request.note}</span>}
      <span className="flex flex-wrap gap-3">
        {request.slug && <Button secondary onClick={() => onOpen(request.slug as string)}>{t("openVideo", { slug: request.slug })}</Button>}
        {canManage && request.status === "queued" && <Button secondary disabled={busy === request.id} onClick={() => void cancel(request)}>{busy === request.id ? t("saving") : t("cancelRequest")}</Button>}
      </span>
    </li>)}</ul>
  </section>;
}

/** What waits on a series card: documents for the owner, lines for the model. */
function WaitingPills({ series }: { series: SeriesSummary }) {
  const t = useTranslations("admin.videoSeries");
  return <>
    {series.docs_pending > 0 && <AdminStatusPill status="pending">{t("docsPending", { count: series.docs_pending })}</AdminStatusPill>}
    {(series.messages_pending ?? 0) > 0 && <AdminStatusPill status="running">{t("messagesPending", { count: series.messages_pending ?? 0 })}</AdminStatusPill>}
  </>;
}

/** The series the owner started, and the one-off episodes; opening a series shows its page. */
function SeriesList({ onOpenSeries, onOpenVideo }: { onOpenSeries: (slug: string) => void; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const manage = useAdminActionGuard("content.manage");
  const [series, setSeries] = useState<SeriesSummary[] | null>(null);
  const [oneOffs, setOneOffs] = useState<SeriesSummary[]>([]);
  const [requests, setRequests] = useState<DramaRequest[]>([]);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<{ series: SeriesSummary[] }>("/admin/video-automation/series?kind=series").then((value) => { setSeries((value.series ?? []).filter((each) => each.kind !== "one-off")); setError(""); }).catch((problem: unknown) => setError(message(problem)));
    // One-off episodes are series of one episode; an older site ignores the filter and is filtered here.
    api<{ series: SeriesSummary[] }>("/admin/video-automation/series?kind=one-off").then((value) => setOneOffs((value.series ?? []).filter((each) => each.kind === "one-off"))).catch(() => setOneOffs([]));
    // Requests from before a one-off was a series still show here until they finish; the others
    // are their series' cards. Finished and withdrawn ones drop off after a week.
    api<{ requests: DramaRequest[] }>("/admin/video-automation/drama-requests").then((value) => {
      const recent = Date.now() - 7 * 24 * 3600_000;
      setRequests((value.requests ?? []).filter((request) => !request.series_slug && (request.status === "queued" || request.status === "started" || Date.parse(request.created_at) > recent)));
    }).catch(() => setRequests([]));
  }, []);
  useRefresh(load);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  return <div className="grid gap-4">
    {manage.allowed && <NewSeriesForm onCreated={(slug) => { load(); onOpenSeries(slug); }} />}
    {series && series.length === 0 && <AdminEmptyState title={t("empty")} detail={t("emptyDetail")} />}
    {series && series.length > 0 && <ul className="grid gap-4" aria-label={t("listTitle")}>{series.map((each) => <li key={each.slug}>
      <button type="button" onClick={() => onOpenSeries(each.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
        <span className="flex flex-wrap items-center gap-3"><BookOpen aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{each.title}</span>
          <AdminStatusPill status={seriesTone[each.status]}>{t(`statuses.${statusKey(each)}`)}</AdminStatusPill>
          <WaitingPills series={each} />
        </span>
        <span className="text-sm text-[var(--muted)]">{t("progress", { done: each.episodes_done, total: each.planned_episodes, chapters: each.chapters })} · {t("spend", { usd: Number(each.media_usd ?? 0).toFixed(2), seconds: each.clip_seconds ?? 0 })}</span>
        <span className="line-clamp-2 text-sm leading-6">{each.premise}</span>
      </button>
    </li>)}</ul>}
    {manage.allowed && <NewDramaForm onFiled={(seriesSlug) => { load(); if (seriesSlug) onOpenSeries(seriesSlug); }} />}
    <DramaQueue requests={requests} canManage={manage.allowed} onChanged={load} onOpen={onOpenVideo} />
    {oneOffs.length > 0 && <section className="grid gap-3" aria-label={t("oneOffTitle")}>
      <h3 className="text-lg font-bold">{t("oneOffTitle")}</h3>
      <ul className="grid gap-4">{oneOffs.map((each) => <li key={each.slug}>
        <button type="button" onClick={() => onOpenSeries(each.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
          <span className="flex flex-wrap items-center gap-3"><span className="text-lg font-bold">{each.title}</span>
            <AdminStatusPill status="active">{t("oneOff")}</AdminStatusPill>
            <AdminStatusPill status={seriesTone[each.status]}>{t(`statuses.${statusKey(each)}`)}</AdminStatusPill>
            <WaitingPills series={each} />
          </span>
          <span className="text-sm text-[var(--muted)]">{t("spend", { usd: Number(each.media_usd ?? 0).toFixed(2), seconds: each.clip_seconds ?? 0 })} · {t(`presets.${each.style_preset}`)} · {t("minutesEach", { minutes: each.target_minutes })}</span>
          <span className="line-clamp-2 text-sm leading-6">{each.premise}</span>
        </button>
      </li>)}</ul>
    </section>}
  </div>;
}

const beatText = (beats: Record<string, unknown>, key: string) => {
  const value = beats[key];
  if (value && typeof value === "object" && !Array.isArray(value)) return text((value as Record<string, unknown>).text) || "";
  return text(value);
};
const cliffType = (beats: Record<string, unknown>) => {
  const value = beats.cliffhanger;
  return value && typeof value === "object" && !Array.isArray(value) ? text((value as Record<string, unknown>).type) : "";
};
const threads = (beats: Record<string, unknown>) => `${list(beats.setups).map(text).join("、") || "—"} / ${list(beats.payoffs).map(text).join("、") || "—"}`;
const tension = (beats: Record<string, unknown>) => list(beats.tension).map(text).join("-");

/** A chapter outline as a table: every episode's hook, conflict, turn, cliffhanger, threads and tension. */
function BeatsTable({ episodes }: { episodes: Record<string, unknown>[] }) {
  const t = useTranslations("admin.videoSeries");
  return <div className="overflow-x-auto"><table className="min-w-full text-sm">
    <thead><tr className="text-left text-xs text-[var(--muted)]">{(["episode", "title", "hook", "conflict", "turn", "cliffhanger", "threads", "tension"] as const).map((key) => <th key={key} className="px-2 py-1 font-semibold">{t(`beats.${key}`)}</th>)}</tr></thead>
    <tbody>{episodes.map((episode) => <tr key={text(episode.number)} className="border-t border-[var(--line)] align-top">
      <td className="px-2 py-2 font-mono">{text(episode.number)}</td>
      <td className="px-2 py-2 font-semibold">{text(episode.title)}</td>
      <td className="px-2 py-2">{beatText(episode, "hook")}</td>
      <td className="px-2 py-2">{beatText(episode, "conflict")}</td>
      <td className="px-2 py-2">{beatText(episode, "turn")}</td>
      <td className="px-2 py-2">{beatText(episode, "cliffhanger")}{cliffType(episode) && <span className="block text-xs text-[var(--muted)]">{cliffType(episode)}</span>}</td>
      <td className="px-2 py-2 font-mono text-xs">{threads(episode)}</td>
      <td className="px-2 py-2 font-mono">{tension(episode)}</td>
    </tr>)}</tbody>
  </table></div>;
}

/**
 * One document of a series: read it, discuss it with the model, approve it or send it back with a
 * note, or rewrite it yourself. The video page of a one-off shows its story bible through this too.
 */
export function DocPanel({ slug, doc, canManage, onChanged }: { slug: string; doc: SeriesDoc; canManage: boolean; onChanged: () => void }) {
  const t = useTranslations("admin.videoSeries");
  const when = useWhen();
  const [note, setNote] = useState("");
  const [draft, setDraft] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const title = doc.kind === "chapter" ? t("chapterN", { n: doc.chapter_number }) : t(`docKinds.${doc.kind}`);
  const decide = async (decision: "approve" | "reject") => {
    setBusy(true);
    setError("");
    try {
      await api(`${docPath(slug, doc)}/decision`, { method: "POST", body: JSON.stringify({ decision, note: note.trim() || undefined }) });
      setNote("");
      onChanged();
    } catch (problem) {
      setError(t("decideError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const save = async (approve: boolean) => {
    if (draft === null || !draft.trim()) return;
    setBusy(true);
    setError("");
    try {
      await api(docPath(slug, doc), { method: "PUT", body: JSON.stringify({ body_md: draft, approve }) });
      setDraft(null);
      onChanged();
    } catch (problem) {
      setError(t("editError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const episodes = doc.kind === "chapter" ? list(doc.body_json.episodes).map(record) : [];
  return <details open={doc.status === "review"} className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="flex cursor-pointer flex-wrap items-center gap-3">
      <span className="text-lg font-bold">{title}</span>
      <AdminStatusPill status={docTone[doc.status]}>{t(`docStatuses.${doc.status}`)}</AdminStatusPill>
      {(doc.unanswered ?? 0) > 0 && <AdminStatusPill status="running">{t("thread.waiting")}</AdminStatusPill>}
      <span className="text-sm text-[var(--muted)]">{t("version", { n: doc.version })} · {when(doc.created_at)}</span>
    </summary>
    <div className="mt-4 grid gap-4">
      {doc.status === "rejected" && doc.note && <p className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6"><strong>{t("sentBack")}</strong> {doc.note}</p>}
      {episodes.length > 0 && <BeatsTable episodes={episodes} />}
      <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("readDoc")}</summary><div className="mt-3 max-h-[40rem] overflow-y-auto whitespace-pre-wrap text-sm leading-7">{doc.body_md}</div></details>
      {/* An approved document keeps its thread as a record; a new version the model writes from the discussion arrives through onChanged. */}
      <DiscussionThread seriesSlug={slug} subject={docSubject(doc.kind, doc.chapter_number)} canManage={canManage} readOnly={doc.status === "approved"} waiting={(doc.unanswered ?? 0) > 0} onPosted={onChanged} />
      {canManage && doc.status === "review" && <div className="grid gap-3 border-t border-[var(--line)] pt-4">
        <label className="grid gap-2 text-sm font-semibold">{t("note")}<textarea className={control} rows={3} value={note} disabled={busy} placeholder={t("notePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
        <div className="flex flex-wrap gap-3">
          <Button disabled={busy} onClick={() => void decide("approve")}>{busy ? t("saving") : t("approve")}</Button>
          <Button secondary disabled={busy || !note.trim()} onClick={() => void decide("reject")}>{t("reject")}</Button>
        </div>
      </div>}
      {canManage && <details className="rounded-2xl border border-[var(--line)] p-4" onToggle={(event) => { if ((event.target as HTMLDetailsElement).open && draft === null) setDraft(doc.body_md); }}>
        <summary className="cursor-pointer font-bold">{t("editDoc")}</summary>
        <div className="mt-3 grid gap-3">
          <p className="text-sm leading-6 text-[var(--muted)]">{t("editHelp")}</p>
          <textarea className={`${control} font-mono text-xs`} rows={16} value={draft ?? doc.body_md} disabled={busy} aria-label={t("editDoc")} onChange={(event) => setDraft(event.target.value)} />
          <div className="flex flex-wrap gap-3">
            <Button disabled={busy || draft === null || !draft.trim()} onClick={() => void save(true)}>{t("saveApprove")}</Button>
            <Button secondary disabled={busy || draft === null || !draft.trim()} onClick={() => void save(false)}>{t("saveReview")}</Button>
          </div>
        </div>
      </details>}
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    </div>
  </details>;
}

/** One series: its documents to approve, its controls, and the episode table. */
function SeriesPage({ slug, onBack, onOpenVideo }: { slug: string; onBack: () => void; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const manage = useAdminActionGuard("content.manage");
  const [series, setSeries] = useState<Series | null>(null);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [busy, setBusy] = useState("");
  const load = useCallback(() => {
    api<Series>(`/admin/video-automation/series/${slug}`).then((value) => { setSeries(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, [slug]);
  useRefresh(load);
  const act = async (what: string, request: () => Promise<unknown>) => {
    setBusy(what);
    setActionError("");
    try {
      await request();
      load();
    } catch (problem) {
      setActionError(t("actionError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  const patch = (body: Record<string, unknown>) => api(`/admin/video-automation/series/${slug}`, { method: "PATCH", body: JSON.stringify(body) });
  const skip = (number: number) => {
    if (!window.confirm(t("skipConfirm", { n: number }))) return;
    void act(`skip-${number}`, () => api(`/admin/video-automation/series/${slug}/episodes/${number}/skip`, { method: "POST" }));
  };
  const order = (doc: SeriesDoc) => (doc.kind === "setting" || doc.kind === "bible" ? 0 : doc.kind === "outline" ? 1 : 1 + doc.chapter_number);
  // A one-off is one episode planned from its bible: no chapters to plan, no episode count worth showing.
  const oneOff = series?.kind === "one-off";
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={onBack}><ArrowLeft aria-hidden size={18} />{t("back")}</Button></div>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {series && <>
      <header className="grid gap-2">
        <h2 className="flex flex-wrap items-center gap-3 text-2xl font-bold">{series.title}{oneOff && <AdminStatusPill status="active">{t("oneOff")}</AdminStatusPill>}<AdminStatusPill status={seriesTone[series.status]}>{t(`statuses.${statusKey(series)}`)}</AdminStatusPill><WaitingPills series={series} /></h2>
        <p className="text-sm text-[var(--muted)]">{oneOff ? "" : `${t("progress", { done: series.episodes_done, total: series.planned_episodes, chapters: series.chapters })} · `}{t("spend", { usd: Number(series.media_usd ?? 0).toFixed(2), seconds: series.clip_seconds ?? 0 })} · {t(`tones.${series.tone}`)} · {t(`presets.${series.style_preset}`)} · {t("minutesEach", { minutes: series.target_minutes })}</p>
        <p className="whitespace-pre-wrap text-sm leading-6">{series.premise}</p>
        {series.note && <p className="text-sm text-[var(--muted)]">{t("fields.note")}: {series.note}</p>}
        {manage.allowed && <div className="flex flex-wrap gap-3">
          {series.status === "active" && <Button secondary disabled={busy === "pause"} onClick={() => void act("pause", () => patch({ status: "paused" }))}>{t("pause")}</Button>}
          {series.status === "paused" && <Button secondary disabled={busy === "resume"} onClick={() => void act("resume", () => patch({ status: "active" }))}>{t("resume")}</Button>}
          {series.status === "active" && !oneOff && <Button secondary disabled={busy === "plan"} onClick={() => void act("plan", () => api(`/admin/video-automation/series/${slug}/actions/plan-next-chapter`, { method: "POST" }))}>{t("planNextChapter")}</Button>}
          {series.status === "active" && <Button secondary disabled={busy === "start"} onClick={() => void act("start", () => api(`/admin/video-automation/series/${slug}/actions/start-next`, { method: "POST" }))}>{t("startNext")}</Button>}
        </div>}
        {(series.requested_chapter || series.force_next) && <p className="text-sm text-[var(--muted)]">{series.requested_chapter ? t("chapterRequested", { n: series.requested_chapter }) : ""}{series.force_next ? ` ${t("nextForced")}` : ""}</p>}
        {actionError && <p role="alert" className="text-sm text-red-800">{actionError}</p>}
      </header>
      <section className="grid gap-4" aria-label={t("docsTitle")}>
        <h3 className="text-lg font-bold">{t("docsTitle")}</h3>
        {series.docs.length === 0 && <p className="text-sm text-[var(--muted)]">{oneOff ? t("bibleEmpty") : t("docsEmpty")}</p>}
        {[...series.docs].sort((a, b) => order(a) - order(b)).map((doc) => <DocPanel key={doc.id} slug={slug} doc={doc} canManage={manage.allowed} onChanged={load} />)}
      </section>
      <section className="grid gap-3" aria-label={t("episodesTitle")}>
        <h3 className="text-lg font-bold">{t("episodesTitle")}</h3>
        {series.episodes.length === 0 ? <p className="text-sm text-[var(--muted)]">{t("episodesEmpty")}</p> : <div className="overflow-x-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)]"><table className="min-w-full text-sm">
          <thead><tr className="text-left text-xs text-[var(--muted)]">{(["number", "chapter", "title", "status", "step", "pending", "spend", "actions"] as const).map((key) => <th key={key} className="px-3 py-2 font-semibold">{t(`episodeColumns.${key}`)}</th>)}</tr></thead>
          <tbody>{series.episodes.map((episode) => {
            const video = episode.video;
            const step = video ? (video.checklist.find((item) => !item.done)?.label ?? video.stage) : "";
            return <tr key={episode.number} className="border-t border-[var(--line)] align-top">
              <td className="px-3 py-2 font-mono">{episode.number}</td>
              <td className="px-3 py-2">{episode.chapter_number}</td>
              <td className="px-3 py-2"><span className="font-semibold">{episode.title}</span>{episode.logline && <span className="block text-xs text-[var(--muted)]">{episode.logline}</span>}</td>
              <td className="px-3 py-2"><AdminStatusPill status={episodeTone[episode.status]}>{t(`episodeStatuses.${episode.status}`)}</AdminStatusPill></td>
              <td className="px-3 py-2">{step}</td>
              <td className="px-3 py-2">{video?.pending ? t("pendingCount", { count: video.pending }) : ""}</td>
              <td className="px-3 py-2">{video && typeof video.media_usd === "number" ? `US$${video.media_usd.toFixed(2)}` : ""}</td>
              <td className="px-3 py-2"><span className="flex flex-wrap gap-2">
                {episode.slug && <Button secondary onClick={() => onOpenVideo(episode.slug as string)}>{t("openVideo")}</Button>}
                {manage.allowed && (episode.status === "planned" || episode.status === "ready") && <Button secondary disabled={busy === `skip-${episode.number}`} onClick={() => skip(episode.number)}>{t("skip")}</Button>}
              </span></td>
            </tr>;
          })}</tbody>
        </table></div>}
      </section>
    </>}
  </section>;
}

/** The drama tab: the series list, or one series when the query names it. */
export function AdminVideoSeries({ onOpenVideo }: { onOpenVideo: (slug: string) => void }) {
  const [slug, setSlug] = useAdminQueryValue("series", "", (value) => SERIES_SLUG.test(value));
  if (slug) return <SeriesPage slug={slug} onBack={() => setSlug("")} onOpenVideo={onOpenVideo} />;
  return <SeriesList onOpenSeries={setSlug} onOpenVideo={onOpenVideo} />;
}
