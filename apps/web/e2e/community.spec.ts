import { expect, request, test, type APIRequestContext, type Page } from "@playwright/test";
import path from "node:path";
import zhCommunity from "../messages/zh-TW/community.json" with { type: "json" };

// No endpoint interception or test authentication bypass. This suite needs the
// CI/local PostgreSQL, Redis, private MinIO, Mailpit and ordinary RQ worker.
test.skip(process.env.COMMUNITY_E2E !== "1", "Requires the community companion services");

const siteOrigin = new URL(process.env.PLAYWRIGHT_BASE_URL || `http://127.0.0.1:${process.env.PLAYWRIGHT_PORT || "3000"}`).origin;

async function json(client: APIRequestContext, method: string, route: string, data?: unknown) {
  const response = await client.fetch(`/api/travel${route}`, { method, data,
    headers: { Origin: siteOrigin } });
  expect(response.ok(), `${method} ${route}: ${await response.text()}`).toBeTruthy();
  return response.status() === 204 ? null : response.json();
}

async function registerAndVerify(page: Page, handle: string, displayName: string) {
  page.setDefaultTimeout(20_000);
  page.setDefaultNavigationTimeout(45_000);
  const email = `${handle}@example.com`;
  await json(page.request, "POST", "/auth/register", { email, password: "community-member-password-123" });
  await page.goto("/zh-TW/community/settings");
  await page.getByLabel("帳號代稱", { exact: false }).fill(handle);
  await page.getByLabel("暱稱", { exact: true }).fill(displayName);
  await page.getByRole("button", { name: "儲存", exact: true }).click();
  await expect(page.getByRole("status").filter({ hasText: "已儲存" })).toBeVisible();
  await page.goto("/zh-TW/account");
  await page.getByRole("button", { name: "寄送驗證信", exact: true }).click();
  const url = await accountMail(page, email, "verify");
  await page.goto(url.pathname + url.search + url.hash);
  await page.getByRole("button", { name: "確認", exact: true }).click();
  await expect(page.getByText("已完成帳號操作", { exact: false })).toBeVisible();
  return json(page.request, "GET", "/community/me");
}

