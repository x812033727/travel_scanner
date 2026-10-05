import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { expect, test, type Locator, type Page, type Response, type TestInfo } from "@playwright/test";
import type { Project, Review } from "../components/admin-video-review-card";
import vps from "../lib/video-vps-messages/zh-TW.json" with { type: "json" };
import admin from "../messages/zh-TW/admin.json" with { type: "json" };
import { pretendSignedIn } from "./session";

// Isolated acceptance of the VPS uploader settings card (docs/videos/vps-web-settings-acceptance).
// The card's own reads, saves and connection tests cross the real Next BFF to the synthetic store
// in tools/e2e-runtime-api.mjs; nothing reaches a VPS, Google or a real channel, and every URL,
// channel ID and secret below is made up for this file.
test.use({ trace: "retain-on-failure" });

const settingsApi = "/api/travel/admin/video-youtube/vps/settings";
const settingsPage = "/zh-TW/admin/videos?tab=settings#youtube-vps-settings";
const secret = "synthetic-e2e-secret-not-real-0000000000";
const nextSecret = "synthetic-e2e-secret-not-real-1111111111";
const serviceUrl = "http://127.0.0.1:18781";
const desktopUrl = "http://127.0.0.1:16080/vnc.html";
const otherDesktopUrl = "http://127.0.0.1:16081/vnc.html";
// The fixture's connection test "reaches" only the first channel; the second is a typo of it.
const channel = "UCSyntheticFixture000001";
const mistypedChannel = "UCSyntheticFixture000002";
const editedChannel = "UCSyntheticFixture000003";
// Set only when refreshing the committed receipt; CI keeps its screenshots under test-results.
const receipt = process.env.VPS_ACCEPTANCE_DIR;

const slug = "vps-settings-fixture";
const approved: Review = {
  id: "synthetic-vps-settings-package", gate: "publish", status: "approved", content_sha256: "a".repeat(64), summary: "Synthetic approved package",
  payload: { zh: { title: "Synthetic VPS settings video", description: "Synthetic description" } }, files: [],
  choice: null, note: null, created_at: "2026-10-05T00:00:00Z", decided_at: "2026-10-05T00:00:00Z",
};
const project: Project = {
  slug, title: "Synthetic VPS settings validation", stage: "publish", checklist: [], pending: 0, youtube_video_id: null,
  last_synced_at: "2026-10-05T00:00:00Z", publish_approved_at: "2026-10-05T00:00:00Z", reviews: [approved], youtube_sync: null,
};
const connection = {
  configured: true, linked: true, audited: false, channel_id: "synthetic-channel", channel_title: "Synthetic channel",
  client_id: null, client_secret_set: false, redirect_uri: "", scope: "", channel_url: null, linked_at: null, verified_at: null, problem: null,
};

type Exchange = { method: string; path: string; status: number; sent: Record<string, unknown> | null; received: Record<string, unknown> | null };

