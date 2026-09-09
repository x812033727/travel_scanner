import { expect, test as base, type Page } from "@playwright/test";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { existsSync } from "node:fs";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { defaultUsageCatalog } from "../lib/usage-catalog";
import { siteFeatureKeys } from "../lib/site-features";
import { stay22ScriptCopy } from "../lib/stay22-script-copy";
import { STAY22_SCRIPT_URL } from "../lib/stay22-script";

const canonical = "https://mokaair.com";
const publicPath = "/zh-TW/destinations/tokyo/services";
const hotelId = "10000000-0000-4000-8000-000000000001";
const bookingId = "20000000-0000-4000-8000-000000000001";
const fixtureLmaId = "000000000000000000000001";
const bookingUrl = "https://www.booking.com/hotel/jp/script-fixture.html";
const officialUrl = "https://hotel.example.test/access";
const copy = stay22ScriptCopy("zh-TW");
const hotel = {
  id: hotelId, title: "Reviewed Script Hotel", destination_id: "tokyo", kind: "hotel",
  category: "city_hotel", official_url: officialUrl, distance_km: 1, reason: "center_distance",
  facts: { country_codes: ["JP"], languages: [], facilities: [], reference_price: null, currency: null },
  offers: [], booking_options: [{ id: bookingId, provider: "booking", name: "Booking.com", mode: "affiliate", affiliate_channel: "stay22", quote_status: "not_configured" }],
};
type Mode = "script" | "off" | "allez" | "error" | "invalid";
type ApiCall = { path: string; method: string; cookie: string; authorization: string };
type Fixture = {
  origin: string; mode: Mode; sdk: "rewrite" | "noop" | "fail";
  optionFailure: boolean; sdkLoads: string[]; driveLoads: string[]; blocked: string[];
  popupLoads: string[]; api: ApiCall[]; errors: string[];
};
type MockWindow = Window & { __stay22Mock?: { lmaID: string; documentUrl: string }; __publicDocumentMarker?: string };

// This synthetic SDK proves our anchors can be observed after the sheet opens.
// It is deliberately not a copy of the vendor SDK or a claim about its behavior.
const mockSdk = `(() => {
  window.__stay22Mock = { lmaID: window.Stay22.params.lmaID, documentUrl: location.href };
  const rewrite = () => document.querySelectorAll('a[href]').forEach((a) => {
    if (a.href.startsWith('https://www.booking.com/hotel/')) {
      a.href = 'https://stay22.example.test/booking?link=' + encodeURIComponent(a.href);
    }
  });
  new MutationObserver(rewrite).observe(document.documentElement, { childList: true, subtree: true });
  rewrite();
})();`;

