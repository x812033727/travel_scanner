import { expect, test } from "@playwright/test";

const targetSha = "b".repeat(40);
const overview = {
  enabled: true,
  agent_connected: true,
  deployed_sha: "a".repeat(40),
  target_sha: targetSha,
  target_commit_subject: "Add deployment center",
  update_available: true,
  ci_status: "success",
  ci_url: "https://github.com/x812033727/travel_scanner/actions/runs/1",
  commits: [{ sha: targetSha, subject: "Add deployment center" }],
  checks: [
    { name: "docker", status: "ok", detail: "可用" },
    { name: "api", status: "ok", detail: "API ready" },
    { name: "web", status: "ok", detail: "Web ready" },
  ],
};

test.beforeEach(async ({ page }) => {
  let activeRun: Record<string, unknown> | undefined;
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ id: "admin", email: "deploy@example.com", is_admin: true, can_deploy: true }),
  }));
  await page.route("**/api/travel/admin/deployments/overview", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ...overview, active_run: activeRun }) }));
  await page.route("**/api/travel/admin/deployments?**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [] }) }));
  await page.route("**/api/travel/admin/deployments/preflight", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true, checked_at: "2026-09-01T12:00:00Z", target_sha: targetSha, checks: overview.checks }) }));
  await page.route("**/api/travel/admin/deployments", async (route) => {
    if (route.request().method() !== "POST") return route.fallback();
    const payload = route.request().postDataJSON();
    expect(payload).toEqual({ expected_target_sha: targetSha, password: "correct password", confirmation: "DEPLOY bbbbbbb" });
    expect(route.request().headers()["idempotency-key"]).toMatch(/^deploy-/);
    activeRun = { id: "run-1", requested_by_email: "deploy@example.com", status: "preflight", stage: "preflight", target_sha: targetSha, created_at: "2026-09-01T12:00:00Z", updated_at: "2026-09-01T12:00:00Z", events: [{ sequence: 1, stage: "preflight", status: "running", message: "正在重新驗證 main 與 CI", created_at: "2026-09-01T12:00:01Z" }] };
    return route.fulfill({ status: 202, contentType: "application/json", body: JSON.stringify(activeRun) });
  });
});

test("deployment admin confirms and starts the pinned green release", async ({ page }) => {
  await page.goto("/zh-TW/admin/deployments");
  await expect(page.getByRole("heading", { name: "部署中心" })).toBeVisible();
  await expect(page.getByRole("link", { name: "部署中心" })).toHaveAttribute("aria-current", "page");
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(await page.evaluate(() => document.documentElement.clientWidth));
  await page.getByRole("button", { name: "重新檢查環境" }).click();
  await expect(page.getByText("API ready")).toBeVisible();
  await page.getByRole("button", { name: "部署最新版本" }).click();
  const dialog = page.getByRole("dialog", { name: "確認部署 bbbbbbb" });
  await expect(dialog).toBeVisible();
  await expect(page.getByLabel("目前密碼")).toBeFocused();
  await page.getByLabel("目前密碼").fill("correct password");
  await page.getByLabel(/輸入 DEPLOY/).fill("DEPLOY bbbbbbb");
  await page.getByRole("button", { name: "確認並開始部署" }).click();
  await expect(page.getByRole("heading", { name: "正在部署 bbbbbbb" })).toBeVisible();
  await expect(page.getByText("正在重新驗證 main 與 CI")).toBeVisible();
});
