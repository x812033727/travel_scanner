import { activeLocale } from "@/lib/locale-format";

/**
 * One label per site locale plus the text in the place's own script
 * (`original`, tagged with `original_locale`). The API resolves `title` and
 * `location_name` for the request locale; this map lets the UI show the
 * original next to it.
 */
export type LocalizedNames = Partial<Record<"en" | "ja" | "ko" | "zh-TW" | "zh-CN", string>> & {
  original?: string;
  original_locale?: string;
};

export type TripItemNames = {
  title?: LocalizedNames;
  location_name?: LocalizedNames;
};

export type TripItem = {
  id: string;
  item_type: string;
  offer_id?: string | null;
  day_date: string;
  position: number;
  title: string;
  location_name?: string | null;
  /** Catalog-backed stops only; empty for free-text rows and after a manual rename. */
  names?: TripItemNames;
  start_time?: string | null;
  end_time?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  locked: boolean;
  is_estimated: boolean;
  data: Record<string, unknown>;
  provider_place_id?: string | null;
  location_source?: string | null;
  location_provider?: string | null;
  duration_minutes?: number | null;
  notes?: string | null;
  fixed_time?: boolean;
  system_role?: "outbound_flight" | "hotel_start" | "lunch" | "dinner" | "hotel_end" | "return_flight" | null;
  is_skipped?: boolean;
};

export type PrimaryLodging = {
  name: string;
  location_name: string;
  provider_place_id?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  location_source: string;
  offer_id?: string | null;
  provider?: string | null;
  hotel_id?: string | null;
  area_code?: string | null;
  selection_source?: "user" | "reoptimize" | null;
  selected_at?: string | null;
  price_snapshot?: {
    nightly_price?: number | string | null;
    total_price?: number | string | null;
    currency?: string | null;
    nights?: number | null;
    retrieved_at?: string | null;
    expires_at?: string | null;
  } | null;
};

export type ScheduleDefaults = {
  day_start_time: string;
  lunch_time: string;
  lunch_duration_minutes: number;
  dinner_time: string;
  dinner_duration_minutes: number;
};

export type RouteStep = {
  travel_mode: string;
  instruction: string;
  duration_minutes?: number | null;
  distance_meters?: number | null;
  departure_stop?: string | null;
  arrival_stop?: string | null;
  departure_time?: string | null;
  arrival_time?: string | null;
  line_name?: string | null;
  line_short_name?: string | null;
  line_color?: string | null;
  headsign?: string | null;
  stop_count?: number | null;
  platform?: string | null;
  exit_name?: string | null;
  recommended_car?: string | null;
};

export type TravelMode = "transit" | "walk" | "drive";

export type RouteScheduleChange = {
  item_id: string;
  title: string;
  old_start_time?: string | null;
  new_start_time?: string | null;
  delta_minutes: number;
  fixed_time: boolean;
};

export type RouteScheduleConflict = {
  item_id: string;
  title: string;
  scheduled_start_time: string;
  projected_start_time: string;
  late_minutes: number;
  suggestions: string[];
};

export type RouteScheduleImpact = {
  affected_items: RouteScheduleChange[];
  conflicts: RouteScheduleConflict[];
};

export type RouteSegment = {
  from_item_id: string;
  to_item_id: string;
  status: string;
  travel_mode?: TravelMode;
  is_override?: boolean;
  provider: string;
  attribution: string;
  generated_at: string;
  requested_departure_time?: string | null;
  schedule_mode: "scheduled" | "preview" | "live";
  preference: string;
  duration_minutes: number;
  buffer_minutes?: number;
  departure_time?: string | null;
  arrival_time?: string | null;
  ready_time?: string | null;
  expires_at?: string | null;
  distance_meters?: number | null;
  fare?: number | string | null;
  currency?: string | null;
  encoded_polyline?: string | null;
  maps_url?: string | null;
  provider_route_key?: string | null;
  route_option_rank?: number | null;
  steps: RouteStep[];
  details_available: string[];
  warnings: string[];
};

