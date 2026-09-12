"use client";

import { Check, ChevronDown, ChevronUp, ExternalLink, Leaf, LoaderCircle, Plane, PlaneLanding, PlaneTakeoff, RefreshCw } from "lucide-react";
import { useMemo, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import { PriceAlertButton } from "@/components/price-alert-button";
import { activeLocale, formatCurrency } from "@/lib/locale-format";

type FlightSegment = {
  origin?: string;
  destination?: string;
  departure_time?: string;
  arrival_time?: string;
  airline?: string;
  flight_number?: string;
  leg_index?: number;
  departure_timezone?: string | null;
  arrival_timezone?: string | null;
};

export type FlightCardOffer = {
  id: string;
  provider?: string;
  source_mode?: "live" | "test" | "mock" | "estimate";
  is_fallback?: boolean;
  airline?: unknown;
  marketing_airline?: unknown;
  operating_airlines?: unknown;
  selling_agent?: unknown;
  origin?: unknown;
  destination?: unknown;
  departure_time?: string;
  arrival_time?: string;
  return_departure_time?: string | null;
  return_arrival_time?: string | null;
  flight_number?: unknown;
  segments?: FlightSegment[];
  stops?: unknown;
  duration_minutes?: unknown;
  total_price?: unknown;
  currency?: string;
  retrieved_at?: string;
  last_verified_at?: string;
  clickout_available?: boolean;
  baggage_summary?: unknown;
  checked_baggage_kg?: unknown;
  carry_on?: unknown;
  arrival_day_offset?: unknown;
  base_price?: unknown;
  taxes?: unknown;
  fees?: unknown;
  refundable?: boolean;
  changeable?: boolean;
  original_currency?: string | null;
  original_total_price?: unknown;
  exchange_rate?: unknown;
  exchange_rate_retrieved_at?: string | null;
  expires_at?: string;
  verification_method?: string | null;
  emissions_kg_per_pax?: unknown;
  emissions_model_version?: string | null;
  status_details?: Array<Record<string, unknown>>;
};

type RefreshResult = { new_price: string | number; price_change: string | number; still_available: boolean; refreshed_at: string };

export type FlightLegDirection = "outbound" | "return";

/**
 * Shown on a search started from a saved trip: each leg of the offer can be
 * written into the trip's flight anchor. Labels come from the caller so the
 * card itself stays out of the message catalogs.
 */
export type FlightOfferTripActions = {
  labels: { outbound: string; return: string; busy: string; doneOutbound: string; doneReturn: string };
  state: Partial<Record<FlightLegDirection, "busy" | "done">>;
  onAttach: (direction: FlightLegDirection) => void;
};

function localParts(value?: string | null) {
  const match = value?.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  return match ? { date: `${Number(match[2])}/${Number(match[3])}`, isoDate: `${match[1]}-${match[2]}-${match[3]}`, time: `${match[4]}:${match[5]}` } : null;
}

type Translate = (key: string, values?: Record<string, string | number>) => string;

function durationLabel(t: Translate, minutes: number) {
  if (!minutes || minutes < 1) return t("notProvided");
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  if (hours && rest) return t("durationHoursMinutes", { hours, minutes: rest });
  return hours ? t("durationHours", { hours }) : t("durationMinutes", { minutes: rest });
}

function legDuration(segments: FlightSegment[], departure?: string | null, arrival?: string | null) {
  const start = segments[0]?.departure_time || departure;
  const end = segments.at(-1)?.arrival_time || arrival;
  if (!start || !end) return 0;
  const value = Math.round((Date.parse(end) - Date.parse(start)) / 60000);
  return Number.isFinite(value) && value > 0 ? value : 0;
}

function splitSegments(offer: FlightCardOffer) {
  const segments = offer.segments || [];
  if (segments.some((segment) => Number(segment.leg_index || 0) > 0)) {
    return [segments.filter((segment) => Number(segment.leg_index || 0) === 0), segments.filter((segment) => Number(segment.leg_index || 0) === 1)];
  }
  const returnIndex = segments.findIndex((segment, index) => index > 0 && segment.origin === String(offer.destination || ""));
  return returnIndex > 0 ? [segments.slice(0, returnIndex), segments.slice(returnIndex)] : [segments, []];
}

function FlightLeg({ label, segments, departure, arrival, fallbackOrigin, fallbackDestination }: { label: string; segments: FlightSegment[]; departure?: string | null; arrival?: string | null; fallbackOrigin: string; fallbackDestination: string }) {
  const t = useTranslations("search.results.flightCard");
  const shared = useTranslations("search.results");
  const first = segments[0];
  const last = segments.at(-1);
  const depart = localParts(first?.departure_time || departure);
  const arrive = localParts(last?.arrival_time || arrival);
  const numbers = Array.from(new Set(segments.map((segment) => segment.flight_number).filter(Boolean)));
  const dayOffset = depart && arrive ? Math.round((Date.parse(arrive.isoDate) - Date.parse(depart.isoDate)) / 86400000) : 0;
  return <div className="grid gap-3 rounded-xl bg-[var(--paper)] p-4 sm:grid-cols-[72px_1fr_auto] sm:items-center">
    <div><span className="rounded-full bg-white px-2.5 py-1 text-xs font-bold text-[var(--teal-dark)]">{label}</span><p className="mt-2 text-xs text-[var(--muted)]">{depart?.date || t("notProvided")}</p></div>
    <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
      <div><strong className="text-xl">{depart?.time || t("notProvided")}</strong><p className="text-sm text-[var(--muted)]">{first?.origin || fallbackOrigin}</p></div>
      <div className="min-w-20 text-center"><p className="text-xs text-[var(--muted)]">{durationLabel(t, legDuration(segments, departure, arrival))}</p><div className="my-1 h-px bg-[var(--line)]" /><p className="text-xs">{Math.max(0, segments.length - 1) ? shared("stops", { count: segments.length - 1 }) : shared("direct")}</p></div>
      <div className="text-right"><strong className="text-xl">{arrive?.time || t("notProvided")}{dayOffset > 0 ? <sup className="ml-1 text-xs text-[var(--coral)]">+{dayOffset}</sup> : null}</strong><p className="text-sm text-[var(--muted)]">{last?.destination || fallbackDestination}</p></div>
    </div>
    <p className="text-xs text-[var(--muted)] sm:text-right">{numbers.length ? numbers.join(shared("listSeparator")) : t("flightNumberUnknown")}<br />{t("localTime")}</p>
  </div>;
}

export function FlightOfferCard({ offer, fallbackUrl, alertReturnPath, tripActions }: { offer: FlightCardOffer; fallbackUrl: string; alertReturnPath?: string; tripActions?: FlightOfferTripActions }) {
  const t = useTranslations("search.results.flightCard");
  const shared = useTranslations("search.results");
  const [price, setPrice] = useState(Number(offer.total_price || 0));
  const [verifiedAt, setVerifiedAt] = useState(offer.last_verified_at || offer.retrieved_at);
  const [refreshing, setRefreshing] = useState(false);
  const [message, setMessage] = useState("");
  const [expanded, setExpanded] = useState(false);
  const [outbound, returning] = useMemo(() => splitSegments(offer), [offer]);
  const hasReturnLeg = returning.length > 0 || Boolean(offer.return_departure_time);
  // An estimate is a price for a date window, not a flight that can be booked.
  const legActions = tripActions && offer.source_mode !== "estimate" ? tripActions : undefined;
  const currency = offer.currency || "TWD";
  const money = (value: unknown) => formatCurrency(Number(value || 0), currency);
  const operating = Array.isArray(offer.operating_airlines) ? offer.operating_airlines.join(shared("listSeparator")) : "";
  const baggage = offer.baggage_summary
    ? String(offer.baggage_summary)
    : Number(offer.checked_baggage_kg || 0) > 0
      ? t("baggageChecked", { kg: String(offer.checked_baggage_kg) })
      : offer.carry_on
        ? t("baggageCarryOn")
        : t("baggageConfirm");

  async function refresh() {
    setRefreshing(true); setMessage("");
    try {
      const result = await api<RefreshResult>(`/offers/${offer.id}/refresh`, { method: "POST" });
      setPrice(Number(result.new_price)); setVerifiedAt(result.refreshed_at);
      setMessage(result.still_available ? t("refreshUpdated") : t("refreshSoldOut"));
    } catch (error) { setMessage((error as Error).message); }
    finally { setRefreshing(false); }
  }

  return <article className="overflow-hidden rounded-[1.5rem] border border-[var(--line)] bg-white">
    <div className="p-5 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4"><div><p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--teal)]"><Plane size={16} />{t(offer.source_mode === "estimate" ? "estimateHeading" : "liveHeading")}{offer.is_fallback ? ` · ${shared("fallbackSource")}` : ""}</p><h2 className="mt-1 text-xl font-bold">{String(offer.marketing_airline || offer.airline || t("airlineTbd"))}</h2><p className="mt-1 text-xs text-[var(--muted)]">{operating ? `${t("operatedBy", { airlines: operating })} · ` : ""}{t("sellingAgent", { agent: String(offer.selling_agent || t("sellingAgentTbd")) })}</p></div><div className="text-right"><strong className="text-xl">{money(price)}</strong><p className="mt-1 text-xs text-[var(--muted)]">{baggage}</p></div></div>
      <div className="mt-4 space-y-2">
        <FlightLeg label={t("legOutbound")} segments={outbound} departure={offer.departure_time} arrival={offer.arrival_time} fallbackOrigin={String(offer.origin || "")} fallbackDestination={String(offer.destination || "")} />
        {(returning.length || offer.return_departure_time) ? <FlightLeg label={t("legReturn")} segments={returning} departure={offer.return_departure_time} arrival={offer.return_arrival_time} fallbackOrigin={String(offer.destination || "")} fallbackDestination={String(offer.origin || "")} /> : null}
      </div>
      {(outbound.length + returning.length > 0) && <button type="button" onClick={() => setExpanded((value) => !value)} className="mt-3 flex items-center gap-1 text-sm font-semibold text-[var(--teal)]">{expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}{t(expanded ? "hideSegments" : "showSegments")}</button>}
      {expanded && <div className="mt-3 space-y-3 border-l-2 border-[var(--teal-soft)] pl-4">{([[
        t("legOutbound"), outbound,
      ], [t("legReturn"), returning]] as Array<[string, FlightSegment[]]>).map(([label, segments]) => segments.length ? <div key={label}><p className="mb-2 text-xs font-bold text-[var(--teal-dark)]">{label}</p>{segments.map((segment, index) => { const depart = localParts(segment.departure_time); const arrive = localParts(segment.arrival_time); const previous = segments[index - 1]; const layover = previous?.arrival_time && segment.departure_time ? Math.round((Date.parse(segment.departure_time) - Date.parse(previous.arrival_time)) / 60000) : 0; return <div key={`${segment.flight_number || "segment"}-${index}`} className="mb-2 rounded-xl border border-[var(--line)] p-3 text-sm">{index > 0 && layover > 0 ? <p className="mb-2 text-xs font-semibold text-[var(--coral)]">{t("layover", { duration: durationLabel(t, layover) })}</p> : null}<div className="flex flex-wrap justify-between gap-2"><strong>{segment.airline || t("airlineUnknown")} · {segment.flight_number || t("flightNumberUnknown")}</strong><span>{depart?.date || t("notProvided")} {depart?.time || t("notProvided")} {segment.origin || "—"} → {arrive?.time || t("notProvided")} {segment.destination || "—"}</span></div><p className="mt-1 text-xs text-[var(--muted)]">{segment.departure_timezone || t("localTime")} → {segment.arrival_timezone || t("localTime")}</p></div>; })}</div> : null)}</div>}
      <p className="mt-3 text-xs text-[var(--muted)]">{shared("sourceLine", { provider: offer.provider || shared("unlabelled") })}{verifiedAt ? ` · ${t("verifiedAt", { time: new Date(verifiedAt).toLocaleString(activeLocale()) })}` : ""}</p>
      <div className="mt-3 grid gap-2 rounded-xl bg-[var(--paper)] p-3 text-xs text-[var(--muted)] sm:grid-cols-2">
        <p>{t("fareLine", { base: money(offer.base_price), taxes: money(offer.taxes) })}{Number(offer.fees || 0) ? ` · ${t("feesExtra", { fees: money(offer.fees) })}` : ""}</p>
        <p>{offer.refundable ? shared("refundable") : t("nonRefundable")} · {t(offer.changeable ? "changeable" : "nonChangeable")}</p>
        {offer.original_currency && offer.original_total_price != null && offer.original_currency !== currency ? <p>{t("originalCurrency", { currency: offer.original_currency, amount: Number(offer.original_total_price).toLocaleString(activeLocale()), rate: String(offer.exchange_rate || t("rateTbd")) })}</p> : null}
        <p>{offer.expires_at ? t("expiresAt", { time: new Date(offer.expires_at).toLocaleString(activeLocale()) }) : t("expiresTbd")}</p>
      </div>
      <p className="mt-3 flex items-center gap-2 text-sm"><Leaf size={16} className="text-emerald-700" />{offer.emissions_kg_per_pax != null ? t("emissions", { kg: Number(offer.emissions_kg_per_pax).toFixed(1), model: `Google Travel Impact Model${offer.emissions_model_version ? ` ${offer.emissions_model_version}` : ""}` }) : t("emissionsUnknown")}</p>
      {offer.status_details?.map((status, index) => <p key={`${String(status.fa_flight_id || status.ident)}-${index}`} className="mt-2 rounded-lg bg-sky-50 px-3 py-2 text-xs text-sky-900">{t("flightAware", { status: status.schedule_only ? t("flightAwareSchedule") : String(status.status || t("flightAwareUpdated")) })}{status.cancelled ? ` · ${t("flightAwareCancelled")}` : ""}{Number(status.departure_delay_seconds || 0) > 0 ? ` · ${t("flightAwareDelay", { minutes: Math.round(Number(status.departure_delay_seconds) / 60) })}` : ""}{status.departure_terminal ? ` · ${t("flightAwareTerminal", { terminal: String(status.departure_terminal) })}` : ""}{status.departure_gate ? ` · ${t("flightAwareGate", { gate: String(status.departure_gate) })}` : ""}</p>)}
      {offer.provider === "skyscanner" && <p className="mt-2 text-xs text-[var(--muted)]">Powered by <a className="font-semibold underline" href="https://www.skyscanner.net" target="_blank" rel="noreferrer">Skyscanner</a></p>}
      {message && <p className="mt-3 text-sm text-[var(--coral)]" role="status">{message}</p>}
      <div className="mt-4 grid gap-2 sm:grid-cols-2"><button type="button" onClick={refresh} disabled={refreshing || offer.source_mode === "estimate"} className="flex items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold disabled:opacity-50"><RefreshCw size={16} className={refreshing ? "animate-spin" : ""} />{t(refreshing ? "verifying" : "verify")}</button>{offer.clickout_available ? <form action={`/api/travel/offers/${offer.id}/clickout`} method="post" target="_blank"><button className="flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white" type="submit">{t("book")} <ExternalLink size={16} /></button></form> : <a href={safeExternalHref(fallbackUrl)} target="_blank" rel="noreferrer" className="flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]">{shared("recheckExternal")}<ExternalLink size={16} /></a>}</div>
      {legActions && <div className="mt-3 grid gap-2 sm:grid-cols-2">{(["outbound", "return"] as const).filter((direction) => direction === "outbound" || hasReturnLeg).map((direction) => {
        const state = legActions.state[direction];
        const label = state === "done" ? (direction === "outbound" ? legActions.labels.doneOutbound : legActions.labels.doneReturn) : state === "busy" ? legActions.labels.busy : direction === "outbound" ? legActions.labels.outbound : legActions.labels.return;
        return <button key={direction} type="button" onClick={() => legActions.onAttach(direction)} disabled={state === "busy"} className={`flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold disabled:opacity-50 ${state === "done" ? "bg-emerald-50 text-emerald-800" : "bg-[var(--teal-soft)] text-[var(--teal-dark)]"}`}>
          {state === "done" ? <Check size={16} /> : state === "busy" ? <LoaderCircle size={16} className="animate-spin" /> : direction === "outbound" ? <PlaneTakeoff size={16} /> : <PlaneLanding size={16} />}{label}
        </button>;
      })}</div>}
      {offer.source_mode !== "estimate" && <PriceAlertButton resourceType="flight" resourceId={offer.id} currentPrice={price} currency={currency} returnPath={alertReturnPath} />}
    </div>
  </article>;
}
