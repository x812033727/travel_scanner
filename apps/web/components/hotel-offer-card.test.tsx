import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { HotelOfferCard, hotelNightlyPrice, hotelRating, type HotelOfferView } from "./hotel-offer-card";

const offer: HotelOfferView = {
  id: "hotel-1",
  hotel_name: "新宿測試飯店",
  provider: "amadeus",
  source_mode: "live",
  room_type: "高級雙人房",
  nights: 2,
  base_price: 8_000,
  taxes: 800,
  fees: 200,
  total_price: 9_000,
  breakfast_included: true,
  refundable: true,
  cancellation_policy: "入住前 3 天免費取消",
  station_walk_minutes: 5,
  address: "東京都新宿區",
  distance_to_center_km: 1.2,
  review_score: 4.7,
  review_count: 321,
  amenities: ["Wi-Fi", "空調"],
  retrieved_at: "2026-08-31T08:00:00Z",
  expires_at: "2026-08-31T08:30:00Z",
  action_kind: "deep_link",
};

describe("HotelOfferCard", () => {
  it("derives comparable nightly price and enriched rating", () => {
    expect(hotelNightlyPrice(offer)).toBe(4_500);
    expect(hotelRating(offer)).toBe(4.7);
  });

  it("shows nightly and total pricing, reviews and cancellation conditions", () => {
    render(<HotelOfferCard offer={offer} actionUrl="https://hotel.example/offer" />);
    expect(screen.getByRole("heading", { name: "新宿測試飯店" })).toBeTruthy();
    expect(screen.getByText(/\$4,500/)).toBeTruthy();
    expect(screen.getByText(/\$9,000/)).toBeTruthy();
    expect(screen.getByText(/4.7（321 則）/)).toBeTruthy();
    expect(screen.getByText(/入住前 3 天免費取消/)).toBeTruthy();
    expect(screen.getByRole("link", { name: /前往供應商/ }).getAttribute("href")).toBe("https://hotel.example/offer");
  });
});
