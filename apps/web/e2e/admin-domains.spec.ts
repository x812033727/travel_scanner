import { expect, test, type Page } from "@playwright/test";
import { pretendSignedIn } from "./session";

async function fixture(page: Page) {
  await pretendSignedIn(page);
  const reads: string[] = [], writes: { path: string; body: Record<string, unknown> }[] = [];
  const operation = { used: 0, feature_used: 0, budget: 100, percentage: 0, projected_month_end: 0, projected_percentage: 0, alert: "normal" };
  const provider = (name: string, config: Record<string, string | number | boolean>) => ({
    provider: name, label: name === "google_maps" ? "Google Maps" : name, description: "Isolated test fixture",
    enabled: true, configured: false, status: "unavailable", status_message: "Fixture only",
    config, config_sources: Object.fromEntries(Object.keys(config).map((key) => [key, "environment"])),
    secrets: {}, updated_at: null as string | null,
  });
  const snapshot = { encryption_source: "SETTINGS_ENCRYPTION_KEY", audit: [], providers: [
    provider("google_maps", { restaurant_scan_enabled: false, restaurant_scan_refresh_days: 7, route_cache_ttl_seconds: 900 }),
    provider("runtime", { hotel_provider_mode: "mock", registration_enabled: true }),
  ] };
  const hotels = { products: [], offers: [], destination_offers: [], destinations: [], brands: [], brand_definitions: {}, coverage: [], review_due: 0, imports: [], operations: {}, network_configured: false, project_id: null,
    config: { public_enabled: false, enabled_kinds: [], enabled_destinations: [], direct_hotel_links_enabled: false, hotel_quote_policies: {} }, version: 0, summary: { total: 0, pending: 0, approved: 0, disabled: 0 } };
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const url = new URL(request.url()), path = url.pathname.replace("/api/travel", "");
    let body: unknown = { items: [], total: 0, page: 1, pages: 0 };
    if (request.method() !== "GET") {
      const payload = request.postDataJSON() ?? {};
      if (path.startsWith("/admin/")) writes.push({ path, body: payload });
      if (path === "/admin/provider-settings/google_maps" && request.method() === "PUT") {
        Object.assign(snapshot.providers[0].config, payload.config);
        snapshot.providers[0].updated_at = "2026-09-08T12:00:00Z";
        body = snapshot;
      } else { await route.fulfill({ status: 403, json: { detail: "Unexpected write in isolated UI fixture" } }); return; }
    } else {
      reads.push(path + url.search);
      if (path === "/auth/me") body = { id: "fixture-admin", email: "admin@example.test", is_admin: true, can_deploy: false };
      else if (path === "/analytics/config") body = { first_party_enabled: false, ga4_enabled: false };
      else if (path === "/admin/provider-settings") body = snapshot;
      else if (path === "/admin/dashboard") body = { counts: { hotspots_total: 10, foods_total: 4, merchants_total: 6, hotels_total: 3, hotspots_pending: 2, foods_pending: 1, merchants_pending: 1, guides_pending: 0, hotels_pending: 1, hotels_without_options: 2 }, can_deploy: false };
      else if (path === "/admin/hotels" || path === "/admin/travel-services") body = hotels;
      else if (path === "/admin/catalog-review") body = { pending_counts: { hotspot: 0, food: 0, merchant: 0, total: 0 }, runs: [], active_run: null, can_discover: false, settings: { enabled: false, configured: false }, providers: {}, usage: {} };
      else if (path === "/admin/hotspots/restaurants/coverage") body = { items: [], total: 0, completed: 0, automation_enabled: false, usage: { available: false, period: "2026-09", operations: { aggregate: operation, nearby: operation, details: operation, ids_only: { used: 0, billing: "no_charge", budget: null, operations: { text_search: 0, place_id_refresh: 0 } } }, skus: [] } };
      else if (path === "/admin/hotspots/restaurants/editorial-coverage") body = { items: [], restaurant_places: { listed: 0, approved: 0, missing: 0 }, food_merchants: { total: 0, destination_context: 0, direct_merchant_evidence: 0, official_website: 0, by_country: [], disclosure: "Fixture only" } };
      else if (path.startsWith("/runtime/") || path.startsWith("/usage-catalog")) { await route.continue(); return; }
    }
    await route.fulfill({ status: 200, json: body });
  });
  return { reads, writes };
}

async function selectTab(page: Page, tab: string, label: string) {
  const desktopTab = page.getByRole("tab", { name: label, exact: true });
  const mobileTabs = page.getByRole("combobox", { name: "管理工作區", exact: true });
  await expect(desktopTab.or(mobileTabs)).toBeVisible();
  if (await desktopTab.isVisible()) await desktopTab.click();
  else await mobileTabs.selectOption(tab);
}

test("three domains, deep search and navigation are usable on desktop and Pixel 7", async ({ page }, info) => {
  const { reads, writes } = await fixture(page);
  await page.goto("/zh-TW/admin");
  for (const name of ["景點", "美食", "飯店"]) await expect(page.getByRole("region", { name, exact: true })).toBeVisible();
  if (info.project.name === "mobile-chromium") await page.getByRole("button", { name: "開啟營運選單" }).click();
  const nav = page.getByRole("navigation", { name: "營運控制台" });
  // Pending-count badges are part of each link's accessible name, so match the
  // destination label without pinning the server-owned count.
  for (const name of ["景點", "美食", "飯店"]) await expect(nav.getByRole("link", { name })).toBeVisible();
  if (info.project.name === "mobile-chromium") await page.locator("#admin-mobile-navigation").getByRole("button", { name: "關閉營運選單" }).click();
  await page.getByRole("button", { name: "搜尋頁面與操作" }).click();
  const palette = page.getByRole("dialog", { name: "搜尋頁面與操作" });
  await palette.getByRole("textbox", { name: "搜尋頁面與操作" }).fill("餐廳來源");
  await palette.getByRole("link", { name: /餐廳來源/ }).click();
  await expect(page).toHaveURL(/admin\/foods\?tab=nearby&section=sources/);
  await expect(page.getByRole("heading", { name: "美食", exact: true })).toBeVisible();
  await expect.poll(() => reads.some((path) => path.includes("/editorial-coverage"))).toBe(true);
  expect(reads.some((path) => path.includes("coordinate-queue"))).toBe(false);
  expect(writes).toEqual([]);
  await expect(page.locator("html")).toHaveJSProperty("scrollWidth", await page.locator("html").evaluate((node) => node.clientWidth));
});

