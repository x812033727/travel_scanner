import { expect, test as base, type APIRequestContext, type Locator, type Page } from "@playwright/test";
import path from "node:path";
import { readFileSync } from "node:fs";
import { plannerCopy } from "../lib/planner-copy";
import tw from "../messages/zh-TW/community.json" with { type: "json" };
import cn from "../messages/zh-CN/community.json" with { type: "json" };
import en from "../messages/en/community.json" with { type: "json" };
import ja from "../messages/ja/community.json" with { type: "json" };
import ko from "../messages/ko/community.json" with { type: "json" };
import type tripsCatalog from "../messages/zh-TW/trips.json";

const catalogs = { "zh-TW": tw, "zh-CN": cn, en, ja, ko };
type LocaleCase = { locale: string; copy: typeof tw };
// A real login per worker, never a forged token or ordinary-member session reuse.
// The 30 cases otherwise spend 30 admin logins in the shared CI IP quota.
const test = base.extend<object, { communityAdmin: APIRequestContext }>({
  communityAdmin: [async ({ playwright }, runFixture) => {
    expect(["localhost", "127.0.0.1", "[::1]"]).toContain(new URL(siteOrigin).hostname);
    const admin = await playwright.request.newContext({ baseURL: siteOrigin });
    try {
      await enableTestCommunity(admin);
      await runFixture(admin);
    } finally {
      await admin.dispose();
    }
  }, { scope: "worker" }],
});

// No endpoint interception or test authentication bypass. This suite needs the
// CI/local PostgreSQL, Redis, private MinIO, Mailpit and ordinary RQ worker.
test.skip(process.env.COMMUNITY_E2E !== "1", "Requires the community companion services");
// The runner traces every browser context, including the separate administrator.
// Keep first-failure evidence on local runs too, without starting tracing twice.
test.use({ trace: "retain-on-failure" });

const siteOrigin = new URL(process.env.PLAYWRIGHT_BASE_URL || `http://127.0.0.1:${process.env.PLAYWRIGHT_PORT || "3000"}`).origin;

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

async function checkAppearance(page: Page, control: Locator, colorScheme: "light" | "dark") {
  await page.emulateMedia({ colorScheme });
  await expect(page.locator("html")).toHaveAttribute("data-theme", colorScheme);
  await expect(control).toBeVisible();
  await expect(control).toBeEnabled();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
}

async function json(client: APIRequestContext, method: string, route: string, data?: unknown) {
  const response = await client.fetch(`/api/travel${route}`, { method, data,
    headers: { Origin: siteOrigin } });
  expect(response.ok(), `${method} ${route}: ${await response.text()}`).toBeTruthy();
  return response.status() === 204 ? null : response.json();
}

async function registerAndVerify(page: Page, handle: string, displayName: string, { locale, copy }: LocaleCase) {
  page.setDefaultTimeout(20_000);
  page.setDefaultNavigationTimeout(45_000);
  const email = `${handle}@example.com`;
  await json(page.request, "POST", "/auth/register", { email, password: "community-member-password-123", preferred_locale: locale });
  await page.goto(`/${locale}/community/settings`);
  await page.getByLabel(copy.handle, { exact: false }).fill(handle);
  await page.getByLabel(copy.displayName, { exact: true }).fill(displayName);
  await page.getByRole("button", { name: copy.save, exact: true }).click();
  await expect(page.getByRole("status").filter({ hasText: copy.saved })).toBeVisible();
  await page.goto(`/${locale}/account`);
  await page.getByRole("button", { name: copy.sendVerification, exact: true }).click();
  const url = await accountMail(page, email, "verify");
  expect(url.pathname).toBe(`/${locale}/account/confirm`);
  await page.goto(url.pathname + url.search + url.hash);
  await page.getByRole("button", { name: copy.confirm, exact: true }).click();
  await expect(page.getByText(copy.accountActionDone, { exact: false })).toBeVisible();
  await expect(page.locator("html")).toHaveAttribute("lang", locale);
  expect((await page.request.get("/api/travel/admin/community/settings")).status()).toBe(403);
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
    posting_enabled: true, comments_enabled: true, messaging_enabled: true, pet_reports_enabled: true, translation_enabled: false }, reason: "Isolated CI acceptance" });
}

