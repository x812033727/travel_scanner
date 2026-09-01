"use client";

import { AlertCircle, ExternalLink, LoaderCircle, Search } from "lucide-react";
import { FormEvent, useState } from "react";
import { useLocale } from "next-intl";
import { api, isUsageInsufficient, twd } from "@/lib/api";
import { useRouter } from "@/i18n/navigation";

type FlightOffer = {
  id: string;
  airline: string;
  marketing_airline?: string;
  selling_agent?: string;
  origin: string;
  destination: string;
  total_price: string | number;
  currency: string;
  clickout_available?: boolean;
};

type Strategy = {
  components: Array<{ role: string; offer: FlightOffer }>;
  total_price: string | number;
  currency: string;
};

type Comparison = {
  mode: "mixed_airlines" | "same_airline";
  conventional?: Strategy | null;
  back_to_back?: Strategy | null;
  savings?: string | number | null;
  verdict: string;
  detail: string;
};

type Response = {
  provider: string;
  comparisons: Comparison[];
  warnings: string[];
  usage?: { status: string };
};

const destinations = [
  ["NRT", "東京成田"],
  ["KIX", "大阪關西"],
  ["FUK", "福岡"],
  ["ICN", "首爾仁川"],
  ["BKK", "曼谷"],
];

const roleLabels: Record<string, string> = {
  conventional_first: "第一趟一般來回",
  conventional_second: "第二趟一般來回",
  head_one_way: "頭段單程",
  middle_two_segment: "外站始發兩段票",
  tail_one_way: "尾段單程",
};

function money(value: string | number, currency: string) {
  return currency === "TWD" ? twd.format(Number(value)) : `${currency} ${value}`;
}

