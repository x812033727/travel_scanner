"use client";

import { ArrowLeft, CheckCircle2, Circle, Clapperboard } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import {
  control, DUB_LOCALES, type Project, type ProjectSummary, REFRESH_MS, ReviewCard, SLUG, fileUrl, useRefresh, useWhen,
} from "@/components/admin-video-review-card";
import { AdminVideoSettings } from "@/components/admin-video-settings";
import { Button, Tabs } from "@/components/community/ui";
import { useAdminQueryState, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The review card, the gate bodies and the shared types live in admin-video-review-card.tsx;
// these two are re-exported so older imports keep working.
export { REFRESH_MS, fileUrl };

// The owner's drama requests (apps/api/app/video_automation/requests.py): an episode to make next,
// which the worker on the host claims before any scheduled draft (docs/videos/DRAMA.md).
type RequestStatus = "queued" | "started" | "done" | "cancelled";
type DramaRequest = {
  id: string; premise: string; title: string | null; source_guide: string | null; style_preset: string; target_minutes: number;
  note: string | null; status: RequestStatus; slug: string | null; created_at: string; started_at: string | null; finished_at: string | null; cancelled_at: string | null;
};
const REQUEST_PRESETS = ["cinematic-3d", "anime-2d", "ink-wash", "custom"] as const;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;

/** Stop a video for good, with a reason; the pipeline leaves it and its topic stays taken. */
function DropVideo({ slug, onDropped }: { slug: string; onDropped: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const drop = async () => {
    if (!note.trim() || !window.confirm(t("dropConfirm"))) return;
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${slug}/drop`, { method: "POST", body: JSON.stringify({ note: note.trim() }) });
      onDropped();
    } catch (problem) {
      setError(t("dropError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-2xl border border-[var(--line)] p-4">
    <summary className="cursor-pointer font-bold">{t("dropTitle")}</summary>
    <div className="mt-3 grid gap-3">
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dropDetail")}</p>
      <label className="grid gap-2 text-sm font-semibold">{t("dropReason")}
        <textarea className={control} rows={2} value={note} disabled={busy} placeholder={t("dropPlaceholder")} onChange={(event) => setNote(event.target.value)} />
      </label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button secondary disabled={busy || !note.trim()} onClick={() => void drop()}>{busy ? t("saving") : t("dropButton")}</Button></div>
    </div>
  </details>;
}

/**
 * The languages to dub this video in (docs/videos/DUBS.md). Every video is made in Traditional
 * Chinese; the worker makes a track for each ticked language once the final cut is approved and
 * sends them back as a card, and the owner uploads them in YouTube Studio. Ticking is allowed
 * before or after the video is public.
 */
function DubLanguages({ slug, project, canManage, onSaved }: { slug: string; project: Project; canManage: boolean; onSaved: () => void }) {
  const t = useTranslations("admin.videoReviews");
  // The parent keys this section by the saved languages, so a save (or another admin's) remounts
  // it with the new boxes while an edit in progress survives the page's minute-by-minute reads.
  const saved = (project.dub_locales ?? []).join(",");
  const [chosen, setChosen] = useState<string[]>(project.dub_locales ?? []);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const ordered = DUB_LOCALES.filter((locale) => chosen.includes(locale));
  const changed = ordered.join(",") !== saved;
  const toggle = (locale: string) => setChosen((current) => (current.includes(locale) ? current.filter((each) => each !== locale) : [...current, locale]));
  const save = async () => {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      await api(`/admin/videos/${slug}/dubs`, { method: "PUT", body: JSON.stringify({ locales: ordered }) });
      setMessage(t("dubsSaved"));
      onSaved();
    } catch (problem) {
      setError(t("dubsError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <section aria-label={t("dubsTitle")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <p className="font-bold">{t("dubsTitle")}</p>
    <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("dubsHelp")}</p>
    <div className="mt-3 flex flex-wrap gap-4">
      {DUB_LOCALES.map((locale) => <label key={locale} className="inline-flex items-center gap-2 text-sm font-semibold">
        <input type="checkbox" checked={chosen.includes(locale)} disabled={!canManage || busy} onChange={() => toggle(locale)} />{t(`locales.${locale}`)}
      </label>)}
    </div>
    {error && <p role="alert" className="mt-2 text-sm text-red-800">{error}</p>}
    {message && !error && <p role="status" className="mt-2 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-3"><Button disabled={!canManage || busy || !changed} onClick={() => void save()}>{busy ? t("saving") : t("dubsSave")}</Button></div>
  </section>;
}

function ProjectDetail({ slug, onBack }: { slug: string; onBack: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const manage = useAdminActionGuard("content.manage");
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Project>(`/admin/videos/${slug}`).then((value) => { setProject(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, [slug]);
  useRefresh(load);
  const live = project?.reviews.filter((review) => review.status === "pending") ?? [];
  const past = project?.reviews.filter((review) => review.status !== "pending") ?? [];
  const dropped = Boolean(project?.dropped_at);
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={onBack}><ArrowLeft aria-hidden size={18} />{t("back")}</Button></div>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {project && <>
      <header className="grid gap-2"><h2 className="text-2xl font-bold">{project.title}</h2>
        {project.youtube_video_id && <p className="text-sm">{t("youtube", { id: project.youtube_video_id })} · {t("previewsGone")}</p>}
        {project.dropped_at && <p role="status" className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">
          <strong>{t("droppedAt", { time: when(project.dropped_at) })}</strong>
          {project.dropped_note && <span className="block whitespace-pre-wrap">{project.dropped_note}</span>}
        </p>}
      </header>
      {project.checklist.length > 0 && <section aria-label={t("checklist")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
        <p className="font-bold">{t("checklist")}</p>
        <ul className="mt-2 grid gap-1 text-sm sm:grid-cols-2">{project.checklist.map((item) => <li key={item.key} className="flex items-center gap-2">{item.done ? <CheckCircle2 aria-hidden size={16} className="text-[var(--teal)]" /> : <Circle aria-hidden size={16} className="text-[var(--muted)]" />}<span className={item.done ? "" : "text-[var(--muted)]"}>{item.label}</span></li>)}</ul>
      </section>}
      {!dropped && (project.format ?? "slides") === "slides" && <DubLanguages key={(project.dub_locales ?? []).join(",")} slug={slug} project={project} canManage={manage.allowed} onSaved={load} />}
      {live.length === 0 && !dropped && <p className="text-[var(--muted)]">{t("noPending")}</p>}
      {live.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={manage.allowed && !dropped} onDecided={load} />)}
      {past.length > 0 && <details className="grid gap-4"><summary className="cursor-pointer font-bold">{t("history")}</summary>
        <div className="mt-4 grid gap-4">{past.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={false} onDecided={load} />)}</div>
      </details>}
      {manage.allowed && !dropped && !project.youtube_video_id && <DropVideo slug={slug} onDropped={load} />}
    </>}
  </section>;
}

/** Ask for an episode: a premise (or an article to adapt), a style and a length; the worker starts it next. */
function NewDramaForm({ onFiled }: { onFiled: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [premise, setPremise] = useState("");
  const [title, setTitle] = useState("");
  const [guide, setGuide] = useState("");
  const [preset, setPreset] = useState<(typeof REQUEST_PRESETS)[number]>("cinematic-3d");
  const [minutes, setMinutes] = useState(3);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const guideOk = !guide.trim() || GUIDE_SLUG.test(guide.trim());
  const file = async () => {
    setBusy(true);
    setError("");
    try {
      await api("/admin/video-automation/drama-requests", {
        method: "POST",
        body: JSON.stringify({ premise: premise.trim(), title: title.trim() || undefined, source_guide: guide.trim() || undefined, style_preset: preset, target_minutes: minutes, note: note.trim() || undefined }),
      });
      setPremise(""); setTitle(""); setGuide(""); setNote("");
      onFiled();
    } catch (problem) {
      setError(t("newDramaError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("newDrama")}</summary>
    <form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); void file(); }} aria-label={t("newDrama")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("newDramaHelp")}</p>
      <label className="grid gap-2 text-sm font-semibold">{t("premise")}
        <textarea className={control} rows={4} value={premise} disabled={busy} maxLength={4000} placeholder={t("premisePlaceholder")} onChange={(event) => setPremise(event.target.value)} />
      </label>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("workingTitle")}<input className={control} value={title} disabled={busy} maxLength={200} onChange={(event) => setTitle(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("sourceGuide")}<input className={control} value={guide} disabled={busy} placeholder={t("sourceGuidePlaceholder")} aria-invalid={!guideOk} onChange={(event) => setGuide(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("stylePreset")}
          <select className={control} value={preset} disabled={busy} onChange={(event) => setPreset(event.target.value as (typeof REQUEST_PRESETS)[number])}>
            {REQUEST_PRESETS.map((each) => <option key={each} value={each}>{t(`presets.${each}`)}</option>)}
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

const requestTone: Record<RequestStatus, string> = { queued: "pending", started: "active", done: "inactive", cancelled: "inactive" };

/** What the owner asked for and where each request stands; a queued one can still be withdrawn. */
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
      setError(t("cancelError", { message: problem instanceof Error ? problem.message : "" }));
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

function ProjectList({ onOpen }: { onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const manage = useAdminActionGuard("content.manage");
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [requests, setRequests] = useState<DramaRequest[]>([]);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<ProjectSummary[]>("/admin/videos").then((value) => { setProjects(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
    // A site from before the drama route answers 404 here: the queue then simply stays empty.
    // Finished and withdrawn requests drop off the queue after a week; the videos they became stay in the list.
    api<{ requests: DramaRequest[] }>("/admin/video-automation/drama-requests").then((value) => {
      const recent = Date.now() - 7 * 24 * 3600_000;
      setRequests((value.requests ?? []).filter((request) => request.status === "queued" || request.status === "started" || Date.parse(request.created_at) > recent));
    }).catch(() => setRequests([]));
  }, []);
  useRefresh(load);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  const controls = <>
    {manage.allowed && <NewDramaForm onFiled={load} />}
    <DramaQueue requests={requests} canManage={manage.allowed} onChanged={load} onOpen={onOpen} />
  </>;
  if (projects && projects.length === 0) return <div className="grid gap-4">{controls}<AdminEmptyState title={t("empty")} detail={t("emptyDetail")} /></div>;
  return <div className="grid gap-4">{controls}<ul className="grid gap-4" aria-label={t("listTitle")}>
    {(projects ?? []).map((project) => <li key={project.slug}>
      <button type="button" onClick={() => onOpen(project.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
        <span className="flex flex-wrap items-center gap-3"><Clapperboard aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{project.title}</span>
          {project.format === "drama" && <AdminStatusPill status="active">{t("drama")}</AdminStatusPill>}
          {project.dropped_at
            ? <AdminStatusPill status="inactive">{t("dropped")}</AdminStatusPill>
            : <AdminStatusPill status={project.pending ? "pending" : "inactive"}>{project.pending ? t("pending", { count: project.pending }) : t("noPendingShort")}</AdminStatusPill>}
        </span>
        <span className="text-sm text-[var(--muted)]">{t("progress", { done: project.checklist.filter((item) => item.done).length, total: project.checklist.length })} · {t("lastSynced", { time: when(project.last_synced_at) })}{project.format === "drama" && typeof project.media_usd === "number" && ` · ${t("spend", { usd: project.media_usd.toFixed(2), seconds: project.clip_seconds ?? 0 })}`}</span>
        {project.stage && !project.youtube_video_id && !project.dropped_at && <span className="text-sm text-[var(--muted)]">{t("currentStep", { step: project.checklist.find((item) => !item.done)?.label ?? project.stage })}</span>}
      </button>
    </li>)}
  </ul></div>;
}

const TABS = ["reviews", "settings"] as const;

export function AdminVideoReviews() {
  const t = useTranslations("admin.videoReviews");
  const [slug, setSlug] = useAdminQueryValue("video", "", (value) => SLUG.test(value));
  const [tab, setTab] = useAdminQueryState("tab", TABS, "reviews");
  if (slug) return <ProjectDetail slug={slug} onBack={() => setSlug("")} />;
  return <div className="mt-6">
    <Tabs value={tab} onChange={(value) => setTab(value as (typeof TABS)[number])} label={t("tabsLabel")}
      items={[{ value: "reviews", label: t("tabReviews") }, { value: "settings", label: t("tabSettings") }]}>
      {tab === "reviews" ? <ProjectList onOpen={setSlug} /> : <AdminVideoSettings />}
    </Tabs>
  </div>;
}
