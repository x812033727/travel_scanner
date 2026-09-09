import { expect, test, type Page } from "@playwright/test";
import { getDiscoveryCopy } from "../lib/discovery-copy";
import type { DiscoveryItem, DiscoveryPreferences } from "../lib/discovery";

// Isolated UX fixtures only. No provider content, paid calls or production account.
const placeId = "10000000-0000-4000-8000-000000000001";
const videoId = "10000000-0000-4000-8000-000000000002";
const items: DiscoveryItem[] = [
  { id: `hotspot:${placeId}`, kind: "hotspot", title: "Tokyo riverside · test fixture", summary: "A reviewed fixture location for planning acceptance.", locale: "en", href: `/hotspots?hotspot=${placeId}`,
    destination: { id: "tokyo", name: "Tokyo", country_code: "JP" }, source: { label: "Fixture editorial", url: "https://example.com/source", kind: "editorial" },
    published_at: null, updated_at: "2026-09-01T00:00:00Z", thumbnail_url: null, recommendation_reason: "editorial",
    collection_ref: { kind: "hotspot", id: placeId } },
  { id: `video:${videoId}`, kind: "video", title: "Kyoto walk · video fixture", summary: "An embedded-player UX fixture, not a scraped travel recommendation.", locale: "en", href: "/hotspots",
    destination: { id: "osaka-kyoto", name: "Kyoto", country_code: "JP" }, source: { label: "Fixture creator", url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", kind: "editorial" },
    published_at: "2026-09-01T00:00:00Z", updated_at: "2026-09-01T00:00:00Z", thumbnail_url: null,
    collection_ref: { kind: "guide", id: videoId }, video: { provider: "youtube", video_id: "dQw4w9WgXcQ", source_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", status: "embeddable", embed_url: "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ" } },
];

async function fixtures(page: Page, options: { enabled?: boolean; authenticated?: boolean } = {}) {
  const writes: Array<{ path: string; body: Record<string, unknown> }> = [];
  let preferences: DiscoveryPreferences = { version: 0, destinations: [], topics: [], include_saved: true, include_following: true };
  const hidden = new Set<string>();
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request(); const url = new URL(request.url());
    const path = url.pathname.replace("/api/travel", "");
    const send = (body: unknown, status = 200) => route.fulfill({ status, contentType: "application/json", body: JSON.stringify(body) });
    if (path === "/discovery/status") return send({ enabled: options.enabled !== false });
    if (path === "/auth/me") return options.authenticated ? send({ id: "20000000-0000-4000-8000-000000000001", email: "fixture@example.test", email_verified: true }) : send({ code: "authentication_required" }, 401);
    if (path === "/community/status") return send({ enabled: false, posting_enabled: false, comments_enabled: false, messaging_enabled: false, translation_enabled: false, pet_reports_enabled: false });
    if (path === "/runtime/site-visibility") return send({ hotspots_enabled: true, trips_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true });
    if (path === "/analytics/config") return send({ first_party_enabled: false, ga4_enabled: false, ga4_measurement_id: null });
    if (path === "/saved-items") return send({ items: [] });
    if (path === "/trips") return send([]);
    if (path === "/discovery/suggestions") return send({ query: url.searchParams.get("q"), items: [], destinations: [{ id: "tokyo", name: "Tokyo" }, { id: "osaka-kyoto", name: "Kyoto" }], topics: [{ id: "culture", label: "Culture" }, { id: "food", label: "Food" }] });
    if (["/discovery/search", "/discovery/feed"].includes(path)) {
      const q = (url.searchParams.get("q") || "").toLowerCase();
      const kind = url.searchParams.get("type");
      const destination = url.searchParams.get("destination");
      const found = items.filter((item) => !hidden.has(item.id) && (!kind || kind === "all" || item.kind === kind) && (!destination || item.destination?.id === destination) && (!q || item.title.toLowerCase().includes(q)));
      return send({ enabled: true, query: url.searchParams.get("q") || "", items: found, next_cursor: null,
        filters: { kinds: kind ? [kind] : [], destinations: destination ? [destination] : [], topics: [] } });
    }
    if (path.startsWith("/discovery/content/")) {
      const item = items.find((item) => path.endsWith(`/${item.kind}/${item.id.split(":")[1]}`));
      return send(item || { code: "not_found" }, item ? 200 : 404);
    }
    if (path === "/discovery/preferences") {
      if (!options.authenticated) return send({ code: "authentication_required" }, 401);
      if (request.method() === "PUT") { const body = request.postDataJSON(); writes.push({ path, body }); preferences = { ...body, version: preferences.version + 1 }; }
      if (request.method() === "DELETE") preferences = { version: preferences.version + 1, destinations: [], topics: [], include_saved: true, include_following: true };
      return send(preferences);
    }
    if (path === "/discovery/dismiss") {
      const body = request.postDataJSON(); writes.push({ path, body });
      if (body.dismissed) hidden.add(body.id); else hidden.delete(body.id);
      return send({ dismissed: body.dismissed });
    }
    if (path === "/discovery/collections") return send({ items: [] });
    return send({ code: "fixture_endpoint_unavailable" }, 404);
  });
  return { writes };
}

for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
  test(`discovery ${locale} is public, readable and keeps the four mobile destinations`, async ({ page }, info) => {
    const c = getDiscoveryCopy(locale);
    await fixtures(page);
    await page.goto(`/${locale}/explore`);
    await expect(page.getByRole("heading", { level: 1, name: c.explore, exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: items[0].title, exact: true })).toBeVisible();
    await expect(page.getByLabel(c.searchLabel, { exact: true })).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    expect(overflow).toBe(false);
    if (info.project.name === "mobile-chromium") {
      const tabs = page.locator(".app-bottom-nav");
      await expect(tabs.getByRole("link")).toHaveCount(4);
      await expect(tabs.getByRole("link", { name: c.trips, exact: true })).toBeVisible();
      for (const link of await tabs.getByRole("link").all()) expect((await link.boundingBox())!.height).toBeGreaterThanOrEqual(44);
    }
    await page.screenshot({ path: info.outputPath(`discovery-${locale}.png`), fullPage: true });
  });
}

