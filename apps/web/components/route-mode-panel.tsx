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
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { RouteMap } from "@/components/route-map";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { api, ApiError } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import type {
  RouteScheduleImpact,
  RouteSegment,
  TravelMode,
  Trip,
  TripItem,
} from "@/lib/trip-types";

type RouteOptionPreview = {
  preview_id: string;
  provider_route_key?: string | null;
  rank: number;
  expires_at: string;
  segment: RouteSegment;
  schedule_impact: RouteScheduleImpact;
};
type ProviderRoutePreview = {
  kind?: "provider";
  preview_id: string;
  expires_at: string;
  segment: RouteSegment;
  schedule_impact: RouteScheduleImpact;
  options?: RouteOptionPreview[];
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
  options?: [];
  external_navigation: ExternalNavigation;
};
type RoutePreview = ProviderRoutePreview | ExternalRoutePreview;

function isProviderPreview(value?: RoutePreview): value is ProviderRoutePreview {
  return Boolean(value && value.kind !== "external_only" && value.segment);
}

function previewOptions(preview?: ProviderRoutePreview): RouteOptionPreview[] {
  if (!preview) return [];
  if (preview.options?.length) return preview.options;
  return [{
    preview_id: preview.preview_id,
    rank: preview.segment.route_option_rank || 1,
    provider_route_key: preview.segment.provider_route_key,
    expires_at: preview.expires_at,
    segment: preview.segment,
    schedule_impact: preview.schedule_impact,
  }];
}

type Translator = ReturnType<typeof useTranslations>;

function requestError(t: Translator, reason: unknown, fallback: string) {
  if (!(reason instanceof Error)) return fallback;
  const trace = reason instanceof ApiError && reason.requestId
    ? t("traceCode", { id: reason.requestId })
    : "";
  return `${reason.message}${trace}`;
}

function routeOptionDetails(segment: RouteSegment) {
  const transitSteps = segment.steps.filter((step) => step.travel_mode === "TRANSIT");
  const walkingMinutes = segment.travel_mode === "walk"
    ? segment.duration_minutes
    : segment.steps
      .filter((step) => step.travel_mode === "WALK")
      .reduce((sum, step) => sum + (step.duration_minutes || 0), 0);
  const lines = [...new Set(transitSteps.map((step) => step.line_short_name || step.line_name).filter(Boolean))];
  return {
    transfers: Math.max(0, transitSteps.length - 1),
    walkingMinutes,
    lines: lines.join(" · "),
  };
}

function formatRouteDistance(t: Translator, distanceMeters?: number | null) {
  if (distanceMeters == null) return undefined;
  if (distanceMeters < 1000) return t("metres", { value: distanceMeters });
  return t("kilometres", { value: (distanceMeters / 1000).toFixed(distanceMeters >= 10_000 ? 0 : 1) });
}

function googleDirectionsUrl(
  fromItem: TripItem,
  toItem: TripItem,
  mode: TravelMode,
  placeFallback: string,
) {
  const endpoint = (item: TripItem) => {
    const googlePlaceId = item.provider_place_id
      && (!item.location_provider || item.location_provider === "google_places")
      ? item.provider_place_id
      : undefined;
    if (googlePlaceId) {
      return { query: item.title || item.location_name || placeFallback, placeId: googlePlaceId };
    }
    if (item.latitude == null || item.longitude == null) return undefined;
    return { query: `${item.latitude.toFixed(7)},${item.longitude.toFixed(7)}` };
  };
  const origin = endpoint(fromItem);
  const destination = endpoint(toItem);
  if (!origin || !destination) return undefined;
  const params = new URLSearchParams({
    api: "1",
    origin: origin.query,
    destination: destination.query,
    travelmode: mode === "walk" ? "walking" : mode === "drive" ? "driving" : "transit",
  });
  if (origin.placeId) params.set("origin_place_id", origin.placeId);
  if (destination.placeId) params.set("destination_place_id", destination.placeId);
  return `https://www.google.com/maps/dir/?${params.toString()}`;
}

