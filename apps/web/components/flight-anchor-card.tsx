import { ArrowRight, Clock3, Pencil, Plane, RadioTower, RouteOff, Search, Tag } from "lucide-react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { itineraryCopy, itineraryText, type ItineraryCopy } from "@/lib/itinerary-copy";
import { activeLocale, formatCurrency } from "@/lib/locale-format";
import { PriceAlertButton } from "@/components/price-alert-button";
import { flightStatusSnapshot, priceSnapshot, type TripItem } from "@/lib/trip-types";

export type FlightAnchorInfo = {
  airline?: string;
  flight_number?: string;
  origin?: string;
  destination?: string;
  departure_local?: string;
  arrival_local?: string;
  departure_timezone?: string | null;
  arrival_timezone?: string | null;
  stops?: number;
};

export function flightAnchorInfo(item: TripItem): FlightAnchorInfo | null {
  const value = item.data.flight_info;
  return value && typeof value === "object" ? value as FlightAnchorInfo : null;
}

/**
 * The anchor carries a wall-clock time at the airport, so it is formatted from its own
 * digits rather than through a Date: constructing one would shift 08:40 in Taipei by
 * whatever zone the reader's browser happens to be in. Only the date is handed to Intl,
 * so the day and month land in the reader's own order while the clock stays untouched.
 */
function localDateTime(copy: ItineraryCopy, locale: string, value?: string) {
  if (!value) return copy.flightTimePending;
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  if (!match) return value;
  const [, year, month, day, hour, minute] = match;
  const parts = new Intl.DateTimeFormat(locale, { month: "numeric", day: "numeric" })
    .format(new Date(Number(year), Number(month) - 1, Number(day)));
  return `${parts} ${hour}:${minute}`;
}

export function FlightAnchorCard({
  item,
  busy = false,
  onEdit,
  search,
  flightStatus,
  alertReturnPath,
}: {
  item: TripItem;
  busy?: boolean;
  onEdit?: () => void;
  /** The trip's flight search (`/search?trip_id=…`) and what one search costs. */
  search?: { href: string; charge: string };
  /** The status lookup for this flight, prefilled from the anchor. */
  flightStatus?: { href: string; charge: string };
  /** Where to send someone who has to sign in before creating the alert. */
  alertReturnPath?: string;
}) {
  const t = useTranslations("trips");
  // The same side catalog the timeline reads. This card is what a share recipient sees at
  // the two ends of someone else's trip, so it answers to their language, not the author's.
  const locale = activeLocale();
  const copy = itineraryCopy(locale);
  const info = flightAnchorInfo(item);
  const outbound = item.system_role === "outbound_flight";
  const label = outbound ? copy.flightOutbound : copy.flightReturn;
  const configuredInfo = info?.airline && info.flight_number ? info : null;
  const configured = Boolean(configuredInfo);
  const departureTimezone = info?.departure_timezone || copy.flightTimezonePending;
  const arrivalTimezone = info?.arrival_timezone || copy.flightTimezonePending;
  // The quote the anchor was created from. A hand-typed flight never carries one,
  // so the line only appears on anchors that came out of a real search.
  const quote = configuredInfo ? priceSnapshot(item) : null;
  const status = configuredInfo ? flightStatusSnapshot(item) : null;

  return <article className="planner-flight-card">
    <div className="flex items-start gap-3">
      <span className="planner-flight-icon"><Plane size={19} /></span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-xs font-bold tracking-[.08em] text-sky-900">{label}</p>
          <span className="planner-flight-badge"><Clock3 size={12} />{copy.flightFixedTime}</span>
          <span className="planner-flight-badge"><RouteOff size={12} />{copy.flightOutsideCityRoute}</span>
        </div>
        {configuredInfo ? <>
          <h3 className="mt-2 text-lg font-bold text-slate-900">{configuredInfo.airline} {configuredInfo.flight_number}</h3>
          <div className="mt-3 grid grid-cols-[1fr_auto_1fr] items-center gap-2 rounded-xl bg-white/70 p-3">
            <div>
              <p className="text-lg font-black text-slate-900">{configuredInfo.origin}</p>
              <p className="mt-0.5 text-sm font-semibold text-slate-700">{localDateTime(copy, locale, configuredInfo.departure_local)}</p>
              <p className={`mt-1 text-xs ${configuredInfo.departure_timezone ? "text-slate-500" : "font-semibold text-amber-700"}`}>{departureTimezone}</p>
            </div>
            <ArrowRight size={18} className="text-sky-600" />
            <div className="text-right">
              <p className="text-lg font-black text-slate-900">{configuredInfo.destination}</p>
              <p className="mt-0.5 text-sm font-semibold text-slate-700">{localDateTime(copy, locale, configuredInfo.arrival_local)}</p>
              <p className={`mt-1 text-xs ${configuredInfo.arrival_timezone ? "text-slate-500" : "font-semibold text-amber-700"}`}>{arrivalTimezone}</p>
            </div>
          </div>
          {typeof configuredInfo.stops === "number" && <p className="mt-2 text-xs text-slate-600">{configuredInfo.stops === 0 ? copy.flightNonstop : itineraryText(copy.flightConnections, { count: configuredInfo.stops })}</p>}
          {quote && <p className="mt-2 flex flex-wrap items-center gap-1.5 text-xs font-semibold text-sky-900">
            <Tag size={13} aria-hidden />
            {t("quotedPrice", { amount: formatCurrency(Number(quote.total_price), quote.currency) })}
            {quote.provider && <span className="font-normal text-slate-600">· {t("quotedBy", { provider: quote.provider })}</span>}
          </p>}
          {status && <p className="mt-2 flex flex-wrap items-center gap-1.5 text-xs font-semibold text-sky-900">
            <RadioTower size={13} aria-hidden />
            {t("flightStatusLine", { status: status.status || "—", date: localDateTime(copy, locale, status.checked_at) })}
            {Number(status.departure_delay_seconds || 0) > 0 && <span className="font-normal text-amber-800">
              · {t("flightStatusDelay", { minutes: Math.round(Number(status.departure_delay_seconds) / 60) })}
            </span>}
          </p>}
        </> : <>
          <h3 className="mt-2 font-bold text-slate-900">{outbound ? copy.flightOutboundUnset : copy.flightReturnUnset}</h3>
          <p className="mt-1 text-sm leading-6 text-slate-600">{copy.flightAnchorHint}</p>
        </>}
      </div>
    </div>
    {search && <Link href={search.href} className="planner-flight-action">
      <Search size={15} />{t("searchFlights", { charge: search.charge })}
    </Link>}
    {flightStatus && configured && <Link href={flightStatus.href} className="planner-flight-action">
      <RadioTower size={15} />{t("statusSearch", { charge: flightStatus.charge })}
    </Link>}
    {onEdit && <button type="button" onClick={onEdit} disabled={busy} className="planner-flight-action">
      <Pencil size={15} />{configured ? copy.flightEdit : outbound ? copy.flightSetOutbound : copy.flightSetReturn}
    </button>}
    {/* The quote is the thing worth watching, so the alert lives with it rather than
        on the trip as a whole: this button tracks this flight's own offer. */}
    {quote && item.offer_id && <PriceAlertButton
      resourceType="flight"
      resourceId={item.offer_id}
      currentPrice={Number(quote.total_price)}
      currency={quote.currency}
      returnPath={alertReturnPath}
    />}
  </article>;
}
