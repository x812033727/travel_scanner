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
  it("never reports zero transfers when no transit steps were supplied", () => {
    render(<RouteSegmentCard defaultExpanded segment={{ ...base, travel_mode: "transit", steps: [], details_available: [] }} />);
    expect(screen.getByText("轉乘次數未提供")).toBeTruthy();
    expect(screen.queryByText("轉乘 0 次")).toBeNull();
    expect(screen.queryByText("查看完整移動步驟")).toBeNull();
  });

  it.each(["manual", "estimate"])("labels %s timing without showing unsourced station steps", (provider) => {
    render(<RouteSegmentCard defaultExpanded segment={{ ...base, travel_mode: "transit", provider }} />);
    expect(screen.getByText("排程出發")).toBeTruthy();
    expect(screen.getByText("排程抵達")).toBeTruthy();
    expect(screen.getByText("目前未取得移動步驟")).toBeTruthy();
    expect(screen.queryByText("搭乘銀座線")).toBeNull();
    expect(screen.queryByText("轉乘 0 次")).toBeNull();
  });

  it("renders sourced boarding, transfer and alighting stops in order", () => {
    const { container } = render(<RouteSegmentCard defaultExpanded segment={{ ...base, steps: [base.steps[0], { ...base.steps[0], instruction: "轉乘2號線", departure_stop: "市廳", arrival_stop: "弘大入口" }] }} />);
    expect(screen.getByText("上車：上野")).toBeTruthy();
    expect(screen.getByText("下車：淺草")).toBeTruthy();
    expect(screen.getByText("轉乘上車：市廳")).toBeTruthy();
    expect(screen.getByText("下車：弘大入口")).toBeTruthy();
    const steps = container.querySelector(".route-step-list")!;
    const metrics = container.querySelector(".route-detail-metrics")!;
    expect(Boolean(steps.compareDocumentPosition(metrics) & Node.DOCUMENT_POSITION_FOLLOWING)).toBe(true);
  });

  it("labels distant-trip preview times as references and renders every step in Seoul time", () => {
    render(<RouteSegmentCard defaultExpanded timezone="Asia/Seoul" segment={{ ...base, provider: "google_routes", schedule_mode: "preview",
      requested_departure_time: "2027-02-11T09:00:00+09:00", departure_time: "2026-09-17T00:00:00Z", arrival_time: "2026-09-17T00:23:00Z",
      steps: [{ travel_mode: "WALK", instruction: "步行至公車站", duration_minutes: 6 },
        { ...base.steps[0], instruction: "搭乘9401公車", line_short_name: "9401", departure_time: "2026-09-17T00:10:00Z", arrival_time: "2026-09-17T00:15:00Z", duration_minutes: 5 },
        { travel_mode: "WALK", instruction: "步行至下一站", duration_minutes: 7 }],
    }} />);
    expect(screen.getByText("以下時刻為近期參考，不是旅程日期已確認的班次。")).toBeTruthy();
    expect(screen.getByText("09:10 → 09:15")).toBeTruthy();
    expect(screen.queryByText("00:10 → 00:15")).toBeNull();
    expect(screen.getByText("步行至公車站")).toBeTruthy();
    expect(screen.getByText("上車：上野")).toBeTruthy();
    expect(screen.getByText("下車：淺草")).toBeTruthy();
    expect(screen.getByText("步行至下一站")).toBeTruthy();
  });

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

  it("keeps ODsay route handoff on NAVER Maps", () => {
    render(<RouteSegmentCard segment={{ ...base, provider: "odsay", attribution: "ODsay", maps_url: "https://map.naver.com/p/directions/example" }} />);
    fireEvent.click(screen.getByRole("button"));
    const link = screen.getByRole("link", { name: /用 NAVER Maps 開啟/ });
    expect(link.getAttribute("href")).toContain("map.naver.com");
  });

  it("renders both server navigation choices for a saved ODsay route", () => {
    render(<RouteSegmentCard defaultExpanded segment={{ ...base, provider: "odsay", attribution: "ODsay", external_navigations: [
      { provider: "naver_maps", label: "NAVER Maps", travel_mode: "transit", web_url: "https://map.naver.com/p/directions/naver", app_url: "nmap://route/public" },
      { provider: "google_maps", label: "Google Maps", travel_mode: "transit", web_url: "https://www.google.com/maps/dir/?api=1", app_url: "https://www.google.com/maps/dir/?api=1" },
    ] }} />);
    expect(screen.getByRole("link", { name: "用 NAVER Maps 導航" }).getAttribute("href")).toContain("map.naver.com");
    expect(screen.getByRole("link", { name: "用 Google Maps 導航" }).getAttribute("href")).toContain("google.com");
    expect(screen.getByRole("link", { name: "開啟 NAVER App" }).getAttribute("href")).toBe("nmap://route/public");
  });

  it("does not revive a legacy maps URL when the server supplies an empty navigation list", () => {
    render(<RouteSegmentCard defaultExpanded segment={{ ...base, maps_url: "https://www.google.com/maps/", external_navigations: [] }} />);
    expect(screen.queryByRole("link")).toBeNull();
  });
});
