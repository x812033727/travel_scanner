import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
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
    expect(screen.getByText(/大眾運輸.*可開始下一站/)).toBeTruthy();
    expect(screen.getByText("單段")).toBeTruthy();
  });

  it("lets an empty segment open transport selection", () => {
    const open = vi.fn();
    render(<RouteTimelineLink nextTitle="晴空塔" onClick={open} />);
    fireEvent.click(screen.getByRole("button", { name: /選擇這段交通方式/ }));
    expect(open).toHaveBeenCalledOnce();
  });
});
