"use client";

import { Map, MapPin, TriangleAlert } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import Script from "next/script";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "@/lib/api";
import type { RouteMapCapabilities, RouteSegment, TravelMode, TripItem } from "@/lib/trip-types";

type PublicMapConfig = {
  google_maps_browser_key?: string | null;
  google_maps_embed_enabled?: boolean;
  google_maps_javascript_enabled?: boolean;
  naver_maps_browser_client_id?: string | null;
  naver_dynamic_map_enabled?: boolean;
};
type Coordinate = { latitude: number; longitude: number };
type MapOverlay = { setMap(map: unknown | null): void };
type GoogleMapInstance = {
  fitBounds(bounds: unknown, padding?: number | Record<string, number>): void;
};
type MapFailureReason = "load" | "authorization";
export type RouteMapProvider = "naver_maps" | "google_maps";

const GOOGLE_MAPS_SCRIPT_ID = "google-route-maps-js";
const GOOGLE_MAPS_READY_CALLBACK = "__mokaairGoogleMapsReady";
const GOOGLE_MAPS_READY_EVENT = "mokaair:google-maps-ready";

function decodePolyline(value?: string | null): Coordinate[] {
  if (!value) return [];
  const points: Coordinate[] = [];
  let index = 0;
  let latitude = 0;
  let longitude = 0;
  while (index < value.length) {
    const read = () => {
      let result = 0;
      let shift = 0;
      let byte = 0;
      do {
        if (index >= value.length) throw new Error("invalid_polyline");
        byte = value.charCodeAt(index++) - 63;
        result |= (byte & 0x1f) << shift;
        shift += 5;
      } while (byte >= 0x20);
      return (result & 1) ? ~(result >> 1) : result >> 1;
    };
    try {
      latitude += read();
      longitude += read();
    } catch {
      return [];
    }
    points.push({ latitude: latitude / 1e5, longitude: longitude / 1e5 });
  }
  return points;
}

