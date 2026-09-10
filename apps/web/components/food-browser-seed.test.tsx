import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { FoodBrowser } from "./food-browser";
import { SavedItemsProvider } from "./saved-items-provider";

/**
 * The server-seeded merchant list.
 *
 * A separate file from food-browser.test.tsx because that one belongs to
 * 2026-09-07-merchant-style-discovery. What it covers is different anyway: this is about what
 * reaches the page before any client fetch runs.
 */

const merchant = {
  id: "merchant-1", slug: "tokyo-ichiran", name: "Ichiran Shibuya", local_name: "一蘭 渋谷店",
  destination_id: "tokyo", destination_name: "東京", country_code: "JP",
  area: { id: "a1", slug: "tokyo-shibuya", name: "澀谷", local_name: "渋谷" },
  categories: [{ slug: "ramen", name: "拉麵", is_primary: true }], styles: [], signature_dishes: [],
  address: "Shibuya", latitude: 35.66, longitude: 139.7,
  coordinate_source: null, official_website_url: null, map_links: [], reservation_links: [],
  verified_at: "2026-09-01T00:00:00Z", sources: [],
};
const seeded = { total: 1, has_more: false, next_cursor: null, items: [merchant] };
const cities = { total_merchants: 1, countries: [] };
const categories = { items: [] };

afterEach(() => { vi.unstubAllGlobals(); });

function draw(path: string, props: Record<string, unknown>) {
  window.history.replaceState({}, "", path);
  const calls: string[] = [];
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    calls.push(String(input));
    return new Response(JSON.stringify(seeded));
  });
  vi.stubGlobal("fetch", fetchMock);
  render(<SavedItemsProvider><FoodBrowser {...props} /></SavedItemsProvider>);
  return calls;
}

describe("FoodBrowser merchant seed", () => {
  it("shows the seeded merchants without waiting for a client fetch", async () => {
    const calls = draw("/foods", { initialCities: cities, initialCategories: categories, initialMerchants: seeded });
    // Present on the first paint, not after an effect resolves.
    expect(screen.getByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
    await waitFor(() => expect(calls.some((url) => url.includes("/foods/merchants"))).toBe(false));
  });

  it("still asks for its own list when the reader arrives with filters", async () => {
    // The server only seeds the unfiltered page, so a filtered arrival cannot reuse it.
    const calls = draw("/foods?destination_id=tokyo&category=ramen", {
      initialCities: cities, initialCategories: categories, initialMerchants: seeded,
    });
    await waitFor(() => expect(calls.some((url) => url.includes("destination_id=tokyo"))).toBe(true));
  });

  it("falls back to fetching when the server could not seed", async () => {
    const calls = draw("/foods", { initialCities: cities, initialCategories: categories, initialMerchants: null });
    await waitFor(() => expect(calls.some((url) => url.includes("/foods/merchants"))).toBe(true));
  });

  it("ignores a seed that is not a merchant response", async () => {
    const calls = draw("/foods", { initialCities: cities, initialCategories: categories, initialMerchants: { oops: true } });
    await waitFor(() => expect(calls.some((url) => url.includes("/foods/merchants"))).toBe(true));
  });
});
