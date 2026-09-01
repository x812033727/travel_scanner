"use client";

import { BusFront, CarFront, ChevronRight, Clock3, Footprints, Loader2, Route, TriangleAlert } from "lucide-react";
import { formatTime, type RouteSegment, type TravelMode } from "@/lib/trip-types";

const modeIcon: Record<TravelMode, typeof BusFront> = {
  transit: BusFront,
  walk: Footprints,
  drive: CarFront,
};

const modeLabel: Record<TravelMode, string> = {
  transit: "大眾運輸",
  walk: "步行",
  drive: "汽車",
};

export function RouteTimelineLink({
  segment,
  nextTitle,
  loading,
  stale,
  onClick,
}: {
  segment?: RouteSegment;
  nextTitle: string;
  loading?: boolean;
  stale?: boolean;
  onClick: () => void;
}) {
  if (loading) return <div className="route-timeline-loading" aria-live="polite"><Loader2 size={16} className="animate-spin" /><span>正在計算前往 {nextTitle} 的移動時間…</span></div>;
  if (!segment || stale) return <button type="button" onClick={onClick} className="route-timeline-empty"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white text-[var(--teal)]"><Route size={16} /></span><span className="min-w-0 flex-1"><strong className="block">{stale ? "移動時間需要更新" : "選擇這段交通方式"}</strong><span className="mt-0.5 block truncate text-xs text-[var(--muted)]">前往 {nextTitle} · 大眾運輸／步行／汽車</span></span><ChevronRight size={17} /></button>;

  const mode = segment.travel_mode || "transit";
  const Icon = modeIcon[mode];
  const lines = segment.steps.filter((step) => step.travel_mode === "TRANSIT").map((step) => step.line_short_name || step.line_name).filter(Boolean).join(" → ");
  return <button type="button" aria-label={`查看前往 ${nextTitle} 的路線`} onClick={onClick} className={`route-timeline-segment ${segment.status === "conflict" ? "route-timeline-conflict" : ""}`}><span className={`route-timeline-mode route-timeline-mode-${mode}`}><Icon size={17} /></span><span className="min-w-0 flex-1"><span className="flex flex-wrap items-center gap-2"><strong>{formatTime(segment.departure_time)} → {formatTime(segment.arrival_time)}</strong><span className="route-timeline-duration">{segment.duration_minutes} 分</span>{segment.buffer_minutes ? <span className="route-timeline-buffer">＋緩衝 {segment.buffer_minutes} 分</span> : null}{segment.is_override && <span className="route-override-badge">單段</span>}</span><span className="mt-1 flex items-center gap-1.5 truncate text-xs text-[var(--muted)]"><Clock3 size={13} />{modeLabel[mode]}{lines ? ` · ${lines}` : ""} · {formatTime(segment.ready_time)} 可開始下一站</span></span>{segment.status === "conflict" ? <TriangleAlert size={18} className="shrink-0 text-red-700" /> : <ChevronRight size={18} className="shrink-0 text-[var(--teal)]" />}</button>;
}
