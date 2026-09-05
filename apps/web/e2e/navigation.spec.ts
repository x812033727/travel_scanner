import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ id: "00000000-0000-4000-8000-000000000001", email: "tester@example.com" }),
  }));
});

for (const [locale, heading] of [
  ["en", /Open fewer tabs\.\s*Understand more of your trip\./],
  ["ja", /タブを減らして、\s*旅をもっと深く理解。/],
  ["ko", /탭은 적게 열고,\s*여행은 더 깊이 이해하세요\./],
  ["zh-TW", /少開十個分頁，\s*多看懂一趟旅行。/],
  ["zh-CN", /少开十个页面，\s*多看懂一趟旅行。/],
] as const) {
  test(`${locale} home has localized metadata shell and hero`, async ({ page }) => {
    await page.goto(`/${locale}`);
    await expect(page.locator("html")).toHaveAttribute("lang", locale);
    await expect(page.getByRole("heading", { name: heading })).toBeVisible();
  });
}

test("first visit detects browser language and preserves query", async ({ request }) => {
  const response = await request.get("/?campaign=autumn", {
    headers: { "Accept-Language": "ja-JP,ja;q=0.9" },
    maxRedirects: 0,
  });
  expect(response.status()).toBeGreaterThanOrEqual(300);
  expect(response.status()).toBeLessThan(400);
  expect(response.headers().location).toMatch(/\/ja\/?\?campaign=autumn$/);
});

test("mobile app shell shows five primary destinations and compact account state", async ({ page }) => {
  let authRequests = 0;
  await page.unroute("**/api/travel/auth/me");
  await page.route("**/api/travel/auth/me", (route) => {
    authRequests += 1;
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: "00000000-0000-4000-8000-000000000001",
        email: "admin@example.com",
        is_admin: true,
      }),
    });
  });
  await page.setViewportSize({ width: 390, height: 760 });
  await page.goto("/zh-TW");
  const navigation = page.getByRole("navigation", { name: "手機主要導覽" });
  await expect(navigation.getByRole("link")).toHaveCount(5);
  await expect(navigation.getByRole("link", { name: "探索" })).toHaveAttribute("href", "/zh-TW/hotspots");
  await expect(page.getByRole("link", { name: "Account" })).toHaveAttribute("href", "/zh-TW/account");
  expect(authRequests).toBe(1);
});

