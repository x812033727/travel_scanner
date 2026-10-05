"use client";

import { useTranslations } from "next-intl";
import { AdminStatusPill } from "@/components/admin-ui";

export type VideoWorkerState = "not_adopted" | "registered" | "blocked" | "stopped" | "done" | "dropped" | "unavailable";
const TONES: Record<VideoWorkerState, string> = {
  not_adopted: "warning", registered: "queued", blocked: "failed", stopped: "warning",
  done: "inactive", dropped: "inactive", unavailable: "inactive",
};

/** The source is persisted worker registration; it cannot establish whether a process is alive. */
export function VideoProductionState({ state, compact = false }: { state: VideoWorkerState | null | undefined; compact?: boolean }) {
  const t = useTranslations("admin.videoReviews.production");
  // Older APIs omit this field; an absent field must not imply failed handoff.
  if (!state || !(state in TONES)) return null;
  const help = t(`help.${state}`);
  return <span className="inline-flex flex-wrap items-center gap-1" title={help}>
    <AdminStatusPill status={TONES[state]}>{t(`states.${state}`)}</AdminStatusPill>
    <span className={compact ? "sr-only" : "basis-full text-xs font-normal leading-5 text-[var(--muted)]"}>{help}</span>
  </span>;
}
