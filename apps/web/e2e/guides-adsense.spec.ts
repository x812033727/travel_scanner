import { expect, test as base, type Route } from "@playwright/test";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defaultUsageCatalog } from "../lib/usage-catalog";
import { siteFeatureKeys } from "../lib/site-features";
import { ADSENSE_SCRIPT_ORIGIN } from "../lib/adsense";

/**
 * Advertising is decided on the server, cached per process, and gated on the production
 * origin — so it cannot be toggled through the shared e2e fixture without leaking into every
 * other spec. This file spawns its own Next server and its own API double, the way
 * `stay22-script.spec.ts` does, and drives it through the canonical host.
 */
const canonical = "https://mokaair.com";
const PUBLISHER = "ca-pub-4140966684432854";
const SLOT = "1234567890";
const articlePath = "/zh-TW/guides/howto/tokyo-esim";
const hubPath = "/zh-TW/guides/howto";
const AD_LABEL = "廣告";

const paragraph = (text: string) => ({ type: "paragraph", text });
const article = {
  slug: "tokyo-esim", kind: "howto", locale: "zh-TW", status: "published",
  destination_id: null, destination_label: null, topics: [], valid_until: null, expired: false,
  published_locales: ["zh-TW"],
  document: {
    title: "東京 eSIM 怎麼選", description: "三家方案比較", version: 1,
    published_at: "2026-09-10T00:00:00Z", modified_at: null, hero: null, sources: [],
    blocks: [
      { type: "heading", text: "先看流量", level: 2 }, paragraph("先決定一天要用多少。"),
      ...Array.from({ length: 8 }, (_, index) => paragraph(`第 ${index + 1} 段內文。`)),
    ],
  },
};

type Fixture = { origin: string; enabled: boolean; cmp: boolean; adRequests: string[] };

/**
 * Forward a canonical-host request to the isolated server.
 *
 * Router prefetches for other routes keep arriving while a test finishes, and a reset or a
 * closed context must not be reported as a failure of what the test was actually checking.
 */
async function proxyToSite(route: Route, origin: string) {
  const url = new URL(route.request().url());
  const headers = {
    ...await route.request().allHeaders(),
    host: url.host, "x-forwarded-host": url.host, "x-forwarded-proto": url.protocol.slice(0, -1),
  };
  try {
    const response = await route.fetch({ url: `${origin}${url.pathname}${url.search}`, headers, maxRedirects: 0 });
    return await route.fulfill({ response });
  } catch {
    return route.abort().catch(() => undefined);
  }
}

