"use client";

import {
  AlertCircle,
  ArrowRight,
  CalendarRange,
  Info,
  LoaderCircle,
  Plane,
  ShieldAlert,
  Shuffle,
} from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { FormEvent, useMemo, useState } from "react";
import { api, isUsageInsufficient, twd } from "@/lib/api";

type AirlineCode = "CI" | "BR" | "JX";
type FareTicketRole = "conventional_first" | "conventional_second" | "wrapper" | "reverse";
type ComparisonMode = "mixed_airlines" | "same_airline";
type ComparisonVerdict =
  | "back_to_back_cheaper"
  | "conventional_cheaper"
  | "same_price"
  | "comparison_unavailable";
type BackToBackPricingCapability = "full_back_to_back" | "open_jaw_provider_required";
type BackToBackStrategy = "nested_round_trips" | "reverse_two_segment";
type SupplementalFareRole =
  | "conventional_first_manual"
  | "conventional_second_manual"
  | "head_one_way"
  | "middle_two_segment"
  | "tail_one_way";
type UsageStatus = { status: "reserved" | "charged" | "released"; uses: number; reference: string };

type FareQuote = {
  id: string;
  airline_code: AirlineCode;
  airline_name: string;
  origin: string;
  destination: string;
  departure_date: string;
  return_date?: string;
  total_price: string | number;
  currency: string;
  source_url: string;
};

type FxRateSnapshot = {
  base_currency: string;
  quote_currency: string;
  rate: string | number;
  as_of: string;
  source_url: string;
  is_stale: boolean;
};

type FareTicketComponent = {
  role: FareTicketRole;
  quote: FareQuote;
  estimated_twd?: string | number;
  fx_rate?: FxRateSnapshot;
};

type FareStrategyTotal = {
  tickets: FareTicketComponent[];
  supplemental_fares?: SupplementalFareComponent[];
  original_currency_totals: Record<string, string | number>;
  estimated_twd?: string | number;
};

type SupplementalFareComponent = {
  role: SupplementalFareRole;
  origin: string;
  destination: string;
  departure_date: string;
  amount: string | number;
  currency: string;
  airline_code?: AirlineCode;
  segments?: Array<{ origin: string; destination: string; departure_date: string }>;
  estimated_twd?: string | number;
  source: "manual";
  is_live: false;
};

type BackToBackComparison = {
  mode: ComparisonMode;
  conventional?: FareStrategyTotal;
  back_to_back?: FareStrategyTotal;
  savings_twd?: string | number | null;
  savings_percent?: string | number | null;
  verdict: ComparisonVerdict;
  detail: string;
};

type BackToBackResponse = {
  queried_at: string;
  query?: {
    strategy?: BackToBackStrategy;
    first_destination?: string;
    second_destination?: string;
  };
  pricing_capability: BackToBackPricingCapability;
  comparisons: BackToBackComparison[];
  candidates: Array<{ role: FareTicketRole; quotes: FareQuote[] }>;
  fx_rates: FxRateSnapshot[];
  warnings: string[];
  usage?: UsageStatus;
};

const airlines: Array<{ code: AirlineCode; short: string }> = [
  { code: "CI", short: "華航" },
  { code: "BR", short: "長榮" },
  { code: "JX", short: "星宇" },
];

const destinationGroups = [
  {
    country: "日本",
    cities: [
      { code: "TYO", city: "東京（成田／羽田）" },
      { code: "OSA", city: "大阪（關西／伊丹）" },
      { code: "FUK", city: "福岡" },
      { code: "CTS", city: "札幌新千歲" },
    ],
  },
  { country: "韓國", cities: [{ code: "SEL", city: "首爾（仁川／金浦）" }] },
  { country: "泰國", cities: [{ code: "BKK", city: "曼谷" }] },
  { country: "新加坡", cities: [{ code: "SIN", city: "新加坡" }] },
];

const roleLabels: Record<FareTicketRole, string> = {
  conventional_first: "第一趟一般票",
  conventional_second: "第二趟一般票",
  wrapper: "台灣始發包覆票",
  reverse: "外站始發倒買票",
};

