import { expect, test as base, type Page } from "@playwright/test";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { existsSync, readFileSync } from "node:fs";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { defaultUsageCatalog } from "../lib/usage-catalog";
import type { Stay22AllezCopy } from "../lib/stay22-allez-copy";
import { klookAffiliateCopy } from "../lib/klook-affiliate-copy";
import { siteFeatureKeys } from "../lib/site-features";
import { stay22ScriptCopy } from "../lib/stay22-script-copy";
import { STAY22_SCRIPT_URL } from "../lib/stay22-script";
import { localeLabels, locales } from "../i18n/routing";

const canonical = "https://mokaair.com";
const publicPath = "/zh-TW/destinations/tokyo/services";
const hotelId = "10000000-0000-4000-8000-000000000001";
const bookingId = "20000000-0000-4000-8000-000000000001";
const fixtureLmaId = "000000000000000000000001";
const bookingUrl = "https://www.booking.com/hotel/jp/script-fixture.html";
const officialUrl = "https://hotel.example.test/access";
const copy = stay22ScriptCopy("zh-TW");
const bookingCopy: Stay22AllezCopy = JSON.parse(readFileSync(new URL("../lib/stay22-allez-messages/zh-TW.json", import.meta.url), "utf8"));
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
  optionFailure: boolean; operatingRules: boolean; sdkLoads: string[]; driveLoads: string[]; blocked: string[];
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
    const site: Fixture = { origin: "", mode: "script", sdk: "rewrite", optionFailure: false, operatingRules: false, sdkLoads: [], driveLoads: [], blocked: [], popupLoads: [], api: [], errors: [] };
    const upstream = createServer((incoming, outgoing) => {
      incoming.resume();
      const url = new URL(incoming.url || "/", "http://127.0.0.1");
      site.api.push({ path: url.pathname, method: incoming.method || "GET", cookie: incoming.headers.cookie || "", authorization: incoming.headers.authorization || "" });
      const fixtureHotel = { ...hotel, facts: { ...hotel.facts, ...(site.operatingRules ? {
        hotel_operating_rules: { unavailable_stays: [{ start_date: "2099-11-10", end_date: "2099-11-12", reason: "Synthetic maintenance exclusion", source_url: "https://hotel.example.test/notice" }] },
      } : {}) } };
      let result: unknown = {};
      if (url.pathname === "/api/v1/travel-services/stay22-script-config") {
        outgoing.statusCode = site.mode === "error" ? 503 : 200;
        result = { enabled: site.mode === "script" || site.mode === "invalid", integration_mode: site.mode === "allez" ? "allez" : "script", lma_id: site.mode === "invalid" ? "unexpected-id" : site.mode === "script" ? fixtureLmaId : null };
      } else if (url.pathname.endsWith("/stay22-script-options")) {
        outgoing.statusCode = site.optionFailure ? 503 : site.mode !== "script" ? 404 : site.operatingRules ? 422 : 200;
        result = { title: hotel.title, destination_id: "tokyo", options: outgoing.statusCode === 200 ? [
          { id: bookingId, provider: "booking", name: "Booking.com", url: bookingUrl },
          { id: "official-option", provider: "official", name: "Official website", url: officialUrl },
        ] : [] };
      } else if (url.pathname === "/api/v1/travel-services") result = { enabled: true, enabled_kinds: ["hotel"], destinations: ["tokyo"], items: [fixtureHotel], areas: [], selections: [] };
      else if (url.pathname === "/api/v1/travel-services/config") result = { public_enabled: true, enabled_kinds: ["hotel"], enabled_destinations: ["tokyo"] };
      else if (url.pathname === `/api/v1/travel-services/${hotelId}/booking-details`) result = fixtureHotel;
      // Ordinary exact-hotel booking must not depend on the discovery switch.
      else if (url.pathname === "/api/v1/discovery/status") result = { enabled: false };
      else if (url.pathname.startsWith("/api/v1/discovery/")) { outgoing.statusCode = 404; result = { detail: "Discovery is disabled" }; }
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
    let shuttingDown = false;
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
      // Browser offline mode is an independent transport guard: Playwright can
      // skip a route handler after a fulfilled redirect. Local Node route.fetch
      // still works, but an escaped browser request cannot reach the network.
      await context.setOffline(true);
      // Canonical browser URLs are fully intercepted. This exercises production
      // Host/origin gates without adding any production bypass switch.
      await context.route("**/*", async (route) => {
        const url = new URL(route.request().url());
        if (url.hostname === "offline-canary.invalid") return route.continue();
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
          try {
            const response = await route.fetch({ url: `${site.origin}${url.pathname}${url.search}`, headers, maxRedirects: 0 });
            // Query stripping is tested separately over local HTTP with redirects
            // disabled. Never return a redirect that can escape browser routing.
            if (response.status() >= 300 && response.status() < 400 && response.headers().location) {
              throw new Error(`Unexpected browser fixture redirect: ${url.pathname}`);
            }
            return await route.fulfill({ response });
          } catch (error) {
            if (!shuttingDown) throw error;
            return;
          }
        }
        site.blocked.push(url.href);
        return route.abort();
      });
      const canary = await context.newPage();
      await expect(canary.goto("https://offline-canary.invalid/probe")).rejects.toThrow("ERR_INTERNET_DISCONNECTED");
      await canary.close();
      await runTest(site);
    } finally {
      await testInfo.attach("isolated-script-server", { body: logs, contentType: "text/plain" });
      // Close pages before their local transport. Otherwise legacy Link prefetch
      // may still be using route.fetch and fail with ECONNRESET during teardown.
      shuttingDown = true;
      await context.close();
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

test("public top language links use clean native destinations without account requests", async ({ page, context, site }) => {
  await context.addCookies([{ name: "travel_access", value: "synthetic-private-session", url: canonical, httpOnly: true, secure: true }]);
  await page.goto(`${canonical}${publicPath}#private-note`);
  const language = page.getByRole("banner").getByRole("navigation", { name: "語言", exact: true });
  await expect(language).toBeVisible();
  await expect(language.getByRole("link")).toHaveCount(5);
  for (const locale of locales) {
    const link = language.getByRole("link", { name: localeLabels[locale], exact: true });
    await expect(link).toHaveAttribute("href", `/${locale}/destinations/tokyo/services`);
    await expect(link).toBeVisible();
    expect((await link.boundingBox())!.height).toBeGreaterThanOrEqual(44);
  }
  expect(site.sdkLoads).toEqual([]);
  await page.evaluate(() => { (window as MockWindow).__publicDocumentMarker = "old-language-document"; });
  await language.getByRole("link", { name: "English", exact: true }).click();
  await expect(page).toHaveURL(`${canonical}/en/destinations/tokyo/services`);
  await expect(page.getByRole("heading", { name: stay22ScriptCopy("en").title, exact: true })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Language", exact: true }).getByRole("link", { name: "English", exact: true })).toHaveAttribute("aria-current", "page");
  expect(await page.evaluate(() => (window as MockWindow).__publicDocumentMarker)).toBeUndefined();
  expect(site.api.some((call) => /\/auth\/|\/saved-items|\/trips/.test(call.path))).toBe(false);
  expect(site.api.every((call) => call.method === "GET" && !call.cookie && !call.authorization)).toBe(true);
  expect(site.blocked).toEqual([]);
  expect(site.errors).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
});

test("isolated public hotel controls keep stored dark palettes and semantic button contrast", async ({ page, context, site }) => {
  await context.addInitScript(() => {
    if (location.origin === "https://mokaair.com") {
      localStorage.setItem("mokaair-theme", "dark");
      if (!localStorage.getItem("mokaair-palette")) localStorage.setItem("mokaair-palette", "mocha");
    }
  });
  await page.goto(`${canonical}${publicPath}`);
  for (const [palette, foreground] of [["mocha", "rgb(17, 44, 41)"], ["lagoon", "rgb(8, 45, 64)"], ["forest", "rgb(27, 52, 31)"]]) {
    if (palette !== "mocha") {
      await page.evaluate((value) => localStorage.setItem("mokaair-palette", value), palette);
      await page.reload();
    }
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    await expect(page.locator("html")).toHaveAttribute("data-palette", palette);
    const opener = page.getByRole("button", { name: copy.open, exact: true });
    await expect(opener).toBeVisible();
    await expect(opener).toHaveCSS("color", foreground);
    const ratio = await opener.evaluate((element) => {
      const style = getComputedStyle(element);
      const luminance = (color: string) => {
        const channels = color.match(/[\d.]+/g)?.map(Number);
        if (!channels || channels.length !== 3) throw new Error(`Expected opaque RGB colour, got ${color}`);
        return channels.map((channel) => { const value = channel / 255; return value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4; })
          .reduce((sum, channel, index) => sum + channel * [.2126, .7152, .0722][index], 0);
      };
      const values = [luminance(style.color), luminance(style.backgroundColor)];
      return (Math.max(...values) + .05) / (Math.min(...values) + .05);
    });
    expect(ratio, `${palette} public hotel button`).toBeGreaterThanOrEqual(4.5);
  }
  expect(site.api.some((call) => /\/auth\/|\/saved-items|\/trips/.test(call.path))).toBe(false);
  expect(site.blocked).toEqual([]);
  expect(site.errors).toEqual([]);
});

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
  expect(site.api.filter((call) => call.path.includes("stay22-script")).every((call) => !call.cookie && !call.authorization)).toBe(true);
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
  await page.goto(`${canonical}${publicPath}`);
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

test("non-hotel and conflicting category queries preserve the original service page", async ({ page, request, site }) => {
  await page.goto(`${canonical}${publicPath}?type=tour`);
  await expect(page.getByRole("button", { name: klookAffiliateCopy("zh-TW").tour, exact: true })).toHaveAttribute("aria-pressed", "true");
  await expect(page).toHaveURL(`${canonical}${publicPath}?type=tour`);
  await expect(page.locator(".public-app-shell")).toBeVisible();
  await expect(page.locator("#stay22-lma")).toHaveCount(0);

  const conflictingPath = `${publicPath}?type=hotel&type=esim`;
  const initial = await request.get(`${site.origin}${conflictingPath}`, {
    headers: { Host: "mokaair.com", "X-Forwarded-Host": "mokaair.com", "X-Forwarded-Proto": "https" }, maxRedirects: 0,
  });
  expect(initial.status()).toBe(200);
  expect(initial.headers().location).toBeUndefined();
  const html = await initial.text();
  expect(html).toContain("public-app-shell");
  expect(html).not.toContain(STAY22_SCRIPT_URL);
  expect(site.api.some((call) => call.path.endsWith("stay22-script-config"))).toBe(false);

  await page.goto(`${canonical}${conflictingPath}`);
  // DestinationServices rejects the repeated type array as an initial category.
  // Once hydrated, ServiceCatalog's filter effect selects all and removes type
  // with history.replaceState. This is not a redirect or a new Script document.
  await expect(page).toHaveURL(`${canonical}${publicPath}`);
  await expect(page.getByRole("button", { name: "全部", exact: true })).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator(".public-app-shell")).toBeVisible();
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
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

test("restricted hotel entry discards the SDK document and opens booking dates with discovery disabled", async ({ page, request, site }) => {
  site.operatingRules = true;
  const discovery = await request.get(`${site.origin}/api/travel/discovery/status`);
  expect(await discovery.json()).toMatchObject({ enabled: false });
  await page.goto(`${canonical}${publicPath}`);
  await expect.poll(() => page.evaluate(() => (window as MockWindow).__stay22Mock?.lmaID)).toBe(fixtureLmaId);
  await expect(page.locator("form,input,iframe")).toHaveCount(0);
  expect(site.api.some((call) => /\/auth\/|\/saved-items|\/trips/.test(call.path))).toBe(false);
  const entry = page.getByRole("link", { name: bookingCopy.scriptDateEntry, exact: true });
  const exactPath = `/zh-TW/hotels/${hotelId}`;
  await expect(entry).toHaveAttribute("href", exactPath);
  expect(await entry.getAttribute("target")).toBeNull();
  await expect(page.getByRole("button", { name: copy.open, exact: true })).toHaveCount(0);
  expect(site.api.some((call) => call.path.endsWith("/stay22-script-options"))).toBe(false);
  await page.evaluate(() => { (window as MockWindow).__publicDocumentMarker = "discard-before-hotel-dates"; });
  await entry.click();
  await expect(page).toHaveURL(`${canonical}${exactPath}`);
  await expect(page.locator(".public-app-shell")).toBeVisible();
  expect(await page.evaluate(() => (window as MockWindow).__publicDocumentMarker)).toBeUndefined();
  expect(await page.evaluate(() => (window as MockWindow).__stay22Mock)).toBeUndefined();
  await expect(page.locator("#stay22-lma")).toHaveCount(0);
  const panel = page.getByRole("dialog", { name: hotel.title, exact: true });
  await expect(panel.getByLabel(bookingCopy.checkIn, { exact: true })).toBeVisible();
  await expect(panel.getByLabel(bookingCopy.checkOut, { exact: true })).toBeVisible();
  await expect(panel.getByRole("checkbox", { name: bookingCopy.omitDates })).toHaveCount(0);
  await expect(panel.locator(`form[action*="booking-options/${bookingId}/clickout"]`)).toHaveCount(1);
  await panel.getByLabel(bookingCopy.checkIn, { exact: true }).fill("2099-11-09");
  await panel.getByLabel(bookingCopy.checkOut, { exact: true }).fill("2099-11-10");
  expect(site.sdkLoads).toHaveLength(1);
  expect(site.api.some((call) => call.path === `/api/v1/travel-services/${hotelId}/booking-details`)).toBe(true);
  expect(site.api.some((call) => call.path.startsWith("/api/v1/discovery/") && !call.path.endsWith("/status"))).toBe(false);
  expect(site.api.some((call) => call.path.endsWith("/clickout"))).toBe(false);
  expect(site.blocked).toEqual([]);
  expect(site.errors).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
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

test("private query conditions are removed before Script and URL fragments prevent loading", async ({ page, request, site }) => {
  // Verify the actual Next redirect over local HTTP, then open its clean target
  // as a separate browser navigation. Fulfilled browser redirects can bypass
  // Playwright routing; offline mode would stop them, not silently call live.
  const redirect = await request.get(`${site.origin}${publicPath}?trip_id=private-fixture&check_in=2099-11-10`, {
    headers: { Host: "mokaair.com", "X-Forwarded-Host": "mokaair.com", "X-Forwarded-Proto": "https" }, maxRedirects: 0,
  });
  expect(redirect.status()).toBe(307);
  const target = new URL(redirect.headers().location, canonical);
  expect(target.href).toBe(`${canonical}${publicPath}`);
  expect(await redirect.text()).not.toContain(STAY22_SCRIPT_URL);
  await page.goto(target.href);
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
