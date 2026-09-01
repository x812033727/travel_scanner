"use client";

import { ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { ItineraryTimeline } from "@/components/itinerary-timeline";
import { api } from "@/lib/api";
import type { Trip } from "@/lib/trip-types";

export function SharedTripView({ token }: { token: string }) {
  const [trip, setTrip] = useState<Trip>();
  const [error, setError] = useState<string>();
  useEffect(() => {
    api<Trip>(`/shared-trips/${token}`).then(setTrip).catch((reason: Error) => setError(reason.message));
  }, [token]);
  if (error) return <main className="mx-auto max-w-4xl px-5 py-16"><p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">這個分享連結不存在或已被撤銷。</p></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16 text-[var(--muted)]">正在載入分享旅程…</main>;
  return <main className="mx-auto max-w-4xl px-5 pb-20 md:px-8"><section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><ShieldCheck size={17} />唯讀分享旅程</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{trip.name}</h1><p className="mt-3 text-[var(--muted)]">{trip.destination_name || "旅程"} · 最後更新 {trip.updated_at ? new Date(trip.updated_at).toLocaleString("zh-TW") : "近期"}</p><p className="mt-4 rounded-xl bg-[var(--teal-soft)] p-3 text-sm text-[var(--teal-dark)]">交通班次、出口與價格可能變動；出發當日請重新確認。路線資料來源與更新時間標示於各移動段。</p></section><ItineraryTimeline items={trip.items} routes={trip.route_segments} timezone={trip.timezone} /></main>;
}
