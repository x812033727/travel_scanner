import { expect, test } from "@playwright/test";

// Explicit CI opt-in and loopback guard: this test never writes production settings.
test("admin hotel settings persist without changing other services", async ({ page, baseURL }, info) => {
  test.skip(process.env.ADMIN_DOMAIN_E2E !== "1", "Requires isolated PostgreSQL/Redis stack with fixture administrators.");
  expect(["localhost", "127.0.0.1"]).toContain(new URL(baseURL!).hostname);
  test.setTimeout(90_000);
  const suffix = info.project.name === "mobile-chromium" ? "mobile" : "desktop";
  await page.goto("/zh-TW/login?next=/admin");
  await page.getByLabel("Email").fill("admin-workspace-" + suffix + "@example.com");
  await page.getByLabel("密碼", { exact: true }).fill("isolated-admin-workspace-password-123");
  await page.getByRole("button", { name: "登入", exact: true }).click();
  await expect(page).toHaveURL((url) => url.pathname === "/zh-TW/admin", { timeout: 15_000 });
  await expect(page.getByRole("region", { name: "飯店", exact: true })).toBeVisible();
  const before = await page.evaluate(async () => {
    const response = await fetch("/api/travel/admin/travel-services");
    if (!response.ok) throw new Error("Admin snapshot failed: " + response.status);
    return response.json();
  });
  await page.goto("/zh-TW/admin/hotels?tab=settings&section=catalog");
  const directLabel = page.getByLabel("啟用飯店一般訂房連結", { exact: true });
  await expect(directLabel).toBeVisible();
  const original = await directLabel.isChecked();
  await directLabel.setChecked(!original);
  const saved = page.waitForResponse((response) => response.url().endsWith("/admin/hotels/config") && response.request().method() === "PATCH");
  await directLabel.locator("xpath=ancestor::section[1]").getByRole("button", { name: "儲存設定", exact: true }).click();
  expect((await saved).status()).toBe(200);
  await page.reload();
  await expect(directLabel).toBeChecked({ checked: !original });
  const after = await page.evaluate(async () => {
    const response = await fetch("/api/travel/admin/travel-services");
    if (!response.ok) throw new Error("Admin reload failed: " + response.status);
    return response.json();
  });
  expect(after.config.public_enabled).toBe(before.config.public_enabled);
  expect(after.config.enabled_destinations).toEqual(before.config.enabled_destinations);
  expect(after.config.airalo_feed_enabled).toBe(before.config.airalo_feed_enabled);
  expect(after.config.enabled_kinds.filter((kind: string) => kind !== "hotel")).toEqual(before.config.enabled_kinds.filter((kind: string) => kind !== "hotel"));
  expect(after.config.direct_hotel_links_enabled).toBe(!original);
  const overview = page.waitForResponse((response) => response.url().includes("/admin/catalog-review?scope=foods"));
  await page.goto("/zh-TW/admin/foods?tab=review&section=ai");
  expect((await overview).status()).toBe(200);
  const scoped = await page.evaluate(async () => {
    const response = await fetch("/api/travel/admin/catalog-review?scope=foods");
    return { status: response.status, body: await response.json() };
  });
  expect(scoped.status).toBe(200);
  expect(scoped.body.pending_counts.hotspot).toBe(0);
  expect(scoped.body.runs.every((run: { scope: string }) => run.scope === "foods")).toBe(true);
});
