"use client";

import { ArrowDown, ArrowUp, Check, Clock3, Copy, GripVertical, Link2, LockKeyhole, Plus, RefreshCw, Route as RouteIcon, Save, Sparkles, Trash2, Unlock } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { PlacePicker } from "@/components/place-picker";
import { AffiliatePartnerOptions } from "@/components/affiliate-partner-options";
import { RouteMap } from "@/components/route-map";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { api, isUsageInsufficient, twd } from "@/lib/api";
import type { RouteSegment, Trip, TripItem } from "@/lib/trip-types";

function normalize(items: TripItem[]) {
  const positions = new Map<string, number>();
  return [...items].sort((a, b) => a.day_date.localeCompare(b.day_date) || a.position - b.position).map((item) => {
    const position = positions.get(item.day_date) || 0;
    positions.set(item.day_date, position + 1);
    return { ...item, position };
  });
}

function daysBetween(start?: string | null, end?: string | null) {
  if (!start || !end) return [];
  const days: string[] = [];
  const cursor = new Date(`${start}T00:00:00Z`);
  const last = new Date(`${end}T00:00:00Z`);
  while (cursor <= last && days.length < 62) {
    days.push(cursor.toISOString().slice(0, 10));
    cursor.setUTCDate(cursor.getUTCDate() + 1);
  }
  return days;
}

function timeValue(value?: string | null) { return value?.match(/T(\d{2}:\d{2})/)?.[1] || ""; }
function withTime(day: string, value: string) { return value ? `${day}T${value}:00` : null; }

function countryCodesForTrip(trip?: Trip): string[] {
  if (!trip) return ["jp", "kr", "th"];
  if (trip.timezone === "Asia/Tokyo") return ["jp"];
  if (trip.timezone === "Asia/Seoul") return ["kr"];
  if (trip.timezone === "Asia/Bangkok") return ["th"];
  const destination = trip.destination_name || "";
  if (/日本|東京|大阪|京都|北海道|沖繩|福岡|名古屋/.test(destination)) return ["jp"];
  if (/韓國|首爾|釜山|濟州/.test(destination)) return ["kr"];
  if (/泰國|曼谷|清邁|普吉|喀比/.test(destination)) return ["th"];
  return ["jp", "kr", "th"];
}

type RouteResponse = { segments: RouteSegment[]; failed_pairs: unknown[]; partial: boolean };
type Place = { place_id: string; provider: string; name: string; address?: string | null; latitude?: number | null; longitude?: number | null; opening_hours?: string[]; google_maps_url?: string | null; attribution?: string };

