"use client";

import {
  BusFront,
  CarFront,
  ChevronDown,
  CircleDollarSign,
  Clock3,
  ExternalLink,
  Footprints,
  MapPin,
  Route,
  TrainFront,
  TriangleAlert,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";
import { safeExternalHref } from "@/lib/navigation";
import { formatTime, type RouteSegment, type TravelMode } from "@/lib/trip-types";

type Translator = ReturnType<typeof useTranslations>;

const modeCopy: Record<TravelMode, { key: string; icon: typeof TrainFront; tone: string }> = {
  transit: { key: "modeTransit", icon: TrainFront, tone: "bg-sky-50 text-sky-700" },
  walk: { key: "modeWalk", icon: Footprints, tone: "bg-emerald-50 text-emerald-700" },
  drive: { key: "modeDrive", icon: CarFront, tone: "bg-orange-50 text-orange-700" },
};

function distanceLabel(t: Translator, meters?: number | null) {
  if (meters == null) return null;
  if (meters < 1000) return t("metres", { value: meters });
  return t("kilometres", { value: (meters / 1000).toFixed(meters >= 10_000 ? 0 : 1) });
}

function stepIcon(mode: string) {
  if (mode === "TRANSIT") return BusFront;
  if (mode === "DRIVE") return CarFront;
  return Footprints;
}

export function RouteSegmentCard({
  segment,
  selected,
  onSelect,
  defaultExpanded = false,
  timezone,
}: {
  segment: RouteSegment;
  selected?: boolean;
  onSelect?: () => void;
  defaultExpanded?: boolean;
  timezone?: string;
}) {
  const t = useTranslations("trips.route");
  const locale = useLocale();
  const [expanded, setExpanded] = useState(defaultExpanded);
  const transitSteps = segment.steps.filter((step) => step.travel_mode === "TRANSIT");
  const mode = segment.travel_mode || (transitSteps.length ? "transit" : "walk");
  const modeMeta = modeCopy[mode];
  const ModeIcon = modeMeta.icon;
  const lines = transitSteps.map((step) => step.line_short_name || step.line_name).filter(Boolean).join(" → ");
  const hasConflict = segment.status === "conflict";
  const expired = Boolean(segment.expires_at && new Date(segment.expires_at) < new Date());
  const mapsLabel = segment.provider === "naver_maps" || segment.provider === "odsay" || /NAVER|ODsay/i.test(segment.attribution)
    ? t("openInNaver")
    : t("openInGoogle");

  return <article className={`route-detail-card ${selected ? "route-detail-card-selected" : ""}`}>
    <button type="button" aria-expanded={expanded} onClick={() => { setExpanded(!expanded); onSelect?.(); }} className="flex min-h-14 w-full items-start justify-between gap-3 text-left">
      <span className="flex min-w-0 items-start gap-3"><span className={`grid h-11 w-11 shrink-0 place-items-center rounded-2xl ${modeMeta.tone}`}><ModeIcon size={20} /></span><span className="min-w-0"><span className="flex flex-wrap items-center gap-2"><strong className="text-base">{t(modeMeta.key)} · {t("durationMinutes", { minutes: segment.duration_minutes })}</strong>{segment.is_override && <span className="route-override-badge">{t("overrideBadge")}</span>}{expired && <span className="route-stale-badge">{t("staleBadge")}</span>}</span><span className="mt-1 block truncate text-xs text-[var(--muted)]">{lines || distanceLabel(t, segment.distance_meters) || t("seeSteps")}</span></span></span>
      <ChevronDown size={17} className={`mt-3 shrink-0 transition ${expanded ? "rotate-180" : ""}`} />
    </button>

    <div className="route-time-grid mt-4" aria-label={t("timesLabel")}><div><span>{t("departs")}</span><strong>{formatTime(segment.departure_time, undefined, timezone)}</strong></div><Route size={18} aria-hidden="true" /><div><span>{t("arrives")}</span><strong>{formatTime(segment.arrival_time, undefined, timezone)}</strong></div><div className="route-buffer-summary"><span>{t("bufferLabel")}</span><strong>{t("bufferMinutes", { minutes: segment.buffer_minutes || 0 })}</strong></div><div className="route-ready-summary"><span>{t("nextCanStart")}</span><strong>{formatTime(segment.ready_time, undefined, timezone)}</strong></div></div>

    {hasConflict && <p className="mt-3 flex items-start gap-2 rounded-xl bg-red-50 px-3 py-2.5 text-sm font-semibold text-red-800"><TriangleAlert size={17} className="mt-0.5 shrink-0" />{t("conflictWarning")}</p>}
    {segment.warnings.map((warning) => <p key={warning} className="mt-2 rounded-xl bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">{warning}</p>)}

    {expanded && <div className="mt-4 space-y-4 border-t border-[var(--line)] pt-4">
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4"><div className="route-metric"><Clock3 size={15} /><span>{t("metricTravel")}</span><strong>{t("metricMinutes", { minutes: segment.duration_minutes })}</strong></div><div className="route-metric"><MapPin size={15} /><span>{t("metricDistance")}</span><strong>{distanceLabel(t, segment.distance_meters) || t("notProvided")}</strong></div><div className="route-metric"><BusFront size={15} /><span>{t("metricTransfers")}</span><strong>{t("transfersCount", { count: Math.max(0, transitSteps.length - 1) })}</strong></div><div className="route-metric"><CircleDollarSign size={15} /><span>{t("metricFare")}</span><strong>{segment.fare ? `${segment.currency} ${String(segment.fare)}` : t("notProvided")}</strong></div></div>
      <ol className="route-step-list" aria-label={t("stepsLabel")}>{segment.steps.map((step, index) => { const StepIcon = stepIcon(step.travel_mode); const lineColor = step.line_color && /^#[0-9a-f]{6}$/i.test(step.line_color) ? step.line_color : "#177c78"; return <li key={`${step.instruction}-${index}`} className="route-step-item"><span className="route-step-marker"><StepIcon size={15} /></span><div className="min-w-0 pb-4"><div className="flex flex-wrap items-start justify-between gap-2"><p className="font-semibold leading-5">{step.instruction}</p>{(step.duration_minutes || step.distance_meters) && <span className="shrink-0 text-xs text-[var(--muted)]">{step.duration_minutes ? t("metricMinutes", { minutes: step.duration_minutes }) : ""}{step.duration_minutes && step.distance_meters ? " · " : ""}{distanceLabel(t, step.distance_meters)}</span>}</div>{step.line_name && <p className="mt-2 flex items-center gap-2 text-xs font-bold"><span aria-hidden="true" className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: lineColor }} />{step.line_short_name || step.line_name}</p>}{(step.departure_time || step.arrival_time) && <p className="mt-1 text-xs font-semibold text-[var(--teal)]">{formatTime(step.departure_time, undefined, timezone)} → {formatTime(step.arrival_time, undefined, timezone)}</p>}{step.departure_stop && <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{step.departure_stop} → {step.arrival_stop}{step.headsign ? ` · ${t("towards", { headsign: step.headsign })}` : ""}{step.stop_count ? ` · ${t("stopCount", { count: step.stop_count })}` : ""}</p>}<div className="mt-2 flex flex-wrap gap-1.5 text-xs font-semibold">{step.platform && <span className="rounded-full bg-violet-50 px-2 py-1 text-violet-800">{t("platform", { value: step.platform })}</span>}{step.exit_name && <span className="rounded-full bg-emerald-50 px-2 py-1 text-emerald-800">{t("exit", { value: step.exit_name })}</span>}{step.recommended_car && <span className="rounded-full bg-orange-50 px-2 py-1 text-orange-800">{t("car", { value: step.recommended_car })}</span>}</div></div></li>; })}</ol>
      {!segment.steps.length && <p className="rounded-xl bg-[var(--paper)] px-3 py-3 text-sm text-[var(--muted)]">{t("noSteps")}</p>}
      {!segment.details_available.includes("exit") && mode === "transit" && <p className="flex items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-xs text-[var(--muted)]"><MapPin size={14} />{t("noExit")}</p>}
      <footer className="flex flex-wrap items-center justify-between gap-2 border-t border-[var(--line)] pt-3 text-xs text-[var(--muted)]"><span>{segment.attribution} · {new Date(segment.generated_at).toLocaleString(locale)}</span>{segment.maps_url && <a href={safeExternalHref(segment.maps_url)} target="_blank" rel="noreferrer" className="flex min-h-11 items-center gap-1 font-semibold text-[var(--teal)]">{mapsLabel}<ExternalLink size={13} /></a>}</footer>
    </div>}
  </article>;
}
