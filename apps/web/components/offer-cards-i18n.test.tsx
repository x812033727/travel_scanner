import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { FlightOfferCard, type FlightCardOffer } from "./flight-offer-card";
import { HotelOfferCard, type HotelOfferView } from "./hotel-offer-card";

/**
 * These two cards are the end of the search: the reader decides here whether a
 * fare is refundable, sold out, live or merely estimated. Every other test in
 * this folder gets the zh-TW catalog from vitest.setup.tsx, so a literal and a
 * translation look the same. Here the catalog echoes its key and the fixtures
 * carry no Chinese of their own, so any Han left on screen is the card's.
 */
vi.mock("next-intl", () => ({
  useLocale: () => "en",
  useFormatter: () => ({ number: (value: number) => String(value) }),
  useTranslations: (namespace: string) =>
    Object.assign((key: string) => `[${namespace}.${key}]`, { has: () => true }),
}));

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const flight: FlightCardOffer = {
  id: "flight-1",
  provider: "skyscanner",
  source_mode: "live",
  marketing_airline: "Starlux",
  operating_airlines: ["Starlux"],
  selling_agent: "Test seller",
  origin: "TPE",
  destination: "NRT",
  departure_time: "2026-11-10T08:00:00+08:00",
  arrival_time: "2026-11-10T12:30:00+09:00",
  segments: [
    { origin: "TPE", destination: "HKG", departure_time: "2026-11-10T08:00:00+08:00", arrival_time: "2026-11-10T09:40:00+08:00", airline: "Starlux", flight_number: "JX800", leg_index: 0 },
    { origin: "HKG", destination: "NRT", departure_time: "2026-11-10T11:00:00+08:00", arrival_time: "2026-11-10T12:30:00+09:00", airline: "Starlux", flight_number: "JX802", leg_index: 0 },
  ],
  total_price: 15000,
  currency: "TWD",
  base_price: 12000,
  taxes: 2500,
  fees: 500,
  refundable: false,
  changeable: false,
  checked_baggage_kg: 23,
  last_verified_at: "2026-08-31T08:00:00Z",
  expires_at: "2026-08-31T20:00:00Z",
  emissions_kg_per_pax: 412.5,
  clickout_available: true,
  status_details: [{ ident: "JX800", schedule_only: false, status: "En route", departure_delay_seconds: 900, departure_terminal: "1", departure_gate: "A5" }],
};

const hotel: HotelOfferView = {
  id: "hotel-1",
  hotel_name: "Shinjuku Test Hotel",
  provider: "amadeus",
  source_mode: "live",
  room_type: "Deluxe twin",
  nights: 2,
  base_price: 8000,
  taxes: 800,
  fees: 200,
  total_price: 9000,
  currency: "TWD",
  breakfast_included: false,
  refundable: false,
  station_walk_minutes: 5,
  address: "Shinjuku, Tokyo",
  distance_to_center_km: 1.2,
  rating: 4,
  review_score: 4.7,
  review_count: 321,
  amenities: ["Wi-Fi"],
  retrieved_at: "2026-08-31T08:00:00Z",
  expires_at: "2026-08-31T08:30:00Z",
  freshness_status: "expired",
  is_fallback: true,
  action_kind: "recheck",
};

function offendingRun() {
  const labels = [...document.querySelectorAll("[aria-label], [alt]")]
    .flatMap((node) => [node.getAttribute("aria-label"), node.getAttribute("alt")])
    .filter(Boolean)
    .join(" ");
  return `${document.body.textContent ?? ""} ${labels}`.match(/\p{Script=Han}+/u)?.[0];
}

describe("the offer cards in a language that is not Chinese", () => {
  beforeEach(() => {
    apiMock.mockReset();
    // formatCurrency and toLocaleString read the document language, not the hook.
    document.documentElement.lang = "en";
  });

  it("writes no Chinese of its own on a flight, open or collapsed", async () => {
    render(<FlightOfferCard offer={flight} fallbackUrl="https://example.test/recheck" />);

    expect(screen.getByText("[search.results.flightCard.liveHeading]")).toBeTruthy();
    // "1 stop" and the leg duration are computed, so they are easy to leave behind.
    expect(document.body.textContent).toContain("[search.results.stops]");
    expect(document.body.textContent).toContain("[search.results.flightCard.durationHoursMinutes]");
    // Refundability and changeability are what the reader is deciding on.
    expect(document.body.textContent).toContain("[search.results.flightCard.nonRefundable]");
    expect(document.body.textContent).toContain("[search.results.flightCard.nonChangeable]");
    expect(offendingRun(), "hardcoded copy on the collapsed flight card").toBeUndefined();

    fireEvent.click(screen.getByRole("button", { name: "[search.results.flightCard.showSegments]" }));
    expect(document.body.textContent).toContain("[search.results.flightCard.layover]");
    expect(offendingRun(), "hardcoded copy on the expanded flight card").toBeUndefined();
  });

  it("says a fare sold out without falling back to Chinese", async () => {
    apiMock.mockResolvedValue({ new_price: 15600, price_change: 600, still_available: false, refreshed_at: "2026-08-31T09:00:00Z" });
    render(<FlightOfferCard offer={flight} fallbackUrl="https://example.test/recheck" />);

    fireEvent.click(screen.getByRole("button", { name: "[search.results.flightCard.verify]" }));
    await waitFor(() => expect(screen.getByRole("status").textContent).toBe("[search.results.flightCard.refreshSoldOut]"));
    expect(offendingRun(), "hardcoded copy after re-checking a price").toBeUndefined();
  });

  it("writes no Chinese of its own on an expired hotel quote", () => {
    render(<HotelOfferCard offer={hotel} actionUrl="https://hotel.example/offer" />);

    // The four source labels used to be a second, untranslated copy in this file.
    expect(screen.getByText("[search.results.source.live]")).toBeTruthy();
    for (const key of ["priceRoom", "priceTaxes", "priceTotal", "breakfastUnknown", "nonRefundable", "expired"]) {
      expect(document.body.textContent, key).toContain(`[search.results.hotelCard.${key}]`);
    }
    expect(offendingRun(), "hardcoded copy on the hotel card").toBeUndefined();
  });
});
