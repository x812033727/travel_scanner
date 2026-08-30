import { expect, test } from "@playwright/test";

test("primary travel flow is visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /少開十個分頁/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /比較完整旅程/ })).toBeVisible();
  await Promise.all([
    page.waitForURL(/\/pricing$/, { timeout: 30_000 }),
    page.getByRole("link", { name: "方案" }).click(),
  ]);
  await expect(page.getByRole("heading", { name: /不綁月租的旅遊查價次數/ })).toBeVisible();
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

test("search criteria can be revised before running a new comparison", async ({ page }) => {
  await page.route("**/api/travel/providers/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({
      provider: "amadeus",
      mode: "test",
      status: "ready",
      modules: ["flight", "hotel", "activities", "transport"],
      message: "供應商測試資料已啟用",
    }),
  }));
  await page.goto("/search?origin=TPE&destination=HKT&departure_date=2026-11-10&return_date=2026-11-15&adults=2&children=0&rooms=1&budget_twd=60000&interests=food&preferred_area=%E6%99%AE%E5%90%89%E8%80%81%E5%9F%8E&pace=balanced");
  await expect(page.getByRole("heading", { name: "泰國・普吉完整旅程" })).toBeVisible();
  await page.getByRole("button", { name: "修改搜尋條件" }).click();
  await page.getByLabel("總預算 TWD").fill("85000");
  await page.getByLabel("回程日期").fill("2026-11-16");
  await page.getByRole("button", { name: "海灘／跳島" }).click();
  await page.getByRole("button", { name: "套用並重新規劃" }).click();
  await expect(page).toHaveURL(/budget_twd=85000/);
  await expect(page).toHaveURL(/return_date=2026-11-16/);
  await expect(page).toHaveURL(/interests=food%2Cbeach/);
  await expect(page.getByText(/預算.*85,000/)).toBeVisible();
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
      query: { strategy: "reverse_two_segment" },
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
  await expect(page.getByText(/外站兩段票估算省下.*2,000/).first()).toBeVisible();
});

test("different destinations can complete an external two-segment comparison", async ({ page }) => {
  await page.route("**/api/travel/crawlers/airlines/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ sources: [], safety_rules: [] }),
  }));
  let submitted: Record<string, unknown> = {};
  await page.route("**/api/travel/crawlers/airlines/back-to-back-fares", (route) => {
    submitted = route.request().postDataJSON();
    const manual = (role: string, amount: string, segments: Array<Record<string, string>>) => ({
      role,
      origin: segments[0].origin,
      destination: segments.at(-1)?.destination,
      departure_date: segments[0].departure_date,
      amount,
      currency: "TWD",
      airline_code: "CI",
      estimated_twd: amount,
      source: "manual",
      is_live: false,
      segments,
    });
    const backToBack = {
      tickets: [],
      supplemental_fares: [
        manual("head_one_way", "3000", [{ origin: "TPE", destination: "TYO", departure_date: "2027-02-26" }]),
        manual("middle_two_segment", "9000", [
          { origin: "TYO", destination: "TPE", departure_date: "2027-03-10" },
          { origin: "TPE", destination: "SEL", departure_date: "2027-03-18" },
        ]),
        manual("tail_one_way", "4000", [{ origin: "SEL", destination: "TPE", departure_date: "2027-03-22" }]),
      ],
      original_currency_totals: { TWD: "16000" },
      estimated_twd: "16000",
    };
    const comparison = {
      conventional: { tickets: [], supplemental_fares: [], original_currency_totals: { TWD: "22000" }, estimated_twd: "22000" },
      back_to_back: backToBack,
      savings_twd: "6000",
      savings_percent: "27.3",
      verdict: "back_to_back_cheaper",
      detail: "外站兩段票估算較省。",
    };
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        queried_at: "2026-08-30T10:00:00Z",
        query: { strategy: "reverse_two_segment", first_destination: "TYO", second_destination: "SEL" },
        pricing_capability: "full_back_to_back",
        comparisons: [
          { ...comparison, mode: "mixed_airlines" },
          { ...comparison, mode: "same_airline" },
        ],
        candidates: [],
        fx_rates: [],
        warnings: [],
      }),
    });
  });

  await page.goto("/labs/airlines");
  await page.getByRole("tab", { name: "倒買法" }).click();
  await page.getByLabel("第二次目的地").selectOption("SEL");
  await page.getByLabel("頭段單程每人價格").fill("3000");
  await page.getByLabel("中段反向兩航段每人價格").fill("9000");
  await page.getByLabel("尾段單程每人價格").fill("4000");
  await page.getByLabel("第一次一般來回每人價格").fill("12000");
  await page.getByLabel("第二次一般來回每人價格").fill("10000");
  await page.getByRole("button", { name: "比較倒買價格" }).click();

  await expect(page.getByText("不同目的地的外站兩段票已支援")).toBeVisible();
  await expect(page.getByText(/外站兩段票估算省下.*6,000/).first()).toBeVisible();
  await expect(page.getByText("SEL").first()).toBeVisible();
  expect(submitted).toMatchObject({
    first_destination: "TYO",
    second_destination: "SEL",
    middle_two_segment_fare: { amount: "9000" },
    conventional_first_fare: { amount: "12000" },
    conventional_second_fare: { amount: "10000" },
  });
});
