import { render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripPrintView } from "./trip-print-view";

afterEach(() => vi.unstubAllGlobals());

const asakusa = {
  id: "item-1",
  item_type: "activity",
  day_date: "2026-11-10",
  position: 0,
  title: "淺草寺",
  location_name: "淺草",
  start_time: "2026-11-10T00:00:00Z",
  end_time: "2026-11-10T01:00:00Z",
  duration_minutes: 60,
  latitude: 35.7148,
  longitude: 139.7967,
  locked: false,
  is_estimated: false,
  data: {},
};
const skytree = {
  ...asakusa,
  id: "item-2",
  position: 1,
  title: "晴空塔",
  location_name: "押上",
  start_time: "2026-11-10T02:00:00Z",
  end_time: "2026-11-10T03:00:00Z",
  latitude: 35.7101,
  longitude: 139.8107,
};
const secondDay = { ...asakusa, id: "item-3", day_date: "2026-11-11", title: "上野公園", start_time: "2026-11-11T00:00:00Z", end_time: "2026-11-11T01:00:00Z" };

const trip = {
  id: "trip-1",
  name: "東京五天",
  mode: "manual",
  total_price: 0,
  currency: "TWD",
  data: {},
  version: 1,
  destination_name: "東京",
  timezone: "Asia/Tokyo",
  start_date: "2026-11-10",
  end_date: "2026-11-11",
  items: [asakusa, skytree, secondDay],
  route_segments: [
    {
      from_item_id: "item-1",
      to_item_id: "item-2",
      status: "resolved",
      travel_mode: "transit",
      provider: "google_routes",
      attribution: "Google Maps",
      generated_at: "2026-11-01T00:00:00Z",
      schedule_mode: "scheduled",
      preference: "FEWER_TRANSFERS",
      duration_minutes: 25,
      buffer_minutes: 10,
      fare: 210,
      currency: "JPY",
      steps: [
        { travel_mode: "TRANSIT", instruction: "搭乘銀座線", line_short_name: "G", platform: "3" },
        { travel_mode: "WALK", instruction: "步行" },
        { travel_mode: "TRANSIT", instruction: "搭乘半藏門線", line_short_name: "Z", exit_name: "A2" },
      ],
      details_available: ["steps", "stops"],
      warnings: [],
    },
  ],
  day_notes: {},
};

function stubTrip() {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => trip }));
}

describe("TripPrintView", () => {
  it("prints a cover sheet and one section per day", async () => {
    stubTrip();
    render(<TripPrintView tripId="trip-1" />);

    await screen.findByRole("heading", { level: 1, name: "東京五天" });
    expect(screen.getByText("東京")).toBeTruthy();
    expect(screen.getByText("2 天")).toBeTruthy();
    const days = await screen.findAllByRole("heading", { level: 2 });
    expect(days).toHaveLength(2);
    expect(screen.getByRole("heading", { level: 3, name: "淺草寺" })).toBeTruthy();
    expect(screen.getByRole("heading", { level: 3, name: "上野公園" })).toBeTruthy();
  });

  it("writes the leg under the stop it leaves, with what the provider knew", async () => {
    stubTrip();
    render(<TripPrintView tripId="trip-1" />);

    const stop = (await screen.findByRole("heading", { level: 3, name: "淺草寺" })).closest("li");
    expect(stop).toBeTruthy();
    const line = within(stop as HTMLElement).getByText(/大眾運輸/);
    expect(line.textContent).toContain("25 分鐘");
    expect(line.textContent).toContain("轉乘 1 次");
    expect(line.textContent).toContain("G · Z");
    expect(line.textContent).toContain("車資 JPY 210");
    expect(line.textContent).toContain("月台 3");
    expect(line.textContent).toContain("出口 A2");
    expect(line.textContent).not.toContain("估算");
  });

  it("says so when a leg is only an estimate", async () => {
    const unrouted = { ...trip, route_segments: [] };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => unrouted }));
    render(<TripPrintView tripId="trip-1" />);

    await screen.findByRole("heading", { level: 3, name: "淺草寺" });
    await waitFor(() => expect(screen.getByText(/估算/)).toBeTruthy());
  });
});