async function accountMail(page: Page, email: string, purpose: "verify" | "reset" | "delete") {
  let verificationUrl = "";
  await expect.poll(async () => {
    const result = await page.request.get(`http://127.0.0.1:8025/api/v1/search?query=${encodeURIComponent(`to:${email}`)}`);
    const messages = (await result.json()).messages || [];
    if (!messages.length) return false;
    const mail = await page.request.get(`http://127.0.0.1:8025/api/v1/message/${messages[0].ID}`);
    verificationUrl = (await mail.json()).Text.match(/https?:\/\/[^\s]+#token=[A-Za-z0-9_-]+/)?.[0] || "";
    return Boolean(verificationUrl) && new URL(verificationUrl).searchParams.get("purpose") === purpose;
  }, { timeout: 45_000, intervals: [500, 1000, 2000] }).toBe(true);
  return new URL(verificationUrl);
}

async function enableTestCommunity(admin: APIRequestContext) {
  await json(admin, "POST", "/auth/login", { email: "ci-community@example.com", password: "community-ci-password-123" });
  const current = await json(admin, "GET", "/admin/community/settings");
  await json(admin, "PUT", "/admin/community/settings", { settings: { ...current.settings, enabled: true,
    posting_enabled: true, comments_enabled: true, messaging_enabled: true, pet_reports_enabled: true }, reason: "Isolated CI acceptance" });
}

test("verified members publish reviewed private images, fork safely and exchange mutual-only messages", async ({ page, browser, baseURL }, info) => {
  test.setTimeout(300_000);
  const admin = await request.newContext({ baseURL, extraHTTPHeaders: { Origin: baseURL! } });
  const readerContext = await browser.newContext({ baseURL, viewport: info.project.use.viewport,
    isMobile: info.project.use.isMobile, deviceScaleFactor: info.project.use.deviceScaleFactor });
  const reader = await readerContext.newPage();
  try {
    await enableTestCommunity(admin);
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
    const forkResponse = reader.waitForResponse((response) =>
      new URL(response.url()).pathname === `/api/travel/community/posts/${postId}/fork` && response.request().method() === "POST");
    await reader.getByRole("button", { name: "建立私人副本", exact: true }).click();
    const forkResult = await forkResponse;
    expect(forkResult.status(), await forkResult.text()).toBe(201);
    await expect(reader).toHaveURL(/\/trips\/[\da-f-]+$/, { timeout: 20_000 });
    const copiedId = reader.url().split("/").at(-1)!;
    expect(copiedId).not.toBe(trip.id);
    const firstReads = await Promise.all(Array.from({ length: 3 }, () => json(reader.request, "GET", `/trips/${copiedId}`)));
    for (const copy of firstReads) {
      expect(JSON.stringify(copy)).not.toContain("PRIVATE NOTE MUST NEVER BE PUBLISHED");
      const roles = copy.items.filter((item: { system_role: string | null }) => item.system_role)
        .map((item: { day_date: string; system_role: string }) => `${item.day_date}:${item.system_role}`);
      expect(new Set(roles).size).toBe(roles.length);
    }

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
    // Cut the reader's real network connection while the other member writes.
    // Reconnection must catch up through durable events without a page reload.
    await readerContext.setOffline(true);
    const missed = [`Offline first ${suffix}`, `Offline second ${suffix}`];
    for (const [index, body] of missed.entries()) {
      const payload = { body, idempotency_key: `offline-${suffix}-${index}` };
      const sent = await json(page.request, "POST", `/community/conversations/${conversationId}/messages`, payload);
      const replay = await json(page.request, "POST", `/community/conversations/${conversationId}/messages`, payload);
      expect(replay.id).toBe(sent.id);
    }
    for (const body of missed) await expect(reader.getByRole("log").getByText(body, { exact: true })).toHaveCount(0);
    await readerContext.setOffline(false);
    for (const body of missed) {
      await expect(reader.getByRole("log").getByText(body, { exact: true })).toBeVisible({ timeout: 30_000 });
      await expect(reader.getByRole("log").getByText(body, { exact: true })).toHaveCount(1);
    }
    // Unfollowing preserves delivered history but immediately disables new writes.
    await json(reader.request, "DELETE", `/community/profiles/${author.profile.id}/follow`);
    await page.reload();
    await expect(page.getByRole("log").getByText(`Message ${suffix}`, { exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: "傳送", exact: true })).toBeDisabled();
    const unfollowed = await page.request.post(`/api/travel/community/conversations/${conversationId}/messages`, {
      headers: { Origin: baseURL! },
      data: { body: "Must not deliver", idempotency_key: `unfollowed-${suffix}` },
    });
    expect(unfollowed.status()).toBe(403);
    expect((await unfollowed.json()).code).toBe("community_mutual_required");
    await json(reader.request, "PUT", `/community/profiles/${author.profile.id}/block`);
    await page.reload();
    // Blocking hides the counterpart and conversation as well as stopping writes.
    await expect(page.getByRole("main").getByRole("alert")).toHaveText(zhCommunity.errors.community_not_found);
    await expect(page.getByRole("button", { name: "傳送", exact: true })).toHaveCount(0);
    await expect(page.getByRole("log")).toHaveCount(0);
    const blocked = await page.request.post(`/api/travel/community/conversations/${conversationId}/messages`, {
      headers: { Origin: baseURL! },
      data: { body: "Must not deliver", idempotency_key: `blocked-${suffix}` },
    });
    expect(blocked.status()).toBe(404);
    expect((await blocked.json()).code).toBe("community_not_found");
    await json(reader.request, "DELETE", `/community/profiles/${author.profile.id}/block`);
    const delivered = await json(reader.request, "GET", `/community/conversations/${conversationId}/messages`);
    expect(delivered.items.map((message: { body: string }) => message.body)).toEqual([`Message ${suffix}`, ...missed]);
    expect(author.profile.id).not.toBe(recipient.profile.id);
  } finally {
    await admin.dispose();
    await readerContext.close();
  }
});

test("reviewed pet rules filter conservatively and require confirmation before conflicting trip additions", async ({ page, browser, baseURL }, info) => {
  test.setTimeout(300_000);
  const adminContext = await browser.newContext({ baseURL, viewport: info.project.use.viewport,
    isMobile: info.project.use.isMobile, deviceScaleFactor: info.project.use.deviceScaleFactor });
  const admin = await adminContext.newPage();
  admin.setDefaultTimeout(20_000);
  admin.setDefaultNavigationTimeout(45_000);
  await adminContext.tracing.start({ screenshots: true, snapshots: true });
  try {
    await enableTestCommunity(admin.request);
    const suffix = `${Date.now()}${info.workerIndex}`;
    await registerAndVerify(page, `pet${suffix}`, `Pet traveller ${suffix}`);
    const name = `Pet cafe ${suffix}`;
    await page.goto("/zh-TW/pet-friendly");
    await page.getByRole("button", { name: "提交新場所候選", exact: true }).click();
    const suggestion = page.getByRole("dialog", { name: "提交新場所候選" });
    await suggestion.getByLabel("場所名稱", { exact: true }).fill(name);
    await suggestion.getByLabel("目的地", { exact: true }).fill("Taipei");
    await suggestion.getByLabel("官方網站", { exact: true }).fill("https://example.com/pet-policy");
    await suggestion.getByRole("button", { name: "送出", exact: true }).click();
    await expect(suggestion).toHaveCount(0);
    const candidates = await json(admin.request, "GET", "/admin/pet-friendly/places?state=pending");
    const candidate = candidates.items.find((item: { name: string }) => item.name === name);
    expect(candidate).toBeTruthy();
    expect((await page.request.get(`/api/travel/pet-friendly/places/${candidate.id}`)).status()).toBe(404);

    await admin.goto("/zh-TW/admin/pet-friendly");
    const candidateCard = admin.getByRole("article").filter({ has: admin.getByRole("heading", { name: `${name} · Taipei`, exact: true }) });
    await candidateCard.getByRole("button", { name: "查核規定", exact: true }).click();
    const review = admin.getByRole("dialog", { name: "查核規定" });
    await review.getByRole("button", { name: "新增動物種類規定", exact: true }).click();
    const rule = review.getByRole("group", { name: "第 1 組動物規定", exact: true });
    await rule.getByRole("combobox", { name: "狀態", exact: true }).selectOption("conditional");
    await rule.getByRole("combobox", { name: "體重限制", exact: true }).selectOption("limited");
    await rule.getByRole("spinbutton", { name: "體重限制", exact: true }).fill("10");
    await rule.getByRole("combobox", { name: "數量限制", exact: true }).selectOption("none");
    for (const label of [zhCommunity.petFields.carrier_required, zhCommunity.petFields.stroller_required, zhCommunity.petFields.diaper_required]) {
      await rule.getByRole("combobox", { name: label, exact: true }).selectOption("false");
    }
    await rule.getByRole("combobox", { name: zhCommunity.petFields.leash_required, exact: true }).selectOption("true");
    await rule.getByRole("combobox", { name: "可進室內", exact: true }).selectOption("true");
    await review.getByLabel("規定來源", { exact: true }).fill("https://example.com/pet-policy");
    await review.getByLabel("原因", { exact: true }).fill("Isolated test fixture: dogs up to 10 kg; other species unknown");
    await review.getByRole("button", { name: "儲存查核結果", exact: true }).click();
    await expect(review).toHaveCount(0);

    await page.reload();
    await page.getByLabel("搜尋", { exact: true }).fill(name);
    await page.getByLabel("依我的寵物條件篩選").check();
    await page.getByLabel("動物種類", { exact: true }).fill("dog");
    await page.getByLabel("每隻體重（公斤）", { exact: true }).fill("5");
    await page.getByRole("button", { name: zhCommunity.filter, exact: true }).click();
    await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();
    await page.getByLabel("動物種類", { exact: true }).fill("cat");
    await page.getByRole("button", { name: zhCommunity.filter, exact: true }).click();
    await expect(page.getByRole("heading", { name, exact: true })).toHaveCount(0);
    await page.getByLabel("也顯示待確認或不符合條件的資料").check();
    await page.getByRole("button", { name: zhCommunity.filter, exact: true }).click();
    await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();
    await expect(page.getByText(zhCommunity.conflicts.species_unknown, { exact: true })).toBeVisible();

    const departure = new Date(Date.now() + 30 * 86400_000).toISOString().slice(0, 10);
    const trip = await json(page.request, "POST", "/trips", { source: "blank", planning_mode: "manual_blank",
      name: `Pet trip ${suffix}`, destination_name: "Taipei", start_date: departure, end_date: departure,
      notes: "Preserve this private note", timezone: "Asia/Taipei" });
    // Creation notes are planner input in data.notes; editable trip notes use PATCH.
    const withNotes = await json(page.request, "PATCH", `/trips/${trip.id}`, {
      version: trip.version, notes: "Preserve this private note" });
    expect(withNotes.notes).toBe("Preserve this private note");
    await page.goto(`/zh-TW/trips/${trip.id}`);
    await page.getByRole("button", { name: /^(開啟)?旅程工具$/ }).click();
    const petPanel = page.locator("details").filter({ has: page.locator("summary").filter({ hasText: /^寵物同行條件$/ }) });
    await petPanel.locator("summary").click();
    await petPanel.getByLabel("這趟旅行有寵物同行").check();
    await petPanel.getByLabel("動物種類", { exact: true }).fill("cat");
    await petPanel.getByRole("button", { name: "儲存", exact: true }).click();
    await expect(petPanel.getByRole("status")).toHaveText("已儲存");
    const savedPet = await json(page.request, "GET", `/community/trips/${trip.id}/pet-preferences`);
    expect(savedPet.requirements.species).toBe("cat");
    const beforeAdd = await json(page.request, "GET", `/trips/${trip.id}`);
    expect(beforeAdd.notes).toBe("Preserve this private note");
    await page.goto(`/zh-TW/pet-friendly/${candidate.id}`);
    await page.getByRole("button", { name: "加入我的行程", exact: true }).click();
    const add = page.getByRole("dialog", { name: "加入我的行程" });
    await add.getByRole("combobox", { name: "選擇我的行程", exact: true }).selectOption(trip.id);
    await add.getByLabel("日期", { exact: true }).fill(departure);
    await add.getByRole("button", { name: "加入我的行程", exact: true }).click();
    await expect(add.getByText(zhCommunity.conflicts.species_unknown, { exact: true })).toBeVisible();
    const unconfirmed = await json(page.request, "GET", `/trips/${trip.id}`);
    expect(unconfirmed.items).toEqual(beforeAdd.items);
    await add.getByRole("button", { name: "確認仍要加入", exact: true }).click();
    await expect(add).toHaveCount(0);
    const confirmed = await json(page.request, "GET", `/trips/${trip.id}`);
    expect(confirmed.items.filter((item: { data: { pet_place_id?: string } }) => item.data.pet_place_id === candidate.id)).toHaveLength(1);
    expect(confirmed.notes).toBe("Preserve this private note");
    expect(confirmed.data.notes).toBe(beforeAdd.data.notes);

    await page.getByRole("button", { name: "回報到訪經驗", exact: true }).click();
    const report = page.getByRole("dialog", { name: "回報到訪經驗" });
    const observation = `Traveller observation ${suffix}: policies may have changed.`;
    await report.getByLabel("到訪經驗與觀察", { exact: true }).fill(observation);
    await report.getByLabel("自述到訪日期", { exact: true }).fill(new Date().toISOString().slice(0, 10));
    await report.getByRole("button", { name: zhCommunity.submitForReview, exact: true }).click();
    await expect(report).toHaveCount(0);
    const pendingReportPlace = await json(page.request, "GET", `/pet-friendly/places/${candidate.id}`);
    expect(pendingReportPlace.experiences).toHaveLength(0);
    expect(pendingReportPlace.verification_current).toBe(true);
    const reports = await json(admin.request, "GET", "/admin/pet-friendly/reports");
    const submitted = reports.items.find((item: { body: string }) => item.body === observation);
    await json(admin.request, "PUT", `/admin/pet-friendly/reports/${submitted.id}`, {
      status: "resolved", flag_conflict: true, reason: "Test observation requires source reconfirmation" });
    await page.reload();
    await expect(page.getByRole("heading", { name: "待確認", exact: true })).toBeVisible();
    await expect(page.getByText(observation, { exact: true })).toBeVisible();
    const disputed = await json(page.request, "GET", `/pet-friendly/places/${candidate.id}`);
    expect(disputed.policies).toEqual(pendingReportPlace.policies);
    expect(disputed.verification_current).toBe(false);
    await page.screenshot({ path: info.outputPath("pet-reviewed-experience.png"), fullPage: true });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);

    // The editor associates a catalog identity through search, never pasted IDs.
    await page.goto("/zh-TW/community/new");
    await page.getByLabel("標題", { exact: true }).fill(`Pet visit ${suffix}`);
    await page.getByLabel("旅行心得", { exact: true }).fill("A personal visit; current rules need reconfirmation.");
    await page.getByLabel("目的地", { exact: true }).fill("Taipei");
    await page.getByLabel(zhCommunity.searchPlaces, { exact: true }).fill(name);
    await page.getByRole("button", { name: "搜尋", exact: true }).click();
    await page.getByRole("button", { name: `加入 ${name}`, exact: true }).click();
    await expect(page.getByRole("button", { name: `加入 ${name}`, exact: true })).toBeDisabled();
    await page.getByRole("button", { name: "發佈", exact: true }).click();
    await expect(page).toHaveURL(/\/community\/posts\/[^/]+\/edit$/);
    const postId = page.url().split("/").at(-2)!;
    const draft = await json(page.request, "GET", `/community/posts/${postId}/draft`);
    expect(draft.places.map((place: { id: string; kind: string }) => ({ id: place.id, kind: place.kind })))
      .toEqual([{ id: candidate.id, kind: "pet_place" }]);
    await json(admin.request, "PUT", `/admin/community/posts/${postId}`, {
      version: draft.version, action: "approve", reason: "Test visit association reviewed" });
    await page.goto(`/zh-TW/community/posts/${postId}`);
    await expect(page.getByRole("link", { name, exact: true })).toHaveAttribute("href", `/zh-TW/pet-friendly/${candidate.id}`);
  } finally {
    // Preserve the actual failed UI operation, including the secondary admin
    // page, instead of masking it with teardown errors after the test timeout.
    await adminContext.tracing.stop({ path: info.outputPath("pet-admin-trace.zip") }).catch(() => {});
    await adminContext.close().catch(() => {});
  }
});

