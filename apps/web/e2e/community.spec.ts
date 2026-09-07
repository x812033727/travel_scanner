import { expect, request, test, type APIRequestContext, type Page } from "@playwright/test";
import path from "node:path";

// No endpoint interception or test authentication bypass. This suite needs the
// CI/local PostgreSQL, Redis, private MinIO, Mailpit and ordinary RQ worker.
test.skip(process.env.COMMUNITY_E2E !== "1", "Requires the community companion services");

async function json(client: APIRequestContext, method: string, route: string, data?: unknown) {
  const response = await client.fetch(`/api/travel${route}`, { method, data,
    headers: { Origin: `http://127.0.0.1:${process.env.PLAYWRIGHT_PORT || "3000"}` } });
  expect(response.ok(), `${method} ${route}: ${await response.text()}`).toBeTruthy();
  return response.status() === 204 ? null : response.json();
}

async function registerAndVerify(page: Page, handle: string, displayName: string) {
  const email = `${handle}@example.com`;
  await json(page.request, "POST", "/auth/register", { email, password: "community-member-password-123" });
  await page.goto("/zh-TW/community/settings");
  await page.getByLabel("帳號代稱", { exact: false }).fill(handle);
  await page.getByLabel("暱稱", { exact: true }).fill(displayName);
  await page.getByRole("button", { name: "儲存", exact: true }).click();
  await expect(page.getByRole("status").filter({ hasText: "已儲存" })).toBeVisible();
  await page.goto("/zh-TW/account");
  await page.getByRole("button", { name: "寄送驗證信", exact: true }).click();
  let verificationUrl = "";
  await expect.poll(async () => {
    const result = await page.request.get(`http://127.0.0.1:8025/api/v1/search?query=${encodeURIComponent(`to:${email}`)}`);
    const messages = (await result.json()).messages || [];
    if (!messages.length) return false;
    const mail = await page.request.get(`http://127.0.0.1:8025/api/v1/message/${messages[0].ID}`);
    verificationUrl = (await mail.json()).Text.match(/https?:\/\/[^\s]+#token=[A-Za-z0-9_-]+/)?.[0] || "";
    return Boolean(verificationUrl);
  }, { timeout: 45_000, intervals: [500, 1000, 2000] }).toBe(true);
  const url = new URL(verificationUrl);
  await page.goto(url.pathname + url.search + url.hash);
  await page.getByRole("button", { name: "確認", exact: true }).click();
  await expect(page.getByText("已完成帳號操作", { exact: false })).toBeVisible();
  return json(page.request, "GET", "/community/me");
}

test("verified members publish reviewed private images, fork safely and exchange mutual-only messages", async ({ page, browser, baseURL }, info) => {
  test.setTimeout(300_000);
  const admin = await request.newContext({ baseURL, extraHTTPHeaders: { Origin: baseURL! } });
  const readerContext = await browser.newContext({ baseURL, viewport: info.project.use.viewport,
    isMobile: info.project.use.isMobile, deviceScaleFactor: info.project.use.deviceScaleFactor });
  const reader = await readerContext.newPage();
  try {
    await json(admin, "POST", "/auth/login", { email: "ci-community@example.com", password: "community-ci-password-123" });
    const current = await json(admin, "GET", "/admin/community/settings");
    await json(admin, "PUT", "/admin/community/settings", { settings: { ...current.settings, enabled: true,
      posting_enabled: true, comments_enabled: true, messaging_enabled: true, pet_reports_enabled: true }, reason: "Isolated CI acceptance" });
    const suffix = `${Date.now()}${info.workerIndex}`;
    const authorHandle = `author${suffix}`;
    const readerHandle = `reader${suffix}`;
    const author = await registerAndVerify(page, authorHandle, `Author ${suffix}`);
    const recipient = await registerAndVerify(reader, readerHandle, `Reader ${suffix}`);
    const departure = new Date(Date.now() + 30 * 86400_000).toISOString().slice(0, 10);
    const trip = await json(page.request, "POST", "/trips", { source: "blank", planning_mode: "manual_blank",
      name: `Private ${suffix}`, destination_name: "Tokyo", start_date: departure, end_date: departure,
      notes: "PRIVATE NOTE MUST NEVER BE PUBLISHED", timezone: "Asia/Tokyo" });

    await page.goto("/zh-TW/community/new");
    const title = `Community acceptance ${suffix}`;
    await page.getByLabel("標題", { exact: true }).fill(title);
    await page.getByLabel("目的地", { exact: true }).fill("Tokyo");
    await page.getByLabel("旅行心得", { exact: true }).fill("A real test account sharing its test itinerary.");
    await page.getByLabel("圖片說明", { exact: true }).fill("Mokaair test image");
    await page.getByLabel("上傳圖片", { exact: true }).setInputFiles(path.resolve("public/brand/mokaair-monogram.png"));
    const image = page.getByRole("img", { name: "Mokaair test image" });
    await expect(image).toBeVisible({ timeout: 30_000 });
    await expect.poll(() => image.evaluate((element) => (element as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
    await page.getByLabel("選擇私人行程來源").selectOption(trip.id);
    await page.getByLabel("允許其他會員免費套用此行程").check();
    await page.getByRole("button", { name: "預覽", exact: true }).click();
    const preview = page.getByRole("dialog", { name: "預覽" });
    await expect(preview).not.toContainText("PRIVATE NOTE MUST NEVER BE PUBLISHED");
    await preview.getByLabel(/我已確認這份快照可公開/).check();
    await preview.getByRole("button", { name: "關閉", exact: true }).click();
    await page.getByRole("button", { name: "發佈", exact: true }).click();
    await expect(page).toHaveURL(/\/community\/posts\/[\da-f-]+\/edit$/);
    const postId = page.url().match(/posts\/([\da-f-]+)\/edit/)![1];
    const pending = await json(page.request, "GET", `/community/posts/${postId}/draft`);
    expect(pending.pending_revision_id).toBeTruthy();
    expect((await reader.request.get(`/api/travel/community/posts/${postId}`)).status()).toBe(404);
    expect((await reader.request.get(`/api/travel/community/media/${pending.media[0].id}`)).status()).toBe(404);
    await json(admin, "PUT", `/admin/community/posts/${postId}`, { action: "approve", version: pending.version, reason: "Reviewed CI source and private snapshot" });

    await reader.goto(`/zh-TW/community/posts/${postId}`);
    await expect(reader.getByRole("heading", { name: title, exact: true })).toBeVisible();
    await expect(reader.getByRole("img", { name: "Mokaair test image" })).toBeVisible();
    await reader.getByRole("button", { name: /^按讚/ }).click();
    await expect(reader.getByRole("button", { name: /^取消讚/ })).toBeVisible();
    await reader.getByLabel("撰寫留言").fill(`Comment ${suffix}`);
    await reader.getByRole("button", { name: "送出", exact: true }).click();
    await expect(reader.getByText(`Comment ${suffix}`, { exact: true })).toBeVisible();
    await reader.getByRole("button", { name: "免費套用行程", exact: true }).click();
    await reader.getByLabel("我的出發日期").fill(departure);
    await reader.getByRole("button", { name: "建立私人副本", exact: true }).click();
    await expect(reader).toHaveURL(/\/trips\/[\da-f-]+$/, { timeout: 20_000 });
    const copiedId = reader.url().split("/").at(-1)!;
    expect(copiedId).not.toBe(trip.id);
    expect(JSON.stringify(await json(reader.request, "GET", `/trips/${copiedId}`))).not.toContain("PRIVATE NOTE MUST NEVER BE PUBLISHED");

    await reader.goto(`/zh-TW/community/profiles/${authorHandle}`);
    await expect(reader.getByRole("button", { name: "私訊", exact: true })).toBeDisabled();
    await reader.getByRole("button", { name: "追蹤", exact: true }).click();
    await page.goto(`/zh-TW/community/profiles/${readerHandle}`);
    await page.getByRole("button", { name: "追蹤", exact: true }).click();
    await expect(page.getByRole("button", { name: "私訊", exact: true })).toBeEnabled();
    await page.getByRole("button", { name: "私訊", exact: true }).click();
    await page.getByLabel("私訊", { exact: true }).fill(`Message ${suffix}`);
    await page.getByRole("button", { name: "傳送", exact: true }).click();
    await expect(page.getByRole("log").getByText(`Message ${suffix}`, { exact: true })).toBeVisible();
    const conversationId = new URL(page.url()).searchParams.get("conversation")!;
    await reader.goto(`/zh-TW/community/messages?conversation=${conversationId}`);
    await expect(reader.getByRole("log").getByText(`Message ${suffix}`, { exact: true })).toBeVisible();
    await reader.screenshot({ path: info.outputPath("community-conversation.png"), fullPage: true });
    expect(await reader.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    await json(reader.request, "PUT", `/community/profiles/${author.profile.id}/block`);
    await page.reload();
    await expect(page.getByRole("button", { name: "傳送", exact: true })).toBeDisabled();
    const blocked = await page.request.post(`/api/travel/community/conversations/${conversationId}/messages`, {
      headers: { Origin: baseURL! },
      data: { body: "Must not deliver", idempotency_key: `blocked-${suffix}` },
    });
    expect(blocked.status()).toBe(403);
    expect(author.profile.id).not.toBe(recipient.profile.id);
  } finally {
    await admin.dispose();
    await readerContext.close();
  }
});