const supplementalRoleLabels: Record<SupplementalFareRole, string> = {
  conventional_first_manual: "第一趟一般來回票",
  conventional_second_manual: "第二趟一般來回票",
  head_one_way: "頭段單程票",
  middle_two_segment: "中段反向兩航段票",
  tail_one_way: "尾段單程票",
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

function formatMoney(value: string | number, currency: string) {
  return new Intl.NumberFormat("zh-TW", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(Number(value));
}

function dateFromToday(days: number) {
  const now = new Date();
  const date = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + days));
  return date.toISOString().slice(0, 10);
}

function DestinationOptions() {
  return destinationGroups.map((group) => (
    <optgroup key={group.country} label={group.country}>
      {group.cities.map((item) => (
        <option value={item.code} key={item.code}>{item.city} {item.code}</option>
      ))}
    </optgroup>
  ));
}

function StrategySummary({
  title,
  strategy,
  emptyCopy = "缺少完整票價或換算匯率",
}: {
  title: string;
  strategy?: FareStrategyTotal;
  emptyCopy?: string;
}) {
  if (!strategy || strategy.estimated_twd === undefined) {
    return (
      <div className="rounded-2xl bg-[#f7f9f5] p-4">
        <p className="text-sm font-semibold">{title}</p>
        <p className="mt-2 text-sm text-[var(--muted)]">{emptyCopy}</p>
      </div>
    );
  }
  return (
    <div className="rounded-2xl bg-[#f7f9f5] p-4">
      <p className="text-sm text-[var(--muted)]">{title}</p>
      <p className="mt-1 text-2xl font-bold">{twd.format(Number(strategy.estimated_twd))}</p>
      <p className="mt-1 text-xs text-[var(--muted)]">每位旅客 · TWD 估算</p>
    </div>
  );
}

function TicketTimeline({ tickets }: { tickets: FareTicketComponent[] }) {
  return (
    <div className="mt-5 space-y-3">
      {tickets.map((ticket) => (
        <article key={`${ticket.role}-${ticket.quote.id}`} className="rounded-2xl border border-[var(--line)] p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="text-xs font-semibold text-[var(--coral)]">{roleLabels[ticket.role]}</p>
              <p className="mt-1 font-bold">{ticket.quote.airline_name} · {ticket.quote.airline_code}</p>
            </div>
            <div className="text-right">
              <p className="font-bold">{formatMoney(ticket.quote.total_price, ticket.quote.currency)}</p>
              {ticket.quote.currency !== "TWD" && ticket.estimated_twd !== undefined && (
                <p className="text-xs text-[var(--muted)]">約 {twd.format(Number(ticket.estimated_twd))}</p>
              )}
            </div>
          </div>
          <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-[var(--muted)]">
            <span>{ticket.quote.origin}</span><ArrowRight size={14} /><span>{ticket.quote.destination}</span>
            <span className="mx-1 text-[var(--line)]">|</span>
            <span>{formatDate(ticket.quote.departure_date)}</span><ArrowRight size={14} /><span>{formatDate(ticket.quote.return_date)}</span>
          </div>
        </article>
      ))}
    </div>
  );
}

function SupplementalFareCard({ fare }: { fare: SupplementalFareComponent }) {
  const segments = fare.segments?.length
    ? fare.segments
    : [{ origin: fare.origin, destination: fare.destination, departure_date: fare.departure_date }];
  return (
    <article className="rounded-2xl border border-dashed border-amber-300 bg-amber-50/50 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold text-amber-800">{supplementalRoleLabels[fare.role]} · 手動輸入</p>
          <p className="mt-1 font-bold">{fare.airline_code || "航空公司未指定"}</p>
        </div>
        <div className="text-right">
          <p className="font-bold">{formatMoney(fare.amount, fare.currency)}</p>
          {fare.currency !== "TWD" && fare.estimated_twd !== undefined && (
            <p className="text-xs text-[var(--muted)]">約 {twd.format(Number(fare.estimated_twd))}</p>
          )}
        </div>
      </div>
      <div className="mt-3 space-y-2 text-sm text-[var(--muted)]">
        {segments.map((segment, index) => (
          <div key={`${segment.origin}-${segment.destination}-${segment.departure_date}-${index}`} className="flex flex-wrap items-center gap-2">
            <span>{segment.origin}</span><ArrowRight size={14} /><span>{segment.destination}</span>
            <span className="mx-1 text-[var(--line)]">|</span>
            <span>{formatDate(segment.departure_date)}</span>
          </div>
        ))}
      </div>
    </article>
  );
}