test("mail recovery revokes old sessions and deletion immediately hides the public identity", async ({ page, browser, baseURL }, info) => {
  test.setTimeout(180_000);
  const admin = await request.newContext({ baseURL });
  const stale = await browser.newContext({ baseURL });
  try {
    await enableTestCommunity(admin);
    const handle = `safety${Date.now()}${info.workerIndex}`;
    const email = `${handle}@example.com`;
    await registerAndVerify(page, handle, "Account safety test");
    const oldPassword = "community-member-password-123";
    const newPassword = "community-recovered-password-456";
    await json(stale.request, "POST", "/auth/login", { email, password: oldPassword });
    await page.goto("/zh-TW/forgot-password");
    await page.getByLabel("Email", { exact: true }).fill(email);
    await page.getByRole("button", { name: "寄送重設連結", exact: true }).click();
    await expect(page.getByRole("status")).toContainText("若此帳號可重設密碼");
    const reset = await accountMail(page, email, "reset");
    await page.goto(reset.pathname + reset.search + reset.hash);
    await page.getByLabel("新密碼", { exact: true }).fill(newPassword);
    await expect(page).not.toHaveURL(/#token=/);
    await page.getByRole("button", { name: "確認", exact: true }).click();
    await expect(page).toHaveURL(/\/login$/);
    expect((await stale.request.get("/api/travel/auth/me")).status()).toBe(401);
    const oldLogin = await stale.request.post("/api/travel/auth/login", {
      headers: { Origin: baseURL! }, data: { email, password: oldPassword } });
    expect(oldLogin.status()).toBe(401);
    const replay = await page.request.post("/api/travel/auth/reset-password", {
      headers: { Origin: baseURL! }, data: { token: new URLSearchParams(reset.hash.slice(1)).get("token"), password: newPassword } });
    expect(replay.status()).toBe(400);
    await json(page.request, "POST", "/auth/login", { email, password: newPassword });
    await json(stale.request, "POST", "/auth/login", { email, password: newPassword });
    await page.goto("/zh-TW/account");
    page.once("dialog", (dialog) => dialog.accept());
    await page.getByRole("button", { name: "寄送刪除確認信", exact: true }).click();
    const deletion = await accountMail(page, email, "delete");
    await page.goto(deletion.pathname + deletion.search + deletion.hash);
    await page.getByLabel("輸入 DELETE 確認刪除", { exact: true }).fill("DELETE");
    await page.getByRole("button", { name: "確認", exact: true }).click();
    await expect(page).toHaveURL(/\/login$/);
    expect((await stale.request.get("/api/travel/auth/me")).status()).toBe(401);
    expect((await page.request.get(`/api/travel/community/profiles/${handle}`)).status()).toBe(404);
    expect((await page.request.post("/api/travel/auth/login", {
      headers: { Origin: baseURL! }, data: { email, password: newPassword } })).status()).toBe(401);
  } finally {
    await admin.dispose();
    await stale.close();
  }
});
