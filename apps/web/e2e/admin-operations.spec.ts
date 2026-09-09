import { expect, test, type Page, type Route } from "@playwright/test";

const ADMIN_PAGES = [
  "/admin",
  "/admin/hotspots",
  "/admin/foods",
  "/admin/hotels",
  "/admin/travel-services",
  "/admin/catalog-review",
  "/admin/community",
  "/admin/pet-friendly",
  "/admin/users",
  "/admin/analytics",
  "/admin/partners",
  "/admin/settings",
  "/admin/usage-settings",
  "/admin/layout-settings",
  "/admin/ui-text",
  "/admin/system-settings",
  "/admin/database",
  "/admin/deployments",
  "/admin/audit",
] as const;

const ROLE_NAVIGATION = {
  viewer: ADMIN_PAGES.filter((path) => !["/admin/database", "/admin/deployments"].includes(path)),
  support: ["/admin", "/admin/community", "/admin/pet-friendly", "/admin/users", "/admin/audit"],
  content: ["/admin", "/admin/hotspots", "/admin/foods", "/admin/hotels", "/admin/travel-services", "/admin/catalog-review", "/admin/community", "/admin/pet-friendly", "/admin/partners", "/admin/audit"],
  operations: ["/admin", "/admin/analytics", "/admin/settings", "/admin/usage-settings", "/admin/layout-settings", "/admin/ui-text", "/admin/system-settings", "/admin/audit"],
  database_operator: ["/admin", "/admin/database", "/admin/audit"],
  deployer: ["/admin", "/admin/deployments", "/admin/audit"],
  owner: [...ADMIN_PAGES],
} as const;

const now = "2026-09-09T00:00:00Z";
const memberId = "00000000-0000-4000-8000-000000000010";

const user = {
  id: memberId,
  email: "traveler@example.test",
  is_active: true,
  is_admin: false,
  effective_is_admin: false,
  admin_source: "none",
  is_self: false,
  can_adjust_usage: true,
  remaining_uses: 20,
  reserved_uses: 0,
  available_uses: 20,
  created_at: now,
  updated_at: now,
  status: "active",
  admin_roles: [],
  auth_methods: ["password"],
  email_verified: false,
  last_login_at: now,
  erasure_status: "none",
};

const userDetail = {
  ...user,
  activity: { trips: 2, searches: 4, alerts: 1, community_posts: 0, community_comments: 0 },
  auth_identities: [],
  erasure: null,
  usage_history: [],
  admin_history: [],
};

const operationCosts = [
  "travel_search", "flexible_flight_search", "flight_hotel_search", "full_trip_search",
  "multi_city_search", "public_airline_fare_search", "back_to_back_fare_search",
  "live_back_to_back_fare_search", "flight_status_lookup", "ai_itinerary_generation",
  "ai_itinerary_refine", "itinerary_optimization", "price_reoptimization",
].map((operation) => ({ operation, uses: 1, source: "default" }));

function pageResult() {
  return { items: [], total: 0, page: 1, limit: 20, pages: 1 };
}

function travelServices() {
  return {
    products: [], offers: [], destination_offers: [], destinations: [], brands: [],
    brand_definitions: {}, coverage: [], review_due: 0, imports: [], operations: {},
    network_configured: false, project_id: null,
    config: {
      public_enabled: false, enabled_kinds: [], enabled_destinations: [],
      direct_hotel_links_enabled: false, hotel_quote_policies: {},
    },
    version: 0,
    summary: { total: 0, pending: 0, approved: 0, disabled: 0 },
  };
}

type RecordedWrite = { method: string; path: string; body: unknown };

