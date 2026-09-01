import { describe, expect, it } from "vitest";
import { formatTime } from "./trip-types";

describe("formatTime", () => {
  it("keeps offset-free itinerary values as trip-local wall-clock time", () => {
    expect(formatTime("2026-11-10T15:00:00", "zh-TW", "Asia/Tokyo")).toBe("15:00");
  });

  it("converts offset-aware values into the trip timezone", () => {
    expect(formatTime("2026-11-10T06:00:00Z", "zh-TW", "Asia/Tokyo")).toBe("15:00");
  });
});
