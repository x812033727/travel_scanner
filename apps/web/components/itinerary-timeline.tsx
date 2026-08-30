import { CalendarDays, Clock3, LockKeyhole, MapPin, Sparkles } from "lucide-react";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { formatTime, groupTripItems, type RouteSegment, type TripItem } from "@/lib/trip-types";

const dayFormatter = new Intl.DateTimeFormat("zh-TW", {
  month: "long",
  day: "numeric",
  weekday: "short",
  timeZone: "UTC",
});

export function ItineraryTimeline({ items, routes = [] }: { items: TripItem[]; routes?: RouteSegment[] }) {
  return <div className="space-y-6">{groupTripItems(items).map(([day, rows], dayIndex) => <section key={day} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-6">
    <div className="mb-5 flex items-center justify-between gap-3"><div><p className="text-xs font-semibold uppercase tracking-[.16em] text-[var(--teal)]">DAY {dayIndex + 1}</p><h2 className="mt-1 flex items-center gap-2 text-xl font-bold"><CalendarDays size={19} />{dayFormatter.format(new Date(`${day}T00:00:00Z`))}</h2></div><span className="text-xs text-[var(--muted)]">{rows.length} 個安排</span></div>
    <ol className="relative space-y-3 before:absolute before:bottom-4 before:left-[1.15rem] before:top-4 before:w-px before:bg-[var(--line)]">{rows.map((item, index) => { const route = routes.find((segment) => segment.from_item_id === item.id && segment.to_item_id === rows[index + 1]?.id); return <li key={item.id}><div className="relative grid grid-cols-[2.3rem_1fr] gap-3"><span className={`z-10 mt-3 grid h-9 w-9 place-items-center rounded-full ${item.is_estimated ? "bg-amber-100 text-amber-800" : "bg-[var(--teal-soft)] text-[var(--teal)]"}`}>{item.is_estimated ? <Sparkles size={16} /> : <Clock3 size={16} />}</span><div className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"><div className="flex flex-wrap items-start justify-between gap-2"><div><p className="text-xs font-semibold text-[var(--muted)]">{formatTime(item.start_time)}{item.end_time ? `–${formatTime(item.end_time)}` : ""}</p><h3 className="mt-1 font-semibold">{item.title}</h3></div><div className="flex gap-2">{item.locked && <span title="固定項目" className="rounded-full bg-white p-1.5 text-[var(--teal)]"><LockKeyhole size={14} /></span>}{item.is_estimated && <span className="rounded-full bg-amber-100 px-2 py-1 text-[.68rem] font-semibold text-amber-900">估算</span>}</div></div>{item.location_name && <p className="mt-2 flex items-center gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} />{item.location_name}</p>}</div></div>{route && <div className="mt-3"><RouteSegmentCard segment={route} /></div>}</li>; })}</ol>
  </section>)}</div>;
}
