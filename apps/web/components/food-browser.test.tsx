import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { FoodMerchant } from "@/lib/foods";
import { FoodBrowser } from "./food-browser";
import { SavedItemsProvider } from "./saved-items-provider";

const cities = {
  total_merchants: 1,
  countries: [
    {
      code: "JP",
      name: "日本",
      merchant_count: 1,
      cities: [
        {
          id: "tokyo",
          name: "東京",
          local_name: null,
          english_name: "Tokyo",
          country_code: "JP",
          role: "primary",
          parent_destination_id: null,
          merchant_count: 1,
          area_count: 4,
        },
        {
          id: "kanazawa",
          name: "金澤",
          local_name: "金沢",
          english_name: "Kanazawa",
          country_code: "JP",
          role: "secondary",
          parent_destination_id: null,
          merchant_count: 0,
          area_count: 4,
        },
      ],
    },
  ],
};
const categories = {
  items: [
    { slug: "ramen", name: "拉麵", merchant_count: 1 },
    { slug: "sushi", name: "壽司", merchant_count: 0 },
  ],
};
const ichiran: FoodMerchant = {
  id: "merchant-1",
  slug: "tokyo-ichiran-shibuya",
  name: "Ichiran Shibuya",
  local_name: "一蘭 渋谷店",
  destination_id: "tokyo",
  destination_name: "東京",
  country_code: "JP",
  area: { id: "area-1", slug: "tokyo-shibuya", name: "澀谷", local_name: "渋谷" },
  categories: [{ slug: "ramen", name: "拉麵", is_primary: true }],
  signature_dishes: [
    {
      food_id: "food-jp-ramen",
      slug: "jp-ramen",
      name: "拉麵",
      local_name: "ラーメン",
      food_kind: "noodle_soup",
      meal_types: ["lunch", "dinner"],
    },
  ],
  address: "Shibuya",
  latitude: 35.66,
  longitude: 139.7,
  coordinate_source: { type: "official_tourism", url: "https://www.gotokyo.org/", verified_at: null },
  official_website_url: null,
  map_links: [
    {
      provider: "google",
      label: "Google Maps",
      url: "https://www.google.com/maps/search/?api=1&query=Ichiran&query_place_id=ChIJ1",
      primary: true,
    },
  ],
  verified_at: "2026-09-01T00:00:00Z",
  sources: [],
};
const second: FoodMerchant = {
  ...ichiran,
  id: "merchant-2",
  slug: "tokyo-second",
  name: "Second Shop",
  local_name: "二番",
  area: null,
  categories: [{ slug: "sushi", name: "壽司", is_primary: true }],
};
const tokyoFacets = {
  areas: [
    { id: "area-1", slug: "tokyo-shibuya", name: "澀谷", local_name: "渋谷", merchant_count: 1 },
    { id: "area-2", slug: "tokyo-shinjuku", name: "新宿", local_name: "新宿", merchant_count: 0 },
  ],
  unassigned_area_count: 1,
  categories: [
    { slug: "ramen", name: "拉麵", merchant_count: 1 },
    { slug: "sushi", name: "壽司", merchant_count: 1 },
  ],
};
const dish = {
  id: "food-1",
  slug: "kr-bibimbap",
  country_code: "KR",
  country_name: "韓國",
  name: "韓式拌飯",
  local_name: "비빔밥",
  romanized_name: "Bibimbap",
  summary: "以米飯、蔬菜與醬料拌勻的韓國代表料理。",
  food_kind: "main",
  meal_types: ["lunch"],
  ingredient_tags: [],
  dietary_notes: [],
  source_urls: [],
  destinations: [],
  food_hotspots: [],
  recommended_merchants: [],
};

