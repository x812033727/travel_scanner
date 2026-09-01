import {
  BedDouble,
  Clock3,
  MapPin,
  RotateCcw,
  SkipForward,
  Utensils,
} from "lucide-react";
import { formatTime, type TripItem } from "@/lib/trip-types";

export function SystemItineraryCard({
  item,
  locale,
  timezone,
  busy,
  routeStale = false,
  onEdit,
  onSkip,
}: {
  item: TripItem;
  locale: string;
  timezone?: string;
  busy: boolean;
  routeStale?: boolean;
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
  const timeMode = item.fixed_time
    ? `固定時間 · ${formatTime(item.start_time, locale, timezone)}`
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
        <h3 className="mt-1.5 line-clamp-2 font-bold">{item.title}</h3>
        <p className="mt-1 flex items-start gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} className="mt-0.5 shrink-0" />{item.location_name || (hotel ? "尚未設定主要飯店" : "尚未選擇餐廳")}</p>
        {meal && item.is_skipped
          ? <p className="mt-2 text-xs font-semibold text-slate-600">已跳過，不計停留時間與路線</p>
          : unresolved && <p className="mt-2 text-xs font-semibold text-amber-800">設定並確認地點後，才能計算完整路線</p>}
      </div>
    </div>
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