const test = base.extend<{ site: Fixture }>({
  site: async ({ context, request }, runTest, testInfo) => {
    test.skip(!existsSync(new URL("../.next/BUILD_ID", import.meta.url)), "Run next build for isolated Script browser coverage");
    const site: Fixture = { origin: "", mode: "script", sdk: "rewrite", optionFailure: false, sdkLoads: [], driveLoads: [], blocked: [], popupLoads: [], api: [], errors: [] };
    const upstream = createServer((incoming, outgoing) => {
      incoming.resume();
      const url = new URL(incoming.url || "/", "http://127.0.0.1");
      site.api.push({ path: url.pathname, method: incoming.method || "GET", cookie: incoming.headers.cookie || "", authorization: incoming.headers.authorization || "" });
      let result: unknown = {};
      if (url.pathname === "/api/v1/travel-services/stay22-script-config") {
        outgoing.statusCode = site.mode === "error" ? 503 : 200;
        result = { enabled: site.mode === "script" || site.mode === "invalid", integration_mode: site.mode === "allez" ? "allez" : "script", lma_id: site.mode === "invalid" ? "unexpected-id" : site.mode === "script" ? fixtureLmaId : null };
      } else if (url.pathname.endsWith("/stay22-script-options")) {
        outgoing.statusCode = site.optionFailure ? 503 : site.mode === "script" ? 200 : 404;
        result = { title: hotel.title, destination_id: "tokyo", options: outgoing.statusCode === 200 ? [
          { id: bookingId, provider: "booking", name: "Booking.com", url: bookingUrl },
          { id: "official-option", provider: "official", name: "Official website", url: officialUrl },
        ] : [] };
      } else if (url.pathname === "/api/v1/travel-services") result = { enabled: true, enabled_kinds: ["hotel"], destinations: ["tokyo"], items: [hotel], areas: [], selections: [] };
      else if (url.pathname === "/api/v1/travel-services/config") result = { public_enabled: true, enabled_kinds: ["hotel"], enabled_destinations: ["tokyo"] };
      else if (url.pathname.includes("destination-offers")) result = { options: [] };
      else if (url.pathname === "/api/v1/runtime/site-visibility") result = Object.fromEntries(siteFeatureKeys.map((key) => [`${key}_enabled`, true]));
      else if (url.pathname === "/api/v1/usage-catalog") result = defaultUsageCatalog;
      else if (url.pathname === "/api/v1/destinations") result = { items: [
        { id: "tokyo", city: "東京", country: "日本", role: "destination" },
        { id: "osaka", city: "大阪", country: "日本", role: "destination" },
        { id: "fukuoka", city: "福岡", country: "日本", role: "destination" },
      ] };
      else if (url.pathname === "/api/v1/runtime/public-config") result = { hotspots_enabled: true, hotspots_destinations: ["tokyo"] };
      else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) result = { locale: "zh-TW", version: "fixture", entries: {} };
      else if (url.pathname === "/api/v1/analytics/config") result = { first_party_enabled: false, ga4_enabled: false };
      else if (url.pathname === "/api/v1/auth/me") result = { id: "00000000-0000-4000-8000-000000000001", email: "private-fixture@example.test", preferred_locale: "zh-TW" };
      else if (url.pathname.startsWith("/api/v1/saved-items")) result = { items: [] };
      else if (url.pathname === "/api/v1/trips") result = [];
      else if (url.pathname === "/api/v1/community/status") result = { enabled: false };
      outgoing.setHeader("Content-Type", "application/json");
      outgoing.setHeader("Cache-Control", "no-store");
      outgoing.end(JSON.stringify(result));
    });
    const probe = createServer();
    await new Promise<void>((resolve) => upstream.listen(0, "127.0.0.1", resolve));
    await new Promise<void>((resolve) => probe.listen(0, "127.0.0.1", resolve));
    const port = (probe.address() as { port: number }).port;
    await new Promise<void>((resolve) => probe.close(() => resolve()));
    site.origin = `http://127.0.0.1:${port}`;
    const server = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
      cwd: fileURLToPath(new URL("../", import.meta.url)),
      env: { ...process.env, NODE_ENV: "production", API_INTERNAL_URL: `http://127.0.0.1:${(upstream.address() as { port: number }).port}`, NEXT_TELEMETRY_DISABLED: "1" },
      stdio: ["ignore", "pipe", "pipe"], windowsHide: true,
    });
    let logs = "";
    server.stdout.on("data", (chunk) => { logs = `${logs}${chunk}`.slice(-12_000); });
    server.stderr.on("data", (chunk) => { logs = `${logs}${chunk}`.slice(-12_000); });
    server.on("error", (error) => { logs += error.message; });
    const observe = (page: Page) => {
      page.on("pageerror", (error) => site.errors.push(error.message));
      page.on("console", (message) => {
        if (message.type() === "error" && message.location().url.startsWith(canonical)
          && !message.text().includes("Content Security Policy")) site.errors.push(message.text());
      });
    };
    context.pages().forEach(observe);
    context.on("page", observe);
    try {
      await expect.poll(async () => {
        try { return (await request.get(`${site.origin}/api/travel/auth/me`, { timeout: 1_000, maxRedirects: 0 })).status(); }
        catch { return 0; }
      }, { timeout: 30_000 }).toBe(200);
      site.api.length = 0;
      // Canonical browser URLs are fully intercepted. This exercises production
      // Host/origin gates without adding any production bypass switch.
      await context.route("**/*", async (route) => {
        const url = new URL(route.request().url());
        if (url.href === STAY22_SCRIPT_URL) {
          site.sdkLoads.push(url.href);
          if (site.sdk === "fail") return route.abort();
          return route.fulfill({ contentType: "application/javascript", body: site.sdk === "rewrite" ? mockSdk : "window.__stay22Mock={lmaID:window.Stay22.params.lmaID,documentUrl:location.href};" });
        }
        if (url.hostname === "emrldtp.cc") {
          site.driveLoads.push(url.href);
          return route.fulfill({ contentType: "application/javascript", body: "/* Isolated inert Drive fixture */" });
        }
        if (["stay22.example.test", "hotel.example.test"].includes(url.hostname)) {
          site.popupLoads.push(url.href);
          return route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Isolated hotel link</title><h1>Fixture only</h1>" });
        }
        if (["mokaair.com", "www.mokaair.com", "preview.example.test"].includes(url.hostname) || url.origin === site.origin) {
          const headers = { ...await route.request().allHeaders(), host: url.host, "x-forwarded-host": url.host, "x-forwarded-proto": url.protocol.slice(0, -1) };
          const response = await route.fetch({ url: `${site.origin}${url.pathname}${url.search}`, headers, maxRedirects: 0 });
          return route.fulfill({ response });
        }
        site.blocked.push(url.href);
        return route.abort();
      });
      await runTest(site);
    } finally {
      await testInfo.attach("isolated-script-server", { body: logs, contentType: "text/plain" });
      if (server.exitCode === null && server.signalCode === null) {
        const exited = once(server, "exit"); server.kill(); await exited;
      }
      upstream.closeAllConnections();
      await new Promise<void>((resolve) => upstream.close(() => resolve()));
    }
  },
});

