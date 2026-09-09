import "@testing-library/jest-dom/vitest";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
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
const hotel: TripItem = { ...lunch, id: "hotel", item_type: "hotel", system_role: "hotel_start", title: "東京飯店" };

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

  it("shows the original-script name under a catalog meal", () => {
    render(
      <SystemItineraryCard
        item={{
          ...lunch,
          title: "拉麵 · 一蘭 澀谷店",
          names: {
            title: {
              "zh-TW": "拉麵 · 一蘭 澀谷店",
              en: "Ramen · Ichiran Shibuya",
              original: "ラーメン · 一蘭 渋谷店",
              original_locale: "ja",
            },
          },
        }}
        locale="zh-TW"
        timezone="Asia/Tokyo"
        busy={false}
        onEdit={vi.fn()}
      />,
    );

    expect(screen.getByText("拉麵 · 一蘭 澀谷店")).toBeTruthy();
    expect(screen.getByText("ラーメン · 一蘭 渋谷店").getAttribute("lang")).toBe("ja");
  });

  it("hides the original line when it is the label already on show", () => {
    render(
      <SystemItineraryCard
        item={{ ...lunch, title: "浅草寺", names: { title: { ja: "浅草寺", original: "浅草寺" } } }}
        locale="ja"
        timezone="Asia/Tokyo"
        busy={false}
        onEdit={vi.fn()}
      />,
    );

    expect(screen.getAllByText("浅草寺")).toHaveLength(1);
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

  it("preserves legacy blur and Enter departure saves unless explicitly opted in", () => {
    const onDepartureTimeChange = vi.fn();
    render(<SystemItineraryCard item={hotel} locale="zh-TW" busy={false} onEdit={vi.fn()} departureTime="09:00" onDepartureTimeChange={onDepartureTimeChange} />);
    const input = screen.getByLabelText("每天從飯店出發的時間");
    fireEvent.change(input, { target: { value: "10:00" } });
    expect(onDepartureTimeChange).not.toHaveBeenCalled();
    fireEvent.blur(input);
    expect(onDepartureTimeChange).toHaveBeenCalledWith("10:00");
    expect(screen.queryByRole("button", { name: "儲存" })).not.toBeInTheDocument();
    input.focus();
    fireEvent.change(input, { target: { value: "11:00" } });
    fireEvent.keyDown(input, { key: "Enter" });
    expect(onDepartureTimeChange).toHaveBeenLastCalledWith("11:00");
  });

  it("never writes an explicit departure draft on blur or Enter, and Cancel resets it", () => {
    const onDepartureTimeChange = vi.fn(), onDepartureDirtyChange = vi.fn();
    render(<SystemItineraryCard item={hotel} locale="zh-TW" busy={false} onEdit={vi.fn()} departureTime="09:00" explicitDepartureSave onDepartureTimeChange={onDepartureTimeChange} onDepartureDirtyChange={onDepartureDirtyChange} />);
    const input = screen.getByLabelText("每天從飯店出發的時間");
    fireEvent.change(input, { target: { value: "10:00" } });
    fireEvent.blur(input); fireEvent.keyDown(input, { key: "Enter" });
    expect(onDepartureTimeChange).not.toHaveBeenCalled();
    expect(onDepartureDirtyChange).toHaveBeenLastCalledWith(true);
    fireEvent.click(screen.getByRole("button", { name: "取消" }));
    expect(input).toHaveValue("09:00");
    expect(onDepartureDirtyChange).toHaveBeenLastCalledWith(false);
    expect(onDepartureTimeChange).not.toHaveBeenCalled();
  });

  it.each(["false", "reject"] as const)("keeps a departure draft after %s, and a successful retry clears dirty state", async (failure) => {
    const onDepartureTimeChange = vi.fn<() => Promise<boolean | void>>();
    if (failure === "false") onDepartureTimeChange.mockResolvedValueOnce(false);
    else onDepartureTimeChange.mockRejectedValueOnce(new Error("Not saved"));
    onDepartureTimeChange.mockResolvedValueOnce(true);
    const onDepartureDirtyChange = vi.fn();
    const props = { item: hotel, locale: "zh-TW", busy: false, onEdit: vi.fn(), departureTime: "09:00", explicitDepartureSave: true, onDepartureTimeChange, onDepartureDirtyChange };
    const view = render(<SystemItineraryCard {...props} />);
    fireEvent.change(screen.getByLabelText("每天從飯店出發的時間"), { target: { value: "10:00" } });
    view.rerender(<SystemItineraryCard {...props} departureTime="08:00" />);
    expect(screen.getByLabelText("每天從飯店出發的時間")).toHaveValue("10:00");
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("內容已保留");
    expect(screen.getByLabelText("每天從飯店出發的時間")).toHaveValue("10:00");
    expect(onDepartureDirtyChange).toHaveBeenLastCalledWith(true);
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    await waitFor(() => expect(onDepartureDirtyChange).toHaveBeenLastCalledWith(false));
    expect(onDepartureTimeChange.mock.calls).toEqual([["10:00"], ["10:00"]]);
    expect(screen.getByLabelText("每天從飯店出發的時間")).toHaveValue("10:00");
  });

  it("blocks repeated explicit saves and reports busy until the callback settles", async () => {
    let finish!: (result: boolean) => void;
    const onDepartureTimeChange = vi.fn(() => new Promise<boolean>((resolve) => { finish = resolve; }));
    const onDepartureBusyChange = vi.fn();
    render(<SystemItineraryCard item={hotel} locale="zh-TW" busy={false} onEdit={vi.fn()} departureTime="09:00" explicitDepartureSave onDepartureTimeChange={onDepartureTimeChange} onDepartureBusyChange={onDepartureBusyChange} />);
    fireEvent.change(screen.getByLabelText("每天從飯店出發的時間"), { target: { value: "10:00" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    expect(onDepartureTimeChange).toHaveBeenCalledOnce();
    expect(onDepartureBusyChange).toHaveBeenLastCalledWith(true);
    expect(screen.getByRole("button", { name: "取消" })).toBeDisabled();
    expect(screen.getByLabelText("每天從飯店出發的時間")).toBeDisabled();
    await act(async () => { finish(true); });
    expect(onDepartureBusyChange).toHaveBeenLastCalledWith(false);
    expect(screen.getByRole("status")).toHaveTextContent("已儲存");
  });

  it("disables Save for an empty departure and ignores late callbacks after the card unmounts", async () => {
    let finish!: () => void;
    const onDepartureTimeChange = vi.fn(() => new Promise<void>((resolve) => { finish = resolve; }));
    const onDepartureDirtyChange = vi.fn();
    const view = render(<SystemItineraryCard item={hotel} locale="zh-TW" busy={false} onEdit={vi.fn()} departureTime="09:00" explicitDepartureSave onDepartureTimeChange={onDepartureTimeChange} onDepartureDirtyChange={onDepartureDirtyChange} />);
    fireEvent.change(screen.getByLabelText("每天從飯店出發的時間"), { target: { value: "" } });
    expect(screen.getByRole("button", { name: "儲存" })).toBeDisabled();
    fireEvent.change(screen.getByLabelText("每天從飯店出發的時間"), { target: { value: "10:00" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    view.unmount(); onDepartureDirtyChange.mockClear();
    await act(async () => { finish(); });
    expect(onDepartureDirtyChange).not.toHaveBeenCalled();
  });
});