async function fixture(page: Page, baseURL: string | undefined, info: TestInfo) {
  const origin = new URL(baseURL || "http://127.0.0.1:3000").origin;
  expect(["127.0.0.1", "localhost"]).toContain(new URL(origin).hostname);
  // One store per test and attempt in the runtime fixture, so parallel projects never share a revision.
  const key = `${info.project.name}-${info.testId}-${info.retry}`;
  const store = `${settingsApi}?fixture=${encodeURIComponent(key)}`;
  const writes: string[] = [], external: string[] = [], errors: string[] = [], exchanges: Exchange[] = [];
  const bodies: Promise<unknown>[] = [], texts: string[] = [];
  /** What a settings exchange carried, for the receipt: the secret is a field name there, never a value. */
  const record = (response: Response, path: string, body: Promise<string>) => {
    const request = response.request();
    const sent = request.method() === "PUT" ? request.postDataJSON() as Record<string, unknown> : null;
    const exchange: Exchange = {
      method: request.method(), path, status: response.status(),
      sent: sent && Object.fromEntries(Object.entries(sent).map(([name, value]) => [name, name === "secret" ? "<synthetic secret>" : value])),
      received: null,
    };
    exchanges.push(exchange);
    return body.then((text) => {
      try {
        const received = JSON.parse(text) as Record<string, unknown>;
        exchange.received = Object.fromEntries(["code", "enabled", "configured", "secret_set", "source", "updated_at", "last_test_status", "browser_status", "active_jobs"]
          .filter((name) => name in received).map((name) => [name, received[name]]));
      } catch { /* not JSON: recorded as null */ }
    });
  };
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("response", (response) => {
    const url = new URL(response.url());
    // Every administrator API answer the page reads, where a saved secret could leak.
    if (url.origin !== origin || !url.pathname.startsWith("/api/travel/admin/")) return;
    const body = response.text().catch(() => "");
    bodies.push(body.then((text) => texts.push(text)));
    if (url.pathname === settingsApi || url.pathname === `${settingsApi}/test`) bodies.push(record(response, url.pathname, body));
  });
  await page.context().route("**/*", async (route) => {
    const request = route.request(), url = new URL(request.url());
    if (url.origin !== origin) {
      // The saved desktop link opens a new tab; answer that loopback page here, never a real desktop.
      if ([desktopUrl, otherDesktopUrl].includes(url.href)) {
        return route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Synthetic remote desktop</title><p>Synthetic remote desktop fixture</p>" });
      }
      external.push(url.origin + url.pathname);
      return route.abort("blockedbyclient");
    }
    if (!url.pathname.startsWith("/api/")) return route.fallback();
    if (url.pathname === settingsApi || url.pathname === `${settingsApi}/test`) {
      if (request.method() !== "GET") writes.push(`${request.method()} ${url.pathname}`);
      url.searchParams.set("fixture", key);
      return route.continue({ url: url.href });
    }
    if (request.method() !== "GET") {
      writes.push(`${request.method()} ${url.pathname}`);
      return route.fulfill({ status: 403, json: { code: "unexpected_fixture_write" } });
    }
    const path = url.pathname.replace("/api/travel", "");
    if (path === "/admin/video-youtube") return route.fulfill({ json: connection });
    // The automation settings below the card are another page section with its own tests; the
    // runtime fixture's Shorts-sized answer would crash it, so it shows its load error here.
    if (path === "/admin/video-automation/settings") return route.fulfill({ status: 503, json: { code: "fixture_not_covered", detail: "Synthetic fixture: outside this acceptance" } });
    if (path === `/admin/videos/${slug}`) return route.fulfill({ json: project });
    if (path === `/admin/videos/${slug}/youtube/vps`) return route.fulfill({ json: { configured: false, linked: false, job: null } });
    return route.fallback();
  });
  /** Another administrator's save, through the same BFF and store the card uses. */
  const otherAdminSaves = async (changes: Record<string, unknown>) => {
    const current = await page.request.get(store);
    expect(current.status()).toBe(200);
    const { updated_at } = await current.json() as { updated_at: string | null };
    const saved = await page.request.put(store, { headers: { Origin: origin }, data: { expected_updated_at: updated_at, ...changes } });
    expect(saved.status()).toBe(200);
    expect(await saved.text()).not.toContain(secret);
    return await saved.json() as { updated_at: string };
  };
  /** Another administrator's connection test of the saved settings. */
  const otherAdminTests = async () => {
    const tested = await page.request.post(`${settingsApi}/test?fixture=${encodeURIComponent(key)}`, { headers: { Origin: origin }, data: {} });
    expect(tested.status()).toBe(200);
    return await tested.json() as { last_test_status: string | null };
  };
  const finish = async (name: string) => {
    await Promise.all(bodies);
    expect(texts.length).toBeGreaterThan(0);
    for (const text of texts) {
      expect(text).not.toContain(secret);
      expect(text).not.toContain(nextSecret);
    }
    expect(await page.content()).not.toContain(secret);
    expect(external).toEqual([]);
    expect(errors).toEqual([]);
    if (receipt) {
      const file = join(receipt, `observed-requests-${info.project.name}.json`);
      const previous = await readFile(file, "utf8").then((text) => JSON.parse(text) as Record<string, unknown>).catch(() => ({}));
      await writeFile(file, JSON.stringify({ ...previous, [name]: exchanges }, null, 2) + "\n");
    }
  };
  return { origin, store, writes, otherAdminSaves, otherAdminTests, finish };
}