async function sheet(page: Page) {
  const opener = page.getByRole("button", { name: copy.open, exact: true });
  await opener.click();
  const dialog = page.getByRole("dialog", { name: hotel.title, exact: true });
  await expect(dialog).toBeVisible();
  return { opener, dialog };
}

test("public Script rewrites dynamically opened original links without Allez double-wrapping", async ({ page, context, site }) => {
  await context.addCookies([{ name: "travel_access", value: "synthetic-private-session", url: canonical, httpOnly: true, secure: true }]);
  await page.goto(`${canonical}${publicPath}`);
  await expect(page.getByRole("heading", { name: copy.title, exact: true })).toBeVisible();
  await expect.poll(() => site.sdkLoads.length).toBe(1);
  await expect.poll(() => page.evaluate(() => (window as MockWindow).__stay22Mock?.lmaID)).toBe(fixtureLmaId);
  expect(site.api.some((call) => /\/auth\/|\/saved-items|\/trips/.test(call.path))).toBe(false);
  expect(site.api.filter((call) => call.path.includes("stay22-script")).every((call) => !call.cookie && !call.authorization)).toBe(true);
  await expect(page.getByText("private-fixture@example.test")).toHaveCount(0);
  await expect(page.locator("#travelpayouts-drive")).toHaveCount(0);
  expect(site.driveLoads).toEqual([]);
  const { opener, dialog } = await sheet(page);
  const booking = dialog.getByRole("link", { name: /前往 Booking.com/ });
  await expect(booking).toHaveAttribute("href", /^https:\/\/stay22\.example\.test\/booking\?/);
  expect(new URL((await booking.getAttribute("href"))!).searchParams.get("link")).toBe(bookingUrl);
  await expect(dialog.getByRole("link", { name: /飯店官網/ })).toHaveAttribute("href", officialUrl);
  await expect(dialog.locator("form")).toHaveCount(0);
  await expect(dialog.locator("input[type=date]")).toHaveCount(0);
  await expect(dialog.getByText(copy.dateNotice)).toBeVisible();
  await expect(booking).toHaveAttribute("rel", "sponsored noopener noreferrer");
  expect((await booking.boundingBox())!.height).toBeGreaterThanOrEqual(44);
  const popupPromise = context.waitForEvent("page");
  await booking.click();
  const popup = await popupPromise;
  await expect(popup).toHaveTitle("Isolated hotel link");
  expect(await popup.evaluate(() => window.opener === null)).toBe(true);
  await popup.close();
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(opener).toBeFocused();
  const reopened = await sheet(page);
  await expect(reopened.dialog.getByRole("link", { name: /前往 Booking.com/ })).toHaveAttribute("href", /^https:\/\/stay22\.example\.test\/booking\?/);
  expect(site.sdkLoads).toHaveLength(1);
  expect(site.api.some((call) => call.path.endsWith("/clickout"))).toBe(false);
  expect(site.blocked).toEqual([]);
  expect(site.errors).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  const bounds = await reopened.dialog.boundingBox();
  expect(bounds!.x).toBeGreaterThanOrEqual(0);
  expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(page.viewportSize()!.width + 1);
  await page.screenshot({ path: test.info().outputPath("stay22-script-public-panel.png") });
});

