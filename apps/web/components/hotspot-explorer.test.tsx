import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SavedItemsProvider } from "./saved-items-provider";
import { HotspotExplorer } from "./hotspot-explorer";

describe("HotspotExplorer", () => {
  it("shows ranked hotspots with provenance and freshness", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) {
        return new Response(JSON.stringify({ code: "authentication_required" }), { status: 401 });
      }
      if (url.includes("/hotspots/sources")) {
        return new Response(JSON.stringify({
          collection_interval_seconds: 21600,
          sources: [{
            id: "wikimedia_pageviews",
            name: "Wikimedia Analytics",
            status: "ready",
            purpose: "比較公開頁面瀏覽趨勢",
            persistence: "每日彙總數字",
          }],
        }));
      }
      if (url.includes("/hotspots/facets")) {
        return new Response(JSON.stringify({
          total: 170,
          countries: [{ code: "JP", name: "日本", count: 56 }],
          cities: [{ code: "NRT", destination_id: "tokyo", name: "東京", country_code: "JP", count: 12, destination_role: "primary", parent_destination_id: null, is_cross_city: false }],
          categories: [{ code: "culture", count: 80 }],
          styles: [{ code: "all", name: "全部旅遊", count: 170 }, { code: "deep", name: "深度旅遊", count: 95 }],
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
          plus_code: { global_code: "8Q7XPQ7W+WM", compound_code: null },
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
          score: 88,
          components: { interest: 90, growth: 80, quality: 92, confidence: 80 },
          pageviews_30d: 12345,
          growth_rate: 0.2,
          trend_label: "近期升溫",
          sources: ["curated_catalog", "wikimedia_pageviews"],
          source_urls: ["https://en.wikipedia.org/wiki/Sens%C5%8D-ji"],
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
    expect(await screen.findByText("Wikimedia 趨勢")).toBeTruthy();
    expect(screen.getByText("已載入 1／170 個結果")).toBeTruthy();
    expect(screen.getByRole("button", { name: "載入更多" })).toBeTruthy();
    expect(screen.getAllByText(/深度旅遊/).length).toBeGreaterThan(0);
    expect(screen.getByText("市區巷弄")).toBeTruthy();
    expect(screen.getByText(/交通約 20 分鐘/)).toBeTruthy();
    expect(screen.getByRole("button", { name: /景點詳情/ })).toBeTruthy();
    const map = screen.getByRole("link", { name: /Google Maps/ });
    expect(map.textContent).toContain("東京 · 文化古蹟");
    expect(map.getAttribute("href")).toContain("query_place_id=ChIJ-test");
    expect(map.getAttribute("href")).not.toContain("35.7");
    expect(map.getAttribute("target")).toBe("_blank");
    expect(map.getAttribute("rel")).toContain("noopener");
    expect(screen.getAllByRole("link", { name: /Google Maps/ })).toHaveLength(1);
    const diningButton = screen.getByRole("button", { name: /附近用餐/ });
    expect(diningButton.textContent).toContain("登入後查詢");
    diningButton.focus();
    fireEvent.click(diningButton);
    expect(await screen.findByRole("heading", { name: "登入後查看附近用餐" })).toBeTruthy();
    const loginLink = screen.getByRole("link", { name: "登入後繼續" });
    expect(loginLink.getAttribute("href")).toContain("/login?next=");
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("restaurant-searches"))).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: "關閉登入提示" }));
    await waitFor(() => expect(document.activeElement).toBe(diningButton));
    fireEvent.click(screen.getByRole("button", { name: /景點詳情/ }));
    expect(await screen.findByRole("heading", { name: "認識 淺草寺" })).toBeTruthy();
    const dialog = screen.getByRole("dialog", { name: "認識 淺草寺" });
    const address = within(dialog).getByRole("link", { name: /東京都台東区浅草2丁目3-1.*Google Maps/ });
    expect(address.getAttribute("href")).toContain("query_place_id=ChIJ-test");
    expect(address.getAttribute("target")).toBe("_blank");
    expect(address.getAttribute("rel")).toContain("noopener");
    expect(within(dialog).getAllByRole("link", { name: /Google Maps/ })).toHaveLength(1);
    const attribution = within(dialog).getByText("Google Maps");
    expect(attribution.getAttribute("translate")).toBe("no");
    expect(within(dialog).queryByRole("img", { name: "Google Maps" })).toBeNull();
    expect(within(dialog).getByRole("link", { name: /Japan Map Center/ }).getAttribute("rel")).toContain("noopener");
    expect(within(dialog).queryByText("8Q7XPQ7W+WM")).toBeNull();
    expect(within(dialog).queryByText("35.714765, 139.796655")).toBeNull();
    expect(within(dialog).queryByText(/Google 資料更新/)).toBeNull();
    expect(within(dialog).queryByText(/供應商內容語系/)).toBeNull();
    const official = within(dialog).getByRole("link", { name: /官方網站/ });
    expect(official.getAttribute("rel")).toContain("noopener");
    const guide = await screen.findByRole("link", { name: /第一次去淺草寺/ });
    expect(guide.getAttribute("target")).toBe("_blank");
    expect(guide.getAttribute("href")).toContain("/zh-TW/out/guides/");
  });
});
