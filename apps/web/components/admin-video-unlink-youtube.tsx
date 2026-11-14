"use client";

import { Unlink } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { type ProjectSummary, publishState } from "@/components/admin-video-review-card";
import { syncRunning } from "@/components/admin-video-youtube";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

/**
 * Whether the owner may take the YouTube link off: only in the "linked, no publish time" state
 * (a scheduled or public video keeps its link) and not while a send to YouTube is running, the
 * same rules DELETE /admin/videos/{slug}/youtube enforces (apps/api/app/video_reviews/admin_service.py
 * unlink_youtube).
 */
export function canUnlinkYoutube(project: ProjectSummary): boolean {
  return publishState(project) === "linked" && !syncRunning(project.youtube_sync);
}

/**
 * A remade cut was pushed again while the old upload's id is still recorded: unlinking puts the
 * video back to waiting for an upload, so the new cut can be uploaded and linked (owner, 2026-11-14).
 */
export function UnlinkYoutube({ project, onUnlinked }: { project: ProjectSummary; onUnlinked: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  if (!canUnlinkYoutube(project)) return null;
  const id = project.youtube_video_id ?? "";
  const unlink = async () => {
    if (!window.confirm(t("unlinkConfirm", { id }))) return;
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${project.slug}/youtube`, { method: "DELETE" });
      onUnlinked();
    } catch (problem) {
      setError(t("unlinkError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <section className="grid gap-3 rounded-2xl border border-[var(--line)] p-4" aria-label={t("unlinkTitle")}>
    <p className="font-bold">{t("unlinkTitle")}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("unlinkHelp", { id })}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <div><Button secondary disabled={busy} onClick={() => void unlink()}><Unlink aria-hidden size={18} />{busy ? t("saving") : t("unlinkButton")}</Button></div>
  </section>;
}
