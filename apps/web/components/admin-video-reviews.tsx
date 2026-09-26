"use client";

import { ArrowLeft, CheckCircle2, Circle, Clapperboard } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import {
  control, type Project, type ProjectSummary, REFRESH_MS, ReviewCard, SLUG, fileUrl, useRefresh, useWhen,
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
        {project.series_slug && <p className="text-sm text-[var(--muted)]">{t("episodeOf", { series: project.series_slug, number: project.episode_number ?? 0 })}</p>}
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
      {live.length === 0 && !dropped && <p className="text-[var(--muted)]">{t("noPending")}</p>}
      {live.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={manage.allowed && !dropped} onDecided={load} />)}
      {past.length > 0 && <details className="grid gap-4"><summary className="cursor-pointer font-bold">{t("history")}</summary>
        <div className="mt-4 grid gap-4">{past.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={false} onDecided={load} />)}</div>
      </details>}
      {manage.allowed && !dropped && !project.youtube_video_id && <DropVideo slug={slug} onDropped={load} />}
    </>}
  </section>;
}

/** The tutorials (slides videos): dramas live on their own tab. */
function ProjectList({ onOpen }: { onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<ProjectSummary[]>("/admin/videos").then((value) => { setProjects(value.filter((project) => project.format !== "drama")); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, []);
  useRefresh(load);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (projects && projects.length === 0) return <AdminEmptyState title={t("empty")} detail={t("emptyDetail")} />;
  return <ul className="grid gap-4" aria-label={t("listTitle")}>
    {(projects ?? []).map((project) => <li key={project.slug}>
      <button type="button" onClick={() => onOpen(project.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
        <span className="flex flex-wrap items-center gap-3"><Clapperboard aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{project.title}</span>
          {project.dropped_at
            ? <AdminStatusPill status="inactive">{t("dropped")}</AdminStatusPill>
            : <AdminStatusPill status={project.pending ? "pending" : "inactive"}>{project.pending ? t("pending", { count: project.pending }) : t("noPendingShort")}</AdminStatusPill>}
        </span>
        <span className="text-sm text-[var(--muted)]">{t("progress", { done: project.checklist.filter((item) => item.done).length, total: project.checklist.length })} · {t("lastSynced", { time: when(project.last_synced_at) })}</span>
        {project.stage && !project.youtube_video_id && !project.dropped_at && <span className="text-sm text-[var(--muted)]">{t("currentStep", { step: project.checklist.find((item) => !item.done)?.label ?? project.stage })}</span>}
      </button>
    </li>)}
  </ul>;
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
