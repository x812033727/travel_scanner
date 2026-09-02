import { expect, test } from "@playwright/test";

const dashboard = {
  range: "30d", timezone: "Asia/Taipei", source: "raw",
  summary: { live_sessions_30m: 4, page_views: 128, avg_daily_visitors: 17.5, sessions: 42, pages_per_session: 3.05, registration_completed: 8, search_completed: 26, trip_created: 14, outbound_click: 11, previous: {}, changes: { page_views: 12.5 } },
  timeseries: [{ bucket: "2026-09-01", page_view: 80 }, { bucket: "2026-09-02", page_view: 48 }],
  funnel: [{ step: "sessions", sessions: 42, conversion_rate: 100 }, { step: "search_completed", sessions: 26, conversion_rate: 61.9 }, { step: "trip_created", sessions: 14, conversion_rate: 33.3 }, { step: "outbound_click", sessions: 11, conversion_rate: 26.2 }],
  top_pages: [{ key: "/hotspots", value: 45 }, { key: "/search", value: 38 }],
  referrers: [{ key: "search", value: 51 }], utm_sources: [{ key: "autumn", value: 20 }],
  devices: [{ key: "mobile", value: 90 }], locales: [{ key: "zh-TW", value: 80 }], countries: [{ key: "TW", value: 76 }],
  heatmap: [{ weekday: 1, hour: 20, value: 9 }],
  authoritative: { registrations: 9, completed_searches: 28, trips_created: 15, affiliate_clicks: 12 },
  data_quality: { tracking_started_at: "2026-09-01T00:00:00+08:00", last_event_at: "2026-09-02T08:00:00Z", last_rollup_day: "2026-09-01", country_coverage_percent: 82.5, ga4_enabled: true, ga4_configured: true, bots_excluded: true, raw_retention_days: 90, rollup_retention_months: 25 },
};

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ id: "admin", email: "admin@example.com", is_admin: true }) }));
  await page.route("**/api/travel/analytics/config", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ first_party_enabled: false, ga4_enabled: false, ga4_measurement_id: null }) }));
  await page.route("**/api/travel/admin/analytics/dashboard**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(dashboard) }));
});

for (const [locale, title] of [
  ["en", "Traffic and product analytics"], ["ja", "トラフィック・プロダクト分析"],
  ["ko", "트래픽 및 제품 분석"], ["zh-TW", "流量與產品分析"], ["zh-CN", "流量与产品分析"],
] as const) {
  test(`${locale} analytics dashboard is localized`, async ({ page }) => {
    await page.goto(`/${locale}/admin/analytics`);
    await expect(page.getByRole("heading", { name: title })).toBeVisible();
    await expect(page.getByText("128", { exact: true }).first()).toBeVisible();
  });
}

for (const width of [320, 390]) {
  test(`analytics dashboard stays app-like at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 780 });
    await page.goto("/zh-TW/admin/analytics");
    await expect(page.getByRole("heading", { name: "流量與產品分析" })).toBeVisible();
    await page.getByRole("button", { name: "12 個月" }).click();
    await page.getByRole("checkbox", { name: "包含機器流量" }).check();
    await expect(page.locator("html")).toHaveJSProperty(
      "scrollWidth",
      await page.locator("html").evaluate((node) => node.clientWidth),
    );
    await expect(page.getByRole("table", { name: "星期與小時熱區" })).toBeAttached();
  });
}