/** Open the settings tab and wait for the card's own read, not for a fixed time. */
async function openSettings(page: Page) {
  const loaded = page.waitForResponse((response) => new URL(response.url()).pathname === settingsApi && response.request().method() === "GET");
  await page.goto(settingsPage);
  expect((await loaded).status()).toBe(200);
  const card = page.getByRole("region", { name: vps.title, exact: true });
  await expect(card.getByRole("checkbox", { name: vps.enabled })).toBeVisible();
  return card;
}

const fields = (card: Locator) => ({
  enabled: card.getByRole("checkbox", { name: vps.enabled }),
  url: card.getByRole("textbox", { name: vps.url, exact: true }),
  channel: card.getByRole("textbox", { name: vps.channel, exact: true }),
  secret: card.getByLabel(vps.secret, { exact: true }),
  desktop: card.getByRole("textbox", { name: vps.desktop, exact: true }),
  save: card.getByRole("button", { name: vps.save, exact: true }),
  test: card.getByRole("button", { name: vps.test, exact: true }),
  refresh: card.getByRole("button", { name: vps.refresh, exact: true }),
});

/** Wait for the one settings request an action sends, and answer what it carried and got back. */
async function send(page: Page, method: "PUT" | "POST" | "GET", action: () => Promise<void>) {
  const answered = page.waitForResponse((response) => new URL(response.url()).pathname.startsWith(settingsApi) && response.request().method() === method);
  await action();
  const response = await answered;
  const received = await response.json() as { updated_at?: string | null };
  return { status: response.status(), sent: method === "PUT" ? response.request().postDataJSON() as Record<string, unknown> : null, received };
}

/** No page or card overflow and nothing cut at the card's edges, in light and dark. */
async function inspect(page: Page, card: Locator, info: TestInfo, name?: string) {
  for (const theme of ["light", "dark"] as const) {
    await page.emulateMedia({ colorScheme: theme, reducedMotion: "reduce" });
    await page.evaluate((value) => { document.documentElement.dataset.theme = value; }, theme);
    expect(await page.locator("html").evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
    expect(await card.evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
    const clipped = await card.evaluate((node) => {
      const box = node.getBoundingClientRect();
      return [...node.querySelectorAll("h2, p, label, input, button, a")].filter((child) => {
        const rect = child.getBoundingClientRect();
        // A text field scrolls its own value; anything else wider than its box is cut off.
        const cut = child.tagName !== "INPUT" && child.scrollWidth > child.clientWidth + 1 && getComputedStyle(child).overflowX !== "visible";
        return rect.width > 0 && (rect.left < box.left - 1 || rect.right > box.right + 1 || cut);
      }).map((child) => child.outerHTML.slice(0, 120));
    });
    expect(clipped).toEqual([]);
    if (name) {
      const dir = receipt ?? info.outputPath();
      await mkdir(dir, { recursive: true });
      // A clip of the full page from its top, not an element shot: the sticky admin header sits at
      // the scroll position, and a scrolled capture paints it over the middle of the card.
      const clip = await card.evaluate((node) => {
        window.scrollTo(0, 0);
        const rect = node.getBoundingClientRect();
        return { x: rect.left + window.scrollX, y: rect.top + window.scrollY, width: rect.width, height: rect.height };
      });
      await page.screenshot({ path: join(dir, `youtube-vps-settings-${info.project.name}-${name}-${theme}.jpg`), fullPage: true, clip, type: "jpeg", quality: 70, scale: "css", animations: "disabled" });
    }
  }
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });
  await page.evaluate(() => { document.documentElement.dataset.theme = "light"; });
}