export function RouteMap({
  items,
  segment,
  segments,
  selectedSegmentIndex = 0,
  onSelectSegment,
  fromItemId,
  toItemId,
  variant = "drawer",
  countryCode,
  travelMode,
  mapProvider,
  mapCapabilities,
  onMapProviderChange,
  externalOnly = false,
}: {
  items: TripItem[];
  segment?: RouteSegment;
  segments?: RouteSegment[];
  selectedSegmentIndex?: number;
  onSelectSegment?: (index: number) => void;
  fromItemId?: string;
  toItemId?: string;
  travelMode?: TravelMode;
  mapProvider?: RouteMapProvider;
  mapCapabilities?: RouteMapCapabilities;
  onMapProviderChange?: (provider: RouteMapProvider) => void;
  variant?: "sidebar" | "drawer";
  countryCode?: string | null;
  externalOnly?: boolean;
}) {
  const locale = useLocale();
  const t = useTranslations("trips.route");
  const isKorea = countryCode?.toUpperCase() === "KR";
  const mapElement = useRef<HTMLDivElement>(null);
  const googleMap = useRef<GoogleMapInstance | null>(null);
  const destroyMap = useRef<(() => void) | null>(null);
  const overlays = useRef<MapOverlay[]>([]);
  const [config, setConfig] = useState<PublicMapConfig>({});
  const [walkingMap, setWalkingMap] = useState<RouteMapProvider>("naver_maps");
  const mode = travelMode || segment?.travel_mode || segments?.[selectedSegmentIndex]?.travel_mode || "transit";
  const walkingProviders = mapCapabilities?.providers.length ? mapCapabilities.providers : ["naver_maps", "google_maps"] as const;
  const walkingChoice = mapProvider || walkingMap;
  const provider: RouteMapProvider = !isKorea || mode === "transit" ? "google_maps"
    : mode === "drive" ? "naver_maps" : walkingProviders.includes(walkingChoice)
      ? walkingChoice : mapCapabilities?.default_provider || "naver_maps";
  const [readyProviders, setReadyProviders] = useState<Partial<Record<RouteMapProvider, boolean>>>({});
  const [mapFailures, setMapFailures] = useState<Partial<Record<RouteMapProvider, MapFailureReason>>>(
    () => typeof window !== "undefined" && window.mokaairGoogleMapsAuthFailed
      ? { google_maps: "authorization" } : {},
  );
  const sdkReady = readyProviders[provider];
  const mapFailure = mapFailures[provider];
  const setProviderReady = useCallback((key: RouteMapProvider, ready: boolean) => {
    setReadyProviders((current) => current[key] === ready ? current : { ...current, [key]: ready });
  }, []);
  const failProvider = useCallback((key: RouteMapProvider, reason: MapFailureReason) => {
    setProviderReady(key, false);
    setMapFailures((current) => current[key] === reason ? current : { ...current, [key]: reason });
  }, [setProviderReady]);

  useEffect(() => {
    let active = true;
    api<PublicMapConfig>("/runtime/public-config")
      .then((value) => { if (active) setConfig(value); })
      .catch(() => {
        if (active) {
          setConfig({
            google_maps_javascript_enabled: false,
          });
        }
      });
    return () => { active = false; };
  }, []);

  const routeOptions = useMemo(
    () => segments?.length ? segments : segment ? [segment] : [],
    [segment, segments],
  );
  const selectedIndex = Math.min(Math.max(selectedSegmentIndex, 0), Math.max(0, routeOptions.length - 1));
  const selectedSegment = routeOptions[selectedIndex];
  const origin = items.find((item) => item.id === (selectedSegment?.from_item_id || fromItemId));
  const destination = items.find((item) => item.id === (selectedSegment?.to_item_id || toItemId));
  const hasCoordinates = origin?.latitude != null && origin.longitude != null
    && destination?.latitude != null && destination.longitude != null;
  const useNaver = provider === "naver_maps"
    && config.naver_dynamic_map_enabled
    && Boolean(config.naver_maps_browser_client_id);
  const javascriptAllowed = config.google_maps_javascript_enabled === true;
  const useGoogle = provider === "google_maps"
    && javascriptAllowed
    && Boolean(config.google_maps_browser_key);
  const mapFailed = Boolean(mapFailure);
  const optionCoordinates = useMemo(
    () => routeOptions.map((option) => {
      // A walking basemap is only an endpoint display. Provider geometry must
      // also stay on its permitted basemap; switching maps never computes a path.
      if (externalOnly || (isKorea && mode === "walk")) return [];
      if (provider === "naver_maps" && option.provider === "google_routes") return [];
      if (provider === "google_maps" && option.provider === "naver_maps") return [];
      return decodePolyline(option.encoded_polyline);
    }),
    [externalOnly, isKorea, mode, provider, routeOptions],
  );
  const showSchematic = hasCoordinates
    && (externalOnly || (optionCoordinates[selectedIndex]?.length || 0) < 2);

  const clearOverlays = useCallback(() => {
    for (const overlay of overlays.current) {
      if (provider === "google_maps") window.google?.maps.event?.clearInstanceListeners(overlay);
      else window.naver?.maps.Event.clearInstanceListeners?.(overlay);
      overlay.setMap(null);
    }
    overlays.current = [];
  }, [provider]);

  const disposeMap = useCallback(() => {
    clearOverlays();
    destroyMap.current?.();
    destroyMap.current = null;
    if (googleMap.current) {
      window.google?.maps.event?.clearInstanceListeners(googleMap.current);
      googleMap.current = null;
    }
    mapElement.current?.replaceChildren();
  }, [clearOverlays]);

  useEffect(() => {
    if (provider !== "google_maps") return;
    const previousHandler = window.gm_authFailure;
    const handleAuthorizationFailure = () => {
      window.mokaairGoogleMapsAuthFailed = true;
      failProvider("google_maps", "authorization");
    };
    window.gm_authFailure = handleAuthorizationFailure;
    return () => {
      if (window.gm_authFailure === handleAuthorizationFailure) {
        window.gm_authFailure = previousHandler;
      }
    };
  }, [failProvider, provider]);

  useEffect(() => {
    if (!useGoogle || mapFailed) return;
    let active = true;
    let timeoutId: number | undefined;
    const isReady = () => Boolean(window.google?.maps?.Map);
    const handleReady = () => {
      if (!active || !isReady() || window.mokaairGoogleMapsAuthFailed) return;
      if (timeoutId !== undefined) window.clearTimeout(timeoutId);
      setProviderReady("google_maps", true);
    };
    const handleLoadFailure = () => {
      if (!active) return;
      document.getElementById(GOOGLE_MAPS_SCRIPT_ID)?.remove();
      failProvider("google_maps", "load");
    };

    window.addEventListener(GOOGLE_MAPS_READY_EVENT, handleReady);
    if (isReady()) {
      handleReady();
    } else {
      window[GOOGLE_MAPS_READY_CALLBACK] = () => {
        window.dispatchEvent(new Event(GOOGLE_MAPS_READY_EVENT));
      };
      let script = document.getElementById(GOOGLE_MAPS_SCRIPT_ID) as HTMLScriptElement | null;
      if (!script) {
        script = document.createElement("script");
        script.id = GOOGLE_MAPS_SCRIPT_ID;
        script.async = true;
        script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(config.google_maps_browser_key || "")}&v=quarterly&loading=async&callback=${GOOGLE_MAPS_READY_CALLBACK}&auth_referrer_policy=origin&language=${encodeURIComponent(locale)}`;
        document.head.append(script);
      }
      script.addEventListener("error", handleLoadFailure, { once: true });
      timeoutId = window.setTimeout(() => {
        if (!isReady()) handleLoadFailure();
      }, 15_000);
    }

    return () => {
      active = false;
      if (timeoutId !== undefined) window.clearTimeout(timeoutId);
      window.removeEventListener(GOOGLE_MAPS_READY_EVENT, handleReady);
      document.getElementById(GOOGLE_MAPS_SCRIPT_ID)
        ?.removeEventListener("error", handleLoadFailure);
    };
  }, [config.google_maps_browser_key, failProvider, locale, mapFailed, setProviderReady, useGoogle]);

  const renderNaverMap = useCallback(() => {
    if (mapFailed || !useNaver || !hasCoordinates || !mapElement.current || !window.naver?.maps || !origin || !destination) return;
    disposeMap();
    const maps = window.naver.maps;
    const originPoint = new maps.LatLng(origin.latitude as number, origin.longitude as number);
    const destinationPoint = new maps.LatLng(destination.latitude as number, destination.longitude as number);
    const map = new maps.Map(mapElement.current, { center: originPoint, zoom: 13, minZoom: 6, zoomControl: true });
    destroyMap.current = () => map.destroy?.();
    overlays.current.push(
      new maps.Marker({ position: originPoint, map, title: `1 · ${origin.title}` }),
      new maps.Marker({ position: destinationPoint, map, title: `2 · ${destination.title}` }),
    );
    const visiblePoints: Coordinate[] = [
      { latitude: origin.latitude as number, longitude: origin.longitude as number },
      { latitude: destination.latitude as number, longitude: destination.longitude as number },
    ];
    optionCoordinates.forEach((coordinates, index) => {
      if (coordinates.length < 2) return;
      visiblePoints.push(...coordinates);
      const selected = index === selectedIndex;
      const line = new maps.Polyline({
        map,
        path: coordinates.map((point) => new maps.LatLng(point.latitude, point.longitude)),
        strokeColor: selected ? "#0f7773" : "#5f7776",
        strokeOpacity: selected ? 0.95 : 0.32,
        strokeWeight: selected ? 6 : 4,
        zIndex: selected ? 20 : 10,
        clickable: true,
      });
      maps.Event.addListener(line, "click", () => onSelectSegment?.(index));
      overlays.current.push(line);
    });
    if (showSchematic) {
      overlays.current.push(new maps.Polyline({
        map,
        path: [originPoint, destinationPoint],
        strokeColor: "#687878",
        strokeOpacity: 0.8,
        strokeWeight: 4,
        strokeStyle: "shortdash",
      }));
    }
    const latitudes = visiblePoints.map((point) => point.latitude);
    const longitudes = visiblePoints.map((point) => point.longitude);
    const bounds = new maps.LatLngBounds(
      new maps.LatLng(Math.min(...latitudes), Math.min(...longitudes)),
      new maps.LatLng(Math.max(...latitudes), Math.max(...longitudes)),
    );
    map.fitBounds(bounds, { top: 42, right: 42, bottom: 42, left: 42 });
  }, [destination, disposeMap, hasCoordinates, mapFailed, onSelectSegment, optionCoordinates, origin, selectedIndex, showSchematic, useNaver]);

  const renderGoogleMap = useCallback(() => {
    if (mapFailed || !useGoogle || !hasCoordinates || !mapElement.current || !window.google?.maps || !origin || !destination) return;
    clearOverlays();
    const maps = window.google.maps;
    const originPoint = { lat: origin.latitude as number, lng: origin.longitude as number };
    const destinationPoint = { lat: destination.latitude as number, lng: destination.longitude as number };
    const map = googleMap.current || new maps.Map(mapElement.current, {
      center: originPoint,
      zoom: 13,
      renderingType: maps.RenderingType?.RASTER || "RASTER",
      mapTypeControl: false,
      fullscreenControl: false,
      streetViewControl: false,
    });
    googleMap.current = map;
    overlays.current.push(
      new maps.Marker({ position: originPoint, map, label: "1", title: origin.title }),
      new maps.Marker({ position: destinationPoint, map, label: "2", title: destination.title }),
    );
    const bounds = new maps.LatLngBounds();
    bounds.extend(originPoint);
    bounds.extend(destinationPoint);
    optionCoordinates.forEach((coordinates, index) => {
      if (coordinates.length < 2) return;
      coordinates.forEach((point) => bounds.extend({ lat: point.latitude, lng: point.longitude }));
      const selected = index === selectedIndex;
      const line = new maps.Polyline({
        map,
        path: coordinates.map((point) => ({ lat: point.latitude, lng: point.longitude })),
        strokeColor: selected ? "#0f7773" : "#607473",
        strokeOpacity: selected ? 0.96 : 0.3,
        strokeWeight: selected ? 6 : 4,
        zIndex: selected ? 20 : 10,
        clickable: true,
      });
      line.addListener("click", () => onSelectSegment?.(index));
      overlays.current.push(line);
    });
    if (showSchematic) {
      overlays.current.push(new maps.Polyline({
        map,
        path: [originPoint, destinationPoint],
        strokeColor: "#687878",
        strokeOpacity: 0,
        strokeWeight: 4,
        icons: [{ icon: { path: "M 0,-1 0,1", strokeOpacity: 1, scale: 3 }, offset: "0", repeat: "16px" }],
      }));
    }
    map.fitBounds(bounds, 44);
  }, [clearOverlays, destination, hasCoordinates, mapFailed, onSelectSegment, optionCoordinates, origin, selectedIndex, showSchematic, useGoogle]);

  useEffect(() => {
    if (mapFailed) {
      disposeMap();
      return;
    }
    if (!sdkReady) return;
    let active = true;
    try {
      if (useNaver) renderNaverMap();
      if (useGoogle) renderGoogleMap();
    } catch {
      queueMicrotask(() => { if (active) failProvider(provider, "load"); });
    }
    return () => { active = false; };
  }, [disposeMap, failProvider, mapFailed, provider, renderGoogleMap, renderNaverMap, sdkReady, useGoogle, useNaver]);

  useEffect(() => disposeMap, [disposeMap]);

  const mapSource = provider === "naver_maps" ? "NAVER Maps" : "Google Maps";
  const mapEnabled = useNaver || useGoogle;
  const emptyTitle = !hasCoordinates
    ? t("mapMissingPlaces")
    : mapFailed
      ? t("mapLoadFailed")
      : provider === "google_maps" && Boolean(config.google_maps_browser_key) && !javascriptAllowed
        ? t("mapSafelyDisabled")
        : t("mapNotEnabled");
  const originName = origin?.title || t("startFallback");
  const destinationName = destination?.title || t("endFallback");

  return <section className={`route-map-card route-map-${variant}`} data-map-provider={provider}>
    {useNaver && <Script id="naver-maps-js" src={`https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=${encodeURIComponent(config.naver_maps_browser_client_id || "")}`} strategy="afterInteractive" onReady={() => setProviderReady("naver_maps", true)} onError={() => failProvider("naver_maps", "load")} />}
    <div className="border-b border-[var(--line)] px-5 py-3.5">
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0 flex-1"><p className="text-xs font-semibold tracking-[.14em] text-[var(--teal)]">{t("mapTitle")}{` · ${mapSource}`}</p><h2 className="mt-1 truncate font-bold">{selectedSegment ? t("mapOptionSummary", { index: selectedIndex + 1, minutes: selectedSegment.duration_minutes }) : `${originName} → ${destinationName}`}</h2></div>
        {isKorea && mode === "walk"
          ? <select aria-label={t("mapProviderLabel")} value={provider} onChange={(event) => { const next = event.target.value as RouteMapProvider; setWalkingMap(next); onMapProviderChange?.(next); }} className="min-h-11 max-w-[50%] shrink-0 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm font-semibold">{walkingProviders.map((value) => <option key={value} value={value}>{value === "naver_maps" ? "NAVER Maps" : "Google Maps"}</option>)}</select>
          : <Map size={20} className="shrink-0 text-[var(--teal)]" />}
      </div>
      {isKorea && mode === "walk" && <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{t("mapProviderHint")}</p>}
    </div>
    <div className="route-map-frame overflow-hidden">
      {mapEnabled && hasCoordinates && !mapFailed
        ? <div key={provider} ref={mapElement} role="img" aria-label={t("mapAria", { from: originName, to: destinationName, provider: mapSource })} className="absolute inset-0 h-full w-full" />
        : <div className="route-map-empty absolute inset-0 grid place-items-center p-6 text-center"><div>{mapFailed ? <TriangleAlert size={28} className="mx-auto text-amber-700" /> : <MapPin size={28} className="mx-auto text-[var(--teal)]" />}<p className="mt-3 font-semibold">{emptyTitle}</p><p className="mx-auto mt-2 max-w-xs text-sm leading-6 text-[var(--muted)]">{!hasCoordinates ? t("mapMissingHint") : mapFailure === "authorization" ? t("mapAuthorizationHint") : mapFailure === "load" ? t("mapLoadHint") : provider === "naver_maps" ? t("mapNaverHint") : Boolean(config.google_maps_browser_key) ? t("mapSafetyHint") : t("mapKeyHint")}</p></div></div>}
      {mapEnabled && hasCoordinates && showSchematic && !mapFailed && <div className="route-map-schematic-notice" role="status">{t("mapSchematic")}</div>}
    </div>
    <div className="border-t border-[var(--line)] px-5 py-3 text-xs text-[var(--muted)]">{showSchematic ? t("mapEndpointsOnly") : selectedSegment ? `${selectedSegment.provider === "manual" ? t("manualTiming") : selectedSegment.status === "estimated" || selectedSegment.provider === "estimate" || String(selectedSegment.schedule_mode) === "estimate" ? t("estimatedTiming") : selectedSegment.schedule_mode === "preview" ? t("nearTerm") : selectedSegment.schedule_mode === "live" ? t("liveRoute") : t("scheduled")} · ${selectedSegment.attribution}` : t("mapEndpointsOnly")}</div>
    {selectedSegment && <p className="px-5 pb-3 text-xs text-[var(--muted)]">{t("mapTimeSource", { provider: selectedSegment.provider === "manual" ? t("manualTiming") : selectedSegment.provider === "estimate" || selectedSegment.status === "estimated" || String(selectedSegment.schedule_mode) === "estimate" ? t("estimatedTiming") : selectedSegment.attribution })}</p>}
  </section>;
}
