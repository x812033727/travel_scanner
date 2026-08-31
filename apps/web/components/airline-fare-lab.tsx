"use client";

import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  CircleDot,
  ExternalLink,
  Info,
  LoaderCircle,
  Plane,
  Radar,
  Search,
  ShieldCheck,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { BackToBackFareSearch } from "@/components/back-to-back-fare-search";
import { LiveBackToBackSearch } from "@/components/live-back-to-back-search";
import { api, isUsageInsufficient, twd } from "@/lib/api";

type AirlineCode = "CI" | "BR" | "JX";
type SourceState = "ready" | "success" | "disabled" | "blocked" | "failed";
type UsageStatus = { status: "reserved" | "charged" | "released"; uses: number; reference: string };

type CrawlerSource = {
  airline_code: AirlineCode;
  airline_name: string;
  host: string;
  state: SourceState;
  policy: string;
  detail: string;
  quote_count: number;
  cache_hit: boolean;
};

type CrawlerStatus = {
  sources: CrawlerSource[];
  safety_rules: string[];
};

type FareQuote = {
  id: string;
  airline_code: AirlineCode;
  airline_name: string;
  origin: string;
  destination: string;
  departure_date: string;
  return_date?: string;
  trip_type: string;
  cabin_class: string;
  total_price: string | number;
  currency: string;
  price_last_seen?: string;
  source_url: string;
  is_live: boolean;
  is_bookable: boolean;
  disclaimer: string;
};

type FareSearchResponse = {
  queried_at: string;
  quotes: FareQuote[];
  sources: CrawlerSource[];
  warnings: string[];
  usage?: UsageStatus;
};

const airlines: Array<{ code: AirlineCode; name: string; short: string }> = [
  { code: "CI", name: "中華航空", short: "華航" },
  { code: "BR", name: "長榮航空", short: "長榮" },
  { code: "JX", name: "星宇航空", short: "星宇" },
];

const destinations = [
  { code: "NRT", city: "東京成田" },
  { code: "KIX", city: "大阪關西" },
  { code: "FUK", city: "福岡" },
  { code: "CTS", city: "札幌新千歲" },
  { code: "ICN", city: "首爾仁川" },
  { code: "BKK", city: "曼谷" },
  { code: "SIN", city: "新加坡" },
];

const stateCopy: Record<SourceState, { label: string; className: string }> = {
  ready: { label: "可查詢", className: "bg-emerald-50 text-emerald-800" },
  success: { label: "已取得", className: "bg-emerald-50 text-emerald-800" },
  disabled: { label: "政策停用", className: "bg-amber-50 text-amber-800" },
  blocked: { label: "來源阻擋", className: "bg-amber-50 text-amber-800" },
  failed: { label: "暫時失敗", className: "bg-red-50 text-red-800" },
};

