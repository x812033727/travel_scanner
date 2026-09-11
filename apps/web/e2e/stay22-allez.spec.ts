import { expect, test, type BrowserContext, type Locator, type Page } from "@playwright/test";
import type { Stay22AllezCopy } from "../lib/stay22-allez-copy";
import type { HotelOperatingRules } from "../lib/hotel-operation-rules";
import { getDiscoveryCopy } from "../lib/discovery-copy";
import { existsSync, readFileSync } from "node:fs";
import { createServer } from "node:http";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { pretendSignedIn } from "./session";
import travelServicesCopy from "../messages/zh-TW/travelServices.json" with { type: "json" };

const localizedCopy: Stay22AllezCopy = JSON.parse(readFileSync(new URL("../lib/stay22-allez-messages/zh-TW.json", import.meta.url), "utf8"));
const platformCta = (platform: string) => localizedCopy.openPlatform.replace("{platform}", platform);
const bookingOptionId = "20000000-0000-4000-8000-000000000001";

test("production HTTP preserves clickout policies without following external redirects", async ({ request }, testInfo) => {
  test.skip(!existsSync(new URL("../.next/BUILD_ID", import.meta.url)), "Run next build for production wire coverage");
  test.setTimeout(60_000);
  const posts: string[] = [];
  const destination = "https://booking.example.test/verified-hotel";
  const upstream = createServer((incoming, outgoing) => {
    const url = new URL(incoming.url || "/", "http://127.0.0.1");
    incoming.resume();
    if (incoming.method === "POST" && url.pathname.endsWith("/clickout")) {
      posts.push(url.pathname);
      if (!url.searchParams.has("failure")) {
        outgoing.writeHead(303, { Location: destination, "Referrer-Policy": "no-referrer" });
        outgoing.end();
        return;
      }
      outgoing.statusCode = 404;
    }
    outgoing.setHeader("Content-Type", "application/json");
    outgoing.end(JSON.stringify({ detail: "Isolated header fixture" }));
  });
  const portProbe = createServer();
  await new Promise<void>((resolve) => upstream.listen(0, "127.0.0.1", resolve));
  await new Promise<void>((resolve) => portProbe.listen(0, "127.0.0.1", resolve));
  const port = (portProbe.address() as { port: number }).port;
  const apiPort = (upstream.address() as { port: number }).port;
  await new Promise<void>((resolve) => portProbe.close(() => resolve()));
  const origin = `http://127.0.0.1:${port}`;
  const server = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
    cwd: fileURLToPath(new URL("../", import.meta.url)),
    env: { ...process.env, NODE_ENV: "production", API_INTERNAL_URL: `http://127.0.0.1:${apiPort}`, NEXT_PUBLIC_SITE_URL: origin, NEXT_TELEMETRY_DISABLED: "1" },
    stdio: ["ignore", "pipe", "pipe"], windowsHide: true,
  });
  let logs = "";
  server.stdout.on("data", (chunk) => { logs = `${logs}${chunk}`.slice(-12_000); });
  server.stderr.on("data", (chunk) => { logs = `${logs}${chunk}`.slice(-12_000); });
  server.on("error", (error) => { logs += error.message; });
  try {
    await expect.poll(async () => {
      try { return (await request.get(`${origin}/api/travel/auth/me`, { timeout: 1_000, maxRedirects: 0 })).status(); }
      catch { return 0; }
    }, { timeout: 30_000 }).toBe(200);
    for (const path of ["/zh-TW/explore", "/api/travel/auth/me"]) {
      const response = await request.get(`${origin}${path}`, { maxRedirects: 0 });
      expect(response.headers()["referrer-policy"]).toBe("strict-origin-when-cross-origin");
      expect(response.headers()["x-content-type-options"]).toBe("nosniff");
    }
    const endpoints = [
      `/travel-services/${bookingOptionId}/booking-options/${bookingOptionId}/clickout`,
      `/travel-services/${bookingOptionId}/hotel-links/booking/clickout`,
      `/affiliates/offers/${bookingOptionId}/clickout`,
      `/affiliates/destination-offers/${bookingOptionId}/clickout`,
      `/offers/${bookingOptionId}/clickout`,
    ];
    const headers = { Origin: origin, Accept: "text/html", Referer: `${origin}/zh-TW/explore` };
    for (const endpoint of endpoints) {
      // No browser navigation and no redirect following: even a regression can
      // only reach the local fixture, never a real hotel/affiliate destination.
      const response = await request.post(`${origin}/api/travel${endpoint}?placement=discovery`, { headers, form: {}, maxRedirects: 0 });
      expect(response.status()).toBe(303);
      expect(response.headers()["location"]).toBe(destination);
      expect(response.headers()["referrer-policy"]).toBe("no-referrer");
      expect(response.headers()["cache-control"]).toBe("no-store");
      expect(response.headers()["x-frame-options"]).toBe("DENY");
    }
    const error = await request.post(`${origin}/api/travel${endpoints[0]}?placement=discovery&failure=1`, { headers, form: {}, maxRedirects: 0 });
    expect(error.status()).toBe(404);
    expect(error.headers()["referrer-policy"]).toBe("same-origin");
    expect(error.headers()["content-type"]).toContain("text/html");
    expect(await error.text()).toContain(localizedCopy.retry);
    expect(posts).toHaveLength(endpoints.length + 1);
  } finally {
    await testInfo.attach("isolated-production-server", { body: logs, contentType: "text/plain" });
    if (server.exitCode === null && server.signalCode === null) {
      const exited = once(server, "exit");
      server.kill();
      await exited;
    }
    upstream.closeAllConnections();
    await new Promise<void>((resolve) => upstream.close(() => resolve()));
  }
});

