import { describe, expect, it } from "vitest";
import { isUsageCatalog, searchUsageOperation, usageOperations } from "./usage-catalog";

const costs = Object.fromEntries(usageOperations.map((operation) => [operation, 1]));

describe("usage catalog", () => {
  it("accepts a complete bounded catalog and rejects missing or invalid costs", () => {
    const catalog = { trial_uses: 3, packages: [], operation_costs: costs };
    expect(isUsageCatalog(catalog)).toBe(true);
    expect(isUsageCatalog({ ...catalog, operation_costs: { travel_search: 1 } })).toBe(false);
    expect(isUsageCatalog({
      ...catalog,
      operation_costs: { ...costs, travel_search: 101 },
    })).toBe(false);
  });

  it("selects all five search billing operations from the submitted shape", () => {
    expect(searchUsageOperation({ modules: ["flight"] })).toBe("travel_search");
    expect(searchUsageOperation({ modules: ["flight"], flexibleDates: true })).toBe("flexible_flight_search");
    expect(searchUsageOperation({ modules: ["flight", "hotel"] })).toBe("flight_hotel_search");
    expect(searchUsageOperation({ modules: ["flight", "hotel", "activity"], optimizationMode: "balanced" })).toBe("full_trip_search");
    expect(searchUsageOperation({ tripType: "multi_city", modules: ["flight"] })).toBe("multi_city_search");
  });
});
