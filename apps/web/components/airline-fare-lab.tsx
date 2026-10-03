"use client";

import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  CircleDot,
  ExternalLink,
  Info,
  LoaderCircle,
  LogIn,
  Plane,
  Radar,
  Search,
  ShieldCheck,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/navigation";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { BackToBackFareSearch } from "@/components/back-to-back-fare-search";
import { LiveBackToBackSearch } from "@/components/live-back-to-back-search";
import { useSavedItems } from "@/components/saved-items-provider";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { UsageInsufficientNotice } from "@/components/usage-insufficient-notice";
import { api, ApiError, isUsageInsufficient, twd } from "@/lib/api";
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
} from "@/lib/fare-lab-copy";
import { loginPath, safeExternalHref } from "@/lib/navigation";

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

const airlines: AirlineCode[] = ["CI", "BR", "JX"];

const destinations = ["NRT", "KIX", "FUK", "CTS", "ICN", "BKK", "SIN"];

const stateClass: Record<SourceState, string> = {
  ready: "bg-emerald-50 text-emerald-800",
  success: "bg-emerald-50 text-emerald-800",
  disabled: "bg-amber-50 text-amber-800",
  blocked: "bg-amber-50 text-amber-800",
  failed: "bg-red-50 text-red-800",
};

function sourceFor(code: AirlineCode, sources: CrawlerSource[]) {
  return sources.find((source) => source.airline_code === code);
}

function searchError(reason: unknown) {
  return { message: (reason as Error).message, signIn: reason instanceof ApiError && reason.status === 401 };
}

const FARE_MODES = ["conventional", "back_to_back", "live_back_to_back"] as const;
type FareMode = (typeof FARE_MODES)[number];
const FARE_TAB_KEYS = ["ArrowLeft", "ArrowRight", "Home", "End"];

