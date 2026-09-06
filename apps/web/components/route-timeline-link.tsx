"use client";

import { BusFront, CarFront, ChevronRight, Clock3, Footprints, Loader2, MapPinOff, Route, TriangleAlert } from "lucide-react";
import { useTranslations } from "next-intl";
import { formatTime, type RouteSegment, type TravelMode } from "@/lib/trip-types";

const modeIcon: Record<TravelMode, typeof BusFront> = {
  transit: BusFront,
  walk: Footprints,
  drive: CarFront,
};

export function RouteTimelineLink({
  segment,
  nextTitle,
  loading,
  stale,
  timezone,
  needsSetup,
  onClick,
}: {
  segment?: RouteSegment;
  nextTitle: string;
  loading?: boolean;
  stale?: boolean;
  timezone?: string;
  needsSetup?: "lodging" | "location";
  onClick: () => void;
}) {
  const t = useTranslations("trips.route");
  if (needsSetup) return <button type="button" onClick={onClick} className="route-timeline-empty route-timeline-blocked"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white text-amber-800"><MapPinOff size={16} /></span><span className="min-w-0 flex-1"><strong className="block">{needsSetup === "lodging" ? t("setupLodging") : t("setupLocation")}</strong><span className="mt-0.5 block truncate text-xs text-[var(--muted)]">{t("setupHint", { title: nextTitle })}</span></span><ChevronRight size={17} /></button>;
  if (loading) return <div className="route-timeline-loading" aria-live="polite"><Loader2 size={16} className="animate-spin" /><span>{t("computing", { title: nextTitle })}</span></div>;
  if (!segment || stale) return <button type="button" onClick={onClick} className="route-timeline-empty"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white text-[var(--teal)]"><Route size={16} /></span><span className="min-w-0 flex-1"><strong className="block">{stale ? t("stale") : t("choose")}</strong><span className="mt-0.5 block truncate text-xs text-[var(--muted)]">{t("chooseHint", { title: nextTitle })}</span></span><ChevronRight size={17} /></button>;

  const mode = segment.travel_mode || "transit";
  const Icon = modeIcon[mode];
  const lines = segment.steps.filter((step) => step.travel_mode === "TRANSIT").map((step) => step.line_short_name || step.line_name).filter(Boolean).join(" → ");
  return <button type="button" aria-label={t("viewRoute", { title: nextTitle })} onClick={onClick} className={`route-timeline-segment ${segment.status === "conflict" ? "route-timeline-conflict" : ""}`}><span className={`route-timeline-mode route-timeline-mode-${mode}`}><Icon size={17} /></span><span className="min-w-0 flex-1"><span className="flex flex-wrap items-center gap-2"><strong>{formatTime(segment.departure_time, undefined, timezone)} → {formatTime(segment.arrival_time, undefined, timezone)}</strong><span className="route-timeline-duration">{t("minutes", { minutes: segment.duration_minutes })}</span>{segment.buffer_minutes ? <span className="route-timeline-buffer">{t("buffer", { minutes: segment.buffer_minutes })}</span> : null}{segment.is_override && <span className="route-override-badge">{t("override")}</span>}</span><span className="mt-1 flex items-center gap-1.5 truncate text-xs text-[var(--muted)]"><Clock3 size={13} />{t(`mode.${mode}`)}{lines ? ` · ${lines}` : ""} · {t("readyAt", { time: formatTime(segment.ready_time, undefined, timezone) })}</span></span>{segment.status === "conflict" ? <TriangleAlert size={18} className="shrink-0 text-red-700" /> : <ChevronRight size={18} className="shrink-0 text-[var(--teal)]" />}</button>;
}
