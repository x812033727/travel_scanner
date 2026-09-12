import { describe, expect, it } from "vitest";
import type { TripItem } from "@/lib/trip-types";
import { afterAiPartnerModules, dayPartnerKind, dayPartnerModules } from "./trip-partner-offers";

const item = (over: Partial<TripItem>): TripItem => ({
  id: over.id ?? "item", title: "x", item_type: "hotspot", day_date: "2026-11-11", position: 0,
  data: {}, ...over,
} as TripItem);

const days = ["2026-11-11", "2026-11-12", "2026-11-13"];

describe("dayPartnerKind", () => {
  it("uses the flight anchors when the trip has them", () => {
    const items = [
      item({ id: "out", system_role: "outbound_flight", item_type: "flight", day_date: "2026-11-11" }),
      item({ id: "back", system_role: "return_flight", item_type: "flight", day_date: "2026-11-13" }),
    ];
    expect(dayPartnerKind("2026-11-11", days, items)).toBe("arrival");
    expect(dayPartnerKind("2026-11-12", days, items)).toBe("day");
    expect(dayPartnerKind("2026-11-13", days, items)).toBe("departure");
  });

  it("falls back to the first and last day without flights, and a single day is arrival", () => {
    expect(dayPartnerKind("2026-11-11", days, [])).toBe("arrival");
    expect(dayPartnerKind("2026-11-13", days, [])).toBe("departure");
    expect(dayPartnerKind("2026-11-12", days, [])).toBe("day");
    expect(dayPartnerKind("2026-11-11", ["2026-11-11"], [])).toBe("arrival");
  });
});

describe("dayPartnerModules", () => {
  const all = ["flight", "hotel", "activities", "transport", "connectivity"] as const;

  it("asks for the airport ride and a way online on arrival, plus a hotel until one is set", () => {
    expect(dayPartnerModules("arrival", { lodgingReady: false, available: all })).toEqual(["hotel", "transport", "connectivity"]);
    expect(dayPartnerModules("arrival", { lodgingReady: true, available: all })).toEqual(["transport", "connectivity"]);
  });

  it("asks only for the ride back on departure and only for tickets in between", () => {
    expect(dayPartnerModules("departure", { lodgingReady: false, available: all })).toEqual(["transport"]);
    expect(dayPartnerModules("day", { lodgingReady: false, available: all })).toEqual(["activities"]);
  });

  it("never names a module the destination has nothing ready for", () => {
    expect(dayPartnerModules("arrival", { lodgingReady: false, available: ["activities"] })).toEqual([]);
    expect(dayPartnerModules("arrival", { lodgingReady: false, available: ["connectivity", "hotel"] })).toEqual(["hotel", "connectivity"]);
    expect(dayPartnerModules("day", { lodgingReady: true, available: [] })).toEqual([]);
  });
});

describe("afterAiPartnerModules", () => {
  it("adds the arrival logistics when the plan covered the whole trip or the arrival day", () => {
    const all = ["activities", "transport", "connectivity"] as const;
    expect(afterAiPartnerModules("trip", "day", all)).toEqual(["activities", "transport", "connectivity"]);
    expect(afterAiPartnerModules("day", "arrival", all)).toEqual(["activities", "transport", "connectivity"]);
    expect(afterAiPartnerModules("day", "day", all)).toEqual(["activities"]);
    expect(afterAiPartnerModules("day", "day", ["transport"])).toEqual([]);
  });
});
