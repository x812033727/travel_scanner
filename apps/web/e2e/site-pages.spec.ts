import { expect, test, type Page } from "@playwright/test";
import type { SitePageDetail, SitePageDocument } from "../lib/site-pages";

// Loopback SSR and browser fixtures only; these are not real published policies.
for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
  test(`public information ${locale}: SSR metadata matches the published document`, async ({ page, baseURL }) => {
    expect(new URL(baseURL!).hostname).toMatch(/^(127\.0\.0\.1|localhost)$/);
    await page.goto(`/${locale}/privacy`);
    await expect(page.getByRole("heading", { name: `Synthetic privacy (${locale})` })).toBeVisible();
    await expect(page).toHaveTitle(new RegExp(`Synthetic privacy \\(${locale}\\)`));
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", `Synthetic published summary (${locale})`);
    await expect(page.getByText(`Synthetic public content (${locale}). Not a real policy.`)).toBeVisible();
    await expect(page.locator("html")).toHaveAttribute("lang", locale);
  });
}

test("public information distinguishes unpublished content from an unavailable service", async ({ page }) => {
  await page.goto("/en/terms");
  await expect(page.getByRole("status")).toContainText("will be published after confirmation");
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", /noindex/);
  await page.goto("/en/about");
  await expect(page.getByRole("main").getByRole("alert")).toContainText("temporarily unavailable");
  await expect(page.getByText(/Synthetic public content/)).toHaveCount(0);
});

const document: SitePageDocument = {
  title: "Synthetic draft", description: "Synthetic description", effective_date: "2026-09-09",
  blocks: [{ type: "paragraph", text: "Synthetic draft body. Not a legal document." }],
  requirements: { operator: "Fixture operator", location: "Fixture location", contact: "fixture@example.test", retention: "Fixture retention", legal: "Fixture legal" },
};

async function adminFixtures(page: Page, baseURL: string, role = "operations", session?: { locale: string; ready: Promise<void> }) {
  const origin = new URL(baseURL);
  expect(origin.hostname).toMatch(/^(127\.0\.0\.1|localhost)$/);
  await page.context().addCookies([{ name: "travel_access", value: `e2e-${role}`, url: origin.origin }]);
  let state: SitePageDetail = { slug: "privacy", locale: "en", version: 1, draft: structuredClone(document), published: null, pending_requirements: [], revisions: [{ id: "fixture-r1", version: 1, action: "initialized", created_at: "2026-09-09T00:00:00Z", created_by_user_id: "fixture-actor" }], audit: [] };
  const writes: Array<{ path: string; body: Record<string, unknown> }> = [];
  await page.route("**/api/travel/**", async (route) => {
    const url = new URL(route.request().url()), path = url.pathname.replace("/api/travel", "");
    const method = route.request().method();
    if (path === "/auth/me" && method === "GET") {
      const response = await route.fetch();
      if (session) await session.ready;
      return route.fulfill({ response, json: { ...await response.json(), preferred_locale: session?.locale || "en" } });
    }
    if (path.startsWith("/admin/site-pages/")) {
      const body = method === "GET" ? {} : route.request().postDataJSON();
      if (method !== "GET") writes.push({ path, body });
      if (path.includes("/revisions/")) return route.fulfill({ json: { ...state.revisions[0], document } });
      if (path.endsWith("/draft")) state = { ...state, version: state.version + 1, draft: body.document };
      if (path.endsWith("/publish")) state = { ...state, version: state.version + 1, published: { ...state.draft, version: state.version + 1, published_at: "2026-09-09T00:00:00Z" } };
      if (path.endsWith("/restore")) state = { ...state, version: state.version + 1, draft: structuredClone(document) };
      return route.fulfill({ json: state });
    }
    if (method !== "GET") return route.fulfill({ status: 405, json: { code: "fixture_write_blocked" } });
    return route.fallback();
  });
  return writes;
}