test("an owner saves and reloads the VPS settings through the BFF, and the secret stays on the server", async ({ page, baseURL }, info) => {
  // Two full server renders of an admin page (the visit and the reload), and the first case a worker runs.
  test.setTimeout(60_000);
  const state = await fixture(page, baseURL, info);
  await pretendSignedIn(page);
  let card = await openSettings(page);
  let form = fields(card);
  await expect(card.getByText(vps.disabled, { exact: true })).toBeVisible();
  await expect(card.getByText(`${vps.source}: ${vps.sourceNone}`, { exact: true })).toBeVisible();
  await expect(form.test).toBeDisabled();
  await inspect(page, card, info);

  await form.enabled.check();
  await form.url.fill(serviceUrl);
  await form.channel.fill(mistypedChannel);
  await form.secret.fill(secret);
  await form.desktop.fill(desktopUrl);
  await expect(form.test).toBeDisabled();
  await expect(card.getByText(vps.saveBeforeTest, { exact: true })).toBeVisible();
  const first = await send(page, "PUT", () => form.save.click());
  expect(first.status).toBe(200);
  expect(first.sent).toEqual({ enabled: true, url: serviceUrl, channel_id: mistypedChannel, desktop_url: desktopUrl, secret, expected_updated_at: null });
  expect(first.received).toMatchObject({ secret_set: true, configured: true });
  expect(first.received).not.toHaveProperty("secret");
  await expect(card.getByText(vps.saved, { exact: true })).toBeVisible();
  await expect(form.secret).toHaveValue("");
  await expect(form.secret).toHaveAttribute("placeholder", vps.secretKept);
  await expect(card.getByText(vps.configured, { exact: true })).toBeVisible();
  expect(await page.content()).not.toContain(secret);

  // A reload reads the saved fields back; the secret stays on the server.
  const reread = page.waitForResponse((response) => new URL(response.url()).pathname === settingsApi);
  await page.reload();
  await reread;
  card = page.getByRole("region", { name: vps.title, exact: true });
  form = fields(card);
  await expect(form.url).toHaveValue(serviceUrl);
  await expect(form.channel).toHaveValue(mistypedChannel);
  await expect(form.desktop).toHaveValue(desktopUrl);
  await expect(form.enabled).toBeChecked();
  await expect(form.secret).toHaveValue("");
  await expect(form.secret).toHaveAttribute("placeholder", vps.secretKept);
  await expect(card.getByText(`${vps.source}: ${vps.sourceDatabase}`, { exact: true })).toBeVisible();
  expect(await page.content()).not.toContain(secret);
  expect(state.writes).toEqual([`PUT ${settingsApi}`]);
  await state.finish("save and reload");
});

