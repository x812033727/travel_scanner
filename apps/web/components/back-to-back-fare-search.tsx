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
import { useLocale } from "next-intl";
import { useRouter } from "@/i18n/navigation";
import { FormEvent, useMemo, useState } from "react";
import { api, formatCurrency, isUsageInsufficient, twd } from "@/lib/api";
import {
  airlineName,
  cabinOptions,
  cityName,
  fareDate,
  fareLabCopy,
  fareLabText,
  fareLabWarnings,
  flexOptions,
  originOptions,
  type FareLabCopy,
} from "@/lib/fare-lab-copy";
import { useOperationCharge } from "@/components/usage-catalog-provider";

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


const airlines: AirlineCode[] = ["CI", "BR", "JX"];

const destinationGroups = [
  { country: "japan", cities: ["TYO", "OSA", "FUK", "CTS"] },
  { country: "korea", cities: ["SEL"] },
  { country: "thailand", cities: ["BKK"] },
  { country: "singapore", cities: ["SIN"] },
] as const;

function formatMoney(value: string | number, currency: string) {
  return formatCurrency(Number(value), currency);
}

function dateFromToday(days: number) {
  const now = new Date();
  const date = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + days));
  return date.toISOString().slice(0, 10);
}

function DestinationOptions({ copy }: { copy: FareLabCopy }) {
  return destinationGroups.map((group) => (
    <optgroup key={group.country} label={copy[`country.${group.country}`]}>
      {group.cities.map((code) => (
        <option value={code} key={code}>{cityName(copy, code)} {code}</option>
      ))}
    </optgroup>
  ));
}

function AirlineOptions({ copy }: { copy: FareLabCopy }) {
  return <>
    <option value="">{copy["b2b.airlineOther"]}</option>
    {airlines.map((code) => <option key={code} value={code}>{copy[`airlineShort.${code}`]} {code}</option>)}
  </>;
}

function StrategySummary({
  copy,
  title,
  strategy,
  emptyCopy = copy["b2b.summaryMissing"],
}: {
  copy: FareLabCopy;
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
      <p className="mt-1 text-xs text-[var(--muted)]">{copy["b2b.summaryPerTraveller"]}</p>
    </div>
  );
}

function TicketTimeline({ copy, tickets }: { copy: FareLabCopy; tickets: FareTicketComponent[] }) {
  return (
    <div className="mt-5 space-y-3">
      {tickets.map((ticket) => (
        <article key={`${ticket.role}-${ticket.quote.id}`} className="rounded-2xl border border-[var(--line)] p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="text-xs font-semibold text-[var(--coral)]">{copy[`ticketRole.${ticket.role}`]}</p>
              <p className="mt-1 font-bold">{airlineName(copy, ticket.quote.airline_code, ticket.quote.airline_name)} · {ticket.quote.airline_code}</p>
            </div>
            <div className="text-right">
              <p className="font-bold">{formatMoney(ticket.quote.total_price, ticket.quote.currency)}</p>
              {ticket.quote.currency !== "TWD" && ticket.estimated_twd !== undefined && (
                <p className="text-xs text-[var(--muted)]">{fareLabText(copy["b2b.approx"], { amount: twd.format(Number(ticket.estimated_twd)) })}</p>
              )}
            </div>
          </div>
          <div className="mt-3 flex flex-wrap items-center gap-2 text-sm text-[var(--muted)]">
            <span>{ticket.quote.origin}</span><ArrowRight size={14} /><span>{ticket.quote.destination}</span>
            <span className="mx-1 text-[var(--line)]">|</span>
            <span>{fareDate(ticket.quote.departure_date)}</span><ArrowRight size={14} /><span>{fareDate(ticket.quote.return_date)}</span>
          </div>
        </article>
      ))}
    </div>
  );
}

