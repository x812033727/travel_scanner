"use client";

import { Map, MapPin } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { RouteSegment, TravelMode, TripItem } from "@/lib/trip-types";

type PublicMapConfig = {
  google_maps_browser_key?: string | null;
  google_maps_embed_enabled?: boolean;
};

export function RouteMap({
  items,
  segment,
  fromItemId,
  toItemId,
  travelMode = "transit",
  variant = "drawer",
}: {
  items: TripItem[];
  segment?: RouteSegment;
  fromItemId?: string;
  toItemId?: string;
  travelMode?: TravelMode;
  variant?: "sidebar" | "drawer";
}) {
  const locale = useLocale();
  const [browserKey, setBrowserKey] = useState<string>();
  useEffect(() => {
    let active = true;
    api<PublicMapConfig>("/runtime/public-config")
      .then((config) => {
        if (active && config.google_maps_embed_enabled !== false) {
          setBrowserKey(config.google_maps_browser_key || undefined);
        }
      })
      .catch(() => {
        if (active) setBrowserKey(process.env.NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY);
      });
    return () => { active = false; };
  }, []);
  const origin = items.find((item) => item.id === (segment?.from_item_id || fromItemId));
  const destination = items.find((item) => item.id === (segment?.to_item_id || toItemId));
  const hasCoordinates = origin?.latitude != null && origin.longitude != null
    && destination?.latitude != null && destination.longitude != null;
  const canEmbed = Boolean(browserKey && hasCoordinates);
  const originValue = origin?.provider_place_id
    ? `place_id:${origin.provider_place_id}`
    : `${origin?.latitude},${origin?.longitude}`;
  const destinationValue = destination?.provider_place_id
    ? `place_id:${destination.provider_place_id}`
    : `${destination?.latitude},${destination?.longitude}`;
  const selectedMode = segment?.travel_mode || travelMode;
  const mapMode = selectedMode === "walk"
    ? "walking"
    : selectedMode === "drive" ? "driving" : "transit";
  const src = canEmbed
    ? `https://www.google.com/maps/embed/v1/directions?key=${encodeURIComponent(browserKey || "")}&origin=${encodeURIComponent(originValue)}&destination=${encodeURIComponent(destinationValue)}&mode=${mapMode}&language=${encodeURIComponent(locale)}`
    : undefined;
  const emptyTitle = !hasCoordinates
    ? "補齊兩端地點後顯示地圖"
    : segment ? "路線步驟已準備好" : "正在準備路線預覽";

  return <section className={`route-map-card route-map-${variant}`}>
    <div className="flex items-center justify-between border-b border-[var(--line)] px-5 py-3.5"><div className="min-w-0"><p className="text-xs font-semibold tracking-[.14em] text-[var(--teal)]">ROUTE MAP</p><h2 className="mt-1 truncate font-bold">{segment ? `這段約 ${segment.duration_minutes} 分鐘` : `${origin?.title || "起點"} → ${destination?.title || "終點"}`}</h2></div><Map size={20} className="shrink-0 text-[var(--teal)]" /></div>
    <div className="route-map-frame">
      {src ? <iframe title="行程路線地圖" src={src} className="absolute inset-0 h-full w-full border-0" loading="lazy" allowFullScreen referrerPolicy="strict-origin-when-cross-origin" /> : <div className="absolute inset-0 grid place-items-center bg-[linear-gradient(135deg,#edf5f1,#f8f5ee)] p-6 text-center"><div><MapPin size={28} className="mx-auto text-[var(--teal)]" /><p className="mt-3 font-semibold">{emptyTitle}</p><p className="mx-auto mt-2 max-w-xs text-sm leading-6 text-[var(--muted)]">{!hasCoordinates ? "系統會先嘗試 Google 自動配對；仍找不到時可直接編輯景點。" : "地圖金鑰若受網域限制，仍可查看已驗證的搭車步驟。"}</p></div></div>}
    </div>
    <div className="border-t border-[var(--line)] px-5 py-3 text-xs text-[var(--muted)]">{segment ? `${segment.schedule_mode === "preview" ? "預覽班次" : segment.schedule_mode === "live" ? "目前路線" : "指定日期班次"} · ${segment.attribution}` : "地圖僅供視覺確認；有 Provider 路線後才可套用時間"}</div>
  </section>;
}
