import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminFoodMerchantsPanel } from "./admin-food-merchants-panel";

const merchant = {
  id: "11111111-1111-4111-8111-111111111111",
  slug: "hong-kong-yat-lok",
  destination_id: "hong-kong",
  country_code: "HK",
  name: "Yat Lok Restaurant",
  local_name: "一樂燒鵝",
  address: "Hong Kong",
  latitude: 22.2821,
  longitude: 114.1556,
  plus_code_global: null,
  coordinate_source_type: "merchant_official",
  coordinate_source_url: "https://example.test/yat-lok",
  coordinate_verified_at: null,
  google_place_id: "ChIJ-yat-lok",
  naver_map_url: null,
  official_website_url: null,
  official_website_verified_at: null,
  map_match_status: "unverified",
  review_status: "pending",
  is_active: false,
  foods: [{ id: "food-1", slug: "hk-roast-goose", name: "燒鵝" }],
  sources: [{
    id: "source-1",
    source_type: "official_tourism",
    source_scope: "destination_context",
    source_title: "Official destination food guide (regional context only)",
    source_url: "https://tourism.example/hong-kong/dining",
    claims: [],
    edition_year: null,
    distinction: null,
    is_current: true,
  }],
};

describe("AdminFoodMerchantsPanel", () => {
  it("shows unavailable auto matching and computes Plus Code from permanent coordinates", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("map-candidates")) {
        return new Response(JSON.stringify({ configured: false, candidates: [], reason: "google_places_not_configured", message: "Google Places 金鑰未設定" }));
      }
      if (url.includes("plus-code-preview")) {
        return new Response(JSON.stringify({ plus_code_global: "7PJP75J4+R6" }));
      }
      if (init?.method === "PATCH") {
        const body = JSON.parse(String(init.body));
        expect(body.google_place_id).toBe("ChIJ-yat-lok");
        expect(body.coordinate_source_type).toBe("merchant_official");
        expect(body.official_website_url).toBe("https://restaurant.example/");
        expect(body.sources).toEqual(expect.arrayContaining([
          expect.objectContaining({
            source_scope: "merchant_website",
            source_url: "https://restaurant.example/",
            claims: ["display_name", "official_website"],
          }),
        ]));
        return new Response(JSON.stringify(merchant));
      }
      return new Response(JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }));
    }));

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Yat Lok Restaurant")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    fireEvent.click(screen.getByRole("button", { name: "搜尋 Google 候選" }));
    expect(await screen.findByText("Google Places 金鑰未設定")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "預覽 Plus Code" }));
    expect(await screen.findByText("7PJP75J4+R6")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("店家官方網站"), {
      target: { value: "https://restaurant.example/" },
    });
    fireEvent.click(screen.getByRole("button", { name: "新增直接來源" }));
    const titles = screen.getAllByLabelText("來源標題");
    const urls = screen.getAllByLabelText("HTTPS 來源網址");
    fireEvent.change(titles[titles.length - 1], { target: { value: "Restaurant website" } });
    fireEvent.change(urls[urls.length - 1], {
      target: { value: "https://restaurant.example/" },
    });
    fireEvent.click(screen.getByRole("button", { name: "儲存並重算 Plus Code" }));
    expect(await screen.findByText(/已儲存店家地點/)).toBeTruthy();
  });
});