function SupplementalFareCard({ copy, fare }: { copy: FareLabCopy; fare: SupplementalFareComponent }) {
  const segments = fare.segments?.length
    ? fare.segments
    : [{ origin: fare.origin, destination: fare.destination, departure_date: fare.departure_date }];
  return (
    <article className="rounded-2xl border border-dashed border-amber-300 bg-amber-50/50 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold text-amber-800">{fareLabText(copy["b2b.manualTag"], { role: copy[`manualRole.${fare.role}`] })}</p>
          <p className="mt-1 font-bold">{fare.airline_code || copy["b2b.airlineUnknown"]}</p>
        </div>
        <div className="text-right">
          <p className="font-bold">{formatMoney(fare.amount, fare.currency)}</p>
          {fare.currency !== "TWD" && fare.estimated_twd !== undefined && (
            <p className="text-xs text-[var(--muted)]">{fareLabText(copy["b2b.approx"], { amount: twd.format(Number(fare.estimated_twd)) })}</p>
          )}
        </div>
      </div>
      <div className="mt-3 space-y-2 text-sm text-[var(--muted)]">
        {segments.map((segment, index) => (
          <div key={`${segment.origin}-${segment.destination}-${segment.departure_date}-${index}`} className="flex flex-wrap items-center gap-2">
            <span>{segment.origin}</span><ArrowRight size={14} /><span>{segment.destination}</span>
            <span className="mx-1 text-[var(--line)]">|</span>
            <span>{fareDate(segment.departure_date)}</span>
          </div>
        ))}
      </div>
    </article>
  );
}

function StrategyTimeline({ copy, strategy }: { copy: FareLabCopy; strategy: FareStrategyTotal }) {
  const head = strategy.supplemental_fares?.find((fare) => fare.role === "head_one_way");
  const middle = strategy.supplemental_fares?.find((fare) => fare.role === "middle_two_segment");
  const tail = strategy.supplemental_fares?.find((fare) => fare.role === "tail_one_way");
  const conventional = strategy.supplemental_fares?.filter((fare) => fare.role.startsWith("conventional_")) || [];
  return (
    <div className="mt-5 space-y-3">
      {conventional.map((fare) => <SupplementalFareCard key={fare.role} copy={copy} fare={fare} />)}
      {head && <SupplementalFareCard copy={copy} fare={head} />}
      <TicketTimeline copy={copy} tickets={strategy.tickets} />
      {middle && <SupplementalFareCard copy={copy} fare={middle} />}
      {tail && <SupplementalFareCard copy={copy} fare={tail} />}
    </div>
  );
}