const sourceCredit = {
  title: "Reviewed hotel source", publisher: "Fixture publisher", url: "https://source.example.test/hotel",
  license_name: "Fixture license", license_url: "https://source.example.test/license",
  changes: "Mokaair 將公開資料整理為飯店介紹，補充地址並調整格式；這是保留於來源資料的整理備註。",
};
const product = {
  id: "10000000-0000-4000-8000-000000000001", kind: "hotel", destination_id: "tokyo", title: "Reviewed Tokyo Hotel", source_url: "https://hotel.example.test", distance_km: 0.8,
  reason: "center_distance", facts: { country_codes: ["JP"], languages: [], facilities: [], tethering: null, reference_price: null, currency: null, source_credits: [sourceCredit] }, offers: [],
  booking_options: [
    { id: bookingOptionId, provider: "booking", name: "Booking.com", mode: "affiliate", affiliate_channel: "stay22", quote_status: "not_configured" },
    { id: "20000000-0000-4000-8000-000000000002", provider: "agoda", name: "Agoda", mode: "affiliate", affiliate_channel: "existing", quote_status: "not_configured" },
    { id: "20000000-0000-4000-8000-000000000003", provider: "expedia", name: "Expedia", mode: "affiliate", affiliate_channel: "stay22", quote_status: "not_configured" },
    { id: "20000000-0000-4000-8000-000000000004", provider: "official", name: null, mode: "direct", quote_status: "not_configured" },
  ],
};

const discoveryHotel = {
  id: `hotel:${product.id}`, kind: "hotel", title: product.title,
  summary: "Synthetic reviewed hotel fixture, not a real booking or price.",
  locale: "zh-TW", href: "/destinations/tokyo/services?type=hotel",
  destination: { id: "tokyo", name: "東京" },
  source: { kind: "editorial", label: "Synthetic catalog fixture", url: null },
  published_at: null, updated_at: null, thumbnail_url: null,
  collection_ref: { kind: "hotel", id: product.id },
  detail: { hotel: product, guides: [], merchants: [] },
};

async function expectSimplifiedBookingCopy(panel: Locator) {
  await expect(panel.getByText("透過 Stay22 合作連結", { exact: true })).toHaveCount(0);
  await expect(panel.getByText(localizedCopy.disclosure, { exact: true })).toBeVisible();
  await expect(panel.getByText("資料來源與授權", { exact: true })).toHaveCount(0);
  const summary = panel.locator("summary").filter({ hasText: /^資料來源$/ });
  await expect(summary).toHaveText("資料來源");
  await summary.click();
  const source = panel.getByRole("link", { name: `${sourceCredit.title} · ${travelServicesCopy.newTab}`, exact: true });
  const license = panel.getByRole("link", { name: `${sourceCredit.license_name} · ${travelServicesCopy.newTab}`, exact: true });
  await expect(source).toBeVisible();
  await expect(source).toHaveAttribute("href", sourceCredit.url);
  await expect(license).toBeVisible();
  await expect(license).toHaveAttribute("href", sourceCredit.license_url);
  for (const link of [source, license]) {
    await expect(link).toHaveAttribute("target", "_blank");
    await expect(link).toHaveAttribute("rel", "noopener noreferrer");
  }
  await expect(panel.getByText(sourceCredit.publisher, { exact: false })).toBeVisible();
  // Verify absent DOM text, not just content hidden by the collapsed disclosure.
  await expect(panel.getByText(sourceCredit.changes, { exact: true })).toHaveCount(0);
}

