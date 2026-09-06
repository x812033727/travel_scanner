"use client";

import { CalendarRange, LoaderCircle } from "lucide-react";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { twd } from "@/lib/api";

export type FlightDateOption = {
  shift_days: number;
  departure_date: string;
  return_date?: string | null;
  lowest_price: string | number;
  currency: string;
  provider: string;
  source_mode: "live" | "test" | "mock" | "estimate";
  is_current: boolean;
  offer_count: number;
};

function compactDate(value: string) {
  const [, month, day] = value.split("-");
  return `${Number(month)}/${Number(day)}`;
}

export function FlightDateOptions({
  options,
  selected,
  busy,
  onSelect,
  onApply,
}: {
  options: FlightDateOption[];
  selected?: FlightDateOption;
  busy?: boolean;
  onSelect: (option: FlightDateOption) => void;
  onApply: (option: FlightDateOption) => void;
}) {
  const charge = useOperationCharge("full_trip_search");
  if (!options.length) return null;
  return (
    <section aria-labelledby="flexible-dates-title" className="mb-5 rounded-2xl border border-[var(--line)] bg-white p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 id="flexible-dates-title" className="flex items-center gap-2 font-bold"><CalendarRange size={18} className="text-[var(--teal)]" />彈性日期價格</h2>
          <p className="mt-1 text-xs text-[var(--muted)]">目前日期顯示即時最低價；其他日期為供應商估價，選定後需重新搜尋整趟。</p>
        </div>
        <span className="text-xs text-[var(--muted)]">切換估價不扣次</span>
      </div>
      <div className="mt-4 flex gap-2 overflow-x-auto pb-2" role="list" aria-label="可選日期價格">
        {options.map((option) => {
          const active = selected ? selected.shift_days === option.shift_days : option.is_current;
          return <button key={`${option.departure_date}:${option.return_date || "one-way"}`} type="button" aria-pressed={active} onClick={() => onSelect(option)} className={`min-w-[138px] rounded-xl border px-3 py-3 text-left transition ${active ? "border-[var(--teal)] bg-[var(--teal-soft)]" : "border-[var(--line)] bg-[var(--paper)] hover:border-[var(--teal)]"}`}>
            <span className="block text-xs font-semibold text-[var(--teal-dark)]">{option.is_current ? "目前日期" : option.shift_days > 0 ? `晚 ${option.shift_days} 日` : `早 ${Math.abs(option.shift_days)} 日`}</span>
            <span className="mt-1 block text-sm font-bold">{compactDate(option.departure_date)}{option.return_date ? ` → ${compactDate(option.return_date)}` : ""}</span>
            <span className="mt-1 block text-sm">{twd.format(Number(option.lowest_price))}</span>
            <span className="mt-1 block text-xs text-[var(--muted)]">{option.is_current ? "即時結果" : "估計最低價"}</span>
          </button>;
        })}
      </div>
      {selected && !selected.is_current && <div className="mt-3 flex flex-col gap-3 rounded-xl bg-[var(--paper)] p-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm"><strong>{compactDate(selected.departure_date)}{selected.return_date ? ` → ${compactDate(selected.return_date)}` : ""}</strong><span className="ml-2 text-[var(--muted)]">確認後會更新機票、住宿、活動與接送；{charge.status === "ready" ? charge.label : charge.unavailableHelp}。</span></p>
        <button type="button" disabled={busy || charge.status !== "ready"} onClick={() => onApply(selected)} className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50">{busy && <LoaderCircle size={16} className="animate-spin" />}套用並重新搜尋整趟 · {charge.label}</button>
      </div>}
    </section>
  );
}
