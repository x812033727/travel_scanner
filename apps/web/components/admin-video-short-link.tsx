"use client";

import { useLocale, useTranslations } from "next-intl";
import { type FormEvent, useState } from "react";
import { control, type Project, youtubeVideoId } from "@/components/admin-video-review-card";
import { syncRunning } from "@/components/admin-video-youtube";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";
import { shortLinkCopy } from "@/lib/admin-video-short-link-copy";

/**
 * A Short pushed by hand (a live final or publish review says `hand_pushed`): the owner uploads it,
 * so the page offers no send to YouTube for it. The server holds the same rule, and also counts a
 * link recorded before any package was approved (apps/api/app/video_shorts/hand_upload.py).
 */
export function handPushedShort(project: Project): boolean {
  return Boolean(project.shorts_line) && project.reviews.some((review) => (review.gate === "final" || review.gate === "publish")
    && (review.status === "pending" || review.status === "approved") && review.payload.hand_pushed === true);
}

/**
 * Whether the owner records a hand upload here: the cut is approved and the Short has no publish
 * time yet. One the worker made, with its package approved, goes the site's way instead.
 */
export function canRecordShortUpload(project: Project): boolean {
  if (!project.shorts_line || project.dropped_at || project.youtube_publish_at || syncRunning(project.youtube_sync)) return false;
  const final = project.reviews.find((review) => review.gate === "final" && !review.subject && (review.status === "pending" || review.status === "approved"));
  return final?.status === "approved" && (handPushedShort(project) || !project.publish_approved_at);
}

/**
 * The address of a Short uploaded by hand, and when it goes public. The form stays while there is
 * no time, filled with the recorded video, so the time can be added or a wrong address corrected.
 */
export function ShortLinkForm({ project, onLinked }: { project: Project; onLinked: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const copy = shortLinkCopy(useLocale());
  const [url, setUrl] = useState(project.youtube_video_id ?? "");
  const [publishAt, setPublishAt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [note, setNote] = useState("");
  const id = youtubeVideoId(url);
  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!id) return;
    setBusy(true);
    setError("");
    setNote("");
    try {
      // With no time typed the server asks YouTube, and says why when it found none.
      const saved = await api<{ youtube_publish_note?: string | null }>(`/admin/videos/${project.slug}/youtube`, {
        method: "POST",
        body: JSON.stringify({ url: url.trim(), publish_at: publishAt ? new Date(publishAt).toISOString() : null }),
      });
      setNote(saved.youtube_publish_note ?? "");
      onLinked();
    } catch (problem) {
      setError(t("uploadedError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <form onSubmit={(event) => void submit(event)} className="grid gap-3 rounded-2xl border border-[var(--line)] p-4" aria-label={copy.title}>
    <p className="font-bold">{copy.title}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{project.youtube_video_id ? copy.addTime : copy.help}</p>
    <label className="grid gap-2 text-sm font-semibold">{t("youtubeUrl")}
      <input className={control} value={url} disabled={busy} placeholder={t("youtubeUrlPlaceholder")} onChange={(event) => setUrl(event.target.value)} />
    </label>
    {url.trim() && <p className={`text-sm ${id ? "text-[var(--muted)]" : "text-amber-800"}`}>{id ? t("youtubeId", { id }) : t("youtubeUrlInvalid")}</p>}
    <label className="grid gap-2 text-sm font-semibold">{t("publishAt")}
      <input type="datetime-local" className={control} value={publishAt} disabled={busy} onChange={(event) => setPublishAt(event.target.value)} />
    </label>
    {note && <p role="status" className="text-sm text-amber-900">{note}</p>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <div><Button type="submit" disabled={busy || !id}>{busy ? t("saving") : copy.button}</Button></div>
  </form>;
}