for (const width of [320, 390]) {
  test(`mobile language switch keeps the current page at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 760 });
    await page.goto("/en?campaign=mobile");
    await expect(page.getByRole("combobox", { name: "Appearance" })).toBeEnabled({ timeout: 15_000 });
    await page.getByRole("combobox", { name: "Language" }).selectOption("ja");
    await expect(page).toHaveURL(/\/ja\/?\?campaign=mobile$/);
    await expect(page.locator("html")).toHaveAttribute("lang", "ja");
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(
      await page.evaluate(() => document.documentElement.clientWidth),
    );
  });
}

test("appearance selection persists after reload", async ({ page }) => {
  await page.goto("/en");
  const appearance = page.getByRole("combobox", { name: "Appearance" });
  await expect(appearance).toBeEnabled({ timeout: 15_000 });
  await appearance.selectOption("dark");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect.poll(() => page.evaluate(() => localStorage.getItem("mokaair-theme"))).toBe("dark");

  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(page.getByRole("combobox", { name: "Appearance" })).toHaveValue("dark");
});

test("primary travel flow is visible", async ({ page }) => {
  await page.goto("/zh-TW");
  await expect(page.getByRole("heading", { name: /少開十個分頁/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /下一步/ })).toBeVisible();
  await page.goto("/zh-TW/pricing");
  await expect(page.getByRole("heading", { name: /不綁月租的旅遊查價次數/ })).toBeVisible();
});

test("new trip asks visitors to sign in before showing the long form", async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 401,
    contentType: "application/json",
    body: JSON.stringify({ detail: "未登入" }),
  }));
  await page.goto("/zh-TW/trips/new");
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
  await page.goto("/zh-TW/trips/new");
  await expect(page.getByRole("heading", { name: "目前無法確認登入狀態" })).toBeVisible();
  await expect(page.getByRole("link", { name: "前往登入" })).toHaveCount(0);
});

test("mobile-first planner edits, autosaves, and previews before charging", async ({ page }) => {
  const baseTrip = {
    id: "mobile-trip", name: "東京手機行程", mode: "manual", total_price: 0, currency: "TWD",
    data: {}, version: 1, destination_name: "東京", start_date: "2026-11-11", end_date: "2026-11-11",
    timezone: "Asia/Tokyo", route_preference: "FEWER_TRANSFERS", share_enabled: false, route_segments: [],
    items: [
      { id: "stop-1", item_type: "custom", day_date: "2026-11-11", position: 0, title: "淺草寺", location_name: "淺草", latitude: 35.71, longitude: 139.79, provider_place_id: "asakusa", locked: false, fixed_time: false, is_estimated: false, duration_minutes: 60, data: {} },
      { id: "stop-2", item_type: "custom", day_date: "2026-11-11", position: 1, title: "晴空塔", location_name: "押上", latitude: 35.71, longitude: 139.81, provider_place_id: "skytree", locked: false, fixed_time: false, is_estimated: false, duration_minutes: 60, data: {} },
    ],
  };
  let currentTrip: typeof baseTrip & { planning?: Record<string, unknown> } = baseTrip;
  let saves = 0;
  let aiRequest: { scope: string; day_date: string | null } | undefined;
  await page.route("**/api/travel/runtime/public-config", (route) => route.fulfill({ status: 200, contentType: "application/json", body: "{}" }));
  await page.route("**/api/travel/affiliates/options**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ options: [] }) }));
  await page.route("**/api/travel/trips/mobile-trip**", async (route) => {
    const url = route.request().url();
    const method = route.request().method();
    if (url.endsWith("/itinerary/optimize/preview")) {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({
        preview_id: "preview-1", expires_at: "2026-11-11T10:10:00Z", base_version: currentTrip.version,
        route_preference: "FEWER_TRANSFERS", changed: true, warnings: [], segments: [], charge_on_apply: 1,
        total_duration_before_minutes: 40, total_duration_after_minutes: 24,
        days: [{ date: "2026-11-11", duration_before_minutes: 40, duration_after_minutes: 24, saved_minutes: 16,
          before: currentTrip.items.map((item, index) => ({ id: item.id, title: item.title, position: index, locked: false, fixed_time: false })),
          after: [...currentTrip.items].reverse().map((item, index) => ({ id: item.id, title: item.title, position: index, locked: false, fixed_time: false })),
        }],
      }) });
      return;
    }
    if (url.endsWith("/itinerary/optimize/apply")) {
      currentTrip = { ...currentTrip, version: currentTrip.version + 1 };
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ...currentTrip, usage: { status: "charged", uses: 1, reference: "usage-1" } }) });
      return;
    }
    if (url.endsWith("/itinerary/preview")) {
      const body = route.request().postDataJSON();
      aiRequest = { scope: body.scope, day_date: body.day_date };
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({
        preview_id: "ai-preview-1",
        base_version: currentTrip.version,
        expires_at: "2026-11-11T10:15:00Z",
        scope: body.scope,
        day_date: body.day_date,
        planning: {
          status: "live", readiness: "ready", provider: "minimax",
          model: "MiniMax-M2.1", generated_at: "2026-11-11T10:00:00Z", warnings: [],
        },
        days: [{ date: "2026-11-11", label: "2026-11-11", items: currentTrip.items }],
        unscheduled_slots: [],
        readiness: {
          status: "ready", has_lodging: false, exact_item_count: currentTrip.items.length,
          hotspot_candidate_count: 12, merchant_candidate_count: 4,
          preserved_item_count: currentTrip.items.length, assumptions: [],
        },
        routing_summary: {
          exact_items: currentTrip.items.length,
          eligible_pairs: Math.max(0, currentTrip.items.length - 1),
          hotel_pairs_deferred: 2,
        },
      }) });
      return;
    }
    if (url.endsWith("/itinerary/apply")) {
      currentTrip = {
        ...currentTrip,
        version: currentTrip.version + 1,
        planning: {
          status: "live",
          provider: "minimax",
          model: "MiniMax-M2.1",
          generated_at: "2026-11-11T10:00:00Z",
          warnings: [],
          scope: aiRequest?.scope,
          day_date: aiRequest?.day_date,
        },
      };
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ...currentTrip, usage: { status: "charged", uses: 1, reference: "ai-usage-1" } }) });
      return;
    }
    if (method === "PUT") {
      const body = route.request().postDataJSON();
      currentTrip = { ...currentTrip, version: currentTrip.version + 1, items: body.items };
      saves += 1;
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
      return;
    }
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
  });

  await page.goto("/zh-TW/trips/mobile-trip");
  if (test.info().project.name !== "mobile-chromium") {
    await expect(page.locator(".planner-app-bar")).toBeHidden();
    await expect(page.getByText(/行程規劃器/)).toBeVisible();
    return;
  }
  await expect(page.getByRole("heading", { name: "東京手機行程" })).toBeVisible();
  await expect(page.getByRole("button", { name: "返回我的旅行" })).toBeVisible();
  await page.setViewportSize({ width: 320, height: 700 });
  await expect(page.getByRole("heading", { name: "11月11日週三" })).toBeVisible();
  await expect(page.getByText("2 個已安排 · 停留約 2 小時")).toBeVisible();
  await expect(page.locator(".planner-timeline-marker")).toHaveText(["1", "2"]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(
    await page.evaluate(() => document.documentElement.clientWidth),
  );
  await page.getByRole("button", { name: "排序行程" }).click();
  // Reordering now keeps the dock on screen with an explicit exit; the day
  // header keeps its own toggle, so scope to the dock.
  const dockDone = page.locator(".planner-mobile-dock").getByRole("button", { name: "完成排序" });
  await expect(dockDone).toBeVisible();
  const moveUp = await page.getByRole("button", { name: "上移 晴空塔" }).boundingBox();
  const moveDown = await page.getByRole("button", { name: "下移 晴空塔" }).boundingBox();
  expect(Math.abs((moveUp?.x || 0) - (moveDown?.x || 0))).toBeLessThan(2);
  // Round before comparing: the layout engine reports a 44px control as
  // 43.99993896484375 on some runners, which is a float artefact and not a
  // control that misses the 44px touch target.
  expect(Math.round(moveUp?.height || 0)).toBeGreaterThanOrEqual(44);
  await dockDone.click();
  const addButton = page.getByRole("button", { name: "新增安排" });
  await addButton.click();
  await expect(page.getByRole("dialog", { name: "新增安排" })).toBeVisible();
  await expect(page.locator(".planner-timeline-marker")).toHaveCount(2);
  await page.waitForTimeout(1_100);
  expect(saves).toBe(0);
  await page.getByRole("button", { name: "取消" }).click();
  await expect(page.getByRole("dialog", { name: "新增安排" })).toBeHidden();
  await expect(page.locator(".planner-timeline-marker")).toHaveCount(2);
  await addButton.click();
  await page.getByLabel("安排名稱").fill("銀座午餐");
  await page.getByRole("button", { name: "加入行程" }).click();
  const addedCard = page.getByRole("heading", { name: "銀座午餐" }).locator("xpath=ancestor::article");
  await expect(addedCard).toBeVisible();
  await expect(addedCard).toHaveClass(/planner-itinerary-card-new/);
  await expect(page.getByText("已加入行程")).toBeVisible();
  await expect.poll(() => page.evaluate(() => {
    const card = document.querySelector(".planner-itinerary-card-new")?.getBoundingClientRect();
    return Boolean(card && card.top >= 0 && card.bottom <= window.innerHeight);
  })).toBe(true);
  const completionLayout = await page.evaluate(() => {
    const toast = document.querySelector(".planner-toast-stack")?.getBoundingClientRect();
    const dock = document.querySelector(".planner-mobile-dock")?.getBoundingClientRect();
    return { toastBottom: toast?.bottom, dockTop: dock?.top };
  });
  expect(completionLayout.toastBottom || 701).toBeLessThan(completionLayout.dockTop || 0);
  await expect.poll(() => saves).toBe(1);
  await page.getByRole("button", { name: "開啟旅程工具" }).click();
  await expect(page.getByRole("dialog", { name: "旅程工具" })).toBeVisible();
  await page.getByRole("radio", { name: /暮紫/ }).click();
  await expect(page.locator("[data-planner-theme='lavender']")).toBeVisible();
  await page.getByRole("button", { name: "關閉" }).click();
  await page.getByRole("button", { name: "編輯 淺草寺" }).click();
  await page.getByLabel("安排名稱").fill("淺草寺與雷門");
  await page.getByRole("button", { name: "關閉" }).click();
  await expect.poll(() => saves).toBe(2);
  await page.getByRole("button", { name: /^AI 幫我安排 · 消耗 1 次$/ }).click();
  await expect(page.getByRole("dialog", { name: "AI 幫我安排" })).toBeVisible();
  await expect(page.getByRole("radio", { name: /單日安排/ })).toHaveAttribute("aria-checked", "true");
  await expect(page.getByRole("radio", { name: /全行程安排/ })).toBeVisible();
  await page.getByRole("button", { name: /^產生預覽 · 不扣次$/ }).click();
  await expect.poll(() => aiRequest).toEqual({ scope: "day", day_date: "2026-11-11" });
  await expect(page.getByRole("dialog", { name: "確認 AI 行程預覽" })).toBeVisible();
  await page.getByRole("button", { name: /^套用行程 · 消耗 1 次$/ }).click();
  await expect(page.getByText(/MiniMax 已套用.*並扣除 1 次/)).toBeVisible();
  await page.getByRole("button", { name: /^AI 幫我安排 · 消耗 1 次$/ }).click();
  await page.getByRole("button", { name: /只調整現有動線/ }).click();
  await expect(page.getByRole("dialog", { name: "最佳化預覽" })).toBeVisible();
  await expect(page.getByText("預計節省")).toBeVisible();
  await page.getByRole("button", { name: /^套用 · 消耗 1 次$/ }).click();
  await expect(page.getByText(/已套用最佳動線並扣除 1 次/)).toBeVisible();
  const box = await addButton.boundingBox();
  expect(Math.round(box?.height || 0)).toBeGreaterThanOrEqual(44);
});

test("route drawer previews a car route before applying and keeps it after reload", async ({ page }) => {
  const transitSegment = {
    from_item_id: "route-stop-1", to_item_id: "route-stop-2", status: "resolved", travel_mode: "transit", is_override: false,
    provider: "google_routes", attribution: "Google Maps", generated_at: "2026-09-01T01:00:00Z", expires_at: "2026-09-01T01:15:00Z",
    schedule_mode: "scheduled", preference: "FEWER_TRANSFERS", duration_minutes: 24, buffer_minutes: 10,
    departure_time: "2026-11-11T01:00:00Z", arrival_time: "2026-11-11T01:24:00Z", ready_time: "2026-11-11T01:34:00Z",
    distance_meters: 7200, steps: [], details_available: [] as string[], warnings: [] as string[],
  };
  const carSegment = {
    ...transitSegment, travel_mode: "drive", is_override: true, duration_minutes: 12, buffer_minutes: 10,
    arrival_time: "2026-11-11T01:12:00Z", ready_time: "2026-11-11T01:22:00Z", distance_meters: 6100,
    warnings: ["汽車時間不包含停車或叫車等待時間"],
  };
  const carOptions = [12, 14, 17].map((duration, index) => ({
    preview_id: `route-preview-${index + 1}`,
    provider_route_key: `drive-${index + 1}`,
    rank: index + 1,
    expires_at: "2026-09-01T01:15:00Z",
    segment: {
      ...carSegment,
      duration_minutes: duration,
      route_option_rank: index + 1,
      provider_route_key: `drive-${index + 1}`,
      encoded_polyline: `_p~iF~ps|U_ulLnnqC_mqNvxq\`${index}`,
    },
    schedule_impact: { affected_items: [{ item_id: "route-stop-2", title: "晴空塔", old_start_time: "2026-11-11T01:34:00Z", new_start_time: `2026-11-11T01:${22 + index * 2}:00Z`, delta_minutes: -12 + index * 2 }], conflicts: [] },
  }));
  const routeItems = [
    { id: "route-stop-1", item_type: "custom", day_date: "2026-11-11", position: 0, title: "淺草寺", location_name: "淺草", latitude: 35.71, longitude: 139.79, provider_place_id: "asakusa", locked: false, fixed_time: false, is_estimated: false, start_time: "2026-11-11T00:00:00Z", duration_minutes: 60, data: {} },
    { id: "route-stop-2", item_type: "custom", day_date: "2026-11-11", position: 1, title: "晴空塔", location_name: "押上", latitude: 35.71, longitude: 139.81, provider_place_id: "skytree", locked: false, fixed_time: false, is_estimated: false, start_time: "2026-11-11T01:34:00Z", duration_minutes: 60, data: {} },
  ];
  let currentTrip = {
    id: "routing-trip", name: "東京交通行程", mode: "manual", total_price: 0, currency: "TWD", data: {}, version: 2,
    destination_name: "東京", start_date: "2026-11-11", end_date: "2026-11-11", timezone: "Asia/Tokyo",
    route_preference: "FEWER_TRANSFERS", share_enabled: false, items: routeItems, route_segments: [transitSegment],
    routing: { status: "complete", total: 1, completed: 1, warnings: [], conflicts: [], day_settings: [{ day_date: "2026-11-11", default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: true }] },
  };
  let previewBody: Record<string, unknown> | undefined;
  let applyBody: Record<string, unknown> | undefined;
  await page.route("**/api/travel/runtime/public-config", (route) => route.fulfill({ status: 200, contentType: "application/json", body: "{}" }));
  await page.route("**/api/travel/affiliates/options**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ options: [] }) }));
  await page.route("**/api/travel/trips/routing-trip**", async (route) => {
    const url = route.request().url();
    if (url.endsWith("/routes/preview")) {
      previewBody = route.request().postDataJSON();
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({
        kind: "provider",
        ...carOptions[0],
        options: carOptions,
      }) });
      return;
    }
    if (url.endsWith("/routes/apply")) {
      applyBody = route.request().postDataJSON();
      currentTrip = { ...currentTrip, version: 3, items: [routeItems[0], { ...routeItems[1], start_time: "2026-11-11T01:24:00Z" }], route_segments: [carOptions[1].segment] };
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
      return;
    }
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
  });

  await page.goto("/zh-TW/trips/routing-trip");
  await page.getByRole("button", { name: "查看前往 晴空塔 的路線" }).click();
  const routeDialog = page.getByRole("dialog", { name: "這段路怎麼走" });
  await expect(routeDialog).toBeVisible();
  await routeDialog.getByRole("tab", { name: "汽車" }).click();
  await expect(routeDialog.getByRole("option", { name: /方案 3/ })).toBeVisible();
  await routeDialog.getByRole("option", { name: /方案 2/ }).click();
  await expect(routeDialog.locator(".route-apply-bar strong")).toHaveText("汽車 · 方案 2 · 14 分鐘");
  expect(previewBody).toMatchObject({ version: 2, travel_mode: "drive", buffer_minutes: 10, include_alternatives: true, max_options: 3 });
  expect(currentTrip.version).toBe(2);
  await expect(routeDialog.getByText("晴空塔").first()).toBeVisible();
  await routeDialog.getByRole("button", { name: "套用此路線" }).click();
  await expect(page.getByText("已套用交通方式，後續可調整的開始時間已重新計算。")).toBeVisible();
  expect(applyBody).toMatchObject({ version: 2, source: "provider", preview_id: "route-preview-2" });
  await routeDialog.getByRole("button", { name: "關閉" }).click();
  await expect(page.getByRole("button", { name: "查看前往 晴空塔 的路線" })).toContainText("汽車");
  await page.reload();
  await expect(page.getByRole("button", { name: "查看前往 晴空塔 的路線" })).toContainText("汽車");
});

