export const usageOperations = [
  "travel_search",
  "flexible_flight_search",
  "flight_hotel_search",
  "full_trip_search",
  "multi_city_search",
  "public_airline_fare_search",
  "back_to_back_fare_search",
  "live_back_to_back_fare_search",
  "flight_status_lookup",
  "ai_itinerary_generation",
  "ai_itinerary_refine",
  "itinerary_optimization",
  "price_reoptimization",
] as const;

export type UsageOperation = (typeof usageOperations)[number];

export type PublicUsagePackage = {
  code: string;
  name: string;
  uses: number;
  price_twd: number;
  display_order: number;
  is_featured: boolean;
  expires: boolean;
  purchasable: boolean;
};

export type UsageCatalog = {
  trial_uses: number;
  packages: PublicUsagePackage[];
  operation_costs: Record<UsageOperation, number>;
};

/** What the API actually sent: an older API may not price every operation this build knows. */
export type RawUsageCatalog = Omit<UsageCatalog, "operation_costs"> & {
  operation_costs: Partial<Record<UsageOperation, number>>;
};

export type UsageCatalogState =
  | { status: "ready"; catalog: UsageCatalog }
  | { status: "unavailable"; catalog: null };

export const defaultUsageCatalog: UsageCatalog = {
  trial_uses: 3,
  packages: [],
  operation_costs: Object.fromEntries(
    usageOperations.map((operation) => [operation, 1]),
  ) as Record<UsageOperation, number>,
};

/**
 * Structural validation only. The catalog may omit operations the running API does not
 * know yet (a web bundle deployed ahead of the API); normalizeUsageCatalog prices those.
 * A cost that is present but not an integer in 0..100 is still a broken catalog, and the
 * whole payload is refused: that is corruption, not version skew.
 */
export function isUsageCatalog(value: unknown): value is RawUsageCatalog {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Partial<RawUsageCatalog>;
  if (!Number.isInteger(candidate.trial_uses) || Number(candidate.trial_uses) < 1) return false;
  if (!Array.isArray(candidate.packages) || typeof candidate.operation_costs !== "object" || candidate.operation_costs === null) return false;
  return Object.values(candidate.operation_costs as Record<string, unknown>).every(
    (uses) => Number.isInteger(uses) && Number(uses) >= 0 && Number(uses) <= 100,
  );
}

/**
 * Price every operation this build knows. An operation the API left out is charged the
 * default cost (one use, the conservative guess) and reported in `missing`, so the loader
 * can log it. This is a deliberate policy, decided in
 * tasks/done/2026-09-06-usage-catalog-validation-rejects-everything-when.md: one
 * unknown operation degrades that operation's copy, not every metered surface at once.
 */
export function normalizeUsageCatalog(raw: RawUsageCatalog): {
  catalog: UsageCatalog;
  missing: UsageOperation[];
} {
  const missing = usageOperations.filter((operation) => !(operation in raw.operation_costs));
  if (missing.length === 0) return { catalog: raw as UsageCatalog, missing };
  return {
    catalog: {
      ...raw,
      operation_costs: { ...defaultUsageCatalog.operation_costs, ...raw.operation_costs },
    },
    missing,
  };
}

export function searchUsageOperation(input: {
  tripType?: string;
  modules: string[];
  optimizationMode?: string;
  flexibleDates?: boolean;
}): UsageOperation {
  if (input.tripType === "multi_city") return "multi_city_search";
  const modules = new Set(input.modules);
  if (input.optimizationMode && modules.size >= 3) return "full_trip_search";
  if (modules.size === 2 && modules.has("flight") && modules.has("hotel")) return "flight_hotel_search";
  if (input.flexibleDates && modules.has("flight")) return "flexible_flight_search";
  return "travel_search";
}
