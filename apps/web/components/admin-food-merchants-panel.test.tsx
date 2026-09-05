import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
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
  display_order: 1,
  area: null,
  area_source: null,
  categories: [{ id: "cat-1", slug: "bbq-grill", name: "燒烤／烤肉", is_primary: true, source: "seed" }],
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

const names = { "zh-TW": "中環／上環", "zh-CN": "中环／上环", en: "Central / Sheung Wan", ja: "セントラル・上環", ko: "센트럴·셩완" };
const taxonomy = {
  cities: {
    total_merchants: 0,
    countries: [
      {
        code: "HK",
        name: "香港",
        merchant_count: 0,
        cities: [{ id: "hong-kong", name: "香港", country_code: "HK", merchant_count: 0, area_count: 4 }],
      },
    ],
  },
  categories: [
    { id: "cat-1", slug: "bbq-grill", name: "燒烤／烤肉", names, is_active: true, display_order: 7, source: "seed", merchant_count: 1 },
    { id: "cat-2", slug: "cafe-tea", name: "咖啡／茶飲", names, is_active: true, display_order: 15, source: "seed", merchant_count: 0 },
  ],
  areas: [
    {
      id: "area-1",
      slug: "hong-kong-central-sheung-wan",
      destination_id: "hong-kong",
      destination_name: "香港",
      country_code: "HK",
      name: "中環／上環",
      names,
      match_terms: [],
      latitude: null,
      longitude: null,
      is_active: true,
      display_order: 1,
      source: "seed",
      merchant_count: 1,
    },
  ],
  dishes: [{ id: "food-1", slug: "hk-roast-goose", local_name: "燒鵝", country_code: "HK" }],
};

function taxonomyResponse(url: string): Response | null {
  if (url.includes("/foods/cities")) return new Response(JSON.stringify(taxonomy.cities));
  if (url.includes("/admin/foods/categories")) {
    return new Response(JSON.stringify({ items: taxonomy.categories, total: 2, page: 1, pages: 1 }));
  }
  if (url.includes("/admin/foods/areas")) {
    return new Response(JSON.stringify({ items: taxonomy.areas, total: 1, page: 1, pages: 1 }));
  }
  if (url.includes("/admin/foods?")) {
    return new Response(JSON.stringify({ items: taxonomy.dishes, total: 1, page: 1, pages: 1 }));
  }
  return null;
}