test("route drawer auto-previews an unapplied Tokyo transit route without layout overflow", async ({ page }) => {
  const routeItems = [
    { id: "tokyo-station", item_type: "custom", day_date: "2026-11-12", position: 0, title: "東京車站", location_name: "東京車站", latitude: 35.6812, longitude: 139.7671, provider_place_id: "tokyo-station", location_source: "confirmed", locked: false, fixed_time: false, is_estimated: false, start_time: "2026-11-12T00:00:00Z", duration_minutes: 60, data: {} },
    { id: "sensoji", item_type: "custom", day_date: "2026-11-12", position: 1, title: "淺草寺", location_name: "淺草寺", latitude: 35.7148, longitude: 139.7967, provider_place_id: "sensoji", location_source: "google_places_auto", locked: false, fixed_time: false, is_estimated: true, start_time: "2026-11-12T01:30:00Z", duration_minutes: 60, data: { needs_place_confirmation: true } },
  ];
  const segment = {
    from_item_id: "tokyo-station", to_item_id: "sensoji", status: "resolved", travel_mode: "transit", is_override: false,
    provider: "google_routes", attribution: "Google Maps", generated_at: "2026-09-01T01:00:00Z", expires_at: "2026-09-01T01:15:00Z",
    schedule_mode: "preview", preference: "FEWER_TRANSFERS", duration_minutes: 22, buffer_minutes: 10,
    distance_meters: 5100, steps: [], details_available: [] as string[], warnings: ["遠期班次預覽"],
  };
  const currentTrip = {
    id: "tokyo-preview-trip", name: "東京交通預覽", mode: "manual", total_price: 0, currency: "TWD", data: {}, version: 4,
    destination_name: "東京", start_date: "2026-11-12", end_date: "2026-11-12", timezone: "Asia/Tokyo",
    route_preference: "FEWER_TRANSFERS", share_enabled: false, items: routeItems, route_segments: [],
    routing: { status: "idle", total: 1, completed: 0, warnings: [], conflicts: [], day_settings: [{ day_date: "2026-11-12", default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: true }] },
  };
  await page.route("**/api/travel/runtime/public-config", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ google_routes_enabled: true, google_places_enabled: true, google_maps_embed_enabled: false, navitime_enabled: false }) }));
  await page.route("**/api/travel/affiliates/options**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ options: [] }) }));
  await page.route("**/api/travel/trips/tokyo-preview-trip**", async (route) => {
    if (route.request().url().endsWith("/routes/preview")) {
      await new Promise((resolve) => setTimeout(resolve, 150));
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ preview_id: "tokyo-preview", expires_at: "2026-09-01T01:15:00Z", segment, schedule_impact: { affected_items: [], conflicts: [] } }) });
      return;
    }
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
  });

  await page.goto("/zh-TW/trips/tokyo-preview-trip");
  await page.getByRole("button", { name: /選擇這段交通方式.*淺草寺/ }).click();
  const dialog = page.getByRole("dialog", { name: "這段路怎麼走" });
  await expect(dialog.getByRole("button", { name: "套用此路線" })).toBeVisible();
  await expect(dialog.getByText("目前已套用")).toHaveCount(0);
  const mapHeight = await dialog.locator(".route-map-frame").evaluate((element) => element.getBoundingClientRect().height);
  expect(mapHeight).toBeGreaterThanOrEqual(220);
  expect(mapHeight).toBeLessThanOrEqual(320);
  const noHorizontalOverflow = await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth);
  expect(noHorizontalOverflow).toBe(true);
});

