import { expect, test, type Page } from "@playwright/test";
import { pretendSignedIn } from "./session";
import { editorFixture, editorPlaceOptions } from "./fixtures/itinerary-editor";

// Disposable, isolated UI fixtures. No production trips or paid providers are touched.
async function workspace(page: Page) {
  let trip = structuredClone(editorFixture);
  const writes: string[] = [];
  const requests: string[] = [];
  await pretendSignedIn(page);
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({ json: { id: "premium-ui", email: "ui@example.test", role: "user", is_active: true } }));
  await page.route("**/api/travel/discovery/status", (route) => route.fulfill({ json: { enabled: false } }));
  await page.route("**/api/travel/trips/intuitive-trip**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    requests.push(path);
    if (path.endsWith("/place-options")) return route.fulfill({ json: { items: editorPlaceOptions, context: "nearby", next_offset: null } });
    if (path.endsWith("/itinerary/preview")) return route.fulfill({ json: {
      preview_id: "premium-preview", base_version: trip.version, scope: "day", day_date: trip.start_date,
      expires_at: "2030-01-01T00:00:00Z", planning: { status: "partial", readiness: "partial", provider: "catalog", warnings: [] },
      days: [{ date: trip.start_date, label: "淺草一帶", items: [{ ...editorPlaceOptions[0].item, id: "preview-temple", start_time: "2026-11-11T10:00:00" }] }],
      unscheduled_slots: [], readiness: { status: "partial", exact_item_count: 1, hotspot_candidate_count: 3, merchant_candidate_count: 1, preserved_item_count: trip.items.length, assumptions: [] },
      routing_summary: { exact_items: 1, eligible_pairs: 0, hotel_pairs_deferred: 0 },
    } });
    if (path.endsWith("/itinerary/apply")) {
      writes.push("apply");
      trip = { ...trip, version: trip.version + 1, items: [...trip.items, { ...editorPlaceOptions[0].item, id: "applied-temple", position: 2, day_date: "2026-11-11" }] };
      return route.fulfill({ json: trip });
    }
    if (route.request().method() === "PUT") {
      writes.push("save");
      trip = { ...trip, version: trip.version + 1, items: route.request().postDataJSON().items };
    }
    return route.fulfill({ json: trip });
  });
  await page.goto("/zh-TW/trips/intuitive-trip");
  await expect(page.getByRole("heading", { name: editorFixture.name })).toBeVisible();
  return { writes, requests, current: () => trip };
}

test("itinerary first, category tools and one accessible contextual sheet", async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const state = await workspace(page);
  await expect(page.getByRole("button", { name: /DAY 1/ })).toBeVisible();
  const card = page.locator('[data-stop-id="asakusa"]');
  await expect(card).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("premium-first-screen.png") });
  expect((await card.boundingBox())!.y).toBeLessThan(730);
  expect(state.requests.some((path) => /weather|stay-areas|travel-services|affiliates/.test(path))).toBe(false);
  await page.screenshot({ path: testInfo.outputPath("premium-mobile-timeline.png"), fullPage: true });
  await page.getByRole("button", { name: "開啟旅程工具" }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toHaveCount(1);
  await expect(dialog.getByRole("button", { name: /旅行準備/ })).toBeVisible();
  await expect(page.locator(".premium-mobile-bar")).toBeHidden();
  await dialog.getByRole("button", { name: /旅程設定/ }).click();
  await expect(dialog.getByText("旅伴與旅行偏好", { exact: true })).toBeVisible();
  await dialog.getByRole("button", { name: "返回", exact: true }).click();
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(page.getByRole("button", { name: "開啟旅程工具" })).toBeFocused();
  expect(state.writes).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(390);
});