function formatDate(value?: string) {
  if (!value) return "—";
  return new Intl.DateTimeFormat("zh-TW", {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${value}T00:00:00Z`));
}

function sourceFor(code: AirlineCode, sources: CrawlerSource[]) {
  return sources.find((source) => source.airline_code === code);
}

export function AirlineFareLab() {
  const router = useRouter();
  const [mode, setMode] = useState<"conventional" | "back_to_back" | "live_back_to_back">("conventional");
  const [status, setStatus] = useState<CrawlerStatus>();
  const [result, setResult] = useState<FareSearchResponse>();
  const [selected, setSelected] = useState<Record<AirlineCode, boolean>>({
    CI: true,
    BR: true,
    JX: true,
  });
  const [origin, setOrigin] = useState("TPE");
  const [destination, setDestination] = useState("NRT");
  const [departureDate, setDepartureDate] = useState("2026-11-10");
  const [returnDate, setReturnDate] = useState("2026-11-15");
  const [flexDays, setFlexDays] = useState("7");
  const [cabinClass, setCabinClass] = useState("economy");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  useEffect(() => {
    api<CrawlerStatus>("/crawlers/airlines/status")
      .then(setStatus)
      .catch((reason: Error) => setError(reason.message));
  }, []);

  const selectedAirlines = useMemo(
    () => airlines.filter(({ code }) => selected[code]).map(({ code }) => code),
    [selected],
  );

  async function searchFares(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    if (returnDate && departureDate && returnDate < departureDate) {
      setError("回程日期不能早於出發日期。");
      return;
    }
    if (!selectedAirlines.length) {
      setError("請至少選擇一家航空公司。");
      return;
    }
    setBusy(true);
    try {
      const response = await api<FareSearchResponse>("/crawlers/airlines/fares", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          origin,
          destination,
          departure_date: departureDate || null,
          return_date: returnDate || null,
          flex_days: Number(flexDays),
          cabin_class: cabinClass,
          airlines: selectedAirlines,
          limit_per_airline: 10,
        }),
      });
      setResult(response);
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

  const activeSources = result?.sources || status?.sources || [];
  const needsLogin = error?.toLowerCase().includes("sign in") || error?.includes("登入");

  return (
    <main className="mx-auto max-w-6xl px-5 pb-24 md:px-8">
      <section className="mb-8 grid gap-6 pt-8 lg:grid-cols-[1.25fr_.75fr] lg:items-end">
        <div>
          <p className="mb-3 flex items-center gap-2 text-sm font-semibold text-[var(--coral)]">
            <Radar size={17} /> PUBLIC FARE LAB
          </p>
          <h1 className="max-w-3xl text-4xl font-bold tracking-[-.035em] md:text-6xl">
            三家航空，先看公開票價訊號。
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-[var(--muted)] md:text-lg">
            查詢華航、長榮與星宇公開頁面的近期快取票價。這裡適合找方向，不代表即時庫存，也不能直接訂位。
          </p>
        </div>
        <aside className="rounded-3xl border border-[var(--line)] bg-[#edf5f1] p-5 text-sm leading-6 text-[var(--teal-dark)]">
          <p className="flex items-center gap-2 font-semibold"><ShieldCheck size={18} />安全讀取模式</p>
          <p className="mt-2">固定官方網域、遵守 robots、限制頻率，不登入航空公司帳號，也不接觸私人訂位庫存。</p>
        </aside>
      </section>

      <section aria-label="航空來源狀態" className="mb-6 grid gap-3 sm:grid-cols-3">
        {airlines.map((airline) => {
          const source = sourceFor(airline.code, activeSources);
          const state = source ? stateCopy[source.state] : undefined;
          return (
            <article key={airline.code} className="rounded-2xl border border-[var(--line)] bg-white p-4 shadow-[0_10px_35px_rgba(16,42,43,.05)]">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] font-mono text-sm font-bold text-white">{airline.code}</span>
                  <div><strong className="block">{airline.name}</strong><span className="text-xs text-[var(--muted)]">{source?.host || "檢查來源中"}</span></div>
                </div>
                <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${state?.className || "bg-slate-100 text-slate-600"}`}>
                  {state?.label || "檢查中"}
                </span>
              </div>
            </article>
          );
        })}
      </section>

      <div role="tablist" aria-label="票價搜尋模式" className="mb-6 grid max-w-2xl grid-cols-3 rounded-2xl border border-[var(--line)] bg-white p-1.5">
        <button role="tab" aria-selected={mode === "conventional"} onClick={() => setMode("conventional")} className={`rounded-xl px-4 py-2.5 text-sm font-semibold transition ${mode === "conventional" ? "bg-[var(--ink)] text-white" : "text-[var(--muted)]"}`}>一般來回</button>
        <button role="tab" aria-selected={mode === "back_to_back"} onClick={() => setMode("back_to_back")} className={`rounded-xl px-4 py-2.5 text-sm font-semibold transition ${mode === "back_to_back" ? "bg-[var(--ink)] text-white" : "text-[var(--muted)]"}`}>倒買法</button>
        <button role="tab" aria-selected={mode === "live_back_to_back"} onClick={() => setMode("live_back_to_back")} className={`rounded-xl px-4 py-2.5 text-sm font-semibold transition ${mode === "live_back_to_back" ? "bg-[var(--ink)] text-white" : "text-[var(--muted)]"}`}>即時倒買 API</button>
      </div>

      {mode === "live_back_to_back" ? <LiveBackToBackSearch /> : mode === "back_to_back" ? <BackToBackFareSearch /> : <section className="grid gap-6 lg:grid-cols-[.82fr_1.18fr]">
        <form onSubmit={searchFares} className="self-start rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-[0_22px_70px_rgba(16,42,43,.08)] md:p-7">
          <div className="mb-6 flex items-center justify-between">
            <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Search controls</p><h2 className="mt-1 text-2xl font-bold">設定航線</h2></div>
            <Plane className="text-[var(--teal)]" size={25} />
          </div>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold">航空公司</legend>
            <div className="grid grid-cols-3 gap-2">
              {airlines.map((airline) => (
                <label key={airline.code} className={`cursor-pointer rounded-xl border px-3 py-3 text-center text-sm transition ${selected[airline.code] ? "border-[var(--teal)] bg-[#edf5f1] text-[var(--teal-dark)]" : "border-[var(--line)] text-[var(--muted)]"}`}>
                  <input
                    className="sr-only"
                    type="checkbox"
                    checked={selected[airline.code]}
                    onChange={(event) => setSelected((current) => ({ ...current, [airline.code]: event.target.checked }))}
                  />
                  <span className="font-semibold">{airline.short}</span><span className="ml-1 font-mono text-xs">{airline.code}</span>
                </label>
              ))}
            </div>
          </fieldset>

          <div className="mt-5 grid grid-cols-[1fr_auto_1fr] items-end gap-2">
            <label className="text-sm font-semibold">出發地<select aria-label="出發地" value={origin} onChange={(event) => setOrigin(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><option value="TPE">台北 TPE</option><option value="TSA">台北松山 TSA</option></select></label>
            <ArrowRight className="mb-3 text-[var(--muted)]" size={18} />
            <label className="text-sm font-semibold">目的地<select aria-label="目的地" value={destination} onChange={(event) => setDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{destinations.map((item) => <option value={item.code} key={item.code}>{item.city} {item.code}</option>)}</select></label>
          </div>

          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <label className="text-sm font-semibold">出發日期<input aria-label="出發日期" type="date" value={departureDate} onChange={(event) => setDepartureDate(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">回程日期<input aria-label="回程日期" type="date" value={returnDate} onChange={(event) => setReturnDate(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">彈性日期<select aria-label="彈性日期" value={flexDays} onChange={(event) => setFlexDays(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><option value="0">指定日期</option><option value="3">前後 3 天</option><option value="7">前後 7 天</option><option value="14">前後 14 天</option></select></label>
            <label className="text-sm font-semibold">艙等<select aria-label="艙等" value={cabinClass} onChange={(event) => setCabinClass(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><option value="economy">經濟艙</option><option value="premium_economy">豪華經濟艙</option><option value="business">商務艙</option><option value="first">頭等艙</option></select></label>
          </div>

          <button disabled={busy || !selectedAirlines.length} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white transition hover:bg-[var(--teal-dark)] disabled:cursor-not-allowed disabled:opacity-50">
            {busy ? <><LoaderCircle className="animate-spin" size={18} />正在讀取官方公開頁面</> : <><Search size={18} />搜尋公開票價</>}
          </button>
          <p className="mt-3 text-center text-xs text-[var(--muted)]">需要登入 Travel Scanner；成功取得公開票價才扣 1 次，失敗不扣。</p>
        </form>

        <div aria-live="polite" className="min-h-[34rem] rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7">
          <div className="flex flex-wrap items-start justify-between gap-3 border-b border-[var(--line)] pb-5">
            <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--coral)]">Public fare signals</p><h2 className="mt-1 text-2xl font-bold">票價結果</h2></div>
            {result && <span className="rounded-full bg-[#edf5f1] px-3 py-1.5 text-sm font-semibold text-[var(--teal-dark)]">{result.quotes.length} 筆近期票價</span>}
          </div>

          {error && <div role="alert" className="mt-5 flex items-start gap-3 rounded-2xl bg-red-50 p-4 text-sm leading-6 text-red-800"><AlertCircle className="mt-0.5 shrink-0" size={19} /><div><strong className="block">目前無法完成查詢</strong>{error}{needsLogin && <Link href="/login" className="ml-1 font-semibold underline">前往登入</Link>}</div></div>}

          {!result && !busy && !error && <div className="grid min-h-[25rem] place-items-center text-center"><div className="max-w-sm"><span className="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-[#edf5f1] text-[var(--teal)]"><CircleDot size={28} /></span><h3 className="mt-5 text-xl font-bold">先設定想看的航線</h3><p className="mt-2 leading-7 text-[var(--muted)]">結果會保留航空公司、日期、公開價格、來源更新時間與原始頁面，不補造班號或即時庫存。</p></div></div>}

          {busy && <div className="grid min-h-[25rem] place-items-center text-center"><div><LoaderCircle className="mx-auto animate-spin text-[var(--teal)]" size={36} /><p className="mt-4 font-semibold">逐家確認來源政策與票價頁…</p></div></div>}

          {result && !busy && <div className="mt-5 space-y-4">
            {result.usage && <p className={`rounded-xl p-3 text-sm font-semibold ${result.usage.status === "charged" ? "bg-[#fff4ef] text-[#7e4439]" : "bg-emerald-50 text-emerald-800"}`}>{result.usage.status === "charged" ? "本次已扣除 1 次" : "未取得可用票價，本次未扣次"}</p>}
            {result.warnings.map((warning) => <div key={warning} className="flex gap-2 rounded-xl bg-amber-50 p-3 text-sm text-amber-900"><Info className="mt-0.5 shrink-0" size={17} />{warning}</div>)}
            {result.quotes.length === 0 ? <div className="grid min-h-64 place-items-center text-center text-[var(--muted)]"><div><Search className="mx-auto mb-3" size={28} /><p>指定日期附近沒有公開快取票價。</p></div></div> : result.quotes.map((quote) => (
              <article key={quote.id} className="rounded-2xl border border-[var(--line)] p-4 transition hover:border-[#b7cbc0] md:p-5">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div className="flex items-start gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] font-mono text-sm font-bold text-white">{quote.airline_code}</span><div><h3 className="font-bold">{quote.airline_name}</h3><p className="mt-1 flex items-center gap-2 text-sm text-[var(--muted)]">{quote.origin}<ArrowRight size={14} />{quote.destination}</p></div></div>
                  <div className="text-right"><p className="text-2xl font-bold">{quote.currency === "TWD" ? twd.format(Number(quote.total_price)) : `${quote.currency} ${quote.total_price}`}</p><p className="text-xs text-[var(--muted)]">每位旅客 · 公開快取</p></div>
                </div>
                <div className="mt-4 grid gap-2 rounded-xl bg-[#f7f9f5] p-3 text-sm sm:grid-cols-2"><p><span className="text-[var(--muted)]">去程</span><strong className="ml-2">{formatDate(quote.departure_date)}</strong></p><p><span className="text-[var(--muted)]">回程</span><strong className="ml-2">{formatDate(quote.return_date)}</strong></p></div>
                <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-[var(--muted)]"><span className="flex items-center gap-1.5"><CheckCircle2 size={15} className="text-[var(--teal)]" />非即時 · 不可直接訂位{quote.price_last_seen ? ` · ${quote.price_last_seen}` : ""}</span><a href={quote.source_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 font-semibold text-[var(--teal)]">查看官方來源<ExternalLink size={14} /></a></div>
              </article>
            ))}
          </div>}
        </div>
      </section>}
    </main>
  );
}
