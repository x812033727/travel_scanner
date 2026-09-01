import {
  BedDouble,
  CalendarDays,
  Clock3,
  Info,
  LockKeyhole,
  MapPin,
  Sparkles,
  Utensils,
} from "lucide-react";
import { FlightAnchorCard } from "@/components/flight-anchor-card";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { activeLocale } from "@/lib/locale-format";
import {
  formatTime,
  groupTripItems,
  isActiveRouteItem,
  isFlightAnchor,
  isLogisticsItem,
  type RouteSegment,
  type TripItem,
} from "@/lib/trip-types";

function systemLabel(item: TripItem) {
  if (item.system_role === "lunch") return "午餐";
  if (item.system_role === "dinner") return "晚餐";
  if (item.system_role === "hotel_start") return "從飯店出發";
  return "返回飯店";
}

export function ItineraryTimeline({
  items,
  routes = [],
  timezone,
}: {
  items: TripItem[];
  routes?: RouteSegment[];
  timezone?: string;
}) {
  const dayFormatter = new Intl.DateTimeFormat(activeLocale(), {
    month: "long",
    day: "numeric",
    weekday: "short",
    timeZone: "UTC",
  });
  const visibleItems = items.filter((item) => !item.is_skipped);
  const logistics = visibleItems.filter(isLogisticsItem);
  const dailyItems = visibleItems.filter((item) => !isLogisticsItem(item));

  return (
    <div className="space-y-6">
      {logistics.length > 0 && (
        <section className="rounded-[1.75rem] border border-slate-200 bg-slate-50/80 p-5 md:p-6">
          <div className="flex items-start gap-3">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-white text-slate-600">
              <Info size={18} />
            </span>
            <div>
              <h2 className="font-bold text-slate-900">交通與住宿資訊</h2>
              <p className="mt-1 text-xs leading-5 text-slate-600">
                接送與入住退房資訊獨立保存，不加入每日外出路線。
              </p>
            </div>
          </div>
          <div className="mt-4 grid gap-2 md:grid-cols-2">
            {logistics.map((item) => (
              <article key={item.id} className="rounded-2xl border border-slate-200 bg-white p-4">
                <p className="text-xs font-semibold text-slate-500">
                  {item.day_date} · {formatTime(item.start_time, undefined, timezone)}
                </p>
                <h3 className="mt-1 font-semibold">{item.title}</h3>
                {item.location_name && <p className="mt-1 text-sm text-slate-600">{item.location_name}</p>}
              </article>
            ))}
          </div>
        </section>
      )}

      {groupTripItems(dailyItems).map(([day, rows], dayIndex) => {
        const arrangementCount = rows.filter((item) =>
          !isFlightAnchor(item) && !item.system_role?.startsWith("hotel_"),
        ).length;
        const routeRows = rows.filter(isActiveRouteItem);
        return (
          <section
            key={day}
            className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-6"
          >
            <div className="mb-5 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[.16em] text-[var(--teal)]">
                  DAY {dayIndex + 1}
                </p>
                <h2 className="mt-1 flex items-center gap-2 text-xl font-bold">
                  <CalendarDays size={19} />
                  {dayFormatter.format(new Date(`${day}T00:00:00Z`))}
                </h2>
              </div>
              <span className="text-xs text-[var(--muted)]">{arrangementCount} 個安排</span>
            </div>
            <ol className="relative space-y-3">
              {rows.map((item) => {
                if (isFlightAnchor(item)) {
                  return <li key={item.id}><FlightAnchorCard item={item} /></li>;
                }
                const routeIndex = routeRows.findIndex((row) => row.id === item.id);
                const nextItem = routeIndex >= 0 ? routeRows[routeIndex + 1] : undefined;
                const route = routes.find(
                  (segment) =>
                    segment.from_item_id === item.id
                    && segment.to_item_id === nextItem?.id,
                );
                const incomingRoute = routes.find((segment) => segment.to_item_id === item.id);
                const meal = item.system_role === "lunch" || item.system_role === "dinner";
                const hotel = item.system_role === "hotel_start" || item.system_role === "hotel_end";
                const timeMode = item.fixed_time
                  ? `固定時間 · ${formatTime(item.start_time, undefined, timezone)}`
                  : incomingRoute
                    ? `接續前站 · 預計 ${formatTime(item.start_time, undefined, timezone)}`
                    : "接續前站 · 待路線更新";
                return (
                  <li key={item.id}>
                    <div className="relative grid grid-cols-[2.3rem_1fr] gap-3">
                      <span className={`z-10 mt-3 grid h-9 w-9 place-items-center rounded-full ${meal ? "bg-amber-100 text-amber-800" : hotel ? "bg-slate-100 text-slate-700" : item.is_estimated ? "bg-amber-100 text-amber-800" : "bg-[var(--teal-soft)] text-[var(--teal)]"}`}>
                        {meal ? <Utensils size={16} /> : hotel ? <BedDouble size={16} /> : item.is_estimated ? <Sparkles size={16} /> : <Clock3 size={16} />}
                      </span>
                      <div className={`rounded-2xl border p-4 ${meal ? "border-amber-200 bg-amber-50/70" : hotel ? "border-slate-200 bg-slate-50/80" : "border-[var(--line)] bg-[var(--paper)]"}`}>
                        <div className="flex flex-wrap items-start justify-between gap-2">
                          <div>
                            <p className="text-xs font-semibold text-[var(--muted)]">
                              {item.system_role ? `${systemLabel(item)} · ` : ""}{timeMode}
                              {item.fixed_time && item.end_time ? `–${formatTime(item.end_time, undefined, timezone)}` : ""}
                            </p>
                            <h3 className="mt-1 font-semibold">{item.title}</h3>
                          </div>
                          <div className="flex gap-2">
                            {item.locked && !item.system_role && (
                              <span title="固定項目" className="rounded-full bg-white p-1.5 text-[var(--teal)]">
                                <LockKeyhole size={14} />
                              </span>
                            )}
                            {item.is_estimated && !item.system_role && (
                              <span className="rounded-full bg-amber-100 px-2 py-1 text-[.68rem] font-semibold text-amber-900">估算</span>
                            )}
                          </div>
                        </div>
                        <p className="mt-2 flex items-center gap-1.5 text-sm text-[var(--muted)]">
                          <MapPin size={14} />
                          {item.location_name || (hotel ? "尚未設定主要飯店" : meal ? "待選餐廳" : "尚未設定地點")}
                        </p>
                      </div>
                    </div>
                    {routeIndex >= 0 && nextItem && route && <div className="mt-3"><RouteSegmentCard segment={route} timezone={timezone} /></div>}
                  </li>
                );
              })}
            </ol>
          </section>
        );
      })}
    </div>
  );
}
