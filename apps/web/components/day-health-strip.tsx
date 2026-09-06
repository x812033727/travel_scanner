"use client";

import { Clock3, DoorClosed, RouteOff } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type LateConflict = { item_id: string; title: string; late_minutes: number };
type ClosedStop = { item_id: string; title: string; start_time: string; opens_at?: string | null };
export type DayHealth = { date: string; late: LateConflict[]; closed: ClosedStop[]; unrouted: number };

/**
 * What the traveller cannot see by reading their own day.
 *
 * Everything shown here comes from data already stored — the projected schedule, the
 * cached opening hours, the segments that exist — so the strip costs no provider
 * request. A stop whose hours we do not have is simply absent: one "closed" shown for a
 * place that is open would cost every other warning its credibility.
 */
export function DayHealthStrip({
  tripId,
  day,
  revision,
  onSelectItem,
}: {
  tripId: string;
  day?: string;
  revision?: number;
  onSelectItem?: (itemId: string) => void;
}) {
  const t = useTranslations("trips.health");
  const [days, setDays] = useState<DayHealth[]>([]);

  useEffect(() => {
    let active = true;
    api<{ days: DayHealth[] }>(`/trips/${tripId}/health`)
      // A partial payload must not take the day view down with it.
      .then((value) => { if (active) setDays(Array.isArray(value?.days) ? value.days : []); })
      .catch(() => undefined);
    return () => { active = false; };
  }, [tripId, revision]);

  const health = days.find((entry) => entry.date === day);
  if (!day || !health) return null;
  const warnings = health.late.length + health.closed.length + (health.unrouted > 0 ? 1 : 0);
  if (warnings === 0) return null;

  return <section aria-label={t("label")} className="mb-3 flex flex-wrap gap-2 text-xs">
    {health.late.map((conflict) => <button
      key={`late-${conflict.item_id}`}
      type="button"
      onClick={() => onSelectItem?.(conflict.item_id)}
      className="flex min-h-9 items-center gap-1.5 rounded-full bg-amber-50 px-3 font-semibold text-amber-900"
    >
      <Clock3 size={14} />{t("late", { title: conflict.title, minutes: conflict.late_minutes })}
    </button>)}
    {health.closed.map((stop) => <button
      key={`closed-${stop.item_id}`}
      type="button"
      onClick={() => onSelectItem?.(stop.item_id)}
      className="flex min-h-9 items-center gap-1.5 rounded-full bg-red-50 px-3 font-semibold text-red-900"
    >
      <DoorClosed size={14} />
      {stop.opens_at
        ? t("closedUntil", { title: stop.title, time: stop.opens_at })
        : t("closed", { title: stop.title })}
    </button>)}
    {health.unrouted > 0 && <span className="flex min-h-9 items-center gap-1.5 rounded-full bg-[var(--paper)] px-3 font-semibold text-[var(--muted)]">
      <RouteOff size={14} />{t("unrouted", { count: health.unrouted })}
    </span>}
  </section>;
}
