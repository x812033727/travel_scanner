import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ id: "00000000-0000-4000-8000-000000000001", email: "tester@example.com" }),
  }));
});

test("primary travel flow is visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /少開十個分頁/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /下一步/ })).toBeVisible();
  const mobileMenu = page.getByRole("button", { name: "開啟導覽選單" });
  if (await mobileMenu.isVisible()) await mobileMenu.click();
  await Promise.all([
    page.waitForURL(/\/pricing$/, { timeout: 30_000 }),
    page.getByRole("link", { name: "方案" }).click(),
  ]);
  await expect(page.getByRole("heading", { name: /不綁月租的旅遊查價次數/ })).toBeVisible();
});

test("new trip asks visitors to sign in before showing the long form", async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 401,
    contentType: "application/json",
    body: JSON.stringify({ detail: "未登入" }),
  }));
  await page.goto("/trips/new");
  await expect(page.getByRole("heading", { name: "先登入，再建立你的行程" })).toBeVisible();
  await expect(page.getByRole("link", { name: "前往登入" })).toBeVisible();
  await expect(page.getByLabel("旅程名稱")).toHaveCount(0);
});

test("new trip surfaces authentication service failures", async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 500,
    contentType: "application/json",
    body: JSON.stringify({ detail: "資料庫錯誤" }),
  }));
  await page.goto("/trips/new");
  await expect(page.getByRole("heading", { name: "目前無法確認登入狀態" })).toBeVisible();
  await expect(page.getByRole("link", { name: "前往登入" })).toHaveCount(0);
});

test("Japan Korea Thailand workbench carries structured preferences", async ({ page }) => {
  await page.route("**/api/travel/destinations/discover", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({
      assumptions: ["推薦階段使用估算資料"],
      recommendations: [{ candidate_id: "HKT:2026-11-10:5", city: "普吉", airport: "HKT", country: "泰國", country_code: "TH", areas: ["普吉老城", "卡塔"], reason: "海灘與度假選擇完整", departure_date: "2026-11-10", return_date: "2026-11-15", trip_length_days: 5, estimated_flight_twd: 21000, estimated_lodging_twd: 18000, estimated_total_twd: 55000, score: 92, matched_interests: ["beach"], relaxed_preferences: [] }],
    }),
  }));
  await page.goto("/");
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: /泰國/ }).click();
  await page.getByLabel("指定城市").selectOption("HKT");
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByLabel("兒童人數").selectOption("2");
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: "兩種都接受" }).click();
  await page.getByText("需要含早餐").click();
  await page.getByRole("button", { name: /下一步/ }).click();
  await page.getByRole("button", { name: "海灘／跳島", exact: true }).click();
  await page.getByRole("button", { name: /請 AI 推薦 3 組/ }).click();
  await expect(page.getByRole("heading", { name: "泰國・普吉" })).toBeVisible();
  await page.getByLabel("偏好住宿區域").selectOption("普吉老城");
  await Promise.all([
    page.waitForURL(/destination=HKT/, { timeout: 20_000 }),
    page.getByRole("button", { name: /用這組條件搜尋/ }).click(),
  ]);
  await expect(page).toHaveURL(/children_ages=8%2C8/);
  await expect(page).toHaveURL(/breakfast_required=true/);
  await expect(page).toHaveURL(/include_airbnb=true/);
  await expect(page).toHaveURL(/accepted_property_types=hotel%2Cvacation_rental/);
});

test("Airbnb official search is available without running the paid comparison", async ({ page }) => {
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
  await page.goto("/search?origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=2&children=1&rooms=1&preferred_area=%E6%96%B0%E5%AE%BF&include_airbnb=true");
  const link = page.getByRole("link", { name: /Airbnb 官方外站搜尋/ });
  await expect(link).toBeVisible();
  const href = await link.getAttribute("href");
  expect(href).toContain("https://www.airbnb.com/s/");
  expect(href).toContain("checkin=2026-11-10");
  expect(href).toContain("checkout=2026-11-15");
  expect(href).toContain("adults=2");
  expect(href).toContain("children=1");
  await expect(page.getByText(/Airbnb 官方外站搜尋不扣次/)).toBeVisible();
});

test("alerts page distinguishes signed-out state from service failures", async ({ page }) => {
  await page.route("**/api/travel/alerts", (route) => route.fulfill({
    status: 401,
    contentType: "application/problem+json",
    body: JSON.stringify({ status: 401, code: "authentication_required", detail: "請先登入再繼續" }),
  }));
  await page.goto("/alerts");
  await expect(page.getByText("登入後才能查看這裡的內容")).toBeVisible();
  await expect(page.getByRole("link", { name: "前往登入" })).toHaveAttribute("href", "/login?next=%2Falerts");
});