describe("AdminFoodMerchantsPanel", () => {
  it("shows unavailable auto matching and saves permanent coordinates", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        const stub = taxonomyResponse(url);
        if (stub) return stub;
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
          expect(body.area_slug).toBe("hong-kong-central-sheung-wan");
          expect(body.category_slugs).toEqual(["cafe-tea", "bbq-grill"]);
          expect(body.food_ids).toEqual(["food-1"]);
          expect(body.display_order).toBe(1);
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
    const editor = screen.getByRole("dialog");
    const areaSelect = within(editor).getByLabelText("區域");
    await waitFor(() => expect(areaSelect.querySelectorAll("option").length).toBe(2));
    fireEvent.change(areaSelect, { target: { value: "hong-kong-central-sheung-wan" } });
    fireEvent.click(screen.getByRole("checkbox", { name: "咖啡／茶飲" }));
    fireEvent.click(screen.getByRole("radio", { name: "主要 咖啡／茶飲" }));
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
        const stub = taxonomyResponse(url);
        if (stub) return stub;
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
        const stub = taxonomyResponse(url);
        if (stub) return stub;
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

  it("reports what applying an editor candidate did, and that it is not saved yet", async () => {
    const candidateResponse = (placeId: string) =>
      new Response(
        JSON.stringify({
          configured: true,
          reason: "ok",
          candidates: [
            {
              place_id: placeId,
              name: "一樂燒鵝",
              address: "Hong Kong",
              google_maps_url: "https://maps.example/",
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
    let placeId = "ChIJ-relocated";
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const stub = taxonomyResponse(url);
      if (stub) return stub;
      if (url.includes("map-candidates")) return candidateResponse(placeId);
      if (init?.method === "PATCH") throw new Error("applying must not save on its own");
      return new Response(JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Yat Lok Restaurant")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    const editor = screen.getByRole("dialog");
    const placeIdInput = within(editor).getByLabelText(
      "Google Place ID",
    ) as HTMLInputElement;
    expect(placeIdInput.value).toBe("ChIJ-yat-lok");

    fireEvent.click(within(editor).getByRole("button", { name: "搜尋 Google 候選" }));
    fireEvent.click(
      await within(editor).findByRole("button", {
        name: "套用 Place ID，保留人工審核",
      }),
    );
    expect(placeIdInput.value).toBe("ChIJ-relocated");
    expect(
      await within(editor).findByText(/已填入 Place ID.*未驗證.*儲存按鈕才會寫入/),
    ).toBeTruthy();
    expect(
      (within(editor).getByLabelText("地圖比對狀態") as HTMLSelectElement).value,
    ).toBe("unverified");

    // Re-applying the same Place ID changes nothing, and must say so rather than
    // looking like a dead button.
    placeId = "ChIJ-relocated";
    fireEvent.click(within(editor).getByRole("button", { name: "搜尋 Google 候選" }));
    fireEvent.click(
      await within(editor).findByRole("button", {
        name: "套用 Place ID，保留人工審核",
      }),
    );
    expect(
      await within(editor).findByText("欄位已經是這個 Place ID，沒有變更。"),
    ).toBeTruthy();
  });

  it("creates a merchant with destination, area, cuisine and signature dish", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const stub = taxonomyResponse(url);
      if (stub) return stub;
      if (init?.method === "POST") {
        const body = JSON.parse(String(init.body));
        expect(body.slug).toBe("hong-kong-test-shop");
        expect(body.destination_id).toBe("hong-kong");
        expect(body.country_code).toBe("HK");
        expect(body.area_slug).toBe("hong-kong-central-sheung-wan");
        expect(body.category_slugs).toEqual(["bbq-grill"]);
        expect(body.food_ids).toEqual(["food-1"]);
        expect(body.sources[0].source_url).toBe("https://tourism.example/hong-kong/dining");
        expect(body.names).toEqual({ "zh-TW": "", "zh-CN": "", en: "", ja: "テストショップ", ko: "" });
        return new Response(JSON.stringify({ ...merchant, id: "new-id", slug: body.slug }), { status: 201 });
      }
      return new Response(JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Yat Lok Restaurant")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "新增店家" }));
    const dialog = screen.getByRole("dialog");
    fireEvent.change(within(dialog).getByLabelText("Slug"), {
      target: { value: "hong-kong-test-shop" },
    });
    const destinationSelect = within(dialog).getByLabelText("目的地");
    await waitFor(() => expect(destinationSelect.querySelectorAll("option").length).toBe(2));
    fireEvent.change(destinationSelect, { target: { value: "hong-kong" } });
    fireEvent.change(within(dialog).getAllByLabelText("店名")[0], {
      target: { value: "Test Shop" },
    });
    fireEvent.change(within(dialog).getByLabelText("當地店名"), { target: { value: "測試店" } });
    fireEvent.change(within(dialog).getByLabelText("ja 名稱"), { target: { value: "テストショップ" } });
    const areaSelect = within(dialog).getByLabelText("區域");
    await waitFor(() => expect(areaSelect.querySelectorAll("option").length).toBe(2));
    fireEvent.change(areaSelect, { target: { value: "hong-kong-central-sheung-wan" } });
    fireEvent.click(screen.getByRole("checkbox", { name: "燒烤／烤肉" }));
    fireEvent.click(await screen.findByRole("checkbox", { name: "燒鵝" }));
    fireEvent.change(screen.getAllByLabelText("來源標題")[0], { target: { value: "Official guide" } });
    fireEvent.change(screen.getAllByLabelText("HTTPS 來源網址")[0], {
      target: { value: "https://tourism.example/hong-kong/dining" },
    });
    fireEvent.click(screen.getByRole("button", { name: "儲存店家地點" }));
    expect(await screen.findByText("店家已新增")).toBeTruthy();
    expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true);
  });
});
