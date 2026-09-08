import { isFlightAnchor, isLogisticsItem, type TripItem } from "@/lib/trip-types";

export type InsertionPoint = { day: string; beforeId?: string };

export function dayTimeline(items: TripItem[], day: string): TripItem[] {
  return items.filter((row) => row.day_date === day && !isLogisticsItem(row))
    .sort((a, b) => a.position - b.position);
}

/** The same gap identities power add, drag, keyboard move and cross-day move. */
export function insertionPoints(items: TripItem[], day: string, movingId?: string): InsertionPoint[] {
  const rows = dayTimeline(items, day).filter((row) => row.id !== movingId);
  const points: InsertionPoint[] = rows.filter((row) => !isFlightAnchor(row) && row.system_role !== "hotel_start")
    .map((row) => ({ day, beforeId: row.id }));
  if (!rows.some((row) => row.system_role === "hotel_end")) points.push({ day });
  return points;
}

export function normalizeOrder(items: TripItem[]): TripItem[] {
  const days = [...new Set(items.map((row) => row.day_date))].sort();
  return days.flatMap((day) => {
    const rows = items.filter((row) => row.day_date === day);
    const rank = (row: TripItem) => isLogisticsItem(row) ? 5
      : row.system_role === "outbound_flight" ? 0
        : row.system_role === "hotel_start" ? 1
          : row.system_role === "hotel_end" ? 3
            : row.system_role === "return_flight" ? 4 : 2;
    return rows.sort((a, b) => rank(a) - rank(b) || a.position - b.position)
      .map((row, position) => ({ ...row, position }));
  });
}

export function placeAt(items: TripItem[], item: TripItem, point: InsertionPoint): TripItem[] {
  const without = items.filter((row) => row.id !== item.id);
  const target = without.filter((row) => row.day_date === point.day).sort((a, b) => a.position - b.position);
  let at = point.beforeId ? target.findIndex((row) => row.id === point.beforeId) : -1;
  if (at < 0) at = target.findIndex((row) => row.system_role === "hotel_end" || row.system_role === "return_flight" || isLogisticsItem(row));
  if (at < 0) at = target.length;
  target.splice(at, 0, { ...item, day_date: point.day });
  return normalizeOrder([
    ...without.filter((row) => row.day_date !== point.day),
    ...target.map((row, position) => ({ ...row, position })),
  ]);
}

export function insertionNeighbors(items: TripItem[], point: InsertionPoint) {
  const rows = dayTimeline(items, point.day);
  const target = point.beforeId ? rows.findIndex((row) => row.id === point.beforeId) : rows.length;
  const at = target < 0 ? rows.length : target;
  const routable = (row: TripItem) => !isFlightAnchor(row) && !row.is_skipped;
  return {
    before: rows.slice(0, at).filter(routable).at(-1),
    after: rows.slice(at).find(routable),
    reference: rows.slice(0, at).filter(routable).reverse().find((row) => row.latitude != null && row.longitude != null)
      || rows.slice(at).filter(routable).find((row) => row.latitude != null && row.longitude != null),
  };
}
