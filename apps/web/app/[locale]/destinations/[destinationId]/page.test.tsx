import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import DestinationGuidePage from "./page";
import { openSiteVisibility } from "@/lib/site-features";

const mocks = vi.hoisted(() => ({
  catalog: vi.fn(), places: vi.fn(), merchants: vi.fn(), visibility: vi.fn(),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: mocks.visibility }));
vi.mock("@/lib/destinations.server", () => ({
  getDestinations: mocks.catalog, getDestination: vi.fn(),
  getGuidePlaces: mocks.places, getGuideMerchants: mocks.merchants,
}));

const tokyo = {
  id: "tokyo", city: "Tokyo", country: "Japan", countryCode: "JP", role: "primary",
  localName: null, englishName: null, parentDestinationId: null, extensionIds: [],
  areas: [], recommendedDays: null, timezone: "Asia/Tokyo", currency: "JPY", center: null, reason: "Visit Tokyo",
};
const params = Promise.resolve({ locale: "en" as const, destinationId: "tokyo" });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.catalog.mockResolvedValue([tokyo]);
  mocks.places.mockResolvedValue([{ id: "p1", name: "Reviewed shrine", detail: null }]);
  mocks.merchants.mockResolvedValue([{ id: "m1", name: "Reviewed cafe", detail: null }]);
  mocks.visibility.mockResolvedValue({ status: "ready", features: openSiteVisibility });
});

describe("destination guide publication boundaries", () => {
  it("renders current reviewed places when the feature is enabled", async () => {
    render(await DestinationGuidePage({ params }));
    expect(mocks.places).toHaveBeenCalledWith("en", "tokyo");
    expect(screen.getByText("Reviewed shrine")).toBeTruthy();
  });

  it.each(["closed", "unavailable"])("does not fetch or render hotspots when visibility is %s", async (state) => {
    mocks.visibility.mockResolvedValue({
      status: state === "unavailable" ? "unavailable" : "ready",
      features: { ...openSiteVisibility, hotspots_enabled: state === "unavailable" },
    });
    render(await DestinationGuidePage({ params }));
    expect(mocks.places).not.toHaveBeenCalled();
    expect(screen.queryByText("Reviewed shrine")).toBeNull();
    expect(screen.queryByRole("link", { name: "Browse every reviewed place" })).toBeNull();
    expect(screen.getByText("Reviewed cafe")).toBeTruthy();
  });

  it("keeps a catalog outage distinct from a missing destination without fetching lists", async () => {
    mocks.catalog.mockResolvedValue(null);
    await expect(DestinationGuidePage({ params })).rejects.toThrow("Destination catalog unavailable");
    expect(mocks.places).not.toHaveBeenCalled();
    expect(mocks.merchants).not.toHaveBeenCalled();
  });
});
