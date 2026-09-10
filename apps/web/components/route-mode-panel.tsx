"use client";

import {
  BusFront,
  CarFront,
  Check,
  ChevronDown,
  Clock3,
  ExternalLink,
  Footprints,
  Loader2,
  MapPin,
  Navigation,
  RefreshCw,
  TriangleAlert,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useId, useRef, useState, type KeyboardEvent } from "react";
import { dayTimelineCopy } from "@/components/planner/day-timeline-copy";
import { plannerOverlayCopy } from "@/components/planner/overlay-copy";
import styles from "@/components/planner/route-panel.module.css";
import { RouteMap } from "@/components/route-map";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { api, ApiError } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import { hasRoutePoint } from "@/lib/trip-types";
import type {
  RouteScheduleImpact,
  RouteExternalNavigation,
  RouteMapCapabilities,
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
  external_navigations?: RouteExternalNavigation[];
  map_capabilities?: RouteMapCapabilities;
};
type ExternalRoutePreview = {
  kind: "external_only";
  preview_id: null;
  expires_at: null;
  segment: null;
  schedule_impact: null;
  options?: [];
  external_navigation?: RouteExternalNavigation;
  external_navigations?: RouteExternalNavigation[];
  map_capabilities?: RouteMapCapabilities;
};
type RoutePreview = ProviderRoutePreview | ExternalRoutePreview;
type RouteAvailability = {
  status: "available" | "unconfigured" | "external_only";
  provider: string | null;
  can_query: boolean;
};
type NavigationResult = {
  external_navigations: RouteExternalNavigation[];
  map_capabilities?: RouteMapCapabilities;
  route_availability?: RouteAvailability;
};

function isProviderPreview(value?: RoutePreview): value is ProviderRoutePreview {
  return Boolean(value && value.kind !== "external_only" && value.segment);
}

function previewExpired(expiresAt: string) {
  const expiry = Date.parse(expiresAt);
  return !Number.isFinite(expiry) || expiry <= Date.now();
}

function hasUsableDuration(segment?: RouteSegment) {
  return Boolean(segment && Number.isFinite(segment.duration_minutes) && segment.duration_minutes >= 0
    && ["resolved", "complete", "manual", "estimated", "stale", "conflict"].includes(segment.status));
}

function isEstimatedTiming(segment?: RouteSegment) {
  return Boolean(segment && (segment.status === "estimated" || segment.provider === "estimate"
    || String(segment.schedule_mode) === "estimate"));
}

function isManualTiming(segment?: RouteSegment) {
  return Boolean(segment && !isEstimatedTiming(segment)
    && (segment.provider === "manual" || segment.status === "manual"));
}

function hasVerifiedTiming(segment?: RouteSegment) {
  // A schedule conflict describes a late fixed reservation, not invalid routing
  // data. The backend preserves the source when projecting that status.
  return Boolean(segment && hasUsableDuration(segment) && segment.provider.trim()
    && !isManualTiming(segment) && !isEstimatedTiming(segment)
    && ["resolved", "complete", "conflict"].includes(segment.status));
}

