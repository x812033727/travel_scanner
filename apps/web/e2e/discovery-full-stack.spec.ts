import { expect, request, test, type APIRequestContext, type Page } from "@playwright/test";
import { getDiscoveryCopy } from "../lib/discovery-copy";

// Ordinary production paths against isolated PostgreSQL/Redis/Mailpit. No route
// interception, injected tokens, paid-provider requests or production credentials.
test.skip(process.env.DISCOVERY_E2E !== "1", "Requires the isolated discovery acceptance stack");
const origin = new URL(process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000").origin;
async function json(client: APIRequestContext, method: string, path: string, data?: unknown) {
  const response = await client.fetch(`/api/travel${path}`, { method, data, headers: { Origin: origin, "X-Travel-Locale": "en" } });
  expect(response.ok(), `${method} ${path}: ${await response.text()}`).toBeTruthy();
  return response.status() === 204 ? null : response.json();
}
async function verifyMail(page: Page, email: string) {
  await json(page.request, "POST", "/auth/request-verification");
  let verification = "";
  await expect.poll(async () => {
    const messages = await page.request.get(`http://127.0.0.1:8025/api/v1/search?query=${encodeURIComponent(`to:${email}`)}`);
    const id = (await messages.json()).messages?.[0]?.ID;
    if (!id) return false;
    const mail = await page.request.get(`http://127.0.0.1:8025/api/v1/message/${id}`);
    verification = (await mail.json()).Text.match(/https?:\/\/[^\s]+#token=[A-Za-z0-9_-]+/)?.[0] || "";
    return Boolean(verification) && new URL(verification).searchParams.get("purpose") === "verify";
  }, { timeout: 45_000, intervals: [500, 1000, 2000] }).toBe(true);
  const url = new URL(verification);
  await page.goto(url.pathname + url.search + url.hash);
  // Account links use the member's ordinary locale (default Traditional Chinese).
  await page.getByRole("button", { name: /^(確認|Confirm)$/ }).click();
  await expect.poll(async () => (await json(page.request, "GET", "/auth/me")).email_verified).toBe(true);
}

test("reviewed story discovery, private collections and preferences survive reload and withdrawal", async ({ page, browser, baseURL }, info) => {
  test.setTimeout(240_000);
  const c = getDiscoveryCopy("en");
  const admin = await request.newContext({ baseURL, extraHTTPHeaders: { Origin: origin } });
  const guest = await browser.newContext({ baseURL, viewport: info.project.use.viewport, isMobile: info.project.use.isMobile });
  try {
    await json(admin, "POST", "/auth/login", { email: "discovery-admin@example.com", password: "discovery-ci-password-123" });
    expect((await json(admin, "GET", "/discovery/status")).enabled).toBe(true);
    const community = await json(admin, "GET", "/admin/community/settings");
    if (!community.settings.enabled) await json(admin, "PUT", "/admin/community/settings", { settings: { ...community.settings, enabled: true }, reason: "Isolated discovery browser acceptance" });
    const suffix = `${Date.now()}${info.workerIndex}`;
    const handle = `discovery${suffix}`;
    const email = `${handle}@example.com`;
    await json(page.request, "POST", "/auth/register", { email, password: "discovery-member-password-123", preferred_locale: "en" });
    await verifyMail(page, email);
    const user = await json(page.request, "GET", "/auth/me");
    await json(page.request, "PUT", "/community/me", { handle, display_name: `Discovery tester ${suffix}`, languages: ["en"], destinations: ["Tokyo"] });

    const title = `Tokyo discovery test ${suffix}`;
    const draft = await json(page.request, "POST", "/community/posts", { title, body: "An isolated acceptance story. This is test content, not a travel recommendation.", locale: "en", destination: "Tokyo", kind: "story", topics: ["culture"], video_refs: [{ provider: "youtube", video_id: "dQw4w9WgXcQ" }] });
    const denied = await page.request.post(`/api/travel/community/posts/${draft.id}/publish`, { data: { version: draft.version }, headers: { Origin: origin } });
    expect(denied.status()).toBe(403);
    await json(admin, "PUT", `/admin/community/creator-invitations/${user.id}`, { version: 0, invited: true, reason: "Invited isolated acceptance creator" });
    const pending = await json(page.request, "POST", `/community/posts/${draft.id}/publish`, { version: draft.version });
    expect(pending.state).toBe("pending");
    const searchPath = `/discovery/search?q=${encodeURIComponent(title)}&type=post&locale=en`;
    expect((await json(guest.request, "GET", searchPath)).items).toHaveLength(0);
    await json(admin, "PUT", `/admin/community/posts/${draft.id}`, { action: "approve", version: pending.version, reason: "Reviewed isolated source and privacy boundaries" });
    const published = await json(guest.request, "GET", `/community/posts/${draft.id}`);
    expect(published.video_refs[0]).toMatchObject({ video_id: "dQw4w9WgXcQ", status: "link_only", source_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", embed_url: null });

    const visitor = await guest.newPage();
    await visitor.goto(`/en/explore?q=${encodeURIComponent(title)}&type=post&locale=en`);
    await expect(visitor.getByRole("button", { name: title, exact: true })).toBeVisible();
    await visitor.getByRole("button", { name: title, exact: true }).click();
    await expect(visitor.getByRole("dialog", { name: title })).toBeVisible();
    await expect(visitor.getByRole("dialog", { name: title }).getByRole("link", { name: c.source, exact: true })).toHaveAttribute("href", "https://www.youtube.com/watch?v=dQw4w9WgXcQ");
    await expect(visitor.locator("iframe")).toHaveCount(0); // No provider evidence/key: link-only.

    await page.goto("/en/explore/collections");
    await page.getByLabel("New collection", { exact: true }).fill(`Saved trip ideas ${suffix}`);
    await page.getByRole("button", { name: "Create", exact: true }).click();
    await expect(page.getByRole("combobox", { name: "Collection", exact: true })).not.toHaveValue("");
    const collection = { id: await page.getByRole("combobox", { name: "Collection", exact: true }).inputValue(), name: `Saved trip ideas ${suffix}` };
    await json(page.request, "POST", `/discovery/collections/${collection.id}/items`, { kind: "post", id: draft.id });
    await json(page.request, "POST", `/discovery/collections/${collection.id}/items`, { kind: "post", id: draft.id });
    const saved = await json(page.request, "GET", `/discovery/collections/${collection.id}?locale=en`);
    expect(saved.items).toHaveLength(1);
    expect((await guest.request.get(`/api/travel/discovery/collections/${collection.id}`)).status()).toBe(401);
    await page.goto("/en/explore/collections");
    await expect(page.getByRole("heading", { name: c.collections, exact: true })).toBeVisible();
    await page.reload();
    await page.getByRole("combobox", { name: "Collection", exact: true }).selectOption(collection.id);
    await expect(page.getByRole("button", { name: title, exact: true })).toBeVisible();

    const current = await json(page.request, "GET", "/discovery/preferences");
    const interests = { ...current, destinations: ["Tokyo"], topics: ["culture"] };
    const updated = await json(page.request, "PUT", "/discovery/preferences", interests);
    expect(updated.version).toBeGreaterThan(current.version);
    const conflict = await page.request.put("/api/travel/discovery/preferences", { data: interests, headers: { Origin: origin } });
    expect(conflict.status()).toBe(409);
    await page.goto("/en/explore");
    await page.getByRole("button", { name: c.preferences, exact: true }).click();
    const dialog = page.getByRole("dialog", { name: c.preferences });
    await expect(dialog).toBeVisible();
    await expect(dialog).toContainText(c.preferenceHelp);
    await page.keyboard.press("Escape");
    await page.reload();
    expect((await json(page.request, "GET", "/discovery/preferences")).topics).toEqual(["culture"]);
    await page.screenshot({ path: info.outputPath("discovery-real-stack.png"), fullPage: true });

    await json(page.request, "POST", `/community/posts/${draft.id}/withdraw`);
    expect((await json(guest.request, "GET", searchPath)).items).toHaveLength(0);
    const invisible = await json(page.request, "GET", `/discovery/collections/${collection.id}?locale=en`);
    expect(invisible.items).toHaveLength(1);
    expect(invisible.items[0].unavailable).toBe(true);
    expect(invisible.items[0].discovery).toBeUndefined();
    await visitor.reload();
    await expect(visitor.getByRole("button", { name: title, exact: true })).toHaveCount(0);
  } finally {
    await guest.close(); await admin.dispose();
  }
});