test("continuous additions, card actions and cross-day movement preserve manual stops", async ({ page }) => {
  const state = await workspace(page);
  await page.getByRole("button", { name: "排序行程", exact: true }).click();
  await page.getByRole("button", { name: "在 午餐・河畔食堂 前插入新安排" }).click();
  const picker = page.getByRole("dialog", { name: "下一站想去哪裡？" });
  await picker.getByRole("textbox", { name: "搜尋地點", exact: true }).fill("淺草");
  await picker.getByRole("button", { name: "選擇 淺草寺" }).click();
  const draft = page.getByRole("dialog", { name: "新增安排", exact: true });
  expect(state.writes).toEqual([]);
  await draft.getByRole("button", { name: "加入行程", exact: true }).click();
  await expect(draft).toBeHidden();
  await page.getByRole("button", { name: "在 午餐・河畔食堂 前插入新安排" }).click();
  await expect(picker.getByRole("textbox", { name: "搜尋地點", exact: true })).toHaveValue("淺草");
  await picker.getByRole("button", { name: "選擇 隅田公園" }).click();
  await expect(page.getByRole("dialog")).toHaveCount(1);
  expect(state.writes).toEqual(["save"]);
  await draft.getByRole("button", { name: "加入行程", exact: true }).click();
  await expect(draft).toBeHidden();
  expect(state.writes).toEqual(["save", "save"]);
  const card = page.locator('[data-stop-id="asakusa"]');
  await card.getByLabel("淺草散步 的更多操作").click();
  await card.getByRole("button", { name: "移動 淺草散步", exact: true }).click();
  await test.info().attach("move-dialog-dom", { contentType: "application/json", body: await page.locator('[role="dialog"]').evaluate((element) => JSON.stringify({
    markup: element.outerHTML.slice(0, 450),
    labels: Array.from(document.querySelectorAll('[id]')).filter((node) => node.id === element.getAttribute('aria-labelledby')).map((node) => ({ html: node.outerHTML, hidden: node.closest('[inert], [aria-hidden="true"]')?.outerHTML.slice(0, 250) })),
  })) });
  const move = page.getByRole("dialog", { name: "移動這個行程" });
  await move.getByLabel("日期").selectOption("2026-11-12");
  await move.getByRole("button", { name: "移到這裡" }).click();
  await expect.poll(() => state.current().items.find((item) => item.id === "asakusa")?.day_date).toBe("2026-11-12");
  expect(state.current().items.filter((item) => item.system_role).length).toBe(8);
});

test("AI preview is cancellable and does not write until explicit apply", async ({ page }, testInfo) => {
  const state = await workspace(page);
  const aiButton = page.locator(".premium-desktop-actions button").first();
  const open = async () => {
    if (await aiButton.isVisible()) await aiButton.click();
    else await page.locator(".premium-mobile-dock button").last().click();
  };
  await open();
  let dialog = page.getByRole("dialog");
  await expect(dialog.getByRole("button", { name: "調整現有行程", exact: true })).toBeVisible();
  await dialog.getByRole("button", { name: "產生預覽 · 不扣次", exact: true }).click();
  await expect(dialog.locator("strong").filter({ hasText: /^淺草寺$/ })).toBeVisible();
  expect(state.writes).toEqual([]);
  expect(state.current().version).toBe(1);
  await page.screenshot({ path: testInfo.outputPath("premium-ai-preview.png"), fullPage: true });
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  expect(state.current().version).toBe(1);
  await open();
  dialog = page.getByRole("dialog");
  await dialog.getByRole("button", { name: "產生預覽 · 不扣次", exact: true }).click();
  await dialog.getByRole("button", { name: /套用.*免費/ }).click();
  await expect.poll(() => state.writes).toEqual(["apply"]);
  expect(state.current().items.some((item) => item.id === "asakusa")).toBe(true);
});


