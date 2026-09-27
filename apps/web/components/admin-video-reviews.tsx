"use client";

import { ArrowLeft, CheckCircle2, Circle, Clapperboard, Upload } from "lucide-react";
import { useTranslations } from "next-intl";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import {
  control, DUB_LOCALES, isBlocked, mp4Retired, needsOwner, type Project, type ProjectSummary, REFRESH_MS, readyToUpload, ReviewCard, SLUG,
  UploadPackage, UploadedForm, fileUrl, useRefresh, useWhen,
} from "@/components/admin-video-review-card";
import { AdminVideoSeries } from "@/components/admin-video-series";
import { AdminVideoSettings } from "@/components/admin-video-settings";
import { Button, Tabs } from "@/components/community/ui";
import { useAdminQueryState, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The review card, the gate bodies and the shared types live in admin-video-review-card.tsx;
// these two are re-exported so older imports keep working. The drama tab (series and one-off
// episodes) is admin-video-series.tsx; this file holds the tutorial list, the video page and the tabs.
export { REFRESH_MS, fileUrl };

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
  const retired = project ? mp4Retired(project) : false;
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={onBack}><ArrowLeft aria-hidden size={18} />{t("back")}</Button></div>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {project && <>
      <header className="grid gap-2"><h2 className="text-2xl font-bold">{project.title}</h2>
        {project.series_slug && <p className="text-sm text-[var(--muted)]">{t("episodeOf", { series: project.series_slug, number: project.episode_number ?? 0 })}</p>}
        {project.youtube_video_id && <p className="text-sm">
          {t("youtube", { id: project.youtube_video_id })}
          {project.youtube_publish_at && ` · ${t("scheduledAt", { time: when(project.youtube_publish_at) })}`}
          <span className="block text-[var(--muted)]">{retired ? t("mp4Retired") : t("previewsGone")}</span>
        </p>}
        {project.dropped_at && <p role="status" className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">
          <strong>{t("droppedAt", { time: when(project.dropped_at) })}</strong>
          {project.dropped_note && <span className="block whitespace-pre-wrap">{project.dropped_note}</span>}
        </p>}
      </header>
      {project.checklist.length > 0 && <section aria-label={t("checklist")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
        <p className="font-bold">{t("checklist")}</p>
        <ul className="mt-2 grid gap-1 text-sm sm:grid-cols-2">{project.checklist.map((item) => <li key={item.key} className="flex items-center gap-2">{item.done ? <CheckCircle2 aria-hidden size={16} className="text-[var(--teal)]" /> : <Circle aria-hidden size={16} className="text-[var(--muted)]" />}<span className={item.done ? "" : "text-[var(--muted)]"}>{item.label}</span></li>)}</ul>
      </section>}
      {readyToUpload(project) && manage.allowed && <UploadedForm slug={slug} onLinked={load} />}
      {!dropped && (project.format ?? "slides") === "slides" && <DubLanguages key={(project.dub_locales ?? []).join(",")} slug={slug} project={project} canManage={manage.allowed} onSaved={load} />}
      {live.length === 0 && !dropped && <p className="text-[var(--muted)]">{t("noPending")}</p>}
      {live.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={manage.allowed && !dropped} onDecided={load} mp4Gone={retired} />)}
      {past.length > 0 && <details className="grid gap-4" open={readyToUpload(project)}><summary className="cursor-pointer font-bold">{t("history")}</summary>
        <div className="mt-4 grid gap-4">{past.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={false} onDecided={load} mp4Gone={retired} />)}</div>
      </details>}
      {manage.allowed && !dropped && !project.youtube_video_id && <DropVideo slug={slug} onDropped={load} />}
    </>}
  </section>;
}

