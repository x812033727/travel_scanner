import { expect, test } from "@playwright/test";

const hotspotId = "11111111-1111-4111-8111-111111111111";

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ id: "admin-1", email: "admin@example.com", is_admin: true }),
  }));
  await page.route("**/api/travel/admin/hotspots/**", (route) => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.pathname.endsWith("/guides/coverage")) return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [{ id: hotspotId, name: "淺草寺", complete: false, coverage: {
          en: { article: 0, video: 0 }, ja: { article: 0, video: 0 },
          ko: { article: 0, video: 0 }, "zh-TW": { article: 0, video: 0 },
          "zh-CN": { article: 0, video: 0 },
        } }],
        total: 1,
        complete: 0,
        quotas: { youtube: { used: 4, automatic_limit: 80, manual_limit: 100 }, brave: { used: 3, limit: 30 } },
        ai_search: { enabled: true, default_provider: "minimax",
          providers: { minimax: true, openai: false, anthropic: true },
          sources: { brave: true, youtube: true },
          quota: { runs_used: 1, runs_limit: 10, calls_used: 2, calls_limit: 60 } },
      }),
    });
    if (url.pathname.endsWith("/guides/ai-search") && request.method() === "POST") return route.fulfill({
      status: 202,
      contentType: "application/json",
      body: JSON.stringify({ run_id: "run-1", status: "queued", progress: 0, current: {}, usage: {}, result: {}, error_code: null }),
    });
    if (url.pathname.endsWith("/guides/ai-search/run-1")) return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ run_id: "run-1", status: "completed", progress: 100, current: { stage: "finished" }, usage: { ai_calls: 2, brave_calls: 5, youtube_calls: 5 }, result: { evaluated: 20, created: 8, errors: [] }, error_code: null }),
    });
    if (url.pathname.endsWith("/guides")) return route.fulfill({
      status: 200, contentType: "application/json",
      body: JSON.stringify({ items: [], total: 0, page: 1, pages: 0 }),
    });
    if (url.pathname.endsWith("/candidates")) return route.fulfill({
      status: 200, contentType: "application/json",
      body: JSON.stringify({ items: [], total: 0, page: 1, pages: 0 }),
    });
    return route.fulfill({ status: 200, contentType: "application/json", body: "{}" });
  });
});

for (const width of [320, 390]) {
  test(`AI deep-search sheet is app-like at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 760 });
    await page.goto("/zh-TW/admin/hotspots#guides");
    await page.getByRole("button", { name: "AI 搜尋" }).click();
    const dialog = page.getByRole("dialog", { name: "淺草寺" });
    await expect(dialog).toBeVisible();
    await expect(dialog.getByLabel("AI 供應商")).toHaveValue("minimax");
    await expect(dialog.getByLabel("搜尋深度")).toHaveValue("deep");
    const box = await dialog.boundingBox();
    expect(box?.width).toBeLessThanOrEqual(width);
    await expect(page.locator("html")).toHaveJSProperty(
      "scrollWidth",
      await page.locator("html").evaluate((node) => node.clientWidth),
    );
    await dialog.getByRole("button", { name: "開始 AI 深度搜尋" }).click();
    await expect(dialog.getByText(/新增 8 筆待審候選/)).toBeVisible({ timeout: 5_000 });
  });
}

test("desktop uses a focused side panel", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop-chromium", "desktop layout only");
  await page.goto("/zh-TW/admin/hotspots#guides");
  await page.getByRole("button", { name: "AI 搜尋" }).click();
  const dialog = page.getByRole("dialog", { name: "淺草寺" });
  await expect(dialog).toBeVisible();
  const box = await dialog.boundingBox();
  expect(box?.width).toBeGreaterThanOrEqual(550);
  expect(box?.x).toBeGreaterThan(500);
  await expect(dialog.getByText("預估呼叫量")).toBeVisible();
});