test("Seoul route drawer uses NAVER drive and keeps transit external-only", async ({ page }) => {
  test.setTimeout(60_000);
  const routeItems = [
    { id: "gyeongbokgung", item_type: "custom", day_date: "2026-11-13", position: 0, title: "景福宮", location_name: "서울특별시 종로구 사직로 161", latitude: 37.5796, longitude: 126.977, provider_place_id: "naver-palace", location_source: "naver_local_auto", location_provider: "naver_local", locked: false, fixed_time: false, is_estimated: true, start_time: "2026-11-13T00:00:00Z", duration_minutes: 60, data: { place_provider: "naver_local", needs_place_confirmation: true } },
    { id: "bukchon", item_type: "custom", day_date: "2026-11-13", position: 1, title: "北村韓屋村", location_name: "서울특별시 종로구 계동길 37", latitude: 37.5826, longitude: 126.985, provider_place_id: "naver-bukchon", location_source: "naver_local_auto", location_provider: "naver_local", locked: false, fixed_time: false, is_estimated: true, start_time: "2026-11-13T01:30:00Z", duration_minutes: 60, data: { place_provider: "naver_local", needs_place_confirmation: true } },
  ];
  const carSegment = {
    from_item_id: "gyeongbokgung", to_item_id: "bukchon", status: "resolved", travel_mode: "drive", is_override: true,
    provider: "naver_maps", attribution: "NAVER Maps", generated_at: "2026-09-01T01:00:00Z", expires_at: "2026-09-01T01:15:00Z",
    schedule_mode: "preview", preference: "FEWER_TRANSFERS", duration_minutes: 12, buffer_minutes: 10,
    departure_time: "2026-11-13T01:00:00Z", arrival_time: "2026-11-13T01:12:00Z", ready_time: "2026-11-13T01:22:00Z",
    distance_meters: 4300, encoded_polyline: "_p~iF~ps|U_ulLnnqC_mqNvxq`@", maps_url: "https://map.naver.com/p/directions/126.977,37.5796,%EA%B2%BD%EB%B3%B5%EA%B6%81/126.985,37.5826,%EB%B6%81%EC%B4%8C/-/car",
    steps: [{ travel_mode: "DRIVE", instruction: "사직로 방면으로 우회전", duration_minutes: 3, distance_meters: 900 }], details_available: ["steps", "traffic"], warnings: ["NAVER 汽車路線依目前路況估算，不代表行程日期的即時路況。"],
  };
  let currentTrip = {
    id: "seoul-route-trip", name: "首爾 NAVER 行程", mode: "manual", total_price: 0, currency: "TWD", data: { destination_country_code: "KR" }, version: 5,
    destination_name: "韓國首爾", destination_country_code: "KR", start_date: "2026-11-13", end_date: "2026-11-13", timezone: "Asia/Seoul",
    route_preference: "FEWER_TRANSFERS", share_enabled: false, items: routeItems, route_segments: [] as typeof carSegment[],
    routing: { status: "idle", total: 1, completed: 0, warnings: [], conflicts: [], day_settings: [{ day_date: "2026-11-13", default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: true }] },
  };
  let applyBody: Record<string, unknown> | undefined;
  await page.route("**/api/travel/runtime/public-config", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ google_routes_enabled: true, naver_directions_enabled: true, naver_dynamic_map_enabled: false }) }));
  await page.route("**/api/travel/affiliates/options**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ options: [] }) }));
  await page.route("**/api/travel/trips/seoul-route-trip**", async (route) => {
    const url = route.request().url();
    if (url.endsWith("/routes/preview")) {
      const body = route.request().postDataJSON();
      if (body.travel_mode === "transit") {
        await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ kind: "external_only", preview_id: null, expires_at: null, segment: null, schedule_impact: null, external_navigation: { provider: "naver_maps", label: "NAVER Maps", travel_mode: "transit", app_url: "nmap://route/public?slat=37.5796&slng=126.977&dlat=37.5826&dlng=126.985", web_url: "https://map.naver.com/p/directions/126.977,37.5796,%EA%B2%BD%EB%B3%B5%EA%B6%81/126.985,37.5826,%EB%B6%81%EC%B4%8C/-/transit", reason: "NAVER 官方 Directions API 不提供可保存的大眾運輸班次；請到 NAVER Maps 查看。" } }) });
      } else {
        await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ kind: "provider", preview_id: "naver-drive-preview", expires_at: "2026-09-01T01:15:00Z", segment: carSegment, schedule_impact: { affected_items: [{ item_id: "bukchon", title: "北村韓屋村", old_start_time: "2026-11-13T01:30:00Z", new_start_time: "2026-11-13T01:22:00Z", delta_minutes: -8 }], conflicts: [] } }) });
      }
      return;
    }
    if (url.endsWith("/routes/apply")) {
      applyBody = route.request().postDataJSON();
      currentTrip = { ...currentTrip, version: 6, items: [routeItems[0], { ...routeItems[1], start_time: "2026-11-13T01:22:00Z" }], route_segments: [carSegment] };
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
      return;
    }
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(currentTrip) });
  });

  await page.goto("/zh-TW/trips/seoul-route-trip");
  await page.getByRole("button", { name: /選擇這段交通方式.*北村韓屋村/ }).click();
  const dialog = page.getByRole("dialog", { name: "這段路怎麼走" });
  await expect(dialog.getByRole("link", { name: /用 NAVER Maps 規劃/ })).toBeVisible();
  await expect(dialog.getByRole("button", { name: "外部導航，無法套用" })).toBeDisabled();
  await dialog.getByRole("tab", { name: "汽車" }).click();
  await expect(dialog.getByRole("button", { name: "套用此路線" })).toBeEnabled();
  await expect(dialog.getByText("NAVER Maps").first()).toBeVisible();
  await dialog.getByRole("button", { name: "套用此路線" }).click();
  await expect.poll(() => applyBody).toMatchObject({ version: 5, source: "provider", preview_id: "naver-drive-preview" });
  await dialog.getByRole("button", { name: "關閉" }).click();
  await expect(page.getByRole("button", { name: /查看前往 北村韓屋村 的路線/ })).toContainText("汽車");
  await page.reload();
  await expect(page.getByRole("button", { name: /查看前往 北村韓屋村 的路線/ })).toContainText("汽車");
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
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
  await page.goto("/zh-TW");
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
  await page.goto("/zh-TW/search?origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=2&children=1&rooms=1&preferred_area=%E6%96%B0%E5%AE%BF&include_airbnb=true");
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
  await page.goto("/zh-TW/alerts");
  await expect(page.getByText("登入後才能查看這裡的內容")).toBeVisible();
  await expect(page.getByRole("link", { name: "前往登入" })).toHaveAttribute("href", "/zh-TW/login?next=%2Falerts");
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
  await page.goto("/zh-TW/search?origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=2&include_airbnb=true");
  const login = page.getByRole("link", { name: "登入後開始搜尋" });
  await expect(login).toBeVisible();
  await expect(login).toHaveAttribute("href", /\/zh-TW\/login\?next=%2Fsearch%3Forigin%3DTPE/);
  await expect(page.getByRole("link", { name: /Airbnb 官方外站搜尋/ })).toBeVisible();
});

