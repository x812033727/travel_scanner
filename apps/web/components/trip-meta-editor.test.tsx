import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { Trip, TripItem } from "@/lib/trip-types";
import { TripMetaEditor } from "./trip-meta-editor";

function item(overrides: Partial<TripItem>): TripItem {
  return {
    id: "i1",
    item_type: "custom",
    day_date: "2026-11-10",
    position: 0,
    title: "淺草寺",
    locked: false,
    is_estimated: false,
    data: {},
    ...overrides,
  };
}

const baseTrip: Trip = {
  id: "t1",
  name: "東京三日",
  status: "planning",
  mode: "manual",
  total_price: 0,
  currency: "TWD",
  data: {},
  version: 4,
  start_date: "2026-11-10",
  end_date: "2026-11-12",
  timezone: "Asia/Tokyo",
  items: [
    item({ id: "a1", day_date: "2026-11-12", title: "台場" }),
    item({
      id: "m1",
      day_date: "2026-11-12",
      item_type: "meal",
      system_role: "lunch",
      title: "拉麵店",
      data: { meal_selection_source: "user" },
    }),
    item({
      id: "m2",
      day_date: "2026-11-12",
      item_type: "meal",
      system_role: "dinner",
      title: "晚餐",
      data: {},
    }),
  ],
  route_segments: [],
};

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

function lastRequestBody(fetchMock: ReturnType<typeof vi.fn>): Record<string, unknown> {
  const call = fetchMock.mock.calls.at(-1) as unknown as [string, RequestInit];
  return JSON.parse(String(call[1].body)) as Record<string, unknown>;
}

afterEach(() => vi.unstubAllGlobals());

describe("trip meta editor", () => {
  it("renames the trip through PATCH and hands the fresh payload back", async () => {
    const fetchMock = vi.fn(async () => ok({ ...baseTrip, name: "東京五日", version: 5 }));
    vi.stubGlobal("fetch", fetchMock);
    const onUpdated = vi.fn();
    render(<TripMetaEditor trip={baseTrip} variant="hero" onUpdated={onUpdated} />);

    fireEvent.click(screen.getByRole("button", { name: "編輯旅程資訊" }));
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: " 東京五日 " } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));

    await waitFor(() => expect(onUpdated).toHaveBeenCalled());
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit];
    expect(url).toBe("/api/travel/trips/t1");
    expect(init.method).toBe("PATCH");
    expect(lastRequestBody(fetchMock)).toEqual({ version: 4, name: "東京五日" });
    expect(onUpdated.mock.calls[0][0].version).toBe(5);
  });

  it("blocks a shrink behind an explicit confirmation and reports what it deletes", async () => {
    const fetchMock = vi.fn(async () => ok({ ...baseTrip, end_date: "2026-11-11", version: 5 }));
    vi.stubGlobal("fetch", fetchMock);
    const onUpdated = vi.fn();
    render(<TripMetaEditor trip={baseTrip} variant="tools" onUpdated={onUpdated} />);

    fireEvent.click(screen.getByRole("button", { name: /旅程資訊/ }));
    fireEvent.change(screen.getByLabelText("結束日期"), { target: { value: "2026-11-11" } });

    // One removed day carrying two traveller-owned rows: the activity and the
    // hand-picked lunch. The empty dinner card is regenerable and not counted.
    expect(screen.getByText(/1 天/)).toBeTruthy();
    expect(screen.getByText(/2 筆/)).toBeTruthy();
    const save = screen.getByRole("button", { name: "儲存變更" });
    expect(save).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("checkbox"));
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);

    await waitFor(() => expect(onUpdated).toHaveBeenCalled());
    expect(lastRequestBody(fetchMock)).toEqual({
      version: 4,
      start_date: "2026-11-10",
      end_date: "2026-11-11",
      confirm_removed_days: true,
    });
  });

  it("asks for the same confirmation when a pure extension would reset a booked flight", async () => {
    const withBooking: Trip = {
      ...baseTrip,
      items: [
        ...baseTrip.items,
        item({
          id: "f2",
          day_date: "2026-11-12",
          item_type: "flight",
          system_role: "return_flight",
          title: "JAL JL802",
          locked: true,
          data: { flight_info: { airline: "JAL", flight_number: "JL802" } },
        }),
      ],
    };
    const fetchMock = vi.fn(async () => ok({ ...withBooking, end_date: "2026-11-14", version: 5 }));
    vi.stubGlobal("fetch", fetchMock);
    const onUpdated = vi.fn();
    render(<TripMetaEditor trip={withBooking} variant="tools" onUpdated={onUpdated} />);

    fireEvent.click(screen.getByRole("button", { name: /旅程資訊/ }));
    fireEvent.change(screen.getByLabelText("結束日期"), { target: { value: "2026-11-14" } });

    // Nothing is dropped, so no removed-day copy; the flight reset is what needs consent.
    expect(screen.queryByText(/移除 .* 天/)).toBeNull();
    expect(screen.getByText(/航班班號綁定原本的日期/)).toBeTruthy();
    const save = screen.getByRole("button", { name: "儲存變更" });
    expect(save).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("checkbox", { name: /我了解已設定的航班資訊將被重設/ }));
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);

    await waitFor(() => expect(onUpdated).toHaveBeenCalled());
    expect(lastRequestBody(fetchMock)).toEqual({
      version: 4,
      start_date: "2026-11-10",
      end_date: "2026-11-14",
      confirm_removed_days: true,
    });
  });

  it("sends a pure shift as shift_days and keeps the trip length visible", async () => {
    const fetchMock = vi.fn(async () => ok({ ...baseTrip, version: 5 }));
    vi.stubGlobal("fetch", fetchMock);
    const onUpdated = vi.fn();
    render(<TripMetaEditor trip={baseTrip} variant="hero" onUpdated={onUpdated} />);

    fireEvent.click(screen.getByRole("button", { name: "編輯旅程資訊" }));
    fireEvent.click(screen.getByRole("radio", { name: "整趟平移" }));
    expect(screen.getByText("旅程長度維持 3 天。")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("新的開始日期"), { target: { value: "2026-11-13" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));

    await waitFor(() => expect(onUpdated).toHaveBeenCalled());
    expect(lastRequestBody(fetchMock)).toEqual({ version: 4, shift_days: 3 });
  });

  it("surfaces a version conflict without pretending the save happened", async () => {
    const fetchMock = vi.fn(async () => ({
      ok: false,
      status: 409,
      json: async () => ({ code: "trip_version_conflict", detail: "旅程已被更新" }),
    }));
    vi.stubGlobal("fetch", fetchMock);
    const onUpdated = vi.fn();
    render(<TripMetaEditor trip={baseTrip} variant="hero" onUpdated={onUpdated} />);

    fireEvent.click(screen.getByRole("button", { name: "編輯旅程資訊" }));
    fireEvent.change(screen.getByLabelText("旅程名稱"), { target: { value: "新名字" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));

    expect(await screen.findByText("旅程已在其他視窗更新，請先重新載入再編輯。")).toBeTruthy();
    expect(onUpdated).not.toHaveBeenCalled();
  });
});
