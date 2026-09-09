import { describe, expect, it } from "vitest";
import {
  adjacentPairKeys,
  distanceKm,
  deriveDayTimeline,
  estimateLegMinutes,
  formatTime,
  hasRoutePoint,
  missingSegmentCount,
  projectChainedStarts,
  segmentsForRows,
  type RouteSegment,
  type TripItem,
} from "./trip-types";

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
    latitude: 35.68,
    longitude: 139.76,
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

    // Even nearby coordinates include an estimated transit overhead and buffer.
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:20");
    expect(formatTime(projected.get("market")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:40");
    expect(projected.get("museum")?.estimated).toBe(true);
    expect(projected.get("market")?.estimated).toBe(true);
  });

  it("chains a computed segment by its duration and marks it as no longer an estimate", () => {
    const rows = [hotel, item({ id: "museum" }), item({ id: "market" })];
    const projected = projectChainedStarts(rows, [segment("hotel", "museum", "2026-11-10T09:35:00+09:00")], 10);

    // 09:00 出發 + 路線 20 分 + 當日緩衝 10 分（segment 沒帶 buffer）→ 09:30；
    // 存在 segment 上的 ready_time 只是算出當時的絕對時間，不拿來定錨
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:30");
    expect(projected.get("museum")?.estimated).toBe(false);
    // 後續沒有路線的站別仍然接著累加：09:30 + 60 分停留 + 10 分緩衝
    expect(formatTime(projected.get("market")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:50");
    expect(projected.get("market")?.estimated).toBe(true);
  });

  it("re-anchors a surviving downstream segment after the leg before it changed", () => {
    const rows = [
      item({ id: "hotel", system_role: "hotel_start", fixed_time: true, start_time: "2026-11-10T09:00:00+09:00", duration_minutes: 0, latitude: 35.6812, longitude: 139.7671 }),
      item({ id: "temple", latitude: 35.7148, longitude: 139.7967 }),
      item({ id: "tower", latitude: 35.7101, longitude: 139.8107 }),
    ];
    // temple→tower survived an edit; its stored ready time predates the new estimate above it.
    const stale = { ...segment("temple", "tower", "2026-11-10T09:50:00+09:00"), duration_minutes: 15, buffer_minutes: 5 };
    const projected = projectChainedStarts(rows, [stale], 10, "transit");

    // hotel→temple 缺路線：09:00 + 約 25 分 + 10 → 09:35；temple→tower 用它的 15 + 5 接著算
    expect(formatTime(projected.get("temple")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:35");
    expect(projected.get("temple")?.estimated).toBe(true);
    expect(formatTime(projected.get("tower")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:55");
    // A saved downstream duration cannot make the estimated upstream arrival certain.
    expect(projected.get("tower")?.estimated).toBe(true);
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
    expect(formatTime(projected.get("tower")?.start, "zh-TW", "Asia/Tokyo")).toBe("13:25");
  });

  it("skips items the member removed from the day", () => {
    const rows = [
      hotel,
      item({ id: "dinner", system_role: "dinner", fixed_time: true, start_time: "2026-11-10T18:30:00+09:00", is_skipped: true }),
      item({ id: "museum" }),
    ];
    const projected = projectChainedStarts(rows, [], 10);

    expect(projected.has("dinner")).toBe(false);
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:20");
  });

  it("keeps wall-clock itinerary values on the same clock instead of shifting them", () => {
    const rows = [
      item({ id: "hotel", system_role: "hotel_start", fixed_time: true, start_time: "2026-11-10T09:00:00", duration_minutes: 0 }),
      item({ id: "museum" }),
    ];
    const projected = projectChainedStarts(rows, [], 10);

    expect(projected.get("museum")?.start).toBe("2026-11-10T09:20");
    expect(formatTime(projected.get("museum")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:20");
  });
});

describe("estimateLegMinutes", () => {
  const station = { latitude: 35.6812, longitude: 139.7671 };
  const temple = { latitude: 35.7148, longitude: 139.7967 };

  it("scales the straight-line distance by a modest speed per mode, in five-minute steps", () => {
    // 東京車站 → 淺草寺 直線約 4.6 公里
    expect(distanceKm(station, temple)).toBeCloseTo(4.59, 1);
    expect(estimateLegMinutes(station, temple, "walk")).toBe(65);
    expect(estimateLegMinutes(station, temple, "transit")).toBe(25);
    expect(estimateLegMinutes(station, temple, "drive")).toBe(15);
  });

  it("never returns zero for a short hop and gives up without coordinates", () => {
    expect(estimateLegMinutes(station, { latitude: 35.6815, longitude: 139.7675 }, "walk")).toBe(5);
    expect(estimateLegMinutes(station, { latitude: null, longitude: null }, "walk")).toBeUndefined();
  });
});

describe("projectChainedStarts with located stops", () => {
  it("adds a distance-based travel estimate between stops that have no route yet", () => {
    const rows = [
      item({ id: "hotel", system_role: "hotel_start", fixed_time: true, start_time: "2026-11-10T09:00:00+09:00", duration_minutes: 0, latitude: 35.6812, longitude: 139.7671 }),
      item({ id: "temple", latitude: 35.7148, longitude: 139.7967 }),
    ];
    const projected = projectChainedStarts(rows, [], 10, "transit");

    // 09:00 出發 + 約 25 分大眾運輸 + 10 分緩衝 → 09:35，仍標示為估計
    expect(formatTime(projected.get("temple")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:35");
    expect(projected.get("temple")?.estimated).toBe(true);
  });

  it("uses the computed segment for a routed leg and the estimate only for the missing one", () => {
    const rows = [
      item({ id: "hotel", system_role: "hotel_start", fixed_time: true, start_time: "2026-11-10T09:00:00+09:00", duration_minutes: 0, latitude: 35.6812, longitude: 139.7671 }),
      item({ id: "temple", latitude: 35.7148, longitude: 139.7967 }),
      item({ id: "tower", latitude: 35.7101, longitude: 139.8107 }),
    ];
    const projected = projectChainedStarts(rows, [segment("hotel", "temple", "2026-11-10T09:28:00+09:00")], 10, "walk");

    // 09:00 + 路線 20 分 + 10 緩衝 → 09:30
    expect(formatTime(projected.get("temple")?.start, "zh-TW", "Asia/Tokyo")).toBe("09:30");
    expect(projected.get("temple")?.estimated).toBe(false);
    // 淺草寺 → 晴空塔 約 1.4 公里步行 ≈ 20 分：10:30 + 20 + 10 緩衝
    expect(formatTime(projected.get("tower")?.start, "zh-TW", "Asia/Tokyo")).toBe("11:00");
    expect(projected.get("tower")?.estimated).toBe(true);
  });
});

describe("adjacent pair helpers", () => {
  const rows = ["a", "b", "c", "d"].map((id, position) => item({ id, position }));
  const segments = [
    segment("a", "b", "2026-11-10T09:30:00+09:00"),
    segment("b", "c", "2026-11-10T10:30:00+09:00"),
    segment("c", "d", "2026-11-10T11:30:00+09:00"),
  ];

  it("keeps only the segments whose stops are still adjacent after a reorder", () => {
    const reordered = rows.map((row) => row.id === "d" ? { ...row, position: 2 } : row.id === "c" ? { ...row, position: 3 } : row);
    const surviving = segmentsForRows(segments, reordered);

    expect(surviving.map((entry) => `${entry.from_item_id}->${entry.to_item_id}`)).toEqual(["a->b"]);
    expect(missingSegmentCount(reordered, surviving)).toBe(2);
    expect(missingSegmentCount(rows, segments)).toBe(0);
  });

  it("ignores skipped stops and pairs each day on its own", () => {
    const withSkipAndOtherDay = [
      ...rows.slice(0, 3),
      { ...rows[3], is_skipped: true },
      item({ id: "e", position: 0, day_date: "2026-11-11" }),
      item({ id: "f", position: 1, day_date: "2026-11-11" }),
    ];

    expect([...adjacentPairKeys(withSkipAndOtherDay)]).toEqual(["a->b", "b->c", "e->f"]);
  });
});

describe("deriveDayTimeline", () => {
  const a = item({ id: "a", position: 1, fixed_time: true, start_time: "2026-11-10T09:00:00+09:00" });
  const b = item({ id: "b", position: 3 });
  const empty = (id: string, role: TripItem["system_role"], position: number) => item({
    id, position, system_role: role, latitude: null, longitude: null, fixed_time: true,
    start_time: "2026-11-10T12:00:00+09:00", data: { meal_selection_source: "unset" },
  });

  it("excludes empty hotels and meals from both edges and time without changing stored rows", () => {
    const rows = [empty("hotel", "hotel_start", 0), a, empty("lunch", "lunch", 2), b, empty("dinner", "dinner", 4), empty("return", "hotel_end", 5)];
    const original = JSON.stringify(rows);
    const value = deriveDayTimeline(rows, [segment("a", "b", "2026-11-10T10:30:00+09:00")]);
    expect(value.rows.map((row) => row.id)).toEqual(["a", "b"]);
    expect(value.optionalRows).toHaveLength(4);
    expect(value.edges.map((edge) => `${edge.from.id}->${edge.to.id}`)).toEqual(["a->b"]);
    expect(formatTime(value.starts.get("b")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:30");
    expect(value.starts.get("b")?.status).toBe("ready");
    expect(value.arrangementCount).toBe(2);
    expect(value.durationMinutes).toBe(120);
    expect(JSON.stringify(rows)).toBe(original);
  });

  it.each([undefined, "lunch", "hotel_start"] as const)("keeps a chosen unlocated %s as a barrier, never using a surviving a->b route", (role) => {
    const missing = item({ id: "missing", position: 2, system_role: role, latitude: undefined, longitude: undefined,
      location_name: "My chosen place", locked: true, data: { meal_selection_source: "user" } });
    const value = deriveDayTimeline([a, missing, { ...b, start_time: "2026-11-10T16:00:00+09:00" }], [segment("a", "b", "2026-11-10T10:30:00+09:00")]);
    expect(value.rows).toContain(missing);
    expect(value.optionalRows).toHaveLength(0);
    expect(value.edges.map((edge) => edge.status)).toEqual(["pending", "pending"]);
    expect(value.edges.every((edge) => edge.blocker === missing && !edge.segment)).toBe(true);
    expect(value.starts.has("b")).toBe(false);
    expect(value.unresolvedItems).toEqual([missing]);
  });

  it("retains skipped manual rows and chosen flights for display, without edges or time", () => {
    const skipped = item({ id: "skipped", position: 2, is_skipped: true });
    const flight = item({ id: "flight", position: -1, system_role: "outbound_flight", data: { flight_info: { flight_number: "JL1" } } });
    const value = deriveDayTimeline([flight, a, skipped, b], []);
    expect(value.rows).toEqual([flight, a, skipped, b]);
    expect(value.routeRows).toEqual([a, b]);
    expect(value.edges).toHaveLength(1);
    expect(value.durationMinutes).toBe(120);
  });

  it("propagates stale or estimated timing rather than claiming a reliable downstream arrival", () => {
    const c = item({ id: "c", position: 4 });
    const stale = { ...segment("a", "b", "2026-11-10T10:30:00+09:00"), status: "stale" };
    const value = deriveDayTimeline([a, b, c], [stale, segment("b", "c", "2026-11-10T12:00:00+09:00")]);
    expect(value.edges[0].status).toBe("stale");
    expect(value.starts.get("b")).toMatchObject({ status: "stale", estimated: true });
    expect(value.starts.get("c")).toMatchObject({ status: "stale", estimated: true });
  });

  it.each([
    { status: "failed", duration_minutes: 0 },
    { status: "unavailable", duration_minutes: 0 },
    { status: "failed", duration_minutes: 1 },
    { status: "resolved", duration_minutes: 0 },
  ])("uses a geographic estimate instead of an unknown route duration %j", (invalid) => {
    const saved = { ...segment("a", "b", "2026-11-10T10:00:00+09:00"), ...invalid };
    const value = deriveDayTimeline([a, b], [saved]);
    expect(value.edges[0].segment).toBeUndefined();
    expect(value.edges[0].status).toBe("estimated");
    expect(value.edges[0].estimatedMinutes).toBe(10);
    expect(formatTime(value.starts.get("b")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:20");
  });

  it("retains a genuine estimated provider duration and its buffer", () => {
    const saved = { ...segment("a", "b", "2026-11-10T10:00:00+09:00"), provider: "estimate",
      status: "estimated", duration_minutes: 17, buffer_minutes: 5 };
    const value = deriveDayTimeline([a, b], [saved]);
    expect(value.edges[0].segment).toBe(saved);
    expect(value.edges[0].status).toBe("estimated");
    expect(formatTime(value.starts.get("b")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:22");
  });

  it("preserves a fixed appointment while propagating a late arrival downstream", () => {
    const lunch = item({ id: "lunch", position: 2, system_role: "lunch", fixed_time: true, start_time: "2026-11-10T12:00:00+09:00" });
    const value = deriveDayTimeline([{ ...a, duration_minutes: 180 }, lunch, b], [segment("a", "lunch", "2026-11-10T12:30:00+09:00"), segment("lunch", "b", "2026-11-10T14:00:00+09:00")]);
    expect(value.starts.has("lunch")).toBe(false);
    expect(lunch.start_time).toBe("2026-11-10T12:00:00+09:00");
    expect(formatTime(value.starts.get("b")?.start, "zh-TW", "Asia/Tokyo")).toBe("14:00");
  });

  it("never chains across dates or falls back to stored downstream timestamps after a barrier", () => {
    const nextDay = { ...b, day_date: "2026-11-11", start_time: "2026-11-11T10:00:00+09:00" };
    const value = deriveDayTimeline([a, nextDay], [segment("a", "b", "2026-11-10T10:30:00+09:00")]);
    expect(value.edges).toHaveLength(0);
    expect(formatTime(value.starts.get("b")?.start, "zh-TW", "Asia/Tokyo")).toBe("10:00");
  });

  it.each([{ latitude: undefined, longitude: 0 }, { latitude: 0, longitude: null }, { latitude: NaN, longitude: 0 }, { latitude: 91, longitude: 0 }, { latitude: 0, longitude: -181 }])("rejects partial, nonfinite or out-of-range coordinates %j", (point) => {
    expect(hasRoutePoint(point)).toBe(false);
    expect(estimateLegMinutes(a, point, "walk")).toBeUndefined();
    const value = deriveDayTimeline([a, { ...b, ...point }], []);
    expect(value.edges[0].status).toBe("pending");
  });

  it("accepts zero coordinates", () => { expect(hasRoutePoint({ latitude: 0, longitude: 0 })).toBe(true); });
});