for (const [locale, copy] of Object.entries(catalogs)) {
  const trips = JSON.parse(readFileSync(new URL(`../messages/${locale}/trips.json`, import.meta.url), "utf8")) as typeof tripsCatalog;
  const setup = { locale, copy };

test(`${locale}: verified members publish reviewed private images, fork safely and exchange mutual-only messages`, async ({ page, browser, baseURL, communityAdmin }, info) => {
  test.setTimeout(300_000);
  const admin = communityAdmin;
  const colorScheme = info.project.use.isMobile ? "dark" : "light";
  await page.emulateMedia({ colorScheme });
  const readerContext = await browser.newContext({ baseURL, viewport: info.project.use.viewport,
    isMobile: info.project.use.isMobile, deviceScaleFactor: info.project.use.deviceScaleFactor,
    hasTouch: info.project.use.hasTouch, userAgent: info.project.use.userAgent, locale, colorScheme });
  const reader = await readerContext.newPage();
  try {
    const suffix = `${Date.now()}${info.workerIndex}`;
    const authorHandle = `author${suffix}`;
    const readerHandle = `reader${suffix}`;
    const author = await registerAndVerify(page, authorHandle, `Author ${suffix}`, setup);
    const recipient = await registerAndVerify(reader, readerHandle, `Reader ${suffix}`, setup);
    await expect(page.locator("html")).toHaveAttribute("data-theme", colorScheme);
    const departure = new Date(Date.now() + 30 * 86400_000).toISOString().slice(0, 10);
    const trip = await json(page.request, "POST", "/trips", { source: "blank", planning_mode: "manual_blank",
      name: `Private ${suffix}`, destination_name: "Tokyo", start_date: departure, end_date: departure,
      notes: "PRIVATE NOTE MUST NEVER BE PUBLISHED", timezone: "Asia/Tokyo" });

    await page.goto(`/${locale}/community/new`);
    const title = `Community acceptance ${suffix}`;
    await page.getByLabel(copy.postTitle, { exact: true }).fill(title);
    await page.getByLabel(copy.destination, { exact: true }).fill("Tokyo");
    await page.getByLabel(copy.postBody, { exact: true }).fill("A real test account sharing its test itinerary.");
    await page.getByLabel(copy.imageDescription, { exact: true }).fill("Mokaair test image");
    await page.getByLabel(copy.upload, { exact: true }).setInputFiles(path.resolve("public/brand/mokaair-monogram.png"));
    const image = page.getByRole("img", { name: "Mokaair test image" });
    await expect(image).toBeVisible({ timeout: 30_000 });
    await expect.poll(() => image.evaluate((element) => (element as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
    await page.getByLabel(copy.sourceTrip).selectOption(trip.id);
    await page.getByLabel(copy.allowFork).check();
    await page.getByRole("button", { name: copy.preview, exact: true }).click();
    const preview = page.getByRole("dialog", { name: copy.preview });
    await expect(preview).not.toContainText("PRIVATE NOTE MUST NEVER BE PUBLISHED");
    await preview.getByLabel(copy.confirmPublicSnapshot, { exact: true }).check();
    await preview.getByRole("button", { name: copy.close, exact: true }).click();
    await page.getByRole("button", { name: copy.publish, exact: true }).click();
    await expect(page).toHaveURL(/\/community\/posts\/[\da-f-]+\/edit$/);
    const postId = page.url().match(/posts\/([\da-f-]+)\/edit/)![1];
    const pending = await json(page.request, "GET", `/community/posts/${postId}/draft`);
    expect(pending.pending_revision_id).toBeTruthy();
    expect((await reader.request.get(`/api/travel/community/posts/${postId}`)).status()).toBe(404);
    expect((await reader.request.get(`/api/travel/community/media/${pending.media[0].id}`)).status()).toBe(404);
    await json(admin, "PUT", `/admin/community/posts/${postId}`, { action: "approve", version: pending.version, reason: "Reviewed CI source and private snapshot" });

    await reader.goto(`/${locale}/community/posts/${postId}`);
    await expect(reader.getByRole("heading", { name: title, exact: true })).toBeVisible();
    await expect(reader.getByRole("img", { name: "Mokaair test image" })).toBeVisible();
    await expect(reader.locator("html")).toHaveAttribute("lang", locale);
    await expect(reader.locator("html")).toHaveAttribute("data-theme", colorScheme);
    const reportTrigger = reader.getByRole("button", { name: copy.report, exact: true });
    for (const appearance of ["light", "dark"] as const) {
      await checkAppearance(reader, reportTrigger, appearance);
      await reportTrigger.focus();
      await reader.keyboard.press("Enter");
      const reportDialog = reader.getByRole("dialog", { name: copy.report, exact: true });
      await expect(reportDialog).toBeVisible();
      const closeReport = reportDialog.getByRole("button", { name: copy.close, exact: true });
      await expect(closeReport).toBeFocused();
      await reader.keyboard.press("Shift+Tab");
      await expect(reportDialog.getByRole("button", { name: copy.submit, exact: true })).toBeFocused();
      await reader.keyboard.press("Tab");
      await expect(closeReport).toBeFocused();
      await reader.keyboard.press("Escape");
      await expect(reportDialog).toHaveCount(0);
      await expect(reportTrigger).toBeFocused();
    }

    await reader.getByRole("button", { name: copy.addToCollection, exact: true }).click();
    const collectionDialog = reader.getByRole("dialog", { name: copy.collections, exact: true });
    const collectionName = `Private collection ${suffix}`;
    await collectionDialog.getByLabel(copy.name, { exact: true }).fill(collectionName);
    await collectionDialog.getByRole("button", { name: copy.save, exact: true }).click();
    await expect(collectionDialog).toHaveCount(0);
    const collections = await json(reader.request, "GET", "/community/collections");
    const collection = collections.items.find((item: { name: string }) => item.name === collectionName);
    expect(collection).toBeTruthy();
    const items = await json(reader.request, "GET", `/community/collections/${collection.id}/items`);
    expect(items.items.map((item: { kind: string; target: string }) => ({ kind: item.kind, target: item.target })))
      .toEqual([{ kind: "post", target: postId }]);
    expect((await page.request.get(`/api/travel/community/collections/${collection.id}/items`)).status()).toBe(404);
    await reader.goto(`/${locale}/community/collections`);
    if (info.project.use.isMobile) {
      await reader.getByRole("combobox", { name: copy.collections, exact: true }).selectOption("collections");
    } else {
      await reader.getByRole("tab", { name: copy.collections, exact: true }).click();
    }
    await reader.getByRole("combobox", { name: copy.collection, exact: true }).selectOption(collection.id);
    await expect(reader.getByRole("link", { name: title, exact: true })).toBeVisible();
    await reader.goto(`/${locale}/community/posts/${postId}`);
    await reader.getByRole("button", { name: `${copy.like} · 0`, exact: true }).click();
    await expect(reader.getByRole("button", { name: `${copy.unlike} · 1`, exact: true })).toBeVisible();
    await reader.getByLabel(copy.writeComment).fill(`Comment ${suffix}`);
    await reader.getByRole("button", { name: copy.submit, exact: true }).click();
    await expect(reader.getByText(`Comment ${suffix}`, { exact: true })).toBeVisible();
    await reader.getByRole("button", { name: copy.forkFree, exact: true }).click();
    await reader.getByLabel(copy.departureDate).fill(departure);
    const forkResponse = reader.waitForResponse((response) =>
      new URL(response.url()).pathname === `/api/travel/community/posts/${postId}/fork` && response.request().method() === "POST");
    await reader.getByRole("button", { name: copy.createPrivateTrip, exact: true }).click();
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

    await reader.goto(`/${locale}/community/profiles/${authorHandle}`);
    await expect(reader.getByRole("button", { name: copy.message, exact: true })).toBeDisabled();
    await reader.getByRole("button", { name: copy.follow, exact: true }).click();
    await page.goto(`/${locale}/community/profiles/${readerHandle}`);
    await page.getByRole("button", { name: copy.follow, exact: true }).click();
    await expect(page.getByRole("button", { name: copy.message, exact: true })).toBeEnabled();
    await page.getByRole("button", { name: copy.message, exact: true }).click();
    await page.getByLabel(copy.message, { exact: true }).fill(`Message ${suffix}`);
    await page.getByRole("button", { name: copy.send, exact: true }).click();
    await expect(page.getByRole("log").getByText(`Message ${suffix}`, { exact: true })).toBeVisible();
    const conversationId = new URL(page.url()).searchParams.get("conversation")!;
    await reader.goto(`/${locale}/community/messages?conversation=${conversationId}`);
    await expect(reader.getByRole("log").getByText(`Message ${suffix}`, { exact: true })).toBeVisible();
    for (const appearance of ["light", "dark"] as const) {
      await checkAppearance(reader, reader.getByLabel(copy.message, { exact: true }), appearance);
    }
    await reader.screenshot({ path: info.outputPath("community-conversation.png"), fullPage: true });
    expect(await reader.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    // Take the reader offline while the other member writes, then bring it back. setOffline
    // does not cut an EventSource that is already open: the events still arrive, but the
    // refreshes they trigger fail, so this checks the catch-up that runs once the browser is
    // back online, without a page reload, not a Last-Event-ID replay after a reconnect.
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
    await expect(page.getByRole("button", { name: copy.send, exact: true })).toBeDisabled();
    const unfollowed = await page.request.post(`/api/travel/community/conversations/${conversationId}/messages`, {
      headers: { Origin: baseURL! },
      data: { body: "Must not deliver", idempotency_key: `unfollowed-${suffix}` },
    });
    expect(unfollowed.status()).toBe(403);
    expect((await unfollowed.json()).code).toBe("community_mutual_required");
    await json(reader.request, "PUT", `/community/profiles/${author.profile.id}/block`);
    await page.reload();
    // Blocking hides the counterpart and conversation as well as stopping writes.
    await expect(page.getByRole("main").getByRole("alert")).toHaveText(copy.errors.community_not_found);
    await expect(page.getByRole("button", { name: copy.send, exact: true })).toHaveCount(0);
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
    await readerContext.close();
  }
});

test(`${locale}: reviewed pet rules filter conservatively and require confirmation before conflicting trip additions`, async ({ page, browser, baseURL, communityAdmin }, info) => {
  test.setTimeout(300_000);
  const colorScheme = info.project.use.isMobile ? "dark" : "light";
  await page.emulateMedia({ colorScheme });
  const adminContext = await browser.newContext({ baseURL, storageState: await communityAdmin.storageState(), viewport: info.project.use.viewport,
    isMobile: info.project.use.isMobile, deviceScaleFactor: info.project.use.deviceScaleFactor,
    hasTouch: info.project.use.hasTouch, userAgent: info.project.use.userAgent, locale, colorScheme });
  const admin = await adminContext.newPage();
  admin.setDefaultTimeout(20_000);
  admin.setDefaultNavigationTimeout(45_000);
  try {
    const suffix = `${Date.now()}${info.workerIndex}`;
    await registerAndVerify(page, `pet${suffix}`, `Pet traveller ${suffix}`, setup);
    const name = `Pet cafe ${suffix}`;
    await page.goto(`/${locale}/pet-friendly`);
    await page.getByRole("button", { name: copy.suggestPlace, exact: true }).click();
    const suggestion = page.getByRole("dialog", { name: copy.suggestPlace });
    await suggestion.getByLabel(copy.placeFields.name, { exact: true }).fill(name);
    await suggestion.getByLabel(copy.destination, { exact: true }).fill("Taipei");
    await suggestion.getByLabel(copy.placeFields.official_url, { exact: true }).fill("https://example.com/pet-policy");
    await suggestion.getByRole("button", { name: copy.submit, exact: true }).click();
    await expect(suggestion).toHaveCount(0);
    const candidates = await json(admin.request, "GET", "/admin/pet-friendly/places?state=pending");
    const candidate = candidates.items.find((item: { name: string }) => item.name === name);
    expect(candidate).toBeTruthy();
    expect((await page.request.get(`/api/travel/pet-friendly/places/${candidate.id}`)).status()).toBe(404);

    await admin.goto(`/${locale}/admin/pet-friendly`);
    const candidateCard = admin.getByRole("article").filter({ has: admin.getByRole("heading", { name: `${name} · Taipei`, exact: true }) });
    await candidateCard.getByRole("button", { name: copy.reviewRules, exact: true }).click();
    const review = admin.getByRole("dialog", { name: copy.reviewRules });
    await review.getByRole("button", { name: copy.addSpeciesRule, exact: true }).click();
    const rule = review.getByRole("group", { name: copy.speciesRule.replace("{count}", "1"), exact: true });
    await rule.getByRole("combobox", { name: copy.status, exact: true }).selectOption("conditional");
    await rule.getByRole("combobox", { name: copy.petFields.weight_limit, exact: true }).selectOption("limited");
    await rule.getByRole("spinbutton", { name: copy.petFields.weight_limit, exact: true }).fill("10");
    await rule.getByRole("combobox", { name: copy.petFields.count_limit, exact: true }).selectOption("none");
    for (const label of [copy.petFields.carrier_required, copy.petFields.stroller_required, copy.petFields.diaper_required]) {
      await rule.getByRole("combobox", { name: label, exact: true }).selectOption("false");
    }
    await rule.getByRole("combobox", { name: copy.petFields.leash_required, exact: true }).selectOption("true");
    await rule.getByRole("combobox", { name: copy.petFields.indoor_allowed, exact: true }).selectOption("true");
    await review.getByLabel(copy.ruleSource, { exact: true }).fill("https://example.com/pet-policy");
    await review.getByLabel(copy.reason, { exact: true }).fill("Isolated test fixture: dogs up to 10 kg; other species unknown");
    await review.getByRole("button", { name: copy.saveReview, exact: true }).click();
    await expect(review).toHaveCount(0);

    await page.reload();
    await page.getByLabel(copy.search, { exact: true }).fill(name);
    await page.getByLabel(copy.matchMyPet).check();
    await page.getByLabel(copy.species, { exact: true }).fill("dog");
    await page.getByLabel(copy.petWeight, { exact: true }).fill("5");
    await page.getByRole("button", { name: copy.filter, exact: true }).click();
    await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();
    await page.getByLabel(copy.species, { exact: true }).fill("cat");
    await page.getByRole("button", { name: copy.filter, exact: true }).click();
    await expect(page.getByRole("heading", { name, exact: true })).toHaveCount(0);
    await page.getByLabel(copy.includeUncertain).check();
    await page.getByRole("button", { name: copy.filter, exact: true }).click();
    await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();
    await expect(page.getByText(copy.conflicts.species_unknown, { exact: true })).toBeVisible();

    const departure = new Date(Date.now() + 30 * 86400_000).toISOString().slice(0, 10);
    const trip = await json(page.request, "POST", "/trips", { source: "blank", planning_mode: "manual_blank",
      name: `Pet trip ${suffix}`, destination_name: "Taipei", start_date: departure, end_date: departure,
      notes: "Preserve this private note", timezone: "Asia/Taipei" });
    // Creation notes are planner input in data.notes; editable trip notes use PATCH.
    const withNotes = await json(page.request, "PATCH", `/trips/${trip.id}`, {
      version: trip.version, notes: "Preserve this private note" });
    expect(withNotes.notes).toBe("Preserve this private note");
    await page.goto(`/${locale}/trips/${trip.id}`);
    await page.getByRole("button", { name: trips.editor.openTools, exact: true }).click();
    await page.getByRole("button", { name: new RegExp(`^${escapeRegExp(plannerCopy(locale).preparation)}`) }).click();
    const petPanel = page.locator("details").filter({ has: page.locator("summary").filter({ hasText: new RegExp(`^${escapeRegExp(copy.petCompanion)}$`) }) });
    await petPanel.locator("summary").click();
    await petPanel.getByLabel(copy.travelWithPet).check();
    await petPanel.getByLabel(copy.species, { exact: true }).fill("cat");
    await petPanel.getByRole("button", { name: copy.save, exact: true }).click();
    await expect(petPanel.getByRole("status")).toHaveText(copy.saved);
    const savedPet = await json(page.request, "GET", `/community/trips/${trip.id}/pet-preferences`);
    expect(savedPet.requirements.species).toBe("cat");
    const beforeAdd = await json(page.request, "GET", `/trips/${trip.id}`);
    expect(beforeAdd.notes).toBe("Preserve this private note");
    await page.goto(`/${locale}/pet-friendly/${candidate.id}`);
    await page.getByRole("button", { name: copy.addToTrip, exact: true }).click();
    const add = page.getByRole("dialog", { name: copy.addToTrip });
    await add.getByRole("combobox", { name: copy.chooseTrip, exact: true }).selectOption(trip.id);
    await add.getByLabel(copy.date, { exact: true }).fill(departure);
    await add.getByRole("button", { name: copy.addToTrip, exact: true }).click();
    await expect(add.getByText(copy.conflicts.species_unknown, { exact: true })).toBeVisible();
    const unconfirmed = await json(page.request, "GET", `/trips/${trip.id}`);
    expect(unconfirmed.items).toEqual(beforeAdd.items);
    await add.getByRole("button", { name: copy.confirmAddAnyway, exact: true }).click();
    await expect(add).toHaveCount(0);
    const confirmed = await json(page.request, "GET", `/trips/${trip.id}`);
    expect(confirmed.items.filter((item: { data: { pet_place_id?: string } }) => item.data.pet_place_id === candidate.id)).toHaveLength(1);
    expect(confirmed.notes).toBe("Preserve this private note");
    expect(confirmed.data.notes).toBe(beforeAdd.data.notes);

    await page.getByRole("button", { name: copy.reportVisit, exact: true }).click();
    const report = page.getByRole("dialog", { name: copy.reportVisit });
    const observation = `Traveller observation ${suffix}: policies may have changed.`;
    await report.getByLabel(copy.visitExperience, { exact: true }).fill(observation);
    await report.getByLabel(copy.visitedOn, { exact: true }).fill(new Date().toISOString().slice(0, 10));
    await report.getByRole("button", { name: copy.submitForReview, exact: true }).click();
    await expect(report).toHaveCount(0);
    const pendingReportPlace = await json(page.request, "GET", `/pet-friendly/places/${candidate.id}`);
    expect(pendingReportPlace.experiences).toHaveLength(0);
    expect(pendingReportPlace.verification_current).toBe(true);
    const reports = await json(admin.request, "GET", "/admin/pet-friendly/reports");
    const submitted = reports.items.find((item: { body: string }) => item.body === observation);
    await json(admin.request, "PUT", `/admin/pet-friendly/reports/${submitted.id}`, {
      status: "resolved", flag_conflict: true, reason: "Test observation requires source reconfirmation" });
    await page.reload();
    await expect(page.getByRole("heading", { name: copy.needsConfirmation, exact: true })).toBeVisible();
    await expect(page.getByText(observation, { exact: true })).toBeVisible();
    const disputed = await json(page.request, "GET", `/pet-friendly/places/${candidate.id}`);
    expect(disputed.policies).toEqual(pendingReportPlace.policies);
    expect(disputed.verification_current).toBe(false);
    await page.screenshot({ path: info.outputPath("pet-reviewed-experience.png"), fullPage: true });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    for (const appearance of ["light", "dark"] as const) {
      const reportVisit = page.getByRole("button", { name: copy.reportVisit, exact: true });
      await checkAppearance(page, reportVisit, appearance);
      await reportVisit.focus();
      await page.keyboard.press("Enter");
      const reportDialog = page.getByRole("dialog", { name: copy.reportVisit, exact: true });
      await expect(reportDialog).toBeVisible();
      await page.keyboard.press("Escape");
      await expect(reportDialog).toHaveCount(0);
      await expect(reportVisit).toBeFocused();
    }

    // The editor associates a catalog identity through search, never pasted IDs.
    await page.goto(`/${locale}/community/new`);
    await page.getByLabel(copy.postTitle, { exact: true }).fill(`Pet visit ${suffix}`);
    await page.getByLabel(copy.postBody, { exact: true }).fill("A personal visit; current rules need reconfirmation.");
    await page.getByLabel(copy.destination, { exact: true }).fill("Taipei");
    await page.getByLabel(copy.searchPlaces, { exact: true }).fill(name);
    await page.getByRole("button", { name: copy.search, exact: true }).click();
    await page.getByRole("button", { name: copy.addRelatedPlace.replace("{name}", name), exact: true }).click();
    await expect(page.getByRole("button", { name: copy.addRelatedPlace.replace("{name}", name), exact: true })).toBeDisabled();
    await page.getByRole("button", { name: copy.publish, exact: true }).click();
    await expect(page).toHaveURL(/\/community\/posts\/[^/]+\/edit$/);
    const postId = page.url().split("/").at(-2)!;
    const draft = await json(page.request, "GET", `/community/posts/${postId}/draft`);
    expect(draft.places.map((place: { id: string; kind: string }) => ({ id: place.id, kind: place.kind })))
      .toEqual([{ id: candidate.id, kind: "pet_place" }]);
    await json(admin.request, "PUT", `/admin/community/posts/${postId}`, {
      version: draft.version, action: "approve", reason: "Test visit association reviewed" });
    await page.goto(`/${locale}/community/posts/${postId}`);
    await expect(page.getByRole("link", { name, exact: true })).toHaveAttribute("href", `/${locale}/pet-friendly/${candidate.id}`);
  } finally {
    // Runner-managed tracing preserves the secondary admin page. Do not mask a
    // failed UI operation with a teardown error after the test timeout.
    await adminContext.close().catch(() => {});
  }
});

test(`${locale}: mail recovery revokes old sessions and deletion immediately hides the public identity`, async ({ page, browser, baseURL, communityAdmin }, info) => {
  test.setTimeout(180_000);
  const colorScheme = info.project.use.isMobile ? "dark" : "light";
  await page.emulateMedia({ colorScheme });
  // Request the worker fixture for real community setup before the member journey.
  expect(communityAdmin).toBeTruthy();
  const stale = await browser.newContext({ baseURL });
  try {
    const handle = `safety${Date.now()}${info.workerIndex}`;
    const email = `${handle}@example.com`;
    await registerAndVerify(page, handle, "Account safety test", setup);
    const oldPassword = "community-member-password-123";
    const newPassword = "community-recovered-password-456";
    await json(stale.request, "POST", "/auth/login", { email, password: oldPassword });
    await page.goto(`/${locale}/forgot-password`);
    await page.getByLabel(copy.email, { exact: true }).fill(email);
    await page.getByRole("button", { name: copy.sendReset, exact: true }).click();
    await expect(page.getByRole("status")).toHaveText(copy.resetSent);
    const reset = await accountMail(page, email, "reset");
    expect(reset.pathname).toBe(`/${locale}/account/confirm`);
    await page.goto(reset.pathname + reset.search + reset.hash);
    await page.getByLabel(copy.newPassword, { exact: true }).fill(newPassword);
    await expect(page).not.toHaveURL(/#token=/);
    for (const appearance of ["light", "dark"] as const) {
      await checkAppearance(page, page.getByRole("button", { name: copy.confirm, exact: true }), appearance);
    }
    await page.getByRole("button", { name: copy.confirm, exact: true }).click();
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
    await page.goto(`/${locale}/account`);
    page.once("dialog", (dialog) => dialog.accept());
    await page.getByRole("button", { name: copy.requestDeletion, exact: true }).click();
    const deletion = await accountMail(page, email, "delete");
    expect(deletion.pathname).toBe(`/${locale}/account/confirm`);
    await page.goto(deletion.pathname + deletion.search + deletion.hash);
    await page.getByLabel(copy.typeDelete, { exact: true }).fill("DELETE");
    await page.getByRole("button", { name: copy.confirm, exact: true }).click();
    await expect(page).toHaveURL(/\/login$/);
    expect((await stale.request.get("/api/travel/auth/me")).status()).toBe(401);
    expect((await page.request.get(`/api/travel/community/profiles/${handle}`)).status()).toBe(404);
    expect((await page.request.post("/api/travel/auth/login", {
      headers: { Origin: baseURL! }, data: { email, password: newPassword } })).status()).toBe(401);
  } finally {
    await stale.close();
  }
});

}