test("search filters persist through reload/back and empty results do not invent content", async ({ page, isMobile }) => {
  const c = getDiscoveryCopy("en"); await fixtures(page);
  await page.goto("/en/explore");
  if (isMobile) await page.getByRole("button", { name: c.filters, exact: true }).click();
  await page.getByRole("combobox", { name: c.destination, exact: true }).selectOption("osaka-kyoto");
  await expect(page).toHaveURL(/destination=osaka-kyoto/);
  await expect(page.getByRole("button", { name: items[0].title, exact: true })).toHaveCount(0);
  await page.getByLabel(c.searchLabel).fill("Kyoto");
  await page.getByRole("button", { name: c.search, exact: true }).click();
  await expect(page).toHaveURL(/q=Kyoto/);
  await expect(page.getByRole("button", { name: items[1].title, exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: items[0].title, exact: true })).toHaveCount(0);
  await page.reload();
  await expect(page.getByLabel(c.searchLabel)).toHaveValue("Kyoto");
  await page.getByLabel(c.searchLabel).fill("nonexistent-fixture");
  await page.getByRole("button", { name: c.search, exact: true }).click();
  await expect(page.getByText(c.empty, { exact: true })).toBeVisible();
  await page.goBack();
  await expect(page.getByRole("button", { name: items[1].title, exact: true })).toBeVisible();
});

test("video connects only on explicit click, preserves source and returns keyboard focus", async ({ page }, info) => {
  const c = getDiscoveryCopy("en"); await fixtures(page);
  let externalFrames = 0;
  await page.route("https://www.youtube-nocookie.com/**", async (route) => { externalFrames += 1; await route.fulfill({ contentType: "text/html", body: "<p>Isolated player fixture</p>" }); });
  await page.goto("/en/explore?type=video");
  const trigger = page.getByRole("button", { name: items[1].title, exact: true });
  await trigger.click();
  const dialog = page.getByRole("dialog", { name: items[1].title, exact: true });
  await expect(dialog.getByRole("button", { name: c.loadVideo })).toBeVisible();
  expect(externalFrames).toBe(0);
  await dialog.getByRole("button", { name: c.loadVideo }).click();
  const frame = dialog.locator("iframe");
  await expect(frame).toHaveAttribute("src", /youtube-nocookie\.com\/embed\/dQw4w9WgXcQ\?autoplay=0/);
  await expect.poll(() => externalFrames).toBe(1);
  const bounds = await frame.boundingBox();
  expect(bounds!.height).toBeGreaterThanOrEqual(200); expect(bounds!.width).toBeGreaterThanOrEqual(200);
  for (const link of await dialog.getByRole("link", { name: c.source }).all()) await expect(link).toHaveAttribute("rel", /noopener/);
  await page.evaluate(() => { document.documentElement.dataset.theme = "dark"; });
  await page.screenshot({ path: info.outputPath("discovery-video-dark.png"), fullPage: true });
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(trigger).toBeFocused();
});

test("discovery paused keeps original home and does not reveal the new nav", async ({ page }) => {
  await fixtures(page, { enabled: false });
  await page.goto("/en");
  await expect(page.locator("#trip-search")).toBeVisible();
  await expect(page.locator('.app-bottom-nav a[href="/explore/collections"]')).toHaveCount(0);
  await page.goto("/en/explore");
  await expect(page.locator('main a[href="/en/hotspots"]').first()).toBeVisible();
  await expect(page.getByRole("button", { name: items[0].title, exact: true })).toHaveCount(0);
});

test("private collections ask for login without blocking public discovery", async ({ page }) => {
  const c = getDiscoveryCopy("en"); await fixtures(page);
  await page.goto("/en/explore/collections");
  await expect(page.getByRole("heading", { name: c.collections, exact: true })).toBeVisible();
  await expect(page.getByRole("link", { name: c.login, exact: true })).toHaveAttribute("href", /login\?next=/);
});