test("a connection test fails on a mistyped channel and passes once it is corrected", async ({ page, baseURL }, info) => {
  const state = await fixture(page, baseURL, info);
  await pretendSignedIn(page);
  await state.otherAdminSaves({ enabled: true, url: serviceUrl, channel_id: mistypedChannel, desktop_url: desktopUrl, secret });
  const card = await openSettings(page);
  const form = fields(card);
  await expect(card.getByText(vps.notTested, { exact: true })).toBeVisible();

  // The mistyped channel fails the test; correcting it saves only that field, at the revision the test left.
  const failed = await send(page, "POST", () => form.test.click());
  expect(failed.status).toBe(200);
  await expect(card.getByRole("alert").filter({ hasText: vps.testFailed })).toBeVisible();
  await expect(card.getByText("VPS 設定的頻道與網站不同，請先核對", { exact: true })).toBeVisible();
  await form.channel.fill(channel);
  await expect(form.test).toBeDisabled();
  const corrected = await send(page, "PUT", () => form.save.click());
  expect(corrected.status).toBe(200);
  expect(corrected.sent).toEqual({ channel_id: channel, expected_updated_at: failed.received.updated_at });
  await expect(card.getByText(vps.saved, { exact: true })).toBeVisible();
  await expect(card.getByText(vps.notTested, { exact: true })).toBeVisible();
  expect((await send(page, "POST", () => form.test.click())).status).toBe(200);
  await expect(card.getByRole("status").filter({ hasText: vps.testSuccess })).toBeVisible();
  await expect(card.getByText(`${vps.browser}: ${vps.browserIdle}`, { exact: true })).toBeVisible();
  await expect(card.getByText(`${vps.activeJobs}: 0`, { exact: true })).toBeVisible();
  await expect(card.getByText(vps.lastTest, { exact: false })).toBeVisible();

  // The saved desktop link opens that loopback desktop in a new tab.
  const link = card.getByRole("link", { name: vps.openDesktop });
  await expect(link).toHaveAttribute("href", desktopUrl);
  await expect(link).toHaveAttribute("target", "_blank");
  await expect(link).toHaveAttribute("rel", /noopener/);
  const opened = page.context().waitForEvent("page");
  await link.click();
  const desktop = await opened;
  await desktop.waitForLoadState();
  expect(desktop.url()).toBe(desktopUrl);
  await expect(desktop).toHaveTitle("Synthetic remote desktop");
  await desktop.close();

  expect(state.writes).toEqual([`POST ${settingsApi}/test`, `PUT ${settingsApi}`, `POST ${settingsApi}/test`]);
  await state.finish("connection test and desktop link");
});

test("a configured and tested card fits desktop and mobile in light and dark", async ({ page, baseURL }, info) => {
  const state = await fixture(page, baseURL, info);
  await pretendSignedIn(page);
  await state.otherAdminSaves({ enabled: true, url: serviceUrl, channel_id: channel, desktop_url: desktopUrl, secret });
  expect((await state.otherAdminTests()).last_test_status).toBe("success");
  const card = await openSettings(page);
  await expect(card.getByRole("status").filter({ hasText: vps.testSuccess })).toBeVisible();
  await expect(card.getByRole("link", { name: vps.openDesktop })).toBeVisible();
  await expect(fields(card).secret).toHaveAttribute("placeholder", vps.secretKept);
  // The screenshots are the visual evidence: CI keeps them as an artifact, VPS_ACCEPTANCE_DIR the receipt.
  await inspect(page, card, info, "tested");
  expect(state.writes).toEqual([]);
  await state.finish("layout");
});

test("a stale save keeps the edits, and the retry sends only them at the new revision", async ({ page, baseURL }, info) => {
  const state = await fixture(page, baseURL, info);
  await pretendSignedIn(page);
  await state.otherAdminSaves({ enabled: true, url: serviceUrl, channel_id: channel, desktop_url: desktopUrl, secret });
  const card = await openSettings(page);
  const form = fields(card);
  await expect(form.desktop).toHaveValue(desktopUrl);

  // Another administrator changes the desktop address while this page still shows the old revision.
  const latest = await state.otherAdminSaves({ desktop_url: otherDesktopUrl });
  await form.channel.fill(editedChannel);
  await form.secret.fill(nextSecret);
  expect((await send(page, "PUT", () => form.save.click())).status).toBe(409);
  await expect(card.getByRole("alert").filter({ hasText: vps.conflict })).toBeVisible();
  await expect(form.channel).toHaveValue(editedChannel);
  await expect(form.secret).toHaveValue(nextSecret);
  await expect(form.desktop).toHaveValue(desktopUrl);

  // Reading again takes the other administrator's desktop address and keeps this page's edits.
  expect((await send(page, "GET", () => form.refresh.click())).status).toBe(200);
  await expect(card.getByText(vps.refreshed, { exact: true })).toBeVisible();
  await expect(form.desktop).toHaveValue(otherDesktopUrl);
  await expect(form.channel).toHaveValue(editedChannel);
  await expect(form.secret).toHaveValue(nextSecret);
  const retried = await send(page, "PUT", () => form.save.click());
  expect(retried.status).toBe(200);
  expect(retried.sent).toEqual({ channel_id: editedChannel, secret: nextSecret, expected_updated_at: latest.updated_at });
  await expect(card.getByText(vps.saved, { exact: true })).toBeVisible();
  await expect(form.secret).toHaveValue("");
  await expect(card.getByRole("link", { name: vps.openDesktop })).toHaveAttribute("href", otherDesktopUrl);

  const saved = await page.request.get(state.store);
  const text = await saved.text();
  expect(text).not.toContain(nextSecret);
  expect(JSON.parse(text)).toMatchObject({ channel_id: editedChannel, desktop_url: otherDesktopUrl, url: serviceUrl, secret_set: true });
  expect(state.writes).toEqual([`PUT ${settingsApi}`, `PUT ${settingsApi}`]);
  await state.finish("stale write recovery");
});