export function AirlineFareLab() {
  const copy = fareLabCopy(useLocale());
  const charge = useOperationCharge("public_airline_fare_search");
  const [insufficient, setInsufficient] = useState(false);
  // All three modes charge a use; a signed-out visitor gets one sign-in card instead of
  // three live charge buttons that can only fail with 401.
  const session = useSavedItems();
  const pathname = usePathname();
  const usage = useTranslations("usage");
  const auth = useTranslations("auth");
  const [mode, setMode] = useState<FareMode>("conventional");

  /** Arrow keys move between tabs, as the role promises. Same shape as admin-tabs. */
  function moveFareTab(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    if (!FARE_TAB_KEYS.includes(event.key)) return;
    event.preventDefault();
    const next = event.key === "Home"
      ? 0
      : event.key === "End"
        ? FARE_MODES.length - 1
        : (index + (event.key === "ArrowRight" ? 1 : -1) + FARE_MODES.length) % FARE_MODES.length;
    setMode(FARE_MODES[next]);
    requestAnimationFrame(() => document.getElementById(`fare-tab-${FARE_MODES[next]}`)?.focus());
  }
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
  // `signIn` comes from the status code. It used to be read off the message, which
  // only worked while the message was English or Chinese.
  const [error, setError] = useState<{ message: string; signIn?: boolean }>();

  useEffect(() => {
    api<CrawlerStatus>("/crawlers/airlines/status")
      .then(setStatus)
      .catch((reason: unknown) => setError(searchError(reason)));
  }, []);

  const selectedAirlines = useMemo(
    () => airlines.filter((code) => selected[code]),
    [selected],
  );

  async function searchFares(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(undefined);
    if (returnDate && departureDate && returnDate < departureDate) {
      setError({ message: copy["lab.returnBeforeDeparture"] });
      return;
    }
    if (!selectedAirlines.length) {
      setError({ message: copy["form.selectAirline"] });
      return;
    }
    setBusy(true);
    setInsufficient(false);
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
        setInsufficient(true);
        return;
      }
      setError(searchError(reason));
    } finally {
      setBusy(false);
    }
  }

  const activeSources = result?.sources || status?.sources || [];

  return (
    <main className="mx-auto max-w-6xl px-5 pb-24 md:px-8">
      <section className="mb-8 grid gap-6 pt-8 lg:grid-cols-[1.25fr_.75fr] lg:items-end">
        <div>
          <p className="mb-3 flex items-center gap-2 text-sm font-semibold text-[var(--coral)]">
            <Radar size={17} /> PUBLIC FARE LAB
          </p>
          <h1 className="max-w-3xl text-4xl font-bold tracking-[-.035em] md:text-6xl">
            {copy["lab.title"]}
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-[var(--muted)] md:text-lg">
            {copy["lab.intro"]}
          </p>
        </div>
        <aside className="rounded-3xl border border-[var(--line)] bg-[#edf5f1] p-5 text-sm leading-6 text-[var(--teal-dark)]">
          <p className="flex items-center gap-2 font-semibold"><ShieldCheck size={18} />{copy["lab.safeTitle"]}</p>
          <p className="mt-2">{copy["lab.safeBody"]}</p>
        </aside>
      </section>

      <section aria-label={copy["lab.sources"]} className="mb-6 grid gap-3 sm:grid-cols-3">
        {airlines.map((code) => {
          const source = sourceFor(code, activeSources);
          return (
            <article key={code} className="rounded-2xl border border-[var(--line)] bg-white p-4 shadow-[0_10px_35px_rgba(16,42,43,.05)]">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] font-mono text-sm font-bold text-white">{code}</span>
                  <div><strong className="block">{airlineName(copy, code)}</strong><span className="text-xs text-[var(--muted)]">{source?.host || copy["lab.sourceChecking"]}</span></div>
                </div>
                <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${source ? stateClass[source.state] : "bg-slate-100 text-slate-600"}`}>
                  {source ? copy[`state.${source.state}`] : copy["lab.stateChecking"]}
                </span>
              </div>
            </article>
          );
        })}
      </section>

      {/* role="tab" without a roving tabindex, aria-controls or a panel promised a
          widget that was not there: every tab was its own tab stop and none of them
          said what it controlled. admin-tabs.tsx is the house pattern. */}
      <div role="tablist" aria-label={copy["lab.tablist"]} className="mb-6 grid max-w-2xl grid-cols-1 gap-1 rounded-2xl border border-[var(--line)] bg-white p-1.5 sm:grid-cols-3 sm:gap-0">
        {FARE_MODES.map((tab, index) => {
          const selected = mode === tab;
          return <button
            key={tab}
            id={`fare-tab-${tab}`}
            type="button"
            role="tab"
            aria-selected={selected}
            aria-controls="fare-tabpanel"
            tabIndex={selected ? 0 : -1}
            onKeyDown={(event) => moveFareTab(event, index)}
            onClick={() => setMode(tab)}
            className={`min-h-11 rounded-xl px-4 py-2.5 text-sm font-semibold transition ${selected ? "bg-[var(--ink)] text-white" : "text-[var(--muted)]"}`}
          >{copy[`lab.tab.${tab}`]}</button>;
        })}
      </div>
      <div id="fare-tabpanel" role="tabpanel" aria-labelledby={`fare-tab-${mode}`} tabIndex={0}>

      {session.status === "signed_out" ? <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-8 text-center shadow-[0_22px_70px_rgba(16,42,43,.08)]">
        <LogIn className="mx-auto text-[var(--teal)]" size={30} />
        <h2 className="mt-4 text-2xl font-bold">{usage("signInToUse")} · {charge.label}</h2>
        <Link href={loginPath(pathname)} className="mt-6 inline-flex min-h-12 items-center rounded-2xl bg-[var(--teal)] px-6 font-bold text-white">{auth("signIn")}</Link>
      </section> : mode === "live_back_to_back" ? <LiveBackToBackSearch /> : mode === "back_to_back" ? <BackToBackFareSearch /> : <section className="grid gap-6 lg:grid-cols-[.82fr_1.18fr]">
        <form onSubmit={searchFares} className="self-start rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-[0_22px_70px_rgba(16,42,43,.08)] md:p-7">
          <div className="mb-6 flex items-center justify-between">
            <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--teal)]">Search controls</p><h2 className="mt-1 text-2xl font-bold">{copy["lab.formTitle"]}</h2></div>
            <Plane className="text-[var(--teal)]" size={25} />
          </div>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold">{copy["form.airlines"]}</legend>
            <div className="grid grid-cols-3 gap-2">
              {airlines.map((code) => (
                <label key={code} className={`cursor-pointer rounded-xl border px-3 py-3 text-center text-sm transition ${selected[code] ? "border-[var(--teal)] bg-[#edf5f1] text-[var(--teal-dark)]" : "border-[var(--line)] text-[var(--muted)]"}`}>
                  <input
                    className="sr-only"
                    type="checkbox"
                    checked={selected[code]}
                    onChange={(event) => setSelected((current) => ({ ...current, [code]: event.target.checked }))}
                  />
                  <span className="font-semibold">{copy[`airlineShort.${code}`]}</span><span className="ml-1 font-mono text-xs">{code}</span>
                </label>
              ))}
            </div>
          </fieldset>

          <div className="mt-5 grid grid-cols-[1fr_auto_1fr] items-end gap-2">
            <label className="text-sm font-semibold">{copy["form.origin"]}<select aria-label={copy["form.origin"]} value={origin} onChange={(event) => setOrigin(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{originOptions(copy).map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
            <ArrowRight className="mb-3 text-[var(--muted)]" size={18} />
            <label className="text-sm font-semibold">{copy["lab.destination"]}<select aria-label={copy["lab.destination"]} value={destination} onChange={(event) => setDestination(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{destinations.map((code) => <option value={code} key={code}>{cityName(copy, code)} {code}</option>)}</select></label>
          </div>

          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <label className="text-sm font-semibold">{copy["lab.departureDate"]}<input aria-label={copy["lab.departureDate"]} type="date" value={departureDate} onChange={(event) => setDepartureDate(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">{copy["lab.returnDate"]}<input aria-label={copy["lab.returnDate"]} type="date" value={returnDate} onChange={(event) => setReturnDate(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3" /></label>
            <label className="text-sm font-semibold">{copy["form.flexDays"]}<select aria-label={copy["form.flexDays"]} value={flexDays} onChange={(event) => setFlexDays(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{flexOptions(copy).map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
            <label className="text-sm font-semibold">{copy["form.cabin"]}<select aria-label={copy["form.cabin"]} value={cabinClass} onChange={(event) => setCabinClass(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-[#fbfcf9] p-3">{cabinOptions(copy).map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
          </div>

          <button disabled={busy || !selectedAirlines.length || charge.status !== "ready"} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white transition hover:bg-[var(--teal-dark)] disabled:cursor-not-allowed disabled:opacity-50">
            {busy ? <><LoaderCircle className="animate-spin" size={18} />{copy["lab.searching"]}</> : <><Search size={18} />{fareLabText(copy["lab.search"], { charge: charge.label })}</>}
          </button>
          <p className="mt-3 text-center text-xs text-[var(--muted)]">{charge.status === "ready" ? fareLabText(copy["lab.chargeHelp"], { charge: charge.label }) : charge.unavailableHelp}</p>
        </form>

        <div aria-live="polite" className="min-h-[34rem] rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7">
          <div className="flex flex-wrap items-start justify-between gap-3 border-b border-[var(--line)] pb-5">
            <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-[var(--coral)]">Public fare signals</p><h2 className="mt-1 text-2xl font-bold">{copy["lab.resultsTitle"]}</h2></div>
            {result && <span className="rounded-full bg-[#edf5f1] px-3 py-1.5 text-sm font-semibold text-[var(--teal-dark)]">{fareLabText(copy["lab.resultCount"], { count: result.quotes.length })}</span>}
          </div>

          {insufficient && <div className="mt-5"><UsageInsufficientNotice chargeLabel={charge.label} /></div>}
          {error && <div role="alert" className="mt-5 flex items-start gap-3 rounded-2xl bg-red-50 p-4 text-sm leading-6 text-red-800"><AlertCircle className="mt-0.5 shrink-0" size={19} /><div><strong className="block">{copy["lab.errorTitle"]}</strong>{error.message}{error.signIn && <Link href={loginPath(pathname)} className="ml-1 font-semibold underline">{copy["lab.goSignIn"]}</Link>}</div></div>}

          {!result && !busy && !error && <div className="grid min-h-[25rem] place-items-center text-center"><div className="max-w-sm"><span className="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-[#edf5f1] text-[var(--teal)]"><CircleDot size={28} /></span><h3 className="mt-5 text-xl font-bold">{copy["lab.emptyTitle"]}</h3><p className="mt-2 leading-7 text-[var(--muted)]">{copy["lab.emptyBody"]}</p></div></div>}

          {busy && <div className="grid min-h-[25rem] place-items-center text-center"><div><LoaderCircle className="mx-auto animate-spin text-[var(--teal)]" size={36} /><p className="mt-4 font-semibold">{copy["lab.busy"]}</p></div></div>}

          {result && !busy && <div className="mt-5 space-y-4">
            {result.usage && <p className={`rounded-xl p-3 text-sm font-semibold ${result.usage.status === "charged" ? "bg-[#fff4ef] text-[#7e4439]" : "bg-emerald-50 text-emerald-800"}`}>{result.usage.status === "charged" ? fareLabText(copy["usage.charged"], { uses: result.usage.uses }) : copy["lab.notCharged"]}</p>}
            {fareLabWarnings(result.warnings, copy, "ticketRole").map((warning) => <div key={warning} className="flex gap-2 rounded-xl bg-amber-50 p-3 text-sm text-amber-900"><Info className="mt-0.5 shrink-0" size={17} />{warning}</div>)}
            {result.quotes.length === 0 ? <div className="grid min-h-64 place-items-center text-center text-[var(--muted)]"><div><Search className="mx-auto mb-3" size={28} /><p>{copy["lab.noQuotes"]}</p></div></div> : result.quotes.map((quote) => (
              <article key={quote.id} className="rounded-2xl border border-[var(--line)] p-4 transition hover:border-[#b7cbc0] md:p-5">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div className="flex items-start gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-[var(--ink)] font-mono text-sm font-bold text-white">{quote.airline_code}</span><div><h3 className="font-bold">{airlineName(copy, quote.airline_code, quote.airline_name)}</h3><p className="mt-1 flex items-center gap-2 text-sm text-[var(--muted)]">{quote.origin}<ArrowRight size={14} />{quote.destination}</p></div></div>
                  <div className="text-right"><p className="text-2xl font-bold">{quote.currency === "TWD" ? twd.format(Number(quote.total_price)) : `${quote.currency} ${quote.total_price}`}</p><p className="text-xs text-[var(--muted)]">{copy["lab.perTraveller"]}</p></div>
                </div>
                <div className="mt-4 grid gap-2 rounded-xl bg-[#f7f9f5] p-3 text-sm sm:grid-cols-2"><p><span className="text-[var(--muted)]">{copy["lab.outbound"]}</span><strong className="ml-2">{fareDate(quote.departure_date)}</strong></p><p><span className="text-[var(--muted)]">{copy["lab.inbound"]}</span><strong className="ml-2">{fareDate(quote.return_date)}</strong></p></div>
                <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-[var(--muted)]"><span className="flex items-center gap-1.5"><CheckCircle2 size={15} className="text-[var(--teal)]" />{copy["lab.notLive"]}{quote.price_last_seen ? ` · ${quote.price_last_seen}` : ""}</span><a href={safeExternalHref(quote.source_url)} target="_blank" rel="noreferrer" className="flex items-center gap-1 font-semibold text-[var(--teal)]">{copy["lab.officialSource"]}<ExternalLink size={14} /></a></div>
              </article>
            ))}
          </div>}
        </div>
      </section>}
      </div>
    </main>
  );
}
