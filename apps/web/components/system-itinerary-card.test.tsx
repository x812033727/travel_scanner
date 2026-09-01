import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { TripItem } from "@/lib/trip-types";
import { SystemItineraryCard } from "./system-itinerary-card";

const lunch: TripItem = {
  id: "lunch",
  item_type: "meal",
  day_date: "2026-11-10",
  position: 2,
  title: "東京定食",
  location_name: "東京車站",
  start_time: "2026-11-10T12:00:00+09:00",
  duration_minutes: 60,
  locked: true,
  fixed_time: true,
  system_role: "lunch",
  is_skipped: false,
  is_estimated: false,
  latitude: 35.68,
  longitude: 139.76,
  data: {},
};

describe("system itinerary card", () => {
  it("shows fixed meal details and exposes explicit edit and skip actions", () => {
    const edit = vi.fn();
    const skip = vi.fn();
    render(
      <SystemItineraryCard
        item={lunch}
        locale="zh-TW"
        timezone="Asia/Tokyo"
        busy={false}
        onEdit={edit}
        onSkip={skip}
      />,
    );

    expect(screen.getByText("午餐")).toBeTruthy();
    expect(screen.getByText(/12:00 · 60 分/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "更換餐廳" }));
    fireEvent.click(screen.getByRole("button", { name: "跳過" }));
    expect(edit).toHaveBeenCalledOnce();
    expect(skip).toHaveBeenCalledOnce();
  });

  it("keeps skipped meal details visible in a muted card with restore as the only action", () => {
    const restore = vi.fn();
    render(
      <SystemItineraryCard
        item={{ ...lunch, is_skipped: true }}
        locale="zh-TW"
        timezone="Asia/Tokyo"
        busy={false}
        onEdit={vi.fn()}
        onSkip={restore}
      />,
    );

    expect(screen.getByText("已跳過，不計停留時間與路線")).toBeTruthy();
    expect(screen.getByText("東京定食")).toBeTruthy();
    expect(screen.getByText(/固定時間 · 12:00 · 60 分/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: "更換餐廳" })).toBeNull();
    expect(screen.queryByRole("button", { name: "跳過" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "恢復" }));
    expect(restore).toHaveBeenCalledOnce();
  }, 10_000);
});
