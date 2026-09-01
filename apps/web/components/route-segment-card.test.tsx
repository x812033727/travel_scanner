import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { RouteSegmentCard } from "./route-segment-card";

const base = {
  from_item_id: "from",
  to_item_id: "to",
  status: "resolved",
  provider: "google_routes",
  attribution: "Google Maps",
  generated_at: "2026-08-31T00:00:00Z",
  schedule_mode: "scheduled" as const,
  preference: "FEWER_TRANSFERS",
  duration_minutes: 24,
  details_available: ["steps", "stops"],
  warnings: [],
  steps: [{
    travel_mode: "TRANSIT",
    instruction: "搭乘銀座線",
    line_name: "銀座線",
    line_short_name: "G",
    line_color: "#ff9500",
    departure_stop: "上野",
    arrival_stop: "淺草",
    headsign: "淺草方向",
    stop_count: 3,
  }],
};

describe("route segment card", () => {
  it("labels missing exit data instead of inventing an exit", () => {
    render(<RouteSegmentCard segment={base} />);
    fireEvent.click(screen.getByRole("button"));
    expect(screen.getByText("此路線來源未提供可驗證的出口編號。")).toBeTruthy();
    expect(screen.getByText(/往 淺草方向/)).toBeTruthy();
    expect(screen.getAllByText("G").length).toBeGreaterThan(0);
  });

  it("shows sourced Japan platform, exit and recommended car", () => {
    render(<RouteSegmentCard segment={{ ...base, provider: "navitime", attribution: "NAVITIME JAPAN", details_available: [...base.details_available, "platform", "exit", "recommended_car"], steps: [{ ...base.steps[0], platform: "1", exit_name: "B3", recommended_car: "前方第 2 節" }] }} />);
    fireEvent.click(screen.getByRole("button"));
    expect(screen.getByText("月台 1")).toBeTruthy();
    expect(screen.getByText("出口 B3")).toBeTruthy();
    expect(screen.getByText("建議車廂 前方第 2 節")).toBeTruthy();
  });
});