test("single-page creation needs only city and dates and opens an unpaid blank itinerary", async ({ page }, testInfo) => {
  if ((page.viewportSize()?.width || 1280) < 1024) await page.setViewportSize({ width: 390, height: 844 });
  let createdBody: Record<string, unknown> | undefined;
  let createCount = 0;
  const unexpectedRequests: string[] = [];
  const mutationPaths: string[] = [];
  let createdTrip = { ...structuredClone(editorFixture), id: "premium-created-trip", items: [], primary_lodging: null };
  await pretendSignedIn(page);
  // Catch every browser API request so an unexpected provider call cannot reach a real service.
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (!["GET", "HEAD"].includes(request.method())) mutationPaths.push(path);
    if (path.endsWith("/auth/me")) return route.fulfill({ json: { id: "premium-create-ui", email: "create-ui@example.test", role: "user", is_active: true } });
    // The global shell and editor also read first-party state, never paid providers.
    if (request.method() === "GET" && ["/api/travel/saved-items", "/api/travel/trips"].includes(path)) return route.fulfill({ json: [] });
    if (request.method() === "GET" && ["/api/travel/community/status", "/api/travel/discovery/status", "/api/travel/analytics/config"].includes(path)) return route.fulfill({ json: { enabled: false } });
    if (request.method() === "GET" && ["/api/travel/usage", "/api/travel/runtime/public-config", "/api/travel/trips/premium-created-trip/health"].includes(path)) return route.fulfill({ json: {} });
    if (path.endsWith("/holidays")) return route.fulfill({ json: { country: "JP", country_name: "日本", locale: "zh-TW", coverage_start: null, coverage_end: null, attribution: "", holidays: [] } });
    if (path === "/api/travel/trips" && request.method() === "POST") {
      createCount += 1;
      createdBody = request.postDataJSON();
      createdTrip = { ...createdTrip, name: String(createdBody!.name), destination_name: String(createdBody!.destination_name), start_date: String(createdBody!.start_date), end_date: String(createdBody!.end_date) };
      return route.fulfill({ status: 201, json: createdTrip });
    }
    if (path === "/api/travel/trips/premium-created-trip" && request.method() === "GET") return route.fulfill({ json: createdTrip });
    unexpectedRequests.push(path);
    return route.fulfill({ status: 503, json: { detail: "Unstubbed request blocked by isolated creation test" } });
  });

  await page.goto("/zh-TW/trips/new");
  await expect(page.getByRole("heading", { name: "先選一座城市，開始你的旅行" })).toBeVisible();
  const startPlanning = page.getByRole("button", { name: "開始安排", exact: true });
  if ((page.viewportSize()?.width || 1280) < 1024) {
    const bounds = (await startPlanning.boundingBox())!;
    expect(bounds.y).toBeGreaterThan(0);
    expect(bounds.y + bounds.height).toBeLessThanOrEqual(page.viewportSize()!.height);
    await expect(page.locator(".app-bottom-nav")).toBeHidden();
    expect(await startPlanning.evaluate((button) => {
      const bounds = button.getBoundingClientRect();
      return button.contains(document.elementFromPoint(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2));
    })).toBe(true);
  }
  await startPlanning.click();
  await expect(page.locator(".premium-new-trip").getByRole("alert")).toContainText("請輸入目的地");
  await page.getByRole("button", { name: "東京", exact: true }).click();
  await startPlanning.click();
  await expect(page.locator(".premium-new-trip").getByRole("alert")).toContainText("請選擇開始與結束日期");
  expect(createCount).toBe(0);
  const travelers = page.locator(".calm-new-trip-travelers");
  await expect(travelers).not.toHaveAttribute("open", "");
  await travelers.locator("summary").click();
  await expect(page.getByLabel("成人", { exact: true })).toHaveValue("2");
  await expect(page.getByLabel("兒童", { exact: true })).toHaveValue("0");
  await expect(page.getByLabel("房間", { exact: true })).toHaveValue("1");
  await travelers.locator("summary").click();
  await expect(page.locator(".premium-new-trip-advanced")).not.toHaveAttribute("open", "");
  await expect(page.getByRole("grid")).toHaveCount(0);

  const [start, end] = await page.evaluate(() => [14, 19].map((offset) => {
    const date = new Date();
    date.setDate(date.getDate() + offset);
    return date.toLocaleDateString("sv");
  }));
  await page.getByRole("button", { name: "選擇旅行日期", exact: true }).click();
  for (const date of [start, end]) {
    const cell = page.locator('[data-date="' + date + '"]');
    for (let attempt = 0; attempt < 3 && await cell.count() === 0; attempt += 1) await page.getByRole("button", { name: "下個月", exact: true }).click();
    await cell.click();
  }
  await page.locator(".calm-new-trip-name > summary").click();
  await expect(page.getByLabel("旅程名稱", { exact: true })).toHaveValue("東京・6 天");
  await page.locator(".calm-new-trip-name > summary").click();
  // Completing both dates now collapses the calendar automatically.
  await expect(page.getByRole("grid")).toHaveCount(0);
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: "instant" }));
  if ((page.viewportSize()?.width || 1280) < 1024) {
    const bounds = (await startPlanning.boundingBox())!;
    expect(bounds.y + bounds.height).toBeLessThanOrEqual(page.viewportSize()!.height);
    expect(await startPlanning.evaluate((button) => {
      const bounds = button.getBoundingClientRect();
      return button.contains(document.elementFromPoint(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2));
    })).toBe(true);
  }
  await page.screenshot({ path: testInfo.outputPath("premium-single-page-create.png"), fullPage: true });
  await startPlanning.click();
  await expect(page).toHaveURL(/\/zh-TW\/trips\/premium-created-trip$/);
  await expect(page.getByRole("heading", { name: "東京・6 天", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "加入第一個地點", exact: true })).toBeVisible();

  expect(createCount).toBe(1);
  expect(createdBody).toMatchObject({
    source: "blank", planning_mode: "manual_blank", name: "東京・6 天", destination_name: "東京", destination_place_id: null,
    start_date: start, end_date: end, travelers: { adults: 2, children: 0, rooms: 1 },
    routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
  });
  expect(mutationPaths).toEqual(["/api/travel/trips"]);
  expect(unexpectedRequests).toEqual([]);
});