async function openDiscoveryBookingPanel(page: Page) {
  await page.goto("/zh-TW/explore?destination=tokyo&category=hotels");
  await page.locator(`article[id="${discoveryHotel.id}"]`).getByRole("link", { name: product.title, exact: true }).click();
  const detail = page.getByRole("dialog", { name: getDiscoveryCopy("zh-TW").details, exact: true });
  await expect(detail.getByRole("heading", { name: product.title, exact: true })).toBeVisible();
  await detail.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  const panel = page.getByRole("dialog", { name: product.title, exact: true });
  await expect(panel).toBeVisible();
  await expectSimplifiedBookingCopy(panel);
  return panel;
}

async function fixture(context: BrowserContext, { realClickout = false, operatingRules }: { realClickout?: boolean; operatingRules?: HotelOperatingRules } = {}) {
  const fixtureProduct = { ...product, facts: { ...product.facts, ...(operatingRules ? { hotel_operating_rules: operatingRules } : {}) } };
  const posts: { body: string; path: string; url: string; origin: string | null }[] = [];
  const external: string[] = [];
  const quotes: string[] = [];
  await context.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (["127.0.0.1", "localhost", "[::1]"].includes(url.hostname)) return route.fallback();
    external.push(url.href);
    await route.abort();
  });
  await context.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname.replace("/api/travel", "");
    if (path.endsWith("/clickout")) {
      posts.push({ body: request.postData() || "", path, url: request.url(), origin: await request.headerValue("origin") });
      if (realClickout) return route.fallback();
      // Fulfill the popup locally: Playwright routing does not reliably intercept subsequent redirects.
      // Redirect URL generation is covered by API tests; no affiliate host is contacted here.
      await route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Fixture booking platform</title><h1>Reviewed Tokyo Hotel</h1>", headers: { "Cache-Control": "no-store", "Referrer-Policy": "no-referrer" } });
      return;
    }
    if (path.includes("hotel-quotes")) quotes.push(path);
    let body: unknown = {};
    if (path === "/discovery/status") body = { enabled: true };
    else if (path === "/community/status") body = { enabled: false };
    else if (path === "/analytics/config") body = { first_party_enabled: false, ga4_enabled: false };
    else if (path === "/discovery/feed" || path === "/discovery/search") body = { enabled: true, query: "", items: [discoveryHotel], next_cursor: null, filters: { kinds: [], destinations: [], topics: [] } };
    else if (path === `/discovery/content/hotel/${product.id}`) body = discoveryHotel;
    else if (path === "/discovery/suggestions") body = { items: [], destinations: [{ id: "tokyo", name: "東京" }], topics: [] };
    else if (path === "/travel-services/config") body = { public_enabled: true, enabled_kinds: ["hotel"], enabled_destinations: ["tokyo"] };
    else if (path === "/travel-services") body = { enabled: true, enabled_kinds: ["hotel"], destinations: ["tokyo"], items: [fixtureProduct], areas: [], selections: [] };
    else if (path.includes("destination-offers")) body = { options: [] };
    else if (path.includes("/saved-items")) body = { items: [], total: 0, has_more: false };
    else if (path === "/runtime/public-config") body = { hotspots_enabled: true, hotspots_destinations: ["tokyo"] };
    else if (path === "/auth/me") { await route.fulfill({ status: 401, json: { detail: "not signed in" } }); return; }
    await route.fulfill({ json: body });
  });
  return { posts, external, quotes };
}

