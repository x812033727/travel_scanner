"use client";

import { ChevronDown, ChevronUp, ExternalLink, Plane, RefreshCw } from "lucide-react";
import { useMemo, useState } from "react";
import { api, twd } from "@/lib/api";

type FlightSegment = {
  origin?: string;
  destination?: string;
  departure_time?: string;
  arrival_time?: string;
  airline?: string;
  flight_number?: string;
  leg_index?: number;
  departure_timezone?: string | null;
  arrival_timezone?: string | null;
};

export type FlightCardOffer = {
  id: string;
  provider?: string;
  source_mode?: "live" | "test" | "mock" | "estimate";
  is_fallback?: boolean;
  airline?: unknown;
  marketing_airline?: unknown;
  operating_airlines?: unknown;
  selling_agent?: unknown;
  origin?: unknown;
  destination?: unknown;
  departure_time?: string;
  arrival_time?: string;
  return_departure_time?: string | null;
  return_arrival_time?: string | null;
  flight_number?: unknown;
  segments?: FlightSegment[];
  stops?: unknown;
  duration_minutes?: unknown;
  total_price?: unknown;
  retrieved_at?: string;
  last_verified_at?: string;
  clickout_available?: boolean;
  baggage_summary?: unknown;
  checked_baggage_kg?: unknown;
  carry_on?: unknown;
  arrival_day_offset?: unknown;
};

type RefreshResult = { new_price: string | number; price_change: string | number; still_available: boolean; refreshed_at: string };

function localParts(value?: string | null) {
  const match = value?.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  return match ? { date: `${Number(match[2])}/${Number(match[3])}`, isoDate: `${match[1]}-${match[2]}-${match[3]}`, time: `${match[4]}:${match[5]}` } : null;
}

function durationLabel(minutes: number) {
  if (!minutes || minutes < 1) return "供應商未提供";
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return `${hours ? `${hours} 小時` : ""}${hours && rest ? " " : ""}${rest ? `${rest} 分` : ""}`;
}

function legDuration(segments: FlightSegment[], departure?: string | null, arrival?: string | null) {
  const start = segments[0]?.departure_time || departure;
  const end = segments.at(-1)?.arrival_time || arrival;
  if (!start || !end) return 0;
  const value = Math.round((Date.parse(end) - Date.parse(start)) / 60000);
  return Number.isFinite(value) && value > 0 ? value : 0;
}

function splitSegments(offer: FlightCardOffer) {
  const segments = offer.segments || [];
  if (segments.some((segment) => Number(segment.leg_index || 0) > 0)) {
    return [segments.filter((segment) => Number(segment.leg_index || 0) === 0), segments.filter((segment) => Number(segment.leg_index || 0) === 1)];
  }
  const returnIndex = segments.findIndex((segment, index) => index > 0 && segment.origin === String(offer.destination || ""));
  return returnIndex > 0 ? [segments.slice(0, returnIndex), segments.slice(returnIndex)] : [segments, []];
}

function FlightLeg({ label, segments, departure, arrival, fallbackOrigin, fallbackDestination }: { label: string; segments: FlightSegment[]; departure?: string | null; arrival?: string | null; fallbackOrigin: string; fallbackDestination: string }) {
  const first = segments[0];
  const last = segments.at(-1);
  const depart = localParts(first?.departure_time || departure);
  const arrive = localParts(last?.arrival_time || arrival);
  const numbers = Array.from(new Set(segments.map((segment) => segment.flight_number).filter(Boolean)));
  const dayOffset = depart && arrive ? Math.round((Date.parse(arrive.isoDate) - Date.parse(depart.isoDate)) / 86400000) : 0;
  return <div className="grid gap-3 rounded-xl bg-[var(--paper)] p-4 sm:grid-cols-[72px_1fr_auto] sm:items-center">
    <div><span className="rounded-full bg-white px-2.5 py-1 text-xs font-bold text-[var(--teal-dark)]">{label}</span><p className="mt-2 text-xs text-[var(--muted)]">{depart?.date || "供應商未提供"}</p></div>
    <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
      <div><strong className="text-xl">{depart?.time || "供應商未提供"}</strong><p className="text-sm text-[var(--muted)]">{first?.origin || fallbackOrigin}</p></div>
      <div className="min-w-20 text-center"><p className="text-xs text-[var(--muted)]">{durationLabel(legDuration(segments, departure, arrival))}</p><div className="my-1 h-px bg-[var(--line)]" /><p className="text-xs">{Math.max(0, segments.length - 1) ? `${segments.length - 1} 次轉機` : "直飛"}</p></div>
      <div className="text-right"><strong className="text-xl">{arrive?.time || "供應商未提供"}{dayOffset > 0 ? <sup className="ml-1 text-xs text-[var(--coral)]">+{dayOffset}</sup> : null}</strong><p className="text-sm text-[var(--muted)]">{last?.destination || fallbackDestination}</p></div>
    </div>
    <p className="text-xs text-[var(--muted)] sm:text-right">{numbers.length ? numbers.join("、") : "班號：供應商未提供"}<br />當地時間</p>
  </div>;
}

