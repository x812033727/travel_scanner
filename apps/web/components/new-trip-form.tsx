"use client";

import { ArrowRight, CalendarDays, MapPinned, Route } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { PlacePicker } from "@/components/place-picker";

type CreatedTrip = { id: string };

export function NewTripForm() {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [form, setForm] = useState({
    name: "",
    destination_name: "",
    destination_place_id: "",
    start_date: "",
    end_date: "",
    route_preference: "FEWER_TRANSFERS",
  });

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    const name = form.name.trim();
    const destinationName = form.destination_name.trim();
    if (!name) {
      setError("請輸入旅程名稱。");
      return;
    }
    if (!destinationName) {
      setError("請輸入目的地。");
      return;
    }
    if (!form.start_date || !form.end_date) {
      setError("請選擇開始與結束日期。");
      return;
    }
    if (form.end_date < form.start_date) {
      setError("結束日期不可早於開始日期。");
      return;
    }
    setBusy(true);
    try {
      const trip = await api<CreatedTrip>("/trips", {
        method: "POST",
        body: JSON.stringify({
          source: "blank",
          ...form,
          name,
          destination_name: destinationName,
          destination_place_id: form.destination_place_id || null,
        }),
      });
      router.push(`/trips/${trip.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "建立行程失敗，請稍後再試。");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
      <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
        <div className="mb-7 flex items-start gap-4">
          <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-[var(--teal-soft)] text-[var(--teal)]"><MapPinned size={23} /></span>
          <div><p className="text-sm font-semibold text-[var(--teal)]">建立自己的行程</p><h1 className="mt-1 text-3xl font-bold">先決定去哪裡，再慢慢排滿每一天</h1></div>
        </div>
        <div className="grid gap-5">
          <label className="text-sm font-semibold">旅程名稱<input required maxLength={255} value={form.name} onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))} placeholder="例如：東京五日賞楓" className="mt-2 w-full rounded-xl border border-[var(--line)] px-4 py-3 font-normal outline-none focus:border-[var(--teal)]" /></label>
          <label className="text-sm font-semibold">目的地<div className="mt-2"><PlacePicker value={form.destination_name} confirmed={Boolean(form.destination_place_id)} countryCodes={["jp", "kr", "th"]} onTextChange={(value) => setForm((current) => ({ ...current, destination_name: value, destination_place_id: "" }))} onSelect={(place) => setForm((current) => ({ ...current, destination_name: place.name, destination_place_id: place.place_id }))} /></div><span className="mt-1 block text-xs font-normal text-[var(--muted)]">由 Google Maps 搜尋日本、韓國與泰國城市；未啟用服務時仍可輸入文字建立。</span></label>
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="text-sm font-semibold">開始日期<input required type="date" value={form.start_date} onChange={(event) => setForm((current) => ({ ...current, start_date: event.target.value, end_date: current.end_date && current.end_date < event.target.value ? "" : current.end_date }))} className="mt-2 w-full rounded-xl border border-[var(--line)] px-4 py-3 font-normal outline-none focus:border-[var(--teal)]" /></label>
            <label className="text-sm font-semibold">結束日期<input required type="date" min={form.start_date} value={form.end_date} onChange={(event) => setForm((current) => ({ ...current, end_date: event.target.value }))} className="mt-2 w-full rounded-xl border border-[var(--line)] px-4 py-3 font-normal outline-none focus:border-[var(--teal)]" /></label>
          </div>
          <label className="text-sm font-semibold">大眾運輸偏好<select value={form.route_preference} onChange={(event) => setForm((current) => ({ ...current, route_preference: event.target.value }))} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-4 py-3 font-normal outline-none focus:border-[var(--teal)]"><option value="FEWER_TRANSFERS">少轉乘</option><option value="FASTEST">最快抵達</option><option value="LESS_WALKING">少走路</option></select></label>
        </div>
        {error && <p role="alert" aria-live="polite" className="mt-5 rounded-xl bg-red-50 p-4 text-sm text-red-800">{error}</p>}
        <button type="submit" disabled={busy} className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white disabled:opacity-60">{busy ? "建立中…" : "建立空白行程"}<ArrowRight size={18} /></button>
      </section>
      <aside className="rounded-[2rem] bg-[var(--ink)] p-6 text-white md:p-8">
        <p className="text-xs font-semibold tracking-[.18em] text-emerald-200">接下來可以做什麼</p>
        <div className="mt-6 space-y-5">
          <div className="flex gap-3"><CalendarDays className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h2 className="font-semibold">安排每天的景點</h2><p className="mt-1 text-sm leading-6 text-white/65">新增地點、設定停留時間，拖曳調整順序並鎖定預約。</p></div></div>
          <div className="flex gap-3"><Route className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h2 className="font-semibold">看懂每一段怎麼走</h2><p className="mt-1 text-sm leading-6 text-white/65">查看步行、搭車、轉乘方向；日本路線在來源有資料時顯示月台與出口。</p></div></div>
        </div>
        <p className="mt-8 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-white/75">手動編排行程與查路免費；只有成功套用整日自動最佳化才扣 1 次。</p>
      </aside>
    </form>
  );
}