function scheduleDeltaLabel(t: Translator, deltaMinutes: number) {
  if (deltaMinutes < 0) return t("earlierBy", { minutes: Math.abs(deltaMinutes) });
  if (deltaMinutes > 0) return t("laterBy", { minutes: deltaMinutes });
  return t("sameTime");
}

function formatRouteTime(value: string | null | undefined, timezone?: string) {
  if (!value) return undefined;
  return new Intl.DateTimeFormat("zh-TW", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: timezone || "UTC",
  }).format(new Date(value));
}

type UnresolvedItem = { item_id: string; title: string; reason: string };
type LocationResolveResponse = {
  trip: Trip;
  matched_items: Array<{ item_id: string; title: string }>;
  unresolved_items: UnresolvedItem[];
};

const modes: Array<{ value: TravelMode; labelKey: string; icon: typeof BusFront }> = [
  { value: "transit", labelKey: "modeTransit", icon: BusFront },
  { value: "walk", labelKey: "modeWalk", icon: Footprints },
  { value: "drive", labelKey: "modeDrive", icon: CarFront },
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
  const t = useTranslations("trips.route");
  const modeLabel = (value: TravelMode) => t(modes.find((item) => item.value === value)?.labelKey || "modeTransit");
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
  const [selectedOptions, setSelectedOptions] = useState<Partial<Record<TravelMode, number>>>({});
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
  const options = previewOptions(providerPreview);
  const selectedOptionIndex = Math.min(
    selectedOptions[mode] || 0,
    Math.max(0, options.length - 1),
  );
  const selectedOption = options[selectedOptionIndex];
  const externalNavigation = preview?.kind === "external_only" ? preview.external_navigation : undefined;
  const externalIsNaver = externalNavigation?.provider === "naver_maps";
  const activeSegment = selectedOption?.segment
    || (initialSegment?.travel_mode === mode ? initialSegment : undefined);
  const activeImpact = selectedOption?.schedule_impact;
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
          include_alternatives: true,
          max_options: 3,
        }),
      });
      setPreviews((current) => ({ ...current, [nextMode]: value }));
      setSelectedOptions((current) => ({ ...current, [nextMode]: 0 }));
    } catch (reason) {
      setLocalError(requestError(t, reason, t("modeUnavailable")));
    } finally {
      setLoadingMode(undefined);
    }
  }, [buffer, fromItemId, toItemId, t, trip.id, trip.route_preference, trip.version]);

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
          setLocalError(requestError(t, reason, t("matchFailed")));
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
    t,
    trip.id,
    trip.version,
  ]);

  async function applyPreview() {
    if (!selectedOption) return;
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
          preview_id: selectedOption.preview_id,
          inherit_day_default: inherits,
        }),
      });
      onApplied(updated);
    } catch (reason) {
      const message = requestError(t, reason, t("applyFailed"));
      setLocalError(message);
      onError(message);
    } finally {
      setApplying(false);
    }
  }

  async function applyManual() {
    const duration = Number(manualMinutes);
    if (!Number.isInteger(duration) || duration < 1 || duration > 1440) {
      setLocalError(t("manualRange"));
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
          note: t("manualNote"),
        }),
      });
      onApplied(updated);
    } catch (reason) {
      const message = requestError(t, reason, t("manualSaveFailed"));
      setLocalError(message);
      onError(message);
    } finally {
      setApplying(false);
    }
  }

  const directionsUrl = trip.destination_country_code !== "KR" && fromItem && toItem
    ? googleDirectionsUrl(fromItem, toItem, mode, t("placeFallback"))
    : undefined;

  const navigationUrl = externalNavigation?.web_url || activeSegment?.maps_url || directionsUrl;
  const routeSummary = activeSegment
    ? t("durationMinutes", { minutes: activeSegment.duration_minutes })
    : externalNavigation
      ? t("externalNavigation")
      : resolvingLocations || loadingMode === mode
        ? t("fetching")
        : unresolvedItems.length
          ? t("placePending")
          : localError
            ? t("temporarilyUnavailable")
            : t("noRouteYet");

  return <div className="route-panel-layout">
    <div className="route-panel-map min-w-0">
      <RouteMap
        items={items}
        segment={activeSegment}
        segments={options.map((option) => option.segment)}
        selectedSegmentIndex={selectedOptionIndex}
        onSelectSegment={(index) => setSelectedOptions((current) => ({ ...current, [mode]: index }))}
        fromItemId={fromItemId}
        toItemId={toItemId}
        travelMode={mode}
        variant="drawer"
        countryCode={trip.destination_country_code}
        externalOnly={Boolean(externalNavigation)}
      />
    </div>

    <section className="route-panel-modes" aria-label={t("endpointsLabel")}>
      <div className="route-endpoints">
        <div className="route-endpoint"><span aria-hidden="true">1</span><p><small>{t("from")}</small><strong>{fromItem?.title || fromItem?.location_name || t("originPending")}</strong></p></div>
        <div className="route-endpoint"><span aria-hidden="true">2</span><p><small>{t("to")}</small><strong>{toItem?.title || toItem?.location_name || t("destinationPending")}</strong></p></div>
      </div>
      <div className="route-mode-toolbar">
        <div className="route-mode-tabs" role="tablist" aria-label={t("chooseMode")}>{modes.map(({ value, labelKey, icon: Icon }) => <button key={value} type="button" role="tab" aria-selected={mode === value} onClick={() => { if (previews[value] || initialSegment?.travel_mode === value) setMode(value); else void previewMode(value); }} className={`route-mode-tab ${mode === value ? "route-mode-tab-active" : ""}`}><Icon size={18} />{t(labelKey)}{loadingMode === value && <Loader2 size={14} className="animate-spin" />}</button>)}</div>
        {navigationUrl && <a href={safeExternalHref(navigationUrl)} target="_blank" rel="noreferrer" className="route-navigation-link" aria-label={t("navigateFromTo", { from: fromItem?.title || t("startFallback"), to: toItem?.title || t("endFallback") })}><Navigation size={16} /><span>{t("navigate")}</span></a>}
      </div>
      <div className="route-selection-summary"><strong>{routeSummary}</strong><span>{activeSegment?.schedule_mode === "preview" ? t("nearTerm") : activeSegment?.schedule_mode === "live" ? t("liveRoute") : t("scheduled")}</span></div>
    </section>

    <div className="route-panel-controls space-y-4">
      <section className="route-buffer-control"><div><p className="font-semibold">{t("transferBuffer")}</p><p className="mt-1 text-xs text-[var(--muted)]">{t("transferBufferHint")}</p></div><select aria-label={t("bufferSelectLabel")} value={buffer} onChange={(event) => { const value = Number(event.target.value); setBuffer(value); void previewMode(mode, value); }} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold">{bufferOptions.map((value) => <option key={value} value={value}>{t("bufferMinutesOption", { minutes: value })}</option>)}</select></section>

      {resolvingLocations && <div className="route-preview-skeleton compact" aria-live="polite"><Loader2 size={22} className="animate-spin text-[var(--teal)]" /><strong>{t("resolvingPlaces")}</strong><span>{t("resolvingHint")}</span></div>}
      {unresolvedItems.length > 0 && <section className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-center gap-2 font-semibold"><MapPin size={18} />{t("missingPlaces")}</p>{unresolvedItems.map((item) => <div key={item.item_id} className="mt-3 flex items-center justify-between gap-3 rounded-xl bg-white/70 p-3"><span className="min-w-0"><strong className="block truncate">{item.title}</strong><span className="mt-0.5 block text-xs">{item.reason}</span></span><button type="button" onClick={() => onEditItem?.(item.item_id)} className="min-h-11 shrink-0 rounded-xl border border-amber-300 px-3 font-bold">{t("fixPlace")}</button></div>)}</section>}
      {localError && <div role="alert" className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-start gap-2 font-semibold"><TriangleAlert size={18} className="mt-0.5 shrink-0" />{localError}</p><div className="mt-3 flex flex-wrap gap-2"><button type="button" onClick={() => void previewMode(mode)} className="flex min-h-11 items-center gap-2 rounded-xl border border-amber-300 bg-white px-3 font-bold"><RefreshCw size={15} />{t("retry")}</button><button type="button" onClick={() => setManualOpen(true)} className="min-h-11 rounded-xl px-3 font-bold text-[var(--teal)]">{t("manualTime")}</button>{directionsUrl && <a href={safeExternalHref(directionsUrl)} target="_blank" rel="noreferrer" className="flex min-h-11 items-center gap-2 rounded-xl px-3 font-bold text-[var(--teal)]">{t("googleMaps")}<ExternalLink size={15} /></a>}</div></div>}
      {loadingMode === mode && !activeSegment && <div className="route-preview-skeleton compact" aria-live="polite"><Loader2 size={22} className="animate-spin text-[var(--teal)]" /><strong>{t("fetchingMode", { mode: modeLabel(mode) })}</strong><span>{t("onlySelectedMode")}</span></div>}
      {!resolvingLocations && !loadingMode && !activeSegment && !externalNavigation && !localError && !unresolvedItems.length && <div className="route-empty-state"><MapPin size={20} /><div><strong>{t("noRouteYet")}</strong><p>{t("applyBlocked")}</p></div></div>}

      {options.length > 0 && <section aria-label={t("optionsLabel")}>
        <div className="mb-2 flex items-end justify-between gap-3"><div><h3 className="font-bold">{t("chooseRoute")}</h3><p className="mt-1 text-xs text-[var(--muted)]">{t("chooseRouteHint")}</p></div><span className="shrink-0 text-xs font-semibold text-[var(--muted)]">{t("optionsCount", { count: options.length })}</span></div>
        <div className="route-option-scroll" role="listbox" aria-label={t("optionsFor", { mode: modeLabel(mode) })}>
          {options.map((option, index) => {
            const details = routeOptionDetails(option.segment);
            const selected = index === selectedOptionIndex;
            const departure = formatRouteTime(option.segment.departure_time, trip.timezone);
            const arrival = formatRouteTime(option.segment.arrival_time, trip.timezone);
            const fare = option.segment.fare != null
              ? `${option.segment.currency || ""} ${option.segment.fare}`.trim()
              : undefined;
            return <button
              key={option.preview_id}
              type="button"
              role="option"
              aria-selected={selected}
              onClick={() => setSelectedOptions((current) => ({ ...current, [mode]: index }))}
              className={`route-option-card ${selected ? "route-option-card-selected" : ""}`}
            >
              <span className="flex items-center justify-between gap-3"><strong>{t("optionNumber", { index: index + 1 })}</strong>{index === 0 && <span className="route-option-recommended">{t("recommended")}</span>}</span>
              <span className="mt-3 flex items-end justify-between gap-3"><strong className="text-xl text-[var(--teal-dark)]">{t("optionMinutes", { minutes: option.segment.duration_minutes })}</strong>{departure && arrival && <span className="text-xs font-semibold text-[var(--muted)]">{departure} → {arrival}</span>}</span>
              <span className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs text-[var(--muted)]">{option.segment.travel_mode === "transit" ? <><span>{t("transfersCount", { count: details.transfers })}</span><span>{t("walkingMinutes", { minutes: details.walkingMinutes })}</span></> : <span>{formatRouteDistance(t, option.segment.distance_meters) || t("distanceUnknown")}</span>}{fare && <span>{fare}</span>}</span>
              {details.lines && <span className="mt-2 block truncate text-left text-xs font-semibold text-[var(--teal-dark)]">{details.lines}</span>}
            </button>;
          })}
        </div>
      </section>}

      {externalNavigation && <section className={`rounded-2xl border p-4 text-sm ${externalIsNaver ? "border-[#b8e7ca] bg-[#eefaf2] text-[#075c31]" : "border-sky-200 bg-sky-50 text-sky-950"}`} aria-label={t("externalAria", { provider: externalNavigation.label })}><p className="flex items-center gap-2 font-bold"><ExternalLink size={18} />{t("switchToProvider", { provider: externalNavigation.label })}</p><p className="mt-2 leading-6">{externalNavigation.reason}</p><p className={`mt-2 text-xs leading-5 ${externalIsNaver ? "text-[#397354]" : "text-sky-800"}`}>{t("externalNote")}</p><div className="mt-3 flex flex-wrap gap-2"><a href={safeExternalHref(externalNavigation.web_url)} target="_blank" rel="noreferrer" className={`flex min-h-11 items-center gap-2 rounded-xl px-4 font-bold text-white ${externalIsNaver ? "bg-[#03c75a]" : "bg-sky-700"}`}>{t("planWithProvider", { provider: externalNavigation.label })}<ExternalLink size={15} /></a>{externalIsNaver && externalNavigation.app_url !== externalNavigation.web_url && <a href={safeExternalHref(externalNavigation.app_url, ["nmap:", "https:"])} className="flex min-h-11 items-center gap-2 rounded-xl border border-[#7fd5a3] bg-white px-4 font-bold">{t("openNaverApp")}</a>}<button type="button" onClick={() => setManualOpen(true)} className="min-h-11 rounded-xl px-3 font-bold">{t("manualEntry")}</button></div></section>}

      {activeImpact && (activeImpact.affected_items.length > 0 || activeImpact.conflicts.length > 0) && <section className="route-impact-card"><div className="flex items-center gap-2"><Clock3 size={18} /><h3 className="font-bold">{t("impactTitle")}</h3></div>{activeImpact.affected_items.slice(0, 4).map((item) => <p key={item.item_id} className="mt-2 flex justify-between gap-3 text-sm"><span className="truncate">{item.title}</span><strong className={`route-impact-value shrink-0 ${item.delta_minutes < 0 ? "route-impact-earlier" : item.delta_minutes > 0 ? "route-impact-later" : ""}`}>{scheduleDeltaLabel(t, item.delta_minutes)}</strong></p>)}{activeImpact.conflicts.map((conflict) => <div key={conflict.item_id} className="mt-3 rounded-xl bg-red-50 p-3 text-sm text-red-900"><strong>{t("conflictLate", { minutes: conflict.late_minutes })}</strong><p className="mt-1">{t("conflictKeeps", { title: conflict.title })}</p><p className="mt-1 text-xs">{t("suggestionsLabel", { list: conflict.suggestions.join(t("listSeparator")) })}</p></div>)}</section>}

      {manualOpen && <section className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"><h3 className="font-bold">{t("manualTitle")}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("manualHint")}</p><label className="mt-3 block text-sm font-semibold">{t("manualMinutesLabel")}<input type="number" min="1" max="1440" value={manualMinutes} onChange={(event) => setManualMinutes(event.target.value)} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3" /></label><button type="button" onClick={() => void applyManual()} disabled={applying} className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}{t("applyManual")}</button></section>}
    </div>

    <div className="route-panel-detail min-w-0">{activeSegment && <RouteSegmentCard segment={activeSegment} selected defaultExpanded timezone={trip.timezone} />}</div>

    <div className="route-apply-bar"><div className="route-apply-selection min-w-0"><span className="block text-xs text-[var(--muted)]">{t("currentChoice")}</span><strong className="block">{modeLabel(mode)}{activeSegment ? `${options.length ? ` · ${t("optionNumber", { index: selectedOptionIndex + 1 })}` : ""} · ${t("durationMinutes", { minutes: activeSegment.duration_minutes })}` : externalNavigation ? ` · ${t("externalNavigation")}` : ` · ${t("notFetched")}`}</strong></div><button type="button" aria-label={selectedOption ? t("applyThisRoute") : undefined} onClick={() => selectedOption ? void applyPreview() : void previewMode(mode)} disabled={applying || Boolean(loadingMode) || resolvingLocations || unresolvedItems.length > 0 || isApplied || Boolean(externalNavigation)} className="route-apply-button flex min-h-12 shrink-0 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : isApplied ? <Check size={17} /> : null}{isApplied ? t("applied") : selectedOption ? <><span className="route-apply-label-long">{t("applyThisRoute")}</span><span className="route-apply-label-short">{t("applyShort")}</span></> : externalNavigation ? t("externalCannotApply") : loadingMode ? t("fetchingShort") : t("fetchRoute")}</button></div>
  </div>;
}
