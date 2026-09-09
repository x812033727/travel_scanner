import { expect, test, type Page } from "@playwright/test";

const OWNER_NAVIGATION = [
  "/admin", "/admin/hotspots", "/admin/foods", "/admin/hotels", "/admin/travel-services",
  "/admin/catalog-review", "/admin/community", "/admin/pet-friendly", "/admin/users",
  "/admin/analytics", "/admin/partners", "/admin/settings", "/admin/usage-settings",
  "/admin/layout-settings", "/admin/ui-text", "/admin/system-settings", "/admin/database",
  "/admin/deployments", "/admin/audit",
];

const ownerPassword = "isolated-admin-workspace-password-123";
const ROLE_NAVIGATION: Record<string, string[]> = {
  viewer: OWNER_NAVIGATION.filter((href) => !["/admin/database", "/admin/deployments"].includes(href)),
  support: ["/admin", "/admin/community", "/admin/pet-friendly", "/admin/users", "/admin/audit"],
  content: [
    "/admin", "/admin/hotspots", "/admin/foods", "/admin/hotels", "/admin/travel-services",
    "/admin/catalog-review", "/admin/community", "/admin/pet-friendly", "/admin/partners", "/admin/audit",
  ],
  operations: [
    "/admin", "/admin/analytics", "/admin/settings", "/admin/usage-settings",
    "/admin/layout-settings", "/admin/ui-text", "/admin/system-settings", "/admin/audit",
  ],
  database_operator: ["/admin", "/admin/database", "/admin/audit"],
  deployer: ["/admin", "/admin/deployments", "/admin/audit"],
};

function requireIsolatedStack(baseURL: string | undefined) {
  test.skip(process.env.ADMIN_OPERATIONS_E2E !== "1", "Requires the isolated PostgreSQL/Redis/RQ stack.");
  expect(baseURL).toBeTruthy();
  expect(["localhost", "127.0.0.1"]).toContain(new URL(baseURL!).hostname);
}

async function login(page: Page, email: string, password: string, next = "/admin") {
  await page.goto(`/zh-TW/login?next=${encodeURIComponent(next)}`);
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("密碼", { exact: true }).fill(password);
  await page.getByRole("button", { name: "登入", exact: true }).click();
  await expect(page).toHaveURL((url) => url.pathname === `/zh-TW${next}`, { timeout: 15_000 });
}

async function bootstrap(page: Page) {
  return page.evaluate(async () => {
    const response = await fetch("/api/travel/admin/bootstrap", { headers: { Accept: "application/json" } });
    return { status: response.status, body: await response.json() };
  });
}

async function adminMutation(
  page: Page,
  path: string,
  method: "POST" | "PATCH" | "DELETE",
  body: Record<string, unknown>,
  idempotencyKey?: string,
) {
  return page.evaluate(async ({ path, method, body, idempotencyKey }) => {
    const response = await fetch(`/api/travel${path}`, {
      method,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...(idempotencyKey ? { "Idempotency-Key": idempotencyKey } : {}),
      },
      body: JSON.stringify(body),
    });
    return { status: response.status, body: await response.json() };
  }, { path, method, body, idempotencyKey });
}

test("real owner bootstrap registry loads every admin page without console or first-party errors", async ({ page, baseURL }, info) => {
  requireIsolatedStack(baseURL);
  test.skip(info.project.name !== "desktop-chromium", "The full registry runs once against the real stack.");
  test.setTimeout(180_000);
  const consoleErrors: string[] = [];
  const pageErrors: string[] = [];
  const failedResponses: string[] = [];

  await login(page, "admin-workspace-desktop@example.com", ownerPassword);
  page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("response", (response) => {
    const url = new URL(response.url());
    if ((response.request().resourceType() === "document" || url.pathname.startsWith("/api/travel/")) && response.status() >= 400) {
      failedResponses.push(`${response.status()} ${url.pathname}${url.search}`);
    }
  });
  const result = await bootstrap(page);
  expect(result.status).toBe(200);
  expect(result.body.actor.roles).toContain("owner");
  expect(result.body.navigation.map((item: { href: string }) => item.href)).toEqual(OWNER_NAVIGATION);

  for (const path of OWNER_NAVIGATION) {
    const response = await page.goto(`/zh-TW${path}`);
    expect(response?.status(), path).toBe(200);
    await expect(page.locator("h1").first(), path).toBeVisible();
    await expect(page.getByRole("navigation", { name: "營運控制台" }), path).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, `${path} must not overflow the desktop viewport`).toBeLessThanOrEqual(0);
  }

  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(failedResponses).toEqual([]);
});

