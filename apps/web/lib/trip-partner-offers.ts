import type { AffiliateModule } from "@/components/affiliate-partner-options";
import { isFlightAnchor, type TripItem } from "@/lib/trip-types";

/**
 * Which partner modules a day of the trip can honestly end with.
 *
 * The day that holds the outbound flight is the arrival day: what a traveller needs
 * there is the ride from the airport and a way online (and a hotel, if none is set).
 * The day that holds the return flight is the departure day: only the ride back. Every
 * other day is about what to do there. A trip without dates or flights falls back to
 * its first and last day, and a single-day trip counts as arrival.
 */
export type DayPartnerKind = "arrival" | "departure" | "day";

/** Fixed canonical order, the same the destination panel uses, never commission-shaped. */
const MODULE_ORDER: readonly AffiliateModule[] = ["flight", "hotel", "activities", "transport", "connectivity"];

function dayOf(items: readonly TripItem[], role: "outbound_flight" | "return_flight"): string | undefined {
  return items.find((item) => isFlightAnchor(item) && item.system_role === role)?.day_date ?? undefined;
}

export function dayPartnerKind(day: string, days: readonly string[], items: readonly TripItem[]): DayPartnerKind {
  const arrival = dayOf(items, "outbound_flight") ?? days[0];
  if (day === arrival) return "arrival";
  const departure = dayOf(items, "return_flight") ?? days[days.length - 1];
  if (day === departure) return "departure";
  return "day";
}

function intersect(wanted: readonly AffiliateModule[], available: readonly AffiliateModule[]): AffiliateModule[] {
  const ready = new Set(available);
  return MODULE_ORDER.filter((module) => wanted.includes(module) && ready.has(module));
}

export function dayPartnerModules(
  kind: DayPartnerKind,
  { lodgingReady, available }: { lodgingReady: boolean; available: readonly AffiliateModule[] },
): AffiliateModule[] {
  if (kind === "arrival") return intersect(lodgingReady ? ["transport", "connectivity"] : ["hotel", "transport", "connectivity"], available);
  if (kind === "departure") return intersect(["transport"], available);
  return intersect(["activities"], available);
}

/** After an AI plan lands: tickets for the new stops, plus the arrival logistics when the plan covered day one. */
export function afterAiPartnerModules(
  scope: "day" | "trip",
  kind: DayPartnerKind,
  available: readonly AffiliateModule[],
): AffiliateModule[] {
  const wanted: AffiliateModule[] = scope === "trip" || kind === "arrival"
    ? ["activities", "transport", "connectivity"]
    : ["activities"];
  return intersect(wanted, available);
}
