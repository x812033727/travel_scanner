"use client";

import { BusFront, CarFront, Check, Clock3, Footprints, Loader2, TriangleAlert } from "lucide-react";
import { useState } from "react";
import { RouteMap } from "@/components/route-map";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { api } from "@/lib/api";
import type {
  RouteScheduleImpact,
  RouteSegment,
  TravelMode,
  Trip,
  TripItem,
} from "@/lib/trip-types";

type RoutePreview = {
  preview_id: string;
  expires_at: string;
  segment: RouteSegment;
  schedule_impact: RouteScheduleImpact;
};

const modes: Array<{ value: TravelMode; label: string; icon: typeof BusFront }> = [
  { value: "transit", label: "大眾運輸", icon: BusFront },
  { value: "walk", label: "步行", icon: Footprints },
  { value: "drive", label: "汽車", icon: CarFront },
];

const bufferOptions = [0, 5, 10, 15, 30];

export function RouteModePanel({
  trip,
  items,
  fromItemId,
  toItemId,
  initialSegment,
  onApplied,
  onError,
}: {
  trip: Trip;
  items: TripItem[];
  fromItemId: string;
  toItemId: string;
  initialSegment?: RouteSegment;
  onApplied: (trip: Trip) => void;
  onError: (message: string) => void;
}) {
  const fromItem = items.find((item) => item.id === fromItemId);
  const daySetting = trip.routing?.day_settings.find((setting) => setting.day_date === fromItem?.day_date);
  const initialMode = initialSegment?.travel_mode || daySetting?.default_travel_mode || "transit";
  const [mode, setMode] = useState<TravelMode>(initialMode);
  const [buffer, setBuffer] = useState(initialSegment?.buffer_minutes ?? daySetting?.default_buffer_minutes ?? 10);
  const [previews, setPreviews] = useState<Partial<Record<TravelMode, RoutePreview>>>({});
  const [loadingMode, setLoadingMode] = useState<TravelMode>();
  const [applying, setApplying] = useState(false);
  const [manualOpen, setManualOpen] = useState(false);
  const [manualMinutes, setManualMinutes] = useState("20");
  const [localError, setLocalError] = useState<string>();
  const preview = previews[mode];
  const activeSegment = preview?.segment || (initialSegment?.travel_mode === mode ? initialSegment : undefined);
  const activeImpact = preview?.schedule_impact;
  const appliedMode = initialSegment?.travel_mode || "transit";

  async function previewMode(nextMode: TravelMode, nextBuffer = buffer) {
    setMode(nextMode);
    setLoadingMode(nextMode);
    setLocalError(undefined);
    try {
      const value = await api<RoutePreview>(`/trips/${trip.id}/routes/preview`, {
        method: "POST",
        body: JSON.stringify({
          version: trip.version,
          from_item_id: fromItemId,
          to_item_id: toItemId,
          travel_mode: nextMode,
          buffer_minutes: nextBuffer,
          route_preference: trip.route_preference,
        }),
      });
      setPreviews((current) => ({ ...current, [nextMode]: value }));
    } catch (reason) {
      const message = reason instanceof Error ? reason.message : "目前無法取得這個交通方式";
      setLocalError(message);
    } finally {
      setLoadingMode(undefined);
    }
  }

  async function applyPreview() {
    if (!preview) return;
    setApplying(true);
    setLocalError(undefined);
    try {
      const inherits = mode === daySetting?.default_travel_mode
        && buffer === daySetting.default_buffer_minutes;
      const updated = await api<Trip>(`/trips/${trip.id}/routes/apply`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          version: trip.version,
          source: "provider",
          preview_id: preview.preview_id,
          inherit_day_default: inherits,
        }),
      });
      onApplied(updated);
    } catch (reason) {
      const message = reason instanceof Error ? reason.message : "套用路線失敗";
      setLocalError(message);
      onError(message);
    } finally {
      setApplying(false);
    }
  }

  async function applyManual() {
    const duration = Number(manualMinutes);
    if (!Number.isInteger(duration) || duration < 1 || duration > 1440) {
      setLocalError("請輸入 1 到 1440 分鐘的移動時間");
      return;
    }
    setApplying(true);
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/routes/apply`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          version: trip.version,
          source: "manual",
          from_item_id: fromItemId,
          to_item_id: toItemId,
          travel_mode: mode,
          duration_minutes: duration,
          buffer_minutes: buffer,
          note: "使用者於行程編輯器輸入",
        }),
      });
      onApplied(updated);
    } catch (reason) {
      const message = reason instanceof Error ? reason.message : "儲存手動移動時間失敗";
      setLocalError(message);
      onError(message);
    } finally {
      setApplying(false);
    }
  }

  return <div className="space-y-5">
    <div className="route-mode-tabs" role="tablist" aria-label="選擇交通工具">{modes.map(({ value, label, icon: Icon }) => <button key={value} type="button" role="tab" aria-selected={mode === value} onClick={() => { if (mode === value) return; if (previews[value] || initialSegment?.travel_mode === value) setMode(value); else void previewMode(value); }} className={`route-mode-tab ${mode === value ? "route-mode-tab-active" : ""}`}><Icon size={18} />{label}{loadingMode === value && <Loader2 size={14} className="animate-spin" />}</button>)}</div>

    <section className="route-buffer-control"><div><p className="font-semibold">預留轉場時間</p><p className="mt-1 text-xs text-[var(--muted)]">找路、等車或停車不會被算進純路程時間。</p></div><select aria-label="移動緩衝時間" value={buffer} onChange={(event) => { const value = Number(event.target.value); setBuffer(value); void previewMode(mode, value); }} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold">{bufferOptions.map((value) => <option key={value} value={value}>{value} 分鐘</option>)}</select></section>

    {localError && <div role="alert" className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-start gap-2 font-semibold"><TriangleAlert size={18} className="mt-0.5 shrink-0" />{localError}</p><button type="button" onClick={() => setManualOpen(true)} className="mt-3 min-h-11 font-bold text-[var(--teal)] underline">改用手動移動時間</button></div>}
    {loadingMode === mode && !activeSegment && <div className="route-preview-skeleton" aria-live="polite"><Loader2 size={22} className="animate-spin text-[var(--teal)]" /><strong>正在取得{modes.find((item) => item.value === mode)?.label}路線…</strong><span>只查詢你目前選擇的交通方式</span></div>}
    {activeSegment && <><RouteMap items={items} segment={activeSegment} /><RouteSegmentCard segment={activeSegment} selected defaultExpanded /></>}

    {activeImpact && (activeImpact.affected_items.length > 0 || activeImpact.conflicts.length > 0) && <section className="route-impact-card"><div className="flex items-center gap-2"><Clock3 size={18} /><h3 className="font-bold">套用後的時間影響</h3></div>{activeImpact.affected_items.slice(0, 4).map((item) => <p key={item.item_id} className="mt-2 flex justify-between gap-3 text-sm"><span className="truncate">{item.title}</span><strong className="shrink-0">{item.delta_minutes > 0 ? "+" : ""}{item.delta_minutes} 分</strong></p>)}{activeImpact.conflicts.map((conflict) => <div key={conflict.item_id} className="mt-3 rounded-xl bg-red-50 p-3 text-sm text-red-900"><strong>可能遲到 {conflict.late_minutes} 分鐘</strong><p className="mt-1">{conflict.title} 保留原訂時間，不會被自動延後。</p><p className="mt-1 text-xs">建議：{conflict.suggestions.join("、")}</p></div>)}</section>}

    {manualOpen && <section className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"><h3 className="font-bold">手動輸入移動時間</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">查不到路線時可使用；畫面會明確標示未經地圖服務驗證。</p><label className="mt-3 block text-sm font-semibold">移動分鐘<input type="number" min="1" max="1440" value={manualMinutes} onChange={(event) => setManualMinutes(event.target.value)} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3" /></label><button type="button" onClick={() => void applyManual()} disabled={applying} className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}套用手動時間</button></section>}

    <div className="route-apply-bar"><div className="min-w-0"><span className="block text-xs text-[var(--muted)]">目前選擇</span><strong className="truncate">{modes.find((item) => item.value === mode)?.label}{activeSegment ? ` · ${activeSegment.duration_minutes} 分鐘` : ""}</strong></div><button type="button" onClick={() => preview ? void applyPreview() : void previewMode(mode)} disabled={applying || Boolean(loadingMode) || (mode === appliedMode && !preview)} className="flex min-h-12 shrink-0 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : mode === appliedMode && !preview ? <Check size={17} /> : null}{mode === appliedMode && !preview ? "目前已套用" : preview ? "套用此路線" : "取得路線"}</button></div>
  </div>;
}
