import { render, screen } from "@testing-library/react";
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
          cities: [{ code: "NRT", name: "東京", country_code: "JP", count: 12 }],
          categories: [{ code: "culture", count: 80 }],
          styles: [{ code: "all", name: "全部旅遊", count: 170 }, { code: "deep", name: "深度旅遊", count: 95 }],
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
        }],
      }));
    }));

    render(<HotspotExplorer />);

    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();
    expect(screen.getByText("12,345")).toBeTruthy();
    expect(screen.getByText("Wikimedia 趨勢")).toBeTruthy();
    expect(await screen.findByText("Wikimedia Analytics")).toBeTruthy();
    expect(screen.getByText("已載入 1／170 個結果")).toBeTruthy();
    expect(screen.getByRole("button", { name: "載入更多" })).toBeTruthy();
    expect(screen.getAllByText(/深度旅遊/).length).toBeGreaterThan(0);
    expect(screen.getByText("市區巷弄")).toBeTruthy();
    expect(screen.getByText(/交通約 20 分鐘/)).toBeTruthy();
  });
});
