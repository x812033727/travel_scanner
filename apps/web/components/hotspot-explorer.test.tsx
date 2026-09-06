import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SavedItemsProvider } from "./saved-items-provider";
import { HotspotExplorer } from "./hotspot-explorer";


function rankingItem(overrides: Record<string, unknown> = {}) {
  return {
    id: "hotspot-1", slug: "sensoji", rank: 1, name: "淺草寺", destination_id: "tokyo",
    destination_role: "primary", parent_destination_id: null, is_cross_city: false,
    city_code: "NRT", city_name: "東京", country_code: "JP", country_name: "日本",
    category: "culture", area: null, score: 88,
    components: { interest: 90, growth: 80, quality: 92, confidence: 80 },
    pageviews_30d: 12345, growth_rate: 0.2, trend_label: "近期升溫",
    sources: ["curated_catalog"], has_source: false, signal_date: "2026-08-30",
    is_estimate: false, is_deep_travel: false, depth_kind: null, depth_score: null,
    depth_reason: null, local_name: null, access_minutes: null,
    recommended_duration_minutes: null, guide_counts: { article: 0, video: 0 },
    map_links: [], place_summary: null, ...overrides,
  };
}

function rankingBody(items: unknown[]) {
  return JSON.stringify({
    scope: "global", scope_key: "global", observed_on: "2026-08-31", window_days: 30,
    total: items.length, has_more: false, next_cursor: null, items,
  });
}

function facetsBody(themes: unknown[]) {
  return JSON.stringify({ total: 1, countries: [], cities: [], categories: [], areas: [], themes });
}

