import { describe, expect, it } from "vitest";
import {
  defaultUsageCatalog,
  isUsageCatalog,
  normalizeUsageCatalog,
  searchUsageOperation,
  usageOperations,
} from "./usage-catalog";

const costs: Record<string, number> = Object.fromEntries(
  usageOperations.map((operation) => [operation, 1]),
);

describe("usage catalog", () => {
  it("accepts a complete bounded catalog and rejects an invalid cost", () => {
    const catalog = { trial_uses: 3, packages: [], operation_costs: costs };
    expect(isUsageCatalog(catalog)).toBe(true);
    expect(isUsageCatalog({
      ...catalog,
      operation_costs: { ...costs, travel_search: 101 },
    })).toBe(false);
    expect(isUsageCatalog({ ...catalog, operation_costs: { ...costs, travel_search: "1" } })).toBe(false);
    expect(isUsageCatalog({ ...catalog, trial_uses: 0 })).toBe(false);
  });

  it("prices an operation the API does not know yet at the default cost instead of blanking the catalog", () => {
    // An API that has not learned ai_itinerary_refine still prices everything else.
    const older: Record<string, number> = { ...costs, travel_search: 2 };
    delete older.ai_itinerary_refine;
    const raw = { trial_uses: 3, packages: [], operation_costs: older };
    expect(isUsageCatalog(raw)).toBe(true);
    if (!isUsageCatalog(raw)) throw new Error("unreachable");

    const { catalog, missing } = normalizeUsageCatalog(raw);
    expect(missing).toEqual(["ai_itinerary_refine"]);
    expect(catalog.operation_costs.ai_itinerary_refine).toBe(defaultUsageCatalog.operation_costs.ai_itinerary_refine);
    expect(catalog.operation_costs.travel_search).toBe(2);
    expect(Object.keys(catalog.operation_costs).sort()).toEqual([...usageOperations].sort());

    // A complete catalog passes through untouched.
    const complete = { trial_uses: 3, packages: [], operation_costs: costs };
    expect(normalizeUsageCatalog(complete)).toEqual({ catalog: complete, missing: [] });
  });

  it("selects all five search billing operations from the submitted shape", () => {
    expect(searchUsageOperation({ modules: ["flight"] })).toBe("travel_search");
    expect(searchUsageOperation({ modules: ["flight"], flexibleDates: true })).toBe("flexible_flight_search");
    expect(searchUsageOperation({ modules: ["flight", "hotel"] })).toBe("flight_hotel_search");
    expect(searchUsageOperation({ modules: ["flight", "hotel", "activity"], optimizationMode: "balanced" })).toBe("full_trip_search");
    expect(searchUsageOperation({ tripType: "multi_city", modules: ["flight"] })).toBe("multi_city_search");
  });
});
