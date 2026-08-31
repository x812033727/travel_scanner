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
      return new Response(JSON.stringify({
        scope: "global",
        scope_key: "global",
        observed_on: "2026-08-31",
        window_days: 30,
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
        }],
      }));
    }));

    render(<HotspotExplorer />);

    expect(await screen.findByRole("heading", { name: "淺草寺" })).toBeTruthy();
    expect(screen.getByText("12,345")).toBeTruthy();
    expect(screen.getByText("Wikimedia 趨勢")).toBeTruthy();
    expect(await screen.findByText("Wikimedia Analytics")).toBeTruthy();
  });
});
