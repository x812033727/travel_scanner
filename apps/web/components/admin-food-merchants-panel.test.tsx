import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
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
  platform_link: {
    id: "platform-1",
    provider: "openrice",
    provider_label: "OpenRice",
    canonical_url: "https://www.openrice.com/en/hongkong/p-yat-lok-restaurant-p23206360",
    localized_urls: {},
    status: "verified",
    checked_at: "2026-09-08T00:00:00Z",
    checked_by_user_id: null,
    review_note: "Exact merchant page",
  },
  expected_platform: { provider: "openrice", label: "OpenRice" },
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
  it("traps editor focus, blocks background replacement and busy Escape, then restores focus and scroll", async () => {
    let finish: (response: Response) => void = () => undefined;
    const second = { ...merchant, id: "22222222-2222-4222-8222-222222222222", name: "Second merchant" };
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const stub = taxonomyResponse(String(input));
      if (stub) return stub;
      if (init?.method === "PUT") return new Promise<Response>((resolve) => { finish = resolve; });
      return new Response(JSON.stringify({ items: [merchant, second], total: 2 }));
    }));
    const originalOverflow = document.body.style.overflow;
    render(<AdminFoodMerchantsPanel />);
    await screen.findByText(merchant.name);
    const [opener, otherEditor] = screen.getAllByRole("button", { name: "編輯地點與來源" }) as HTMLButtonElement[];
    const add = screen.getByRole("button", { name: "新增店家" }) as HTMLButtonElement;
    opener.focus();
    fireEvent.click(opener);
    const dialog = screen.getByRole("dialog");
    const close = within(dialog).getByRole("button", { name: "關閉" });
    const saveMerchant = within(dialog).getByRole("button", { name: "儲存店家地點" });
    expect(document.activeElement).toBe(close);
    expect(document.body.style.overflow).toBe("hidden");
    expect(opener.closest("[inert]")).not.toBeNull();
    expect(otherEditor.disabled).toBe(true);
    expect(add.disabled).toBe(true);
    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(saveMerchant);
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(close);

    fireEvent.change(within(dialog).getByLabelText("查核備註"), { target: { value: "Retained keyboard draft" } });
    fireEvent.click(otherEditor);
    fireEvent.click(add);
    expect(screen.getByRole("dialog")).toBe(dialog);
    expect((within(dialog).getByLabelText("查核備註") as HTMLInputElement).value).toBe("Retained keyboard draft");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(within(dialog).getByText("尚有未儲存的訂位平台草稿，關閉後會遺失。")).toBeTruthy();
    fireEvent.click(within(dialog).getByRole("button", { name: "繼續編輯" }));

    fireEvent.click(within(dialog).getByRole("button", { name: "只儲存訂位平台" }));
    fireEvent.keyDown(document, { key: "Escape" });
    fireEvent.click(otherEditor);
    fireEvent.click(add);
    expect(screen.getByRole("dialog")).toBe(dialog);
    expect(within(dialog).queryByText("尚有未儲存的訂位平台草稿，關閉後會遺失。")).toBeNull();
    await act(async () => finish(new Response(JSON.stringify({ ...merchant, platform_link: { ...merchant.platform_link, review_note: "Retained keyboard draft" } }))));
    await within(dialog).findByText("已儲存 OpenRice 的訂位平台資料。");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(opener);
    expect(document.body.style.overflow).toBe(originalOverflow);
    expect(opener.closest("[inert]")).toBeNull();
  });

  it("saves a platform without saving or refreshing dirty merchant fields, and keeps the other provider", async () => {
    const inline = { ...merchant.platform_link, id: "platform-2", provider: "inline", provider_label: "inline", canonical_url: "https://inline.app/booking/company:1/branch1" };
    const initial = { ...merchant, platform_links: [merchant.platform_link, inline] };
    let finish: (response: Response) => void = () => undefined;
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const stub = taxonomyResponse(String(input));
      if (stub) return stub;
      if (init?.method === "PUT") return new Promise<Response>((resolve) => { finish = resolve; });
      return new Response(JSON.stringify({ items: [initial], total: 1, available_platforms: [{ provider: "openrice", label: "OpenRice" }, { provider: "inline", label: "inline" }] }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminFoodMerchantsPanel />);
    await screen.findByText(merchant.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    const dialog = screen.getByRole("dialog");
    const section = within(dialog).getByRole("region", { name: "旅客訂位平台" });
    const provider = within(section).getByLabelText("訂位平台");
    expect(provider.querySelectorAll("option").length).toBe(2);
    const name = within(dialog).getByRole("textbox", { name: /^店名$/ }) as HTMLInputElement;
    const map = within(dialog).getByLabelText("Google Place ID") as HTMLInputElement;
    const source = within(dialog).getByLabelText("來源標題") as HTMLInputElement;
    fireEvent.change(name, { target: { value: "Dirty merchant name" } });
    fireEvent.change(map, { target: { value: "ChIJ-dirty" } });
    fireEvent.change(source, { target: { value: "Dirty source evidence" } });
    fireEvent.change(within(section).getByLabelText("查核結果"), { target: { value: "disabled" } });
    const listingCalls = () => fetchMock.mock.calls.filter(([url]) => String(url).includes("/merchants?"));
    const before = listingCalls().length;
    fireEvent.click(within(section).getByRole("button", { name: "只儲存訂位平台" }));
    expect((within(dialog).getByRole("button", { name: "關閉" }) as HTMLButtonElement).disabled).toBe(true);
    expect((within(dialog).getByRole("button", { name: "儲存店家地點" }) as HTMLButtonElement).disabled).toBe(true);
    await act(async () => finish(new Response(JSON.stringify({ ...merchant, name: "Server name", sources: [], google_place_id: "Server map", platform_links: [{ ...merchant.platform_link, status: "disabled" }, inline], platform_link: { ...merchant.platform_link, status: "disabled" } }))));
    await within(section).findByText("已儲存 OpenRice 的訂位平台資料。");
    expect(name.value).toBe("Dirty merchant name");
    expect(map.value).toBe("ChIJ-dirty");
    expect(source.value).toBe("Dirty source evidence");
    expect(screen.getByRole("dialog")).toBe(dialog);
    expect(listingCalls().length).toBe(before);
    const writes = fetchMock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET");
    expect(writes).toHaveLength(1);
    expect(writes[0][1]?.method).toBe("PUT");
    expect(JSON.parse(String(writes[0][1]?.body))).toMatchObject({ provider: "openrice", status: "disabled", expected_checked_at: merchant.platform_link.checked_at });
    fireEvent.change(provider, { target: { value: "inline" } });
    expect((within(section).getByLabelText("查核結果") as HTMLSelectElement).value).toBe("verified");
  });

  it("never implicitly saves platform drafts with the merchant and warns before discarding them", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const stub = taxonomyResponse(String(input));
      if (stub) return stub;
      if (init?.method === "PATCH") return new Response(JSON.stringify({ ...merchant, ...JSON.parse(String(init.body)) }));
      return new Response(JSON.stringify({ items: [merchant], total: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminFoodMerchantsPanel />);
    await screen.findByText(merchant.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    fireEvent.change(screen.getByLabelText("查核備註"), { target: { value: "Unsaved platform evidence" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存店家地點" }));
    await screen.findByText(/已儲存店家地點/);
    await waitFor(() => expect((screen.getByRole("button", { name: "關閉" }) as HTMLButtonElement).disabled).toBe(false));
    expect((screen.getByLabelText("查核備註") as HTMLInputElement).value).toBe("Unsaved platform evidence");
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "PATCH")).toHaveLength(1);
    expect(fetchMock.mock.calls.some(([, init]) => init?.method === "PUT")).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: "關閉" }));
    expect(screen.getByText("尚有未儲存的訂位平台草稿，關閉後會遺失。")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "繼續編輯" }));
    expect((screen.getByLabelText("查核備註") as HTMLInputElement).value).toBe("Unsaved platform evidence");
  });

  it("preserves the supplemental Google identity when saving a Korean NAVER location", async () => {
    const korean = { ...merchant, country_code: "KR", destination_id: "seoul", naver_map_url: "https://map.naver.com/p/entry/place/123", google_place_id: "ChIJ-korea-confirmed", map_match_status: "verified" };
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const stub = taxonomyResponse(String(input));
      if (stub) return stub;
      if (init?.method === "PATCH") return new Response(JSON.stringify({ ...korean, ...JSON.parse(String(init.body)) }));
      return new Response(JSON.stringify({ items: [korean], total: 1, page: 1, pages: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminFoodMerchantsPanel />);
    await screen.findByText(korean.name);
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    expect((screen.getByLabelText("Google Place ID") as HTMLInputElement).value).toBe("ChIJ-korea-confirmed");
    fireEvent.change(screen.getByLabelText("Naver 精準地點頁"), { target: { value: "https://map.naver.com/p/entry/place/456" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存店家地點" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "PATCH")).toBe(true));
    const [, init] = fetchMock.mock.calls.find(([, init]) => init?.method === "PATCH")!;
    expect(JSON.parse(String(init?.body))).toMatchObject({ naver_map_url: "https://map.naver.com/p/entry/place/456", map_match_status: "verified" });
    expect(JSON.parse(String(init?.body))).not.toHaveProperty("google_place_id");
    await screen.findByText(/已儲存店家地點/);
  });

  it.each(["", "pending"])("sends the requested review filter %s for searches and explicit reloads", async (initialStatus) => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const stub = taxonomyResponse(String(input));
      if (stub) return stub;
      if (init?.method === "POST") return new Response(JSON.stringify({ updated: 1 }));
      return new Response(JSON.stringify({ items: [merchant], total: 1, page: 1, pages: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminFoodMerchantsPanel initialStatus={initialStatus} />);
    await screen.findByText(merchant.name);
    const listingCalls = () => fetchMock.mock.calls.filter(([url]) => String(url).includes("/merchants?"));
    expect(new URL(String(listingCalls()[0][0]), "https://test.local").searchParams.get("status")).toBe(initialStatus || null);
    fireEvent.change(screen.getByRole("textbox", { name: "店家搜尋" }), { target: { value: "燒鵝" } });
    await waitFor(() => expect(listingCalls().some(([url]) => new URL(String(url), "https://test.local").searchParams.get("q") === "燒鵝")).toBe(true));
    expect(listingCalls().every(([url]) => new URL(String(url), "https://test.local").searchParams.get("status") === (initialStatus || null))).toBe(true);
    fireEvent.click(screen.getByRole("checkbox", { name: `選取 ${merchant.name}` }));
    fireEvent.click(screen.getByRole("button", { name: /批次停用/ }));
    await waitFor(() => expect(listingCalls().length).toBeGreaterThanOrEqual(3));
    expect(new URL(String(listingCalls().at(-1)![0]), "https://test.local").searchParams.get("status")).toBe(initialStatus || null);
    fireEvent.change(screen.getByRole("combobox", { name: "審核狀態" }), { target: { value: "approved" } });
    await waitFor(() => expect(new URL(String(listingCalls().at(-1)![0]), "https://test.local").searchParams.get("status")).toBe("approved"));
  });

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
    expect(within(editor).getByText("旅客訂位平台")).toBeTruthy();
    expect(within(editor).getByDisplayValue("OpenRice")).toBeTruthy();
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

  it("can save an exact Naver URL before a pending merchant has source evidence", async () => {
    const pendingKoreanMerchant = {
      ...merchant,
      name: "Jinokhwa Halmae Wonjo Dakhanmari",
      local_name: "진옥화할매원조닭한마리",
      destination_id: "seoul",
      country_code: "KR",
      google_place_id: null,
      naver_map_url: null,
      latitude: null,
      longitude: null,
      coordinate_source_type: null,
      coordinate_source_url: null,
      sources: [],
    };
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        const stub = taxonomyResponse(url);
        if (stub) return stub;
        if (init?.method === "PATCH") {
          const body = JSON.parse(String(init.body));
          expect(body.naver_map_url).toBe("https://map.naver.com/p/entry/place/11619295");
          expect(body).not.toHaveProperty("sources");
          return new Response(JSON.stringify({ ...pendingKoreanMerchant, ...body }));
        }
        return new Response(
          JSON.stringify({ items: [pendingKoreanMerchant], total: 1, page: 1, pages: 1 }),
        );
      }),
    );

    render(<AdminFoodMerchantsPanel />);
    expect(await screen.findByText("Jinokhwa Halmae Wonjo Dakhanmari")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "編輯地點與來源" }));
    expect(
      screen
        .getByRole("link", { name: "開啟 Naver 搜尋並人工核對" })
        .getAttribute("href"),
    ).toBe(
      `https://map.naver.com/p/search/${encodeURIComponent("진옥화할매원조닭한마리 서울")}`,
    );
    fireEvent.change(screen.getByLabelText("Naver 精準地點頁"), {
      target: { value: "https://map.naver.com/p/entry/place/11619295" },
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