test("SDK load failure retains honest original hotel links", async ({ page, site }) => {
  site.sdk = "fail";
  await page.goto(`${canonical}${publicPath}`);
  await expect(page.getByRole("status").filter({ hasText: copy.scriptUnavailable })).toBeVisible();
  const { dialog } = await sheet(page);
  await expect(dialog.getByRole("link", { name: /前往 Booking.com/ })).toHaveAttribute("href", bookingUrl);
  await expect(dialog.getByRole("link", { name: /飯店官網/ })).toHaveAttribute("href", officialUrl);
  expect(site.api.some((call) => call.path.endsWith("/clickout"))).toBe(false);
  expect(site.blocked).toEqual([]);
});

test("saved mode toggle takes effect on reload and preserves the original Allez panel when off", async ({ page, site }) => {
  site.mode = "allez";
  await page.goto(`${canonical}${publicPath}?type=hotel`);
  await expect(page.locator(".public-app-shell")).toBeVisible();
  await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
  expect(site.sdkLoads).toEqual([]);
  site.mode = "script";
  await page.reload();
  await expect(page.getByRole("heading", { name: copy.title, exact: true })).toBeVisible();
  await expect.poll(() => site.sdkLoads.length).toBe(1);
  site.mode = "off";
  await page.reload();
  await expect(page.locator(".public-app-shell")).toBeVisible();
  expect(site.sdkLoads).toHaveLength(1);
  expect(await page.evaluate(() => (window as MockWindow).__stay22Mock)).toBeUndefined();
  const original = await sheet(page);
  await expect(original.dialog.locator('form[action*="booking-options"]')).toHaveCount(1);
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  expect(site.blocked).toEqual([]);
  expect(site.errors).toEqual([]);
});

for (const mode of ["error", "invalid"] as const) {
  test(`${mode} public configuration fails closed to the original page`, async ({ page, site }) => {
    site.mode = mode;
    await page.goto(`${canonical}${publicPath}?type=hotel`);
    await expect(page.locator(".public-app-shell")).toBeVisible();
    await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
    expect(site.sdkLoads).toEqual([]);
    await expect(page.locator("#stay22-lma")).toHaveCount(0);
    expect(site.blocked).toEqual([]);
    expect(site.errors).toEqual([]);
  });
}

for (const privacy of ["dnt", "gpc"] as const) {
  test(`${privacy} never loads Script or requests a public vendor configuration`, async ({ page, context, site }) => {
    await context.setExtraHTTPHeaders(privacy === "dnt" ? { DNT: "1" } : { "Sec-GPC": "1" });
    await context.addInitScript((signal) => {
      Object.defineProperty(navigator, signal === "dnt" ? "doNotTrack" : "globalPrivacyControl", { configurable: true, get: () => signal === "dnt" ? "1" : true });
    }, privacy);
    await page.goto(`${canonical}${publicPath}?type=hotel`);
    await expect(page.locator(".public-app-shell")).toBeVisible();
    await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
    expect(site.sdkLoads).toEqual([]);
    expect(site.api.some((call) => call.path.endsWith("stay22-script-config"))).toBe(false);
    expect(site.blocked).toEqual([]);
  });
}

test("localhost and preview origins cannot load Script even when server configuration is enabled", async ({ page, site }) => {
  for (const origin of [site.origin, "https://preview.example.test"]) {
    await page.goto(`${origin}${publicPath}?type=hotel`);
    await expect(page.locator(".public-app-shell")).toBeVisible();
    await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
    await expect(page.locator("#stay22-lma")).toHaveCount(0);
  }
  expect(site.sdkLoads).toEqual([]);
  expect(site.blocked).toEqual([]);
});

test("non-hotel and conflicting category queries preserve the original service page", async ({ page, site }) => {
  for (const query of ["type=tour", "type=hotel&type=esim"]) {
    await page.goto(`${canonical}${publicPath}?${query}`);
    await expect(page.locator(".public-app-shell")).toBeVisible();
    await expect(page).toHaveURL(`${canonical}${publicPath}?${query}`);
    await expect(page.locator("#stay22-lma")).toHaveCount(0);
  }
  expect(site.sdkLoads).toEqual([]);
  expect(site.api.some((call) => call.path.endsWith("stay22-script-config"))).toBe(false);
  expect(site.blocked).toEqual([]);
});