function ComparisonCard({
  copy,
  comparison,
  pricingCapability,
  strategy,
}: {
  copy: FareLabCopy;
  comparison: BackToBackComparison;
  pricingCapability: BackToBackPricingCapability;
  strategy: BackToBackStrategy;
}) {
  const mixed = comparison.mode === "mixed_airlines";
  const savings = Number(comparison.savings_twd || 0);
  const savingsCopy = comparison.verdict === "back_to_back_cheaper"
    ? fareLabText(copy["b2b.saves"], { alternative: copy[`b2b.strategy.${strategy}`], amount: twd.format(savings) })
    : comparison.verdict === "conventional_cheaper"
      ? fareLabText(copy["b2b.conventionalSaves"], { amount: twd.format(Math.abs(savings)) })
      : comparison.verdict === "same_price"
        ? copy["b2b.samePrice"]
        : copy["b2b.cannotCompare"];
  const favorable = comparison.verdict === "back_to_back_cheaper";

  return (
    <article className={`rounded-[1.75rem] border bg-white p-5 md:p-6 ${mixed ? "border-[var(--teal)]" : "border-[var(--line)]"}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[.16em] text-[var(--teal)]">{mixed ? "LOWEST MIX" : "SAME AIRLINE"}</p>
          <h3 className="mt-1 text-xl font-bold">{copy[`mode.${comparison.mode}`]}</h3>
        </div>
        <Shuffle className="text-[var(--teal)]" size={22} />
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        <StrategySummary copy={copy} title={copy["b2b.conventionalTitle"]} strategy={comparison.conventional} />
        <StrategySummary
          copy={copy}
          title={
            pricingCapability === "open_jaw_provider_required"
              ? copy["b2b.openJawTickets"]
              : strategy === "reverse_two_segment"
                ? copy["b2b.reverseTickets"]
                : copy["b2b.nestedTickets"]
          }
          strategy={comparison.back_to_back}
          emptyCopy={pricingCapability === "open_jaw_provider_required" ? copy["b2b.openJawSourceNeeded"] : undefined}
        />
      </div>
      <div className={`mt-4 rounded-2xl p-4 text-sm ${favorable ? "bg-emerald-50 text-emerald-900" : "bg-amber-50 text-amber-900"}`}>
        <p className="font-bold">{savingsCopy}{comparison.savings_percent != null ? fareLabText(copy["b2b.percent"], { percent: Math.abs(Number(comparison.savings_percent)) }) : ""}</p>
        <p className="mt-1 leading-6">{fareLabWarnings([comparison.detail], copy, "ticketRole")[0]}</p>
      </div>
      {comparison.back_to_back && <StrategyTimeline copy={copy} strategy={comparison.back_to_back} />}
      {!comparison.back_to_back && comparison.conventional && (
        <StrategyTimeline copy={copy} strategy={comparison.conventional} />
      )}
    </article>
  );
}

/** A sentence with a link where `{name}` is, so a locale can put the link anywhere. */
function withLink(text: string, name: string, link: React.ReactNode) {
  const [before, after = ""] = text.split(`{${name}}`);
  return <>{before}{link}{after}</>;
}

export function BackToBackFareSearch() {
  const copy = fareLabCopy(useLocale());
  const charge = useOperationCharge("back_to_back_fare_search");
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
    () => airlines.filter((code) => selected[code]),
    [selected],
  );

  async function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    const dates = [firstDeparture, firstReturn, secondDeparture, secondReturn];
    if (dates.some((value) => !value) || !(firstDeparture < firstReturn && firstReturn < secondDeparture && secondDeparture < secondReturn)) {
      setError(copy["b2b.datesOutOfOrder"]);
      return;
    }
    if (!selectedAirlines.length) {
      setError(copy["form.selectAirline"]);
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
          <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Back-to-back search</p><h2 className="mt-1 text-2xl font-bold">{copy["b2b.formTitle"]}</h2></div>
          <CalendarRange className="text-[var(--teal)]" size={25} />
        </div>

        <fieldset>
          <legend className="mb-2 text-sm font-semibold">{copy["form.airlines"]}</legend>
          <div className="grid grid-cols-3 gap-2">
            {airlines.map((code) => (
              <label key={code} className={`cursor-pointer rounded-xl border px-3 py-3 text-center text-sm transition ${selected[code] ? "border-[var(--teal)] bg-[#edf5f1] text-[var(--teal-dark)]" : "border-[var(--line)] text-[var(--muted)]"}`}>
                <input className="sr-only" type="checkbox" checked={selected[code]} onChange={(event) => setSelected((current) => ({ ...current, [code]: event.target.checked }))} />
                <span className="font-semibold">{copy[`airlineShort.${code}`]}</span><span className="ml-1 font-mono text-xs">{code}</span>
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset className="mt-5">
          <legend className="mb-2 text-sm font-semibold">{copy["b2b.strategy"]}</legend>
          <div className="grid gap-2 sm:grid-cols-2">
            {(["reverse_two_segment", "nested_round_trips"] as const).map((option) => (
              <label key={option} className={`cursor-pointer rounded-xl border p-3 text-sm leading-5 ${strategy === option ? "border-[var(--teal)] bg-[#edf5f1]" : "border-[var(--line)]"}`}>
                <input className="sr-only" type="radio" name="back-to-back-strategy" value={option} checked={strategy === option} onChange={() => setStrategy(option)} />
                <strong className="block">{copy[`b2b.strategy.${option}`]}</strong>
                <span className="text-xs text-[var(--muted)]">{copy[`b2b.strategyHint.${option}`]}</span>
              </label>
            ))}
          </div>
        </fieldset>

        {strategy === "reverse_two_segment" && (
          <fieldset className="mt-4 rounded-2xl border border-amber-200 bg-amber-50/50 p-4">
            <legend className="px-2 text-sm font-bold text-amber-950">{copy["b2b.reverseLegend"]}</legend>
            <p className="mb-4 text-xs leading-5 text-amber-900">{copy["b2b.reverseHelp"]}</p>
            <div className="grid gap-4 sm:grid-cols-3">
              {[
                {
                  label: copy["b2b.headLabel"],
                  amount: headOneWayAmount,
                  setAmount: setHeadOneWayAmount,
                  currency: headOneWayCurrency,
                  setCurrency: setHeadOneWayCurrency,
                  airline: headOneWayAirline,
                  setAirline: setHeadOneWayAirline,
                  aria: copy["b2b.fare.head"],
                },
                {
                  label: firstDestination === secondDestination
                    ? copy["b2b.middleOptional"]
                    : fareLabText(copy["b2b.middleRoute"], { first: firstDestination, origin, second: secondDestination }),
                  amount: middleTwoSegmentAmount,
                  setAmount: setMiddleTwoSegmentAmount,
                  currency: middleTwoSegmentCurrency,
                  setCurrency: setMiddleTwoSegmentCurrency,
                  airline: middleTwoSegmentAirline,
                  setAirline: setMiddleTwoSegmentAirline,
                  aria: copy["b2b.fare.middle"],
                },
                {
                  label: copy["b2b.tailLabel"],
                  amount: tailOneWayAmount,
                  setAmount: setTailOneWayAmount,
                  currency: tailOneWayCurrency,
                  setCurrency: setTailOneWayCurrency,
                  airline: tailOneWayAirline,
                  setAirline: setTailOneWayAirline,
                  aria: copy["b2b.fare.tail"],
                },
              ].map((fare) => (
                <div key={fare.aria} className="rounded-xl bg-white p-3">
                  <p className="text-sm font-semibold">{fare.label}</p>
                  <label className="mt-3 block text-xs font-semibold">{copy["b2b.pricePerPerson"]}
                    <div className="mt-1 flex gap-2">
                      <input aria-label={fareLabText(copy["b2b.priceAria"], { fare: fare.aria })} type="number" min="1" step="1" placeholder={copy["b2b.notYetFound"]} value={fare.amount} onChange={(event) => fare.setAmount(event.target.value)} className="min-w-0 flex-1 rounded-lg border border-[var(--line)] p-2.5" />
                      <select aria-label={fareLabText(copy["b2b.currencyAria"], { fare: fare.aria })} value={fare.currency} onChange={(event) => fare.setCurrency(event.target.value)} className="rounded-lg border border-[var(--line)] p-2.5"><option value="TWD">TWD</option><option value="JPY">JPY</option><option value="USD">USD</option></select>
                    </div>
                  </label>
                  <label className="mt-3 block text-xs font-semibold">{copy["form.airline"]}
                    <select aria-label={fareLabText(copy["b2b.airlineAria"], { fare: fare.aria })} value={fare.airline} onChange={(event) => fare.setAirline(event.target.value as AirlineCode | "")} className="mt-1 w-full rounded-lg border border-[var(--line)] p-2.5"><AirlineOptions copy={copy} /></select>
                  </label>
                </div>
              ))}
            </div>
          </fieldset>
        )}

        <fieldset className="mt-4 rounded-2xl border border-[var(--line)] bg-[#fbfcf9] p-4">
          <legend className="px-2 text-sm font-bold">{copy["b2b.manualLegend"]}</legend>
          <p className="mb-4 text-xs leading-5 text-[var(--muted)]">{copy["b2b.manualHelp"]}</p>
          <div className="grid gap-4 sm:grid-cols-2">
            {[
              {
                label: copy["b2b.firstConventionalLabel"],
                amount: conventionalFirstAmount,
                setAmount: setConventionalFirstAmount,
                currency: conventionalFirstCurrency,
                setCurrency: setConventionalFirstCurrency,
                airline: conventionalFirstAirline,
                setAirline: setConventionalFirstAirline,
                aria: copy["b2b.fare.conventionalFirst"],
              },
              {
                label: copy["b2b.secondConventionalLabel"],
                amount: conventionalSecondAmount,
                setAmount: setConventionalSecondAmount,
                currency: conventionalSecondCurrency,
                setCurrency: setConventionalSecondCurrency,
                airline: conventionalSecondAirline,
                setAirline: setConventionalSecondAirline,
                aria: copy["b2b.fare.conventionalSecond"],
              },
            ].map((fare) => (
              <div key={fare.aria} className="rounded-xl border border-[var(--line)] bg-white p-3">
                <p className="text-sm font-semibold">{fare.label}</p>
                <label className="mt-3 block text-xs font-semibold">{copy["b2b.pricePerPerson"]}
                  <div className="mt-1 flex gap-2">
                    <input aria-label={fareLabText(copy["b2b.priceAria"], { fare: fare.aria })} type="number" min="1" step="1" placeholder={copy["b2b.usePublicFare"]} value={fare.amount} onChange={(event) => fare.setAmount(event.target.value)} className="min-w-0 flex-1 rounded-lg border border-[var(--line)] p-2.5" />
                    <select aria-label={fareLabText(copy["b2b.currencyAria"], { fare: fare.aria })} value={fare.currency} onChange={(event) => fare.setCurrency(event.target.value)} className="rounded-lg border border-[var(--line)] p-2.5"><option value="TWD">TWD</option><option value="JPY">JPY</option><option value="USD">USD</option></select>
                  </div>
                </label>
                <label className="mt-3 block text-xs font-semibold">{copy["form.airline"]}
                  <select aria-label={fareLabText(copy["b2b.airlineAria"], { fare: fare.aria })} value={fare.airline} onChange={(event) => fare.setAirline(event.target.value as AirlineCode | "")} className="mt-1 w-full rounded-lg border border-[var(--line)] p-2.5"><AirlineOptions copy={copy} /></select>
                </label>
              </div>
            ))}
          </div>
        </fieldset>

        {selectedAirlines.length === 1 && selectedAirlines[0] === "JX" && firstDestination === secondDestination && (
          <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm leading-6 text-amber-950">
            <strong className="block">{copy["b2b.starluxTitle"]}</strong>
            {copy["b2b.starluxBody"]}
          </div>
        )}

        <div className="mt-5">
          <label className="text-sm font-semibold">{copy["form.origin"]}<select aria-label={copy["b2b.originAria"]} value={origin} onChange={(event) => setOrigin(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{originOptions(copy).map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
        </div>

        <fieldset className="mt-5 rounded-2xl border border-[var(--line)] p-4">
          <legend className="px-2 text-sm font-bold">{copy["b2b.firstTrip"]}</legend>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm font-semibold sm:col-span-2">{copy["b2b.firstDestinationLabel"]}<select aria-label={copy["b2b.firstDestinationAria"]} value={firstDestination} onChange={(event) => setFirstDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><DestinationOptions copy={copy} /></select></label>
            <label className="text-sm font-semibold">{copy["b2b.depart"]}<input aria-label={copy["b2b.firstDepartAria"]} required type="date" value={firstDeparture} onChange={(event) => setFirstDeparture(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">{copy["b2b.return"]}<input aria-label={copy["b2b.firstReturnAria"]} required type="date" value={firstReturn} onChange={(event) => setFirstReturn(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
          </div>
        </fieldset>
        <fieldset className="mt-4 rounded-2xl border border-[var(--line)] p-4">
          <legend className="px-2 text-sm font-bold">{copy["b2b.secondTrip"]}</legend>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm font-semibold sm:col-span-2">{copy["b2b.secondDestinationLabel"]}<select aria-label={copy["b2b.secondDestinationAria"]} value={secondDestination} onChange={(event) => setSecondDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3"><DestinationOptions copy={copy} /></select></label>
            <label className="text-sm font-semibold">{copy["b2b.depart"]}<input aria-label={copy["b2b.secondDepartAria"]} required type="date" value={secondDeparture} onChange={(event) => setSecondDeparture(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">{copy["b2b.return"]}<input aria-label={copy["b2b.secondReturnAria"]} required type="date" value={secondReturn} onChange={(event) => setSecondReturn(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
          </div>
        </fieldset>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <label className="text-sm font-semibold">{copy["form.flexDays"]}<select aria-label={copy["b2b.flexAria"]} value={flexDays} onChange={(event) => setFlexDays(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{flexOptions(copy).map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
          <label className="text-sm font-semibold">{copy["form.cabin"]}<select aria-label={copy["b2b.cabinAria"]} value={cabinClass} onChange={(event) => setCabinClass(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{cabinOptions(copy).map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
        </div>

        <button disabled={busy || !selectedAirlines.length || charge.status !== "ready"} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white transition hover:bg-[var(--teal-dark)] disabled:cursor-not-allowed disabled:opacity-50">
          {busy ? <><LoaderCircle className="animate-spin" size={18} />{copy["b2b.comparing"]}</> : <><Shuffle size={18} />{fareLabText(copy["b2b.compare"], { charge: charge.label })}</>}
        </button>
        <p className="mt-3 text-center text-xs text-[var(--muted)]">{charge.status === "ready" ? fareLabText(copy["b2b.chargeHelp"], { charge: charge.label }) : charge.unavailableHelp}</p>
        {error && <div role="alert" className="mt-4 flex gap-2 rounded-xl bg-red-50 p-4 text-sm leading-6 text-red-800"><AlertCircle className="mt-0.5 shrink-0" size={18} />{error}</div>}
      </form>

      <div aria-live="polite" className="min-h-[38rem] rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7">
        <div className="border-b border-[var(--line)] pb-5">
          <p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Two-trip comparison</p>
          <h2 className="mt-1 text-2xl font-bold">{copy["b2b.resultsTitle"]}</h2>
        </div>
        {!result && !busy && <div className="grid min-h-[27rem] place-items-center text-center"><div className="max-w-md"><span className="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-[#edf5f1] text-[var(--teal)]"><Plane size={28} /></span><h3 className="mt-5 text-xl font-bold">{copy["b2b.emptyTitle"]}</h3><p className="mt-2 leading-7 text-[var(--muted)]">{copy["b2b.emptyBody"]}</p></div></div>}
        {busy && <div className="grid min-h-[27rem] place-items-center text-center text-[var(--muted)]"><div><LoaderCircle className="mx-auto animate-spin text-[var(--teal)]" size={32} /><p className="mt-4">{copy["b2b.busy"]}</p></div></div>}
        {result && !busy && <div className="mt-5 space-y-5">
          {result.usage && <p className={`rounded-xl p-3 text-sm font-semibold ${result.usage.status === "charged" ? "bg-[#fff4ef] text-[#7e4439]" : "bg-emerald-50 text-emerald-800"}`}>{result.usage.status === "charged" ? fareLabText(copy["usage.charged"], { uses: result.usage.uses }) : copy["b2b.notCharged"]}</p>}
          {result.query?.strategy === "reverse_two_segment" && result.query.first_destination !== result.query.second_destination && (
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm leading-6 text-emerald-950">
              <p className="font-bold">{copy["b2b.differentDestinationsTitle"]}</p>
              <p className="mt-1">{copy["b2b.differentDestinationsBody"]}</p>
            </div>
          )}
          {result.pricing_capability === "open_jaw_provider_required" && (
            <div className="rounded-2xl border border-sky-200 bg-sky-50 p-4 text-sm leading-6 text-sky-950">
              <p className="font-bold">{copy["b2b.openJawTitle"]}</p>
              <p className="mt-1">{copy["b2b.openJawBody"]}</p>
            </div>
          )}
          {fareLabWarnings(result.warnings, copy, "ticketRole").map((warning) => <div key={warning} className="flex gap-2 rounded-xl bg-amber-50 p-3 text-sm leading-6 text-amber-900"><Info className="mt-0.5 shrink-0" size={17} />{warning}</div>)}
          {result.comparisons.map((comparison) => <ComparisonCard key={comparison.mode} copy={copy} comparison={comparison} pricingCapability={result.pricing_capability} strategy={result.query?.strategy || strategy} />)}
          {result.comparisons.every((comparison) => comparison.verdict === "comparison_unavailable") && rawCandidates.length > 0 && (
            <section className="rounded-2xl border border-[var(--line)] p-4">
              <h3 className="font-bold">{copy["b2b.rawTitle"]}</h3>
              <div className="mt-3 space-y-2 text-sm">{rawCandidates.map((candidate) => <p key={candidate.role} className="flex justify-between gap-4"><span className="text-[var(--muted)]">{copy[`ticketRole.${candidate.role}`]}</span><strong>{fareLabText(copy["b2b.from"], { price: formatMoney(candidate.quotes[0].total_price, candidate.quotes[0].currency) })}</strong></p>)}</div>
            </section>
          )}
          {externalRates.length > 0 && <p className="text-xs leading-5 text-[var(--muted)]">{withLink(
            fareLabText(copy["b2b.fxNote"], {
              rates: externalRates.map((rate) => `${rate.base_currency} ${rate.as_of}${rate.is_stale ? copy["b2b.fxStale"] : ""}`).join(copy["b2b.listSeparator"]),
            }),
            "source",
            <a className="font-semibold text-[var(--teal)] underline" href="https://frankfurter.dev/" target="_blank" rel="noreferrer">Frankfurter</a>,
          )}</p>}
        </div>}

        <div className="mt-6 flex gap-3 rounded-2xl bg-[#fff4ef] p-4 text-sm leading-6 text-[#7e4439]">
          <ShieldAlert className="mt-0.5 shrink-0" size={20} />
          <p><strong className="block">{copy["b2b.disclaimerTitle"]}</strong>{copy["b2b.disclaimerBody"]}</p>
        </div>
      </div>
    </section>
  );
}
