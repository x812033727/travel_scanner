import { expect, test } from "@playwright/test";

const hotspotId = "11111111-1111-4111-8111-111111111111";
const guideId = "22222222-2222-4222-8222-222222222222";

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({ status: 401, contentType: "application/json", body: "{}" }));
  await page.route("**/api/travel/hotspots/**", (route) => {
    const url = new URL(route.request().url());
    if (url.pathname.endsWith("/sources")) return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ collection_interval_seconds: 21600, sources: [{ id: "youtube_guides", name: "YouTube", status: "ready", purpose: "", persistence: "" }] }) });
    if (url.pathname.endsWith("/facets")) return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ total: 1, countries: [], cities: [], categories: [], styles: [] }) });
    if (url.pathname.endsWith("/rankings")) return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ scope: "global", scope_key: "global", observed_on: "2026-09-01", window_days: 30, total: 1, has_more: false, next_cursor: null, items: [{ id: hotspotId, slug: "sensoji", rank: 1, name: "Senso-ji", city_code: "NRT", city_name: "Tokyo", country_code: "JP", country_name: "Japan", category: "culture", score: 92, components: { interest: 90, growth: 90, quality: 90, confidence: 90 }, pageviews_30d: 12345, growth_rate: 0.2, trend_label: "up", sources: ["wikimedia_pageviews"], source_urls: [], signal_date: "2026-09-01", is_estimate: false, is_deep_travel: false, depth_kind: null, depth_score: null, depth_reason: null, local_name: "浅草寺", access_minutes: null, recommended_duration_minutes: null, guide_counts: { article: 1, video: 1 } }] }) });
    if (url.pathname.endsWith(`/${hotspotId}/guides`)) {
      const includeOther = url.searchParams.get("include_other_languages") === "true";
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ hotspot_id: hotspotId, hotspot_name: "Senso-ji", locale: "zh-TW", other_languages_available: true, updated_at: "2026-09-01T00:00:00Z", videos: [{ id: guideId, type: "video", provider: "youtube", locale: "zh-TW", title: "淺草寺第一次自由行", creator_name: "旅行頻道", thumbnail_url: null, summary: null, published_at: "2026-08-01T00:00:00Z", duration_seconds: null, view_count: 98000, opens_30d: 0, updated_at: "2026-09-01T00:00:00Z" }], articles: [{ id: "33333333-3333-4333-8333-333333333333", type: "article", provider: "brave", locale: includeOther ? "ja" : "zh-TW", title: includeOther ? "浅草寺の歩き方" : "淺草寺散步攻略", creator_name: "Travel Blog", thumbnail_url: null, summary: null, published_at: null, duration_seconds: null, view_count: null, opens_30d: 42, updated_at: "2026-09-01T00:00:00Z" }] }) });
    }
    return route.abort();
  });
});

for (const [locale, buttonName] of [
  ["en", "Articles & videos"], ["ja", "記事・動画を見る"], ["ko", "글과 영상 보기"],
  ["zh-TW", "文章與影片介紹"], ["zh-CN", "文章与视频介绍"],
] as const) {
  test(`${locale} loads language-aware guide entry`, async ({ page }) => {
    await page.goto(`/${locale}/hotspots`);
    await expect(page.getByRole("button", { name: new RegExp(buttonName) })).toBeVisible();
  });
}

for (const width of [320, 390]) {
  test(`mobile guide sheet is app-like at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 760 });
    await page.goto("/zh-TW/hotspots");
    await page.getByRole("button", { name: /文章與影片介紹/ }).click();
    const dialog = page.getByRole("dialog", { name: "認識 Senso-ji" });
    await expect(dialog).toBeVisible();
    await expect(dialog.getByText("淺草寺第一次自由行")).toBeVisible();
    const external = dialog.getByRole("link", { name: /淺草寺第一次自由行/ });
    await expect(external).toHaveAttribute("target", "_blank");
    await expect(external).toHaveAttribute("rel", /noopener/);
    await expect(page.locator("html")).toHaveJSProperty("scrollWidth", await page.locator("html").evaluate((node) => node.clientWidth));
    await dialog.getByRole("button", { name: /顯示其他語言/ }).click();
    await expect(dialog.getByText("浅草寺の歩き方")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(dialog).toBeHidden();
  });
}