const test = base.extend<{ site: Fixture }>({
  site: async ({ context, request }, runTest) => {
    test.skip(!existsSync(new URL("../.next/BUILD_ID", import.meta.url)), "Run next build for isolated AdSense coverage");
    const site: Fixture = { origin: "", enabled: true, cmp: false, adRequests: [] };
    const upstream = createServer((incoming, outgoing) => {
      incoming.resume();
      const url = new URL(incoming.url || "/", "http://127.0.0.1");
      let result: unknown = {};
      if (url.pathname === "/api/v1/ads/config") {
        // The server double applies the same privacy rule the real endpoint does.
        const tracking = incoming.headers.dnt !== "1" && incoming.headers["sec-gpc"] !== "1";
        result = site.enabled && tracking
          ? { enabled: true, publisher_id: PUBLISHER, slot_id: SLOT, cmp_enabled: site.cmp }
          : { enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false };
      } else if (url.pathname === "/api/v1/guides/howto/tokyo-esim") result = article;
      else if (url.pathname.startsWith("/api/v1/guides/topics")) result = { items: [] };
      else if (url.pathname.startsWith("/api/v1/guides")) result = { articles: [], total: 0 };
      else if (url.pathname === "/api/v1/runtime/site-visibility") result = Object.fromEntries(siteFeatureKeys.map((key) => [`${key}_enabled`, true]));
      else if (url.pathname === "/api/v1/usage-catalog") result = defaultUsageCatalog;
      else if (url.pathname === "/api/v1/analytics/config") result = { first_party_enabled: false, ga4_enabled: false };
      else if (url.pathname === "/api/v1/community/status") result = { enabled: false };
      else if (url.pathname === "/api/v1/discovery/status") result = { enabled: false };
      else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) result = { locale: "zh-TW", version: "fixture", entries: {} };
      else if (url.pathname === "/api/v1/auth/me") { outgoing.statusCode = 401; result = { detail: "anonymous" }; }
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
    try {
      await expect.poll(async () => {
        try { return (await request.get(`${site.origin}${hubPath}`, { timeout: 1_000, maxRedirects: 0 })).status(); }
        catch { return 0; }
      }, { timeout: 30_000 }).toBe(200);
      // Offline is an independent transport guard: nothing this page asks for may leave.
      await context.setOffline(true);
      await context.route("**/*", async (route) => {
        const url = new URL(route.request().url());
        if (url.origin === ADSENSE_SCRIPT_ORIGIN) {
          site.adRequests.push(url.href);
          return route.fulfill({ contentType: "application/javascript", body: "/* isolated inert AdSense fixture */" });
        }
        if (["mokaair.com", "www.mokaair.com"].includes(url.hostname) || url.origin === site.origin) {
          return proxyToSite(route, site.origin);
        }
        return route.abort().catch(() => undefined);
      });
      await runTest(site);
      await context.unrouteAll({ behavior: "ignoreErrors" });
    } finally {
      server.kill("SIGKILL");
      await new Promise<void>((resolve) => upstream.close(() => resolve()));
    }
  },
});

test("an article carries one labelled slot with its box already reserved", async ({ page, site }) => {
  await page.goto(`${canonical}${articlePath}`);
  const slot = page.locator("ins.adsbygoogle");
  await expect(slot).toHaveCount(1);
  await expect(page.getByText(AD_LABEL, { exact: true })).toBeVisible();
  await expect(slot).toHaveAttribute("data-ad-client", PUBLISHER);
  await expect(slot).toHaveAttribute("data-ad-slot", SLOT);
  // Reserved before the ad arrives: an unreserved box is a layout shift on every page view.
  expect(await slot.evaluate((node) => node.getBoundingClientRect().height)).toBeGreaterThan(100);
  // Below the headline, never the first thing in the body.
  const heading = await page.locator("h1").boundingBox();
  expect((await slot.boundingBox())!.y).toBeGreaterThan(heading!.y);
  await expect.poll(() => site.adRequests.length, { timeout: 10_000 }).toBeGreaterThan(0);
  expect(site.adRequests.every((url) => url.includes(`client=${PUBLISHER}`))).toBe(true);
});

test("without a consent message the tag is told to serve non-personalised ads", async ({ page, site }) => {
  await page.goto(`${canonical}${articlePath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(1);
  // Personalised ads in the EEA, the UK or Switzerland need a certified CMP; with none
  // published, this flag is the only thing keeping the page inside the policy.
  await expect.poll(() => page.evaluate(() => window.adsbygoogle?.requestNonPersonalizedAds))
    .toBe(1);
  expect(site.adRequests.every((url) => url.includes(`client=${PUBLISHER}`))).toBe(true);
});

test("a published consent message leaves personalisation to the reader's answer", async ({ page, site }) => {
  site.cmp = true;
  await page.goto(`${canonical}${articlePath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(1);
  // Forcing the flag here would override whatever the reader chose in Google's message.
  expect(await page.evaluate(() => window.adsbygoogle?.requestNonPersonalizedAds)).toBeUndefined();
});

test("a browser asking not to be tracked gets no slot and no request", async ({ browser, site }) => {
  const context = await browser.newContext({ extraHTTPHeaders: { "Sec-GPC": "1" } });
  const page = await context.newPage();
  await page.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin === ADSENSE_SCRIPT_ORIGIN) {
      site.adRequests.push(url.href);
      return route.abort().catch(() => undefined);
    }
    return proxyToSite(route, site.origin);
  });
  site.adRequests.length = 0;
  await page.goto(`${canonical}${articlePath}`);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  // Not even the reserved space: the page is exactly the page it is with advertising off.
  await expect(page.getByText(AD_LABEL, { exact: true })).toHaveCount(0);
  expect(site.adRequests).toEqual([]);
  await page.unrouteAll({ behavior: "ignoreErrors" });
  await context.close();
});

test("a hub is a listing, not an article, so it carries nothing", async ({ page, site }) => {
  site.adRequests.length = 0;
  await page.goto(`${canonical}${hubPath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  expect(site.adRequests).toEqual([]);
});

test("only an article route relaxes the content security policy", async ({ request, site }) => {
  const article = await request.get(`${site.origin}${articlePath}`, { headers: { host: "mokaair.com", "x-forwarded-host": "mokaair.com", "x-forwarded-proto": "https" } });
  const hub = await request.get(`${site.origin}${hubPath}`, { headers: { host: "mokaair.com", "x-forwarded-host": "mokaair.com", "x-forwarded-proto": "https" } });
  expect(article.headers()["content-security-policy-report-only"]).toContain("'unsafe-eval'");
  expect(hub.headers()["content-security-policy-report-only"]).not.toContain("'unsafe-eval'");
  expect(hub.headers()["content-security-policy-report-only"]).toContain("frame-src https://www.google.com https://www.stay22.com https://www.youtube-nocookie.com;");
});

test("ads.txt is served verbatim and is not sent through locale routing", async ({ request, site }) => {
  const response = await request.get(`${site.origin}/ads.txt`, { maxRedirects: 0 });
  expect(response.status()).toBe(200);
  expect((await response.text()).trim()).toBe("google.com, pub-4140966684432854, DIRECT, f08c47fec0942fa0");
});
