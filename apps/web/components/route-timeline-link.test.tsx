import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { dayTimelineCopy } from "@/components/planner/day-timeline-copy";
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
    expect(screen.getByText("尚未查詢")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /晴空塔.*尚未查詢/ }));
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

  it("labels an unqueried estimate honestly without suggesting a provider duration", () => {
    const edge: DayTimelineEdge = { from: { id: "from" } as TripItem, to: { id: "to" } as TripItem,
      travelMode: "transit", status: "estimated", estimatedMinutes: 15 };
    render(<RouteTimelineLink edge={edge} segment={{ ...segment, status: "failed", duration_minutes: 0 }} nextTitle="淺草寺" onClick={() => undefined} />);
    expect(screen.getByText("尚未查詢")).toBeTruthy();
    expect(screen.getByRole("button").textContent).not.toContain("15");
    expect(screen.getByRole("button").textContent).not.toContain("0 分");
  });

  it.each([
    { provider: "estimate", status: "estimated", duration_minutes: 20 },
    { provider: "google_routes", status: "failed", duration_minutes: 20 },
    { provider: "google_routes", status: "unavailable", duration_minutes: 0 },
  ])("never presents a saved placeholder or failed segment as searched: %j", (invalid) => {
    render(<RouteTimelineLink segment={{ ...segment, ...invalid }} nextTitle="北村韓屋村" onClick={() => undefined} />);
    expect(screen.getByText("尚未查詢")).toBeTruthy();
    expect(screen.queryByText(/^(約 )?20 分$/)).toBeNull();
    expect(screen.queryByText("＋緩衝 10 分")).toBeNull();
  });

  it("keeps walking with unknown timing actionable without claiming a duration", () => {
    const open = vi.fn();
    const edge: DayTimelineEdge = { from: { id: "from" } as TripItem, to: { id: "to" } as TripItem,
      travelMode: "walk", status: "pending" };
    render(<RouteTimelineLink edge={edge} nextTitle="北村韓屋村" onClick={open} />);
    expect(screen.getByText("尚未查詢")).toBeTruthy();
    expect(screen.getByText("交通待確認")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /尚未查詢/ }));
    expect(open).toHaveBeenCalledOnce();
  });

  it("distinguishes a manually reserved duration from a provider timetable", () => {
    render(<RouteTimelineLink segment={{ ...segment, provider: "manual", travel_mode: "walk", duration_minutes: 18 }} nextTitle="北村韓屋村" onClick={() => undefined} />);
    expect(screen.getByText("手動預留 18 分")).toBeTruthy();
    expect(screen.getByText("＋緩衝 10 分")).toBeTruthy();
    expect(screen.queryByText(/^18 分$/)).toBeNull();
    expect(screen.queryByText("尚未查詢")).toBeNull();
  });

  it.each([
    ["zh-TW", "尚未查詢", "手動預留 18 分"],
    ["zh-CN", "尚未查询", "手动预留 18 分"],
    ["en", "Not searched yet", "Manually reserved 18 min"],
    ["ja", "未検索", "手動で18分を確保"],
    ["ko", "아직 검색하지 않음", "수동으로 18분 확보"],
  ])("provides unqueried and manual status copy for %s", (locale, unqueried, manual) => {
    const copy = dayTimelineCopy(locale);
    expect(copy.unqueried).toBe(unqueried);
    expect(copy.manual.replace("{minutes}", "18")).toBe(manual);
  });
});