test("guest keeps search criteria and is sent back after login", async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 401,
    contentType: "application/problem+json",
    body: JSON.stringify({ status: 401, code: "authentication_required", detail: "請先登入再繼續" }),
  }));
  await page.route("**/api/travel/providers/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ provider: "mock", mode: "mock", status: "ready", modules: ["flight", "hotel"], message: "模擬資料已啟用" }),
  }));
  await page.goto("/search?origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=2&include_airbnb=true");
  const login = page.getByRole("link", { name: "登入後開始搜尋" });
  await expect(login).toBeVisible();
  await expect(login).toHaveAttribute("href", /\/login\?next=%2Fsearch%3Forigin%3DTPE/);
  await expect(page.getByRole("link", { name: /Airbnb 官方外站搜尋/ })).toBeVisible();
});

test("empty search explains missing fields and links home", async ({ page }) => {
  await page.route("**/api/travel/providers/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ provider: "mock", mode: "mock", status: "ready", modules: [], message: "模擬資料已啟用" }),
  }));
  await page.goto("/search");
  await expect(page.getByText(/缺少出發地、目的地或出發日期/)).toBeVisible();
  await expect(page.getByRole("link", { name: "回首頁設定條件" })).toHaveAttribute("href", "/");
});

test("failed login keeps email and clears only password", async ({ page }) => {
  await page.route("**/api/travel/auth/login", (route) => route.fulfill({
    status: 401,
    contentType: "application/problem+json",
    body: JSON.stringify({ status: 401, code: "invalid_credentials", detail: "Email 或密碼不正確" }),
  }));
  await page.goto("/login?next=%2Falerts");
  await page.getByLabel("Email").fill("traveler@example.com");
  await page.getByLabel("密碼").fill("wrong-password");
  await page.getByRole("button", { name: "登入" }).click();
  await expect(page.getByText("Email 或密碼不正確", { exact: true })).toBeVisible();
  await expect(page.getByLabel("Email")).toHaveValue("traveler@example.com");
  await expect(page.getByLabel("密碼")).toHaveValue("");
});