test("same-tab fallback is explicit and posts the current checked dates without opening another page", async ({ page, context }) => {
  const calls = await fixture(context);
  await page.goto("/zh-TW/destinations/tokyo/services?type=hotel");
  await page.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  const panel = page.getByRole("dialog", { name: product.title });
  const fallbackName = localizedCopy.openSameTab.replace("{platform}", "Booking.com");
  await expect(panel.getByRole("button", { name: fallbackName, exact: true })).toHaveCount(0);
  const popupWait = context.waitForEvent("page");
  await panel.getByRole("button", { name: /前往 Booking.com 查價格/ }).click();
  const popup = await popupWait;
  await expect(popup).toHaveTitle("Fixture booking platform");
  await popup.close();
  await panel.getByLabel(localizedCopy.checkIn, { exact: true }).fill("2099-11-10");
  await panel.getByLabel(localizedCopy.checkOut, { exact: true }).fill("2099-11-12");
  const fallback = panel.getByRole("button", { name: fallbackName, exact: true });
  await expect(fallback).toHaveAttribute("formtarget", "_self");
  await fallback.scrollIntoViewIfNeeded();
  expect((await fallback.boundingBox())!.height).toBeGreaterThanOrEqual(44);
  const pages = context.pages().length;
  await fallback.focus();
  await page.keyboard.press("Enter");
  await expect(page).toHaveTitle("Fixture booking platform");
  expect(context.pages()).toHaveLength(pages);
  expect(calls.posts).toHaveLength(2);
  expect(Object.fromEntries(new URLSearchParams(calls.posts[1].body))).toEqual({ check_in: "2099-11-10", check_out: "2099-11-12" });
  expect(new URL(calls.posts[1].url).searchParams.has("check_in")).toBe(false);
  expect(calls.external).toEqual([]);
  expect(calls.quotes).toEqual([]);
});

test("hotel restrictions prevent date omission and both clickout targets, with readable source notices", async ({ page, context }) => {
  const calls = await fixture(context, { operatingRules: { unavailable_stays: [{ start_date: "2099-11-10", end_date: "2099-11-12", reason: "Synthetic maintenance exclusion", source_url: "https://hotel.example.test/notice" }] } });
  await page.goto("/zh-TW/destinations/tokyo/services?type=hotel");
  await page.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  const panel = page.getByRole("dialog", { name: product.title });
  await expect(panel.getByRole("checkbox", { name: localizedCopy.omitDates })).toHaveCount(0);
  const open = panel.getByRole("button", { name: /前往 Booking.com 查價格/ });
  await open.click();
  expect(calls.posts).toEqual([]);
  await expect(panel.getByLabel(localizedCopy.checkIn, { exact: true })).toBeFocused();
  await panel.getByLabel(localizedCopy.checkIn, { exact: true }).fill("2099-11-09");
  await panel.getByLabel(localizedCopy.checkOut, { exact: true }).fill("2099-11-10");
  const popupWait = context.waitForEvent("page");
  await open.click();
  const popup = await popupWait;
  await expect(popup).toHaveTitle("Fixture booking platform");
  await popup.close();
  await panel.getByLabel(localizedCopy.checkOut, { exact: true }).fill("2099-11-11");
  const fallback = panel.getByRole("button", { name: localizedCopy.openSameTab.replace("{platform}", "Booking.com"), exact: true });
  await fallback.click();
  await expect(panel.getByRole("alert")).toHaveText(localizedCopy.operatingUnavailable);
  expect(calls.posts).toHaveLength(1);
  const source = panel.getByRole("link", { name: new RegExp(localizedCopy.operatingSource) });
  await expect(source).toHaveAttribute("href", "https://hotel.example.test/notice");
  await expect(source).toHaveAttribute("rel", "noopener noreferrer");
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  await page.screenshot({ path: test.info().outputPath("hotel-restriction-panel.png") });
  expect(calls.external).toEqual([]);
});

