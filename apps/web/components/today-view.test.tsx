import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { nowAndNext, TodayView } from "./today-view";
import type { TripItem } from "@/lib/trip-types";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

function stop(id: string, title: string, start: string, end: string): TripItem {
  return {
    id,
    item_type: "activity",
    day_date: "2026-11-10",
    position: 0,
    title,
    location_name: `${title}前`,
    start_time: start,
    end_time: end,
    duration_minutes: 60,
    locked: false,
    is_estimated: false,
    latitude: 35.71,
    longitude: 139.79,
    data: {},
  } as TripItem;
}

const morning = stop("a", "淺草寺", "2026-11-10T00:00:00Z", "2026-11-10T01:00:00Z");
const noon = stop("b", "晴空塔", "2026-11-10T03:00:00Z", "2026-11-10T04:00:00Z");
const evening = stop("c", "上野公園", "2026-11-10T08:00:00Z", "2026-11-10T09:00:00Z");

const trip = {
  id: "trip-1",
  name: "東京五天",
  mode: "manual",
  total_price: 0,
  currency: "TWD",
  data: {},
  version: 1,
  timezone: "Asia/Tokyo",
  items: [morning, noon, evening],
  route_segments: [],
};

describe("nowAndNext", () => {
  it("picks the stop that is running and the one after it", () => {
    const result = nowAndNext([morning, noon, evening], new Date("2026-11-10T00:30:00Z"));
    expect(result.now?.title).toBe("淺草寺");
    expect(result.next?.title).toBe("晴空塔");
  });

  it("between two stops there is no now, only a next", () => {
    const result = nowAndNext([morning, noon, evening], new Date("2026-11-10T02:00:00Z"));
    expect(result.now).toBeUndefined();
    expect(result.next?.title).toBe("晴空塔");
  });

  it("before the day starts the first stop is what comes next", () => {
    const result = nowAndNext([morning, noon], new Date("2026-11-09T22:00:00Z"));
    expect(result.next?.title).toBe("淺草寺");
  });
});

describe("TodayView", () => {
  it("shows now, next and the rest of the day", async () => {
    vi.setSystemTime(new Date("2026-11-10T00:30:00Z"));
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => trip }));

    render(<TodayView tripId="trip-1" />);

    expect(await screen.findByRole("heading", { level: 1, name: "東京五天" })).toBeTruthy();
    expect(screen.getByText("現在")).toBeTruthy();
    expect(screen.getByText("接下來")).toBeTruthy();
    expect(screen.getByRole("heading", { level: 2, name: "淺草寺" })).toBeTruthy();
    expect(screen.getByRole("heading", { level: 2, name: "晴空塔" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "打開完整行程" }).getAttribute("href")).toBe("/trips/trip-1");
  });

  it("says so when the trip cannot be read at all", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    render(<TodayView tripId="trip-1" />);
    expect(await screen.findByText(/連上網路後再試一次/)).toBeTruthy();
  });
});
