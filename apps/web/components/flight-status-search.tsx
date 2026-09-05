"use client";

import { Clock3, LoaderCircle, LogIn, Map, Plane, Search } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { Link, usePathname } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { useSavedItems } from "@/components/saved-items-provider";
import { useOperationCharge } from "@/components/usage-catalog-provider";

type StatusItem = {
  item_id: string;
  fa_flight_id?: string | null;
  ident?: string | null;
  origin?: string;
  destination?: string;
  status?: string;
  schedule_only?: boolean;
  cancelled?: boolean;
  diverted?: boolean;
  departure_delay_seconds?: number | null;
  arrival_delay_seconds?: number | null;
  departure_terminal?: string | null;
  departure_gate?: string | null;
  arrival_terminal?: string | null;
  arrival_gate?: string | null;
  scheduled_out?: string | null;
  estimated_out?: string | null;
  actual_out?: string | null;
  scheduled_in?: string | null;
  estimated_in?: string | null;
  actual_in?: string | null;
  updated_at?: string;
};

type Lookup = {
  id: string;
  items: StatusItem[];
  cache_hit: boolean;
  usage?: { status: "reserved" | "charged" | "released"; uses: number };
};

type Track = {
  positions?: Array<{ latitude?: number; longitude?: number; altitude?: number; timestamp?: string }>;
  retrieved_at?: string;
  cache_hit?: boolean;
};

const statusLabels: Record<string, string> = {
  schedule_verified: "班表已核對",
  scheduled: "預定",
  en_route: "飛行中",
  arrived: "已抵達",
  cancelled: "已取消",
  diverted: "轉降",
};

function time(value?: string | null) {
  return value ? new Date(value).toLocaleString("zh-TW", { dateStyle: "medium", timeStyle: "short" }) : "尚未提供";
}

function TrackPreview({ track }: { track: Track }) {
  const positions = track.positions || [];
  if (!positions.length) return <p className="mt-3 text-sm text-[var(--muted)]">FlightAware 尚未提供實際位置。</p>;
  const latitudes = positions.map((item) => Number(item.latitude)).filter(Number.isFinite);
  const longitudes = positions.map((item) => Number(item.longitude)).filter(Number.isFinite);
  if (!latitudes.length || !longitudes.length) return null;
  const minLat = Math.min(...latitudes); const maxLat = Math.max(...latitudes);
  const minLng = Math.min(...longitudes); const maxLng = Math.max(...longitudes);
  const points = positions.map((item) => {
    const x = 15 + ((Number(item.longitude) - minLng) / Math.max(0.001, maxLng - minLng)) * 370;
    const y = 145 - ((Number(item.latitude) - minLat) / Math.max(0.001, maxLat - minLat)) * 130;
    return `${x},${y}`;
  }).join(" ");
  const latest = positions.at(-1);
  return <div className="mt-4 overflow-hidden rounded-xl border border-sky-200 bg-sky-50 p-3">
    <svg viewBox="0 0 400 160" role="img" aria-label="FlightAware 實際航跡" className="h-48 w-full">
      <path d="M0 40 C90 5 160 85 250 35 S360 25 400 70" fill="none" stroke="#d5e6e5" strokeWidth="18" />
      <polyline points={points} fill="none" stroke="#0d6b68" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
      {points && <circle cx={points.split(" ").at(-1)?.split(",")[0]} cy={points.split(" ").at(-1)?.split(",")[1]} r="6" fill="#e4765c" />}
    </svg>
    <p className="text-xs text-sky-950">最新位置：{latest?.latitude?.toFixed(3)}, {latest?.longitude?.toFixed(3)}{latest?.altitude ? ` · 高度 ${latest.altitude}` : ""} · Powered by FlightAware</p>
  </div>;
}

