import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminAnalyticsPanel } from "./admin-analytics-panel";

const dashboard = {
  range: "30d", timezone: "Asia/Taipei", source: "raw",
  summary: { live_sessions_30m: 3, page_views: 42, avg_daily_visitors: 8, sessions: 10, pages_per_session: 4.2, registration_completed: 2, search_completed: 7, trip_created: 4, outbound_click: 3, changes: { page_views: 12 } },
  timeseries: [{ bucket: "2026-09-01", page_view: 42 }],
  funnel: [{ step: "sessions", sessions: 10, conversion_rate: 100 }, { step: "search_completed", sessions: 7, conversion_rate: 70 }],
  top_pages: [{ key: "/hotspots", value: 20 }], referrers: [{ key: "search", value: 15 }],
  utm_sources: [], devices: [{ key: "mobile", value: 30 }], locales: [{ key: "zh-TW", value: 35 }], countries: [{ key: "TW", value: 30 }], heatmap: [],
  authoritative: { registrations: 2, completed_searches: 8, trips_created: 5, affiliate_clicks: 3 },
  data_quality: { ga4_enabled: true, ga4_configured: true, last_event_at: "2026-09-02T01:00:00Z", last_rollup_day: "2026-09-01", country_coverage_percent: 80 },
};

describe("AdminAnalyticsPanel", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("shows first-party metrics, the product funnel, and data quality", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(dashboard))));
    render(<AdminAnalyticsPanel />);
    expect((await screen.findAllByText("42")).length).toBeGreaterThan(0);
    expect(screen.getByText("核心產品漏斗")).toBeTruthy();
    expect(screen.getByText("GA4 cookieless 狀態")).toBeTruthy();
    expect(screen.getByText("權威營運總量")).toBeTruthy();
  });
});