export type TripRouteDaySetting = {
  day_date: string;
  default_travel_mode: TravelMode;
  default_buffer_minutes: number;
  route_preference: "FEWER_TRANSFERS" | "LESS_WALKING" | "FASTEST";
  auto_compute: boolean;
};

export type TripRouting = {
  status: "idle" | "queued" | "processing" | "complete" | "partial" | "failed" | "stale" | "unavailable" | "needs_locations";
  total: number;
  completed: number;
  warnings?: string[];
  unresolved_items?: Array<{ item_id: string; title: string; reason: string }>;
  conflicts?: RouteScheduleConflict[];
  updated_at?: string;
  day_settings: TripRouteDaySetting[];
};

export type PriceSnapshot = {
  total_price: string;
  currency: string;
  provider?: string | null;
  source_mode?: string | null;
  retrieved_at?: string | null;
  expires_at?: string | null;
  nightly_price?: string | null;
  nights?: number | null;
};

export type TripPricingItem = PriceSnapshot & {
  kind: "flight" | "hotel";
  role: string;
  item_id: string | null;
  title?: string | null;
  offer_id?: string | null;
  counted: boolean;
};

export type TripPricing = {
  currency: string;
  quoted_total: string;
  estimated_total: string | null;
  items: TripPricingItem[];
  unsummed_currencies: string[];
};

export type TripOptimizationSummary = {
  movable_limit: number;
  days: Array<{ date: string; movable_count: number }>;
};

export function priceSnapshot(item: TripItem): PriceSnapshot | null {
  const value = item.data.price_snapshot;
  if (!value || typeof value !== "object") return null;
  const snapshot = value as Partial<PriceSnapshot>;
  return typeof snapshot.total_price === "string" && typeof snapshot.currency === "string"
    ? (snapshot as PriceSnapshot)
    : null;
}

export type TripStatus = "planning" | "ready" | "travelling" | "closed";

export type TripRescheduleSummary = {
  removed_days: string[];
  removed_item_count: number;
  removed_protected: Array<{ kind: "activity" | "chosen_meal" | "booked_flight"; title: string; day_date: string }>;
  invalidated_flight_anchors: number;
  route_segments_cleared: number;
};

export type TripExpenseCategory =
  | "flight"
  | "lodging"
  | "transport"
  | "food"
  | "activity"
  | "shopping"
  | "other";

export type TripExpense = {
  id: string;
  day_date: string;
  label: string;
  /** Decimal string: the ledger must not round-trip through a float. */
  amount: string;
  category: TripExpenseCategory;
  source: "manual" | "seeded";
  source_key: string | null;
  position: number;
};

export type TripCost = {
  currency: string;
  budget: string | null;
  total: string;
  /** Budget minus spend, so negative means over. Null without a budget. */
  difference: string | null;
  by_day: Record<string, string>;
  by_category: Record<string, string>;
  items: TripExpense[];
};

export type Trip = {
  id: string;
  name: string;
  status?: TripStatus;
  cover_image_url?: string | null;
  mode: string;
  total_price: number;
  currency: string;
  data: Record<string, unknown>;
  primary_lodging?: PrimaryLodging | null;
  pricing?: TripPricing | null;
  optimization?: TripOptimizationSummary | null;
  schedule_defaults?: ScheduleDefaults;
  planning?: {
    status: "live" | "fallback" | "partial";
    readiness?: "ready" | "partial" | "needs_setup" | "fallback";
    provider: "openai" | "anthropic" | "minimax" | "catalog";
    model?: string | null;
    generated_at: string;
    warnings: string[];
    exact_item_count?: number;
    candidate_count?: number;
    unscheduled_slots?: Array<{ date: string; slot: "activity" | "lunch" | "dinner" }>;
    scope?: "day" | "trip";
    day_date?: string | null;
  } | null;
  version: number;
  destination_name?: string | null;
  destination_country_code?: string | null;
  destination_place_id?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  timezone?: string;
  route_preference?: "FEWER_TRANSFERS" | "LESS_WALKING" | "FASTEST";
  notes?: string | null;
  /** Keyed by ISO day; days with nothing written have no entry. */
  day_notes?: Record<string, string>;
  /** Absent on list payloads, which do not carry items either. */
  cost?: TripCost | null;
  items: TripItem[];
  route_segments?: RouteSegment[];
  routing?: TripRouting;
  share_enabled?: boolean;
  created_at?: string;
  updated_at?: string;
  usage?: { status: "reserved" | "charged" | "released"; uses: number; reference: string };
  /** Present only on the response of a date-changing PATCH /trips/{id}. */
  reschedule?: TripRescheduleSummary;
};