export function TripEditor({ tripId }: { tripId: string }) {
  const router = useRouter();
  const [trip, setTrip] = useState<Trip>();
  const [items, setItems] = useState<TripItem[]>([]);
  const [routes, setRoutes] = useState<RouteSegment[]>([]);
  const [selectedRoute, setSelectedRoute] = useState<RouteSegment>();
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [busy, setBusy] = useState(false);
  const [shareUrl, setShareUrl] = useState("");
  const [dragged, setDragged] = useState<string>();

  useEffect(() => {
    api<Trip>(`/trips/${tripId}`)
      .then((value) => { setTrip(value); setItems(value.items); setRoutes(value.route_segments || []); setSelectedRoute(value.route_segments?.[0]); })
      .catch((reason: Error) => setError(reason.message));
  }, [tripId]);

  const days = useMemo(() => {
    const explicit = daysBetween(trip?.start_date, trip?.end_date);
    return explicit.length ? explicit : [...new Set(items.map((item) => item.day_date))].sort();
  }, [items, trip?.end_date, trip?.start_date]);
  const groups = useMemo(() => days.map((day) => [day, normalize(items).filter((item) => item.day_date === day)] as const), [days, items]);
  const placeCountryCodes = useMemo(() => countryCodesForTrip(trip), [trip]);
  const placeBias = useMemo(() => {
    const reference = items.find((item) => item.latitude != null && item.longitude != null);
    return reference?.latitude != null && reference.longitude != null
      ? { latitude: reference.latitude, longitude: reference.longitude }
      : undefined;
  }, [items]);

  function patchItem(id: string, patch: Partial<TripItem>) {
    setItems((current) => current.map((item) => item.id === id ? { ...item, ...patch } : item));
    setRoutes((current) => current.filter((route) => route.from_item_id !== id && route.to_item_id !== id));
  }

  function move(id: string, direction: -1 | 1) {
    setItems((current) => {
      const item = current.find((row) => row.id === id);
      if (!item) return current;
      const sameDay = current.filter((row) => row.day_date === item.day_date).sort((a, b) => a.position - b.position);
      const index = sameDay.findIndex((row) => row.id === id);
      const target = sameDay[index + direction];
      if (!target) return current;
      return normalize(current.map((row) => row.id === id ? { ...row, position: target.position } : row.id === target.id ? { ...row, position: item.position } : row));
    });
  }

  function drop(targetId: string) {
    if (!dragged || dragged === targetId) return;
    setItems((current) => {
      const source = current.find((item) => item.id === dragged);
      const target = current.find((item) => item.id === targetId);
      if (!source || !target) return current;
      return normalize(current.map((item) => item.id === source.id ? { ...item, day_date: target.day_date, position: target.position } : item.id === target.id && source.day_date === target.day_date ? { ...item, position: source.position } : item));
    });
    setRoutes([]);
    setDragged(undefined);
  }

  function add(day: string) {
    const position = items.filter((item) => item.day_date === day).length;
    setItems((current) => [...current, { id: crypto.randomUUID(), item_type: "custom", day_date: day, position, title: "新的行程安排", location_name: "", locked: false, fixed_time: false, is_estimated: true, duration_minutes: 60, data: { source_mode: "manual" } }]);
  }

  function choosePlace(item: TripItem, place: Place) {
    patchItem(item.id, { title: item.title === "新的行程安排" ? place.name : item.title, location_name: place.address || place.name, latitude: place.latitude, longitude: place.longitude, provider_place_id: place.place_id, location_source: place.provider, is_estimated: false, data: { ...item.data, opening_hours: place.opening_hours || [], google_maps_url: place.google_maps_url, attribution: place.attribution } });
  }

  async function save(showNotice = true): Promise<Trip | undefined> {
    if (!trip) return undefined;
    setBusy(true); setError(undefined); setNotice(undefined);
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/itinerary`, { method: "PUT", body: JSON.stringify({ version: trip.version, items: normalize(items), route_preference: trip.route_preference }) });
      setTrip(updated); setItems(updated.items); setRoutes(updated.route_segments || []); if (showNotice) setNotice("行程已儲存"); return updated;
    } catch (reason) { setError((reason as Error).message); return undefined; }
    finally { setBusy(false); }
  }

  async function computeRoutes(day: string, refresh = false) {
    if (!trip) return;
    const currentTrip = await save(false);
    if (!currentTrip) return;
    setBusy(true); setError(undefined); setNotice(undefined);
    try {
      const result = await api<RouteResponse>(`/trips/${currentTrip.id}/routes/${refresh ? "refresh" : "compute"}`, { method: "POST", body: JSON.stringify({ version: currentTrip.version, day_date: day, route_preference: currentTrip.route_preference }) });
      const dayIds = new Set(items.filter((item) => item.day_date === day).map((item) => item.id));
      setRoutes((current) => [...current.filter((route) => !dayIds.has(route.from_item_id)), ...result.segments]);
      setSelectedRoute(result.segments[0]);
      const providers = [...new Set(result.segments.map((segment) => segment.attribution))].join("、");
      setNotice(result.partial ? `已透過 ${providers} 更新可取得的路線；部分地點尚未確認位置。` : `路線已透過 ${providers} 更新，本次不扣次。`);
    } catch (reason) { setError(`${(reason as Error).message}；本次未扣次。`); }
    finally { setBusy(false); }
  }

  async function optimize(day?: string) {
    if (!trip) return;
    const currentTrip = await save(false);
    if (!currentTrip) return;
    setBusy(true); setError(undefined); setNotice(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/itinerary/optimize`, { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() }, body: JSON.stringify({ version: currentTrip.version, day_date: day || null, route_preference: currentTrip.route_preference }) });
      setTrip(updated); setItems(updated.items); setRoutes(updated.route_segments || []); setSelectedRoute(updated.route_segments?.[0]);
      setNotice(updated.usage?.status === "charged" ? "已完成同日動線最佳化並扣除 1 次；鎖定與預約項目保持不動。" : "已檢查動線，本次未扣次。");
    } catch (reason) {
      if (isUsageInsufficient(reason)) { router.push("/pricing"); return; }
      setError(`${(reason as Error).message}；本次未扣次。`);
    } finally { setBusy(false); }
  }

  async function reoptimizePrices() {
    if (!trip) return;
    setBusy(true); setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/reoptimize`, { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() } });
      setTrip(updated); setItems(updated.items); setNotice(updated.usage?.status === "charged" ? "已重新查價並扣除 1 次。" : "已重新檢查價格，本次未扣次。");
    } catch (reason) { if (isUsageInsufficient(reason)) router.push("/pricing"); else setError(`${(reason as Error).message}；本次未扣次。`); }
    finally { setBusy(false); }
  }

  async function share() {
    if (!trip) return;
    try { const result = await api<{ share_url: string }>(`/trips/${trip.id}/share`, { method: "POST" }); setShareUrl(result.share_url); setTrip({ ...trip, share_enabled: true }); await navigator.clipboard?.writeText(result.share_url); setNotice("新的唯讀連結已建立並複製。"); }
    catch (reason) { setError((reason as Error).message); }
  }
  async function revoke() { if (!trip) return; try { await api(`/trips/${trip.id}/share`, { method: "DELETE" }); setShareUrl(""); setTrip({ ...trip, share_enabled: false }); setNotice("分享連結已撤銷"); } catch (reason) { setError((reason as Error).message); } }

  if (error && !trip) return <main className="mx-auto max-w-4xl px-5 py-16"><p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{error}，請先登入或確認旅程仍存在。</p></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16 text-[var(--muted)]">正在載入旅程…</main>;
  const today = new Intl.DateTimeFormat("en-CA", { timeZone: trip.timezone || "UTC" }).format(new Date());

  return <main className="mx-auto max-w-7xl px-5 pb-20 md:px-8">
    <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
      <div className="flex flex-wrap items-start justify-between gap-5"><div><p className="text-sm font-semibold text-[var(--teal)]">行程規劃器 · 版本 {trip.version}</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{trip.name}</h1><p className="mt-3 text-[var(--muted)]">{trip.destination_name || "旅程"}{trip.start_date ? ` · ${trip.start_date} 至 ${trip.end_date}` : ""}{Number(trip.total_price) > 0 ? ` · ${twd.format(Number(trip.total_price))}` : ""}</p><p className="mt-2 text-xs text-[var(--muted)]">手動編輯與固定順序查路免費；整日／整趟最佳化成功才扣 1 次。</p></div><div className="flex flex-wrap gap-2"><button onClick={reoptimizePrices} disabled={busy || trip.mode === "manual"} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold disabled:opacity-40"><RefreshCw size={16} />重新查價</button><button onClick={() => optimize()} disabled={busy} className="flex items-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />最佳化整趟</button><button onClick={() => save()} disabled={busy} className="flex items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white"><Save size={16} />{busy ? "處理中…" : "儲存變更"}</button></div></div>
      {error && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-4 text-sm text-red-800">{error}</p>}{notice && <p className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"><Check size={16} />{notice}</p>}
    </section>

    <section className="mb-6 flex flex-wrap items-center gap-3 rounded-2xl border border-[var(--line)] bg-white p-4"><label className="flex items-center gap-2 text-sm font-semibold">路線偏好<select value={trip.route_preference || "FEWER_TRANSFERS"} onChange={(event) => setTrip({ ...trip, route_preference: event.target.value as Trip["route_preference"] })} className="rounded-xl border border-[var(--line)] bg-white px-3 py-2"><option value="FEWER_TRANSFERS">少轉乘</option><option value="FASTEST">最快抵達</option><option value="LESS_WALKING">少走路</option></select></label><span className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-xs font-semibold text-[var(--teal)]">地點與路線：Google Maps{placeCountryCodes[0] === "jp" ? " · 日本可備援 NAVITIME" : ""}</span><span className="h-6 w-px bg-[var(--line)]" /><button onClick={share} className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-semibold text-[var(--teal)]"><Link2 size={16} />建立唯讀連結</button>{trip.share_enabled && <button onClick={revoke} className="rounded-xl px-3 py-2 text-sm font-semibold text-red-700">撤銷連結</button>}{shareUrl && <label className="flex min-w-0 flex-1 items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm"><input aria-label="唯讀分享連結" readOnly value={shareUrl} className="min-w-0 flex-1 bg-transparent outline-none" /><button aria-label="複製分享連結" onClick={() => navigator.clipboard?.writeText(shareUrl)}><Copy size={16} /></button></label>}</section>

    <AffiliatePartnerOptions tripId={trip.id} modules={["flight", "hotel", "activities", "transport", "connectivity"]} title="這趟旅程的合作平台" />

    <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,.65fr)]"><div className="space-y-6">{groups.map(([day, rows], dayIndex) => { const hasRoutes = routes.some((route) => rows.some((item) => item.id === route.from_item_id)); return <section key={day} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-6"><div className="mb-4 flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-semibold tracking-[.16em] text-[var(--teal)]">DAY {dayIndex + 1}{day === today ? " · 當日模式" : ""}</p><h2 className="mt-1 text-xl font-bold">{day}</h2></div><div className="flex flex-wrap gap-2"><button onClick={() => computeRoutes(day, hasRoutes || day === today)} disabled={busy || rows.length < 2} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold disabled:opacity-40"><RouteIcon size={16} />{hasRoutes || day === today ? "重新整理路線" : "計算路線"}</button><button onClick={() => optimize(day)} disabled={busy || rows.length < 2} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold disabled:opacity-40"><Sparkles size={16} />最佳化當天</button><button onClick={() => add(day)} className="flex items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm font-semibold"><Plus size={16} />新增安排</button></div></div>
      {rows.length === 0 ? <button onClick={() => add(day)} className="w-full rounded-2xl border border-dashed border-[var(--line)] p-8 text-sm text-[var(--muted)]">這天還沒有安排，加入第一個地點</button> : <ol className="space-y-3">{rows.map((item, index) => { const segment = routes.find((route) => route.from_item_id === item.id && route.to_item_id === rows[index + 1]?.id); return <li key={item.id}><article draggable onDragStart={() => setDragged(item.id)} onDragOver={(event) => event.preventDefault()} onDrop={() => drop(item.id)} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 md:grid-cols-[auto_1fr_auto]"><span className="mt-3 cursor-grab text-[var(--muted)]" title="拖曳排序"><GripVertical size={19} /></span><div className="grid gap-3 md:grid-cols-2"><label className="text-xs font-semibold text-[var(--muted)]">安排名稱<input value={item.title} onChange={(event) => patchItem(item.id, { title: event.target.value })} className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm text-[var(--ink)]" /></label><label className="text-xs font-semibold text-[var(--muted)]">地點<PlacePicker value={item.location_name || ""} confirmed={Boolean(item.provider_place_id && item.latitude != null)} countryCodes={placeCountryCodes} bias={placeBias} onTextChange={(value) => patchItem(item.id, { location_name: value, provider_place_id: null, latitude: null, longitude: null, is_estimated: true })} onSelect={(place) => choosePlace(item, place)} /></label><label className="text-xs font-semibold text-[var(--muted)]">日期<select value={item.day_date} onChange={(event) => patchItem(item.id, { day_date: event.target.value, start_time: withTime(event.target.value, timeValue(item.start_time)) })} className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm">{days.map((value) => <option key={value} value={value}>{value}</option>)}</select></label><label className="text-xs font-semibold text-[var(--muted)]">開始時間<input type="time" value={timeValue(item.start_time)} onChange={(event) => patchItem(item.id, { start_time: withTime(item.day_date, event.target.value) })} className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm" /></label><label className="text-xs font-semibold text-[var(--muted)]">停留時間<select value={item.duration_minutes || 60} onChange={(event) => patchItem(item.id, { duration_minutes: Number(event.target.value) })} className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm"><option value="30">30 分鐘</option><option value="60">1 小時</option><option value="90">1.5 小時</option><option value="120">2 小時</option><option value="180">3 小時</option></select></label><label className="text-xs font-semibold text-[var(--muted)]">備註<input value={item.notes || ""} onChange={(event) => patchItem(item.id, { notes: event.target.value })} placeholder="票券、集合方式或集合點" className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm" /></label><p className="md:col-span-2 flex items-center gap-2 text-xs text-[var(--muted)]">{item.provider_place_id ? <><Check size={13} className="text-emerald-600" />已從 Google Maps 確認地點，可計算路線</> : "請從 Google Maps 搜尋結果選取地點後再計算路線"}{item.fixed_time && <span className="rounded-full bg-violet-50 px-2 py-1 font-semibold text-violet-800">固定預約時間</span>}</p></div><div className="flex items-start gap-1"><button aria-label="上移" disabled={index === 0} onClick={() => move(item.id, -1)} className="rounded-lg p-2 disabled:opacity-30"><ArrowUp size={16} /></button><button aria-label="下移" disabled={index === rows.length - 1} onClick={() => move(item.id, 1)} className="rounded-lg p-2 disabled:opacity-30"><ArrowDown size={16} /></button><button aria-label={item.locked ? "解除鎖定" : "鎖定"} onClick={() => patchItem(item.id, { locked: !item.locked })} className="rounded-lg p-2 text-[var(--teal)]">{item.locked ? <LockKeyhole size={16} /> : <Unlock size={16} />}</button><button aria-label={item.fixed_time ? "取消固定時間" : "固定預約時間"} onClick={() => patchItem(item.id, { fixed_time: !item.fixed_time })} className="rounded-lg p-2 text-violet-700"><Clock3 size={16} /></button><button aria-label="刪除安排" onClick={() => setItems((current) => current.filter((row) => row.id !== item.id))} className="rounded-lg p-2 text-red-700"><Trash2 size={16} /></button></div></article>{segment && <div className="mt-3"><RouteSegmentCard segment={segment} selected={selectedRoute?.from_item_id === segment.from_item_id} onSelect={() => setSelectedRoute(segment)} /></div>}</li>; })}</ol>}
    </section>; })}</div><RouteMap items={items} segment={selectedRoute} /></div>
  </main>;
}
