import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { FoodExplorer } from "./food-explorer";

describe("FoodExplorer", () => {
  it("renders localized food, filters, public areas, map links, and pagination", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/foods/facets")) {
        return new Response(JSON.stringify({
          total: 70,
          countries: [{ code: "KR", name: "韓國", count: 10 }],
          destinations: [{ id: "seoul", name: "首爾", local_name: "서울", english_name: "Seoul", country_code: "KR", role: "primary", parent_destination_id: null, count: 10 }],
          food_kinds: [{ code: "main", count: 20 }],
          meal_types: [{ code: "dinner", count: 40 }],
        }));
      }
      return new Response(JSON.stringify({
        total: 10,
        has_more: true,
        next_cursor: "MTA",
        items: [{
          id: "food-1", slug: "kr-bibimbap", country_code: "KR", country_name: "韓國",
          name: "韓式拌飯", local_name: "비빔밥", romanized_name: "Bibimbap",
          summary: "以米飯、蔬菜與醬料拌勻的韓國代表料理。", food_kind: "main",
          meal_types: ["lunch", "dinner"], ingredient_tags: ["rice"], dietary_notes: [],
          source_urls: ["https://en.wikipedia.org/wiki/Bibimbap"],
          destinations: [{ id: "seoul", name: "首爾", local_name: "서울", english_name: "Seoul", country_code: "KR", role: "primary", parent_destination_id: null }],
          food_hotspots: [{ hotspot_id: "hotspot-1", slug: "gwangjang-market", name: "廣藏市場", local_name: "광장시장", destination_id: "seoul", latitude: 37.57, longitude: 126.99, map_links: [{ provider: "naver", label: "Naver Map", url: "https://map.naver.com/p/entry/place/13304114", primary: true }] }],
          recommended_merchants: [{ merchant_id: "merchant-1", slug: "seoul-hankook-jib", name: "Hankook Jib", local_name: "한국집", destination_id: "seoul", address: "Seoul", latitude: 37.57, longitude: 126.99, plus_code_global: "8Q98HXCF+2R", map_links: [{ provider: "naver", label: "Naver Map", url: "https://map.naver.com/p/entry/place/123456", primary: true }], verified_at: "2026-09-01T00:00:00Z", sources: [] }],
        }],
      }));
    }));

    render(<FoodExplorer />);
    expect(await screen.findByRole("heading", { name: "韓式拌飯" })).toBeTruthy();
    expect(screen.getByText("비빔밥 · Bibimbap")).toBeTruthy();
    expect(screen.getByText("廣藏市場")).toBeTruthy();
    expect(screen.getByText("Hankook Jib")).toBeTruthy();
    const naver = screen.getByRole("link", { name: /Naver Map/ });
    expect(naver.getAttribute("target")).toBe("_blank");
    expect(naver.getAttribute("href")).toBe("https://map.naver.com/p/entry/place/123456");
    expect(screen.getByText("廣藏市場").closest("a")).toBeNull();
    expect(screen.getByRole("link", { name: "查看推薦美食區" }).getAttribute("href")).toContain("category=food");
    expect(screen.getByRole("button", { name: "載入更多" })).toBeTruthy();
    fireEvent.change(screen.getByLabelText("全部料理類型"), { target: { value: "main" } });
    fireEvent.click(screen.getByRole("button", { name: "搜尋美食" }));
    expect(await screen.findByText("已載入 1／10 道")).toBeTruthy();
  });
});
