import {
  BedDouble,
  Clock3,
  MapPin,
  RotateCcw,
  SkipForward,
  Utensils,
} from "lucide-react";
import { formatTime, originalItemName, type ChainedStart, type TripItem } from "@/lib/trip-types";

export function SystemItineraryCard({
  item,
  locale,
  timezone,
  busy,
  routeStale = false,
  chainedStart,
  departureTime,
  departureBusy = false,
  onDepartureTimeChange,
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
  onDepartureTimeChange?: (value: string) => void;
  onEdit: () => void;
  onSkip?: () => void;
}) {
  const meal = item.system_role === "lunch" || item.system_role === "dinner";
  const hotel = item.system_role === "hotel_start" || item.system_role === "hotel_end";
  const label = item.system_role === "lunch"
    ? "午餐"
    : item.system_role === "dinner"
      ? "晚餐"
      : item.system_role === "hotel_start"
        ? "住宿據點 · 出發"
        : "住宿據點 · 返回";

  const unresolved = Boolean(item.data.needs_place_confirmation)
    || item.latitude == null
    || item.longitude == null;
  const unsetHotel = hotel && unresolved;
  const timeMode = item.fixed_time
    ? `固定時間 · ${formatTime(item.start_time, locale, timezone)}`
    : chainedStart
      ? `接續前站 · ${chainedStart.estimated ? "約" : "預計"} ${formatTime(chainedStart.start, locale, timezone)}`
      : routeStale || !item.start_time
        ? "接續前站 · 待路線更新"
        : `接續前站 · 預計 ${formatTime(item.start_time, locale, timezone)}`;
  return <article className={`planner-system-card ${meal ? "planner-meal-card" : "planner-hotel-card"} ${meal && item.is_skipped ? "planner-system-card-skipped" : ""}`}>
    <div className="flex items-start gap-3">
      <span className="planner-system-icon">{meal ? <Utensils size={18} /> : <BedDouble size={18} />}</span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-xs font-bold tracking-[.08em]">{label}</p>
          <span className="flex items-center gap-1 text-xs text-[var(--muted)]"><Clock3 size={13} />{timeMode}{meal ? ` · ${item.duration_minutes} 分` : ""}</span>
          {meal && item.is_skipped && <span className="rounded-full bg-slate-200 px-2 py-1 text-[.68rem] font-extrabold text-slate-700">已跳過</span>}
        </div>
        <h3 className="mt-1.5 line-clamp-2 font-bold">{unsetHotel && item.title.includes("尚未設定飯店") ? "尚未設定主要飯店" : item.title}</h3>
        {originalItemName(item) && <p className="mt-0.5 truncate text-sm text-[var(--muted)]" lang={item.names?.title?.original_locale}>{originalItemName(item)}</p>}
        {!unsetHotel && <p className="mt-1 flex items-start gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} className="mt-0.5 shrink-0" />{item.location_name || (hotel ? "尚未設定主要飯店" : "尚未選擇餐廳")}</p>}
        {meal && item.is_skipped
          ? <p className="mt-2 text-xs font-semibold text-slate-600">已跳過，不計停留時間與路線</p>
          : unresolved && <p className="mt-2 text-xs font-semibold text-amber-800">{unsetHotel ? "設定一次後，會建立每天的出發與返回路線" : "設定並確認地點後，才能計算完整路線"}</p>}
      </div>
    </div>
    {item.system_role === "hotel_start" && departureTime && onDepartureTimeChange && <label className="planner-departure-field mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 border-t border-black/5 pt-3 text-xs font-semibold">
      <span className="flex items-center gap-1.5"><Clock3 size={14} />出發時間</span>
      <input type="time" aria-label="每天從飯店出發的時間" defaultValue={departureTime} key={departureTime} disabled={departureBusy} onBlur={(event) => { if (event.target.value && event.target.value !== departureTime) onDepartureTimeChange(event.target.value); }} onKeyDown={(event) => { if (event.key === "Enter") (event.target as HTMLInputElement).blur(); }} className="min-h-10 rounded-xl border border-[var(--line)] bg-white px-2.5 font-bold disabled:opacity-45" />
      <span className="font-normal text-[var(--muted)]">{departureBusy ? "儲存中…" : "套用到每一天"}</span>
    </label>}
    <div className="mt-3 flex gap-2 border-t border-black/5 pt-3">
      {meal && item.is_skipped
        ? <button type="button" onClick={onSkip} disabled={busy} className="planner-system-primary"><RotateCcw size={15} />恢復</button>
        : <>
          <button type="button" onClick={onEdit} disabled={busy} className="planner-system-primary">
            {hotel ? "設定主要飯店" : unresolved ? "選擇餐廳" : "更換餐廳"}
          </button>
          {meal && <button type="button" onClick={onSkip} disabled={busy} className="planner-system-action">
            <SkipForward size={15} />跳過
          </button>}
        </>}
    </div>
  </article>;
}
