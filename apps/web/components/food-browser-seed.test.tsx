import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { FoodBrowser } from "./food-browser";
import { SavedItemsProvider } from "./saved-items-provider";
import { renderToStaticMarkup } from "react-dom/server";
import { readFoodBrowserFilters } from "@/lib/foods";

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
    // A legacy caller without initialFilters supplies a global seed, not this query's seed.
    const calls = draw("/foods?destination_id=tokyo&category=ramen", {
      initialCities: cities, initialCategories: categories, initialMerchants: seeded,
    });
    await waitFor(() => expect(calls.some((url) => url.includes("destination_id=tokyo"))).toBe(true));
  });

  it("renders a matching filtered seed and controls without another merchant request", async () => {
    const initialFilters = readFoodBrowserFilters("destination_id=tokyo&category=ramen&q=Ichiran");
    const calls = draw("/foods?destination_id=tokyo&category=ramen&q=Ichiran", {
      initialCities: cities, initialCategories: categories, initialMerchants: seeded, initialFilters,
    });
    expect(screen.getByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
    expect((screen.getByRole("textbox", { name: "搜尋店名、料理或地址" }) as HTMLInputElement).value).toBe("Ichiran");
    await waitFor(() => expect(calls.some((url) => url.includes("/foods/merchants"))).toBe(false));
  });

  it("includes the same filtered list and controls in server HTML before hydration", () => {
    const markup = renderToStaticMarkup(<SavedItemsProvider><FoodBrowser
      initialCities={cities} initialCategories={categories} initialMerchants={seeded}
      initialFilters={readFoodBrowserFilters("destination_id=tokyo&category=ramen&q=Ichiran")}
    /></SavedItemsProvider>);
    expect(markup).toContain("Ichiran Shibuya");
    expect(markup).toContain('value="Ichiran"');
  });

  it("never shows a mismatched global seed or cursor when a filtered request fails", async () => {
    window.history.replaceState({}, "", "/foods?destination_id=seoul");
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ detail: "offline" }), { status: 503 })));
    render(<SavedItemsProvider><FoodBrowser
      initialCities={cities} initialCategories={categories}
      initialMerchants={{ ...seeded, has_more: true, next_cursor: "global-cursor" }}
    /></SavedItemsProvider>);
    expect(screen.queryByRole("heading", { name: "Ichiran Shibuya" })).toBeNull();
    expect(screen.queryByRole("button", { name: "載入更多" })).toBeNull();
    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Ichiran Shibuya" })).toBeNull();
    expect(screen.queryByRole("button", { name: "載入更多" })).toBeNull();
  });

  it("does not let a late previous query replace the current matching result", async () => {
    window.history.replaceState({}, "", "/foods");
    let resolveOld!: (response: Response) => void;
    let resolveNew!: (response: Response) => void;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("q=old")) return new Promise<Response>((resolve) => { resolveOld = resolve; });
      if (url.includes("q=new")) return new Promise<Response>((resolve) => { resolveNew = resolve; });
      return Promise.resolve(new Response(JSON.stringify({ items: [] })));
    }));
    render(<SavedItemsProvider><FoodBrowser initialCities={cities} initialCategories={categories} initialMerchants={seeded} /></SavedItemsProvider>);
    const input = screen.getByRole("textbox", { name: "搜尋店名、料理或地址" });
    fireEvent.change(input, { target: { value: "old" } });
    fireEvent.click(screen.getByRole("button", { name: "搜尋店家" }));
    fireEvent.change(input, { target: { value: "new" } });
    fireEvent.click(screen.getByRole("button", { name: "搜尋店家" }));
    await act(async () => { resolveNew(new Response(JSON.stringify({ ...seeded, items: [{ ...merchant, name: "New query shop" }] }))); });
    expect(await screen.findByRole("heading", { name: "New query shop" })).toBeTruthy();
    await act(async () => { resolveOld(new Response(JSON.stringify({ ...seeded, items: [{ ...merchant, name: "Old query shop" }] }))); });
    expect(screen.getByRole("heading", { name: "New query shop" })).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Old query shop" })).toBeNull();
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
