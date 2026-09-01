"use client";

import { Map, MapPin } from "lucide-react";
import { useLocale } from "next-intl";
import Script from "next/script";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "@/lib/api";
import type { RouteSegment, TravelMode, TripItem } from "@/lib/trip-types";

type PublicMapConfig = {
  google_maps_browser_key?: string | null;
  google_maps_embed_enabled?: boolean;
  naver_maps_browser_client_id?: string | null;
  naver_dynamic_map_enabled?: boolean;
};
type Coordinate = { latitude: number; longitude: number };

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
      let byte: number;
      do {
        byte = value.charCodeAt(index++) - 63;
        result |= (byte & 0x1f) << shift;
        shift += 5;
      } while (byte >= 0x20 && index <= value.length);
      return (result & 1) ? ~(result >> 1) : result >> 1;
    };
    latitude += read();
    longitude += read();
    points.push({ latitude: latitude / 1e5, longitude: longitude / 1e5 });
  }
  return points;
}

function isGooglePlace(item?: TripItem) {
  const metadataProvider = typeof item?.data.place_provider === "string"
    ? item.data.place_provider
    : undefined;
  const provider = item?.location_provider || metadataProvider || item?.location_source;
  return provider === "google_places" || (!provider && Boolean(item?.provider_place_id));
}

