"use client";

import { BusFront, CarFront, ChevronRight, Footprints, Loader2, Route } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { dayTimelineCopy } from "@/components/planner/day-timeline-copy";
import type { DayTimelineEdge, RouteSegment, TravelMode } from "@/lib/trip-types";

const modeIcon: Record<TravelMode, typeof BusFront> = { transit: BusFront, walk: Footprints, drive: CarFront };

/** A connector describes one real edge; opening details never queries a provider. */
export function RouteTimelineLink({ edge, segment: saved, nextTitle, loading, stale, needsSetup, onClick }: {
  edge?: DayTimelineEdge;
  segment?: RouteSegment;
  nextTitle: string;
  loading?: boolean;
  stale?: boolean;
  timezone?: string;
  needsSetup?: "lodging" | "location";
  onClick: () => void;
}) {
  const t = useTranslations("trips.route");
  const copy = dayTimelineCopy(useLocale());
  const segment = edge ? edge.segment : saved;
  const hasDuration = segment && Number.isFinite(segment.duration_minutes) && segment.duration_minutes > 0;
  const isPlaceholder = segment?.provider === "estimate" || ["estimated", "failed", "unavailable"].includes(segment?.status || "");
  const status = needsSetup ? "pending" : edge?.status || (stale || segment?.status === "stale" ? "stale" : hasDuration && !isPlaceholder ? "ready" : "estimated");
  if (status === "pending" && (needsSetup || edge?.blocker)) return <div className="planner-route-connector planner-route-pending flex min-h-11 items-center gap-2 px-2 text-xs text-[var(--muted)]"><Route size={14} aria-hidden /><span>{copy.pending}</span></div>;
  if (loading) return <div className="planner-route-connector flex min-h-11 items-center gap-2 px-2 text-xs text-[var(--muted)]" aria-live="polite"><Loader2 size={14} className="animate-spin" aria-hidden /><span>{t("computing", { title: nextTitle })}</span></div>;
  const mode = edge?.travelMode || segment?.travel_mode || "transit";
  const Icon = modeIcon[mode];
  const minutes = segment?.duration_minutes;
  const label = status === "stale" ? copy.stale
    : status !== "ready" || !hasDuration || isPlaceholder ? copy.unqueried
      : segment?.provider === "manual" ? copy.manual.replace("{minutes}", String(minutes))
        : t("minutes", { minutes: minutes! });
  return <button type="button" onClick={onClick} aria-label={t("viewRoute", { title: nextTitle }) + " · " + label} className={"planner-route-connector flex min-h-11 w-full items-center gap-2 rounded-lg px-2 text-left text-xs text-[var(--muted)] hover:bg-[var(--paper)] " + (status === "stale" ? "planner-route-stale" : "")}>
    <Icon size={14} aria-hidden /><span>{t(`mode.${mode}`)}</span><strong className="font-medium">{label}</strong>
    {status === "pending" && <span>{copy.pending}</span>}
    {status === "ready" && Boolean(segment?.buffer_minutes) && <span>{t("buffer", { minutes: segment!.buffer_minutes! })}</span>}
    {segment?.is_override && <span className="sr-only">{t("override")}</span>}
    <ChevronRight size={14} className="ml-auto" aria-hidden />
  </button>;
}
