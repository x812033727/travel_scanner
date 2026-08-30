import { expect, test } from "@playwright/test";

test("primary travel flow is visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /少開十個分頁/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /比較完整旅程/ })).toBeVisible();
  await page.getByRole("link", { name: "方案" }).click();
  await expect(page.getByRole("heading", { name: /搜尋點數/ })).toBeVisible();
});

test("Japan Korea Thailand workbench carries structured preferences", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /泰國/ }).click();
  await expect(page.getByRole("button", { name: /^普吉/ })).toBeVisible();
  await page.getByRole("button", { name: /^普吉/ }).click();
  await page.getByLabel("兒童人數").selectOption("2");
  await page.getByRole("button", { name: "海灘／跳島", exact: true }).click();
  await page.getByText("進階住宿與行程條件").click();
  await page.getByText("住宿含早餐").click();
  await Promise.all([
    page.waitForURL(/destination=HKT/, { timeout: 20_000 }),
    page.getByRole("button", { name: /比較完整旅程/ }).click(),
  ]);
  await expect(page).toHaveURL(/children_ages=8%2C8/);
  await expect(page).toHaveURL(/breakfast_required=true/);
});

test("airline public fare lab is available", async ({ page }) => {
  await page.goto("/labs/airlines");
  await expect(page.getByRole("heading", { name: /三家航空/ })).toBeVisible();
  await expect(page.getByRole("button", { name: "搜尋公開票價" })).toBeVisible();
  await expect(page.getByText("中華航空")).toBeVisible();
  await expect(page.getByText("長榮航空")).toBeVisible();
  await expect(page.getByText("星宇航空")).toBeVisible();
});

test("back-to-back fare comparison renders both strategy modes", async ({ page }) => {
  await page.route("**/api/travel/crawlers/airlines/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({
      sources: [
        { airline_code: "CI", airline_name: "中華航空", host: "flights.china-airlines.com", state: "ready", policy: "robots", detail: "ok", quote_count: 0, cache_hit: false },
        { airline_code: "BR", airline_name: "長榮航空", host: "flights.evaair.com", state: "disabled", policy: "fail_closed", detail: "robots unavailable", quote_count: 0, cache_hit: false },
        { airline_code: "JX", airline_name: "星宇航空", host: "www.starlux-airlines.com", state: "ready", policy: "robots", detail: "ok", quote_count: 0, cache_hit: false },
      ],
      safety_rules: [],
    }),
  }));
  await page.route("**/api/travel/crawlers/airlines/back-to-back-fares", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({
      queried_at: "2026-08-30T10:00:00Z",
      pricing_capability: "full_back_to_back",
      comparisons: [
        {
          mode: "mixed_airlines",
          conventional: { tickets: [], original_currency_totals: { TWD: "20000" }, estimated_twd: "20000" },
          back_to_back: { tickets: [], original_currency_totals: { TWD: "18000" }, estimated_twd: "18000" },
          savings_twd: "2000",
          savings_percent: "10.0",
          verdict: "back_to_back_cheaper",
          detail: "混搭航空公司的倒買法估算較省。",
        },
        {
          mode: "same_airline",
          conventional: { tickets: [], original_currency_totals: { TWD: "21000" }, estimated_twd: "21000" },
          back_to_back: { tickets: [], original_currency_totals: { TWD: "19000" }, estimated_twd: "19000" },
          savings_twd: "2000",
          savings_percent: "9.5",
          verdict: "back_to_back_cheaper",
          detail: "同航空公司的倒買法估算較省。",
        },
      ],
      candidates: [],
      fx_rates: [],
      warnings: [],
    }),
  }));

  await page.goto("/labs/airlines");
  await expect(page.getByText("政策停用")).toBeVisible();
  const backToBackTab = page.getByRole("tab", { name: "倒買法" });
  await backToBackTab.click();
  await expect(backToBackTab).toHaveAttribute("aria-selected", "true");
  await expect(page.getByRole("heading", { name: "設定兩趟旅行" })).toBeVisible({ timeout: 15_000 });
  await page.getByRole("button", { name: "比較倒買價格" }).click();
  await expect(page.getByRole("heading", { name: "最低混搭" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最低同航空公司" })).toBeVisible();
  await expect(page.getByText(/(?:倒買法|外站兩段票)估算省下.*2,000/).first()).toBeVisible();
});
