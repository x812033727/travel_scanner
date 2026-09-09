import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { DayTimelineEdge, TripItem } from "@/lib/trip-types";
import { RouteTimelineLink } from "./route-timeline-link";

const segment = {
  from_item_id: "from",
  to_item_id: "to",
  status: "resolved",
  travel_mode: "transit" as const,
  is_override: true,
  provider: "google_routes",
  attribution: "Google Maps",
  generated_at: "2026-09-01T00:00:00Z",
  schedule_mode: "scheduled" as const,
  preference: "FEWER_TRANSFERS",
  duration_minutes: 24,
  buffer_minutes: 10,
  departure_time: "2026-11-10T01:00:00Z",
  arrival_time: "2026-11-10T01:24:00Z",
  ready_time: "2026-11-10T01:34:00Z",
  steps: [],
  details_available: [],
  warnings: [],
};

describe("route timeline link", () => {
  it("shows travel time, separate buffer and selected mode", () => {
    render(<RouteTimelineLink segment={segment} nextTitle="淺草寺" onClick={() => undefined} />);
    expect(screen.getByText("24 分")).toBeTruthy();
    expect(screen.getByText("＋緩衝 10 分")).toBeTruthy();
    expect(screen.getByText("大眾運輸")).toBeTruthy();
    expect(screen.queryByText(/可開始下一站/)).toBeNull();
    expect(screen.getByText("單段")).toBeTruthy();
  });

  it("lets an empty segment open transport selection", () => {
    const open = vi.fn();
    render(<RouteTimelineLink nextTitle="晴空塔" onClick={open} />);
    fireEvent.click(screen.getByRole("button", { name: /查看交通/ }));
    expect(open).toHaveBeenCalledOnce();
  });

  it("shows one quiet pending connector instead of another place setup button", () => {
    const open = vi.fn();
    render(<RouteTimelineLink needsSetup="location" nextTitle="尚未安排午餐" onClick={open} />);
    expect(screen.getByText("交通待確認")).toBeTruthy();
    expect(screen.queryByRole("button")).toBeNull();
    expect(open).not.toHaveBeenCalled();
  });

  it("does not present stale absolute route timestamps as a current arrival", () => {
    render(<RouteTimelineLink segment={{ ...segment, status: "stale" }} nextTitle="淺草寺" onClick={() => undefined} />);
    expect(screen.getByText("路線待更新")).toBeTruthy();
    expect(screen.queryByText("24 分")).toBeNull();
  });

  it("uses the derived estimate when an invalid saved duration was excluded", () => {
    const edge: DayTimelineEdge = { from: { id: "from" } as TripItem, to: { id: "to" } as TripItem,
      travelMode: "transit", status: "estimated", estimatedMinutes: 15 };
    render(<RouteTimelineLink edge={edge} segment={{ ...segment, status: "failed", duration_minutes: 0 }} nextTitle="淺草寺" onClick={() => undefined} />);
    expect(screen.getByRole("button").textContent).toContain("15");
    expect(screen.getByRole("button").textContent).not.toContain("0 分");
  });
});