test("food settings keep drafts and save only owned dirty fields", async ({ page }) => {
  const { reads, writes } = await fixture(page);
  await page.goto("/zh-TW/admin/foods?tab=settings&provider=google_maps&field=restaurant_scan_refresh_days");
  const input = page.getByRole("spinbutton", { name: /餐廳覆蓋重掃週期/ });
  await expect(input).toHaveValue("7");
  await input.fill("9");
  await selectTab(page, "catalog", "目錄");
  await selectTab(page, "settings", "設定");
  await expect(input).toHaveValue("9");
  const panel = page.getByRole("tabpanel", { name: "設定", exact: true });
  await panel.getByRole("button", { name: /儲存/ }).click();
  await expect.poll(() => writes.length).toBe(1);
  expect(writes[0]).toEqual({ path: "/admin/provider-settings/google_maps", body: { config: { restaurant_scan_refresh_days: 9 }, secrets: {}, expected_updated_at: null } });
  await page.reload();
  await expect(input).toHaveValue("9");
  expect(reads.some((path) => path.includes("coordinate-queue"))).toBe(false);
  expect(reads.some((path) => path.endsWith("/test"))).toBe(false);
});

test("legacy hashes redirect without loading the wrong workspace", async ({ page }) => {
  const { reads } = await fixture(page);
  await page.goto("/zh-TW/admin/hotspots?q=Atomic%20Bomb#sources");
  await expect(page).toHaveURL((url) => url.pathname.endsWith("/admin/foods") && url.searchParams.get("tab") === "nearby" && url.searchParams.get("section") === "sources");
  expect(new URL(page.url()).searchParams.get("q")).toBe("Atomic Bomb");
  expect(reads.some((path) => path.includes("/candidates"))).toBe(false);
  await selectTab(page, "catalog", "目錄");
  await selectTab(page, "settings", "設定");
  await page.goBack();
  await expect(page).toHaveURL(/tab=catalog/);
  await page.goForward();
  await expect(page).toHaveURL(/tab=settings/);
});

test("restaurant scan bookmarks lead to the single automation editor without starting a scan", async ({ page }, info) => {
  const { writes } = await fixture(page);
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
  await page.goto("/zh-TW/admin/hotspots#restaurants");
  await expect(page).toHaveURL(/admin\/foods\?tab=nearby&section=scans/);
  await expect(page.getByText("餐廳自動掃描已暫停")).toBeVisible();
  await page.screenshot({ path: info.outputPath("admin-food-scans-dark.png"), fullPage: true });
  await page.getByRole("link", { name: "前往美食設定管理自動掃描" }).click();
  await expect(page.getByRole("switch", { name: /啟用景點周邊餐廳掃描/ })).toBeVisible();
  await expect(page.getByRole("spinbutton", { name: /餐廳覆蓋重掃週期/ })).toHaveValue("7");
  expect(writes).toEqual([]);
  expect(errors).toEqual([]);
});

test("hotel provider deep links and old hotel entries reach the hotel-only workspace", async ({ page }) => {
  const { reads, writes } = await fixture(page);
  await page.goto("/zh-TW/admin/hotels?tab=settings&section=providers&provider=runtime&field=hotel_provider_mode");
  await expect(page.getByRole("combobox", { name: /飯店查詢來源/ })).toHaveValue("mock");
  await expect(page.getByRole("heading", { name: "飯店", exact: true })).toBeVisible();
  expect(reads.some((path) => path.startsWith("/admin/hotels"))).toBe(true);
  await page.goto("/zh-TW/admin/travel-services?type=hotel");
  await expect(page).toHaveURL(/admin\/hotels\?tab=catalog&section=catalog/);
  await expect(page.getByRole("link", { name: "管理共用合作夥伴" })).toBeVisible();
  expect(writes).toEqual([]);
});

for (const [locale, overview, hotels] of [["zh-TW", "總覽", "飯店"], ["zh-CN", "总览", "酒店"], ["en", "Overview", "Hotels"], ["ja", "概要", "ホテル"], ["ko", "개요", "호텔"]]) {
  test(locale + " domain hierarchy and dark mode stay readable", async ({ page }, info) => {
    await fixture(page);
    await page.addInitScript(() => { localStorage.setItem("mokaair-theme", "dark"); });
    await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
    await page.goto("/" + locale + "/admin");
    await expect(page.getByRole("heading", { level: 1, name: overview, exact: true })).toBeVisible();
    await expect(page.getByRole("region", { name: hotels, exact: true })).toBeVisible();
    await expect(page.locator("html")).toHaveJSProperty("scrollWidth", await page.locator("html").evaluate((node) => node.clientWidth));
    const targets = page.getByRole("region", { name: hotels }).getByRole("link");
    for (const target of await targets.all()) expect((await target.boundingBox())?.height).toBeGreaterThanOrEqual(44);
    if (locale === "zh-TW") await page.screenshot({ path: info.outputPath("admin-domains-dark.png"), fullPage: true });
  });
}