export function formatTime(value?: string | null, locale?: string, timeZone?: string) {
  if (!value) return "彈性時段";
  const localWallClock = value.match(
    /^\d{4}-\d{2}-\d{2}T(\d{2}):(\d{2})(?::\d{2}(?:\.\d+)?)?$/,
  );
  if (localWallClock) return `${localWallClock[1]}:${localWallClock[2]}`;
  return new Intl.DateTimeFormat(locale || activeLocale(), {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone,
  }).format(new Date(value));
}

/** The stop's name in its own script when it differs from the label on show. */
export function originalItemName(item: Pick<TripItem, "title" | "names">) {
  const original = item.names?.title?.original?.trim();
  return original && original !== item.title.trim() ? original : null;
}

export function groupTripItems(items: TripItem[]) {
  const grouped = new Map<string, TripItem[]>();
  for (const item of [...items].sort((a, b) => a.day_date.localeCompare(b.day_date) || a.position - b.position)) {
    grouped.set(item.day_date, [...(grouped.get(item.day_date) || []), item]);
  }
  return [...grouped.entries()];
}

export function isLogisticsItem(item: TripItem) {
  return !item.system_role && (
    ["flight", "transport", "hotel"].includes(item.item_type)
    || item.data.timeline_section === "logistics"
  );
}

export function isFlightAnchor(item: TripItem): item is TripItem & {
  system_role: "outbound_flight" | "return_flight";
} {
  return item.system_role === "outbound_flight" || item.system_role === "return_flight";
}

export function isActiveRouteItem(item: TripItem) {
  const systemLocationReady = item.latitude != null && item.longitude != null;
  return !item.is_skipped
    && !isFlightAnchor(item)
    && !isLogisticsItem(item)
    && (!["hotel_start", "hotel_end", "lunch", "dinner"].includes(item.system_role || "") || systemLocationReady);
}

export type ChainedStart = { start: string; estimated: boolean };

const EARTH_RADIUS_KM = 6371;

/** Great-circle distance between two stops, or undefined when either has no coordinates. */
export function distanceKm(
  from: Pick<TripItem, "latitude" | "longitude">,
  to: Pick<TripItem, "latitude" | "longitude">,
): number | undefined {
  if (from.latitude == null || from.longitude == null || to.latitude == null || to.longitude == null) {
    return undefined;
  }
  const toRadians = (degrees: number) => (degrees * Math.PI) / 180;
  const deltaLatitude = toRadians(to.latitude - from.latitude);
  const deltaLongitude = toRadians(to.longitude - from.longitude);
  const halfChord = Math.sin(deltaLatitude / 2) ** 2
    + Math.cos(toRadians(from.latitude)) * Math.cos(toRadians(to.latitude)) * Math.sin(deltaLongitude / 2) ** 2;
  return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(halfChord));
}

/**
 * A rough travel time for a leg nobody has queried yet, so the timeline keeps a
 * believable running total without spending a provider request. Straight-line
 * distance at a modest speed plus a fixed overhead for transit and driving, rounded
 * up to five minutes; undefined when a stop has no coordinates.
 */
export function estimateLegMinutes(
  from: Pick<TripItem, "latitude" | "longitude">,
  to: Pick<TripItem, "latitude" | "longitude">,
  mode: TravelMode,
): number | undefined {
  const km = distanceKm(from, to);
  if (km === undefined) return undefined;
  const minutes = mode === "walk"
    ? (km / 4.5) * 60
    : mode === "drive"
      ? 5 + (km / 30) * 60
      : 10 + (km / 20) * 60;
  return Math.max(5, Math.ceil(minutes / 5) * 5);
}