function StrategyTimeline({ strategy }: { strategy: FareStrategyTotal }) {
  const head = strategy.supplemental_fares?.find((fare) => fare.role === "head_one_way");
  const middle = strategy.supplemental_fares?.find((fare) => fare.role === "middle_two_segment");
  const tail = strategy.supplemental_fares?.find((fare) => fare.role === "tail_one_way");
  const conventional = strategy.supplemental_fares?.filter((fare) => fare.role.startsWith("conventional_")) || [];
  return (
    <div className="mt-5 space-y-3">
      {conventional.map((fare) => <SupplementalFareCard key={fare.role} fare={fare} />)}
      {head && <SupplementalFareCard fare={head} />}
      <TicketTimeline tickets={strategy.tickets} />
      {middle && <SupplementalFareCard fare={middle} />}
      {tail && <SupplementalFareCard fare={tail} />}
    </div>
  );
}

function ComparisonCard({
  comparison,
  pricingCapability,
  strategy,
}: {
  comparison: BackToBackComparison;
  pricingCapability: BackToBackPricingCapability;
  strategy: BackToBackStrategy;
}) {
  const mixed = comparison.mode === "mixed_airlines";
  const savings = Number(comparison.savings_twd || 0);
  const alternativeName = strategy === "reverse_two_segment" ? "外站兩段票" : "包覆倒買";
  const savingsCopy = comparison.verdict === "back_to_back_cheaper"
    ? `${alternativeName}估算省下 ${twd.format(savings)}`
    : comparison.verdict === "conventional_cheaper"
      ? `一般買法估算省下 ${twd.format(Math.abs(savings))}`
      : comparison.verdict === "same_price"
        ? "兩種買法估算同價"
        : "目前無法完成價格比較";
  const favorable = comparison.verdict === "back_to_back_cheaper";

  return (
    <article className={`rounded-[1.75rem] border bg-white p-5 md:p-6 ${mixed ? "border-[var(--teal)]" : "border-[var(--line)]"}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[.16em] text-[var(--teal)]">{mixed ? "LOWEST MIX" : "SAME AIRLINE"}</p>
          <h3 className="mt-1 text-xl font-bold">{mixed ? "最低混搭" : "最低同航空公司"}</h3>
        </div>
        <Shuffle className="text-[var(--teal)]" size={22} />
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        <StrategySummary title="兩張一般來回票" strategy={comparison.conventional} />
        <StrategySummary
          title={
            pricingCapability === "open_jaw_provider_required"
              ? "兩張開口倒買票"
              : strategy === "reverse_two_segment"
                ? "外站兩段票＋頭尾單程"
                : "包覆票＋外站倒買票"
          }
          strategy={comparison.back_to_back}
          emptyCopy={pricingCapability === "open_jaw_provider_required" ? "需串接開口票價格來源" : undefined}
        />
      </div>
      <div className={`mt-4 rounded-2xl p-4 text-sm ${favorable ? "bg-emerald-50 text-emerald-900" : "bg-amber-50 text-amber-900"}`}>
        <p className="font-bold">{savingsCopy}{comparison.savings_percent != null ? `（${Math.abs(Number(comparison.savings_percent))}%）` : ""}</p>
        <p className="mt-1 leading-6">{comparison.detail}</p>
      </div>
      {comparison.back_to_back && <StrategyTimeline strategy={comparison.back_to_back} />}
      {!comparison.back_to_back && comparison.conventional && (
        <StrategyTimeline strategy={comparison.conventional} />
      )}
    </article>
  );
}

export function BackToBackFareSearch() {
  const router = useRouter();
  const [selected, setSelected] = useState<Record<AirlineCode, boolean>>({ CI: true, BR: true, JX: true });
  const [strategy, setStrategy] = useState<BackToBackStrategy>("reverse_two_segment");
  const [origin, setOrigin] = useState("TPE");
  const [firstDestination, setFirstDestination] = useState("TYO");
  const [secondDestination, setSecondDestination] = useState("TYO");
  const [firstDeparture, setFirstDeparture] = useState(() => dateFromToday(180));
  const [firstReturn, setFirstReturn] = useState(() => dateFromToday(192));
  const [secondDeparture, setSecondDeparture] = useState(() => dateFromToday(200));
  const [secondReturn, setSecondReturn] = useState(() => dateFromToday(204));
  const [flexDays, setFlexDays] = useState("7");
  const [cabinClass, setCabinClass] = useState("economy");
  const [headOneWayAmount, setHeadOneWayAmount] = useState("");
  const [middleTwoSegmentAmount, setMiddleTwoSegmentAmount] = useState("");
  const [tailOneWayAmount, setTailOneWayAmount] = useState("");
  const [headOneWayCurrency, setHeadOneWayCurrency] = useState("TWD");
  const [middleTwoSegmentCurrency, setMiddleTwoSegmentCurrency] = useState("TWD");
  const [tailOneWayCurrency, setTailOneWayCurrency] = useState("TWD");
  const [headOneWayAirline, setHeadOneWayAirline] = useState<AirlineCode | "">("");
  const [middleTwoSegmentAirline, setMiddleTwoSegmentAirline] = useState<AirlineCode | "">("");
  const [tailOneWayAirline, setTailOneWayAirline] = useState<AirlineCode | "">("");
  const [conventionalFirstAmount, setConventionalFirstAmount] = useState("");
  const [conventionalSecondAmount, setConventionalSecondAmount] = useState("");
  const [conventionalFirstCurrency, setConventionalFirstCurrency] = useState("TWD");
  const [conventionalSecondCurrency, setConventionalSecondCurrency] = useState("TWD");
  const [conventionalFirstAirline, setConventionalFirstAirline] = useState<AirlineCode | "">("");
  const [conventionalSecondAirline, setConventionalSecondAirline] = useState<AirlineCode | "">("");
  const [result, setResult] = useState<BackToBackResponse>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  const selectedAirlines = useMemo(
    () => airlines.filter(({ code }) => selected[code]).map(({ code }) => code),
    [selected],
  );

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    const dates = [firstDeparture, firstReturn, secondDeparture, secondReturn];
    if (dates.some((value) => !value) || !(firstDeparture < firstReturn && firstReturn < secondDeparture && secondDeparture < secondReturn)) {
      setError("日期必須依序為：第一次出發、第一次回程、第二次出發、第二次回程。");
      return;
    }
    if (!selectedAirlines.length) {
      setError("請至少選擇一家航空公司。");
      return;
    }
    setBusy(true);
    try {
      const response = await api<BackToBackResponse>("/crawlers/airlines/back-to-back-fares", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          origin,
          first_destination: firstDestination,
          second_destination: secondDestination,
          first_trip: { departure_date: firstDeparture, return_date: firstReturn },
          second_trip: { departure_date: secondDeparture, return_date: secondReturn },
          flex_days: Number(flexDays),
          cabin_class: cabinClass,
          airlines: selectedAirlines,
          limit_per_airline: 10,
          strategy,
          ...(strategy === "reverse_two_segment" && Number(headOneWayAmount) > 0 ? {
            head_one_way_fare: {
              amount: headOneWayAmount,
              currency: headOneWayCurrency,
              airline_code: headOneWayAirline || null,
            },
          } : {}),
          ...(strategy === "reverse_two_segment" && Number(middleTwoSegmentAmount) > 0 ? {
            middle_two_segment_fare: {
              amount: middleTwoSegmentAmount,
              currency: middleTwoSegmentCurrency,
              airline_code: middleTwoSegmentAirline || null,
            },
          } : {}),
          ...(strategy === "reverse_two_segment" && Number(tailOneWayAmount) > 0 ? {
            tail_one_way_fare: {
              amount: tailOneWayAmount,
              currency: tailOneWayCurrency,
              airline_code: tailOneWayAirline || null,
            },
          } : {}),
          ...(Number(conventionalFirstAmount) > 0 ? {
            conventional_first_fare: {
              amount: conventionalFirstAmount,
              currency: conventionalFirstCurrency,
              airline_code: conventionalFirstAirline || null,
            },
          } : {}),
          ...(Number(conventionalSecondAmount) > 0 ? {
            conventional_second_fare: {
              amount: conventionalSecondAmount,
              currency: conventionalSecondCurrency,
              airline_code: conventionalSecondAirline || null,
            },
          } : {}),
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

  const rawCandidates = result?.candidates.filter((candidate) => candidate.quotes.length) || [];
  const externalRates = result?.fx_rates.filter((rate) => rate.base_currency !== "TWD") || [];

  return (
    <section className="grid gap-6 lg:grid-cols-[.82fr_1.18fr]">
      <form onSubmit={search} className="self-start rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-[0_22px_70px_rgba(16,42,43,.08)] md:p-7">
        <div className="mb-6 flex items-center justify-between">
          <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Back-to-back search</p><h2 className="mt-1 text-2xl font-bold">設定兩趟旅行</h2></div>
          <CalendarRange className="text-[var(--teal)]" size={25} />
        </div>

        <fieldset>
          <legend className="mb-2 text-sm font-semibold">航空公司</legend>
          <div className="grid grid-cols-3 gap-2">
            {airlines.map((airline) => (
              <label key={airline.code} className={`cursor-pointer rounded-xl border px-3 py-3 text-center text-sm transition ${selected[airline.code] ? "border-[var(--teal)] bg-[#edf5f1] text-[var(--teal-dark)]" : "border-[var(--line)] text-[var(--muted)]"}`}>
                <input className="sr-only" type="checkbox" checked={selected[airline.code]} onChange={(event) => setSelected((current) => ({ ...current, [airline.code]: event.target.checked }))} />
                <span className="font-semibold">{airline.short}</span><span className="ml-1 font-mono text-xs">{airline.code}</span>
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset className="mt-5">
          <legend className="mb-2 text-sm font-semibold">比較策略</legend>
          <div className="grid gap-2 sm:grid-cols-2">
            <label className={`cursor-pointer rounded-xl border p-3 text-sm leading-5 ${strategy === "reverse_two_segment" ? "border-[var(--teal)] bg-[#edf5f1]" : "border-[var(--line)]"}`}>
              <input className="sr-only" type="radio" name="back-to-back-strategy" value="reverse_two_segment" checked={strategy === "reverse_two_segment"} onChange={() => setStrategy("reverse_two_segment")} />
              <strong className="block">外站兩段票</strong>
              <span className="text-xs text-[var(--muted)]">反向來回票＋頭尾兩張單程</span>
            </label>
            <label className={`cursor-pointer rounded-xl border p-3 text-sm leading-5 ${strategy === "nested_round_trips" ? "border-[var(--teal)] bg-[#edf5f1]" : "border-[var(--line)]"}`}>
              <input className="sr-only" type="radio" name="back-to-back-strategy" value="nested_round_trips" checked={strategy === "nested_round_trips"} onChange={() => setStrategy("nested_round_trips")} />
              <strong className="block">包覆倒買</strong>
              <span className="text-xs text-[var(--muted)]">台灣始發來回票＋外站始發來回票</span>
            </label>
          </div>
        </fieldset>

        {strategy === "reverse_two_segment" && (
          <fieldset className="mt-4 rounded-2xl border border-amber-200 bg-amber-50/50 p-4">
            <legend className="px-2 text-sm font-bold text-amber-950">補齊外站兩段票</legend>
            <p className="mb-4 text-xs leading-5 text-amber-900">請填每位旅客實際查到的頭尾單程價。中段若為相同目的地，可留空讓系統比對公開反向來回價；兩次目的地不同時，中段是「第一次目的地 → 台灣 → 第二次目的地」多城市票，請手動補入。所有手動值都會明確標示，不會從來回票拆算。</p>
            <div className="grid gap-4 sm:grid-cols-3">
              {[
                {
                  label: "頭段：第一次旅行去程",
                  amount: headOneWayAmount,
                  setAmount: setHeadOneWayAmount,
                  currency: headOneWayCurrency,
                  setCurrency: setHeadOneWayCurrency,
                  airline: headOneWayAirline,
                  setAirline: setHeadOneWayAirline,
                  aria: "頭段單程",
                },
                {
                  label: firstDestination === secondDestination
                    ? "中段：外站反向來回票（可留空）"
                    : `中段：${firstDestination} → ${origin} → ${secondDestination}`,
                  amount: middleTwoSegmentAmount,
                  setAmount: setMiddleTwoSegmentAmount,
                  currency: middleTwoSegmentCurrency,
                  setCurrency: setMiddleTwoSegmentCurrency,
                  airline: middleTwoSegmentAirline,
                  setAirline: setMiddleTwoSegmentAirline,
                  aria: "中段反向兩航段",
                },
                {
                  label: "尾段：第二次旅行回程",
                  amount: tailOneWayAmount,
                  setAmount: setTailOneWayAmount,
                  currency: tailOneWayCurrency,
                  setCurrency: setTailOneWayCurrency,
                  airline: tailOneWayAirline,
                  setAirline: setTailOneWayAirline,
                  aria: "尾段單程",
                },
              ].map((fare) => (
                <div key={fare.aria} className="rounded-xl bg-white p-3">
                  <p className="text-sm font-semibold">{fare.label}</p>
                  <label className="mt-3 block text-xs font-semibold">每人價格
                    <div className="mt-1 flex gap-2">
                      <input aria-label={`${fare.aria}每人價格`} type="number" min="1" step="1" placeholder="尚未取得" value={fare.amount} onChange={(event) => fare.setAmount(event.target.value)} className="min-w-0 flex-1 rounded-lg border border-[var(--line)] p-2.5" />
                      <select aria-label={`${fare.aria}幣別`} value={fare.currency} onChange={(event) => fare.setCurrency(event.target.value)} className="rounded-lg border border-[var(--line)] p-2.5"><option value="TWD">TWD</option><option value="JPY">JPY</option><option value="USD">USD</option></select>
                    </div>
                  </label>
                  <label className="mt-3 block text-xs font-semibold">航空公司
                    <select aria-label={`${fare.aria}航空公司`} value={fare.airline} onChange={(event) => fare.setAirline(event.target.value as AirlineCode | "")} className="mt-1 w-full rounded-lg border border-[var(--line)] p-2.5"><option value="">未指定／其他</option><option value="CI">華航 CI</option><option value="BR">長榮 BR</option><option value="JX">星宇 JX</option></select>
                  </label>
                </div>
              ))}
            </div>
          </fieldset>
        )}

        <fieldset className="mt-4 rounded-2xl border border-[var(--line)] bg-[#fbfcf9] p-4">
          <legend className="px-2 text-sm font-bold">公開一般票找不到時補價</legend>
          <p className="mb-4 text-xs leading-5 text-[var(--muted)]">兩欄皆為選填。若航空公開快取在日期附近沒有一般來回價，可填入你在航空公司或 OTA 查到的每人總價，讓比較仍可完成。</p>
          <div className="grid gap-4 sm:grid-cols-2">
            {[
              {
                label: "第一次旅行一般來回票",
                amount: conventionalFirstAmount,
                setAmount: setConventionalFirstAmount,
                currency: conventionalFirstCurrency,
                setCurrency: setConventionalFirstCurrency,
                airline: conventionalFirstAirline,
                setAirline: setConventionalFirstAirline,
                aria: "第一次一般來回",
              },
              {
                label: "第二次旅行一般來回票",
                amount: conventionalSecondAmount,
                setAmount: setConventionalSecondAmount,
                currency: conventionalSecondCurrency,
                setCurrency: setConventionalSecondCurrency,
                airline: conventionalSecondAirline,
                setAirline: setConventionalSecondAirline,
                aria: "第二次一般來回",
              },
            ].map((fare) => (
              <div key={fare.aria} className="rounded-xl border border-[var(--line)] bg-white p-3">
                <p className="text-sm font-semibold">{fare.label}</p>
                <label className="mt-3 block text-xs font-semibold">每人價格
                  <div className="mt-1 flex gap-2">
                    <input aria-label={`${fare.aria}每人價格`} type="number" min="1" step="1" placeholder="使用公開票價" value={fare.amount} onChange={(event) => fare.setAmount(event.target.value)} className="min-w-0 flex-1 rounded-lg border border-[var(--line)] p-2.5" />
                    <select aria-label={`${fare.aria}幣別`} value={fare.currency} onChange={(event) => fare.setCurrency(event.target.value)} className="rounded-lg border border-[var(--line)] p-2.5"><option value="TWD">TWD</option><option value="JPY">JPY</option><option value="USD">USD</option></select>
                  </div>
                </label>
                <label className="mt-3 block text-xs font-semibold">航空公司
                  <select aria-label={`${fare.aria}航空公司`} value={fare.airline} onChange={(event) => fare.setAirline(event.target.value as AirlineCode | "")} className="mt-1 w-full rounded-lg border border-[var(--line)] p-2.5"><option value="">未指定／其他</option><option value="CI">華航 CI</option><option value="BR">長榮 BR</option><option value="JX">星宇 JX</option></select>
                </label>
              </div>
            ))}
          </div>
        </fieldset>

        {selectedAirlines.length === 1 && selectedAirlines[0] === "JX" && firstDestination === secondDestination && (
          <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm leading-6 text-amber-950">
            <strong className="block">單選星宇可能沒有完整倒買組合</strong>
            星宇公開頁的日期較零散；需要的公開票價必須在彈性日期內命中才能比較。系統仍會查詢並列出最接近的公開日期；若要先驗證完整流程，可同時勾選華航。
          </div>
        )}

        <div className="mt-5">
          <label className="text-sm font-semibold">出發地<select aria-label="倒買出發地" value={origin} onChange={(event) => setOrigin(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><option value="TPE">台北 TPE</option><option value="TSA">台北松山 TSA</option></select></label>
        </div>

        <fieldset className="mt-5 rounded-2xl border border-[var(--line)] p-4">
          <legend className="px-2 text-sm font-bold">第一次旅行</legend>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm font-semibold sm:col-span-2">第一次目的地國家／城市<select aria-label="第一次目的地" value={firstDestination} onChange={(event) => setFirstDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><DestinationOptions /></select></label>
            <label className="text-sm font-semibold">出發<input aria-label="第一次出發日" required type="date" value={firstDeparture} onChange={(event) => setFirstDeparture(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">回程<input aria-label="第一次回程日" required type="date" value={firstReturn} onChange={(event) => setFirstReturn(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
          </div>
        </fieldset>
        <fieldset className="mt-4 rounded-2xl border border-[var(--line)] p-4">
          <legend className="px-2 text-sm font-bold">第二次旅行</legend>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm font-semibold sm:col-span-2">第二次目的地國家／城市<select aria-label="第二次目的地" value={secondDestination} onChange={(event) => setSecondDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><DestinationOptions /></select></label>
            <label className="text-sm font-semibold">出發<input aria-label="第二次出發日" required type="date" value={secondDeparture} onChange={(event) => setSecondDeparture(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">回程<input aria-label="第二次回程日" required type="date" value={secondReturn} onChange={(event) => setSecondReturn(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
          </div>
        </fieldset>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="text-sm font-semibold">彈性日期<select aria-label="倒買彈性日期" value={flexDays} onChange={(event) => setFlexDays(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><option value="0">指定日期</option><option value="3">前後 3 天</option><option value="7">前後 7 天</option><option value="14">前後 14 天</option></select></label>
          <label className="text-sm font-semibold">艙等<select aria-label="倒買艙等" value={cabinClass} onChange={(event) => setCabinClass(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><option value="economy">經濟艙</option><option value="premium_economy">豪華經濟艙</option><option value="business">商務艙</option><option value="first">頭等艙</option></select></label>
        </div>

        <button disabled={busy || !selectedAirlines.length} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white transition hover:bg-[var(--teal-dark)] disabled:cursor-not-allowed disabled:opacity-50">
          {busy ? <><LoaderCircle className="animate-spin" size={18} />正在比對兩種買法</> : <><Shuffle size={18} />比較倒買價格</>}
        </button>
        <p className="mt-3 text-center text-xs text-[var(--muted)]">成功取得至少一組可比較價格才扣 1 次；失敗不扣。</p>
        {error && <div role="alert" className="mt-4 flex gap-2 rounded-xl bg-red-50 p-4 text-sm leading-6 text-red-800"><AlertCircle className="mt-0.5 shrink-0" size={18} />{error}</div>}
      </form>

      <div aria-live="polite" className="min-h-[38rem] rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7">
        <div className="border-b border-[var(--line)] pb-5">
          <p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Two-trip comparison</p>
          <h2 className="mt-1 text-2xl font-bold">兩趟旅行價格比較</h2>
        </div>
        {!result && !busy && <div className="grid min-h-[27rem] place-items-center text-center"><div className="max-w-md"><span className="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-[#edf5f1] text-[var(--teal)]"><Plane size={28} /></span><h3 className="mt-5 text-xl font-bold">需要兩趟旅行才能正確比較</h3><p className="mt-2 leading-7 text-[var(--muted)]">可分別比較「外站兩段票＋頭尾單程」及「包覆票＋外站始發倒買票」，不再把兩種玩法混稱為同一種倒買。</p></div></div>}
        {busy && <div className="grid min-h-[27rem] place-items-center text-center text-[var(--muted)]"><div><LoaderCircle className="mx-auto animate-spin text-[var(--teal)]" size={32} /><p className="mt-4">正在讀取台灣與外站始發公開票價…</p></div></div>}
        {result && !busy && <div className="mt-5 space-y-5">
          {result.usage && <p className={`rounded-xl p-3 text-sm font-semibold ${result.usage.status === "charged" ? "bg-[#fff4ef] text-[#7e4439]" : "bg-emerald-50 text-emerald-800"}`}>{result.usage.status === "charged" ? "本次已扣除 1 次" : "未取得可比較價格，本次未扣次"}</p>}
          {result.query?.strategy === "reverse_two_segment" && result.query.first_destination !== result.query.second_destination && (
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm leading-6 text-emerald-950">
              <p className="font-bold">不同目的地的外站兩段票已支援</p>
              <p className="mt-1">中段會依序顯示「第一次目的地 → 台灣」與「台灣 → 第二次目的地」。目前公開快取沒有這種多城市總價，因此使用你填入且標示為手動的中段票價完成比較。</p>
            </div>
          )}
          {result.pricing_capability === "open_jaw_provider_required" && (
            <div className="rounded-2xl border border-sky-200 bg-sky-50 p-4 text-sm leading-6 text-sky-950">
              <p className="font-bold">兩次目的地不同，倒買票會變成開口票</p>
              <p className="mt-1">目前可驗證兩張台灣來回票的基準價格；完整倒買方案需要「台灣→第一次目的地、第二次目的地→台灣」及反向的多城市票價來源，接上前不會估造價格。</p>
            </div>
          )}
          {result.warnings.map((warning) => <div key={warning} className="flex gap-2 rounded-xl bg-amber-50 p-3 text-sm leading-6 text-amber-900"><Info className="mt-0.5 shrink-0" size={17} />{warning}</div>)}
          {result.comparisons.map((comparison) => <ComparisonCard key={comparison.mode} comparison={comparison} pricingCapability={result.pricing_capability} strategy={result.query?.strategy || strategy} />)}
          {result.comparisons.every((comparison) => comparison.verdict === "comparison_unavailable") && rawCandidates.length > 0 && (
            <section className="rounded-2xl border border-[var(--line)] p-4">
              <h3 className="font-bold">已取得的原幣票價</h3>
              <div className="mt-3 space-y-2 text-sm">{rawCandidates.map((candidate) => <p key={candidate.role} className="flex justify-between gap-4"><span className="text-[var(--muted)]">{roleLabels[candidate.role]}</span><strong>{formatMoney(candidate.quotes[0].total_price, candidate.quotes[0].currency)} 起</strong></p>)}</div>
            </section>
          )}
          {externalRates.length > 0 && <p className="text-xs leading-5 text-[var(--muted)]">TWD 估算採用 <a className="font-semibold text-[var(--teal)] underline" href="https://frankfurter.dev/" target="_blank" rel="noreferrer">Frankfurter</a> {externalRates.map((rate) => `${rate.base_currency} ${rate.as_of}${rate.is_stale ? "（舊快取）" : ""}`).join("、")} 匯率；實際刷卡金額可能不同。</p>}
        </div>}

        <div className="mt-6 flex gap-3 rounded-2xl bg-[#fff4ef] p-4 text-sm leading-6 text-[#7e4439]">
          <ShieldAlert className="mt-0.5 shrink-0" size={20} />
          <p><strong className="block">倒買不是跳段票</strong>每張票都必須依票券順序完整搭乘。外站兩段票的頭尾單程、反向票須分開管理；公開價格非即時庫存、不可直接訂位，改票與取消也要分別處理。</p>
        </div>
      </div>
    </section>
  );
}