for (const option of product.booking_options) {
  test(`discovery: first ${option.provider} click preserves its entry and booking conditions without retry`, async ({ page, context }) => {
    const calls = await fixture(context);
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    const panel = await openDiscoveryBookingPanel(page);
    const fields = { check_in: "2099-11-10", check_out: "2099-11-20", adults: "2", children: "1" };
    await panel.getByLabel(localizedCopy.checkIn, { exact: true }).fill(fields.check_in);
    await panel.getByLabel(localizedCopy.checkOut, { exact: true }).fill(fields.check_out);
    await panel.getByLabel(localizedCopy.adults, { exact: true }).fill(fields.adults);
    await panel.getByLabel(localizedCopy.children, { exact: true }).fill(fields.children);
    const name = option.provider === "official" ? travelServicesCopy.officialHotel : option.name!;
    const open = panel.getByRole("button", { name: `${platformCta(name)} · ${travelServicesCopy.newTab}`, exact: true });
    const popupWait = context.waitForEvent("page");
    await open.click();
    const popup = await popupWait;
    await expect(popup).toHaveTitle("Fixture booking platform");
    await expect(popup.getByRole("button", { name: localizedCopy.retry })).toHaveCount(0);
    expect(await popup.evaluate(() => window.opener === null)).toBe(true);
    expect(calls.posts).toHaveLength(1);
    const [post] = calls.posts;
    expect(post.path).toBe(`/travel-services/${product.id}/booking-options/${option.id}/clickout`);
    expect(new URL(post.url).searchParams.get("placement")).toBe("discovery");
    expect(post.origin).toBe(new URL(page.url()).origin);
    expect(Object.fromEntries(new URLSearchParams(post.body))).toEqual(fields);
    await popup.close();
    await expect(panel.getByLabel(localizedCopy.checkIn, { exact: true })).toHaveValue(fields.check_in);
    expect(calls.posts).toHaveLength(1);
    expect(calls.external).toEqual([]);
    expect(calls.quotes).toEqual([]);
    expect(errors).toEqual([]);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  });
}

for (const entry of ["destination", "nearby"] as const) {
  test(`${entry}: exact hotel platform clickout without map or real affiliate traffic`, async ({ page, context }) => {
    const calls = await fixture(context);
    const copy = localizedCopy;
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(`/zh-TW/destinations/tokyo/services?type=hotel${entry === "nearby" ? "&hotspot_id=fixture-hotspot&radius_km=3" : ""}`);
    await page.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
    const panel = page.getByRole("dialog", { name: product.title });
    await expect(panel).toBeVisible();
    await expectSimplifiedBookingCopy(panel);
    expect(calls.external).toEqual([]);
    expect(calls.quotes).toEqual([]);
    await expect(page.locator("iframe")).toHaveCount(0);
    await panel.getByLabel(copy.checkIn, { exact: true }).fill("2099-11-10");
    await panel.getByLabel(copy.checkOut, { exact: true }).fill("2099-12-20");
    await panel.getByLabel(copy.adults, { exact: true }).fill("2");
    await panel.getByLabel(copy.children, { exact: true }).fill("1");
    const open = panel.getByRole("button", { name: new RegExp(platformCta("Booking.com").replace(".", "\\.")) });
    await open.scrollIntoViewIfNeeded();
    expect((await open.boundingBox())!.height).toBeGreaterThanOrEqual(44);
    const popupWait = context.waitForEvent("page");
    await open.click();
    const popup = await popupWait;
    await expect(popup).toHaveTitle("Fixture booking platform");
    expect(await popup.evaluate(() => window.opener === null)).toBe(true);
    expect(calls.posts).toHaveLength(1);
    expect(Object.fromEntries(new URLSearchParams(calls.posts[0].body))).toEqual({ check_in: "2099-11-10", check_out: "2099-12-20", adults: "2", children: "1" });
    expect(calls.posts[0].path).toBe(`/travel-services/${product.id}/booking-options/${bookingOptionId}/clickout`);
    await popup.close();
    await expect(panel.getByLabel(copy.checkOut, { exact: true })).toHaveValue("2099-12-20");
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
    const bounds = await panel.boundingBox();
    expect(bounds!.x).toBeGreaterThanOrEqual(0);
    expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(page.viewportSize()!.width + 1);
    if (entry === "destination") await page.screenshot({ path: test.info().outputPath("stay22-direct-booking-panel.png") });
    await page.keyboard.press("Escape");
    await expect(panel).toHaveCount(0);
    await expect(page.getByRole("button", { name: travelServicesCopy.platforms, exact: true })).toBeFocused();
    expect(errors).toEqual([]);
    expect(calls.quotes).toEqual([]);
  });
}