test("public to private navigation discards vendor document state and back returns to public content", async ({ page, site }) => {
  await page.goto(`${canonical}${publicPath}`);
  await expect.poll(() => site.sdkLoads.length).toBe(1);
  await page.evaluate(() => { (window as MockWindow).__publicDocumentMarker = "discard-before-private"; });
  const navigation = page.waitForURL(`${canonical}/zh-TW/trips`);
  await page.getByRole("link", { name: copy.trips, exact: true }).click();
  await navigation;
  await expect(page.locator(".public-app-shell")).toBeVisible();
  expect(await page.evaluate(() => (window as MockWindow).__publicDocumentMarker)).toBeUndefined();
  expect(await page.evaluate(() => (window as MockWindow).__stay22Mock)).toBeUndefined();
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  await page.goBack();
  await expect(page.getByRole("heading", { name: copy.title, exact: true })).toBeVisible();
  await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
  expect(site.blocked).toEqual([]);
  expect(site.errors).toEqual([]);
});

test("destination navigation from a transfer page creates a fresh public document", async ({ page, site }) => {
  await page.goto(`${canonical}${publicPath}?type=transfer`);
  await expect(page.locator(".public-app-shell")).toBeVisible();
  await page.evaluate(() => { (window as MockWindow).__publicDocumentMarker = "old-transfer-document"; });
  await page.locator('nav a[href="/zh-TW/destinations/osaka/services"]').click();
  await expect(page).toHaveURL(`${canonical}/zh-TW/destinations/osaka/services`);
  await expect(page.getByRole("heading", { name: copy.title, exact: true })).toBeVisible();
  expect(await page.evaluate(() => (window as MockWindow).__publicDocumentMarker)).toBeUndefined();
  await expect(page.locator(".public-app-shell")).toHaveCount(0);
  // The source's query is unsafe for document.referrer, so keep original links
  // in this public document instead of leaking that query to the mock SDK.
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  expect(site.sdkLoads).toEqual([]);
  expect(site.blocked).toEqual([]);
});

test("destinations outside the reviewed Script catalogue retain their original page", async ({ page, site }) => {
  await page.goto(`${canonical}/zh-TW/destinations/fukuoka/services?type=hotel`);
  await expect(page.locator(".public-app-shell")).toBeVisible();
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  expect(site.api.some((call) => call.path.endsWith("stay22-script-config"))).toBe(false);
  expect(site.sdkLoads).toEqual([]);
  expect(site.blocked).toEqual([]);
});

test("native navigation from a private document cannot expose its referrer to Script", async ({ page, site }) => {
  await page.goto(`${canonical}/zh-TW/trips?private_condition=fixture`);
  await expect(page.locator(".public-app-shell")).toBeVisible();
  // A fixture link exercises the browser's native document.referrer behavior;
  // it is not a claim that the empty private-trip UI contains this control.
  await page.evaluate((href) => {
    const anchor = document.createElement("a");
    anchor.href = href;
    anchor.id = "fixture-public-catalog";
    anchor.textContent = "Open public hotel fixture";
    anchor.style.cssText = "position:fixed;top:8px;left:8px;z-index:1000;background:white;padding:12px";
    document.body.appendChild(anchor);
  }, `${canonical}${publicPath}`);
  await page.locator("#fixture-public-catalog").click();
  await expect(page).toHaveURL(`${canonical}${publicPath}`);
  await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
  expect(await page.evaluate(() => document.referrer)).toContain("/zh-TW/trips");
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  expect(site.sdkLoads).toEqual([]);
  await page.goto("about:blank");
  await page.goto(`${canonical}${publicPath}`);
  await expect.poll(() => site.sdkLoads.length).toBe(1);
  expect(site.blocked).toEqual([]);
});

test("private query conditions are removed before Script and URL fragments prevent loading", async ({ page, site }) => {
  await page.goto(`${canonical}${publicPath}?trip_id=private-fixture&check_in=2099-11-10`);
  await expect(page).toHaveURL(`${canonical}${publicPath}`);
  await expect.poll(() => site.sdkLoads.length).toBe(1);
  await expect.poll(() => page.evaluate(() => (window as MockWindow).__stay22Mock?.documentUrl)).toBe(`${canonical}${publicPath}`);
  await page.goto("about:blank");
  await page.goto(`${canonical}${publicPath}#private-note`);
  await expect(page.getByRole("heading", { name: hotel.title })).toBeVisible();
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  expect(site.sdkLoads).toHaveLength(1);
  expect(site.blocked).toEqual([]);
});
