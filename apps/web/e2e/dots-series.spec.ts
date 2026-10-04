/** Local publication fixture; screenshots from this suite are UI tests, not dots evidence. */
import { expect, test, type Page } from "@playwright/test";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import type { GuideArticleState } from "../lib/guides";
import type { GuideSeries } from "../lib/guide-series";
import { siteFeatureKeys } from "../lib/site-features";
import { defaultUsageCatalog } from "../lib/usage-catalog";

const read = (relative: string) => JSON.parse(readFileSync(new URL(relative, import.meta.url), "utf8"));
const catalogue = read("../../api/app/guides/series_data/dots.json") as {
  slug: string; hub: string; groups: GuideSeries["groups"]; paths: GuideSeries["paths"];
  entries: (GuideSeries["entries"][number] & { prerequisites: string[]; related: string[] })[];
};
const packs = new Map([catalogue.hub, ...catalogue.entries.map(entry => entry.slug)].map(slug => [slug, read(`../../api/app/guides/content/${slug}.json`)]));
const reference = (slug: string) => ({ kind: "life" as const, slug, title: packs.get(slug).locales["zh-TW"].title });
const entries = catalogue.entries.map(entry => ({ ...entry, ...reference(entry.slug), description: packs.get(entry.slug).locales["zh-TW"].description, minutes: 6 }));
const hubPath = `/zh-TW/life/${catalogue.hub}`;

async function startPreview() {
  if (!existsSync(new URL("../.next/BUILD_ID", import.meta.url))) throw new Error("Run npm run build:web before this isolated course UI test.");
  const state = { withdrawn: new Set<string>() };
  let origin = "";
  const upstream = createServer((request, response) => {
    request.resume();
    const url = new URL(request.url || "/", "http://127.0.0.1");
    const locale = url.searchParams.get("locale") || "zh-TW";
    const visible = (slug: string) => locale === "zh-TW" && packs.has(slug) && !state.withdrawn.has(slug);
    const visibleEntries = entries.filter(entry => visible(entry.slug));
    let body: unknown = {};
    if (request.method !== "GET") { response.writeHead(405); response.end(); return; }
    if (url.pathname === `/api/v1/guides/series/${catalogue.slug}`) {
      if (!visible(catalogue.hub)) { response.statusCode = 404; body = { detail: "unpublished series" }; }
      else body = { slug: catalogue.slug, locale, hub: reference(catalogue.hub), groups: catalogue.groups,
        paths: catalogue.paths.map(path => ({ ...path, slugs: path.slugs.filter(visible) })), entries: visibleEntries };
    } else if (url.pathname.startsWith("/api/v1/guides/life/")) {
      const slug = url.pathname.split("/").at(-1)!;
      const pack = packs.get(slug);
      const index = visibleEntries.findIndex(entry => entry.slug === slug);
      const entry = catalogue.entries.find(entry => entry.slug === slug);
      const document = visible(slug) ? { ...pack.locales["zh-TW"], version: 1, published_at: "2026-10-03T00:00:00Z", modified_at: null,
        blocks: pack.locales["zh-TW"].blocks.map((block: { type: string; inlines?: { type: string; url?: string }[] }) => block.inlines
          ? { ...block, inlines: block.inlines.map(inline => inline.type === "link" && inline.url?.startsWith("https://mokaair.com/dots-course/")
            ? { ...inline, url: origin + new URL(inline.url).pathname } : inline) } : block) } : null;
      body = { slug, kind: "life", locale, status: document ? "published" : "unpublished", document,
        published_locales: pack && !state.withdrawn.has(slug) ? ["zh-TW"] : [], destination_id: null, destination_label: null,
        topics: [], valid_until: null, expired: false, article_links: [...packs.keys()].filter(visible).map(reference),
        series: document && visible(catalogue.hub) ? { slug: catalogue.slug, hub: reference(catalogue.hub), current: index >= 0 ? visibleEntries[index] : null,
          previous: index > 0 ? reference(visibleEntries[index - 1].slug) : null,
          next: index >= 0 && index + 1 < visibleEntries.length ? reference(visibleEntries[index + 1].slug) : null,
          prerequisites: entry?.prerequisites.filter(visible).map(reference) || [], related: entry?.related.filter(visible).map(reference) || [] } : null } satisfies Partial<GuideArticleState>;
    } else if (url.pathname === "/api/v1/guides/topics") body = { topics: [] };
    else if (url.pathname === "/api/v1/guides") body = { articles: visibleEntries.map(entry => ({ ...entry, locale, topics: [], destination_id: null, destination_label: null, valid_until: null, expired: false, published_at: "2026-10-03T00:00:00Z" })), next_cursor: null };
    else if (url.pathname === "/api/v1/runtime/site-visibility") body = Object.fromEntries(siteFeatureKeys.map(key => [`${key}_enabled`, true]));
    else if (url.pathname === "/api/v1/usage-catalog") body = defaultUsageCatalog;
    else if (url.pathname === "/api/v1/ads/config") body = { enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false };
    else if (url.pathname === "/api/v1/analytics/config") body = { first_party_enabled: false, ga4_enabled: false };
    else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) body = { locale, version: "dots-test", entries: {} };
    else if (url.pathname === "/api/v1/auth/me") { response.statusCode = 401; body = { detail: "anonymous" }; }
    else body = { enabled: false };
    response.setHeader("Content-Type", "application/json");
    response.setHeader("Cache-Control", "no-store");
    response.end(JSON.stringify(body));
  });
  await new Promise<void>(resolve => upstream.listen(0, "127.0.0.1", resolve));
  const probe = createServer();
  await new Promise<void>(resolve => probe.listen(0, "127.0.0.1", resolve));
  const port = (probe.address() as { port: number }).port;
  await new Promise<void>(resolve => probe.close(() => resolve()));
  origin = `http://127.0.0.1:${port}`;
  const next = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
    cwd: fileURLToPath(new URL("../", import.meta.url)), windowsHide: true, stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, NODE_ENV: "production", API_INTERNAL_URL: `http://127.0.0.1:${(upstream.address() as { port: number }).port}`, NEXT_TELEMETRY_DISABLED: "1" },
  });
  let logs = "";
  next.stdout.on("data", chunk => { logs = (logs + chunk).slice(-8000); });
  next.stderr.on("data", chunk => { logs = (logs + chunk).slice(-8000); });
  const stop = async () => { next.kill(); upstream.closeAllConnections(); await new Promise<void>(resolve => upstream.close(() => resolve())); };
  try {
    await expect.poll(async () => {
      if (next.exitCode !== null) throw new Error(logs);
      try { return (await fetch(origin + hubPath, { signal: AbortSignal.timeout(2000) })).status; } catch { return 0; }
    }, { timeout: 60000 }).toBe(200);
    return { origin, state, stop };
  } catch (error) { await stop(); throw error; }
}

