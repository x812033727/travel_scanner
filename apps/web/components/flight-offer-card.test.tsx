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
    expect(screen.getByText(/Powered by/)).toBeTruthy();
    expect(container.querySelector("form")?.getAttribute("action")).toBe(
      "/api/travel/offers/flight-1/clickout",
    );
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
});
