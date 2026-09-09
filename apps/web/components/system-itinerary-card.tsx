import {
  BedDouble,
  Clock3,
  MapPin,
  RotateCcw,
  SkipForward,
  Utensils,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { formatTime, originalItemName, type ChainedStart, type TripItem } from "@/lib/trip-types";
import { DepartureTimeField } from "@/components/planner/departure-time-field";
import { calmEditCopy } from "@/components/planner/calm-edit-copy";
import { getStopTone, stopToneClassName, stopToneStyles } from "@/components/planner/stop-tone";

export function SystemItineraryCard({
  item,
  locale,
  timezone,
  busy,
  routeStale = false,
  chainedStart,
  departureTime,
  departureBusy = false,
  explicitDepartureSave = false,
  onDepartureTimeChange,
  onDepartureDirtyChange,
  onDepartureBusyChange,
  onEdit,
  onSkip,
}: {
  item: TripItem;
  locale: string;
  timezone?: string;
  busy: boolean;
  routeStale?: boolean;
  chainedStart?: ChainedStart;
  departureTime?: string;
  departureBusy?: boolean;
  explicitDepartureSave?: boolean;
  onDepartureTimeChange?: (value: string) => void | Promise<boolean | void>;
  onDepartureDirtyChange?: (dirty: boolean) => void;
  onDepartureBusyChange?: (busy: boolean) => void;
  onEdit: () => void;
  onSkip?: () => void;
}) {
  const t = useTranslations("trips.systemStop");
  const editor = useTranslations("trips.editor");
  const departureCopy = calmEditCopy(locale);
  const meal = item.system_role === "lunch" || item.system_role === "dinner";
  const hotel = item.system_role === "hotel_start" || item.system_role === "hotel_end";
  const label = item.system_role === "lunch"
    ? editor("slot.lunch")
    : item.system_role === "dinner"
      ? editor("slot.dinner")
      : item.system_role === "hotel_start"
        ? t("hotelStart")
        : t("hotelEnd");

  const unresolved = Boolean(item.data.needs_place_confirmation)
    || item.latitude == null
    || item.longitude == null;
  const unsetHotel = hotel && unresolved;
  const timeMode = item.fixed_time
    ? editor("fixedTimeAt", { time: formatTime(item.start_time, locale, timezone) })
    : chainedStart
      ? editor("chained", { kind: editor(chainedStart.estimated ? "chainedApprox" : "chainedExpected"), time: formatTime(chainedStart.start, locale, timezone) })
      : routeStale || !item.start_time
        ? editor("chainedPending")
        : editor("chained", { kind: editor("chainedExpected"), time: formatTime(item.start_time, locale, timezone) });
  return <article className={`planner-system-card ${stopToneClassName(item.system_role, "card", item.is_skipped)}`}
    data-stop-tone={getStopTone(item.system_role)} data-stop-skipped={item.is_skipped || undefined}>
    <div className="flex items-start gap-3">
      <span className="planner-system-icon">{meal ? <Utensils size={18} /> : <BedDouble size={18} />}</span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <p className={`${stopToneStyles.roleLabel} text-xs font-bold tracking-[.08em]`}>{label}</p>
          <span className="flex items-center gap-1 text-xs text-[var(--muted)]"><Clock3 size={13} />{timeMode}{meal && item.duration_minutes != null ? ` · ${editor("minutesShort", { minutes: item.duration_minutes })}` : ""}</span>
          {meal && item.is_skipped && <span className={stopToneStyles.statusBadge}>{t("skipped")}</span>}
        </div>
        <h3 className="mt-1.5 line-clamp-2 font-bold">{unsetHotel && item.title.includes("尚未設定飯店") ? t("hotelUnset") : item.title}</h3>
        {originalItemName(item) && <p className="mt-0.5 truncate text-sm text-[var(--muted)]" lang={item.names?.title?.original_locale}>{originalItemName(item)}</p>}
        {!unsetHotel && <p className="mt-1 flex items-start gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} className="mt-0.5 shrink-0" />{item.location_name || t(hotel ? "hotelUnset" : "restaurantUnset")}</p>}
        {meal && item.is_skipped
          ? <p className={`${stopToneStyles.status} mt-2 text-xs font-semibold`}>{t("skippedHint")}</p>
          : unresolved && <p className={`${stopToneStyles.status} mt-2 text-xs font-semibold`}>{t(unsetHotel ? "hotelHint" : "placeHint")}</p>}
      </div>
    </div>
    {item.system_role === "hotel_start" && departureTime && onDepartureTimeChange && (explicitDepartureSave
      ? <DepartureTimeField key={item.id} value={departureTime} locale={locale} busy={departureBusy}
        onSave={onDepartureTimeChange} onDirtyChange={onDepartureDirtyChange} onBusyChange={onDepartureBusyChange} />
      : <label className="planner-departure-field mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 border-t border-black/5 pt-3 text-xs font-semibold">
      <span className="flex items-center gap-1.5"><Clock3 size={14} />{departureCopy.departureTime}</span>
      <input type="time" aria-label={departureCopy.departureLabel} defaultValue={departureTime} key={departureTime} disabled={departureBusy} onBlur={(event) => { if (event.target.value && event.target.value !== departureTime) onDepartureTimeChange(event.target.value); }} onKeyDown={(event) => { if (event.key === "Enter") (event.target as HTMLInputElement).blur(); }} className="min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-2.5 font-bold disabled:opacity-45" />
      <span className="font-normal text-[var(--muted)]">{departureBusy ? departureCopy.saving : departureCopy.departureApplies}</span>
    </label>)}
    <div className="mt-3 flex gap-2 border-t border-black/5 pt-3">
      {meal && item.is_skipped
        ? <button type="button" onClick={onSkip} disabled={busy} className="planner-system-primary"><RotateCcw size={15} />{t("restore")}</button>
        : <>
          <button type="button" onClick={onEdit} disabled={busy} className="planner-system-primary">
            {hotel ? editor("setMainHotel") : t(unresolved ? "chooseRestaurant" : "changeRestaurant")}
          </button>
          {meal && <button type="button" onClick={onSkip} disabled={busy} className="planner-system-action">
            <SkipForward size={15} />{t("skip")}
          </button>}
        </>}
    </div>
  </article>;
}
