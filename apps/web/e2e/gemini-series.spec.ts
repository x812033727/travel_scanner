import { expect, test as base, type BrowserContext, type Page } from "@playwright/test";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import catalogue from "../lib/guide-series.json" with { type: "json" };
import { projectGeminiSeries } from "../lib/gemini-series-projection";
const advanced = process.env.GEMINI_E2E_ADVANCED === "true";
const series = projectGeminiSeries(catalogue, advanced);
const hiddenArticles = catalogue.articles.filter(article => !series.articles.some(visible => visible.slug === article.slug));
import { defaultUsageCatalog } from "../lib/usage-catalog";
import { siteFeatureKeys } from "../lib/site-features";

const canonical = "https://mokaair.com";
const hub = `/zh-TW/life/${series.hubSlug}`;
const packs = new Map([series.hubSlug, ...catalogue.articles.map((a) => a.slug)].map((slug) => {
  const pack = JSON.parse(readFileSync(new URL(`../../api/app/guides/content/${slug}.json`, import.meta.url), "utf8"));
  return [slug, pack];
}));
function state(slug: string) {
  const pack = packs.get(slug);
  return pack && { slug, kind: "life", locale: "zh-TW", status: "published", destination_id: null,
    destination_label: null, topics: [], valid_until: null, expired: false, published_locales: ["zh-TW"],
    article_links: catalogue.articles.map(article => ({ kind: "life", slug: article.slug, title: article.title })),
    document: { ...pack.locales["zh-TW"], blocks: [...pack.locales["zh-TW"].blocks, ...(slug === catalogue.hubSlug ? catalogue.articles.filter(article => article.number > 50).flatMap(article => [
      { type: "rich_paragraph", inlines: [{ type: "link", text: "深入教學", url: `${canonical}/zh-TW/life/${article.slug}#section-3` }, { type: "article", kind: "life", slug: article.slug, text: "深入參照" }] },
      { type: "link", text: "延伸教學", url: `${canonical}/zh-TW/life/${article.slug}` },
      { type: "list", ordered: false, items: [`${canonical}/zh-TW/life/${article.slug}`] },
    ]) : [])], version: 1, published_at: "2026-09-14T00:00:00Z", modified_at: null } };
}
type Site = { origin: string; hubPublished: boolean };
async function connect(context: BrowserContext, site: Site) {
  await context.setOffline(true);
  await context.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin !== canonical) return route.abort();
    try {
      const response = await route.fetch({ url: `${site.origin}${url.pathname}${url.search}`,
        headers: { ...await route.request().allHeaders(), host: url.host, "x-forwarded-host": url.host, "x-forwarded-proto": "https" }, maxRedirects: 0,
        // The loopback proxy can reuse a socket just closed by Next. Retry GET ECONNRESET once;
        // Playwright never retries HTTP error responses through this option.
        maxRetries: route.request().method() === "GET" ? 1 : 0 });
      await route.fulfill({ response });
    } catch (error) {
      console.error("Gemini loopback request failed:", url.pathname, error instanceof Error ? error.message.split("\n")[0] : String(error));
      await route.abort().catch(() => undefined);
    }
  });
}
const test = base.extend<object, { site: Site }>({
  site: [async ({ playwright }, runTest) => {
    if (!existsSync(new URL("../.next/BUILD_ID", import.meta.url))) throw new Error("Build the web app before this integration test.");
    const site = { origin: "", hubPublished: true };
    const api = createServer((request, response) => {
      request.resume();
      const url = new URL(request.url || "/", "http://127.0.0.1");
      let body: unknown = {};
      if (url.pathname.startsWith("/api/v1/guides/life/")) {
        const slug = url.pathname.split("/").at(-1)!;
        body = slug === series.hubSlug && !site.hubPublished ? { status: "not_found", document: null, published_locales: [] } : state(slug);
        if (!body) { response.statusCode = 404; body = { detail: "not found" }; }
      } else if (url.pathname === "/api/v1/guides/topics") body = { items: [] };
      else if (url.pathname.startsWith("/api/v1/guides")) body = { articles: url.searchParams.get("kind") === "life" ? catalogue.articles.map(article => ({
        slug: article.slug, kind: "life", title: article.title, description: article.purpose, destination_id: null, destination_label: null, topics: [], published_at: "2026-09-14T00:00:00Z", valid_until: null, featured: false,
      })) : [], total: catalogue.articles.length, next_cursor: null };
      else if (url.pathname === "/api/v1/runtime/site-visibility") body = Object.fromEntries(siteFeatureKeys.map((k) => [`${k}_enabled`, true]));
      else if (url.pathname === "/api/v1/usage-catalog") body = defaultUsageCatalog;
      else if (url.pathname === "/api/v1/ads/config") body = { enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false };
      else if (url.pathname === "/api/v1/analytics/config") body = { first_party_enabled: false, ga4_enabled: false };
      else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) body = { locale: "zh-TW", version: "fixture", entries: {} };
      else if (url.pathname === "/api/v1/auth/me") { response.statusCode = 401; body = { detail: "anonymous" }; }
      else body = { enabled: false };
      response.setHeader("Content-Type", "application/json");
      response.setHeader("Cache-Control", "no-store");
      response.end(JSON.stringify(body));
    });
    const probe = createServer();
    await new Promise<void>((resolve) => api.listen(0, "127.0.0.1", resolve));
    await new Promise<void>((resolve) => probe.listen(0, "127.0.0.1", resolve));
    const port = (probe.address() as { port: number }).port;
    await new Promise<void>((resolve) => probe.close(() => resolve()));
    site.origin = `http://127.0.0.1:${port}`;
    const server = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
      cwd: fileURLToPath(new URL("../", import.meta.url)), windowsHide: true, stdio: "ignore",
      env: { ...process.env, NODE_ENV: "production", GEMINI_ADVANCED_SERIES_ENABLED: String(advanced), API_INTERNAL_URL: `http://127.0.0.1:${(api.address() as { port: number }).port}`, NEXT_TELEMETRY_DISABLED: "1" },
    });
    const request = await playwright.request.newContext();
    try {
      await expect.poll(async () => { try { return (await request.get(site.origin + hub, { timeout: 3000 })).status(); } catch { return 0; } }, { timeout: 60000 }).toBe(200);
      await runTest(site);
    } finally {
      await request.dispose();
      server.kill("SIGKILL");
      api.closeAllConnections();
      await new Promise<void>((resolve) => api.close(() => resolve()));
    }
  }, { scope: "worker", timeout: 90000 }],
});
test.beforeEach(async ({ context, site }) => { site.hubPublished = true; await connect(context, site); });
async function noOverflow(page: Page) {
  await page.evaluate(() => document.fonts.ready);
  const layout = await page.evaluate(() => ({
    width: window.innerWidth, scroll: document.documentElement.scrollWidth,
    overflowing: [...document.querySelectorAll("body *")].filter((element) => {
      const box = element.getBoundingClientRect();
      return box.width > 0 && box.right > window.innerWidth + 1 && getComputedStyle(element).position !== "fixed";
    }).slice(0, 8).map((element) => ({ tag: element.tagName, class: element.className, text: element.textContent?.slice(0, 60) })),
  }));
  expect(layout.scroll, JSON.stringify(layout)).toBeLessThanOrEqual(layout.width + 1);
}