/** One row of the list: the title, what state it is in, and where the worker is. */
function ProjectItem({ project, onOpen }: { project: ProjectSummary; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  return <li>
    <button type="button" onClick={() => onOpen(project.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
      <span className="flex flex-wrap items-center gap-3"><Clapperboard aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{project.title}</span>
        {project.dropped_at
          ? <AdminStatusPill status="inactive">{t("dropped")}</AdminStatusPill>
          : <AdminStatusPill status={project.pending ? "pending" : "inactive"}>{project.pending ? t("pending", { count: project.pending }) : t("noPendingShort")}</AdminStatusPill>}
        {!project.dropped_at && isBlocked(project) && <AdminStatusPill status="failed">{t("stuck")}</AdminStatusPill>}
        {readyToUpload(project) && <AdminStatusPill status="active">{t("readyToUpload")}</AdminStatusPill>}
      </span>
      <span className="text-sm text-[var(--muted)]">{t("progress", { done: project.checklist.filter((item) => item.done).length, total: project.checklist.length })} · {t("lastSynced", { time: when(project.last_synced_at) })}</span>
      {project.youtube_video_id && <span className="text-sm text-[var(--muted)]">{t("youtube", { id: project.youtube_video_id })}{project.youtube_publish_at && ` · ${t("scheduledAt", { time: when(project.youtube_publish_at) })}`}</span>}
      {project.stage && !project.youtube_video_id && !project.dropped_at && <span className="text-sm text-[var(--muted)]">{t("currentStep", { step: project.checklist.find((item) => !item.done)?.label ?? project.stage })}</span>}
    </button>
  </li>;
}

/**
 * A video whose upload confirmation is approved and that is not on YouTube yet: its package,
 * read from the approved publish review, and the form the owner fills in after uploading.
 */
function ReadyCard({ project, canManage, onOpen, onLinked }: { project: ProjectSummary; canManage: boolean; onOpen: (slug: string) => void; onLinked: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [detail, setDetail] = useState<Project | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let current = true;
    api<Project>(`/admin/videos/${project.slug}`)
      .then((value) => { if (current) { setDetail(value); setError(""); } })
      .catch((problem: unknown) => { if (current) setError(problem instanceof Error ? problem.message : ""); });
    return () => { current = false; };
  }, [project.slug, project.last_synced_at]);
  // Reviews come newest first, so the first approved confirmation is the current package.
  const confirmation = detail?.reviews.find((review) => review.gate === "publish" && review.status === "approved") ?? null;
  return <li>
    <article className="grid gap-4 rounded-[1.5rem] border border-[var(--teal)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" aria-label={project.title}>
      <header className="flex flex-wrap items-center gap-3">
        <Upload aria-hidden size={20} className="text-[var(--teal)]" />
        <h3 className="text-lg font-bold">{project.title}</h3>
        <AdminStatusPill status="active">{t("readyToUpload")}</AdminStatusPill>
        <Button secondary className="ml-auto" onClick={() => onOpen(project.slug)}>{t("openVideo", { slug: project.slug })}</Button>
      </header>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      {!detail && !error && <p className="text-sm text-[var(--muted)]">{t("readyLoading")}</p>}
      {confirmation && <UploadPackage slug={project.slug} review={confirmation} />}
      {canManage && <UploadedForm slug={project.slug} onLinked={onLinked} />}
    </article>
  </li>;
}

function Group({ title, children }: { title: string; children: ReactNode }) {
  return <section aria-label={title} className="grid gap-3">
    <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{title}</h2>
    <ul className="grid gap-4">{children}</ul>
  </section>;
}

/**
 * The tutorials (slides videos): dramas live on their own tab. What waits for the owner comes
 * first, then what is ready to upload, then the rest by state (docs/videos/HANDS-OFF.md).
 */
function ProjectList({ onOpen }: { onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const manage = useAdminActionGuard("content.manage");
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<ProjectSummary[]>("/admin/videos").then((value) => { setProjects(value.filter((project) => project.format !== "drama")); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, []);
  useRefresh(load);
  const groups = useMemo(() => {
    const listed = projects ?? [];
    const rest = listed.filter((project) => !needsOwner(project) && !readyToUpload(project));
    return {
      needs: listed.filter(needsOwner),
      ready: listed.filter((project) => !needsOwner(project) && readyToUpload(project)),
      working: rest.filter((project) => !project.youtube_video_id && !project.dropped_at),
      published: rest.filter((project) => Boolean(project.youtube_video_id) && !project.dropped_at),
      dropped: rest.filter((project) => Boolean(project.dropped_at)),
    };
  }, [projects]);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (projects && projects.length === 0) return <AdminEmptyState title={t("empty")} detail={t("emptyDetail")} />;
  const rows = (items: ProjectSummary[]) => items.map((project) => <ProjectItem key={project.slug} project={project} onOpen={onOpen} />);
  return <div className="grid gap-6" aria-label={t("listTitle")}>
    {groups.needs.length > 0 && <Group title={t("needsYou")}>{rows(groups.needs)}</Group>}
    {groups.ready.length > 0 && <Group title={t("readyToUpload")}>{groups.ready.map((project) => <ReadyCard key={project.slug} project={project} canManage={manage.allowed} onOpen={onOpen} onLinked={load} />)}</Group>}
    {groups.working.length > 0 && <Group title={t("inProgress")}>{rows(groups.working)}</Group>}
    {groups.published.length > 0 && <Group title={t("publishedSection")}>{rows(groups.published)}</Group>}
    {groups.dropped.length > 0 && <Group title={t("dropped")}>{rows(groups.dropped)}</Group>}
  </div>;
}

const TABS = ["reviews", "drama", "settings"] as const;

export function AdminVideoReviews() {
  const t = useTranslations("admin.videoReviews");
  const [slug, setSlug] = useAdminQueryValue("video", "", (value) => SLUG.test(value));
  const [tab, setTab] = useAdminQueryState("tab", TABS, "reviews");
  if (slug) return <ProjectDetail slug={slug} onBack={() => setSlug("")} />;
  return <div className="mt-6">
    <Tabs value={tab} onChange={(value) => setTab(value as (typeof TABS)[number])} label={t("tabsLabel")}
      items={[{ value: "reviews", label: t("tabReviews") }, { value: "drama", label: t("tabDrama") }, { value: "settings", label: t("tabSettings") }]}>
      {tab === "reviews" && <ProjectList onOpen={setSlug} />}
      {tab === "drama" && <AdminVideoSeries onOpenVideo={setSlug} />}
      {tab === "settings" && <AdminVideoSettings />}
    </Tabs>
  </div>;
}
