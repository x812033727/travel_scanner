"use client";

import {
  BusFront,
  CarFront,
  Check,
  Clock3,
  ExternalLink,
  Footprints,
  Loader2,
  MapPin,
  Navigation,
  RefreshCw,
  TriangleAlert,
} from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
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

type ProviderRoutePreview = {
  kind?: "provider";
  preview_id: string;
  expires_at: string;
  segment: RouteSegment;
  schedule_impact: RouteScheduleImpact;
};
type ExternalNavigation = {
  provider: "naver_maps" | "google_maps";
  label: string;
  travel_mode: TravelMode;
  app_url: string;
  web_url: string;
  reason: string;
};
type ExternalRoutePreview = {
  kind: "external_only";
  preview_id: null;
  expires_at: null;
  segment: null;
  schedule_impact: null;
  external_navigation: ExternalNavigation;
};
type RoutePreview = ProviderRoutePreview | ExternalRoutePreview;

function isProviderPreview(value?: RoutePreview): value is ProviderRoutePreview {
  return Boolean(value && value.kind !== "external_only" && value.segment);
}

type UnresolvedItem = { item_id: string; title: string; reason: string };
type LocationResolveResponse = {
  trip: Trip;
  matched_items: Array<{ item_id: string; title: string }>;
  unresolved_items: UnresolvedItem[];
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
  onResolved,
  onEditItem,
  onError,
}: {
  trip: Trip;
  items: TripItem[];
  fromItemId: string;
  toItemId: string;
  initialSegment?: RouteSegment;
  onApplied: (trip: Trip) => void;
  onResolved?: (trip: Trip) => void;
  onEditItem?: (itemId: string) => void;
  onError: (message: string) => void;
}) {
  const fromItem = items.find((item) => item.id === fromItemId);
  const toItem = items.find((item) => item.id === toItemId);
  const daySetting = trip.routing?.day_settings.find(
    (setting) => setting.day_date === fromItem?.day_date,
  );
  const initialMode = initialSegment?.travel_mode
    || daySetting?.default_travel_mode
    || "transit";
  const [mode, setMode] = useState<TravelMode>(initialMode);
  const [buffer, setBuffer] = useState(
    initialSegment?.buffer_minutes ?? daySetting?.default_buffer_minutes ?? 10,
  );
  const [previews, setPreviews] = useState<Partial<Record<TravelMode, RoutePreview>>>({});
  const [loadingMode, setLoadingMode] = useState<TravelMode>();
  const [resolvingLocations, setResolvingLocations] = useState(false);
  const [unresolvedItems, setUnresolvedItems] = useState<UnresolvedItem[]>([]);
  const [applying, setApplying] = useState(false);
  const [manualOpen, setManualOpen] = useState(false);
  const [manualMinutes, setManualMinutes] = useState("20");
  const [localError, setLocalError] = useState<string>();
  const autoStarted = useRef(false);
  const preview = previews[mode];
  const providerPreview = isProviderPreview(preview) ? preview : undefined;
  const externalNavigation = preview?.kind === "external_only" ? preview.external_navigation : undefined;
  const externalIsNaver = externalNavigation?.provider === "naver_maps";
  const activeSegment = providerPreview?.segment
    || (initialSegment?.travel_mode === mode ? initialSegment : undefined);
  const activeImpact = providerPreview?.schedule_impact;
  const isApplied = Boolean(initialSegment && initialSegment.travel_mode === mode && !preview);
  const missingItemIds = useMemo(
    () => [fromItem, toItem]
      .filter((item) => item && (item.latitude == null || item.longitude == null))
      .map((item) => item?.id)
      .filter((id): id is string => Boolean(id)),
    [fromItem, toItem],
  );

  const previewMode = useCallback(async (nextMode: TravelMode, nextBuffer = buffer) => {
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
      setLocalError(reason instanceof Error ? reason.message : "目前無法取得這個交通方式");
    } finally {
      setLoadingMode(undefined);
    }
  }, [buffer, fromItemId, toItemId, trip.id, trip.route_preference, trip.version]);

  useEffect(() => {
    if (autoStarted.current || initialSegment) return;
    autoStarted.current = true;
    async function prepareDefaultRoute() {
      if (missingItemIds.length) {
        setResolvingLocations(true);
        setLocalError(undefined);
        try {
          const result = await api<LocationResolveResponse>(
            `/trips/${trip.id}/locations/resolve`,
            {
              method: "POST",
              headers: { "Idempotency-Key": crypto.randomUUID() },
              body: JSON.stringify({ version: trip.version, item_ids: missingItemIds }),
            },
          );
          setUnresolvedItems(result.unresolved_items);
          if (result.matched_items.length) {
            onResolved?.(result.trip);
          }
        } catch (reason) {
          setLocalError(reason instanceof Error ? reason.message : "目前無法自動配對地點");
        } finally {
          setResolvingLocations(false);
        }
        return;
      }
      await previewMode(initialMode);
    }
    void prepareDefaultRoute();
  }, [
    initialMode,
    initialSegment,
    missingItemIds,
    onResolved,
    previewMode,
    trip.id,
    trip.version,
  ]);

  async function applyPreview() {
    if (!providerPreview) return;
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
          preview_id: providerPreview.preview_id,
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

  const directionsUrl = trip.destination_country_code !== "KR" && fromItem && toItem
    ? `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(fromItem.location_name || fromItem.title)}&destination=${encodeURIComponent(toItem.location_name || toItem.title)}&travelmode=${mode === "walk" ? "walking" : mode === "drive" ? "driving" : "transit"}`
    : undefined;

  const navigationUrl = externalNavigation?.web_url || activeSegment?.maps_url || directionsUrl;
  const routeSummary = activeSegment
    ? `${activeSegment.duration_minutes} 分鐘`
    : externalNavigation
      ? "外部導航"
      : resolvingLocations || loadingMode === mode
        ? "正在取得路線"
        : unresolvedItems.length
          ? "地點待確認"
          : localError
            ? "路線暫時無法取得"
            : "尚未取得路線";

  return <div className="route-panel-layout">
    <div className="route-panel-map min-w-0">
      <RouteMap items={items} segment={activeSegment} fromItemId={fromItemId} toItemId={toItemId} travelMode={mode} variant="drawer" countryCode={trip.destination_country_code} />
    </div>

    <section className="route-panel-modes" aria-label="路線起訖與交通方式">
      <div className="route-endpoints">
        <div className="route-endpoint"><span aria-hidden="true">1</span><p><small>從</small><strong>{fromItem?.location_name || fromItem?.title || "起點待確認"}</strong></p></div>
        <div className="route-endpoint"><span aria-hidden="true">2</span><p><small>到</small><strong>{toItem?.location_name || toItem?.title || "終點待確認"}</strong></p></div>
      </div>
      <div className="route-mode-toolbar">
        <div className="route-mode-tabs" role="tablist" aria-label="選擇交通工具">{modes.map(({ value, label, icon: Icon }) => <button key={value} type="button" role="tab" aria-selected={mode === value} onClick={() => { if (previews[value] || initialSegment?.travel_mode === value) setMode(value); else void previewMode(value); }} className={`route-mode-tab ${mode === value ? "route-mode-tab-active" : ""}`}><Icon size={18} />{label}{loadingMode === value && <Loader2 size={14} className="animate-spin" />}</button>)}</div>
        {navigationUrl && <a href={navigationUrl} target="_blank" rel="noreferrer" className="route-navigation-link" aria-label={`導航：${fromItem?.title || "起點"}到${toItem?.title || "終點"}`}><Navigation size={16} />導航</a>}
      </div>
      <div className="route-selection-summary"><strong>{routeSummary}</strong><span>{activeSegment?.schedule_mode === "preview" ? "自訂時間預覽" : activeSegment?.schedule_mode === "live" ? "目前路線" : "依行程時間規劃"}</span></div>
    </section>

    <div className="route-panel-controls space-y-4">
      <section className="route-buffer-control"><div><p className="font-semibold">預留轉場時間</p><p className="mt-1 text-xs text-[var(--muted)]">找路、等車或停車不會被算進純路程時間。</p></div><select aria-label="移動緩衝時間" value={buffer} onChange={(event) => { const value = Number(event.target.value); setBuffer(value); void previewMode(mode, value); }} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold">{bufferOptions.map((value) => <option key={value} value={value}>{value} 分鐘</option>)}</select></section>

      {resolvingLocations && <div className="route-preview-skeleton compact" aria-live="polite"><Loader2 size={22} className="animate-spin text-[var(--teal)]" /><strong>正在補齊兩端地點…</strong><span>依旅程國家使用 NAVER 或 Google 搜尋</span></div>}
      {unresolvedItems.length > 0 && <section className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-center gap-2 font-semibold"><MapPin size={18} />還缺少可定位的地點</p>{unresolvedItems.map((item) => <div key={item.item_id} className="mt-3 flex items-center justify-between gap-3 rounded-xl bg-white/70 p-3"><span className="min-w-0"><strong className="block truncate">{item.title}</strong><span className="mt-0.5 block text-xs">{item.reason}</span></span><button type="button" onClick={() => onEditItem?.(item.item_id)} className="min-h-11 shrink-0 rounded-xl border border-amber-300 px-3 font-bold">補上地點</button></div>)}</section>}
      {localError && <div role="alert" className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-start gap-2 font-semibold"><TriangleAlert size={18} className="mt-0.5 shrink-0" />{localError}</p><div className="mt-3 flex flex-wrap gap-2"><button type="button" onClick={() => void previewMode(mode)} className="flex min-h-11 items-center gap-2 rounded-xl border border-amber-300 bg-white px-3 font-bold"><RefreshCw size={15} />重試</button><button type="button" onClick={() => setManualOpen(true)} className="min-h-11 rounded-xl px-3 font-bold text-[var(--teal)]">手動時間</button>{directionsUrl && <a href={directionsUrl} target="_blank" rel="noreferrer" className="flex min-h-11 items-center gap-2 rounded-xl px-3 font-bold text-[var(--teal)]">Google 地圖<ExternalLink size={15} /></a>}</div></div>}
      {loadingMode === mode && !activeSegment && <div className="route-preview-skeleton compact" aria-live="polite"><Loader2 size={22} className="animate-spin text-[var(--teal)]" /><strong>正在取得{modes.find((item) => item.value === mode)?.label}路線…</strong><span>只查詢你目前選擇的交通方式</span></div>}
      {!resolvingLocations && !loadingMode && !activeSegment && !externalNavigation && !localError && !unresolvedItems.length && <div className="route-empty-state"><MapPin size={20} /><div><strong>尚未取得路線</strong><p>取得 Provider 驗證結果後，才會開放套用。</p></div></div>}

      {externalNavigation && <section className={`rounded-2xl border p-4 text-sm ${externalIsNaver ? "border-[#b8e7ca] bg-[#eefaf2] text-[#075c31]" : "border-sky-200 bg-sky-50 text-sky-950"}`} aria-label={`${externalNavigation.label} 外部導航`}><p className="flex items-center gap-2 font-bold"><ExternalLink size={18} />改用 {externalNavigation.label} 規劃</p><p className="mt-2 leading-6">{externalNavigation.reason}</p><p className={`mt-2 text-xs leading-5 ${externalIsNaver ? "text-[#397354]" : "text-sky-800"}`}>離開本站後才能查看即時班次；外部結果不會自動套用到行程時間。</p><div className="mt-3 flex flex-wrap gap-2"><a href={externalNavigation.web_url} target="_blank" rel="noreferrer" className={`flex min-h-11 items-center gap-2 rounded-xl px-4 font-bold text-white ${externalIsNaver ? "bg-[#03c75a]" : "bg-sky-700"}`}>用 {externalNavigation.label} 規劃<ExternalLink size={15} /></a>{externalIsNaver && externalNavigation.app_url !== externalNavigation.web_url && <a href={externalNavigation.app_url} className="flex min-h-11 items-center gap-2 rounded-xl border border-[#7fd5a3] bg-white px-4 font-bold">開啟 NAVER App</a>}<button type="button" onClick={() => setManualOpen(true)} className="min-h-11 rounded-xl px-3 font-bold">手動輸入時間</button></div></section>}

      {activeImpact && (activeImpact.affected_items.length > 0 || activeImpact.conflicts.length > 0) && <section className="route-impact-card"><div className="flex items-center gap-2"><Clock3 size={18} /><h3 className="font-bold">套用後的時間影響</h3></div>{activeImpact.affected_items.slice(0, 4).map((item) => <p key={item.item_id} className="mt-2 flex justify-between gap-3 text-sm"><span className="truncate">{item.title}</span><strong className="shrink-0">{item.delta_minutes > 0 ? "+" : ""}{item.delta_minutes} 分</strong></p>)}{activeImpact.conflicts.map((conflict) => <div key={conflict.item_id} className="mt-3 rounded-xl bg-red-50 p-3 text-sm text-red-900"><strong>可能遲到 {conflict.late_minutes} 分鐘</strong><p className="mt-1">{conflict.title} 保留原訂時間，不會被自動延後。</p><p className="mt-1 text-xs">建議：{conflict.suggestions.join("、")}</p></div>)}</section>}

      {manualOpen && <section className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"><h3 className="font-bold">手動輸入移動時間</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">查不到路線時可使用；畫面會明確標示未經地圖服務驗證。</p><label className="mt-3 block text-sm font-semibold">移動分鐘<input type="number" min="1" max="1440" value={manualMinutes} onChange={(event) => setManualMinutes(event.target.value)} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3" /></label><button type="button" onClick={() => void applyManual()} disabled={applying} className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}套用手動時間</button></section>}
    </div>

    <div className="route-panel-detail min-w-0">{activeSegment && <RouteSegmentCard segment={activeSegment} selected defaultExpanded timezone={trip.timezone} />}</div>

    <div className="route-apply-bar"><div className="min-w-0"><span className="block text-xs text-[var(--muted)]">目前選擇</span><strong className="block truncate">{modes.find((item) => item.value === mode)?.label}{activeSegment ? ` · ${activeSegment.duration_minutes} 分鐘` : externalNavigation ? " · 外部導航" : " · 尚未取得"}</strong></div><button type="button" onClick={() => providerPreview ? void applyPreview() : void previewMode(mode)} disabled={applying || Boolean(loadingMode) || resolvingLocations || unresolvedItems.length > 0 || isApplied || Boolean(externalNavigation)} className="flex min-h-12 shrink-0 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : isApplied ? <Check size={17} /> : null}{isApplied ? "目前已套用" : providerPreview ? "套用此路線" : externalNavigation ? "外部導航，無法套用" : loadingMode ? "取得中…" : "取得路線"}</button></div>
  </div>;
}