function stubFetch(options: { failFirstMerchants?: boolean } = {}) {
  const calls: string[] = [];
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    calls.push(url);
    if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
    if (url.includes("/foods/cities")) return new Response(JSON.stringify(cities));
    if (url.includes("/foods/categories")) return new Response(JSON.stringify(categories));
    if (url.includes("/foods/merchants?")) {
      const merchantCalls = calls.filter((item) => item.includes("/foods/merchants?")).length;
      if (options.failFirstMerchants && merchantCalls === 1) {
        return new Response(JSON.stringify({ code: "internal_error", detail: "boom" }), {
          status: 500,
        });
      }
      const params = new URL(url, "http://localhost").searchParams;
      if (params.get("destination_id") === "kanazawa") {
        return new Response(
          JSON.stringify({
            total: 0,
            has_more: false,
            next_cursor: null,
            items: [],
            facets: { areas: [], unassigned_area_count: 0, categories: [] },
          }),
        );
      }
      if (params.get("cursor")) {
        return new Response(
          JSON.stringify({
            total: 2,
            has_more: false,
            next_cursor: null,
            items: [second],
            facets: tokyoFacets,
          }),
        );
      }
      return new Response(
        JSON.stringify({
          total: 2,
          has_more: true,
          next_cursor: "MQ",
          items: [ichiran],
          facets: tokyoFacets,
        }),
      );
    }
    if (url.includes("/foods?")) {
      return new Response(
        JSON.stringify({ total: 1, has_more: false, next_cursor: null, items: [dish] }),
      );
    }
    return new Response(JSON.stringify({}), { status: 404 });
  });
  vi.stubGlobal("fetch", fetchMock);
  return { fetchMock, calls };
}

function renderBrowser(path: string, options: { failFirstMerchants?: boolean } = {}) {
  window.history.replaceState({}, "", path);
  const stub = stubFetch(options);
  render(
    <SavedItemsProvider>
      <FoodBrowser />
    </SavedItemsProvider>,
  );
  return stub;
}

describe("FoodBrowser", () => {
  it("hydrates the city, area and cuisine from the URL", async () => {
    const { calls } = renderBrowser("/foods?destination_id=tokyo&area=tokyo-shibuya&category=ramen");

    expect(await screen.findByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
    const merchantCall = calls.find((url) => url.includes("/foods/merchants?"));
    expect(merchantCall).toContain("destination_id=tokyo");
    expect(merchantCall).toContain("area=tokyo-shibuya");
    expect(merchantCall).toContain("category=ramen");
    expect(screen.getByRole("button", { name: /澀谷/, pressed: true })).toBeTruthy();
    expect(screen.getByRole("button", { name: /拉麵/, pressed: true })).toBeTruthy();
    expect(screen.getByRole("button", { name: /其他區域/ })).toBeTruthy();
    expect((screen.getByRole("combobox", { name: "城市" }) as HTMLSelectElement).value).toBe(
      "tokyo",
    );
  });

  it("cascades city, area and cuisine into the query string", async () => {
    renderBrowser("/foods");

    fireEvent.click(await screen.findByRole("button", { name: "東京 · 1 間店家" }));
    await waitFor(() => expect(window.location.search).toContain("destination_id=tokyo"));
    expect(await screen.findByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /澀谷/, pressed: false }));
    await waitFor(() => expect(window.location.search).toContain("area=tokyo-shibuya"));
    fireEvent.click(screen.getByRole("button", { name: /壽司/, pressed: false }));
    await waitFor(() => expect(window.location.search).toContain("category=sushi"));
    fireEvent.change(screen.getByRole("combobox", { name: "城市" }), {
      target: { value: "kanazawa" },
    });
    await waitFor(() => expect(window.location.search).toContain("destination_id=kanazawa"));
    expect(window.location.search).not.toContain("area=");
    expect(window.location.search).toContain("category=sushi");
  });

  it("falls back to signature dishes when a city has no verified merchant", async () => {
    renderBrowser("/foods?destination_id=kanazawa");

    expect(await screen.findByRole("heading", { name: "先看國民美食" })).toBeTruthy();
    expect(await screen.findByRole("heading", { name: "韓式拌飯" })).toBeTruthy();
    expect(screen.getByText("金澤 的店家仍在核對中")).toBeTruthy();
  });

  it("loads the next page with the cursor", async () => {
    const { calls } = renderBrowser("/foods?destination_id=tokyo");

    expect(await screen.findByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "載入更多" }));
    expect(await screen.findByRole("heading", { name: "Second Shop" })).toBeTruthy();
    expect(calls.some((url) => url.includes("cursor=MQ"))).toBe(true);
    expect(screen.getByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
  });

  it("shows an alert and retries after a failed request", async () => {
    renderBrowser("/foods?destination_id=tokyo", { failFirstMerchants: true });

    expect(await screen.findByRole("alert")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "重新載入" }));
    expect(await screen.findByRole("heading", { name: "Ichiran Shibuya" })).toBeTruthy();
    expect(screen.queryByRole("alert")).toBeNull();
  });
});
