"use client";

import { ExternalLink } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminStatusPill } from "@/components/admin-ui";
import { control, useRefresh, useWhen } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { api, ApiError } from "@/lib/api";

// The owner's requests for a slides video of one site article (docs/videos/AUTOMATION.md): the form
// on the tutorials tab files one, and the worker plans it before any scheduled draft. The server
// stores queued, started, done and cancelled; it also says done once the request's video is on
// YouTube, and dropped once that video was dropped.
type SlidesRequestStatus = "queued" | "started" | "done" | "cancelled" | "dropped";
export type SlidesRequest = {
  id: string; source_guide: string; title: string | null; url: string; note: string | null; status: SlidesRequestStatus; slug: string | null;
  created_by_user_id: string | null; created_at: string; started_at: string | null; finished_at: string | null; cancelled_at: string | null;
};

// The API's GUIDE_SLUG_PATTERN (apps/api/app/video_automation/schemas.py), so a slug the server
// would refuse never leaves the form.
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
const NOTE_MAX = 2000;
// Finished and withdrawn requests stay on the list for a week after they were filed, as the drama queue's do.
const RECENT_MS = 7 * 24 * 3600_000;
const tone: Record<SlidesRequestStatus, string> = { queued: "pending", started: "active", done: "ok", cancelled: "inactive", dropped: "inactive" };
const message = (problem: unknown) => (problem instanceof Error ? problem.message : "");

/**
 * The requests from an answer, whatever came back: an older page stub or a proxy may answer this
 * path with something that is not the list, and the tutorials list must not break on it.
 */
function requestsOf(value: unknown): SlidesRequest[] {
  const listed: unknown = value && typeof value === "object" ? (value as { requests?: unknown }).requests : undefined;
  if (!Array.isArray(listed)) return [];
  return listed.filter((each: unknown): each is SlidesRequest => {
    const row = each && typeof each === "object" ? each as Partial<SlidesRequest> : null;
    return typeof row?.id === "string" && typeof row.source_guide === "string" && typeof row.created_at === "string";
  });
}

/** A published life article's slug and a note for the planner; the server checks the article and the duplicates. */
function NewSlidesRequestForm({ onFiled }: { onFiled: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [guide, setGuide] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const slug = guide.trim();
  const guideOk = GUIDE_SLUG.test(slug);
  const file = async () => {
    setBusy(true);
    setError("");
    try {
      await api<SlidesRequest>("/admin/video-automation/slides-requests", {
        method: "POST",
        body: JSON.stringify({ source_guide: slug, note: note.trim() || undefined }),
      });
      setGuide(""); setNote("");
      onFiled();
    } catch (problem) {
      setError(t("slidesRequests.error", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("slidesRequests.title")}</summary>
    <form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); void file(); }} aria-label={t("slidesRequests.title")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("slidesRequests.help")}</p>
      <label className="grid gap-2 text-sm font-semibold">{t("slidesRequests.article")}
        <input className={control} value={guide} disabled={busy} maxLength={120} placeholder={t("slidesRequests.articlePlaceholder")} aria-invalid={Boolean(slug) && !guideOk} onChange={(event) => setGuide(event.target.value)} />
      </label>
      <label className="grid gap-2 text-sm font-semibold">{t("slidesRequests.note")}
        <textarea className={control} rows={2} value={note} disabled={busy} maxLength={NOTE_MAX} placeholder={t("slidesRequests.notePlaceholder")} onChange={(event) => setNote(event.target.value)} />
      </label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button type="submit" disabled={busy || !guideOk}>{busy ? t("saving") : t("slidesRequests.submit")}</Button></div>
    </form>
  </details>;
}

/** What the owner asked for and where each stands; a queued one can be withdrawn, a started one opens its video. */
function SlidesQueue({ requests, canManage, onChanged, onOpen }: { requests: SlidesRequest[]; canManage: boolean; onChanged: () => void; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const cancel = async (request: SlidesRequest) => {
    if (!window.confirm(t("cancelConfirm"))) return;
    setBusy(request.id);
    setError("");
    try {
      await api(`/admin/video-automation/slides-requests/${request.id}`, { method: "DELETE" });
      onChanged();
    } catch (problem) {
      setError(t("cancelError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  if (!requests.length) return null;
  // An h2 like the tutorials tab's other sections (the groups and the catalog), which it sits above.
  return <section className="grid gap-3" aria-label={t("slidesRequests.queue")}>
    <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{t("slidesRequests.queue")}</h2>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <ul className="grid gap-3">{requests.map((request) => <li key={request.id} className="grid gap-2 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
      <span className="flex flex-wrap items-center gap-3">
        <AdminStatusPill status={tone[request.status] ?? "inactive"}>{t(`slidesRequests.statuses.${request.status}`)}</AdminStatusPill>
        <span className="font-bold">{request.title || request.source_guide}</span>
        <span className="text-sm text-[var(--muted)]">{request.source_guide} · {t("filedAt", { time: when(request.created_at) })}</span>
      </span>
      {request.note && <span className="whitespace-pre-wrap text-sm text-[var(--muted)]">{t("slidesRequests.note")}: {request.note}</span>}
      <span className="flex flex-wrap items-center gap-3">
        {/^https:\/\//.test(request.url ?? "") && <a href={request.url} target="_blank" rel="noreferrer noopener" className="inline-flex min-h-11 items-center gap-2 text-sm font-semibold text-[var(--teal)] underline">{t("slidesRequests.openArticle")}<ExternalLink aria-hidden size={15} /></a>}
        {request.slug && <Button secondary onClick={() => onOpen(request.slug as string)}>{t("openVideo", { slug: request.slug })}</Button>}
        {canManage && request.status === "queued" && <Button secondary disabled={busy === request.id} onClick={() => void cancel(request)}>{busy === request.id ? t("saving") : t("cancelRequest")}</Button>}
      </span>
    </li>)}</ul>
  </section>;
}

/**
 * The top of the tutorials tab: the form that asks for a slides video of a site article (for a
 * content manager) and the queue of those requests. An API older than the route answers 404, and
 * then nothing shows; until the first answer nothing shows either, so the form never flashes.
 */
export function SlidesRequests({ onOpen }: { onOpen: (slug: string) => void }) {
  const manage = useAdminActionGuard("content.manage");
  const [requests, setRequests] = useState<SlidesRequest[] | null>(null);
  const [missing, setMissing] = useState(false);
  const load = useCallback(() => {
    api<unknown>("/admin/video-automation/slides-requests").then((value) => {
      // Queued and started ones stay however old; the rest drop off a week after they were filed.
      const recent = Date.now() - RECENT_MS;
      setRequests(requestsOf(value).filter((request) => request.status === "queued" || request.status === "started" || Date.parse(request.created_at) > recent));
      setMissing(false);
    }).catch((problem: unknown) => {
      if (problem instanceof ApiError && problem.status === 404) { setMissing(true); return; }
      // A failed refresh keeps the list it had; the tutorials list below reports an API that is down.
      setRequests((current) => current ?? []);
    });
  }, []);
  useRefresh(load);
  if (missing || requests === null) return null;
  if (!manage.allowed && requests.length === 0) return null;
  return <div className="grid gap-4">
    {manage.allowed && <NewSlidesRequestForm onFiled={load} />}
    <SlidesQueue requests={requests} canManage={manage.allowed} onChanged={load} onOpen={onOpen} />
  </div>;
}