function previewOptions(preview?: ProviderRoutePreview): RouteOptionPreview[] {
  if (!preview) return [];
  if (preview.options?.length) return preview.options.filter((option) => hasVerifiedTiming(option.segment));
  if (!hasVerifiedTiming(preview.segment)) return [];
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
  const walkingSteps = segment.steps.filter((step) => step.travel_mode === "WALK");
  const walkingMinutes = segment.travel_mode === "walk"
    ? segment.duration_minutes
    : walkingSteps.length && walkingSteps.every((step) => step.duration_minutes != null)
      ? walkingSteps.reduce((sum, step) => sum + step.duration_minutes!, 0) : undefined;
  const lines = [...new Set(transitSteps.map((step) => step.line_short_name || step.line_name).filter(Boolean))];
  return {
    transfers: transitSteps.length ? transitSteps.length - 1 : undefined,
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

function formatRouteTime(value: string | null | undefined, locale: string, timezone?: string) {
  if (!value) return undefined;
  return new Intl.DateTimeFormat(locale, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: timezone || "UTC",
  }).format(new Date(value));
}

const modes: Array<{ value: TravelMode; labelKey: string; icon: typeof BusFront }> = [
  { value: "transit", labelKey: "modeTransit", icon: BusFront },
  { value: "walk", labelKey: "modeWalk", icon: Footprints },
  { value: "drive", labelKey: "modeDrive", icon: CarFront },
];
const bufferOptions = [0, 5, 10, 15, 30];

function nextKeyboardIndex(event: KeyboardEvent, index: number, count: number) {
  if (!count) return undefined;
  if (event.key === "Home") return 0;
  if (event.key === "End") return count - 1;
  if (event.key === "ArrowRight" || event.key === "ArrowDown") return (index + 1) % count;
  if (event.key === "ArrowLeft" || event.key === "ArrowUp") return (index + count - 1) % count;
  return undefined;
}

export function RouteModePanel({
  trip,
  items,
  fromItemId,
  toItemId,
  initialSegment,
  initialTravelMode,
  initialBufferMinutes,
  onApplied,
  onEditItem,
  onError,
  onBusy,
}: {
  trip: Trip;
  items: TripItem[];
  fromItemId: string;
  toItemId: string;
  initialSegment?: RouteSegment;
  initialTravelMode?: TravelMode;
  initialBufferMinutes?: number;
  onApplied: (trip: Trip) => void;
  onResolved?: (trip: Trip) => void;
  onEditItem?: (itemId: string) => void;
  onError: (message: string) => void;
  onBusy?: (busy: boolean) => void;
}) {
  const t = useTranslations("trips.route");
  const locale = useLocale();
  const copy = plannerOverlayCopy(locale);
  const timelineCopy = dayTimelineCopy(locale);
  const panelId = useId();
  const modeLabel = (value: TravelMode) => t(modes.find((item) => item.value === value)?.labelKey || "modeTransit");
  const fromItem = items.find((item) => item.id === fromItemId);
  const toItem = items.find((item) => item.id === toItemId);
  const daySetting = trip.routing?.day_settings.find(
    (setting) => setting.day_date === fromItem?.day_date,
  );
  const initialMode = initialTravelMode || initialSegment?.travel_mode
    || daySetting?.default_travel_mode
    || "transit";
  const [mode, setMode] = useState<TravelMode>(initialMode);
  const [buffer, setBuffer] = useState(
    initialBufferMinutes ?? initialSegment?.buffer_minutes ?? daySetting?.default_buffer_minutes ?? 10,
  );
  const [previews, setPreviews] = useState<Record<string, RoutePreview>>({});
  const [navigationResult, setNavigationResult] = useState<NavigationResult & { key: string }>();
  const [selectedOptions, setSelectedOptions] = useState<Record<string, number>>({});
  const [loadingMode, setLoadingMode] = useState<TravelMode>();
  const [applying, setApplying] = useState(false);
  const [manualOpen, setManualOpen] = useState(false);
  const [mapOpen, setMapOpen] = useState(false);
  const manualButtonRef = useRef<HTMLButtonElement>(null);
  const manualInputRef = useRef<HTMLInputElement>(null);
  const detailRef = useRef<HTMLElement>(null);
  const focusNextPreviewRef = useRef(false);
  const [manualMinutes, setManualMinutes] = useState("");
  const [localError, setLocalError] = useState<string>();
  const [, refreshExpiry] = useState(0);
  const busyRef = useRef(false);
  const mountedRef = useRef(false);
  const requestKey = JSON.stringify([trip.id, trip.version, fromItemId, toItemId, mode, buffer, trip.route_preference]);
  const navigationKey = JSON.stringify([trip.id, trip.version, fromItemId, toItemId, mode]);
  const routeAvailability = navigationResult?.key === navigationKey ? navigationResult.route_availability : undefined;
  const cannotQuery = routeAvailability?.can_query === false;
  const requestKeyRef = useRef(requestKey);
  useEffect(() => { requestKeyRef.current = requestKey; }, [requestKey]);
  useEffect(() => { mountedRef.current = true; return () => { mountedRef.current = false; }; }, []);
  useEffect(() => {
    if (manualOpen) manualInputRef.current?.focus();
  }, [manualOpen]);
  function openManual() {
    setManualMinutes(isManualTiming(initialSegment) && initialSegment?.travel_mode === mode ? String(initialSegment.duration_minutes) : "");
    setLocalError(undefined);
    setManualOpen(true);
  }
  const preview = previews[requestKey];
  const providerPreview = isProviderPreview(preview) ? preview : undefined;
  useEffect(() => {
    if (!providerPreview || !focusNextPreviewRef.current || !detailRef.current) return;
    focusNextPreviewRef.current = false;
    detailRef.current.focus({ preventScroll: true });
    detailRef.current.scrollIntoView?.({ block: "start", behavior: "auto" });
  }, [providerPreview]);
  const options = previewOptions(providerPreview);
  const selectedOptionIndex = Math.min(
    selectedOptions[requestKey] || 0,
    Math.max(0, options.length - 1),
  );
  const selectedOption = options[selectedOptionIndex];
  const expiresAt = selectedOption?.expires_at || (initialSegment?.provider !== "manual" ? initialSegment?.expires_at : undefined);
  useEffect(() => {
    if (!expiresAt) return;
    const remaining = Date.parse(expiresAt) - Date.now();
    if (!Number.isFinite(remaining) || remaining <= 0) return;
    const timer = window.setTimeout(() => refreshExpiry((value) => value + 1), Math.min(remaining + 1, 2_147_483_647));
    return () => window.clearTimeout(timer);
  }, [expiresAt]);
  const selectedExpired = Boolean(selectedOption && previewExpired(selectedOption.expires_at));
  const canApplyPreview = Boolean(selectedOption && hasVerifiedTiming(selectedOption.segment) && !selectedExpired && !localError);
  const isExternalPreview = preview?.kind === "external_only";
  const externalNavigation = isExternalPreview
    ? preview.external_navigations?.[0] || preview.external_navigation : undefined;
  const initialMatches = initialSegment?.travel_mode === mode
    && (initialSegment.buffer_minutes ?? 10) === buffer
    && initialSegment.from_item_id === fromItemId && initialSegment.to_item_id === toItemId;
  const activeSegment = hasUsableDuration(selectedOption?.segment) ? selectedOption?.segment
    : initialMatches && hasUsableDuration(initialSegment) ? initialSegment : undefined;
  const activeImpact = selectedOption?.schedule_impact;
  const savedExpired = Boolean(initialMatches && initialSegment?.provider !== "manual"
    && initialSegment?.expires_at && previewExpired(initialSegment.expires_at));
  const isApplied = Boolean(initialMatches && hasUsableDuration(initialSegment)
    && (hasVerifiedTiming(initialSegment) || (isManualTiming(initialSegment) && initialSegment?.status !== "stale"))
    && !savedExpired && !preview);
  const unresolvedItems = [fromItem, toItem].filter((item): item is TripItem => Boolean(item && !hasRoutePoint(item)))
    .map((item) => ({ item_id: item.id, title: item.title, reason: t("placePending") }));
  const settingsOutdated = !preview && (Boolean(initialSegment && !initialMatches) || Object.keys(previews).length > 0);
  const routeState = loadingMode ? "loading" : localError ? "error" : unresolvedItems.length ? "missing"
    : selectedExpired ? "expired" : canApplyPreview ? "preview" : isExternalPreview ? "external"
      : isApplied ? (isManualTiming(initialSegment) ? "manual" : "applied")
        : initialMatches && (initialSegment?.status === "stale" || savedExpired) ? "stale"
          : isEstimatedTiming(activeSegment) ? "estimated"
            : preview || (initialMatches && initialSegment) ? "unavailable" : settingsOutdated ? "changed" : "idle";

  async function previewMode(nextMode: TravelMode, nextBuffer = buffer) {
    if (busyRef.current || cannotQuery || !fromItem || !toItem || unresolvedItems.length) return;
    busyRef.current = true;
    onBusy?.(true);
    const identity = requestKey;
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
      if (!mountedRef.current || requestKeyRef.current !== identity) return;
      focusNextPreviewRef.current = isProviderPreview(value);
      setPreviews((current) => ({ ...current, [identity]: value }));
      setSelectedOptions((current) => ({ ...current, [identity]: 0 }));
    } catch (reason) {
      if (mountedRef.current && requestKeyRef.current === identity) setLocalError(requestError(t, reason, t("modeUnavailable")));
    } finally {
      busyRef.current = false;
      onBusy?.(false);
      if (mountedRef.current) setLoadingMode(undefined);
    }
  }

  async function applyPreview() {
    if (!selectedOption || busyRef.current) return;
    if (previewExpired(selectedOption.expires_at)) { setLocalError(t("previewExpired")); return; }
    if (!hasVerifiedTiming(selectedOption.segment)) { setLocalError(t("temporarilyUnavailable")); return; }
    busyRef.current = true;
    onBusy?.(true);
    const identity = requestKey;
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
      if (mountedRef.current && requestKeyRef.current === identity) onApplied(updated);
    } catch (reason) {
      const message = requestError(t, reason, t("applyFailed"));
      if (mountedRef.current && requestKeyRef.current === identity) { setLocalError(message); onError(message); }
    } finally {
      busyRef.current = false;
      onBusy?.(false);
      if (mountedRef.current) setApplying(false);
    }
  }

  async function applyManual() {
    if (busyRef.current) return;
    const duration = Number(manualMinutes);
    if (!Number.isInteger(duration) || duration < 1 || duration > 1440) {
      setLocalError(t("manualRange"));
      return;
    }
    busyRef.current = true;
    onBusy?.(true);
    const identity = requestKey;
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
      if (mountedRef.current && requestKeyRef.current === identity) onApplied(updated);
    } catch (reason) {
      const message = requestError(t, reason, t("manualSaveFailed"));
      if (mountedRef.current && requestKeyRef.current === identity) { setLocalError(message); onError(message); }
    } finally {
      busyRef.current = false;
      onBusy?.(false);
      if (mountedRef.current) setApplying(false);
    }
  }

  const directionsUrl = trip.destination_country_code !== "KR" && fromItem && toItem
    ? googleDirectionsUrl(fromItem, toItem, mode, t("placeFallback"))
    : undefined;

  const navigationUrl = externalNavigation?.web_url || activeSegment?.maps_url || directionsUrl;
  const suppliedNavigations = preview?.external_navigations ?? activeSegment?.external_navigations;
  const needsNavigationLookup = trip.destination_country_code === "KR"
    && unresolvedItems.length === 0 && Boolean(fromItem && toItem);
  useEffect(() => {
    if (!needsNavigationLookup) return;
    const controller = new AbortController();
    const params = new URLSearchParams({ from_item_id: fromItemId, to_item_id: toItemId, travel_mode: mode });
    api<NavigationResult>(`/trips/${trip.id}/routes/navigation?${params}`, { signal: controller.signal })
      .then((value) => {
        if (!controller.signal.aborted && Array.isArray(value.external_navigations)) {
          setNavigationResult({ key: navigationKey, ...value });
        }
      }).catch(() => { /* Route queries and map display remain independently usable. */ });
    return () => controller.abort();
  }, [fromItemId, mode, navigationKey, needsNavigationLookup, toItemId, trip.id]);
  const availableNavigations = suppliedNavigations
    ?? (navigationResult?.key === navigationKey ? navigationResult.external_navigations : undefined);
  const navigations = (availableNavigations
    ?? (externalNavigation ? [externalNavigation] : []))
    .filter((navigation) => navigation.travel_mode === mode
      && (trip.destination_country_code !== "KR" || mode !== "drive" || navigation.provider === "naver_maps"));
  const hasNavigationContract = availableNavigations !== undefined || Boolean(externalNavigation);
  const stateLabel = routeState === "preview" ? t("previewReady") : routeState === "expired" ? t("previewExpired")
    : routeState === "stale" ? t("staleRoute") : routeState === "manual" ? t("manualApplied")
      : routeState === "estimated" ? t("estimatedTiming") : routeState === "applied" ? t(initialSegment?.status === "conflict" ? "appliedConflict" : "applied")
        : routeState === "external" ? t("externalNavigation") : routeState === "loading" ? t("fetching")
          : routeState === "error" || routeState === "unavailable" ? t("temporarilyUnavailable")
            : routeState === "missing" ? t("placePending") : routeState === "changed" && !cannotQuery ? timelineCopy.outdated : undefined;

  const verifiedRoute = hasVerifiedTiming(activeSegment);
  const externalMode = (isExternalPreview || cannotQuery) && !canApplyPreview && !(isApplied && verifiedRoute);
  const primaryNavigation = navigations.find((navigation) => safeExternalHref(navigation.web_url));
  const providerLabel = routeAvailability?.provider === "odsay" ? "ODsay"
    : routeAvailability?.provider === "naver_maps" ? "NAVER Maps"
      : routeAvailability?.provider === "google_routes" ? "Google Maps" : t("transportUx.routingService");
  const manualValid = manualMinutes.trim() !== "" && Number.isInteger(Number(manualMinutes))
    && Number(manualMinutes) >= 1 && Number(manualMinutes) <= 1440;
  const showNavigation = navigations.length > 0 || (!hasNavigationContract && Boolean(navigationUrl));
  const actionClass = "route-apply-button flex min-h-12 shrink-0 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 text-center font-bold text-white disabled:opacity-45";

  return <div className={styles.container}><div className={`route-panel-layout ${styles.layout}`} data-route-state={externalMode ? "external" : routeState}>
    <section className={`route-panel-modes ${styles.modes}`} aria-label={t("endpointsLabel")}>
      <div className="route-endpoints">
        <div className="route-endpoint"><span aria-hidden="true">1</span><p><small>{t("from")}</small><strong>{fromItem?.title || fromItem?.location_name || t("originPending")}</strong></p></div>
        <div className="route-endpoint"><span aria-hidden="true">2</span><p><small>{t("to")}</small><strong>{toItem?.title || toItem?.location_name || t("destinationPending")}</strong></p></div>
      </div>
      <h3 className="px-4 pt-3 text-sm font-bold">{t("transportUx.settings")}</h3>
      <div className="route-mode-toolbar">
        <div className="route-mode-tabs" role="tablist" aria-label={t("chooseMode")}>{modes.map(({ value, labelKey, icon: Icon }, index) => <button key={value} id={`${panelId}-${value}`} type="button" role="tab" aria-selected={mode === value} aria-controls={`${panelId}-options`} tabIndex={mode === value ? 0 : -1} disabled={applying || Boolean(loadingMode)} onKeyDown={(event) => {
          const next = nextKeyboardIndex(event, index, modes.length);
          if (next === undefined) return;
          event.preventDefault();
          event.currentTarget.parentElement?.querySelectorAll<HTMLButtonElement>("[role='tab']")[next]?.focus({ preventScroll: true });
        }} onClick={() => { setMode(value); setManualOpen(false); setLocalError(undefined); }} className={`route-mode-tab ${mode === value ? "route-mode-tab-active" : ""}`}><Icon size={18} />{t(labelKey)}{loadingMode === value && <Loader2 size={14} className="animate-spin" />}</button>)}</div>
      </div>
      <section className="route-buffer-control px-4 pb-4"><div><p className="font-semibold">{t("transferBuffer")}</p><p className="mt-1 text-xs text-[var(--muted)]">{t("transferBufferHint")}</p></div><select aria-label={t("bufferSelectLabel")} value={buffer} disabled={applying || Boolean(loadingMode)} onChange={(event) => { setBuffer(Number(event.target.value)); setLocalError(undefined); }} className="min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm font-semibold">{bufferOptions.map((value) => <option key={value} value={value}>{t("bufferMinutesOption", { minutes: value })}</option>)}</select></section>
      <div className={styles.feedback}>
        {stateLabel && <p role="status" className={styles.state}><strong>{stateLabel}</strong>{activeSegment && ["preview", "applied"].includes(routeState) && <span>{activeSegment.schedule_mode === "preview" ? t("nearTerm") : activeSegment.schedule_mode === "live" ? t("liveRoute") : t("scheduled")}</span>}</p>}
        {routeState === "idle" && !cannotQuery && <p className={styles.hint} data-route-instruction="idle">{t("queryHint")}</p>}
        {!cannotQuery && !isExternalPreview && (isApplied || canApplyPreview || routeState === "estimated") && <button type="button" onClick={() => void previewMode(mode)} disabled={applying || Boolean(loadingMode) || unresolvedItems.length > 0} className={styles.requery}><RefreshCw size={15} />{timelineCopy.requery}</button>}
      </div>
    </section>

    <div id={`${panelId}-options`} className={`route-panel-controls space-y-4 ${styles.controls}`} role="tabpanel" aria-labelledby={`${panelId}-${mode}`}>
      <h3 className="text-base font-bold">{t("transportUx.information")}</h3>
      {unresolvedItems.length > 0 && <section className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-center gap-2 font-semibold"><MapPin size={18} />{t("missingPlaces")}</p>{unresolvedItems.map((item) => <div key={item.item_id} className="mt-3 flex items-center justify-between gap-3 rounded-xl bg-white/70 p-3"><span className="min-w-0"><strong className="block truncate">{item.title}</strong><span className="mt-0.5 block text-xs">{item.reason}</span></span><button type="button" onClick={() => onEditItem?.(item.item_id)} className="min-h-11 shrink-0 rounded-xl border border-amber-300 px-3 font-bold">{t("fixPlace")}</button></div>)}</section>}
      {localError && <div role="alert" className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="flex items-start gap-2 font-semibold"><TriangleAlert size={18} className="mt-0.5 shrink-0" />{localError}</p></div>}
      {externalMode && <section className="route-availability-notice rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950">
        {!verifiedRoute && <p className="font-bold">{t(mode === "transit" ? "transportUx.transitStepsMissing" : "transportUx.stepsMissing")}</p>}
        <p className="mt-2 leading-6">{routeAvailability?.status === "unconfigured"
          ? t("transportUx.unconfigured", { provider: providerLabel }) : t("transportUx.externalOnly")}</p>
        {!routeAvailability && externalNavigation?.reason && <p className="mt-2 text-xs leading-5">{externalNavigation.reason}</p>}
      </section>}

      {options.length > 1 && <section aria-label={t("optionsLabel")}>
        <div className="mb-2 flex items-end justify-between gap-3"><div><h3 className="font-bold">{t("chooseRoute")}</h3><p className="mt-1 text-xs text-[var(--muted)]">{t("chooseRouteHint")}</p></div><span className="shrink-0 text-xs font-semibold">{t("optionsCount", { count: options.length })}</span></div>
        <div className="route-option-scroll" role="listbox" aria-label={t("optionsFor", { mode: modeLabel(mode) })}>
          {options.map((option, index) => {
            const details = routeOptionDetails(option.segment);
            const selected = index === selectedOptionIndex;
            const departure = formatRouteTime(option.segment.departure_time, locale, trip.timezone);
            const arrival = formatRouteTime(option.segment.arrival_time, locale, trip.timezone);
            const fare = option.segment.fare != null ? `${option.segment.currency || ""} ${option.segment.fare}`.trim() : undefined;
            return <button key={option.preview_id} type="button" role="option" aria-selected={selected} tabIndex={selected ? 0 : -1}
              onKeyDown={(event) => {
                const next = nextKeyboardIndex(event, index, options.length);
                if (next === undefined) return;
                event.preventDefault(); setSelectedOptions((current) => ({ ...current, [requestKey]: next }));
                event.currentTarget.parentElement?.querySelectorAll<HTMLButtonElement>("[role='option']")[next]?.focus({ preventScroll: true });
              }}
              onClick={() => setSelectedOptions((current) => ({ ...current, [requestKey]: index }))}
              className={`route-option-card ${selected ? "route-option-card-selected" : ""}`}>
              <span className="flex items-center justify-between gap-3"><strong>{t("optionNumber", { index: index + 1 })}</strong>{index === 0 && <span className="route-option-recommended">{t("recommended")}</span>}</span>
              <span className="mt-3 flex items-end justify-between gap-3"><strong className="text-xl text-[var(--teal-dark)]">{t("optionMinutes", { minutes: option.segment.duration_minutes })}</strong>{departure && arrival && <span className="text-xs text-[var(--muted)]">{departure} → {arrival}</span>}</span>
              <span className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs text-[var(--muted)]">{option.segment.travel_mode === "transit" ? <><span>{details.transfers == null ? t("transportUx.transfersUnknown") : t("transfersCount", { count: details.transfers })}</span><span>{details.walkingMinutes == null ? t("transportUx.walkingUnknown") : t("walkingMinutes", { minutes: details.walkingMinutes })}</span></> : <span>{formatRouteDistance(t, option.segment.distance_meters) || t("distanceUnknown")}</span>}{fare && <span>{fare}</span>}</span>
              {details.lines && <span className="mt-2 block truncate text-left text-xs font-semibold text-[var(--teal-dark)]">{details.lines}</span>}
            </button>;
          })}
        </div>
      </section>}

      {activeSegment && <section ref={detailRef} tabIndex={-1} className={`route-panel-detail min-w-0 ${styles.detail}`} aria-label={t("transportUx.stepsTitle")}>
        {preview && !selectedOption && <p className="mb-2 text-sm font-semibold">{t("transportUx.savedTiming")}</p>}
        <RouteSegmentCard key={selectedOption?.preview_id || `${mode}-applied`} segment={activeSegment} selected defaultExpanded showNavigation={false} timezone={trip.timezone} />
      </section>}

      {activeImpact && (activeImpact.affected_items.length > 0 || activeImpact.conflicts.length > 0) && <section className="route-impact-card"><div className="flex items-center gap-2"><Clock3 size={18} /><h3 className="font-bold">{t("impactTitle")}</h3></div>{activeImpact.affected_items.slice(0, 4).map((item) => <p key={item.item_id} className="mt-2 flex justify-between gap-3 text-sm"><span className="truncate">{item.title}</span><strong className={`route-impact-value shrink-0 ${item.delta_minutes < 0 ? "route-impact-earlier" : item.delta_minutes > 0 ? "route-impact-later" : ""}`}>{scheduleDeltaLabel(t, item.delta_minutes)}</strong></p>)}{activeImpact.conflicts.map((conflict) => <div key={conflict.item_id} className="mt-3 rounded-xl bg-red-50 p-3 text-sm text-red-900"><strong>{t("conflictLate", { minutes: conflict.late_minutes })}</strong><p className="mt-1">{t("conflictKeeps", { title: conflict.title })}</p><p className="mt-1 text-xs">{t("suggestionsLabel", { list: conflict.suggestions.join(t("listSeparator")) })}</p></div>)}</section>}

      {showNavigation && <section className="route-external-actions rounded-2xl border border-[var(--line)] p-4" aria-label={t("navigationProviders")}>
        <h3 className="flex items-center gap-2 font-bold"><ExternalLink size={17} />{t("transportUx.externalViewing")}</h3>
        <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{t("externalNote")}</p>
        <div className="mt-3 flex flex-wrap gap-2">{navigations.map((navigation) => <a key={navigation.provider} href={safeExternalHref(navigation.web_url)} target="_blank" rel="noopener noreferrer" className="route-navigation-link" aria-label={t("navigateWithProvider", { provider: navigation.label })}><Navigation size={16} /><span>{t("transportUx.externalLink", { provider: navigation.label })}</span></a>)}
          {!hasNavigationContract && navigationUrl && <a href={safeExternalHref(navigationUrl)} target="_blank" rel="noopener noreferrer" className="route-navigation-link" aria-label={t("navigateFromTo", { from: fromItem?.title || t("startFallback"), to: toItem?.title || t("endFallback") })}><Navigation size={16} />{t("transportUx.externalViewing")}</a>}
          {navigations.filter((navigation) => navigation.provider === "naver_maps" && navigation.app_url !== navigation.web_url).map((navigation) => <a key={navigation.provider} href={safeExternalHref(navigation.app_url, ["nmap:", "https:"])} className="route-navigation-link">{t("openNaverApp")}</a>)}
        </div>
      </section>}

      {!manualOpen && <button ref={manualButtonRef} type="button" onClick={openManual} disabled={applying || Boolean(loadingMode) || unresolvedItems.length > 0} className="min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-bold text-[var(--teal)]">{isManualTiming(activeSegment) ? t("transportUx.editManual") : t("manualEntry")}</button>}
      {manualOpen && <section className="route-manual-settings rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
        <div className="flex items-center justify-between gap-3"><h3 className="font-bold">{t("manualTitle")}</h3><button type="button" disabled={applying} onClick={() => { setManualOpen(false); window.requestAnimationFrame(() => manualButtonRef.current?.focus()); }} className="min-h-11 text-xs font-semibold text-[var(--muted)]">{copy.closeManual}</button></div>
        <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("manualHint")}</p>
        <label className="mt-3 block text-sm font-semibold">{t("manualMinutesLabel")}<input ref={manualInputRef} type="number" inputMode="numeric" min="1" max="1440" value={manualMinutes} onChange={(event) => setManualMinutes(event.target.value)} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3" /></label>
        <button type="button" onClick={() => void applyManual()} disabled={applying || !manualValid} className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] font-bold text-white disabled:opacity-45">{applying ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}{t("applyManual")}</button>
      </section>}
    </div>

    <details className={`route-panel-map min-w-0 ${styles.map}`} open={mapOpen} onToggle={(event) => setMapOpen(event.currentTarget.open)}>
      <summary className="flex min-h-12 cursor-pointer items-center gap-2 rounded-xl border border-[var(--line)] px-4 font-semibold"><MapPin size={17} />{t("transportUx.mapExpand")}<ChevronDown size={16} className="ml-auto" /></summary>
      {mapOpen && <RouteMap items={items} segment={verifiedRoute ? activeSegment : undefined} segments={options.map((option) => option.segment)}
        selectedSegmentIndex={selectedOptionIndex} onSelectSegment={(index) => setSelectedOptions((current) => ({ ...current, [requestKey]: index }))}
        fromItemId={fromItemId} toItemId={toItemId} travelMode={mode}
        mapCapabilities={preview?.map_capabilities ?? activeSegment?.map_capabilities ?? (navigationResult?.key === navigationKey ? navigationResult.map_capabilities : undefined)}
        variant="drawer" countryCode={trip.destination_country_code} externalOnly={isExternalPreview || !verifiedRoute} />}
    </details>

    <div className={`route-apply-bar ${styles.applyBar}`}><div className="route-apply-selection min-w-0"><span className="block text-xs text-[var(--muted)]">{t("currentChoice")}</span><strong className="block">{modeLabel(mode)}{activeSegment ? `${options.length ? ` · ${t("optionNumber", { index: selectedOptionIndex + 1 })}` : ""} · ${t(isManualTiming(activeSegment) ? "transportUx.manualDuration" : "durationMinutes", { minutes: activeSegment.duration_minutes })}` : ""}</strong>{isManualTiming(activeSegment) && <span className="block text-xs">{t("transportUx.manualReserved")}</span>}{isEstimatedTiming(activeSegment) && <span className="block text-xs">{t("estimatedTiming")}</span>}</div>
      {externalMode ? primaryNavigation
        ? <a href={safeExternalHref(primaryNavigation.web_url)} target="_blank" rel="noopener noreferrer" className={actionClass}>{t("transportUx.viewExternally", { provider: primaryNavigation.label })}<ExternalLink size={16} /></a>
        : <button type="button" onClick={openManual} disabled={applying || unresolvedItems.length > 0} className={actionClass}>{t("manualEntry")}</button>
        : <button type="button" aria-label={canApplyPreview ? t("applyThisRoute") : undefined} onClick={() => canApplyPreview ? void applyPreview() : void previewMode(mode)} disabled={applying || Boolean(loadingMode) || unresolvedItems.length > 0 || !fromItem || !toItem || (isApplied && !localError) || (cannotQuery && !canApplyPreview)} className={actionClass}>{applying || loadingMode ? <Loader2 size={17} className="animate-spin" /> : isApplied && !localError ? <Check size={17} /> : null}{localError ? t("retry") : loadingMode ? t("fetchingShort") : isApplied ? t("applied") : canApplyPreview ? <><span className="route-apply-label-long">{t("applyThisRoute")}</span><span className="route-apply-label-short">{t("applyShort")}</span></> : selectedExpired || routeState === "stale" ? timelineCopy.requery : timelineCopy.query}</button>}
    </div>
  </div></div>;
}