export function FlightStatusSearch() {
  const charge = useOperationCharge("flight_status_lookup");
  // The lookup charges a use, so a visitor must not see a live charge button:
  // the layout-level session is the one auth probe every public page already pays for.
  const session = useSavedItems();
  const pathname = usePathname();
  const usage = useTranslations("usage");
  const [mode, setMode] = useState<"ident" | "route">("ident");
  const [ident, setIdent] = useState("");
  const [origin, setOrigin] = useState("TPE");
  const [destination, setDestination] = useState("NRT");
  const [departureDate, setDepartureDate] = useState("");
  const [lookup, setLookup] = useState<Lookup>();
  const [tracks, setTracks] = useState<Record<string, Track>>({});
  const [busy, setBusy] = useState(false);
  const [trackBusy, setTrackBusy] = useState<string>();
  const [error, setError] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault(); setBusy(true); setError(""); setLookup(undefined); setTracks({});
    try {
      const body = mode === "ident" ? { ident, departure_date: departureDate } : { origin, destination, departure_date: departureDate };
      setLookup(await api<Lookup>("/flights/status-lookups", { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() }, body: JSON.stringify(body) }));
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  async function loadTrack(item: StatusItem) {
    if (!lookup) return;
    setTrackBusy(item.item_id); setError("");
    try {
      const result = await api<Track>(`/flights/status-lookups/${lookup.id}/items/${item.item_id}/track`);
      setTracks((current) => ({ ...current, [item.item_id]: result }));
    } catch (reason) { setError((reason as Error).message); }
    finally { setTrackBusy(undefined); }
  }

  return <main className="mx-auto max-w-5xl px-5 pb-20 md:px-8">
    <section className="rounded-[2rem] bg-gradient-to-br from-[var(--teal-dark)] to-[var(--teal)] p-6 text-white md:p-10">
      <p className="text-sm font-semibold text-white/75">FLIGHTAWARE 航班動態</p>
      <h1 className="mt-2 text-3xl font-bold md:text-5xl">查航班狀態、延誤與登機門</h1>
      <p className="mt-3 max-w-2xl text-white/80">兩天內顯示即時動態；更遠日期只標示班表核對。票價請回旅遊搜尋比較。</p>
    </section>
    <form onSubmit={submit} className="relative -mt-5 mx-3 rounded-3xl border border-[var(--line)] bg-white p-5 shadow-[var(--shadow-lg)] md:mx-8 md:p-7">
      <div className="mb-5 flex gap-2" role="tablist"><button type="button" onClick={() => setMode("ident")} className={`rounded-full px-4 py-2 text-sm font-semibold ${mode === "ident" ? "bg-[var(--teal)] text-white" : "bg-[var(--paper)]"}`}>依班號</button><button type="button" onClick={() => setMode("route")} className={`rounded-full px-4 py-2 text-sm font-semibold ${mode === "route" ? "bg-[var(--teal)] text-white" : "bg-[var(--paper)]"}`}>依航線</button></div>
      <div className="grid gap-4 md:grid-cols-[1fr_1fr_auto]">
        {mode === "ident" ? <label className="grid gap-1 text-sm font-semibold">班號<input required value={ident} onChange={(event) => setIdent(event.target.value.toUpperCase())} placeholder="例如 BR198" className="rounded-xl border border-[var(--line)] px-4 py-3 font-normal uppercase" /></label> : <div className="grid grid-cols-2 gap-3"><label className="grid gap-1 text-sm font-semibold">出發機場<input required value={origin} onChange={(event) => setOrigin(event.target.value.toUpperCase())} maxLength={4} className="rounded-xl border border-[var(--line)] px-4 py-3 font-normal uppercase" /></label><label className="grid gap-1 text-sm font-semibold">抵達機場<input required value={destination} onChange={(event) => setDestination(event.target.value.toUpperCase())} maxLength={4} className="rounded-xl border border-[var(--line)] px-4 py-3 font-normal uppercase" /></label></div>}
        <label className="grid gap-1 text-sm font-semibold">出發日期<input required type="date" value={departureDate} onChange={(event) => setDepartureDate(event.target.value)} className="rounded-xl border border-[var(--line)] px-4 py-3 font-normal" /></label>
        {session.status === "signed_out"
          ? <Link href={loginPath(pathname)} className="mt-auto flex items-center justify-center gap-2 rounded-xl bg-[var(--coral)] px-6 py-3 font-semibold text-white"><LogIn size={18} />{usage("signInToUse")} · {charge.label}</Link>
          : <button disabled={busy || charge.status !== "ready" || session.status === "loading"} className="mt-auto flex items-center justify-center gap-2 rounded-xl bg-[var(--coral)] px-6 py-3 font-semibold text-white disabled:opacity-60">{busy ? <LoaderCircle size={18} className="animate-spin" /> : <Search size={18} />}查詢 · {charge.label}</button>}
      </div>
      <p className="mt-3 text-xs text-[var(--muted)]">{charge.status === "ready" ? `快取命中、空結果或供應商失敗不扣次；成功取得新的外部資料才${charge.label}。` : charge.unavailableHelp}</p>
      {error && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-800">{error}</p>}
    </form>
    {lookup && <section className="mt-8 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2"><h2 className="text-2xl font-bold">查詢結果</h2><p className="text-sm text-[var(--muted)]">{lookup.cache_hit ? "快取命中，本次未扣次" : lookup.usage?.status === "charged" ? `已扣 ${lookup.usage.uses} 次` : "無結果，本次未扣次"}</p></div>
      {!lookup.items.length && <p className="rounded-2xl border border-dashed border-[var(--line)] bg-white p-10 text-center text-[var(--muted)]">找不到完全符合班號、日期與機場的航班；系統不會套用近似班次。</p>}
      {lookup.items.map((item) => <article key={item.item_id} className="rounded-2xl border border-[var(--line)] bg-white p-5 md:p-6">
        <div className="flex flex-wrap items-start justify-between gap-4"><div><p className="flex items-center gap-2 text-xs font-bold text-[var(--teal)]"><Plane size={16} />{item.ident || "班號未提供"}</p><h3 className="mt-1 text-2xl font-bold">{item.origin} → {item.destination}</h3></div><span className={`rounded-full px-3 py-1.5 text-sm font-semibold ${item.cancelled ? "bg-red-50 text-red-800" : "bg-emerald-50 text-emerald-800"}`}>{item.cancelled ? "已取消" : statusLabels[item.status || ""] || item.status || "狀態待確認"}</span></div>
        <div className="mt-4 grid gap-3 text-sm sm:grid-cols-2 lg:grid-cols-4"><p><strong className="block text-xs text-[var(--muted)]">預定出發</strong>{time(item.scheduled_out)}</p><p><strong className="block text-xs text-[var(--muted)]">最新出發</strong>{time(item.actual_out || item.estimated_out)}</p><p><strong className="block text-xs text-[var(--muted)]">航廈／登機門</strong>{item.departure_terminal || "—"}／{item.departure_gate || "—"}</p><p><strong className="block text-xs text-[var(--muted)]">延誤</strong>{Number(item.departure_delay_seconds || 0) > 0 ? `${Math.round(Number(item.departure_delay_seconds) / 60)} 分鐘` : "未標示延誤"}</p></div>
        <p className="mt-4 flex items-center gap-2 text-xs text-[var(--muted)]"><Clock3 size={15} />{item.schedule_only ? "未進入即時窗口，僅核對班表" : `FlightAware 更新：${time(item.updated_at)}`}</p>
        {item.fa_flight_id && !item.schedule_only && <button type="button" onClick={() => loadTrack(item)} disabled={trackBusy === item.item_id} className="mt-4 flex items-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-[var(--teal)]"><Map size={17} />{trackBusy === item.item_id ? "載入航跡…" : tracks[item.item_id] ? "重新載入航跡" : "顯示實際航跡"}</button>}
        {tracks[item.item_id] && <TrackPreview track={tracks[item.item_id]} />}
      </article>)}
    </section>}
  </main>;
}