describe("HotspotExplorer", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    // Filters live in the address bar, so a test that set one would otherwise
    // decide what the next test's first request asks for.
    window.history.replaceState(null, "", "/");
  });

  it("shows ranked hotspots with provenance and freshness", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) {
        return new Response(JSON.stringify({ items: [] }));
      }
      if (url.includes("/hotspots/facets")) {
        return new Response(JSON.stringify({
          total: 170,
          countries: [{ code: "JP", name: "日本", count: 56 }],
          cities: [{ code: "NRT", destination_id: "tokyo", name: "東京", country_code: "JP", count: 12, destination_role: "primary", parent_destination_id: null, is_cross_city: false }],
          categories: [{ code: "culture", count: 80 }],
          areas: [
            { destination_id: "tokyo", city_code: "NRT", code: "asakusa", name: "淺草／晴空塔", count: 2 },
            { destination_id: "tokyo", city_code: "NRT", code: "akihabara", name: "秋葉原／神田", count: 1 },
          ],
        }));
      }
      if (url.includes("/hotspots/hotspot-1/guides")) {
        return new Response(JSON.stringify({
          hotspot_id: "hotspot-1",
          hotspot_name: "淺草寺",
          locale: "zh-TW",
          other_languages_available: true,
          updated_at: "2026-08-31T00:00:00Z",
          videos: [{
            id: "11111111-1111-1111-1111-111111111111",
            type: "video",
            provider: "youtube",
            locale: "zh-TW",
            title: "第一次去淺草寺",
            creator_name: "旅行頻道",
            thumbnail_url: null,
            summary: null,
            published_at: "2026-08-01T00:00:00Z",
            duration_seconds: null,
            view_count: 45678,
            opens_30d: 0,
            updated_at: "2026-08-31T00:00:00Z",
          }],
          articles: [],
        }));
      }
      if (url.includes("/hotspots/hotspot-1/place")) {
        return new Response(JSON.stringify({
          hotspot_id: "hotspot-1",
          hotspot_name: "淺草寺",
          status: "ready",
          google_maps_url: "https://www.google.com/maps/search/?api=1&query=%E6%B5%85%E8%8D%89%E5%AF%BA%20%E6%9D%B1%E4%BA%AC&query_place_id=ChIJ-test",
          map_links: [{ provider: "google", label: "Google Maps", url: "https://www.google.com/maps/search/?api=1&query=%E6%B5%85%E8%8D%89%E5%AF%BA%20%E6%9D%B1%E4%BA%AC&query_place_id=ChIJ-test", primary: true }],
          official_website_url: "https://www.senso-ji.jp/",
          official_website_verified: true,
          has_details: true,
          updated_at: "2026-08-31T00:00:00Z",
          address: "東京都台東区浅草2丁目3-1",
          coordinates: { latitude: 35.714765, longitude: 139.796655, source: "wikidata" },
          opening_hours: { weekday_descriptions: ["星期一：06:00–17:00"] },
          data_locale: "ja",
          fetched_at: "2026-08-31T00:00:00Z",
          expires_at: "2026-09-30T00:00:00Z",
          attribution: { provider: "Google Maps", provider_url: "https://maps.google.com", third_party: [{ provider: "Japan Map Center", providerUri: "https://example.com/attribution" }] },
        }));
      }
      return new Response(JSON.stringify({
        scope: "global",
        scope_key: "global",
        observed_on: "2026-08-31",
        window_days: 30,
        total: 170,
        has_more: true,
        next_cursor: 1,
        items: [{
          id: "hotspot-1",
          slug: "sensoji",
          rank: 1,
          name: "淺草寺",
          destination_id: "tokyo",
          destination_role: "primary",
          parent_destination_id: null,
          is_cross_city: false,
          city_code: "NRT",
          city_name: "東京",
          country_code: "JP",
          country_name: "日本",
          category: "culture",
          area: { code: "asakusa", name: "淺草／晴空塔" },
          score: 88,
          components: { interest: 90, growth: 80, quality: 92, confidence: 80 },
          pageviews_30d: 12345,
          growth_rate: 0.2,
          trend_label: "近期升溫",
          sources: ["curated_catalog", "wikimedia_pageviews"],
          has_source: true,
          signal_date: "2026-08-30",
          is_estimate: false,
          is_deep_travel: true,
          depth_kind: "urban_local",
          depth_score: 88,
          depth_reason: "保留地方生活脈絡",
          local_name: "浅草寺",
          access_minutes: 20,
          recommended_duration_minutes: 90,
          guide_counts: { article: 0, video: 1 },
          map_links: [{ provider: "google", label: "Google Maps", url: "https://www.google.com/maps/search/?api=1&query=%E6%B5%85%E8%8D%89%E5%AF%BA%20%E6%9D%B1%E4%BA%AC&query_place_id=ChIJ-test", primary: true }],
          place_summary: { status: "ready", google_maps_url: "https://www.google.com/maps/search/?api=1&query=%E6%B5%85%E8%8D%89%E5%AF%BA%20%E6%9D%B1%E4%BA%AC&query_place_id=ChIJ-test", map_links: [{ provider: "google", label: "Google Maps", url: "https://www.google.com/maps/search/?api=1&query=%E6%B5%85%E8%8D%89%E5%AF%BA%20%E6%9D%B1%E4%BA%AC&query_place_id=ChIJ-test", primary: true }], official_website_url: "https://www.senso-ji.jp/", official_website_verified: true, has_details: true, updated_at: "2026-08-31T00:00:00Z" },
        }],
      }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<SavedItemsProvider><HotspotExplorer /></SavedItemsProvider>);

    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();
    expect(screen.getByText("12,345")).toBeTruthy();
    expect(screen.queryByText("資料來源狀態")).toBeNull();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/hotspots/sources"))).toBe(false);
    expect(screen.getByText("已載入 1／170 個結果")).toBeTruthy();
    expect(screen.getByRole("button", { name: "載入更多" })).toBeTruthy();
    // City tiers and deep-travel styles are gone from the public page: no selects, no chips.
    expect(screen.queryByText(/深度旅遊/)).toBeNull();
    expect(screen.queryByText("市區巷弄")).toBeNull();
    expect(screen.queryByText(/交通約 20 分鐘/)).toBeNull();
    expect(screen.queryByRole("combobox", { name: "全部城市層級" })).toBeNull();
    expect(screen.queryByRole("combobox", { name: "全部旅遊" })).toBeNull();
    expect(screen.getByRole("button", { name: /景點詳情/ })).toBeTruthy();
    const map = screen.getByRole("link", { name: /Google Maps/ });
    expect(map.textContent).toContain("東京 · 淺草／晴空塔 · 文化古蹟");
    expect(map.getAttribute("href")).toContain("query_place_id=ChIJ-test");
    expect(map.getAttribute("href")).not.toContain("35.7");
    expect(map.getAttribute("target")).toBe("_blank");
    expect(map.getAttribute("rel")).toContain("noopener");
    expect(screen.getAllByRole("link", { name: /Google Maps/ })).toHaveLength(1);
    const diningButton = screen.getByRole("button", { name: /附近用餐/ });
    expect(diningButton.textContent).toContain("即時星等");
    const source = screen.getByRole("link", { name: "查看來源" });
    expect(source.getAttribute("href")).toBe("/zh-TW/out/hotspots/hotspot-1/source");
    fireEvent.click(screen.getByRole("button", { name: /景點詳情/ }));
    expect(await screen.findByRole("heading", { name: "認識 淺草寺" })).toBeTruthy();
    const dialog = screen.getByRole("dialog", { name: "認識 淺草寺" });
    expect(within(dialog).queryByText("地址")).toBeNull();
    expect(within(dialog).queryByText("東京都台東区浅草2丁目3-1")).toBeNull();
    expect(within(dialog).queryByText("營業時間")).toBeNull();
    expect(within(dialog).queryByText("星期一：06:00–17:00")).toBeNull();
    expect(within(dialog).queryByText("Google Maps")).toBeNull();
    expect(within(dialog).queryByText("8Q7XPQ7W+WM")).toBeNull();
    expect(within(dialog).queryByText("35.714765, 139.796655")).toBeNull();
    expect(within(dialog).queryByText(/Google 資料更新/)).toBeNull();
    expect(within(dialog).queryByText(/供應商內容語系/)).toBeNull();
    const official = within(dialog).getByRole("link", { name: /官方網站/ });
    expect(official.getAttribute("rel")).toContain("noopener");
    const guide = await screen.findByRole("link", { name: /第一次去淺草寺/ });
    expect(guide.getAttribute("target")).toBe("_blank");
    expect(guide.getAttribute("href")).toContain("/zh-TW/out/guides/");
    fireEvent.keyDown(document, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog", { name: "認識 淺草寺" })).toBeNull());

    // The area filter only opens once a city is chosen, then scopes the ranking request.
    const areaSelect = screen.getByRole("combobox", { name: "全部區域" }) as HTMLSelectElement;
    expect(areaSelect.disabled).toBe(true);
    fireEvent.change(screen.getByRole("combobox", { name: "全部城市" }), { target: { value: "tokyo" } });
    await waitFor(() => expect(areaSelect.disabled).toBe(false));
    expect(within(areaSelect).getByRole("option", { name: "秋葉原／神田 (1)" })).toBeTruthy();
    fireEvent.change(areaSelect, { target: { value: "akihabara" } });
    fireEvent.click(screen.getByRole("button", { name: "查看排行" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([input]) => {
      const url = String(input);
      return url.includes("/hotspots/rankings?") && url.includes("destination_id=tokyo") && url.includes("area=akihabara") && !url.includes("style=");
    })).toBe(true));
  });

  it("keeps the loaded list on screen when loading more fails", async () => {
    let rankingCalls = 0;
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      if (url.includes("/hotspots/facets")) {
        return new Response(JSON.stringify({ total: 1, countries: [], cities: [], categories: [], areas: [] }));
      }
      rankingCalls += 1;
      if (rankingCalls > 1) {
        return new Response(JSON.stringify({ code: "internal_error", detail: "連線中斷" }), { status: 500 });
      }
      return new Response(JSON.stringify({
        scope: "global", scope_key: "global", observed_on: "2026-08-31", window_days: 30,
        total: 170, has_more: true, next_cursor: 1,
        items: [{
          id: "hotspot-1", slug: "sensoji", rank: 1, name: "淺草寺", destination_id: "tokyo",
          destination_role: "primary", parent_destination_id: null, is_cross_city: false,
          city_code: "NRT", city_name: "東京", country_code: "JP", country_name: "日本",
          category: "culture", area: null, score: 88,
          components: { interest: 90, growth: 80, quality: 92, confidence: 80 },
          pageviews_30d: 12345, growth_rate: 0.2, trend_label: "近期升溫",
          sources: ["curated_catalog"], has_source: false, signal_date: "2026-08-30",
          is_estimate: false, is_deep_travel: false, depth_kind: null, depth_score: null,
          depth_reason: null, local_name: null, access_minutes: null,
          recommended_duration_minutes: null, guide_counts: { article: 0, video: 0 },
          map_links: [], place_summary: null,
        }],
      }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<SavedItemsProvider><HotspotExplorer /></SavedItemsProvider>);

    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "載入更多" }));

    expect(await screen.findByRole("alert")).toBeTruthy();
    // The page the reader already scrolled through must survive the failure.
    expect(screen.getByRole("heading", { name: "淺草寺" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "重新載入" })).toBeTruthy();
  });

  it("requires sign-in for details, sources, and sharing without loading protected content", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) {
        return new Response(JSON.stringify({ code: "authentication_required" }), { status: 401 });
      }
      if (url.includes("/hotspots/facets")) {
        return new Response(JSON.stringify({ total: 1, countries: [], cities: [], categories: [], areas: [] }));
      }
      return new Response(JSON.stringify({
        scope: "global", scope_key: "global", observed_on: "2026-08-31", window_days: 30,
        total: 1, has_more: false, next_cursor: null,
        items: [{
          id: "hotspot-1", slug: "sensoji", rank: 1, name: "淺草寺", local_name: "浅草寺",
          destination_id: "tokyo", destination_role: "primary", parent_destination_id: null,
          is_cross_city: false, city_code: "NRT", city_name: "東京", country_code: "JP", country_name: "日本",
          category: "culture", score: 88, components: { interest: 90, growth: 80, quality: 92, confidence: 80 },
          pageviews_30d: 12345, growth_rate: 0.2, trend_label: "近期升溫", sources: ["curated_catalog"],
          has_source: true, signal_date: "2026-08-30", is_estimate: false, is_deep_travel: false,
          depth_kind: null, depth_score: null, depth_reason: null, access_minutes: null,
          recommended_duration_minutes: 90, guide_counts: { article: 0, video: 1 },
          map_links: [{ provider: "google", label: "Google Maps", url: "https://www.google.com/maps/search/?api=1&query_place_id=ChIJ-test", primary: true }],
          place_summary: { status: "ready", google_maps_url: null, map_links: [], official_website_url: null, official_website_verified: false, has_details: true, updated_at: null },
        }],
      }));
    });
    vi.stubGlobal("fetch", fetchMock);
    const share = vi.fn();
    Object.defineProperty(navigator, "share", { configurable: true, value: share });

    render(<SavedItemsProvider><HotspotExplorer /></SavedItemsProvider>);
    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();
    expect(screen.queryByText("資料來源狀態")).toBeNull();

    const details = screen.getByRole("button", { name: /景點詳情/ });
    details.focus();
    fireEvent.click(details);
    expect(await screen.findByRole("heading", { name: "登入後繼續使用景點功能" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "登入後繼續" }).getAttribute("href")).toContain("/login?next=");
    expect(fetchMock.mock.calls.some(([input]) => /hotspots\/hotspot-1\/(place|guides)/.test(String(input)))).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: "關閉登入提示" }));
    await waitFor(() => expect(document.activeElement).toBe(details));

    fireEvent.click(screen.getByRole("button", { name: "查看來源" }));
    expect(await screen.findByRole("heading", { name: "登入後繼續使用景點功能" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "關閉登入提示" }));

    fireEvent.click(screen.getByRole("button", { name: "分享" }));
    expect(await screen.findByRole("heading", { name: "登入後繼續使用此功能" })).toBeTruthy();
    expect(share).not.toHaveBeenCalled();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/hotspots/sources"))).toBe(false);
  });
  it("filters by a theme chip and keeps it in the address bar", async () => {
    // The chips mark what is in season now, so the fixture is written against the
    // month the test runs in rather than a frozen clock.
    const thisMonth = new Date().getMonth() + 1;
    const otherMonth = (thisMonth % 12) + 1;
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      if (url.includes("/hotspots/facets")) {
        return new Response(facetsBody([
          { slug: "sakura", kind: "season", name: "賞櫻", months: [thisMonth], count: 3 },
          { slug: "ski", kind: "season", name: "滑雪", months: [otherMonth], count: 0 },
          { slug: "drugstore", kind: "shop", name: "藥妝", months: [], count: 2 },
        ]));
      }
      return new Response(rankingBody([rankingItem()]));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<SavedItemsProvider><HotspotExplorer /></SavedItemsProvider>);
    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();

    const chips = await screen.findByRole("group", { name: "主題篩選" });
    const sakura = within(chips).getByRole("button", { name: /賞櫻/ });
    expect(sakura.textContent).toContain("當季");
    expect(within(chips).getByRole("button", { name: /藥妝/ }).textContent).not.toContain("當季");
    // A theme with nothing behind it stays out of the way until it is the selection.
    expect(within(chips).queryByRole("button", { name: /滑雪/ })).toBeNull();
    expect(screen.getByRole("combobox", { name: "所有類型" }).querySelectorAll("option")).toHaveLength(9);

    fireEvent.click(sakura);
    await waitFor(() => expect(fetchMock.mock.calls.some(([input]) => {
      const url = String(input);
      return url.includes("/hotspots/rankings?") && url.includes("theme=sakura");
    })).toBe(true));
    expect(window.location.search).toContain("theme=sakura");
    expect(sakura.getAttribute("aria-pressed")).toBe("true");
    expect(screen.getByRole("button", { name: /熱門景點搜尋/ }).textContent).toContain("1");

    fireEvent.click(sakura);
    await waitFor(() => expect(window.location.search).not.toContain("theme="));
    expect(sakura.getAttribute("aria-pressed")).toBe("false");
  });

  it("opens a shared theme link and offers a way out when it is empty", async () => {
    window.history.replaceState(null, "", "/zh-TW/hotspots?theme=sakura");
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      if (url.includes("/hotspots/facets")) {
        return new Response(facetsBody([
          { slug: "sakura", kind: "season", name: "賞櫻", months: [3, 4], count: 0 },
        ]));
      }
      if (url.includes("theme=sakura")) return new Response(rankingBody([]));
      return new Response(rankingBody([rankingItem()]));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<SavedItemsProvider><HotspotExplorer /></SavedItemsProvider>);

    expect(await screen.findByText(/這個主題在目前條件下還沒有景點/)).toBeTruthy();
    expect(String(fetchMock.mock.calls.find(([input]) => String(input).includes("/hotspots/rankings"))?.[0]))
      .toContain("theme=sakura");
    const chips = await screen.findByRole("group", { name: "主題篩選" });
    // Zero results, but the chip stays because it is what the reader is looking at.
    expect(within(chips).getByRole("button", { name: /賞櫻/ }).getAttribute("aria-pressed")).toBe("true");

    fireEvent.click(screen.getByRole("button", { name: "清除條件" }));
    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();
    expect(window.location.search).toBe("");
  });

  it("shows the months a season badge applies to", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      if (url.includes("/hotspots/facets")) return new Response(facetsBody([]));
      return new Response(rankingBody([rankingItem({
        themes: [
          { slug: "sakura", kind: "season", name: "賞櫻", months: [3, 4] },
          { slug: "illumination", kind: "season", name: "燈飾", months: [11, 12, 1] },
          { slug: "drugstore", kind: "shop", name: "藥妝", months: [] },
        ],
      })]));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<SavedItemsProvider><HotspotExplorer /></SavedItemsProvider>);
    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();

    const badges = screen.getByRole("list", { name: "景點主題" });
    expect(within(badges).getByText("賞櫻").closest("li")?.textContent).toContain("3月–4月");
    // A winter season that crosses new year reads as one span, not two.
    expect(within(badges).getByText("燈飾").closest("li")?.textContent).toContain("11月–1月");
    expect(within(badges).getByText("藥妝").closest("li")?.textContent).not.toMatch(/月/);
    // No facets, so the filter row is absent rather than empty.
    expect(screen.queryByRole("group", { name: "主題篩選" })).toBeNull();
  });
});