test("empty search explains missing fields and links home", async ({ page }) => {
  await page.route("**/api/travel/providers/status", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ provider: "mock", mode: "mock", status: "ready", modules: [], message: "模擬資料已啟用" }),
  }));
  await page.goto("/zh-TW/search");
  await expect(page.getByText(/缺少出發地、目的地或出發日期/)).toBeVisible();
  await expect(page.getByRole("link", { name: "回首頁設定條件" })).toHaveAttribute("href", "/zh-TW");
});

test("failed login keeps email and clears only password", async ({ page }) => {
  await page.route("**/api/travel/auth/login", (route) => route.fulfill({
    status: 401,
    contentType: "application/problem+json",
    body: JSON.stringify({ status: 401, code: "invalid_credentials", detail: "Email 或密碼不正確" }),
  }));
  await page.goto("/zh-TW/login?next=%2Falerts");
  await page.getByLabel("Email").fill("traveler@example.com");
  await page.getByLabel("密碼").fill("wrong-password");
  await page.getByRole("button", { name: "登入" }).click();
  await expect(page.getByText("Email 或密碼不正確", { exact: true })).toBeVisible();
  await expect(page.getByLabel("Email")).toHaveValue("traveler@example.com");
  await expect(page.getByLabel("密碼")).toHaveValue("");
});