test("real owner can grant viewer and the new role is denied a database deep link", async ({ page, request, baseURL }, info) => {
  requireIsolatedStack(baseURL);
  test.skip(info.project.name !== "desktop-chromium", "Role mutation runs once against disposable CI data.");
  test.setTimeout(90_000);
  const suffix = `${Date.now()}-${info.workerIndex}`;
  const email = `admin-ops-viewer-${suffix}@example.test`;
  const password = "admin-ops-fixture-123";
  const registration = await request.post("http://127.0.0.1:8000/api/v1/auth/register", {
    data: { email, password, preferred_locale: "zh-TW" },
  });
  expect(registration.status()).toBe(201);
  const registered = await registration.json();
  const userId = registered.user.id as string;

  await login(page, "admin-workspace-desktop@example.com", ownerPassword);
  await page.goto(`/zh-TW/admin/users?query=${encodeURIComponent(email)}`);
  await expect(page.getByText(email, { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "管理", exact: true }).click();
  const drawer = page.getByRole("dialog", { name: email });
  await drawer.getByRole("checkbox", { name: "唯讀", exact: true }).check();
  await drawer.getByLabel("角色變更原因").fill("full-stack role boundary acceptance");
  await drawer.getByRole("button", { name: "更新角色" }).click();
  const confirmation = page.getByRole("dialog", { name: "確認角色變更" });
  await confirmation.getByLabel("目前密碼").fill(ownerPassword);
  await confirmation.getByLabel("輸入確認文字").fill(`ROLES ${email}`);
  const saved = page.waitForResponse((response) => response.url().endsWith(`/admin/users/${userId}/roles`) && response.request().method() === "PATCH");
  await confirmation.getByRole("button", { name: "更新角色" }).click();
  expect((await saved).status()).toBe(200);

  await page.context().clearCookies();
  await login(page, email, password);
  const viewer = await bootstrap(page);
  expect(viewer.status).toBe(200);
  expect(viewer.body.actor.roles).toEqual(["viewer"]);
  expect(viewer.body.navigation.map((item: { href: string }) => item.href)).not.toContain("/admin/database");
  await page.goto("/zh-TW/admin/database");
  await expect(page.getByRole("heading", { name: "你沒有這個後台的權限" })).toBeVisible();
  await expect(page.getByText("PostgreSQL", { exact: false })).toHaveCount(0);
});

test("real support lifecycle mutations revoke sessions and preserve cancellable erasure", async ({ page, request, baseURL }, info) => {
  requireIsolatedStack(baseURL);
  test.skip(info.project.name !== "desktop-chromium", "Disposable account lifecycle runs once.");
  test.setTimeout(90_000);
  const suffix = `${Date.now()}-${info.workerIndex}`;
  const email = `admin-ops-lifecycle-${suffix}@example.test`;
  const password = "admin-ops-fixture-123";
  const registration = await request.post("http://127.0.0.1:8000/api/v1/auth/register", {
    data: { email, password, preferred_locale: "zh-TW" },
  });
  expect(registration.status()).toBe(201);
  const registered = await registration.json();
  const userId = registered.user.id as string;
  const memberToken = registered.access_token as string;

  await login(page, "admin-workspace-desktop@example.com", ownerPassword);

  const revoked = await adminMutation(
    page,
    `/admin/users/${userId}/sessions/revoke`,
    "POST",
    { reason: "full-stack session revocation" },
  );
  expect(revoked.status).toBe(200);
  const staleSession = await request.get("http://127.0.0.1:8000/api/v1/auth/me", {
    headers: { Authorization: `Bearer ${memberToken}` },
  });
  expect(staleSession.status()).toBe(401);

  const suspendedUntil = new Date(Date.now() + 60 * 60 * 1000).toISOString();
  const suspended = await adminMutation(
    page,
    `/admin/users/${userId}/suspension`,
    "POST",
    { reason: "full-stack timed support hold", suspended_until: suspendedUntil },
    `suspend-${suffix}`,
  );
  expect(suspended.status).toBe(200);
  expect(suspended.body.user.status).toBe("suspended");
  const blockedLogin = await request.post("http://127.0.0.1:8000/api/v1/auth/login", {
    data: { email, password },
  });
  expect(blockedLogin.status()).toBe(403);

  const restored = await adminMutation(
    page,
    `/admin/users/${userId}/suspension`,
    "DELETE",
    { reason: "full-stack support hold cleared" },
  );
  expect(restored.status).toBe(200);
  expect(restored.body.status).toBe("active");

  const verification = await adminMutation(
    page,
    `/admin/users/${userId}/verification`,
    "POST",
    {},
  );
  expect(verification.status).toBe(202);

  const elevated = await adminMutation(
    page,
    "/admin/step-up",
    "POST",
    { password: ownerPassword, scopes: ["users.erase"] },
  );
  expect(elevated.status).toBe(200);
  const scheduled = await adminMutation(
    page,
    `/admin/users/${userId}/erasure`,
    "POST",
    { reason: "full-stack cancellable privacy request", confirmation: `ERASE ${email}` },
    `erase-${suffix}`,
  );
  expect(scheduled.status).toBe(202);
  expect(scheduled.body.user.erasure.status).toBe("scheduled");
  const cancelled = await adminMutation(
    page,
    `/admin/users/${userId}/erasure`,
    "DELETE",
    { reason: "full-stack cancellation acceptance" },
  );
  expect(cancelled.status).toBe(200);
  expect(cancelled.body.erasure.status).toBe("cancelled");
});

test("real bootstrap and direct URLs enforce every fixed role boundary", async ({ page, request, baseURL }, info) => {
  requireIsolatedStack(baseURL);
  test.skip(info.project.name !== "desktop-chromium", "The six-role matrix runs once.");
  test.setTimeout(180_000);
  const suffix = `${Date.now()}-${info.workerIndex}`;
  const password = "admin-ops-role-fixture-123";
  const accounts: Array<{ role: string; email: string; id: string }> = [];
  for (const role of Object.keys(ROLE_NAVIGATION)) {
    const email = `admin-ops-${role.replace("_", "-")}-${suffix}@example.test`;
    const registration = await request.post("http://127.0.0.1:8000/api/v1/auth/register", {
      data: { email, password, preferred_locale: "zh-TW" },
    });
    expect(registration.status(), role).toBe(201);
    accounts.push({ role, email, id: (await registration.json()).user.id as string });
  }

  await login(page, "admin-workspace-desktop@example.com", ownerPassword);
  const elevated = await adminMutation(
    page,
    "/admin/step-up",
    "POST",
    { password: ownerPassword, scopes: ["users.roles"] },
  );
  expect(elevated.status).toBe(200);
  for (const account of accounts) {
    const assigned = await adminMutation(
      page,
      `/admin/users/${account.id}/roles`,
      "PATCH",
      {
        roles: [account.role],
        reason: `full-stack ${account.role} boundary`,
        confirmation: `ROLES ${account.email}`,
      },
      `role-${account.role}-${suffix}`,
    );
    expect(assigned.status, account.role).toBe(200);
  }

  for (const account of accounts) {
    await page.context().clearCookies();
    await login(page, account.email, password);
    const roleBootstrap = await bootstrap(page);
    expect(roleBootstrap.status, account.role).toBe(200);
    expect(roleBootstrap.body.actor.roles, account.role).toEqual([account.role]);
    expect(roleBootstrap.body.navigation.map((item: { href: string }) => item.href), account.role)
      .toEqual(ROLE_NAVIGATION[account.role]);
    const forbidden = account.role === "database_operator" ? "/admin/users" : "/admin/database";
    await page.goto(`/zh-TW${forbidden}`);
    await expect(page.getByRole("heading", { name: "你沒有這個後台的權限" }), account.role)
      .toBeVisible();
    await expect(page.getByRole("navigation", { name: "營運控制台" }), account.role)
      .toHaveCount(0);
  }
});

test("real signed agent verifies backup and controlled analyze operations", async ({ page, baseURL }, info) => {
  requireIsolatedStack(baseURL);
  test.skip(info.project.name !== "desktop-chromium", "Signed fixture mutations run once.");
  test.setTimeout(90_000);
  const suffix = `${Date.now()}-${info.workerIndex}`;
  await login(page, "admin-workspace-desktop@example.com", ownerPassword, "/admin/database");
  const elevated = await adminMutation(
    page,
    "/admin/step-up",
    "POST",
    {
      password: ownerPassword,
      scopes: ["database.backup", "database.analyze"],
    },
  );
  expect(elevated.status).toBe(200);

  const backup = await adminMutation(
    page,
    "/admin/database/backups",
    "POST",
    { confirmation: "BACKUP" },
    `backup-${suffix}`,
  );
  expect(backup.status).toBe(202);
  expect(backup.body.operation_type).toBe("backup");
  expect(backup.body.status).toBe("succeeded");
  expect(backup.body.verified).toBe(true);
  expect(backup.body.checksum_sha256).toMatch(/^[0-9a-f]{64}$/);

  const analyze = await adminMutation(
    page,
    "/admin/database/maintenance",
    "POST",
    { action: "analyze", confirmation: "ANALYZE" },
    `analyze-${suffix}`,
  );
  expect(analyze.status).toBe(202);
  expect(analyze.body.operation_type).toBe("analyze");
  expect(analyze.body.status).toBe("succeeded");
  expect(analyze.body.verified).toBe(false);

  const state = await page.evaluate(async () => {
    const [overviewResponse, backupsResponse] = await Promise.all([
      fetch("/api/travel/admin/database/overview", { headers: { Accept: "application/json" } }),
      fetch("/api/travel/admin/database/backups", { headers: { Accept: "application/json" } }),
    ]);
    return {
      overviewStatus: overviewResponse.status,
      overview: await overviewResponse.json(),
      backupsStatus: backupsResponse.status,
      backups: await backupsResponse.json(),
    };
  });
  expect(state.overviewStatus).toBe(200);
  expect(state.backupsStatus).toBe(200);
  expect(state.overview.agent.connected).toBe(true);
  expect(state.overview.last_backup.verified).toBe(true);
  expect(state.backups.items[0].source).toBe("manual");
  expect(state.backups.items[0].verified).toBe(true);
});

test("real Pixel 7 admin shell opens the new system pages without horizontal overflow", async ({ page, baseURL }, info) => {
  requireIsolatedStack(baseURL);
  test.skip(info.project.name !== "mobile-chromium", "Pixel 7-only acceptance.");
  test.setTimeout(60_000);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await login(page, "admin-workspace-mobile@example.com", ownerPassword, "/admin/database");
  await expect(page.getByRole("heading", { name: "資料庫維運" })).toBeVisible();
  await page.getByRole("button", { name: "開啟營運選單" }).click();
  const navigation = page.getByRole("navigation", { name: "營運控制台" });
  await navigation.getByRole("link", { name: "稽核紀錄" }).click();
  await expect(page.getByRole("heading", { name: "稽核紀錄" })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)).toBeLessThanOrEqual(0);
  expect(await page.evaluate(() => document.body.scrollWidth - document.body.clientWidth)).toBeLessThanOrEqual(0);
});
