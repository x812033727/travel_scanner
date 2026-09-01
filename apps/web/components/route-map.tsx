"use client";

import { Map, MapPin } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { RouteSegment, TripItem } from "@/lib/trip-types";

export function RouteMap({ items, segment }: { items: TripItem[]; segment?: RouteSegment }) {
  const locale = useLocale();
  const [browserKey, setBrowserKey] = useState<string>();
  useEffect(() => {
    let active = true;
    api<{ google_maps_browser_key?: string | null }>("/runtime/public-config")
      .then((config) => { if (active) setBrowserKey(config.google_maps_browser_key || undefined); })
      .catch(() => { if (active) setBrowserKey(process.env.NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY); });
    return () => { active = false; };
  }, []);
  const origin = items.find((item) => item.id === segment?.from_item_id);
  const destination = items.find((item) => item.id === segment?.to_item_id);
  const canEmbed = browserKey && origin?.latitude != null && origin.longitude != null && destination?.latitude != null && destination.longitude != null;
  const originValue = origin?.provider_place_id ? `place_id:${origin.provider_place_id}` : `${origin?.latitude},${origin?.longitude}`;
  const destinationValue = destination?.provider_place_id ? `place_id:${destination.provider_place_id}` : `${destination?.latitude},${destination?.longitude}`;
  const mapMode = segment?.travel_mode === "walk" ? "walking" : segment?.travel_mode === "drive" ? "driving" : "transit";
  const src = canEmbed ? `https://www.google.com/maps/embed/v1/directions?key=${encodeURIComponent(browserKey)}&origin=${encodeURIComponent(originValue)}&destination=${encodeURIComponent(destinationValue)}&mode=${mapMode}&language=${encodeURIComponent(locale)}` : undefined;
  return <section className="overflow-hidden rounded-[1.75rem] border border-[var(--line)] bg-white shadow-sm lg:sticky lg:top-5">
    <div className="flex items-center justify-between border-b border-[var(--line)] px-5 py-4"><div><p className="text-xs font-semibold tracking-[.14em] text-[var(--teal)]">ROUTE MAP</p><h2 className="mt-1 font-bold">{segment ? `這段約 ${segment.duration_minutes} 分鐘` : "選擇一段路線"}</h2></div><Map size={20} className="text-[var(--teal)]" /></div>
    {src ? <iframe title="行程路線地圖" src={src} className="h-[420px] w-full border-0" loading="lazy" allowFullScreen referrerPolicy="strict-origin-when-cross-origin" /> : <div className="grid min-h-[360px] place-items-center bg-[linear-gradient(135deg,#edf5f1,#f8f5ee)] p-8 text-center"><div><MapPin size={30} className="mx-auto text-[var(--teal)]" /><p className="mt-3 font-semibold">{segment ? "路線步驟已準備好" : "計算路線後可在這裡查看地圖"}</p><p className="mx-auto mt-2 max-w-xs text-sm leading-6 text-[var(--muted)]">{segment ? "設定受網域限制的 Google Maps Embed 金鑰後，這裡會顯示互動路線；詳細搭車步驟仍可直接查看。" : "先用 Google Maps 確認每個地點，再選擇「計算路線」。"}</p></div></div>}
    {segment && <div className="border-t border-[var(--line)] px-5 py-3 text-xs text-[var(--muted)]">{segment.schedule_mode === "preview" ? "預覽班次" : segment.schedule_mode === "live" ? "目前路線" : "指定日期班次"} · {segment.attribution}</div>}
  </section>;
}