test("hub has every lesson, searchable aliases, categories and learning paths", async ({ page }, info) => {
  await page.goto(canonical + hub);
  const lessons = page.getByTestId("series-lessons");
  await expect(lessons.locator("li > a")).toHaveCount(series.articles.length);
  expect(await lessons.locator("li > a").evaluateAll((links) => links.map((link) => link.getAttribute("href")).sort()))
    .toEqual(series.articles.map((a) => `/zh-TW/life/${a.slug}`).sort());
  const search = page.getByRole("searchbox", { name: "搜尋教學或指令" });
  for (const [query, slug] of [["MD", "gemini-markdown-basics"], ["GEMINI.md", "gemini-cli-gemini-md"], ["手機", "gemini-ios-app-guide"], ["CLI", "gemini-cli-getting-started"], ["/memory", "gemini-cli-memory-hierarchy"], ["NotebookLM", "notebooklm-guide"]]) {
    await search.fill(query);
    await expect(lessons.locator(`a[href="/zh-TW/life/${slug}"]`)).toBeVisible();
  }
  await page.getByRole("button", { name: "清除篩選" }).click();
  if (series.advancedEnabled) {
    await page.getByRole("combobox", { name: "教學階段", exact: true }).selectOption("2");
    await expect(lessons.locator("li > a")).toHaveCount(36);
    await page.getByRole("combobox", { name: "深入主題", exact: true }).selectOption("md");
    await expect(lessons.locator("li > a")).toHaveCount(6);
    await page.getByRole("button", { name: "清除篩選" }).click();
  }
  await page.getByRole("combobox", { name: "主題分類", exact: true }).selectOption("F");
  await expect(lessons.locator("li > a")).toHaveCount(series.articles.filter(article => article.group === "F").length);
  await page.getByRole("button", { name: "清除篩選" }).click();
  for (const path of series.paths) {
    await page.getByRole("combobox", { name: "學習路線", exact: true }).selectOption(path.id);
    await expect(lessons.locator("li > a")).toHaveCount(path.articles.length);
  }
  await page.getByRole("button", { name: "清除篩選" }).click();
  await noOverflow(page);
  await search.scrollIntoViewIfNeeded();
  await page.screenshot({ path: info.outputPath("hub-search.png") });
});

