"use client";

import { ArrowLeft, CheckCircle2, Circle, Clapperboard } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { Button } from "@/components/community/ui";
import { useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// What the video pipeline reports (apps/api/app/video_reviews/schemas.py). Payloads come from
// tools/video/review; the page reads them defensively, since an older tool may send less.
type Gate = "outline" | "audio" | "final" | "publish";
type Status = "pending" | "approved" | "rejected" | "superseded";
type ReviewFile = { role: string; sha256: string; size: number; content_type: string };
type Review = {
  id: string; gate: Gate; content_sha256: string; summary: string; payload: Record<string, unknown>;
  files: ReviewFile[]; status: Status; choice: string | null; note: string | null;
  decided_at: string | null; created_at: string;
};
type ChecklistItem = { key: string; label: string; done: boolean };
type ProjectSummary = {
  slug: string; title: string; stage: string; checklist: ChecklistItem[];
  youtube_video_id: string | null; last_synced_at: string; pending: number;
};
type Project = ProjectSummary & { reviews: Review[] };

const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const statusTone: Record<Status, string> = { pending: "pending", approved: "active", rejected: "failed", superseded: "inactive" };
const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";

const record = (value: unknown): Record<string, unknown> => (value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {});
const list = (value: unknown): unknown[] => (Array.isArray(value) ? value : []);
const text = (value: unknown): string => (typeof value === "string" ? value : typeof value === "number" ? String(value) : "");
const count = (value: unknown): number => (typeof value === "number" && Number.isFinite(value) ? value : 0);

export function fileUrl(slug: string, file: ReviewFile | undefined): string | undefined {
  return file ? `/api/admin-video-files/${slug}/${file.sha256}` : undefined;
}

const fileFor = (review: Review, role: string) => review.files.find((file) => file.role === role);

function useWhen() {
  const locale = useLocale();
  const formatter = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  return (value: string) => formatter.format(new Date(value));
}

function OutlineBody({ review, choice, onChoice, disabled }: { review: Review; choice: string; onChoice: (key: string) => void; disabled: boolean }) {
  const t = useTranslations("admin.videoReviews");
  const options = list(review.payload.options).map(record).filter((option) => text(option.key));
  const brief = text(review.payload.brief);
  return <div className="grid gap-4">
    {options.length > 0 && <fieldset className="grid gap-3" disabled={disabled || review.status !== "pending"}>
      <legend className="font-bold">{t("chooseOption")}</legend>
      {options.map((option) => {
        const key = text(option.key);
        const selected = (review.status === "pending" ? choice : review.choice) === key;
        return <label key={key} className={`grid gap-1 rounded-2xl border p-4 ${selected ? "border-[var(--teal)] bg-[var(--paper)]" : "border-[var(--line)]"}`}>
          <span className="flex items-center gap-3 font-bold"><input type="radio" name={`outline-${review.id}`} value={key} checked={selected} onChange={() => onChoice(key)} />{t("option", { key })}{text(option.title) && `: ${text(option.title)}`}</span>
          {text(option.summary) && <span className="text-sm leading-6 text-[var(--muted)]">{text(option.summary)}</span>}
          {text(option.hook) && <span className="text-sm leading-6"><strong>{t("hook")}</strong> {text(option.hook)}</span>}
        </label>;
      })}
    </fieldset>}
    {brief && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("brief")}</summary><div className="mt-3 max-h-[32rem] overflow-y-auto whitespace-pre-wrap text-sm leading-7">{brief}</div></details>}
  </div>;
}

