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

const affiliates = {
  range: "30d", timezone: "Asia/Taipei", total: 17, previous_total: 10, change: 70,
  by_partner: [{ key: "travelpayouts", value: 12 }, { key: "klook", value: 5 }],
  by_placement: [{ key: "guide", value: 9 }, { key: "city", value: 4 }, { key: "unknown", value: 4 }],
  by_module: [{ key: "activities", value: 11 }, { key: "hotel", value: 6 }],
  by_destination: [{ key: "tokyo", value: 10 }],
  by_brand: [{ key: "klook", value: 5 }],
  by_target_host: [{ key: "tp.media", value: 12 }],
  top_sub_ids: [{ key: "dst_activities_tokyo_zh-TW_guide", value: 9 }],
};

function stubFetch(report: unknown = affiliates) {
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.includes("/admin/analytics/affiliates")) {
      return report ? new Response(JSON.stringify(report)) : new Response("nope", { status: 503 });
    }
    return new Response(JSON.stringify(dashboard));
  }));
}

describe("AdminAnalyticsPanel", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("shows first-party metrics, the product funnel, and data quality", async () => {
    stubFetch();
    render(<AdminAnalyticsPanel />);
    expect((await screen.findAllByText("42")).length).toBeGreaterThan(0);
    expect(screen.getByText("核心產品漏斗")).toBeTruthy();
    expect(screen.getByText("GA4 cookieless 狀態")).toBeTruthy();
    expect(screen.getByText("權威營運總量")).toBeTruthy();
  });

  it("breaks affiliate clicks down by partner and by the surface that rendered the button", async () => {
    stubFetch();
    render(<AdminAnalyticsPanel />);
    expect((await screen.findByTestId("affiliate-total")).textContent).toBe("17");
    const section = screen.getByRole("region", { name: "聯盟外連" });
    expect(section.textContent).toContain("Placement");
    expect(section.textContent).toContain("guide");
    expect(section.textContent).toContain("travelpayouts");
    expect(section.textContent).toContain("dst_activities_tokyo_zh-TW_guide");
    expect(section.textContent).toContain("70%");
  });

  it("keeps the dashboard when the affiliate report is unavailable", async () => {
    stubFetch(null);
    render(<AdminAnalyticsPanel />);
    expect((await screen.findAllByText("42")).length).toBeGreaterThan(0);
    expect(screen.queryByTestId("affiliate-total")).toBeNull();
  });
});
