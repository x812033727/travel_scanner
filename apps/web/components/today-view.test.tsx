import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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

describe("a way out of the day view", () => {
  /**
   * This page hides the site header below lg, app-bottom-nav returns null for
   * /trips/, and site-footer lists /trips/ in HIDDEN_ON. A traveller standing on a
   * platform had the browser's back button and nothing else.
   */
  it("links back to the trip list and the home page while the trip is loading", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => undefined)));
    render(<TodayView tripId="trip-1" />);

    expect(screen.getByRole("link", { name: "我的旅程" }).getAttribute("href")).toBe("/trips");
    expect(screen.getByRole("link", { name: "首頁" }).getAttribute("href")).toBe("/");
  });

  it("keeps those links when the trip cannot be read at all", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("offline"))));
    render(<TodayView tripId="trip-1" />);

    expect(await screen.findByText(/現在讀不到這趟行程/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "我的旅程" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "首頁" })).toBeTruthy();
  });
});

describe("the day view when the trip cannot be read", () => {
  /** A 500 and a dead connection are different news, and neither had a retry. */
  it("separates a server that answered badly from a network that did not answer", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("{}", { status: 500, headers: { "Content-Type": "application/json" } })));
    render(<TodayView tripId="trip-1" />);

    expect(await screen.findByText(/讀取這趟行程時出了問題/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "重試一次" })).toBeTruthy();
  });

  it("still says offline when the request never reached anything", async () => {
    const fetchMock = vi.fn(async () => { throw new TypeError("Failed to fetch"); });
    vi.stubGlobal("fetch", fetchMock);
    render(<TodayView tripId="trip-1" />);

    expect(await screen.findByText(/連上網路後再試一次/)).toBeTruthy();
    const before = fetchMock.mock.calls.length;
    fireEvent.click(screen.getByRole("button", { name: "重試一次" }));
    await waitFor(() => expect(fetchMock.mock.calls.length).toBeGreaterThan(before));
  });
});
