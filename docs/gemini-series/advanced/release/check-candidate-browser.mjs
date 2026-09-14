/** Reuse the verified Next build with candidate API responses; no public/authenticated traffic. */
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { pathToFileURL } from "node:url";
import path from "node:path";
import { chromium } from "playwright";

const here = import.meta.dirname, root = path.resolve(here, "../../../..");
const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const hash = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");
const prepared = json(path.join(here, "../platform/next-integration/prepared.json"));
const catalogue = json(path.join(here, "candidate/guide-series.json"));
assert.deepEqual(catalogue, json(path.join(prepared.web, "lib/guide-series.json")));
const { workspace } = json(path.join(here, ".workspaces/latest.json"));
const { siteFeatureKeys } = await import(pathToFileURL(path.join(root, "apps/web/lib/site-features.ts")).href);
const { defaultUsageCatalog } = await import(pathToFileURL(path.join(root, "apps/web/lib/usage-catalog.ts")).href);
const packs = new Map([catalogue.hubSlug, ...catalogue.articles.map(a => a.slug)].map(slug => [slug, json(path.join(workspace, "apps/api/app/guides/content", slug + ".json"))]));
const canonical = "https://mokaair.com", hub = "/zh-TW/life/" + catalogue.hubSlug;
const output = path.join(here, "browser");
mkdirSync(output, { recursive: true });
const observations = [];
const api = createServer((request, response) => {
  request.resume();
  const url = new URL(request.url || "/", "http://127.0.0.1");
  let body = { enabled: false };
  if (url.pathname.startsWith("/api/v1/guides/life/")) {
    const slug = url.pathname.split("/").at(-1), pack = packs.get(slug);
    body = pack ? { slug, kind: "life", locale: "zh-TW", status: "published", destination_id: null, destination_label: null,
      topics: [], valid_until: null, expired: false, published_locales: ["zh-TW"], article_links: [],
      document: { ...pack.locales["zh-TW"], version: 1, published_at: "2026-09-14T00:00:00Z", modified_at: null } } : { detail: "not found" };
    if (!pack) response.statusCode = 404;
  } else if (url.pathname.startsWith("/api/v1/guides")) body = { items: [], articles: [], total: 0, next_cursor: null };
  else if (url.pathname === "/api/v1/runtime/site-visibility") body = Object.fromEntries(siteFeatureKeys.map(k => [k + "_enabled", true]));
  else if (url.pathname === "/api/v1/usage-catalog") body = defaultUsageCatalog;
  else if (url.pathname === "/api/v1/ads/config") body = { enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false };
  else if (url.pathname === "/api/v1/analytics/config") body = { first_party_enabled: false, ga4_enabled: false };
  else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) body = { locale: "zh-TW", version: "fixture", entries: {} };
  else if (url.pathname === "/api/v1/auth/me") { response.statusCode = 401; body = { detail: "anonymous" }; }
  response.setHeader("Content-Type", "application/json");
  response.setHeader("Cache-Control", "no-store");
  response.end(JSON.stringify(body));
});
await new Promise(resolve => api.listen(0, "127.0.0.1", resolve));
const browser = await chromium.launch({ headless: true });
try {
  for (const advanced of [false, true]) {
    const probe = createServer();
    await new Promise(resolve => probe.listen(0, "127.0.0.1", resolve));
    const port = probe.address().port;
    await new Promise(resolve => probe.close(resolve));
    const origin = "http://127.0.0.1:" + port;
    const server = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
      cwd: prepared.web, windowsHide: true, stdio: "ignore",
      env: { ...process.env, NODE_ENV: "production", GEMINI_ADVANCED_SERIES_ENABLED: String(advanced), API_INTERNAL_URL: "http://127.0.0.1:" + api.address().port, NEXT_TELEMETRY_DISABLED: "1" },
    });
    try {
      let ready = false;
      for (let i = 0; i < 40; i++) {
        try { ready = (await fetch(origin + hub, { signal: AbortSignal.timeout(2000) })).ok; } catch { /* Startup only. */ }
        if (ready) break;
        await new Promise(resolve => setTimeout(resolve, 500));
      }
      assert.ok(ready, "Next startup");
      for (const [name, width, javaScriptEnabled] of [["desktop", 1200, true], ["mobile", 360, true], ["no-js", 360, false]]) {
        const context = await browser.newContext({ viewport: { width, height: 800 }, javaScriptEnabled });
        try {
          await context.setOffline(true);
          await context.route("**/*", async route => {
            const url = new URL(route.request().url());
            if (url.origin !== canonical) return route.abort();
            try {
              const response = await route.fetch({ url: origin + url.pathname + url.search,
                headers: { ...await route.request().allHeaders(), host: url.host, "x-forwarded-host": url.host, "x-forwarded-proto": "https" },
                maxRedirects: 0, maxRetries: route.request().method() === "GET" ? 1 : 0 });
              await route.fulfill({ response });
            } catch { await route.abort().catch(() => undefined); }
          });
          if (javaScriptEnabled) await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: canonical });
          const page = await context.newPage();
          for (const number of [0, 2, 49]) {
            const slug = number ? catalogue.articles[number - 1].slug : catalogue.hubSlug;
            const response = await page.goto(canonical + "/zh-TW/life/" + slug);
            assert.equal(response.status(), 200);
            await page.locator("h1").waitFor();
            assert.equal(await page.locator("h1").textContent(), packs.get(slug).locales["zh-TW"].title);
            const html = await response.text();
            if (!advanced) for (const article of catalogue.articles.filter(a => a.number > 50)) assert.ok(!html.includes(article.slug), "hidden slug in server HTML: " + article.slug);
            if (!number) assert.equal(await page.getByTestId("series-lessons").locator("li > a").count(), advanced ? 86 : 50);
            const headings = packs.get(slug).locales["zh-TW"].blocks.filter(b => b.type === "heading" && b.level === 2);
            for (let index = 0; index < headings.length; index++) assert.equal((await page.locator("#section-" + (index + 1)).textContent()).trim(), headings[index].text);
            if (number && javaScriptEnabled) {
              const figure = page.locator("figure").filter({ has: page.locator("pre") }).first();
              const text = await figure.locator("code").textContent();
              await figure.getByRole("button").click();
              assert.equal((await page.evaluate(() => navigator.clipboard.readText())).replace(/\r\n/g, "\n"), text);
              if (advanced && name === "mobile") await figure.screenshot({ path: path.join(output, "mobile-" + number + "-copy.png") });
            }
            const layout = await page.evaluate(() => ({ viewport: innerWidth, scroll: document.documentElement.scrollWidth }));
            assert.ok(layout.scroll <= layout.viewport + 1, JSON.stringify(layout));
            observations.push({ advanced, viewport: name, number, status: 200, h2Preserved: headings.length, overflow: false, copyChecked: Boolean(number && javaScriptEnabled) });
          }
        } finally { await context.close(); }
      }
    } finally { server.kill("SIGKILL"); }
  }
} finally {
  await browser.close();
  api.closeAllConnections();
  await new Promise(resolve => api.close(resolve));
  writeFileSync(path.join(output, "verification.json"), JSON.stringify({
    checkedAt: new Date().toISOString(), node: process.version, status: observations.length === 18 ? "passed" : "incomplete",
    method: "Existing verified Next build, candidate API packs, isolated browser; all external traffic blocked",
    priorBuildId: readFileSync(path.join(prepared.web, ".next/BUILD_ID"), "utf8").trim(),
    priorBuildReceiptSha256: hash(path.join(here, "../platform/next-integration/build-results.json")),
    candidateReceiptSha256: hash(path.join(here, "candidate/review.json")), observations,
  }, null, 2) + "\n");
}
console.log("18 candidate page visits passed: both flags, desktop/mobile/no-JavaScript, headings, hidden links, copy and overflow.");
