"use client";

import { AlertCircle, Check, Clock3, Hotel, LoaderCircle, MapPinned, Plane, Save, Sparkles, TrainFront } from "lucide-react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { api, twd } from "@/lib/api";

type Parsed = { origin?: string; destination?: string; destination_region?: string; departure_month?: string; travelers: { adults: number }; trip_length_days?: number; budget_twd?: number; interests: string[]; avoid_red_eye: boolean; hotel_min_rating?: number; confidence: number; missing_fields: string[] };
type Offer = Record<string, string | number | boolean | unknown[]> & { id: string };
type Cost = { confirmed_cost: string | number; estimated_cost: string | number; total_cost: string | number; components: Array<{ label: string; amount: string | number; confidence: string }> };
type Plan = { id: string; mode: string; title: string; duplicate: boolean; total_cost: Cost; flight?: Offer; hotel?: Offer; activity?: Offer; transport?: Offer; pros: string[]; cons: string[]; compared_with_cheapest: { price_difference: string | number; flight_minutes_saved: number } };

const stages = [{ key: "flight", label: "機票", icon: Plane }, { key: "hotel", label: "住宿", icon: Hotel }, { key: "activities", label: "活動", icon: MapPinned }, { key: "transport", label: "交通", icon: TrainFront }];

export function SearchExperience() {
  const params = useSearchParams();
  const text = params.get("q") || "";
  const [parsed, setParsed] = useState<Parsed | null>(null);
  const [progress, setProgress] = useState(0);
  const [done, setDone] = useState<string[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [offers, setOffers] = useState<Record<string, Offer[]>>({});
  const [searchId, setSearchId] = useState<string>();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  const started = useRef(false);

  useEffect(() => {
    if (!text || started.current) return;
    started.current = true;
    api<Parsed>("/ai/parse-trip", { method: "POST", body: JSON.stringify({ text }) }).then(setParsed).catch((reason: Error) => setError(reason.message));
  }, [text]);

  const dates = useMemo(() => {
    const departure = parsed?.departure_month ? new Date(parsed.departure_month) : new Date("2026-11-01");
    departure.setDate(10);
    const returning = new Date(departure);
    returning.setDate(departure.getDate() + (parsed?.trip_length_days || 5));
    return [departure.toISOString().slice(0, 10), returning.toISOString().slice(0, 10)];
  }, [parsed]);

  async function begin() {
    if (!parsed) return;
    setBusy(true); setError(undefined); setProgress(2);
    try {
      const accepted = await api<{ search_id: string }>("/searches", { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() }, body: JSON.stringify({ trip_type: "round_trip", origin: parsed.origin || "TPE", destination: parsed.destination || "NRT", departure_date: dates[0], return_date: dates[1], travelers: parsed.travelers, modules: ["flight", "hotel", "activities", "transport"], preferences: { budget_twd: parsed.budget_twd, avoid_red_eye: parsed.avoid_red_eye, hotel_min_rating: parsed.hotel_min_rating, optimization_mode: "balanced", interests: parsed.interests } }) });
      setSearchId(accepted.search_id);
      const stream = new EventSource(`/api/travel/searches/${accepted.search_id}/events`);
      stream.addEventListener("module.results", (message) => { const data = JSON.parse((message as MessageEvent).data); setProgress(data.progress); setOffers((current) => ({ ...current, [data.module]: data.offers })); });
      stream.addEventListener("provider.completed", (message) => { const data = JSON.parse((message as MessageEvent).data); if (data.status === "completed") setDone((current) => current.includes(data.module) ? current : [...current, data.module]); });
      stream.addEventListener("optimization.completed", (message) => { const data = JSON.parse((message as MessageEvent).data); setProgress(92); setPlans(data.plans); });
      stream.addEventListener("search.completed", () => { setProgress(100); setBusy(false); stream.close(); });
      stream.addEventListener("search.failed", () => { setError("搜尋未能取得任何結果，請稍後再試。"); setBusy(false); stream.close(); });
      stream.onerror = () => { if (progress < 100) setError("即時連線暫時中斷，可重新整理頁面查看結果。"); };
    } catch (reason) { setError((reason as Error).message); setBusy(false); }
  }

  async function save(plan: Plan) {
    if (!searchId) return;
    try { await api("/trips", { method: "POST", body: JSON.stringify({ search_id: searchId, plan_id: plan.id, name: `${plan.title}・日本五日` }) }); alert("已儲存到我的旅程"); } catch (reason) { setError((reason as Error).message); }
  }

  async function refresh(offer: Offer) {
    try { const result = await api<{ old_price: number; new_price: number; still_available: boolean }>(`/offers/${offer.id}/refresh`, { method: "POST" }); alert(result.still_available ? `重新驗價：${twd.format(result.old_price)} → ${twd.format(result.new_price)}` : "此方案已售罄"); } catch (reason) { setError((reason as Error).message); }
  }

  return (
    <main className="mx-auto max-w-6xl px-5 pb-20 md:px-8">
      <section className="mb-8 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[0_20px_70px_rgba(16,42,43,.08)] md:p-8">
        <p className="mb-3 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />你的旅行需求</p>
        <h1 className="text-2xl font-bold md:text-3xl">{text || "進階旅程搜尋"}</h1>
        {parsed && <div className="mt-5 flex flex-wrap gap-2 text-sm">{[`${parsed.travelers.adults} 位旅客`, `${parsed.trip_length_days || 5} 天`, parsed.budget_twd ? `預算 ${twd.format(parsed.budget_twd)}` : null, parsed.avoid_red_eye ? "避開紅眼" : null, ...parsed.interests].filter(Boolean).map((tag) => <span key={tag} className="rounded-full bg-[#edf5f1] px-3 py-1.5 text-[var(--teal-dark)]">{tag}</span>)}</div>}
        {!searchId && <button disabled={!parsed || busy} onClick={begin} className="mt-6 rounded-2xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white disabled:opacity-50">確認條件並開始搜尋</button>}
        {error && <div role="alert" className="mt-5 flex items-start gap-2 rounded-xl bg-red-50 p-4 text-sm text-red-800"><AlertCircle size={18} className="mt-0.5 shrink-0" /><span>{error} {error.includes("sign") || error.includes("登入") ? <Link className="underline" href="/login">前往登入</Link> : null}</span></div>}
      </section>

      {searchId && <section aria-label="搜尋進度" className="mb-9 rounded-3xl border border-[var(--line)] bg-white p-6">
        <div className="mb-4 flex items-center justify-between"><strong>{progress === 100 ? "分析完成" : "正在組合你的旅程"}</strong><span className="font-mono text-sm text-[var(--muted)]">{progress}%</span></div>
        <div className="h-2 overflow-hidden rounded-full bg-[#e4ebe6]"><div className="h-full rounded-full bg-[var(--teal)] transition-all" style={{ width: `${progress}%` }} /></div>
        <div className="mt-5 grid grid-cols-4 gap-3">{stages.map(({ key, label, icon: Icon }) => <div key={key} className={`flex items-center gap-2 rounded-xl p-2 text-sm ${done.includes(key) ? "text-[var(--teal)]" : "text-[var(--muted)]"}`}>{done.includes(key) ? <Check size={17} /> : <LoaderCircle size={17} className={busy ? "animate-spin" : ""} />}<Icon size={17} className="hidden md:block" />{label}</div>)}</div>
      </section>}

      {plans.length > 0 && <section><div className="mb-5 flex items-end justify-between"><div><p className="text-sm font-semibold text-[var(--coral)]">三種選擇，一眼看懂差異</p><h2 className="mt-1 text-3xl font-bold">適合你的完整旅程</h2></div><span className="hidden text-sm text-[var(--muted)] md:block">Confirmed 與 estimated 費用分開計算</span></div>
        <div className="grid gap-5 lg:grid-cols-3">{plans.map((plan, index) => <article key={plan.mode} className={`relative rounded-[1.75rem] border bg-white p-6 ${index === 0 ? "border-[var(--teal)] shadow-[0_20px_60px_rgba(13,107,104,.14)]" : "border-[var(--line)]"}`}>
          {index === 0 && <span className="absolute -top-3 left-6 rounded-full bg-[var(--teal)] px-3 py-1 text-xs font-semibold text-white">BEST OVERALL</span>}
          <div className="flex items-start justify-between"><div><p className="text-sm text-[var(--muted)]">{plan.title}</p><h3 className="mt-1 text-3xl font-bold">{twd.format(Number(plan.total_cost.total_cost))}</h3></div><button onClick={() => save(plan)} aria-label={`儲存${plan.title}`} className="rounded-xl border border-[var(--line)] p-2 text-[var(--teal)]"><Save size={18} /></button></div>
          <div className="my-5 space-y-3 border-y border-[var(--line)] py-5 text-sm">{plan.flight && <button onClick={() => refresh(plan.flight!)} className="flex w-full justify-between text-left"><span className="flex items-center gap-2"><Plane size={16} />{String(plan.flight.airline)}</span><span>{twd.format(Number(plan.flight.total_price))} / 人</span></button>}{plan.hotel && <div className="flex justify-between"><span className="flex items-center gap-2"><Hotel size={16} />{String(plan.hotel.hotel_name)}</span><span>{twd.format(Number(plan.hotel.total_price))}</span></div>}{plan.transport && <div className="flex justify-between"><span className="flex items-center gap-2"><TrainFront size={16} />{String(plan.transport.transport_type)}</span><span>{twd.format(Number(plan.transport.price))}</span></div>}</div>
          {Number(plan.compared_with_cheapest.price_difference) > 0 && <p className="mb-4 rounded-xl bg-[#fff4ef] p-3 text-sm text-[#994b3e]">比 Cheapest 多 {twd.format(Number(plan.compared_with_cheapest.price_difference))}，換取更好的時間與便利性。</p>}
          <ul className="space-y-2 text-sm">{plan.pros.map((item) => <li key={item} className="flex gap-2"><Check size={16} className="mt-0.5 shrink-0 text-[var(--teal)]" />{item}</li>)}{plan.cons.map((item) => <li key={item} className="flex gap-2 text-[var(--muted)]"><Clock3 size={16} className="mt-0.5 shrink-0" />{item}</li>)}</ul>
          <div className="mt-5 border-t border-[var(--line)] pt-4 text-xs text-[var(--muted)]">已確認 {twd.format(Number(plan.total_cost.confirmed_cost))} · 估算 {twd.format(Number(plan.total_cost.estimated_cost))}</div>
        </article>)}</div>
      </section>}
      {searchId && !plans.length && Object.keys(offers).length > 0 && <p className="text-center text-[var(--muted)]">已取得 {Object.values(offers).flat().length} 筆報價，正在比較組合…</p>}
    </main>
  );
}

