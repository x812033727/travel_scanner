import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { FoodItem } from "@/lib/foods";
import { FoodDishCard } from "./food-dish-card";
import { SavedItemsProvider } from "./saved-items-provider";

const food: FoodItem = {
  id: "food-1",
  slug: "kr-bibimbap",
  country_code: "KR",
  country_name: "韓國",
  name: "韓式拌飯",
  local_name: "비빔밥",
  romanized_name: "Bibimbap",
  summary: "以米飯、蔬菜與醬料拌勻的韓國代表料理。",
  food_kind: "main",
  meal_types: ["lunch", "dinner"],
  ingredient_tags: ["rice"],
  dietary_notes: [],
  source_urls: ["https://en.wikipedia.org/wiki/Bibimbap"],
  destinations: [
    {
      id: "seoul",
      name: "首爾",
      local_name: "서울",
      english_name: "Seoul",
      country_code: "KR",
      role: "primary",
      parent_destination_id: null,
    },
  ],
  food_hotspots: [
    {
      hotspot_id: "hotspot-1",
      slug: "gwangjang-market",
      name: "廣藏市場",
      local_name: "광장시장",
      destination_id: "seoul",
      latitude: 37.57,
      longitude: 126.99,
      map_links: [
        {
          provider: "naver",
          label: "Naver Map",
          url: "https://map.naver.com/p/entry/place/13304114",
          primary: true,
        },
      ],
    },
  ],
  recommended_merchants: [
    {
      merchant_id: "merchant-1",
      slug: "seoul-hankook-jib",
      name: "Hankook Jib",
      local_name: "한국집",
      destination_id: "seoul",
      address: "Seoul",
      latitude: 37.57,
      longitude: 126.99,
      map_links: [
        {
          provider: "naver",
          label: "Naver Map",
          url: "https://map.naver.com/p/entry/place/123456",
          primary: true,
        },
      ],
      verified_at: "2026-09-01T00:00:00Z",
    },
  ],
};

describe("FoodDishCard", () => {
  it("renders the localized dish, public food area, and exact merchant map link", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response(JSON.stringify({ items: [] }))),
    );
    render(
      <SavedItemsProvider>
        <FoodDishCard food={food} />
      </SavedItemsProvider>,
    );

    expect(await screen.findByRole("heading", { name: "韓式拌飯" })).toBeTruthy();
    expect(screen.getByText("비빔밥 · Bibimbap")).toBeTruthy();
    expect(screen.getByText("廣藏市場")).toBeTruthy();
    expect(screen.getByText("廣藏市場").closest("a")).toBeNull();
    expect(screen.getByText("Hankook Jib")).toBeTruthy();
    const naver = screen.getByRole("link", { name: /Naver Map/ });
    expect(naver.getAttribute("target")).toBe("_blank");
    expect(naver.getAttribute("href")).toBe("https://map.naver.com/p/entry/place/123456");
    expect(
      screen.getByRole("link", { name: "查看推薦美食區" }).getAttribute("href"),
    ).toContain("category=food");
  });
});
