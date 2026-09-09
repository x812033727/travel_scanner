import { expect, test, type BrowserContext } from "@playwright/test";
import type { Stay22AllezCopy } from "../lib/stay22-allez-copy";
import { readFileSync } from "node:fs";
import { pretendSignedIn } from "./session";
import travelServicesCopy from "../messages/zh-TW/travelServices.json" with { type: "json" };

const localizedCopy: Stay22AllezCopy = JSON.parse(readFileSync(new URL("../lib/stay22-allez-messages/zh-TW.json", import.meta.url), "utf8"));
const platformCta = (platform: string) => localizedCopy.openPlatform.replace("{platform}", platform);
const bookingOptionId = "20000000-0000-4000-8000-000000000001";

const product = {
  id: "10000000-0000-4000-8000-000000000001", kind: "hotel", destination_id: "tokyo", title: "Reviewed Tokyo Hotel", source_url: "https://hotel.example.test", distance_km: 0.8,
  reason: "center_distance", facts: { country_codes: ["JP"], languages: [], facilities: [], tethering: null, reference_price: null, currency: null }, offers: [],
  booking_options: [
    { id: bookingOptionId, provider: "booking", name: "Booking.com", mode: "affiliate", affiliate_channel: "stay22", quote_status: "not_configured" },
    { id: "20000000-0000-4000-8000-000000000002", provider: "agoda", name: "Agoda", mode: "affiliate", affiliate_channel: "existing", quote_status: "not_configured" },
    { id: "20000000-0000-4000-8000-000000000003", provider: "expedia", name: "Expedia", mode: "affiliate", affiliate_channel: "stay22", quote_status: "not_configured" },
  ],
};

async function fixture(context: BrowserContext) {
  const posts: { body: string; path: string }[] = [];
  const external: string[] = [];
  const quotes: string[] = [];
  await context.route("https://**", async (route) => {
    external.push(route.request().url());
    await route.abort();
  });
  await context.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname.replace("/api/travel", "");
    if (path.endsWith("/clickout")) {
      posts.push({ body: request.postData() || "", path });
      // Fulfill the popup locally: Playwright routing does not reliably intercept subsequent redirects.
      // Redirect URL generation is covered by API tests; no affiliate host is contacted here.
      await route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Fixture booking platform</title><h1>Reviewed Tokyo Hotel</h1>", headers: { "Cache-Control": "no-store", "Referrer-Policy": "no-referrer" } });
      return;
    }
    if (path.includes("hotel-quotes")) quotes.push(path);
    let body: unknown = {};
    if (path === "/travel-services/config") body = { public_enabled: true, enabled_kinds: ["hotel"], enabled_destinations: ["tokyo"] };
    else if (path === "/travel-services") body = { enabled: true, enabled_kinds: ["hotel"], destinations: ["tokyo"], items: [product], areas: [], selections: [] };
    else if (path.includes("destination-offers")) body = { options: [] };
    else if (path.includes("/saved-items")) body = { items: [], total: 0, has_more: false };
    else if (path === "/runtime/public-config") body = { hotspots_enabled: true, hotspots_destinations: ["tokyo"] };
    else if (path === "/auth/me") { await route.fulfill({ status: 401, json: { detail: "not signed in" } }); return; }
    await route.fulfill({ json: body });
  });
  return { posts, external, quotes };
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
    await expect(panel.getByText(copy.viaStay22)).toHaveCount(2);
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

test("native same-origin form and retry reach the real BFF instead of an opaque-origin CSRF rejection", async ({ page, context }) => {
  const external: string[] = [];
  await context.route("https://**", (route) => { external.push(route.request().url()); return route.abort(); });
  // Only seed public read models. The clickout POST and its retry exercise the actual Next BFF.
  await context.route("**/api/travel/travel-services/config", (route) => route.fulfill({ json: { public_enabled: true, enabled_kinds: ["hotel"], enabled_destinations: ["tokyo"] } }));
  await context.route("**/api/travel/travel-services?**", (route) => route.fulfill({ json: { enabled: true, enabled_kinds: ["hotel"], destinations: ["tokyo"], items: [product], areas: [], selections: [] } }));
  await context.route("**/api/travel/affiliates/destination-offers?**", (route) => route.fulfill({ json: { options: [] } }));
  await page.goto("/zh-TW/destinations/tokyo/services?type=hotel");
  await page.getByRole("button", { name: travelServicesCopy.platforms, exact: true }).click();
  const panel = page.getByRole("dialog", { name: product.title });
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
  expect(await response.request().headerValue("origin")).toBe(new URL(page.url()).origin);
  await expect(popup.getByRole("heading", { name: localizedCopy.errorTitle })).toBeVisible();
  expect(await popup.evaluate(() => window.opener === null)).toBe(true);
  const retryResponse = context.waitForEvent("response", (value) => value.request().method() === "POST" && value.url().includes(`booking-options/${bookingOptionId}/clickout`));
  await popup.getByRole("button", { name: localizedCopy.retry }).click();
  const retried = await retryResponse;
  expect(retried.status()).toBe(404);
  expect(retried.headers()["content-type"]).toContain("text/html");
  await expect(popup.getByRole("heading", { name: localizedCopy.errorTitle })).toBeVisible();
  await popup.close();
  await expect(panel).toBeVisible();
  expect(external).toEqual([]);
});