function pairKey(from: string, to: string) {
  return `${from}->${to}`;
}

/** Every routable adjacent pair, per day and in display order, as `from->to` keys. */
export function adjacentPairKeys(rows: TripItem[]): Set<string> {
  const keys = new Set<string>();
  for (const [, dayRows] of groupTripItems(rows)) {
    const routable = dayRows.filter(isActiveRouteItem);
    for (let index = 0; index + 1 < routable.length; index += 1) {
      keys.add(pairKey(routable[index].id, routable[index + 1].id));
    }
  }
  return keys;
}

/**
 * Keep only the segments whose stops are still adjacent in `rows`. A reorder only
 * invalidates the legs around the moved stop; the server deletes the same pairs.
 */
export function segmentsForRows(segments: RouteSegment[], rows: TripItem[]): RouteSegment[] {
  const keys = adjacentPairKeys(rows);
  return segments.filter((segment) => keys.has(pairKey(segment.from_item_id, segment.to_item_id)));
}

/** How many routable adjacent pairs in `rows` have no segment yet. */
export function missingSegmentCount(rows: TripItem[], segments: RouteSegment[]): number {
  const covered = new Set(segments.map((segment) => pairKey(segment.from_item_id, segment.to_item_id)));
  let missing = 0;
  for (const key of adjacentPairKeys(rows)) {
    if (!covered.has(key)) missing += 1;
  }
  return missing;
}

const wallClockPattern = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::\d{2}(?:\.\d+)?)?$/;

function readMoment(value?: string | null) {
  if (!value) return undefined;
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) return undefined;
  return { ms: parsed, wallClock: wallClockPattern.test(value) };
}

function writeMoment(ms: number, wallClock: boolean) {
  if (!wallClock) return new Date(ms).toISOString();
  const local = new Date(ms);
  const pad = (part: number) => String(part).padStart(2, "0");
  return `${local.getFullYear()}-${pad(local.getMonth() + 1)}-${pad(local.getDate())}T${pad(local.getHours())}:${pad(local.getMinutes())}`;
}

/**
 * Walk a day in display order and work out when each chained item can start.
 *
 * A routed segment gives the real `ready_time`; without one we still show the member
 * a running total — previous item's end, a distance-based travel estimate when both
 * stops have coordinates, plus the day's transfer buffer — flagged as an estimate so
 * it reads differently from a computed route.
 */
export function projectChainedStarts(
  rows: TripItem[],
  segments: RouteSegment[],
  bufferMinutes: number,
  travelMode: TravelMode = "transit",
): Map<string, ChainedStart> {
  const arrivals = new Map(segments.map((segment) => [segment.to_item_id, segment]));
  const projected = new Map<string, ChainedStart>();
  let cursor: { ms: number; wallClock: boolean; from: TripItem } | undefined;

  for (const row of rows) {
    if (row.is_skipped) continue;
    const anchored = row.fixed_time ? readMoment(row.start_time) : undefined;
    const arrival = anchored ? undefined : readMoment(arrivals.get(row.id)?.ready_time);
    const travelMinutes = cursor ? estimateLegMinutes(cursor.from, row, travelMode) || 0 : 0;
    const chained = anchored
      || arrival
      || (cursor
        ? { ms: cursor.ms + (travelMinutes + bufferMinutes) * 60_000, wallClock: cursor.wallClock }
        : readMoment(row.start_time));
    if (!chained) {
      cursor = undefined;
      continue;
    }
    if (!row.fixed_time) {
      projected.set(row.id, {
        start: writeMoment(chained.ms, chained.wallClock),
        estimated: !arrival,
      });
    }
    cursor = {
      ms: chained.ms + (row.duration_minutes || 0) * 60_000,
      wallClock: chained.wallClock,
      from: row,
    };
  }
  return projected;
}