export function RouteMap({
  items,
  segment,
  fromItemId,
  toItemId,
  travelMode = "transit",
  variant = "drawer",
  countryCode,
}: {
  items: TripItem[];
  segment?: RouteSegment;
  fromItemId?: string;
  toItemId?: string;
  travelMode?: TravelMode;
  variant?: "sidebar" | "drawer";
  countryCode?: string | null;
}) {
  const locale = useLocale();
  const mapElement = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<{ destroy?(): void } | undefined>(undefined);
  const [config, setConfig] = useState<PublicMapConfig>({});
  const [naverFailed, setNaverFailed] = useState(false);
  useEffect(() => {
    let active = true;
    api<PublicMapConfig>("/runtime/public-config")
      .then((value) => { if (active) setConfig(value); })
      .catch(() => {
        if (active) setConfig({
          google_maps_browser_key: process.env.NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY,
          google_maps_embed_enabled: true,
        });
      });
    return () => { active = false; };
  }, []);

  const origin = items.find((item) => item.id === (segment?.from_item_id || fromItemId));
  const destination = items.find((item) => item.id === (segment?.to_item_id || toItemId));
  const hasCoordinates = origin?.latitude != null && origin.longitude != null
    && destination?.latitude != null && destination.longitude != null;
  const useNaver = countryCode?.toUpperCase() === "KR"
    && config.naver_dynamic_map_enabled
    && Boolean(config.naver_maps_browser_client_id)
    && !naverFailed;
  const routeCoordinates = useMemo(
    () => decodePolyline(segment?.encoded_polyline),
    [segment?.encoded_polyline],
  );

  const renderNaverMap = useCallback(() => {
    if (!useNaver || !hasCoordinates || !mapElement.current || !window.naver?.maps || !origin || !destination) return;
    const maps = window.naver.maps;
    mapInstance.current?.destroy?.();
    const originPoint = new maps.LatLng(origin.latitude as number, origin.longitude as number);
    const destinationPoint = new maps.LatLng(destination.latitude as number, destination.longitude as number);
    const map = new maps.Map(mapElement.current, { center: originPoint, zoom: 13, minZoom: 6, zoomControl: true });
    mapInstance.current = map;
    new maps.Marker({ position: originPoint, map, title: origin.title });
    new maps.Marker({ position: destinationPoint, map, title: destination.title });
    const visiblePoints = routeCoordinates.length
      ? routeCoordinates
      : [
          { latitude: origin.latitude as number, longitude: origin.longitude as number },
          { latitude: destination.latitude as number, longitude: destination.longitude as number },
        ];
    if (routeCoordinates.length) {
      new maps.Polyline({
        map,
        path: routeCoordinates.map((point) => new maps.LatLng(point.latitude, point.longitude)),
        strokeColor: "#177c78",
        strokeOpacity: 0.9,
        strokeWeight: 5,
      });
    }
    const latitudes = visiblePoints.map((point) => point.latitude);
    const longitudes = visiblePoints.map((point) => point.longitude);
    const bounds = new maps.LatLngBounds(
      new maps.LatLng(Math.min(...latitudes), Math.min(...longitudes)),
      new maps.LatLng(Math.max(...latitudes), Math.max(...longitudes)),
    );
    map.fitBounds(bounds, { top: 36, right: 36, bottom: 36, left: 36 });
  }, [destination, hasCoordinates, origin, routeCoordinates, useNaver]);

  useEffect(() => {
    if (window.naver?.maps) renderNaverMap();
    return () => {
      mapInstance.current?.destroy?.();
      mapInstance.current = undefined;
    };
  }, [renderNaverMap]);

  const browserKey = config.google_maps_embed_enabled === false ? undefined : config.google_maps_browser_key;
  const originValue = origin?.provider_place_id && isGooglePlace(origin)
    ? `place_id:${origin.provider_place_id}`
    : `${origin?.latitude},${origin?.longitude}`;
  const destinationValue = destination?.provider_place_id && isGooglePlace(destination)
    ? `place_id:${destination.provider_place_id}`
    : `${destination?.latitude},${destination?.longitude}`;
  const selectedMode = segment?.travel_mode || travelMode;
  const mapMode = selectedMode === "walk" ? "walking" : selectedMode === "drive" ? "driving" : "transit";
  const googleSrc = browserKey && hasCoordinates
    ? `https://www.google.com/maps/embed/v1/directions?key=${encodeURIComponent(browserKey)}&origin=${encodeURIComponent(originValue)}&destination=${encodeURIComponent(destinationValue)}&mode=${mapMode}&language=${encodeURIComponent(locale)}`
    : undefined;
  const emptyTitle = !hasCoordinates ? "補齊兩端地點後顯示地圖" : segment ? "路線步驟已準備好" : "正在準備路線預覽";
  const mapSource = useNaver ? "NAVER Maps" : googleSrc ? "Google Maps" : undefined;

  return <section className={`route-map-card route-map-${variant}`}>
    {useNaver && <Script id="naver-maps-js" src={`https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=${encodeURIComponent(config.naver_maps_browser_client_id || "")}`} strategy="afterInteractive" onReady={renderNaverMap} onError={() => setNaverFailed(true)} />}
    <div className="flex items-center justify-between border-b border-[var(--line)] px-5 py-3.5"><div className="min-w-0"><p className="text-xs font-semibold tracking-[.14em] text-[var(--teal)]">ROUTE MAP{mapSource ? ` · ${mapSource}` : ""}</p><h2 className="mt-1 truncate font-bold">{segment ? `這段約 ${segment.duration_minutes} 分鐘` : `${origin?.title || "起點"} → ${destination?.title || "終點"}`}</h2></div><Map size={20} className="shrink-0 text-[var(--teal)]" /></div>
    <div className="route-map-frame overflow-hidden">
      {useNaver && hasCoordinates
        ? <div ref={mapElement} role="img" aria-label={`${origin?.title || "起點"}到${destination?.title || "終點"}的 NAVER 地圖`} className="absolute inset-0 h-full w-full" />
        : googleSrc
          ? <iframe title="行程路線地圖" src={googleSrc} className="absolute inset-0 h-full w-full border-0" loading="lazy" allowFullScreen referrerPolicy="strict-origin-when-cross-origin" />
          : <div className="absolute inset-0 grid place-items-center bg-[linear-gradient(135deg,#edf5f1,#f8f5ee)] p-6 text-center"><div><MapPin size={28} className="mx-auto text-[var(--teal)]" /><p className="mt-3 font-semibold">{emptyTitle}</p><p className="mx-auto mt-2 max-w-xs text-sm leading-6 text-[var(--muted)]">{!hasCoordinates ? "系統會依目的地使用 NAVER 或 Google 自動配對；仍找不到時可直接編輯景點。" : "地圖服務未設定或受網域限制；仍可查看已驗證的移動步驟。"}</p></div></div>}
    </div>
    <div className="border-t border-[var(--line)] px-5 py-3 text-xs text-[var(--muted)]">{segment ? `${segment.schedule_mode === "preview" ? "預覽班次" : segment.schedule_mode === "live" ? "目前路線" : "指定日期班次"} · ${segment.attribution}` : `${mapSource || "地圖"}僅供視覺確認；有 Provider 路線後才可套用時間`}</div>
  </section>;
}
