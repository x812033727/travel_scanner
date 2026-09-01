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
  onEdit,
  onSkip,
}: {
  item: TripItem;
  locale: string;
  timezone?: string;
  busy: boolean;
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

  if (meal && item.is_skipped) {
    return <article className="planner-system-card planner-system-card-skipped">
      <div className="flex min-w-0 items-center gap-3">
        <span className="planner-system-icon"><Utensils size={17} /></span>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-bold text-[var(--muted)]">{label}</p>
          <p className="mt-0.5 text-sm text-[var(--muted)]">已跳過，不計停留時間與路線</p>
        </div>
        <button type="button" onClick={onSkip} disabled={busy} className="planner-system-action">
          <RotateCcw size={15} />恢復
        </button>
      </div>
    </article>;
  }

  const unresolved = Boolean(item.data.needs_place_confirmation)
    || item.latitude == null
    || item.longitude == null;
  return <article className={`planner-system-card ${meal ? "planner-meal-card" : "planner-hotel-card"}`}>
    <div className="flex items-start gap-3">
      <span className="planner-system-icon">{meal ? <Utensils size={18} /> : <BedDouble size={18} />}</span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-xs font-bold tracking-[.08em]">{label}</p>
          {meal && <span className="flex items-center gap-1 text-xs text-[var(--muted)]"><Clock3 size={13} />{formatTime(item.start_time, locale, timezone)} · {item.duration_minutes} 分</span>}
        </div>
        <h3 className="mt-1.5 line-clamp-2 font-bold">{item.title}</h3>
        <p className="mt-1 flex items-start gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} className="mt-0.5 shrink-0" />{item.location_name || (hotel ? "尚未設定主要飯店" : "尚未選擇餐廳")}</p>
        {unresolved && <p className="mt-2 text-xs font-semibold text-amber-800">設定並確認地點後，才能計算完整路線</p>}
      </div>
    </div>
    <div className="mt-3 flex gap-2 border-t border-black/5 pt-3">
      <button type="button" onClick={onEdit} disabled={busy} className="planner-system-primary">
        {hotel ? "設定主要飯店" : unresolved ? "選擇餐廳" : "更換餐廳"}
      </button>
      {meal && <button type="button" onClick={onSkip} disabled={busy} className="planner-system-action">
        <SkipForward size={15} />跳過
      </button>}
    </div>
  </article>;
}