test("administrator can preview, explicitly publish and restore only a draft", async ({ page, baseURL }, info) => {
  const writes = await adminFixtures(page, baseURL!);
  await page.goto("/en/admin/site-pages");
  const main = page.getByRole("main");
  await expect(main.getByRole("heading", { name: "Site information" })).toBeVisible();
  await main.getByRole("textbox", { name: "Document title", exact: true }).fill("Updated synthetic draft");
  await main.getByRole("button", { name: "Preview", exact: true }).click();
  await expect(page.getByRole("dialog").getByRole("heading", { name: "Updated synthetic draft" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await main.getByRole("button", { name: "Save draft", exact: true }).click();
  await expect(main.getByRole("status")).toContainText("Draft saved");
  expect(writes).toHaveLength(1);
  await main.getByRole("button", { name: "Publish", exact: true }).click();
  const dialog = page.getByRole("dialog", { name: "Confirm publication" });
  await expect(dialog.getByRole("button", { name: "Confirm publication" })).toBeDisabled();
  await dialog.getByRole("textbox", { name: "Reason for change" }).fill("Verified isolated fixture");
  await dialog.getByRole("checkbox").check();
  await dialog.getByRole("button", { name: "Confirm publication" }).click();
  await expect(dialog).toHaveCount(0);
  expect(writes.at(-1)?.body).toMatchObject({ expected_version: 2, confirmed: true });
  await main.getByRole("textbox", { name: "Reason for change" }).fill("Restore isolated fixture");
  page.once("dialog", (prompt) => prompt.accept());
  await main.getByRole("button", { name: "Restore as draft", exact: true }).click();
  await expect(main.getByRole("textbox", { name: "Document title", exact: true })).toHaveValue(document.title);
  await expect(main.getByRole("status")).toContainText("Restored as a new unpublished draft");
  expect(writes.filter((entry) => entry.path.endsWith("/publish"))).toHaveLength(1);
  await page.screenshot({ path: info.outputPath("synthetic-site-pages-editor.png"), fullPage: false });
});

test("dirty information drafts survive a cancelled browser Back and language switch", async ({ page, baseURL }) => {
  const writes = await adminFixtures(page, baseURL!);
  await page.goto("/en/my");
  await page.goto("/en/admin/site-pages");
  const field = page.getByRole("textbox", { name: "Document title", exact: true });
  await field.fill("Keep this unsaved draft");
  page.once("dialog", (prompt) => prompt.dismiss());
  await page.goBack();
  await expect(page).toHaveURL(/\/en\/admin\/site-pages$/);
  await expect(field).toHaveValue("Keep this unsaved draft");
  page.once("dialog", (prompt) => prompt.dismiss());
  await page.getByRole("combobox", { name: "Language", exact: true }).selectOption("ja");
  await expect(page).toHaveURL(/\/en\/admin\/site-pages$/);
  await expect(field).toHaveValue("Keep this unsaved draft");
  expect(writes).toHaveLength(0);
});

test("read-only administrator cannot edit information documents", async ({ page, baseURL }) => {
  const writes = await adminFixtures(page, baseURL!, "viewer");
  await page.goto("/en/admin/site-pages");
  await expect(page.getByRole("textbox", { name: "Document title", exact: true })).toBeDisabled();
  await expect(page.getByRole("button", { name: "Publish", exact: true })).toBeDisabled();
  await expect(page.getByRole("button", { name: "Preview", exact: true })).toBeEnabled();
  expect(writes).toHaveLength(0);
});

test("a delayed account language preference cannot discard a document draft", async ({ page, baseURL }) => {
  let releaseSession!: () => void;
  const ready = new Promise<void>((resolve) => { releaseSession = resolve; });
  const writes = await adminFixtures(page, baseURL!, "operations", { locale: "ja", ready });
  await page.goto("/en/admin/site-pages");
  const field = page.getByRole("textbox", { name: "Document title", exact: true });
  await field.fill("Retain draft while login preferences load");
  await expect(page.getByRole("button", { name: "Save draft", exact: true })).toBeEnabled();
  const confirmation = page.waitForEvent("dialog");
  releaseSession();
  await (await confirmation).dismiss();
  await expect(field).toHaveValue("Retain draft while login preferences load");
  await expect(page).toHaveURL(/\/en\/admin\/site-pages$/);
  const cookie = (await page.context().cookies()).find((entry) => entry.name === "travel_locale");
  expect(cookie?.value).not.toBe("ja");
  expect(writes).toHaveLength(0);
});

for (const cancel of [false, true]) {
  test(`jumping back across the draft history guard ${cancel ? "can be cancelled without losing edits" : "honours the selected destination"}`, async ({ page, baseURL, isMobile }) => {
    const writes = await adminFixtures(page, baseURL!);
    const sessionReady = page.waitForResponse((response) => new URL(response.url()).pathname === "/api/travel/auth/me" && response.request().method() === "GET");
    await page.goto("/en/admin/settings");
    await sessionReady;
    const documentStarted = await page.evaluate(() => performance.timeOrigin);
    // Use real Next links so all three entries share a document. Separate goto()
    // loads would exercise beforeunload instead of the SPA popstate guard.
    for (const name of ["Operations overview", "Site information"]) {
      if (isMobile) await page.getByRole("button", { name: "Open operations menu", exact: true }).click();
      await page.getByRole("navigation", { name: "Operations console", exact: true }).getByRole("link", { name, exact: true }).click();
      await expect(page).toHaveURL(name === "Operations overview" ? /\/en\/admin$/ : /\/en\/admin\/site-pages$/);
    }
    expect(await page.evaluate(() => performance.timeOrigin), "history entries must remain in the same document").toBe(documentStarted);
    const field = page.getByRole("textbox", { name: "Document title", exact: true });
    await field.fill("Keep the selected history destination");
    await expect(page.getByRole("button", { name: "Save draft", exact: true })).toBeEnabled();
    await expect.poll(() => page.evaluate(() => Boolean(window.history.state?.mokaairNavigationGuard))).toBe(true);
    const confirmation = page.waitForEvent("dialog");
    // Native multi-entry traversal models choosing the preceding page in the browser's Back menu.
    await page.evaluate(() => window.history.go(-2));
    const prompt = await confirmation;
    if (cancel) {
      await prompt.dismiss();
      await expect(page).toHaveURL(/\/en\/admin\/site-pages$/);
      await expect(field).toHaveValue("Keep the selected history destination");
      page.once("dialog", (nextPrompt) => nextPrompt.accept());
      await page.goBack();
    } else await prompt.accept();
    await expect(page).toHaveURL(/\/en\/admin$/);
    expect(writes).toHaveLength(0);
  });
}