function StrategyCard({ strategy, title }: { strategy?: Strategy | null; title: string }) {
  return (
    <section className="rounded-2xl border border-[var(--line)] bg-[#fbfcf9] p-4">
      <div className="flex items-center justify-between gap-3">
        <h4 className="font-bold">{title}</h4>
        {strategy && <strong>{money(strategy.total_price, strategy.currency)}</strong>}
      </div>
      {!strategy ? (
        <p className="mt-3 text-sm text-[var(--muted)]">必要票價不足，不建立方案。</p>
      ) : (
        <div className="mt-3 space-y-2">
          {strategy.components.map(({ role, offer }) => (
            <div key={role} className="rounded-xl bg-white p-3 text-sm">
              <div className="flex justify-between gap-3">
                <span><strong>{roleLabels[role]}</strong> · {offer.marketing_airline || offer.airline}</span>
                <span>{money(offer.total_price, offer.currency)}</span>
              </div>
              <p className="mt-1 text-xs text-[var(--muted)]">
                {offer.origin} → {offer.destination}{offer.selling_agent ? ` · ${offer.selling_agent}` : ""}
              </p>
              {offer.clickout_available && (
                <form action={`/api/travel/offers/${offer.id}/clickout`} method="post" target="_blank" className="mt-2">
                  <button type="submit" className="flex items-center gap-1 font-semibold text-[var(--teal)]">
                    前往訂票 <ExternalLink size={13} />
                  </button>
                </form>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export function LiveBackToBackSearch() {
  const locale = useLocale();
  const router = useRouter();
  const [firstDestination, setFirstDestination] = useState("NRT");
  const [secondDestination, setSecondDestination] = useState("KIX");
  const [dates, setDates] = useState(["2026-11-10", "2026-11-15", "2027-03-10", "2027-03-15"]);
  const [adults, setAdults] = useState("1");
  const [cabinClass, setCabinClass] = useState("economy");
  const [result, setResult] = useState<Response>();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    if (!dates.every((value, index) => index === 0 || dates[index - 1] < value)) {
      setError("日期必須依序為第一次出發、第一次回程、第二次出發、第二次回程。");
      return;
    }
    setBusy(true);
    try {
      setResult(await api<Response>("/flights/back-to-back", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          origin: "TPE",
          first_destination: firstDestination,
          second_destination: secondDestination,
          first_trip: { departure_date: dates[0], return_date: dates[1] },
          second_trip: { departure_date: dates[2], return_date: dates[3] },
          travelers: { adults: Number(adults), children: 0, rooms: 1 },
          cabin_class: cabinClass,
          currency: "TWD",
          locale,
        }),
      }));
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        router.push("/pricing");
        return;
      }
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="grid gap-6 lg:grid-cols-[.82fr_1.18fr]">
      <form onSubmit={submit} className="self-start rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7">
        <p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Live provider</p>
        <h2 className="mt-1 text-2xl font-bold">即時倒買價格比較</h2>
        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">一次查兩張一般來回與頭、中、尾三張倒買票；缺票時不估造。</p>
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          {[firstDestination, secondDestination].map((value, index) => (
            <label key={index} className="text-sm font-semibold">第 {index + 1} 次目的地
              <select aria-label={`第 ${index + 1} 次目的地`} value={value} onChange={(event) => index ? setSecondDestination(event.target.value) : setFirstDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3">
                {destinations.map(([code, label]) => <option key={code} value={code}>{label} {code}</option>)}
              </select>
            </label>
          ))}
          {["第一次出發", "第一次回程", "第二次出發", "第二次回程"].map((label, index) => (
            <label key={label} className="text-sm font-semibold">{label}
              <input aria-label={label} type="date" value={dates[index]} onChange={(event) => setDates((current) => current.map((item, position) => position === index ? event.target.value : item))} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3" />
            </label>
          ))}
          <label className="text-sm font-semibold">成人
            <select aria-label="成人" value={adults} onChange={(event) => setAdults(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3">{[1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}</select>
          </label>
          <label className="text-sm font-semibold">艙等
            <select aria-label="即時艙等" value={cabinClass} onChange={(event) => setCabinClass(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3"><option value="economy">經濟艙</option><option value="premium_economy">豪華經濟艙</option><option value="business">商務艙</option><option value="first">頭等艙</option></select>
          </label>
        </div>
        <button disabled={busy} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white disabled:opacity-50">
          {busy ? <><LoaderCircle className="animate-spin" size={18} />查詢五組票價</> : <><Search size={18} />開始即時比較</>}
        </button>
      </form>
      <div aria-live="polite" className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7">
        <h2 className="text-2xl font-bold">比較結果</h2>
        {error && <p role="alert" className="mt-4 flex gap-2 rounded-xl bg-red-50 p-4 text-red-800"><AlertCircle size={18} />{error}</p>}
        {!result && !error && <p className="mt-8 text-center text-[var(--muted)]">設定兩趟旅行後開始查詢。</p>}
        {result?.provider === "skyscanner" && <p className="mt-2 text-xs text-[var(--muted)]">Powered by <a className="underline" href="https://www.skyscanner.net">Skyscanner</a></p>}
        {result?.warnings.map((warning) => <p key={warning} className="mt-3 rounded-xl bg-amber-50 p-3 text-sm text-amber-900">{warning}</p>)}
        <div className="mt-5 space-y-5">{result?.comparisons.map((comparison) => (
          <article key={comparison.mode} className="rounded-2xl border border-[var(--line)] p-4">
            <div className="flex justify-between gap-3"><h3 className="text-lg font-bold">{comparison.mode === "mixed_airlines" ? "最低混搭" : "最低同航空公司"}</h3>{comparison.savings != null && <strong>{Number(comparison.savings) > 0 ? `倒買省 ${twd.format(Number(comparison.savings))}` : `一般省 ${twd.format(Math.abs(Number(comparison.savings)))}`}</strong>}</div>
            <p className="mt-1 text-sm text-[var(--muted)]">{comparison.detail}</p>
            <div className="mt-4 grid gap-3 xl:grid-cols-2"><StrategyCard title="兩張一般來回" strategy={comparison.conventional} /><StrategyCard title="頭段＋外站兩段＋尾段" strategy={comparison.back_to_back} /></div>
          </article>
        ))}</div>
      </div>
    </section>
  );
}