test("all visible real article bodies, previous/next, anchors and copy render without overflow", async ({ page, context }, info) => {
  test.setTimeout(600000);
  await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: canonical });
  for (const article of series.articles) {
    await page.goto(`${canonical}/zh-TW/life/${article.slug}`);
    await expect(page.locator("h1")).toHaveText(article.title);
    await expect(page.getByRole("navigation", { name: "Gemini 系列導覽", exact: true }).getByRole("link", { name: "返回 Gemini 教學總目錄" })).toHaveAttribute("href", hub);
    const bottom = page.getByRole("navigation", { name: "繼續閱讀 Gemini 系列" });
    await expect(bottom.locator('a[rel="prev"]')).toHaveCount(article.number > 1 ? 1 : 0);
    await expect(bottom.locator('a[rel="next"]')).toHaveCount(article.number < series.articles.length ? 1 : 0);
    if (article.number > 1) await expect(bottom.locator('a[rel="prev"]')).toHaveAttribute("href", `/zh-TW/life/${series.articles[article.number - 2].slug}`);
    if (article.number < series.articles.length) await expect(bottom.locator('a[rel="next"]')).toHaveAttribute("href", `/zh-TW/life/${series.articles[article.number].slug}`);
    for (const command of series.commands.filter((c) => c.article === article.number && c.anchor)) await expect(page.locator(`#${command.anchor}`)).toHaveCount(1);
    await noOverflow(page);
    if ([18, 36, 47, 50, 69, 73, 81, 86].includes(article.number)) {
      const figure = page.locator("figure").filter({ has: page.locator("pre") }).first();
      const code = await figure.locator("code").textContent();
      await figure.getByRole("button").click();
      // Windows' native clipboard normalizes LF to CRLF; tabs and content must survive.
      expect((await page.evaluate(() => navigator.clipboard.readText())).replace(/\r\n/g, "\n")).toBe(code);
      await figure.evaluate(element => element.scrollIntoView({ block: "center" }));
      await figure.screenshot({ path: info.outputPath(`lesson-${article.number}-code.png`) });
      await noOverflow(page);
    }
  }
});

test("all links remain in server HTML with JavaScript disabled", async ({ browser, site }, info) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 360, height: 800 } });
  try {
    await connect(context, site);
    const page = await context.newPage();
    await page.goto(canonical + hub);
    await expect(page.getByTestId("series-lessons").locator("li > a")).toHaveCount(series.articles.length);
    await page.getByTestId("series-lessons").locator(`a[href="/zh-TW/life/${series.articles[35].slug}"]`).click();
    await expect(page.locator("h1")).toHaveText(series.articles[35].title);
    await noOverflow(page);
    await page.locator('img[src$="diagram-1.svg"]').scrollIntoViewIfNeeded();
    await page.screenshot({ path: info.outputPath("mobile-360-diagram-no-js.png") });
  } finally { await context.close(); }
});

test("life entry and series navigation wait for published hub", async ({ page, site }) => {
  site.hubPublished = false;
  await page.goto(`${canonical}/zh-TW/life/${series.articles[0].slug}`);
  await expect(page.getByRole("navigation", { name: "Gemini 系列導覽", exact: true })).toHaveCount(0);
  await page.goto(`${canonical}/zh-TW/life`);
  await expect(page.locator(`a[href="${hub}"]`)).toHaveCount(0);
  site.hubPublished = true;
  await page.reload();
  await expect(page.locator(`a[href="${hub}"]`)).toHaveCount(1);
});

test("server HTML, RSC, loaded scripts and life cards respect the server flag", async ({ page, site }) => {
  const response = await page.goto(`${canonical}${hub}?GEMINI_ADVANCED_SERIES_ENABLED=true`);
  const html = await response!.text();
  const rsc = await fetch(`${site.origin}${hub}?_rsc=gemini-check`, { headers: { RSC: "1", host: "mokaair.com", "x-forwarded-host": "mokaair.com", "x-forwarded-proto": "https" } });
  expect(rsc.headers.get("content-type")).toContain("text/x-component");
  const payload = await rsc.text();
  for (const article of hiddenArticles) {
    expect(html).not.toContain(article.slug);
    expect(payload).not.toContain(article.slug);
  }
  for (const script of await page.locator('script[src*="/_next/"]').evaluateAll(nodes => nodes.map(node => node.getAttribute("src")!))) {
    const text = await (await fetch(site.origin + new URL(script, canonical).pathname)).text();
    for (const article of catalogue.articles.filter(article => article.number > 50)) expect(text).not.toContain(article.slug);
  }
  await expect(page.getByTestId("series-lessons").locator("li > a")).toHaveCount(series.articles.length);
  await page.goto(`${canonical}/zh-TW/life`);
  for (const article of hiddenArticles) await expect(page.locator(`a[href$="/life/${article.slug}"]`)).toHaveCount(0);
  await expect(page.getByText(`${series.articles.length} 篇完整教學`, { exact: false })).toBeVisible();
});
