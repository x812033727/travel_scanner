import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { FlightOfferCard, type FlightCardOffer } from "./flight-offer-card";

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const offer: FlightCardOffer = {
  id: "flight-1",
  provider: "skyscanner",
  source_mode: "live",
  marketing_airline: "星宇航空",
  operating_airlines: ["星宇航空"],
  selling_agent: "測試售票平台",
  origin: "TPE",
  destination: "NRT",
  departure_time: "2026-11-10T08:00:00+08:00",
  arrival_time: "2026-11-10T12:00:00+09:00",
  return_departure_time: "2026-11-15T13:00:00+09:00",
  return_arrival_time: "2026-11-15T16:00:00+08:00",
  segments: [
    { origin: "TPE", destination: "NRT", departure_time: "2026-11-10T08:00:00+08:00", arrival_time: "2026-11-10T12:00:00+09:00", airline: "星宇航空", flight_number: "JX800", leg_index: 0 },
    { origin: "NRT", destination: "TPE", departure_time: "2026-11-15T13:00:00+09:00", arrival_time: "2026-11-15T16:00:00+08:00", airline: "星宇航空", flight_number: "JX801", leg_index: 1 },
  ],
  total_price: 15000,
  clickout_available: true,
  checked_baggage_kg: 23,
  last_verified_at: "2026-08-31T08:00:00Z",
};

describe("FlightOfferCard", () => {
  beforeEach(() => apiMock.mockReset());

  it("shows carrier, agent, baggage, attribution and secure clickout form", () => {
    const { container } = render(
      <FlightOfferCard offer={offer} fallbackUrl="https://example.test/recheck" />,
    );
    expect(screen.getByRole("heading", { name: "星宇航空" })).toBeTruthy();
    expect(screen.getByText(/實際承運：星宇航空/)).toBeTruthy();
    expect(screen.getByText(/售票端：測試售票平台/)).toBeTruthy();
    expect(screen.getByText(/托運 23 kg/)).toBeTruthy();
    expect(screen.getByText("08:00")).toBeTruthy();
    expect(screen.getByText("12:00")).toBeTruthy();
    expect(screen.getByText("13:00")).toBeTruthy();
    expect(screen.getByText("16:00")).toBeTruthy();
    expect(screen.getByText(/Powered by/)).toBeTruthy();
    expect(container.querySelector("form")?.getAttribute("action")).toBe(
      "/api/travel/offers/flight-1/clickout",
    );
  });

  it("expands outbound and return flight numbers without inventing missing data", () => {
    render(<FlightOfferCard offer={offer} fallbackUrl="https://example.test/recheck" />);
    fireEvent.click(screen.getByRole("button", { name: "查看詳細班次" }));
    expect(screen.getAllByText(/JX800/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/JX801/).length).toBeGreaterThan(0);
  });

  it("refreshes a persisted offer through the BFF", async () => {
    apiMock.mockResolvedValue({
      new_price: 14800,
      price_change: -200,
      still_available: true,
      refreshed_at: "2026-08-31T09:00:00Z",
    });
    render(<FlightOfferCard offer={offer} fallbackUrl="https://example.test/recheck" />);
    fireEvent.click(screen.getByRole("button", { name: "重新驗價" }));
    await waitFor(() => expect(apiMock).toHaveBeenCalledWith(
      "/offers/flight-1/refresh",
      { method: "POST" },
    ));
    expect(screen.getByText(/已更新為供應商最新價格/)).toBeTruthy();
  });

  it("creates a price alert with the displayed price", async () => {
    apiMock.mockResolvedValue({ id: "alert-1" });
    render(<FlightOfferCard offer={offer} fallbackUrl="https://example.test/recheck" />);
    fireEvent.click(screen.getByRole("button", { name: "建立價格通知" }));
    fireEvent.click(screen.getByRole("button", { name: "確認建立" }));
    await waitFor(() => expect(apiMock).toHaveBeenCalledWith(
      "/alerts",
      { method: "POST", body: JSON.stringify({ resource_type: "flight", resource_id: "flight-1", target_price: 15000 }) },
    ));
    expect(screen.getByText(/價格通知已建立/)).toBeTruthy();
  });
});