test("a read-only administrator can read and refresh but not save or test", async ({ page, baseURL }, info) => {
  const state = await fixture(page, baseURL, info);
  await pretendSignedIn(page);
  await state.otherAdminSaves({ enabled: true, url: serviceUrl, channel_id: channel, desktop_url: desktopUrl, secret });
  // The viewer role reads videos but has no settings.manage (tools/e2e-runtime-api.mjs adminCapabilities).
  await page.context().clearCookies();
  await page.context().addCookies([{ name: "travel_access", value: "e2e-viewer", url: state.origin }]);
  const card = await openSettings(page);
  const form = fields(card);
  await expect(card.getByRole("note").filter({ hasText: vps.readOnly })).toBeVisible();
  await expect(form.channel).toHaveValue(channel);
  for (const control of [form.enabled, form.url, form.channel, form.secret, form.desktop, form.save, form.test]) await expect(control).toBeDisabled();
  await expect(card.getByRole("link", { name: vps.openDesktop })).toHaveAttribute("href", desktopUrl);
  expect((await send(page, "GET", () => form.refresh.click())).status).toBe(200);
  await expect(card.getByText(vps.refreshed, { exact: true })).toBeVisible();
  expect(state.writes).toEqual([]);
  await state.finish("read-only");
});

test("an unconfigured uploader links to the VPS settings card", async ({ page, baseURL }, info) => {
  // Two full server renders: the video's page, then the settings tab the link opens.
  test.setTimeout(60_000);
  const state = await fixture(page, baseURL, info);
  await pretendSignedIn(page);
  await page.goto(`/zh-TW/admin/videos?video=${slug}`);
  await expect(page.getByRole("heading", { name: project.title, exact: true })).toBeVisible();
  await page.getByRole("button", { name: admin.videoYoutube.vps.open, exact: true }).first().click();
  const uploader = page.getByRole("region", { name: admin.videoYoutube.vps.title, exact: true });
  await expect(uploader.getByText(admin.videoYoutube.vps.notConfigured, { exact: true })).toBeVisible();
  const link = uploader.getByRole("link", { name: vps.settingsLink, exact: true });
  await expect(link).toHaveAttribute("href", settingsPage);
  const loaded = page.waitForResponse((response) => new URL(response.url()).pathname === settingsApi && response.request().method() === "GET");
  await link.click();
  await loaded;
  await expect(page).toHaveURL((url) => url.pathname === "/zh-TW/admin/videos" && url.search === "?tab=settings" && url.hash === "#youtube-vps-settings");
  const card = page.getByRole("region", { name: vps.title, exact: true });
  await expect(card.getByRole("checkbox", { name: vps.enabled })).toBeVisible();
  await expect(card.getByRole("heading", { name: vps.title })).toBeInViewport();
  expect(state.writes).toEqual([]);
  await state.finish("uploader settings link");
});