let site: Awaited<ReturnType<typeof startPreview>>;
test.beforeAll(async () => { site = await startPreview(); });
test.afterAll(async () => { await site?.stop(); });
test.beforeEach(async ({ context }) => {
  site.state.withdrawn.clear();
  await context.route("**/*", route => new URL(route.request().url()).origin === site.origin ? route.continue() : route.abort());
});
async function containedLayout(page: Page) {
  await page.evaluate(() => document.fonts.ready);
  const layout = await page.evaluate(() => ({ width: innerWidth, content: document.documentElement.scrollWidth,
    overflow: [...document.querySelectorAll("body *")].filter(element => {
      const box = element.getBoundingClientRect();
      return box.width > 0 && box.right > innerWidth + 1 && getComputedStyle(element).position !== "fixed";
    }).slice(0, 10).map(element => ({ tag: element.tagName, class: element.className, text: element.textContent?.slice(0, 80) })) }));
  expect(layout.content, JSON.stringify(layout)).toBeLessThanOrEqual(layout.width + 1);
}

test("course hub exposes sixteen lessons and hides a withdrawn lesson", async ({ page }) => {
  await page.goto(site.origin + hubPath);
  const directory = page.getByRole("region", { name: reference(catalogue.hub).title, exact: true });
  await expect(directory.locator("ol > li > a")).toHaveCount(16);
  await page.getByRole("searchbox", { name: "搜尋教學、指令或檔名" }).fill("Slack");
  await expect(directory.locator('a[href="/zh-TW/life/dots-lesson-05"]')).toBeVisible();
  await page.getByRole("button", { name: "清除篩選", exact: true }).click();
  await containedLayout(page);
  site.state.withdrawn.add("dots-lesson-03");
  await page.reload();
  await expect(directory.locator("ol > li > a")).toHaveCount(15);
  await expect(directory.locator('a[href="/zh-TW/life/dots-lesson-03"]')).toHaveCount(0);
});

test("copyable prompts and real local downloads work on desktop and mobile", async ({ page, context }) => {
  await page.goto(`${site.origin}/zh-TW/life/dots-lesson-03`);
  await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: site.origin });
  const prompt = page.locator("pre").first();
  const expected = await prompt.locator("code").textContent();
  await page.getByRole("button", { name: "複製", exact: true }).first().click();
  await expect.poll(() => page.evaluate(async () => (await navigator.clipboard.readText()).replace(/\r\n/g, "\n"))).toBe(expected?.replace(/\r\n/g, "\n"));
  await expect(page.getByRole("status").filter({ hasText: "已複製" })).toBeVisible();
  await containedLayout(page);
  await page.goto(`${site.origin}/zh-TW/life/dots-lesson-11`);
  const link = page.locator('main a[href*="/dots-course/"]').first();
  await expect(link).toBeVisible();
  const pathname = new URL((await link.getAttribute("href"))!, site.origin).pathname;
  const downloading = page.waitForEvent("download");
  await link.click();
  const download = await downloading;
  const saved = await download.path();
  expect(saved).not.toBeNull();
  const downloaded = createHash("sha256").update(readFileSync(saved!)).digest("hex");
  const local = createHash("sha256").update(readFileSync(new URL(`../public${pathname}`, import.meta.url))).digest("hex");
  expect(downloaded).toBe(local);
  await containedLayout(page);
});

test("unpublished languages and a withdrawn hub do not reveal course content", async ({ page }) => {
  await page.goto(`${site.origin}/en/life/dots-lesson-03`);
  await expect(page.locator("h1")).not.toHaveText(reference("dots-lesson-03").title);
  await expect(page.locator("pre")).toHaveCount(0);
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", /noindex/);
  site.state.withdrawn.add(catalogue.hub);
  await page.goto(site.origin + hubPath);
  await expect(page.getByRole("region", { name: reference(catalogue.hub).title, exact: true })).toHaveCount(0);
  await expect(page.locator("h1")).not.toHaveText(reference(catalogue.hub).title);
});