test("mobile menu exposes trips alerts and account links", async ({ page }) => {
  await page.setViewportSize({ width: 412, height: 915 });
  await page.goto("/");
  await page.getByRole("button", { name: "開啟導覽選單" }).click();
  await expect(page.getByRole("navigation", { name: "手機主要導覽" })).toBeVisible();
  await expect(page.getByRole("link", { name: "我的旅程" })).toBeVisible();
  await expect(page.getByRole("link", { name: "價格通知" })).toBeVisible();
  await expect(page.getByRole("link", { name: "會員帳號" })).toBeVisible();
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

test("flexible flight dates show local schedules and require confirmation before a new search", async ({ page }) => {
  const submitted: Array<Record<string, unknown>> = [];
  let affiliateClickMethod = "";
  const flight = {
    id: "flight-live-1", provider: "skyscanner", source_mode: "live", marketing_airline: "星宇航空", airline: "星宇航空", operating_airlines: ["星宇航空"], selling_agent: "測試售票平台", origin: "TPE", destination: "NRT", departure_time: "2026-11-10T08:00:00+08:00", arrival_time: "2026-11-10T12:00:00+09:00", return_departure_time: "2026-11-15T13:00:00+09:00", return_arrival_time: "2026-11-15T16:00:00+08:00", total_price: 15000, stops: 0, clickout_available: false, segments: [
      { origin: "TPE", destination: "NRT", departure_time: "2026-11-10T08:00:00+08:00", arrival_time: "2026-11-10T12:00:00+09:00", airline: "星宇航空", flight_number: "JX800", leg_index: 0 },
      { origin: "NRT", destination: "TPE", departure_time: "2026-11-15T13:00:00+09:00", arrival_time: "2026-11-15T16:00:00+08:00", airline: "星宇航空", flight_number: "JX801", leg_index: 1 },
    ],
  };
  const options = [
    { shift_days: 0, departure_date: "2026-11-10", return_date: "2026-11-15", lowest_price: 15000, currency: "TWD", provider: "skyscanner", source_mode: "live", is_current: true, offer_count: 1 },
    { shift_days: 2, departure_date: "2026-11-12", return_date: "2026-11-17", lowest_price: 12800, currency: "TWD", provider: "skyscanner", source_mode: "estimate", is_current: false, offer_count: 2 },
  ];
  await page.route("**/api/travel/providers/status", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ provider: "skyscanner", mode: "live", status: "ready", modules: ["flight", "hotel", "activities", "transport"], message: "即時資料已啟用" }) }));
  await page.route("**/api/travel/searches", (route) => {
    submitted.push(route.request().postDataJSON());
    return route.fulfill({ status: 202, contentType: "application/json", body: JSON.stringify({ search_id: `search-${submitted.length}`, usage: { status: "reserved", uses: 1, reference: `usage-${submitted.length}` } }) });
  });
  await page.route(/\/api\/travel\/searches\/search-\d+\/events/, (route) => route.fulfill({
    status: 200,
    contentType: "text/event-stream",
    body: [
      `event: module.results\ndata: ${JSON.stringify({ progress: 25, module: "flight", offers: [flight] })}\n`,
      `event: flight.date_options\ndata: ${JSON.stringify({ options })}\n`,
      `event: provider.completed\ndata: ${JSON.stringify({ module: "flight", status: "complete" })}\n`,
      `event: search.completed\ndata: ${JSON.stringify({ usage: { status: "charged", uses: 1, reference: "usage" } })}\n`,
    ].join("\n\n") + "\n\n",
  }));
  await page.route(/\/api\/travel\/searches\/search-\d+$/, (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "completed", result: { modules: { flight: [flight] }, plans: [], flight_date_options: options }, warnings: [], usage: { status: "charged", uses: 1, reference: "usage" } }) }));
  await page.route("**/api/travel/affiliates/options?*", (route) => {
    const affiliateModule = new URL(route.request().url()).searchParams.get("module");
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        module: affiliateModule,
        disclosure: "透過合作連結預訂，本站可能獲得分潤，價格不因此增加。",
        options: affiliateModule === "flight" ? [{ partner: "trip_com", display_name: "Trip.com", module: "flight", cta: "到 Trip.com 查看", clickout_url: "/api/travel/affiliates/trip_com/clickout?token=safe-token" }] : [],
      }),
    });
  });
  await page.context().route("**/api/travel/affiliates/trip_com/clickout?token=safe-token", (route) => {
    affiliateClickMethod = route.request().method();
    return route.fulfill({ status: 200, contentType: "text/html", body: "<p>safe affiliate redirect</p>" });
  });

  await page.goto("/search?origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=1&rooms=1&flex_days=7");
  await page.getByRole("button", { name: "確認條件並開始搜尋" }).click();
  await expect.poll(() => submitted.length).toBe(1);
  expect(submitted[0]).toMatchObject({ flex_days: 7, flexible_dates: true });
  await page.getByRole("tab", { name: "機票" }).click();
  await expect(page.getByText("08:00")).toBeVisible();
  await expect(page.getByText("JX800")).toBeVisible();
  await expect(page.getByText(/本站可能獲得分潤/)).toBeVisible();
  const [popup] = await Promise.all([
    page.waitForEvent("popup"),
    page.getByRole("button", { name: /到 Trip.com 查看/ }).click(),
  ]);
  await expect(popup.getByText("safe affiliate redirect")).toBeVisible();
  expect(affiliateClickMethod).toBe("POST");
  await popup.close();
  await page.getByRole("button", { name: /晚 2 日/ }).click();
  expect(submitted).toHaveLength(1);
  await page.getByRole("button", { name: "套用並重新搜尋整趟" }).click();
  await expect.poll(() => submitted.length).toBe(2);
  expect(submitted[1]).toMatchObject({ departure_date: "2026-11-12", return_date: "2026-11-17", flex_days: 0, flexible_dates: false });
  await expect(page).toHaveURL(/departure_date=2026-11-12/);
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

test("live flight provider submits the five-ticket reverse comparison", async ({ page }) => {
  await page.route("**/api/travel/crawlers/airlines/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ sources: [], safety_rules: [] }),
  }));
  let submitted: Record<string, unknown> = {};
  await page.route("**/api/travel/flights/back-to-back", (route) => {
    submitted = route.request().postDataJSON();
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        provider: "skyscanner",
        warnings: ["中段票沒有完整即時報價，因此未拼造倒買總價。"],
        comparisons: [
          { mode: "mixed_airlines", conventional: null, back_to_back: null, savings: null, verdict: "comparison_unavailable", detail: "缺少必要票價" },
          { mode: "same_airline", conventional: null, back_to_back: null, savings: null, verdict: "comparison_unavailable", detail: "缺少必要票價" },
        ],
      }),
    });
  });

  await page.goto("/labs/airlines");
  await page.getByRole("tab", { name: "即時倒買 API" }).click();
  await expect(page.getByRole("heading", { name: "即時倒買價格比較" })).toBeVisible();
  await page.getByLabel("成人").selectOption("2");
  await page.getByRole("button", { name: "開始即時比較" }).click();

  await expect(page.getByRole("heading", { name: "最低混搭" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最低同航空公司" })).toBeVisible();
  await expect(page.getByText(/未拼造倒買總價/)).toBeVisible();
  await expect(page.getByText(/Powered by/)).toBeVisible();
  expect(submitted).toMatchObject({
    first_destination: "NRT",
    second_destination: "KIX",
    travelers: { adults: 2 },
  });
});
