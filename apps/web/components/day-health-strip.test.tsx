import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { DayHealthStrip } from "./day-health-strip";

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const health = {
  days: [
    {
      date: "2026-11-10",
      late: [{ item_id: "item-1", title: "壽司預約", late_minutes: 12 }],
      closed: [
        { item_id: "item-2", title: "東京國立博物館", start_time: "2026-11-10T00:00:00Z", opens_at: "09:30" },
        { item_id: "item-3", title: "築地市場", start_time: "2026-11-10T09:00:00Z", opens_at: null },
      ],
      unrouted: 2,
    },
    { date: "2026-11-11", late: [], closed: [], unrouted: 0 },
  ],
};

describe("DayHealthStrip", () => {
  beforeEach(() => apiMock.mockReset());

  it("says what the traveller cannot see by reading the day", async () => {
    apiMock.mockResolvedValue(health);
    const onSelectItem = vi.fn();
    render(<DayHealthStrip tripId="trip-1" day="2026-11-10" onSelectItem={onSelectItem} />);

    expect(await screen.findByText("壽司預約 可能遲到 12 分鐘")).toBeTruthy();
    expect(screen.getByText("東京國立博物館 到達時未開門，09:30 才開")).toBeTruthy();
    expect(screen.getByText("築地市場 到達時已打烊")).toBeTruthy();
    expect(screen.getByText("2 段還沒查路")).toBeTruthy();

    fireEvent.click(screen.getByText("壽司預約 可能遲到 12 分鐘"));
    expect(onSelectItem).toHaveBeenCalledWith("item-1");
  });

  it("shows nothing at all on a day with nothing to say", async () => {
    apiMock.mockResolvedValue(health);
    const { container } = render(<DayHealthStrip tripId="trip-1" day="2026-11-11" />);
    await waitFor(() => expect(apiMock).toHaveBeenCalled());
    expect(container.querySelector("section")).toBeNull();
  });

  it("stays quiet when the day is not in the answer", async () => {
    apiMock.mockResolvedValue(health);
    const { container } = render(<DayHealthStrip tripId="trip-1" day="2026-12-01" />);
    expect(container.querySelector("section")).toBeNull();
  });
});
