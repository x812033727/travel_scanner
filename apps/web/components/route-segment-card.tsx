"use client";

import { BusFront, ChevronDown, CircleDollarSign, ExternalLink, Footprints, MapPin, TrainFront } from "lucide-react";
import { useState } from "react";
import type { RouteSegment } from "@/lib/trip-types";

export function RouteSegmentCard({ segment, selected, onSelect }: { segment: RouteSegment; selected?: boolean; onSelect?: () => void }) {
  const [expanded, setExpanded] = useState(false);
  const transitSteps = segment.steps.filter((step) => step.travel_mode === "TRANSIT");
  return <div className={`ml-8 rounded-2xl border bg-white p-3 ${selected ? "border-[var(--teal)] shadow-sm" : "border-[var(--line)]"}`}>
    <button type="button" onClick={() => { setExpanded(!expanded); onSelect?.(); }} className="flex w-full items-center justify-between gap-3 text-left">
      <span className="flex min-w-0 items-center gap-2 text-sm"><span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-sky-50 text-sky-700">{transitSteps.length ? <TrainFront size={16} /> : <Footprints size={16} />}</span><span><span className="font-semibold">移動約 {segment.duration_minutes} 分鐘</span><span className="ml-2 text-xs text-[var(--muted)]">{transitSteps.map((step) => step.line_short_name || step.line_name).filter(Boolean).join(" → ") || "步行"}</span></span></span>
      <ChevronDown size={16} className={`shrink-0 transition ${expanded ? "rotate-180" : ""}`} />
    </button>
    {segment.warnings.map((warning) => <p key={warning} className="mt-2 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-900">{warning}</p>)}
    {expanded && <div className="mt-3 space-y-3 border-t border-[var(--line)] pt-3">
      {segment.steps.map((step, index) => <div key={`${step.instruction}-${index}`} className="grid grid-cols-[1.75rem_1fr] gap-2 text-sm"><span className="grid h-7 w-7 place-items-center rounded-full bg-[var(--paper)] text-[var(--teal)]">{step.travel_mode === "TRANSIT" ? <BusFront size={14} /> : <Footprints size={14} />}</span><div><p className="font-medium">{step.instruction}</p>{step.departure_stop && <p className="mt-1 text-xs text-[var(--muted)]">{step.departure_stop} → {step.arrival_stop}{step.headsign ? ` · 往 ${step.headsign}` : ""}{step.stop_count ? ` · ${step.stop_count} 站` : ""}</p>}<div className="mt-1 flex flex-wrap gap-1.5 text-[.7rem] font-semibold">{step.platform && <span className="rounded-full bg-violet-50 px-2 py-1 text-violet-800">月台 {step.platform}</span>}{step.exit_name && <span className="rounded-full bg-emerald-50 px-2 py-1 text-emerald-800">出口 {step.exit_name}</span>}{step.recommended_car && <span className="rounded-full bg-orange-50 px-2 py-1 text-orange-800">建議車廂 {step.recommended_car}</span>}</div></div></div>)}
      {!segment.details_available.includes("exit") && <p className="flex items-center gap-2 rounded-lg bg-[var(--paper)] px-3 py-2 text-xs text-[var(--muted)]"><MapPin size={14} />此路線來源未提供可驗證的出口編號。</p>}
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-[var(--muted)]"><span>{segment.attribution} · {new Date(segment.generated_at).toLocaleString("zh-TW")}</span><span className="flex gap-3">{segment.fare && <span className="flex items-center gap-1"><CircleDollarSign size={13} />{segment.currency} {String(segment.fare)}</span>}{segment.maps_url && <a href={segment.maps_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 font-semibold text-[var(--teal)]">用 Google Maps 開啟<ExternalLink size={12} /></a>}</span></div>
    </div>}
  </div>;
}
