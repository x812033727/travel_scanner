import { describe, expect, it } from "vitest";
import { formatTime, projectChainedStarts, type RouteSegment, type TripItem } from "./trip-types";

describe("formatTime", () => {
  it("keeps offset-free itinerary values as trip-local wall-clock time", () => {
    expect(formatTime("2026-11-10T15:00:00", "zh-TW", "Asia/Tokyo")).toBe("15:00");
  });

  it("converts offset-aware values into the trip timezone", () => {
    expect(formatTime("2026-11-10T06:00:00Z", "zh-TW", "Asia/Tokyo")).toBe("15:00");
  });
});

function item(overrides: Partial<TripItem> & Pick<TripItem, "id">): TripItem {
  return {
    day_date: "2026-11-10",
    position: 0,
    item_type: "activity",
    title: overrides.id,
    duration_minutes: 60,
    fixed_time: false,
    locked: false,
    is_skipped: false,
    data: {},
    ...overrides,
  } as TripItem;
}

function segment(from: string, to: string, readyTime: string): RouteSegment {
  return {
    from_item_id: from,
    to_item_id: to,
    ready_time: readyTime,
    status: "ok",
    provider: "test",
    attribution: "test",
    generated_at: "2026-11-09T00:00:00Z",
    schedule_mode: "scheduled",
    preference: "FEWER_TRANSFERS",
    duration_minutes: 20,
    steps: [],
    details_available: [],
    warnings: [],
  } as RouteSegment;
}

describe("projectChainedStarts", () => {
  const hotel = item({ id: "hotel", system_role: "hotel_start", fixed_time: true, start_time: "2026-11-10T09:00:00+09:00", duration_minutes: 0 });

  it("accumulates from the previous stop plus the day buffer when no route exists yet", () => {
    const rows = [hotel, item({ id: "museum" }), item({ id: "market", duration_minutes: 30 })];
    const projected = projectChainedStarts(rows, [], 10);

    // 09:00 出發 + 10 分緩衝 → 09:10；停留 60 分後 + 10 分 → 10:20
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:10");
    expect(formatTime(projected.get("market")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:20");
    expect(projected.get("museum")?.estimated).toBe(true);
    expect(projected.get("market")?.estimated).toBe(true);
  });

  it("prefers a computed segment's ready time and marks it as no longer an estimate", () => {
    const rows = [hotel, item({ id: "museum" }), item({ id: "market" })];
    const projected = projectChainedStarts(rows, [segment("hotel", "museum", "2026-11-10T09:35:00+09:00")], 10);

    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:35");
    expect(projected.get("museum")?.estimated).toBe(false);
    // 後續沒有路線的站別仍然接著累加：09:35 + 60 分停留 + 10 分緩衝
    expect(formatTime(projected.get("market")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:45");
    expect(projected.get("market")?.estimated).toBe(true);
  });

  it("restarts the chain from a fixed-time stop and leaves it out of the result", () => {
    const rows = [
      hotel,
      item({ id: "museum" }),
      item({ id: "lunch", system_role: "lunch", fixed_time: true, start_time: "2026-11-10T12:00:00+09:00" }),
      item({ id: "tower" }),
    ];
    const projected = projectChainedStarts(rows, [], 15);

    expect(projected.has("hotel")).toBe(false);
    expect(projected.has("lunch")).toBe(false);
    // 從固定的 12:00 午餐重新起算：+ 60 分停留 + 15 分緩衝
    expect(formatTime(projected.get("tower")?.start, "zh-TW", "Asia/Tokyo")).toBe("13:15");
  });

  it("skips items the member removed from the day", () => {
    const rows = [
      hotel,
      item({ id: "dinner", system_role: "dinner", fixed_time: true, start_time: "2026-11-10T18:30:00+09:00", is_skipped: true }),
      item({ id: "museum" }),
    ];
    const projected = projectChainedStarts(rows, [], 10);

    expect(projected.has("dinner")).toBe(false);
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:10");
  });

  it("keeps wall-clock itinerary values on the same clock instead of shifting them", () => {
    const rows = [
      item({ id: "hotel", system_role: "hotel_start", fixed_time: true, start_time: "2026-11-10T09:00:00", duration_minutes: 0 }),
      item({ id: "museum" }),
    ];
    const projected = projectChainedStarts(rows, [], 10);

    expect(projected.get("museum")?.start).toBe("2026-11-10T09:10");
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:10");
  });
});