test("mobile bottom navigation exposes trips alerts and account links", async ({ page }) => {
  await page.setViewportSize({ width: 412, height: 915 });
  await page.goto("/zh-TW");
  const navigation = page.getByRole("navigation", { name: "手機主要導覽" });
  await expect(navigation).toBeVisible();
  await expect(navigation.getByRole("link", { name: "旅程" })).toHaveAttribute("href", "/zh-TW/trips");
  await expect(navigation.getByRole("link", { name: "通知" })).toHaveAttribute("href", "/zh-TW/alerts");
  await expect(navigation.getByRole("link", { name: "我的" })).toHaveAttribute("href", "/zh-TW/account");
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
  await page.goto("/zh-TW/search?origin=TPE&destination=HKT&departure_date=2026-11-10&return_date=2026-11-15&adults=2&children=0&rooms=1&budget_twd=60000&interests=food&preferred_area=%E6%99%AE%E5%90%89%E8%80%81%E5%9F%8E&pace=balanced");
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

  await page.goto("/zh-TW/search?origin=TPE&destination=NRT&departure_date=2026-11-10&return_date=2026-11-15&adults=1&rooms=1&flex_days=7");
  await page.getByRole("button", { name: /^確認條件並開始搜尋 · 消耗 1 次$/ }).click();
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
  await page.getByRole("button", { name: /^套用並重新搜尋整趟 · 消耗 1 次$/ }).click();
  await expect.poll(() => submitted.length).toBe(2);
  expect(submitted[1]).toMatchObject({ departure_date: "2026-11-12", return_date: "2026-11-17", flex_days: 0, flexible_dates: false });
  await expect(page).toHaveURL(/departure_date=2026-11-12/);
});

