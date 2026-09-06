import { ArrowRight, Clock3, Pencil, Plane, RouteOff, Tag } from "lucide-react";
import { useTranslations } from "next-intl";
import { formatCurrency } from "@/lib/locale-format";
import { priceSnapshot, type TripItem } from "@/lib/trip-types";

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

function localDateTime(value?: string) {
  if (!value) return "時間待設定";
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  if (!match) return value;
  return `${Number(match[2])}/${Number(match[3])} ${match[4]}:${match[5]}`;
}

export function FlightAnchorCard({
  item,
  busy = false,
  onEdit,
}: {
  item: TripItem;
  busy?: boolean;
  onEdit?: () => void;
}) {
  const t = useTranslations("trips");
  const info = flightAnchorInfo(item);
  const outbound = item.system_role === "outbound_flight";
  const label = outbound ? "去程航班" : "回程航班";
  const configuredInfo = info?.airline && info.flight_number ? info : null;
  const configured = Boolean(configuredInfo);
  const departureTimezone = info?.departure_timezone || "時區待確認";
  const arrivalTimezone = info?.arrival_timezone || "時區待確認";
  // The quote the anchor was created from. A hand-typed flight never carries one,
  // so the line only appears on anchors that came out of a real search.
  const quote = configuredInfo ? priceSnapshot(item) : null;

  return <article className="planner-flight-card">
    <div className="flex items-start gap-3">
      <span className="planner-flight-icon"><Plane size={19} /></span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-xs font-bold tracking-[.08em] text-sky-900">{label}</p>
          <span className="planner-flight-badge"><Clock3 size={12} />固定時間</span>
          <span className="planner-flight-badge"><RouteOff size={12} />不計入市區路線</span>
        </div>
        {configuredInfo ? <>
          <h3 className="mt-2 text-lg font-bold text-slate-900">{configuredInfo.airline} {configuredInfo.flight_number}</h3>
          <div className="mt-3 grid grid-cols-[1fr_auto_1fr] items-center gap-2 rounded-xl bg-white/70 p-3">
            <div>
              <p className="text-lg font-black text-slate-900">{configuredInfo.origin}</p>
              <p className="mt-0.5 text-sm font-semibold text-slate-700">{localDateTime(configuredInfo.departure_local)}</p>
              <p className={`mt-1 text-xs ${configuredInfo.departure_timezone ? "text-slate-500" : "font-semibold text-amber-700"}`}>{departureTimezone}</p>
            </div>
            <ArrowRight size={18} className="text-sky-600" />
            <div className="text-right">
              <p className="text-lg font-black text-slate-900">{configuredInfo.destination}</p>
              <p className="mt-0.5 text-sm font-semibold text-slate-700">{localDateTime(configuredInfo.arrival_local)}</p>
              <p className={`mt-1 text-xs ${configuredInfo.arrival_timezone ? "text-slate-500" : "font-semibold text-amber-700"}`}>{arrivalTimezone}</p>
            </div>
          </div>
          {typeof configuredInfo.stops === "number" && <p className="mt-2 text-xs text-slate-600">{configuredInfo.stops === 0 ? "直飛" : `${configuredInfo.stops} 次轉機`}</p>}
          {quote && <p className="mt-2 flex flex-wrap items-center gap-1.5 text-xs font-semibold text-sky-900">
            <Tag size={13} aria-hidden />
            {t("quotedPrice", { amount: formatCurrency(Number(quote.total_price), quote.currency) })}
            {quote.provider && <span className="font-normal text-slate-600">· {t("quotedBy", { provider: quote.provider })}</span>}
          </p>}
        </> : <>
          <h3 className="mt-2 font-bold text-slate-900">{label}尚未設定</h3>
          <p className="mt-1 text-sm leading-6 text-slate-600">補上航空公司、班號、機場與當地起降時間，同行者就能在行程首尾清楚確認。</p>
        </>}
      </div>
    </div>
    {onEdit && <button type="button" onClick={onEdit} disabled={busy} className="planner-flight-action">
      <Pencil size={15} />{configured ? "編輯航班" : `設定${label}`}
    </button>}
  </article>;
}
