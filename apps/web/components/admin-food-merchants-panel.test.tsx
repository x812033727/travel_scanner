import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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
  sources: [
    {
      id: "source-1",
      source_type: "official_tourism",
      source_scope: "destination_context",
      source_title: "Official destination food guide (regional context only)",
      source_url: "https://tourism.example/hong-kong/dining",
      claims: [],
      edition_year: null,
      distinction: null,
      is_current: true,
    },
  ],
};

describe("AdminFoodMerchantsPanel", () => {
  it("shows unavailable auto matching and saves permanent coordinates", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("map-candidates")) {
          return new Response(
            JSON.stringify({
              configured: false,
              candidates: [],
              reason: "google_places_not_configured",
              message: "Google Places 金鑰未設定",
            }),
          );
        }
        if (init?.method === "PATCH") {
          const body = JSON.parse(String(init.body));
          expect(body.google_place_id).toBe("ChIJ-yat-lok");
          expect(body.coordinate_source_type).toBe("merchant_official");
          expect(body.official_website_url).toBe("https://restaurant.example/");
          expect(body.sources).toEqual(
            expect.arrayContaining([
              expect.objectContaining({
                source_scope: "merchant_website",
                source_url: "https://restaurant.example/",
                claims: ["display_name", "official_website"],
              }),
            ]),
          );
          return new Response(JSON.stringify(merchant));
        }
        return new Response(
          JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }),
        );
      }),
    );

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Yat Lok Restaurant")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    fireEvent.click(screen.getByRole("button", { name: "搜尋 Google 候選" }));
    expect(await screen.findByText("Google Places 金鑰未設定")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("店家官方網站"), {
      target: { value: "https://restaurant.example/" },
    });
    fireEvent.click(screen.getByRole("button", { name: "新增直接來源" }));
    const titles = screen.getAllByLabelText("來源標題");
    const urls = screen.getAllByLabelText("HTTPS 來源網址");
    fireEvent.change(titles[titles.length - 1], {
      target: { value: "Restaurant website" },
    });
    fireEvent.change(urls[urls.length - 1], {
      target: { value: "https://restaurant.example/" },
    });
    fireEvent.click(screen.getByRole("button", { name: "儲存店家地點" }));
    expect(await screen.findByText(/已儲存店家地點/)).toBeTruthy();
  });

  it("selects all visible merchants, filters official data, and batch verifies and activates", async () => {
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("/merchants/batch")) {
          expect(JSON.parse(String(init?.body))).toEqual({
            ids: [merchant.id],
            action: "verify_activate",
          });
          return new Response(
            JSON.stringify({ updated: 1, action: "verify_activate" }),
          );
        }
        return new Response(
          JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }),
        );
      },
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Yat Lok Restaurant")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("官方資料狀態"), {
      target: { value: "missing" },
    });
    await waitFor(() =>
      expect(
        fetchMock.mock.calls.some(([input]) =>
          String(input).includes("official_data=missing"),
        ),
      ).toBe(true),
    );
    fireEvent.click(screen.getByRole("button", { name: "全選目前項目" }));
    expect(screen.getByText("已選 1 間")).toBeTruthy();
    fireEvent.click(
      screen.getByRole("button", { name: "批次設為已驗證並啟用" }),
    );
    expect(await screen.findByText(/設為已驗證、核准並啟用/)).toBeTruthy();
  });

  it("searches Google candidates in batch and applies only the Place ID", async () => {
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("map-candidates")) {
          return new Response(
            JSON.stringify({
              configured: true,
              reason: "ok",
              candidates: [
                {
                  place_id: "ChIJ-confirmed",
                  name: "一樂燒鵝",
                  address: "Hong Kong",
                  google_maps_url:
                    "https://www.google.com/maps/search/?api=1&query_place_id=ChIJ-confirmed",
                  temporary_match_coordinates: {
                    latitude: 22.2821,
                    longitude: 114.1556,
                    expires_in_days: 30,
                    usage: "comparison_only",
                  },
                },
              ],
            }),
          );
        }
        if (init?.method === "PATCH") {
          expect(JSON.parse(String(init.body))).toEqual({
            google_place_id: "ChIJ-confirmed",
            map_match_status: "unverified",
          });
          return new Response(JSON.stringify(merchant));
        }
        return new Response(
          JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }),
        );
      },
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Yat Lok Restaurant")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "全選目前項目" }));
    fireEvent.click(
      screen.getByRole("button", { name: "批次搜尋 Google 候選" }),
    );
    const applyButton = await screen.findByRole("button", {
      name: "套用 Place ID，保留人工審核",
    });
    fireEvent.click(applyButton);
    expect(
      await screen.findByText(/已套用 Place ID，仍保留人工審核/),
    ).toBeTruthy();
  });
});
