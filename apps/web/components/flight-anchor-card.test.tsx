import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { TripItem } from "@/lib/trip-types";
import { FlightAnchorCard, formatFlightMoment } from "./flight-anchor-card";

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

  it("links to the trip's flight search with the charge on the label", () => {
    render(<FlightAnchorCard item={outbound} search={{ href: "/search?trip_id=trip-1", charge: "消耗 1 次" }} />);
    const link = screen.getByRole("link", { name: "查機票 · 消耗 1 次" });
    expect(link.getAttribute("href")).toBe("/search?trip_id=trip-1");
  });

  it("puts the status, its lookup and a price alert on an anchor that has a quote", async () => {
    const quoted = {
      ...outbound,
      offer_id: "offer-1",
      data: {
        ...outbound.data,
        flight_selection_source: "offer",
        price_snapshot: { total_price: "11500", currency: "TWD", provider: "amadeus" },
        flight_status: { ident: "BR198", status: "scheduled", departure_delay_seconds: 1500, checked_at: "2026-11-09T12:00" },
      },
    };
    render(<FlightAnchorCard
      item={quoted}
      flightStatus={{ href: "/flights/status?trip_id=t1&direction=outbound", charge: "消耗 1 次" }}
      alertReturnPath="/trips/t1"
    />);

    expect(screen.getByText(/動態 scheduled/)).toBeTruthy();
    expect(screen.getByText(/延誤 25 分/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "查航班動態 · 消耗 1 次" }).getAttribute("href"))
      .toBe("/flights/status?trip_id=t1&direction=outbound");
    // The alert belongs to the quote, so it only appears where there is one.
    expect(screen.getByRole("button", { name: "建立價格通知" })).toBeTruthy();
  });

  it("moves the UTC lookup time into the reader's zone but leaves airport wall times alone", () => {
    // The zone is passed explicitly here because a vitest worker cannot repin process TZ;
    // the card itself leaves it unset and so uses the browser's zone.
    // What the API writes: datetime.now(UTC).isoformat(). 22:30 UTC is 06:30 next day in Taipei.
    expect(formatFlightMoment("zh-TW", "2026-11-09T22:30:00+00:00", "Asia/Taipei")).toBe("11/10 06:30");
    expect(formatFlightMoment("zh-TW", "2026-11-09T22:30:00Z", "Asia/Tokyo")).toBe("11/10 07:30");
    // A bare wall time is the airport's clock and must not shift with the reader.
    expect(formatFlightMoment("zh-TW", "2026-11-10T08:50", "Asia/Tokyo")).toBe("11/10 08:50");
    expect(formatFlightMoment("zh-TW", "2026-11-10T08:50", "America/Los_Angeles")).toBe("11/10 08:50");

    const checked = {
      ...outbound,
      offer_id: "offer-1",
      data: {
        ...outbound.data,
        flight_selection_source: "offer",
        price_snapshot: { total_price: "11500", currency: "TWD", provider: "amadeus" },
        flight_status: { ident: "BR198", status: "scheduled", departure_delay_seconds: 0, checked_at: "2026-11-09T22:30:00+00:00" },
      },
    };
    render(<FlightAnchorCard item={checked} />);
    // On the card the lookup time is rendered in whatever zone the test machine has, so
    // only its shape and the untouched departure time are asserted here.
    expect(screen.getByText(/查於 \d{1,2}\/\d{1,2} \d{2}:\d{2}$/)).toBeTruthy();
    expect(screen.getByText("11/10 08:50")).toBeTruthy();
  });

  it("offers no price alert and no status line on a hand-typed anchor", () => {
    render(<FlightAnchorCard item={outbound} flightStatus={{ href: "/flights/status", charge: "消耗 1 次" }} />);
    expect(screen.queryByRole("button", { name: "建立價格通知" })).toBeNull();
    // "查於" only appears on the status line; the lookup link says 查航班動態.
    expect(screen.queryByText(/查於/)).toBeNull();
    // The lookup itself still makes sense: the flight is set, its status is not known.
    expect(screen.getByRole("link", { name: /^查航班動態 · / })).toBeTruthy();
  });

  it("shows a clear setup action for an unset return flight", () => {
    render(<FlightAnchorCard item={{ ...outbound, id: "flight-return", system_role: "return_flight", data: { flight_info: null } }} onEdit={vi.fn()} />);
    expect(screen.getByText("回程航班尚未設定")).toBeTruthy();
    expect(screen.getByRole("button", { name: "設定回程航班" })).toBeTruthy();
  });
});
