import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { HotspotExplorer } from "./hotspot-explorer";

describe("HotspotExplorer", () => {
  it("shows ranked hotspots with provenance and freshness", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
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
          google_maps_url: "https://www.google.com/maps/place/?q=place_id:test",
          official_website_url: "https://www.senso-ji.jp/",
          official_website_verified: true,
          has_details: true,
          updated_at: "2026-08-31T00:00:00Z",
          address: "東京都台東区浅草2丁目3-1",
          plus_code: { global_code: "8Q7XPR6F+82", compound_code: "PR6F+82 台東区" },
          coordinates: { latitude: 35.714765, longitude: 139.796655, source: "google_places" },
          opening_hours: { weekday_descriptions: ["星期一：06:00–17:00"] },
          data_locale: "ja",
          fetched_at: "2026-08-31T00:00:00Z",
          expires_at: "2026-09-30T00:00:00Z",
          attribution: { provider: "Google Maps", provider_url: "https://maps.google.com", third_party: [] },
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
          map_links: [{ provider: "google", label: "Google Maps", url: "https://www.google.com/maps/search/?api=1&query=35.7%2C139.7", primary: true }],
          place_summary: { status: "ready", google_maps_url: "https://www.google.com/maps/place/?q=place_id:test", official_website_url: "https://www.senso-ji.jp/", official_website_verified: true, has_details: true, updated_at: "2026-08-31T00:00:00Z" },
        }],
      }));
    }));

    render(<HotspotExplorer />);

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
    expect(map.getAttribute("target")).toBe("_blank");
    expect(map.getAttribute("rel")).toContain("noopener");
    fireEvent.click(screen.getByRole("button", { name: /景點詳情/ }));
    expect(await screen.findByRole("heading", { name: "認識 淺草寺" })).toBeTruthy();
    expect(await screen.findByText("東京都台東区浅草2丁目3-1")).toBeTruthy();
    expect(screen.getByText("PR6F+82 台東区")).toBeTruthy();
    const official = screen.getAllByRole("link", { name: /官方網站/ })[0];
    expect(official.getAttribute("rel")).toContain("noopener");
    const guide = await screen.findByRole("link", { name: /第一次去淺草寺/ });
    expect(guide.getAttribute("target")).toBe("_blank");
    expect(guide.getAttribute("href")).toContain("/zh-TW/out/guides/");
  });
});
