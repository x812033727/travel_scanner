"use client";

import {
  ArrowDown,
  ArrowUp,
  Check,
  Copy,
  GripVertical,
  Link2,
  LockKeyhole,
  Plus,
  RefreshCw,
  Save,
  Trash2,
  Unlock,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { api, isUsageInsufficient, twd } from "@/lib/api";
import { groupTripItems, type Trip, type TripItem } from "@/lib/trip-types";

function normalize(items: TripItem[]) {
  const positions = new Map<string, number>();
  return [...items]
    .sort((a, b) => a.day_date.localeCompare(b.day_date) || a.position - b.position)
    .map((item) => {
      const position = positions.get(item.day_date) || 0;
      positions.set(item.day_date, position + 1);
      return { ...item, position };
    });
}

export function TripEditor({ tripId }: { tripId: string }) {
  const router = useRouter();
  const [trip, setTrip] = useState<Trip>();
  const [items, setItems] = useState<TripItem[]>([]);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [busy, setBusy] = useState(false);
  const [shareUrl, setShareUrl] = useState("");
  const [dragged, setDragged] = useState<string>();

  useEffect(() => {
    api<Trip>(`/trips/${tripId}`)
      .then((value) => { setTrip(value); setItems(value.items); })
      .catch((reason: Error) => setError(reason.message));
  }, [tripId]);

  const groups = useMemo(() => groupTripItems(items), [items]);

  function patchItem(id: string, patch: Partial<TripItem>) {
    setItems((current) => current.map((item) => item.id === id ? { ...item, ...patch } : item));
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
      if (!source || !target || source.day_date !== target.day_date) return current;
      return normalize(current.map((item) => item.id === source.id ? { ...item, position: target.position } : item.id === target.id ? { ...item, position: source.position } : item));
    });
    setDragged(undefined);
  }

  function add(day: string) {
    const position = items.filter((item) => item.day_date === day).length;
    setItems((current) => [...current, {
      id: crypto.randomUUID(),
      item_type: "custom",
      day_date: day,
      position,
      title: "新的行程安排",
      location_name: "",
      locked: false,
      is_estimated: true,
      data: { source_mode: "estimate" },
    }]);
  }

  async function save() {
    if (!trip) return;
    setBusy(true); setError(undefined); setNotice(undefined);
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/itinerary`, {
        method: "PUT",
        body: JSON.stringify({ version: trip.version, items: normalize(items) }),
      });
      setTrip(updated); setItems(updated.items); setNotice("行程已儲存");
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  async function reoptimize() {
    if (!trip) return;
    setBusy(true); setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/reoptimize`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
      });
      setTrip(updated); setItems(updated.items); setNotice(updated.usage?.status === "charged" ? "已重新最佳化並扣除 1 次；固定項目完整保留" : "已重新檢查其餘安排，本次未扣次");
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        router.push("/pricing");
        return;
      }
      setError(`${(reason as Error).message}；本次未扣次。`);
    }
    finally { setBusy(false); }
  }

  async function share() {
    if (!trip) return;
    try {
      const result = await api<{ share_url: string }>(`/trips/${trip.id}/share`, { method: "POST" });
      setShareUrl(result.share_url);
      setTrip({ ...trip, share_enabled: true });
      await navigator.clipboard?.writeText(result.share_url);
      setNotice("新的唯讀連結已建立並複製；再次建立會使舊連結失效。");
    } catch (reason) { setError((reason as Error).message); }
  }

  async function revoke() {
    if (!trip) return;
    try {
      await api(`/trips/${trip.id}/share`, { method: "DELETE" });
      setShareUrl(""); setTrip({ ...trip, share_enabled: false }); setNotice("分享連結已撤銷");
    } catch (reason) { setError((reason as Error).message); }
  }

  if (error && !trip) return <main className="mx-auto max-w-4xl px-5 py-16"><p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{error}，請先登入或確認旅程仍存在。</p></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16 text-[var(--muted)]">正在載入旅程…</main>;

  return <main className="mx-auto max-w-6xl px-5 pb-20 md:px-8">
    <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8"><div className="flex flex-wrap items-start justify-between gap-5"><div><p className="text-sm font-semibold text-[var(--teal)]">可編輯旅程 · 版本 {trip.version}</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{trip.name}</h1><p className="mt-3 text-[var(--muted)]">目前總額 {twd.format(Number(trip.total_price))}。鎖定航班與住宿後，可自由調整每日動線。</p><p className="mt-2 text-xs text-[var(--muted)]">重新最佳化成功才扣 1 次；失敗不扣。</p></div><div className="flex flex-wrap gap-2"><button onClick={reoptimize} disabled={busy} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold"><RefreshCw size={16} />重新最佳化</button><button onClick={save} disabled={busy} className="flex items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white"><Save size={16} />{busy ? "處理中…" : "儲存變更"}</button></div></div>{error && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-4 text-sm text-red-800">{error}</p>}{notice && <p className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"><Check size={16} />{notice}</p>}</section>

    <section className="mb-6 flex flex-wrap items-center gap-3 rounded-2xl border border-[var(--line)] bg-white p-4"><button onClick={share} className="flex items-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-[var(--teal)]"><Link2 size={16} />建立新的秘密連結</button>{trip.share_enabled && <button onClick={revoke} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-red-700">撤銷目前連結</button>}{shareUrl && <label className="flex min-w-0 flex-1 items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm"><input aria-label="唯讀分享連結" readOnly value={shareUrl} className="min-w-0 flex-1 bg-transparent outline-none" /><button aria-label="複製分享連結" onClick={() => navigator.clipboard?.writeText(shareUrl)}><Copy size={16} /></button></label>}</section>

    <div className="space-y-6">{groups.map(([day, rows], dayIndex) => <section key={day} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-6"><div className="mb-4 flex items-center justify-between"><div><p className="text-xs font-semibold tracking-[.16em] text-[var(--teal)]">DAY {dayIndex + 1}</p><h2 className="mt-1 text-xl font-bold">{day}</h2></div><button onClick={() => add(day)} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold"><Plus size={16} />新增安排</button></div><ol className="space-y-3">{rows.map((item, index) => <li key={item.id} draggable onDragStart={() => setDragged(item.id)} onDragOver={(event) => event.preventDefault()} onDrop={() => drop(item.id)} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 md:grid-cols-[auto_1fr_auto]"><span className="mt-3 cursor-grab text-[var(--muted)]" title="拖曳排序"><GripVertical size={19} /></span><div className="grid gap-3 md:grid-cols-2"><label className="text-xs font-semibold text-[var(--muted)]">安排名稱<input value={item.title} onChange={(event) => patchItem(item.id, { title: event.target.value })} className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm text-[var(--ink)]" /></label><label className="text-xs font-semibold text-[var(--muted)]">地點<input value={item.location_name || ""} onChange={(event) => patchItem(item.id, { location_name: event.target.value })} className="mt-1 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm text-[var(--ink)]" /></label><p className="md:col-span-2 text-xs text-[var(--muted)]">{item.is_estimated ? "估算安排，儲存後仍會保留標示" : "已確認來源的安排"}</p></div><div className="flex items-start gap-1"><button aria-label="上移" disabled={index === 0} onClick={() => move(item.id, -1)} className="rounded-lg p-2 disabled:opacity-30"><ArrowUp size={16} /></button><button aria-label="下移" disabled={index === rows.length - 1} onClick={() => move(item.id, 1)} className="rounded-lg p-2 disabled:opacity-30"><ArrowDown size={16} /></button><button aria-label={item.locked ? "解除鎖定" : "鎖定"} onClick={() => patchItem(item.id, { locked: !item.locked })} className="rounded-lg p-2 text-[var(--teal)]">{item.locked ? <LockKeyhole size={16} /> : <Unlock size={16} />}</button><button aria-label="刪除安排" onClick={() => setItems((current) => current.filter((row) => row.id !== item.id))} className="rounded-lg p-2 text-red-700"><Trash2 size={16} /></button></div></li>)}</ol></section>)}</div>
  </main>;
}