test("invalid dates stay in the source panel until the visitor explicitly omits them", async ({ page, context }) => {
  const calls = await fixture(context);
  const copy = localizedCopy;
  await page.goto("/zh-TW/destinations/tokyo/services?type=hotel");
  await page.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  const panel = page.getByRole("dialog", { name: product.title });
  await panel.getByLabel(copy.checkIn, { exact: true }).fill("2020-01-01");
  await panel.getByLabel(copy.checkOut, { exact: true }).fill("2020-01-02");
  await panel.getByRole("button", { name: /前往 Booking.com 查價格/ }).click();
  await expect(panel.getByRole("alert")).toHaveText(copy.pastDates);
  expect(calls.posts).toEqual([]);
  expect(calls.external).toEqual([]);
  await panel.getByRole("checkbox", { name: copy.omitDates }).check();
  const popupWait = context.waitForEvent("page");
  await panel.getByRole("button", { name: /前往 Booking.com 查價格/ }).click();
  const popup = await popupWait;
  await expect(popup).toHaveTitle("Fixture booking platform");
  expect(calls.posts[0].body).toBe("");
  await popup.close();
  await expect(panel.getByLabel(copy.checkIn, { exact: true })).toHaveValue("2020-01-01");
});

test("trip lodging shows the reviewed catalog before its opt-in map and sends untruncated saved preferences", async ({ page, context }) => {
  const calls = await fixture(context);
  await pretendSignedIn(page);
  const tripId = "allez-trip-fixture";
  const bookingContext = { check_in: "2099-11-10", check_out: "2099-12-20", adults: 3, children: 1, rooms: 2, children_ages: [7] };
  const copy = localizedCopy;
  const trip = {
    id: tripId, name: "Private trip fixture", mode: "manual", total_price: 0, currency: "TWD", data: {}, version: 1,
    destination_name: "東京", start_date: bookingContext.check_in, end_date: bookingContext.check_out, timezone: "Asia/Tokyo", route_preference: "FEWER_TRANSFERS",
    primary_lodging: null, share_enabled: false, items: [{
      id: "00000000-0000-4000-8000-000000000010", item_type: "hotel_anchor", day_date: bookingContext.check_in, position: -1,
      title: "Hotel departure fixture", location_name: null, latitude: null, longitude: null, location_source: null,
      locked: false, is_estimated: false, system_role: "hotel_start", fixed_time: true, data: { needs_place_confirmation: true },
    }], route_segments: [], routing: { status: "idle", total: 0, completed: 0, warnings: [], day_settings: [] },
  };
  await context.route("**/api/travel/auth/me", (route) => route.fulfill({ json: { id: "00000000-0000-4000-8000-000000000001", email: "tester@example.test" } }));
  await context.route(`**/api/travel/trips/${tripId}/**`, (route) => {
    const path = new URL(route.request().url()).pathname;
    let body: unknown = {};
    if (path.endsWith("/stay-areas")) body = { trip_id: tripId, version: 1, status: "recommended", city_code: "NRT", booking_context: bookingContext, pricing: { available: false }, current_lodging_area_code: null, located_item_count: 0, unassigned_item_count: 0, excluded_extension: {}, warnings: [], areas: [] };
    else if (path.endsWith("/travel-services")) body = { enabled: true, enabled_kinds: ["hotel"], destinations: ["tokyo"], items: [product], areas: [], selections: [], version: 1, start_date: bookingContext.check_in, end_date: bookingContext.check_out, booking_context: bookingContext };
    else if (path.endsWith("/routes/status")) body = { version: 1, status: "idle" };
    return route.fulfill({ json: body });
  });
  await context.route(`**/api/travel/trips/${tripId}`, (route) => route.fulfill({ json: trip }));
  await page.goto(`/zh-TW/trips/${tripId}`);
  const optional = page.locator(".calm-optional-arrangements");
  await optional.locator(":scope > summary").click();
  await optional.getByRole("button", { name: trip.items[0].title, exact: true }).click();
  const catalog = page.getByRole("region", { name: copy.catalogTitle });
  await expect(catalog).toBeVisible();
  const map = page.locator("details").filter({ has: page.locator("summary").getByText(copy.mapToggle, { exact: true }) });
  await expect(map).not.toHaveAttribute("open");
  await catalog.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  const panel = page.getByRole("dialog", { name: product.title });
  await expectSimplifiedBookingCopy(panel);
  await expect(panel.getByLabel(copy.checkOut, { exact: true })).toHaveValue(bookingContext.check_out);
  await expect(panel.getByLabel(copy.adults, { exact: true })).toHaveValue("3");
  await expect(panel.getByText("原設定：2 間房")).toBeVisible();
  const popupWait = context.waitForEvent("page");
  await panel.getByRole("button", { name: /前往 Booking.com 查價格/ }).click();
  const popup = await popupWait;
  await expect(popup).toHaveTitle("Fixture booking platform");
  expect(Object.fromEntries(new URLSearchParams(calls.posts[0].body))).toEqual({ check_in: bookingContext.check_in, check_out: bookingContext.check_out, adults: "3", children: "1" });
  expect(calls.posts[0].body).not.toContain(tripId);
  expect(calls.posts[0].body).not.toContain("rooms");
  expect(calls.quotes).toEqual([]);
  await popup.close();
});

