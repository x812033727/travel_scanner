import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { TripItem } from "@/lib/trip-types";
import { FlightAnchorCard } from "./flight-anchor-card";

const outbound: TripItem = {
  id: "flight-out",
  item_type: "flight",
  day_date: "2026-11-10",
  position: 0,
  title: "長榮航空 BR 198",
  locked: true,
  fixed_time: true,
  is_estimated: false,
  system_role: "outbound_flight",
  data: {
    flight_selection_source: "manual",
    flight_info: {
      airline: "長榮航空",
      flight_number: "BR 198",
      origin: "TPE",
      destination: "NRT",
      departure_local: "2026-11-10T08:50",
      arrival_local: "2026-11-10T13:10",
      departure_timezone: "Asia/Taipei",
      arrival_timezone: "Asia/Tokyo",
      stops: 0,
    },
  },
};

describe("flight anchor card", () => {
  it("renders airport-local times and keeps the anchor outside city routing", () => {
    const edit = vi.fn();
    render(<FlightAnchorCard item={outbound} onEdit={edit} />);

    expect(screen.getByText("去程航班")).toBeTruthy();
    expect(screen.getByText("TPE")).toBeTruthy();
    expect(screen.getByText("11/10 08:50")).toBeTruthy();
    expect(screen.getByText("不計入市區路線")).toBeTruthy();
    expect(screen.getByText("直飛")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯航班" }));
    expect(edit).toHaveBeenCalledOnce();
  });

  it("shows the quote an anchor was created from, and nothing for a hand-typed flight", () => {
    const { rerender } = render(<FlightAnchorCard item={{
      ...outbound,
      data: {
        ...outbound.data,
        flight_selection_source: "provider",
        price_snapshot: { total_price: "11500", currency: "TWD", provider: "amadeus" },
      },
    }} />);
    expect(screen.getByText(/報價 NT\$11,500/)).toBeTruthy();
    expect(screen.getByText(/來源 amadeus/)).toBeTruthy();

    rerender(<FlightAnchorCard item={outbound} />);
    expect(screen.queryByText(/報價/)).toBeNull();
  });

  it("shows a clear setup action for an unset return flight", () => {
    render(<FlightAnchorCard item={{ ...outbound, id: "flight-return", system_role: "return_flight", data: { flight_info: null } }} onEdit={vi.fn()} />);
    expect(screen.getByText("回程航班尚未設定")).toBeTruthy();
    expect(screen.getByRole("button", { name: "設定回程航班" })).toBeTruthy();
  });
});
