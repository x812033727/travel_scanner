import { describe, expect, it } from "vitest";
import { displayTripStatus } from "@/lib/trip-types";

describe("displayTripStatus", () => {
  const dates = { start_date: "2026-11-10", end_date: "2026-11-14" };

  it("shows a trip as under way while today falls inside its dates", () => {
    expect(displayTripStatus({ ...dates, status: "planning" }, new Date(2026, 10, 12))).toBe("travelling");
    expect(displayTripStatus({ ...dates, status: "planning" }, new Date(2026, 10, 10))).toBe("travelling");
    expect(displayTripStatus({ ...dates, status: "planning" }, new Date(2026, 10, 14))).toBe("travelling");
  });

  it("leaves a trip alone outside its dates, and keeps a status the traveller chose", () => {
    expect(displayTripStatus({ ...dates, status: "planning" }, new Date(2026, 10, 9))).toBe("planning");
    expect(displayTripStatus({ ...dates, status: "planning" }, new Date(2026, 10, 15))).toBe("planning");
    expect(displayTripStatus({ ...dates, status: "closed" }, new Date(2026, 10, 12))).toBe("closed");
    expect(displayTripStatus({ ...dates, status: "ready" }, new Date(2026, 10, 12))).toBe("ready");
  });

  it("falls back to planning when there are no dates at all", () => {
    expect(displayTripStatus({}, new Date(2026, 10, 12))).toBe("planning");
  });
});