for (const entry of ["destination", "discovery"] as const) {
test(`${entry}: native same-origin form and retry preserve placement and conditions through the real BFF`, async ({ page, context }) => {
  // Public read models are synthetic. POST and retry reach the actual Next BFF;
  // the local upstream deliberately returns 404, not a successful provider redirect.
  const calls = await fixture(context, { realClickout: true });
  if (entry === "destination") {
    await page.goto("/zh-TW/destinations/tokyo/services?type=hotel");
    await page.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  } else {
    await openDiscoveryBookingPanel(page);
  }
  const panel = page.getByRole("dialog", { name: product.title, exact: true });
  const fields = { check_in: "2099-11-10", check_out: "2099-11-20", adults: "2", children: "1" };
  await panel.getByLabel(localizedCopy.checkIn, { exact: true }).fill(fields.check_in);
  await panel.getByLabel(localizedCopy.checkOut, { exact: true }).fill(fields.check_out);
  await panel.getByLabel(localizedCopy.adults, { exact: true }).fill(fields.adults);
  await panel.getByLabel(localizedCopy.children, { exact: true }).fill(fields.children);
  const open = panel.getByRole("button", { name: /前往 Booking.com 查價格/ });
  await expect(open.locator("..")).toHaveAttribute("rel", "noopener");
  const responseWait = context.waitForEvent("response", (response) => response.request().method() === "POST" && response.url().includes(`booking-options/${bookingOptionId}/clickout`));
  const popupWait = context.waitForEvent("page");
  await open.click();
  const popup = await popupWait;
  const response = await responseWait;
  // The local upstream fixture deliberately has no booking offer. It must return our recoverable HTML,
  // not fail before reaching the upstream with Origin:null / forbidden-origin.
  expect(response.status()).toBe(404);
  expect(response.headers()["content-type"]).toContain("text/html");
  expect(response.headers()["referrer-policy"]).toBe("same-origin");
  expect(await response.request().headerValue("origin")).toBe(new URL(page.url()).origin);
  expect(new URL(response.url()).searchParams.get("placement")).toBe(entry);
  expect(Object.fromEntries(new URLSearchParams(response.request().postData() || ""))).toEqual(fields);
  await expect(popup.getByRole("heading", { name: localizedCopy.errorTitle })).toBeVisible();
  expect(await popup.evaluate(() => window.opener === null)).toBe(true);
  const retryResponse = context.waitForEvent("response", (value) => value.request().method() === "POST" && value.url().includes(`booking-options/${bookingOptionId}/clickout`));
  await popup.getByRole("button", { name: localizedCopy.retry }).click();
  const retried = await retryResponse;
  expect(retried.status()).toBe(404);
  expect(retried.headers()["content-type"]).toContain("text/html");
  expect(retried.headers()["referrer-policy"]).toBe("same-origin");
  expect(await retried.request().headerValue("origin")).toBe(new URL(page.url()).origin);
  expect(new URL(retried.url()).searchParams.get("placement")).toBe(entry);
  expect(Object.fromEntries(new URLSearchParams(retried.request().postData() || ""))).toEqual(fields);
  expect(calls.posts).toHaveLength(2);
  await expect(popup.getByRole("heading", { name: localizedCopy.errorTitle })).toBeVisible();
  await popup.close();
  await expect(panel).toBeVisible();
  expect(calls.external).toEqual([]);
});
}