async function isolateAdmin(page: Page, role = "owner") {
  await page.context().addCookies([{
    name: "travel_access",
    value: role === "owner" ? "e2e-session" : `e2e-${role}`,
    domain: "127.0.0.1",
    path: "/",
  }]);
  const writes: RecordedWrite[] = [];
  const unexpectedExternal: string[] = [];
  const failedFirstParty: string[] = [];
  let databaseOperation: Record<string, unknown> | null = null;

  page.on("request", (request) => {
    const url = new URL(request.url());
    if (!["127.0.0.1", "localhost"].includes(url.hostname) && !["data:", "blob:"].includes(url.protocol)) {
      unexpectedExternal.push(request.url());
    }
  });
  page.on("response", (response) => {
    const url = new URL(response.url());
    if (["127.0.0.1", "localhost"].includes(url.hostname)
      && (response.request().resourceType() === "document" || url.pathname.startsWith("/api/travel/"))
      && response.status() >= 400) {
      failedFirstParty.push(`${response.status()} ${url.pathname}${url.search}`);
    }
  });

  await page.route("**/api/travel/**", async (route: Route) => {
    const request = route.request();
    const url = new URL(request.url());
    const path = url.pathname.replace("/api/travel", "");
    const method = request.method();
    const body = request.postData() ? request.postDataJSON() : undefined;

    if (method !== "GET") {
      writes.push({ method, path, body });
      if (path === "/admin/step-up" && method === "POST") {
        await route.fulfill({ status: 200, json: { expires_at: "2026-09-09T00:05:00Z", scopes: body?.scopes ?? [] } });
        return;
      }
      if (path === "/admin/database/backups" && method === "POST") {
        databaseOperation = {
          id: "00000000-0000-4000-8000-000000000099", operation_type: "backup",
          status: "queued", requested_by_email: "owner@example.test", created_at: now, updated_at: now,
        };
        await route.fulfill({ status: 202, json: databaseOperation });
        return;
      }
      if (path === `/admin/users/${memberId}/sessions/revoke` && method === "POST") {
        await route.fulfill({ status: 200, json: { ...userDetail, updated_at: "2026-09-09T00:01:00Z" } });
        return;
      }
      await route.fulfill({ status: 409, json: { code: "fixture_write_blocked", detail: `Unexpected isolated write: ${method} ${path}` } });
      return;
    }

    let response: unknown;
    if (path === "/auth/me") {
      response = { id: "00000000-0000-4000-8000-000000000001", email: `${role}@example.test`, is_admin: true };
    } else if (path === "/analytics/config") {
      response = { first_party_enabled: false, ga4_enabled: false };
    } else if (path === "/admin/dashboard") {
      response = { counts: { users_total: 3, hotspots_total: 10, hotspots_pending: 2, foods_total: 4, foods_pending: 1, hotels_total: 3, hotels_pending: 1 }, can_deploy: role === "deployer" };
    } else if (path === "/admin/users") {
      response = { items: [user], page: 1, limit: 20, total: 1, pages: 1, stats: { total: 1, active: 1, administrators: 0, available_uses: 20, suspended: 0, erasure_pending: 0 } };
    } else if (path === `/admin/users/${memberId}`) {
      response = userDetail;
    } else if (path === "/admin/audit") {
      response = { items: [{ id: "00000000-0000-4000-8000-000000000020", actor_user_id: null, actor_email: "owner@example.test", action: "user.sessions_revoked", target: `user:${memberId}`, result: "succeeded", metadata: { reason: "fixture review" }, created_at: now }], total: 1, page: 1, limit: 20, pages: 1 };
    } else if (path === "/admin/database/overview") {
      response = {
        status: "ok",
        checked_at: now,
        postgres: { version: "PostgreSQL 17", database_size_bytes: 1048576, connections: { active: 1, idle: 2, waiting: 0, maximum: 100 }, long_transactions: 0, lock_waits: 0, cache_hit_ratio: 0.99 },
        schema_info: { current_revision: "0068_admin_operations_center", expected_revision: "0068_admin_operations_center", is_current: true },
        agent: { connected: true, available: true, release_sha: "fixture-release", checks: [], active_job: null },
        active_operation: databaseOperation,
        last_backup: null,
        maintenance_enabled: true,
        retention_count: 7,
      };
    } else if (path === "/admin/database/tables") {
      response = { items: [{ name: "users", estimated_rows: 3, data_bytes: 16384, index_bytes: 8192, total_bytes: 24576, dead_rows: 0, last_analyze: now }] };
    } else if (path === "/admin/database/backups") {
      response = { items: databaseOperation ? [databaseOperation] : [] };
    } else if (path === "/admin/deployments/overview") {
      response = { enabled: false, agent_connected: false, deployed_sha: "6eacb821", target_sha: "6eacb821", update_available: false, ci_status: "success", commits: [], checks: [], active_run: null, last_success: null };
    } else if (path === "/admin/deployments") {
      response = { items: [] };
    } else if (path === "/admin/analytics/dashboard") {
      response = { range: "30d", timezone: "Asia/Taipei", source: "raw", summary: { previous: {}, changes: {} }, timeseries: [], funnel: [], top_pages: [], referrers: [], utm_sources: [], devices: [], locales: [], countries: [], heatmap: [], authoritative: {}, data_quality: { ga4_enabled: false, ga4_configured: false, tracking_started_at: null, last_event_at: null, last_rollup_day: null, country_coverage_percent: 0, bots_excluded: true, raw_retention_days: 90, rollup_retention_months: 24 } };
    } else if (path === "/admin/provider-settings") {
      response = { providers: [], audit: [], encryption_source: "fixture" };
    } else if (path === "/admin/usage-settings") {
      response = { trial_uses: 3, packages: [], operation_costs: operationCosts, audit: [] };
    } else if (path === "/admin/ui-text") {
      response = { locale: url.searchParams.get("locale") || "zh-TW", namespace: url.searchParams.get("namespace"), version: "fixture", entries: [] };
    } else if (path === "/admin/hotels" || path === "/admin/travel-services") {
      response = travelServices();
    } else if (path === "/admin/catalog-review") {
      response = { pending_counts: { hotspot: 0, food: 0, merchant: 0, total: 0 }, runs: [], active_run: null, can_discover: false, settings: { enabled: false, configured: false }, providers: {}, usage: {} };
    } else if (path.startsWith("/runtime/")) {
      response = { locale: "zh-TW", version: "fixture", entries: {} };
    } else {
      response = pageResult();
    }
    await route.fulfill({ status: 200, json: response });
  });

  return { writes, unexpectedExternal, failedFirstParty };
}

