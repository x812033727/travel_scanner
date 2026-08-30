"use client";

import { CalendarDays, Hotel, PlaneTakeoff, SlidersHorizontal, Users } from "lucide-react";
import { useRouter } from "next/navigation";
import type { FormEvent } from "react";

const fieldClass =
  "mt-2 w-full rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3.5 text-[var(--ink)] outline-none transition focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

export function SearchWorkbench() {
  const router = useRouter();

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const origin = String(data.get("origin") || "TPE").trim().toUpperCase();
    const destination = String(data.get("destination") || "NRT").trim().toUpperCase();
    const departure = String(data.get("departure") || "");
    const returning = String(data.get("returning") || "");
    const adults = String(data.get("adults") || "1");
    const rooms = String(data.get("rooms") || "1");
    const budget = String(data.get("budget") || "");
    const interests = String(data.get("interests") || "美食、文化").trim();
    const description = `${adults} 位成人從 ${origin} 前往 ${destination}，${departure} 出發、${returning} 回程，${rooms} 間房${budget ? `，總預算 ${budget} 元` : ""}，偏好 ${interests}。`;
    const query = new URLSearchParams({
      q: description,
      origin,
      destination,
      departure_date: departure,
      return_date: returning,
      adults,
      rooms,
      interests,
    });
    if (budget) query.set("budget_twd", budget);
    router.push(`/search?${query.toString()}`);
  }

  return (
    <form onSubmit={submit} className="rounded-[2rem] border border-[var(--line)] bg-white p-5 shadow-[var(--shadow-lg)] md:p-7">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-[var(--teal)]">完整旅程搜尋</p>
          <h2 className="mt-1 text-2xl font-bold">從交通到住宿，一次排好</h2>
        </div>
        <span className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-xs font-semibold text-[var(--teal-dark)]">即時來源準備中</span>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <label className="text-sm font-semibold">
          出發機場
          <span className="relative block">
            <PlaneTakeoff className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <input className={`${fieldClass} pl-11`} name="origin" defaultValue="TPE" maxLength={3} aria-label="出發機場代碼" />
          </span>
        </label>
        <label className="text-sm font-semibold">
          目的地
          <span className="relative block">
            <Hotel className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <input className={`${fieldClass} pl-11`} name="destination" defaultValue="NRT" maxLength={3} aria-label="目的地機場代碼" />
          </span>
        </label>
        <label className="text-sm font-semibold">
          出發日期
          <span className="relative block">
            <CalendarDays className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <input className={`${fieldClass} pl-11`} name="departure" type="date" defaultValue="2026-11-10" />
          </span>
        </label>
        <label className="text-sm font-semibold">
          回程日期
          <span className="relative block">
            <CalendarDays className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <input className={`${fieldClass} pl-11`} name="returning" type="date" defaultValue="2026-11-15" />
          </span>
        </label>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4 md:grid-cols-4">
        <label className="text-sm font-semibold">
          <span className="flex items-center gap-2"><Users size={16} />成人</span>
          <select className={fieldClass} name="adults" defaultValue="2">
            {[1, 2, 3, 4, 5, 6].map((value) => <option key={value}>{value}</option>)}
          </select>
        </label>
        <label className="text-sm font-semibold">
          <span className="flex items-center gap-2"><Hotel size={16} />房間</span>
          <select className={fieldClass} name="rooms" defaultValue="1">
            {[1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}
          </select>
        </label>
        <label className="col-span-2 text-sm font-semibold">
          預算（TWD）
          <input className={fieldClass} name="budget" inputMode="numeric" defaultValue="60000" />
        </label>
      </div>

      <label className="mt-4 block text-sm font-semibold">
        <span className="flex items-center gap-2"><SlidersHorizontal size={16} />旅行偏好</span>
        <input className={fieldClass} name="interests" defaultValue="美食、購物、文化，不要紅眼航班，住宿至少四星" />
      </label>

      <button className="mt-5 flex w-full items-center justify-center gap-2 rounded-2xl bg-[var(--teal)] px-6 py-4 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-[var(--teal-dark)] focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[var(--teal-soft)]">
        <PlaneTakeoff size={19} />比較完整旅程
      </button>
      <p className="mt-4 text-center text-xs leading-5 text-[var(--muted)]">正式環境只顯示已標明來源與擷取時間的報價；預訂前會再次提醒確認價格與庫存。</p>
    </form>
  );
}
