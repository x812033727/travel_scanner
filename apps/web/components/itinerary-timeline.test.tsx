import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { RouteSegment, TripItem } from "@/lib/trip-types";
import { ItineraryTimeline } from "./itinerary-timeline";

function item(id: string, title: string, position: number, patch: Partial<TripItem> = {}): TripItem {
  return {
    id,
    item_type: "activity",
    day_date: "2026-11-10",
    position,
    title,
    start_time: `2026-11-10T${String(9 + position).padStart(2, "0")}:00:00+09:00`,
    locked: false,
    is_estimated: false,
    data: {},
    ...patch,
  };
}

const directRoute: RouteSegment = {
  from_item_id: "activity",
  to_item_id: "dinner",
  status: "resolved",
  travel_mode: "walk",
  provider: "google_routes",
  attribution: "Google Maps",
  generated_at: "2026-09-01T00:00:00Z",
  schedule_mode: "scheduled",
  preference: "FEWER_TRANSFERS",
  duration_minutes: 18,
  steps: [],
  details_available: [],
  warnings: [],
};

describe("readonly itinerary timeline", () => {
  it("hides skipped meals, keeps hotel anchors, and separates logistics", () => {
    const items = [
      item("flight-out", "長榮航空 BR 198", 0, { item_type: "flight", system_role: "outbound_flight", fixed_time: true, locked: true, data: { flight_info: { airline: "長榮航空", flight_number: "BR 198", origin: "TPE", destination: "NRT", departure_local: "2026-11-10T08:50", arrival_local: "2026-11-10T13:10" } } }),
      item("hotel-start", "從丸之內飯店出發", 0, { item_type: "hotel_anchor", system_role: "hotel_start", locked: true }),
      item("activity", "淺草寺", 1, { latitude: 35.7148, longitude: 139.7967 }),
      item("lunch", "已跳過午餐", 2, { item_type: "meal", system_role: "lunch", is_skipped: true, locked: true }),
      item("dinner", "銀座晚餐", 3, { item_type: "meal", system_role: "dinner", locked: true, latitude: 35.6717, longitude: 139.765 }),
      item("hotel-end", "返回丸之內飯店", 4, { item_type: "hotel_anchor", system_role: "hotel_end", locked: true }),
      item("flight-return", "回程航班尚未設定", 5, { item_type: "flight", system_role: "return_flight", fixed_time: true, locked: true, data: { flight_info: null } }),
      item("flight", "抵達羽田機場", 5, { item_type: "flight", data: { timeline_section: "logistics" } }),
    ];

    render(<ItineraryTimeline items={items} routes={[directRoute]} />);

    expect(screen.queryByText("已跳過午餐")).toBeNull();
    expect(screen.getByText("從丸之內飯店出發")).toBeTruthy();
    expect(screen.getByText("返回丸之內飯店")).toBeTruthy();
    expect(screen.getByText("交通與住宿資訊")).toBeTruthy();
    expect(screen.getByText("抵達羽田機場")).toBeTruthy();
    expect(screen.getByText("去程航班")).toBeTruthy();
    expect(screen.getByText("回程航班尚未設定")).toBeTruthy();
    expect(screen.getByText("步行 · 18 分鐘")).toBeTruthy();
  });
});
