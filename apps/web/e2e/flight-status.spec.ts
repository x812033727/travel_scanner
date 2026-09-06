import { expect, test } from "@playwright/test";

test("visitors are asked to sign in before the priced lookup", async ({ page }) => {
  await page.route("**/api/travel/saved-items?*", (route) => route.fulfill({ status: 401, contentType: "application/problem+json", body: JSON.stringify({ status: 401, code: "authentication_required", detail: "請先登入再繼續" }) }));
  await page.goto("/zh-TW/flights/status");
  await expect(page.getByRole("link", { name: "登入後查詢 · 消耗 1 次" })).toHaveAttribute("href", "/zh-TW/login?next=%2Fflights%2Fstatus");
  await expect(page.getByRole("button", { name: /^查詢 · / })).toHaveCount(0);
});

test("flight status lookup shows exact match and loads track on demand", async ({ page }) => {
  let trackCalls = 0;
  await page.route("**/api/travel/saved-items?*", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [] }) }));
  await page.route("**/api/travel/flights/status-lookups", async (route) => {
    const request = route.request();
    expect(request.headers()["idempotency-key"]).toBeTruthy();
    expect(request.postDataJSON()).toEqual({ ident: "BR198", departure_date: "2026-09-01" });
    await route.fulfill({
      status: 201,
      contentType: "application/json",
      body: JSON.stringify({
        id: "lookup-1",
        cache_hit: false,
        usage: { status: "charged", uses: 1, reference: "usage-1" },
        items: [{
          item_id: "11111111-1111-4111-8111-111111111111",
          fa_flight_id: "BR198-20260901",
          ident: "BR198",
          origin: "TPE",
          destination: "NRT",
          status: "Scheduled",
          schedule_only: false,
          departure_terminal: "2",
          departure_gate: "C5",
          departure_delay_seconds: 900,
          scheduled_out: "2026-09-01T08:30:00+08:00",
          estimated_out: "2026-09-01T08:45:00+08:00",
          updated_at: "2026-09-01T07:30:00+08:00",
        }],
      }),
    });
  });
  await page.route("**/api/travel/flights/status-lookups/lookup-1/items/*/track", async (route) => {
    trackCalls += 1;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        fa_flight_id: "BR198-20260901",
        positions: [
          { latitude: 25.1, longitude: 121.2, altitude: 12000 },
          { latitude: 30.2, longitude: 130.4, altitude: 35000 },
          { latitude: 35.5, longitude: 139.7, altitude: 18000 },
        ],
        retrieved_at: "2026-09-01T09:00:00Z",
        attribution: "FlightAware",
      }),
    });
  });

  await page.goto("/zh-TW/flights/status");
  await page.getByLabel("班號").fill("BR198");
  await page.getByLabel("出發日期").fill("2026-09-01");
  await page.getByRole("button", { name: /^查詢 · 消耗 1 次$/ }).click();

  await expect(page.getByRole("heading", { name: "TPE → NRT" })).toBeVisible();
  await expect(page.getByText("2／C5")).toBeVisible();
  await expect(page.getByText("15 分鐘")).toBeVisible();
  await expect(page.getByText("已扣 1 次")).toBeVisible();
  expect(trackCalls).toBe(0);

  await page.getByRole("button", { name: "顯示實際航跡" }).click();
  await expect(page.getByRole("img", { name: "FlightAware 實際航跡" })).toBeVisible();
  await expect(page.getByText(/Powered by FlightAware/)).toBeVisible();
  expect(trackCalls).toBe(1);
});