function navigationHrefs(page: Page) {
  return page.getByRole("navigation", { name: "營運控制台" }).getByRole("link").evaluateAll((links) =>
    links.map((link) => new URL((link as HTMLAnchorElement).href).pathname.replace(/^\/zh-TW/, "")),
  );
}

test("bootstrap registry drives every owner page without first-party failures", async ({ page }, info) => {
  test.skip(info.project.name !== "desktop-chromium", "The full page matrix runs once; mobile layout has a focused acceptance below.");
  test.setTimeout(180_000);
  const fixture = await isolateAdmin(page);
  const pageErrors: string[] = [];
  page.on("pageerror", (error) => pageErrors.push(error.message));

  await page.goto("/zh-TW/admin");
  await expect(page.getByRole("navigation", { name: "營運控制台" })).toBeVisible();
  expect(await navigationHrefs(page)).toEqual(ADMIN_PAGES);

  for (const path of ADMIN_PAGES) {
    const response = await page.goto(`/zh-TW${path}`);
    expect(response?.status(), path).toBe(200);
    await expect(page.locator("h1").first(), path).toBeVisible();
    await expect(page.getByRole("navigation", { name: "營運控制台" }), path).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, `${path} must not overflow the desktop viewport`).toBeLessThanOrEqual(0);
  }

  expect(pageErrors).toEqual([]);
  expect(fixture.failedFirstParty).toEqual([]);
  expect(fixture.unexpectedExternal).toEqual([]);
  expect(fixture.writes).toEqual([]);
});

test("role bootstrap filters navigation and direct URLs fail closed", async ({ page }, info) => {
  test.skip(info.project.name !== "desktop-chromium", "Role matrix runs once.");
  test.setTimeout(120_000);

  for (const [role, expected] of Object.entries(ROLE_NAVIGATION)) {
    await page.context().clearCookies();
    await page.unrouteAll({ behavior: "wait" });
    const fixture = await isolateAdmin(page, role);
    await page.goto("/zh-TW/admin");
    await expect(page.getByRole("navigation", { name: "營運控制台" })).toBeVisible();
    expect(await navigationHrefs(page), role).toEqual(expected);

    if (role !== "owner") {
      const forbidden = role === "database_operator" ? "/admin/users" : "/admin/database";
      await page.goto(`/zh-TW${forbidden}`);
      await expect(page.getByRole("heading", { name: "你沒有這個後台的權限" })).toBeVisible();
      await expect(page.getByRole("navigation", { name: "營運控制台" })).toHaveCount(0);
    }
    expect(fixture.writes).toEqual([]);
    expect(fixture.unexpectedExternal).toEqual([]);
  }
});