test("airline public fare lab is available", async ({ page }) => {
  await page.goto("/zh-TW/labs/airlines");
  await expect(page.getByRole("heading", { name: /三家航空/ })).toBeVisible();
  await expect(page.getByRole("button", { name: /^搜尋公開票價 · 消耗 1 次$/ })).toBeVisible();
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

  await page.goto("/zh-TW/labs/airlines");
  await expect(page.getByText("政策停用")).toBeVisible();
  const backToBackTab = page.getByRole("tab", { name: "倒買法" });
  await backToBackTab.click();
  await expect(backToBackTab).toHaveAttribute("aria-selected", "true");
  await expect(page.getByRole("heading", { name: "設定兩趟旅行" })).toBeVisible({ timeout: 15_000 });
  await page.getByRole("button", { name: /^比較倒買價格 · 消耗 1 次$/ }).click();
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

  await page.goto("/zh-TW/labs/airlines");
  await page.getByRole("tab", { name: "倒買法" }).click();
  await page.getByLabel("第二次目的地").selectOption("SEL");
  await page.getByLabel("頭段單程每人價格").fill("3000");
  await page.getByLabel("中段反向兩航段每人價格").fill("9000");
  await page.getByLabel("尾段單程每人價格").fill("4000");
  await page.getByLabel("第一次一般來回每人價格").fill("12000");
  await page.getByLabel("第二次一般來回每人價格").fill("10000");
  await page.getByRole("button", { name: /^比較倒買價格 · 消耗 1 次$/ }).click();

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

  await page.goto("/zh-TW/labs/airlines");
  await page.getByRole("tab", { name: "即時倒買 API" }).click();
  await expect(page.getByRole("heading", { name: "即時倒買價格比較" })).toBeVisible();
  await page.getByLabel("成人").selectOption("2");
  await page.getByRole("button", { name: /^開始即時比較 · 消耗 1 次$/ }).click();

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