export function FlightOfferCard({ offer, fallbackUrl }: { offer: FlightCardOffer; fallbackUrl: string }) {
  const [price, setPrice] = useState(Number(offer.total_price || 0));
  const [verifiedAt, setVerifiedAt] = useState(offer.last_verified_at || offer.retrieved_at);
  const [refreshing, setRefreshing] = useState(false);
  const [message, setMessage] = useState("");
  const [expanded, setExpanded] = useState(false);
  const [outbound, returning] = useMemo(() => splitSegments(offer), [offer]);
  const operating = Array.isArray(offer.operating_airlines) ? offer.operating_airlines.join("、") : "";
  const baggage = offer.baggage_summary ? String(offer.baggage_summary) : Number(offer.checked_baggage_kg || 0) > 0 ? `托運 ${offer.checked_baggage_kg} kg` : offer.carry_on ? "含手提行李" : "行李需向售票端確認";

  async function refresh() {
    setRefreshing(true); setMessage("");
    try {
      const result = await api<RefreshResult>(`/offers/${offer.id}/refresh`, { method: "POST" });
      setPrice(Number(result.new_price)); setVerifiedAt(result.refreshed_at);
      setMessage(result.still_available ? "已更新為供應商最新價格" : "此票價目前已售罄");
    } catch (error) { setMessage((error as Error).message); }
    finally { setRefreshing(false); }
  }

  return <article className="overflow-hidden rounded-[1.5rem] border border-[var(--line)] bg-white">
    <div className="p-5 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4"><div><p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--teal)]"><Plane size={16} />{offer.source_mode === "estimate" ? "彈性日期估算" : "即時航班價格"}{offer.is_fallback ? " · 備援來源" : ""}</p><h2 className="mt-1 text-xl font-bold">{String(offer.marketing_airline || offer.airline || "航空公司待確認")}</h2><p className="mt-1 text-xs text-[var(--muted)]">{operating ? `實際承運：${operating} · ` : ""}售票端：{String(offer.selling_agent || "重新確認時顯示")}</p></div><div className="text-right"><strong className="text-xl">{twd.format(price)}</strong><p className="mt-1 text-xs text-[var(--muted)]">{baggage}</p></div></div>
      <div className="mt-4 space-y-2">
        <FlightLeg label="去程" segments={outbound} departure={offer.departure_time} arrival={offer.arrival_time} fallbackOrigin={String(offer.origin || "")} fallbackDestination={String(offer.destination || "")} />
        {(returning.length || offer.return_departure_time) ? <FlightLeg label="回程" segments={returning} departure={offer.return_departure_time} arrival={offer.return_arrival_time} fallbackOrigin={String(offer.destination || "")} fallbackDestination={String(offer.origin || "")} /> : null}
      </div>
      {(outbound.length + returning.length > 0) && <button type="button" onClick={() => setExpanded((value) => !value)} className="mt-3 flex items-center gap-1 text-sm font-semibold text-[var(--teal)]">{expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}{expanded ? "收合詳細班次" : "查看詳細班次"}</button>}
      {expanded && <div className="mt-3 space-y-3 border-l-2 border-[var(--teal-soft)] pl-4">{([[
        "去程", outbound,
      ], ["回程", returning]] as Array<[string, FlightSegment[]]>).map(([label, segments]) => segments.length ? <div key={label}><p className="mb-2 text-xs font-bold text-[var(--teal-dark)]">{label}</p>{segments.map((segment, index) => { const depart = localParts(segment.departure_time); const arrive = localParts(segment.arrival_time); const previous = segments[index - 1]; const layover = previous?.arrival_time && segment.departure_time ? Math.round((Date.parse(segment.departure_time) - Date.parse(previous.arrival_time)) / 60000) : 0; return <div key={`${segment.flight_number || "segment"}-${index}`} className="mb-2 rounded-xl border border-[var(--line)] p-3 text-sm">{index > 0 && layover > 0 ? <p className="mb-2 text-xs font-semibold text-[var(--coral)]">轉機停留 {durationLabel(layover)}</p> : null}<div className="flex flex-wrap justify-between gap-2"><strong>{segment.airline || "航空公司：供應商未提供"} · {segment.flight_number || "班號：供應商未提供"}</strong><span>{depart?.date || "供應商未提供"} {depart?.time || "供應商未提供"} {segment.origin || "—"} → {arrive?.time || "供應商未提供"} {segment.destination || "—"}</span></div><p className="mt-1 text-xs text-[var(--muted)]">{segment.departure_timezone || "當地時間"} → {segment.arrival_timezone || "當地時間"}</p></div>; })}</div> : null)}</div>}
      <p className="mt-3 text-xs text-[var(--muted)]">來源：{offer.provider || "未標示"}{verifiedAt ? ` · 驗價 ${new Date(verifiedAt).toLocaleString("zh-TW")}` : ""}</p>
      {offer.provider === "skyscanner" && <p className="mt-2 text-xs text-[var(--muted)]">Powered by <a className="font-semibold underline" href="https://www.skyscanner.net" target="_blank" rel="noreferrer">Skyscanner</a></p>}
      {message && <p className="mt-3 text-sm text-[var(--coral)]" role="status">{message}</p>}
      <div className="mt-4 grid gap-2 sm:grid-cols-2"><button type="button" onClick={refresh} disabled={refreshing || offer.source_mode === "estimate"} className="flex items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold disabled:opacity-50"><RefreshCw size={16} className={refreshing ? "animate-spin" : ""} />{refreshing ? "驗價中" : "重新驗價"}</button>{offer.clickout_available ? <form action={`/api/travel/offers/${offer.id}/clickout`} method="post" target="_blank"><button className="flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white" type="submit">前往訂票 <ExternalLink size={16} /></button></form> : <a href={fallbackUrl} target="_blank" rel="noreferrer" className="flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]">外站重新確認<ExternalLink size={16} /></a>}</div>
    </div>
  </article>;
}