test("URL state, command palette, detail drawers and safe fixture mutations remain usable", async ({ page }) => {
  test.skip(test.info().project.name !== "desktop-chromium", "State and mutation flow runs once; the mobile drawer has a focused acceptance below.");
  test.setTimeout(60_000);
  const fixture = await isolateAdmin(page);
  await page.goto("/zh-TW/admin/users?status=active&auth_method=password");
  await expect(page.getByRole("combobox", { name: /帳號狀態/ })).toHaveValue("active");
  await expect(page.getByRole("combobox", { name: /登入方式/ })).toHaveValue("password");
  await page.getByRole("button", { name: "管理", exact: true }).click();
  await expect(page).toHaveURL(new RegExp(`user=${memberId}`));
  await expect(page.getByRole("dialog", { name: "traveler@example.test" })).toBeVisible();
  await page.reload();
  await expect(page.getByRole("combobox", { name: /帳號狀態/ })).toHaveValue("active");
  const userDrawer = page.getByRole("dialog", { name: "traveler@example.test" });
  await expect(userDrawer).toBeVisible();
  const sessions = userDrawer.getByRole("heading", { name: "登入工作階段" }).locator("..");
  await sessions.getByLabel("操作原因").fill("fixture support review");
  await sessions.getByRole("button", { name: "強制全部裝置登出" }).click();
  await expect(page.getByRole("status")).toContainText("所有既有工作階段已撤銷");

  await page.keyboard.press(process.platform === "darwin" ? "Meta+K" : "Control+K");
  const palette = page.getByRole("dialog", { name: "搜尋頁面與操作" });
  await expect(palette).toBeVisible();
  await palette.getByRole("textbox", { name: "搜尋頁面與操作" }).fill("稽核");
  await palette.getByRole("link", { name: /稽核紀錄/ }).click();
  await expect(page).toHaveURL(/\/admin\/audit/);
  await page.getByLabel("操作者").fill("owner@example.test");
  await page.getByLabel("動作").fill("user.sessions_revoked");
  await page.getByRole("button", { name: "套用篩選" }).click();
  await expect(page).toHaveURL(/actor=owner%40example\.test/);
  await expect(page).toHaveURL(/action=user\.sessions_revoked/);
  await expect(page.getByRole("table", { name: "詳情" }).getByText("成功", { exact: true })).toBeVisible();
  await page.goto("/zh-TW/admin/database");
  await page.goBack();
  await expect(page.getByLabel("操作者")).toHaveValue("owner@example.test");
  await expect(page.getByLabel("動作")).toHaveValue("user.sessions_revoked");
  await page.getByRole("button", { name: "查看詳情" }).click();
  await expect(page).toHaveURL(/event=00000000-0000-4000-8000-000000000020/);
  await expect(page.getByRole("dialog", { name: "稽核事件" })).toBeVisible();

  await page.goto("/zh-TW/admin/database");
  await expect(page.getByText("1 / 100", { exact: true })).toBeVisible();
  await expect(page.getByText("0068_admin_operations_center", { exact: true })).toBeVisible();
  await expect(page.getByText("users", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "建立備份" }).click();
  const confirmation = page.getByRole("dialog", { name: "確認建立資料庫備份" });
  await confirmation.getByLabel("目前密碼").fill("fixture-password-123");
  await confirmation.getByLabel("輸入確認文字").fill("BACKUP");
  await confirmation.getByRole("button", { name: "確認執行" }).click();
  await expect(page.getByText("工作已排入佇列，狀態會自動更新。", { exact: true })).toBeVisible();

  expect(fixture.writes.map(({ method, path }) => `${method} ${path}`)).toEqual([
    `POST /admin/users/${memberId}/sessions/revoke`,
    "POST /admin/step-up",
    "POST /admin/database/backups",
  ]);
  expect(fixture.failedFirstParty).toEqual([]);
  expect(fixture.unexpectedExternal).toEqual([]);
});

test("Pixel 7 shell, drawers and database tables do not overflow horizontally", async ({ page }, info) => {
  test.skip(info.project.name !== "mobile-chromium", "Mobile-only geometry acceptance.");
  test.setTimeout(60_000);
  const fixture = await isolateAdmin(page);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/zh-TW/admin/database");
  await expect(page.getByRole("heading", { name: "資料庫維運" })).toBeVisible();
  await page.getByRole("button", { name: "開啟營運選單" }).click();
  const navigation = page.getByRole("navigation", { name: "營運控制台" });
  await expect(navigation).toBeVisible();
  await navigation.getByRole("link", { name: "使用者" }).click();
  await page.getByRole("button", { name: "管理", exact: true }).click();
  await expect(page.getByRole("dialog", { name: "traveler@example.test" })).toBeVisible();

  const overflow = await page.evaluate(() => ({
    document: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    body: document.body.scrollWidth - document.body.clientWidth,
  }));
  expect(overflow).toEqual({ document: 0, body: 0 });
  const shortTargets = await page.locator("button:visible, a:visible, input:visible, select:visible").evaluateAll((elements) =>
    elements.flatMap((element) => {
      // The local Next.js dev indicator is not application UI and is absent from
      // the production build exercised by CI.
      if (element.getAttribute("aria-label") === "Open Next.js Dev Tools") return [];
      const input = element instanceof HTMLInputElement ? element : null;
      const target = input && ["checkbox", "radio"].includes(input.type)
        ? input.closest("label") ?? input
        : element;
      const box = target.getBoundingClientRect();
      return box.height > 0 && box.height < 44 ? [`${Math.round(box.height)}px ${element.getAttribute("aria-label") || element.textContent?.trim().slice(0, 30)}`] : [];
    }),
  );
  expect(shortTargets, "visible controls must keep a 44px touch target").toEqual([]);
  expect(fixture.failedFirstParty).toEqual([]);
  expect(fixture.unexpectedExternal).toEqual([]);
  expect(fixture.writes).toEqual([]);
});