function AudioBody({ slug, review }: { slug: string; review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const check = record(review.payload.check);
  const flagged = list(review.payload.flagged_lines).map(record);
  const src = fileUrl(slug, fileFor(review, "narration"));
  return <div className="grid gap-4">
    {src && <label className="grid gap-2 font-bold">{t("narration")}<audio controls preload="metadata" src={src} className="w-full" /></label>}
    {Object.keys(check).length > 0 && <p className="leading-7">
      <strong>{t("check")}</strong>{" "}
      {t("checkSummary", { lines: count(check.lines), exact: count(check.exact), alike: count(check.alike), judged: count(check.judged_fine), flagged: count(check.flagged) })}
    </p>}
    {flagged.length > 0 && <div className="grid gap-2"><p className="font-bold">{t("flaggedLines")}</p>
      <ul className="grid gap-2">{flagged.map((line) => <li key={text(line.id)} className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">
        <span className="block">{t("script")}: {text(line.script)}</span><span className="block">{t("heard")}: {text(line.heard)}</span>
      </li>)}</ul>
    </div>}
  </div>;
}

function FinalBody({ slug, review }: { slug: string; review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const checks = record(review.payload.checks);
  const problems = list(checks.problems).map(text).filter(Boolean);
  const chapters = list(review.payload.chapters).map(record);
  const metadata = Object.entries(record(review.payload.metadata)).map(([locale, value]) => [locale, record(value)] as const);
  const video = fileUrl(slug, fileFor(review, "preview"));
  const sheet = fileUrl(slug, fileFor(review, "contact_sheet"));
  const poster = fileUrl(slug, fileFor(review, "thumbnail"));
  return <div className="grid gap-4">
    {video && <label className="grid gap-2 font-bold">{t("preview")}<video controls preload="metadata" src={video} poster={poster} className="aspect-video w-full rounded-xl bg-black" /></label>}
    {Object.keys(checks).length > 0 && <p className="leading-7"><strong>{t("checks")}</strong>{" "}{checks.ok === true ? t("checksOk") : problems.join("; ")}</p>}
    {chapters.length > 0 && <div><p className="font-bold">{t("chapters")}</p><ol className="mt-2 grid gap-1 text-sm">{chapters.map((chapter, index) => <li key={index}><span className="font-mono">{text(chapter.time)}</span> {text(chapter.title)}</li>)}</ol></div>}
    {sheet && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("contactSheet")}</summary>
      {/* A private, session-bound preview: the image optimizer cannot fetch it. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={sheet} alt={t("contactSheet")} className="mt-3 w-full rounded-xl" loading="lazy" />
    </details>}
    {metadata.length > 0 && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("metadata")}</summary>
      <dl className="mt-3 grid gap-3">{metadata.map(([locale, values]) => <div key={locale}><dt className="font-mono text-xs text-[var(--muted)]">{locale}</dt><dd className="font-semibold">{text(values.title)}</dd><dd className="whitespace-pre-wrap text-sm leading-6">{text(values.description)}</dd></div>)}</dl>
    </details>}
  </div>;
}

function PublishBody({ review }: { review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const items = list(review.payload.checklist).map(text).filter(Boolean);
  return items.length ? <div><p className="font-bold">{t("uploadChecklist")}</p><ul className="mt-2 grid gap-1 text-sm leading-6">{items.map((item) => <li key={item}>• {item}</li>)}</ul></div> : null;
}

function ReviewCard({ slug, review, canManage, onDecided }: { slug: string; review: Review; canManage: boolean; onDecided: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [choice, setChoice] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const pending = review.status === "pending";
  const needsChoice = review.gate === "outline" && list(review.payload.options).length > 0;
  const decide = async (decision: "approve" | "reject") => {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${slug}/reviews/${review.id}/decision`, {
        method: "POST",
        body: JSON.stringify({ decision, choice: decision === "approve" && needsChoice ? choice : undefined, note: note.trim() || undefined }),
      });
      onDecided();
    } catch (problem) {
      setError(t("decideError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  const approveLabel = review.gate === "outline" ? t("approveOutline") : review.gate === "publish" ? t("approvePublish") : t("approve");
  return <article className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" aria-label={t(`gates.${review.gate}`)}>
    <header className="flex flex-wrap items-center gap-3">
      <h3 className="text-lg font-bold">{t(`gates.${review.gate}`)}</h3>
      <AdminStatusPill status={statusTone[review.status]}>{t(`statuses.${review.status}`)}</AdminStatusPill>
      <span className="text-sm text-[var(--muted)]">{t("submittedAt", { time: when(review.created_at) })}</span>
    </header>
    <p className="mt-2 leading-7">{review.summary}</p>
    <div className="mt-4">
      {review.gate === "outline" && <OutlineBody review={review} choice={choice} onChoice={setChoice} disabled={!canManage || busy} />}
      {review.gate === "audio" && <AudioBody slug={slug} review={review} />}
      {review.gate === "final" && <FinalBody slug={slug} review={review} />}
      {review.gate === "publish" && <PublishBody review={review} />}
    </div>
    {pending ? <div className="mt-5 grid gap-3 border-t border-[var(--line)] pt-4">
      <label className="grid gap-2 text-sm font-semibold">{t("note")}
        <textarea className={control} rows={3} value={note} disabled={!canManage || busy} placeholder={t("notePlaceholder")} onChange={(event) => setNote(event.target.value)} />
      </label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div className="flex flex-wrap gap-3">
        <Button disabled={!canManage || busy || (needsChoice && !choice)} onClick={() => void decide("approve")}>{busy ? t("saving") : approveLabel}</Button>
        <Button secondary disabled={!canManage || busy || !note.trim()} onClick={() => void decide("reject")}>{t("reject")}</Button>
      </div>
    </div> : review.decided_at && <p className="mt-4 border-t border-[var(--line)] pt-4 text-sm leading-6">
      {t("decidedAt", { time: when(review.decided_at) })}
      {review.choice && ` · ${t("choice", { key: review.choice })}`}
      {review.note && <span className="block whitespace-pre-wrap">{review.note}</span>}
    </p>}
  </article>;
}

function ProjectDetail({ slug, onBack }: { slug: string; onBack: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const manage = useAdminActionGuard("content.manage");
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Project>(`/admin/videos/${slug}`).then((value) => { setProject(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, [slug]);
  useEffect(load, [load]);
  const live = project?.reviews.filter((review) => review.status === "pending") ?? [];
  const past = project?.reviews.filter((review) => review.status !== "pending") ?? [];
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={onBack}><ArrowLeft aria-hidden size={18} />{t("back")}</Button></div>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {project && <>
      <header className="grid gap-2"><h2 className="text-2xl font-bold">{project.title}</h2>
        {project.youtube_video_id && <p className="text-sm">{t("youtube", { id: project.youtube_video_id })} · {t("previewsGone")}</p>}
      </header>
      {project.checklist.length > 0 && <section aria-label={t("checklist")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
        <p className="font-bold">{t("checklist")}</p>
        <ul className="mt-2 grid gap-1 text-sm sm:grid-cols-2">{project.checklist.map((item) => <li key={item.key} className="flex items-center gap-2">{item.done ? <CheckCircle2 aria-hidden size={16} className="text-[var(--teal)]" /> : <Circle aria-hidden size={16} className="text-[var(--muted)]" />}<span className={item.done ? "" : "text-[var(--muted)]"}>{item.label}</span></li>)}</ul>
      </section>}
      {live.length === 0 && <p className="text-[var(--muted)]">{t("noPending")}</p>}
      {live.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={manage.allowed} onDecided={load} />)}
      {past.length > 0 && <details className="grid gap-4"><summary className="cursor-pointer font-bold">{t("history")}</summary>
        <div className="mt-4 grid gap-4">{past.map((review) => <ReviewCard key={review.id} slug={slug} review={review} canManage={false} onDecided={load} />)}</div>
      </details>}
    </>}
  </section>;
}

export function AdminVideoReviews() {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [slug, setSlug] = useAdminQueryValue("video", "", (value) => SLUG.test(value));
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<ProjectSummary[]>("/admin/videos").then((value) => { setProjects(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, []);
  useEffect(() => { if (!slug) load(); }, [slug, load]);
  if (slug) return <ProjectDetail slug={slug} onBack={() => setSlug("")} />;
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (projects && projects.length === 0) return <AdminEmptyState title={t("empty")} detail={t("emptyDetail")} />;
  return <ul className="mt-6 grid gap-4" aria-label={t("listTitle")}>
    {(projects ?? []).map((project) => <li key={project.slug}>
      <button type="button" onClick={() => setSlug(project.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
        <span className="flex flex-wrap items-center gap-3"><Clapperboard aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{project.title}</span>
          <AdminStatusPill status={project.pending ? "pending" : "inactive"}>{project.pending ? t("pending", { count: project.pending }) : t("noPendingShort")}</AdminStatusPill>
        </span>
        <span className="text-sm text-[var(--muted)]">{t("progress", { done: project.checklist.filter((item) => item.done).length, total: project.checklist.length })} · {t("lastSynced", { time: when(project.last_synced_at) })}</span>
      </button>
    </li>)}
  </ul>;
}
