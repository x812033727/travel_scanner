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

export function isUsageCatalog(value: unknown): value is UsageCatalog {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Partial<UsageCatalog>;
  if (!Number.isInteger(candidate.trial_uses) || Number(candidate.trial_uses) < 1) return false;
  if (!Array.isArray(candidate.packages) || typeof candidate.operation_costs !== "object" || candidate.operation_costs === null) return false;
  return usageOperations.every((operation) => {
    const uses = (candidate.operation_costs as Record<string, unknown>)[operation];
    return Number.isInteger(uses) && Number(uses) >= 0 && Number(uses) <= 100;
  });
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
