import { expect, test } from "@playwright/test";
import { mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { catalogue, packs, hubPath, startSeriesPreview, startPracticePreview } from "./fixtures/claude-code-series";

let site: Awaited<ReturnType<typeof startSeriesPreview>>;
const evidence = process.env.CLAUDE_SERIES_EVIDENCE ?? fileURLToPath(new URL("../../../docs/claude-code-series/evidence/", import.meta.url));
test.beforeAll(async () => { site = await startSeriesPreview(); mkdirSync(evidence, { recursive: true }); });
test.afterAll(async () => { await site?.stop(); });
test.beforeEach(async ({ context }) => {
  await context.route("**/*", route => new URL(route.request().url()).origin === site.origin
    ? route.continue() : route.abort());
});

test("directory server-renders all catalogue links without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  await context.route("**/*", route => new URL(route.request().url()).origin === site.origin ? route.continue() : route.abort());
  const page = await context.newPage();
  await page.goto(site.origin + hubPath);
  const directory = page.getByRole("region", { name: "Claude Code 教學目錄", exact: true });
  for (const entry of catalogue.entries) await expect(directory.locator(`a[href="/zh-TW/life/${entry.slug}"]`)).toHaveCount(1);
  const schemas = await page.locator('script[type="application/ld+json"]').allTextContents();
  expect(schemas.join(" ")).toContain("CollectionPage");
  expect(schemas.join(" ")).toContain("ItemList");
  await context.close();
});

test("search aliases, combined filters, URL reload and browser back", async ({ page }) => {
  await page.goto(site.origin + hubPath);
  const directory = page.getByRole("region", { name: "Claude Code 教學目錄", exact: true });
  const search = page.getByRole("searchbox", { name: "搜尋教學、指令或檔名" });
  for (const [term, slug] of [["MD", "claude-md-guide"], ["手機", "mobile-ios"], ["權限", "permissions-plan-mode"], ["/compact", "context-compact-clear"], ["MCP", "mcp-servers"], ["Monorepo", "monorepo-rules-workshop"], ["SOP", "skill-sop-workshop"], ["--json-schema", "structured-cli-pipeline"]]) {
    await search.fill(term);
    await expect(directory.locator(`a[href="/zh-TW/life/claude-code-${slug}"]`)).toHaveCount(1);
    await expect(page).toHaveURL(new RegExp(`q=${encodeURIComponent(term).replaceAll("%20", "\\+")}`));
  }
  await search.fill("/compact");
  await page.getByLabel("平台", { exact: true }).selectOption("cli");
  await page.getByLabel("主題", { exact: true }).selectOption("E");
  await page.getByLabel("程度", { exact: true }).selectOption("intermediate");
  await expect(directory.locator("ol > li > a")).toHaveCount(1);
  await page.reload();
  await expect(search).toHaveValue("/compact");
  await expect(page.getByLabel("平台", { exact: true })).toHaveValue("cli");
  await expect(page.getByLabel("主題", { exact: true })).toHaveValue("E");
  await expect(page.getByLabel("程度", { exact: true })).toHaveValue("intermediate");
  await directory.locator('a[href="/zh-TW/life/claude-code-context-compact-clear"]').click();
  await expect(page.locator("h1")).toContainText("上下文整理");
  await page.goBack();
  await expect(search).toHaveValue("/compact");
  await search.fill("no-such-lesson-987654");
  await expect(page.getByText("沒有符合條件的教學，試試其他關鍵字或清除篩選。")).toBeVisible();
  await page.getByRole("button", { name: "清除篩選", exact: true }).click();
  await expect(directory.locator("ol > li > a")).toHaveCount(catalogue.entries.length);
  await page.getByRole("button", { name: "MD 設定", exact: true }).click();
  const markdownPath = catalogue.paths.find(path => path.id === "markdown")!;
  await expect(directory.locator("ol > li > a")).toHaveCount(markdownPath.slugs.length);
  expect(await directory.locator("ol > li > a").evaluateAll(nodes => nodes.map(node => node.getAttribute("href"))))
    .toEqual(markdownPath.slugs.map(slug => `/zh-TW/life/${slug}`));
  await page.reload();
  await expect(page.getByRole("button", { name: "MD 設定", exact: true })).toHaveAttribute("aria-pressed", "true");
  await page.getByRole("button", { name: "清除篩選", exact: true }).click();
  for (const route of catalogue.paths.filter(path => path.id.startsWith("advanced-"))) {
    await page.getByRole("button", { name: route.title, exact: true }).click();
    expect(await directory.locator("ol > li > a").evaluateAll(nodes => nodes.map(node => node.getAttribute("href"))))
      .toEqual(route.slugs.map(slug => `/zh-TW/life/${slug}`));
    await page.getByRole("button", { name: "清除篩選", exact: true }).click();
  }
  await page.screenshot({ path: `${evidence}/hub-desktop.png`, fullPage: true });
  await directory.scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${evidence}/hub-controls-desktop.png` });
});

test("all catalogue pages render and every internal reference has a valid target", async ({ page }) => {
  test.setTimeout(300000);
  for (const [slug, pack] of packs) {
    await page.goto(`${site.origin}/zh-TW/life/${slug}`, { waitUntil: "domcontentloaded" });
    await expect(page.locator("h1")).toHaveText(pack.locales["zh-TW"].title);
    const links = await page.locator('main a[href*="/life/claude-code-"]').evaluateAll(nodes => nodes.map(node => node.getAttribute("href")!));
    for (const href of links) {
      expect(href.startsWith("/zh-TW/life/")).toBe(true);
      expect(packs.has(href.split("/").at(-1)!.split("#")[0])).toBe(true);
    }
    const index = catalogue.entries.findIndex(entry => entry.slug === slug);
    if (index < 0) continue;
    const navigation = page.getByRole("navigation", { name: "Claude Code 教學目錄", exact: true });
    await expect(navigation.getByRole("link", { name: "回總目錄", exact: true })).toHaveAttribute("href", hubPath);
    if (index > 0) await expect(navigation.getByRole("link", { name: /^上一篇：/ })).toHaveAttribute("href", `/zh-TW/life/${catalogue.entries[index - 1].slug}`);
    else await expect(navigation.getByRole("link", { name: /^上一篇：/ })).toHaveCount(0);
    if (index < catalogue.entries.length - 1) await expect(navigation.getByRole("link", { name: /^下一篇：/ })).toHaveAttribute("href", `/zh-TW/life/${catalogue.entries[index + 1].slug}`);
    else await expect(navigation.getByRole("link", { name: /^下一篇：/ })).toHaveCount(0);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  }
});

test("360 and 390px articles retain TOC, readable tables and contained code", async ({ page }) => {
  for (const width of [360, 390]) {
    await page.setViewportSize({ width, height: 844 });
    for (const suffix of ["claude-md-guide", "hooks-getting-started", "templates-cheatsheet", "project-rules-workshop", "hook-event-test-lab", "structured-cli-pipeline"]) {
      await page.goto(`${site.origin}/zh-TW/life/claude-code-${suffix}`);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
      const contents = page.locator("details").filter({ hasText: "本篇目錄" });
      await contents.locator("summary").click();
      await expect(contents.locator("a").first()).toBeVisible();
      await contents.locator("a").first().click();
      expect(new URL(page.url()).hash).not.toBe("");
      await page.screenshot({ path: `${evidence}/${suffix}-${width}.png`, fullPage: true });
      await page.locator("pre").first().scrollIntoViewIfNeeded();
      await page.screenshot({ path: `${evidence}/${suffix}-code-${width}.png` });
    }
  }
});

test("downloaded complete lab supports filtering, persistence, safe text and corrupted storage", async ({ page, context }) => {
  const lab = await startPracticePreview("advanced/lesson-96", "reference");
  try {
    await context.route(`${lab.origin}/**`, route => route.continue());
    await page.setViewportSize({ width: 360, height: 800 });
    await page.goto(lab.origin);
    for (const title of ["買牛奶", "整理桌面", '<img src=x onerror="alert(1)">']) {
      await page.getByLabel("新增待辦", { exact: true }).fill(title);
      await page.getByRole("button", { name: "新增", exact: true }).click();
    }
    await expect(page.getByRole("list", { name: "待辦項目" }).locator("li")).toHaveCount(3);
    await expect(page.locator("#todo-list img")).toHaveCount(0);
    await page.getByRole("checkbox", { name: "買牛奶", exact: true }).check();
    await page.getByRole("button", { name: "已完成", exact: true }).click();
    await expect(page.locator("#todo-list li")).toHaveCount(1);
    await page.getByRole("button", { name: "全部", exact: true }).click();
    await page.getByRole("button", { name: "刪除 整理桌面", exact: true }).click();
    await page.reload();
    await expect(page.locator("#todo-list li")).toHaveCount(2);
    await expect(page.getByRole("checkbox", { name: "買牛奶", exact: true })).toBeChecked();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: `${evidence}/practice-complete-360.png` });
    await page.evaluate(() => localStorage.setItem("mokaair-todos", "broken JSON"));
    await page.reload();
    await expect(page.locator("#todo-list li")).toHaveCount(0);
    await expect(page.getByRole("status")).toHaveText("目前沒有待辦。");
  } finally { await lab.stop(); }
});

test("downloaded TDD starter reproduces the wrong checkbox and reference fixes the same interaction", async ({ page, context }) => {
  for (const variant of ["starter", "reference"]) {
    const lab = await startPracticePreview("advanced/lesson-85", variant);
    try {
      await context.route(`${lab.origin}/**`, route => route.continue());
      await page.setViewportSize({ width: 390, height: 844 });
      await page.goto(lab.origin);
      for (let index = 0; index < 2; index++) {
        await page.getByLabel("新增待辦", { exact: true }).fill("同名待辦");
        await page.getByRole("button", { name: "新增", exact: true }).click();
      }
      const boxes = page.getByRole("checkbox", { name: "同名待辦", exact: true });
      await expect(boxes).toHaveCount(2);
      await boxes.nth(0).click();
      await expect(boxes.nth(0)).toBeChecked({ checked: variant === "reference" });
      await expect(boxes.nth(1)).toBeChecked({ checked: variant === "starter" });
      await page.screenshot({ path: `${evidence}/tdd-${variant}-390.png` });
    } finally { await lab.stop(); }
  }
});

test("copy preserves raw input, indentation and text through the native clipboard", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await context.addInitScript(() => {
    const write = navigator.clipboard.writeText.bind(navigator.clipboard);
    navigator.clipboard.writeText = value => {
      Object.defineProperty(window, "lastClipboardInput", { value, configurable: true });
      return write(value);
    };
  });
  for (const suffix of ["markdown-basics", "hooks-getting-started", "implement-feature", "skill-sop-workshop", "structured-cli-pipeline"]) {
    const slug = `claude-code-${suffix}`;
    await page.goto(`${site.origin}/zh-TW/life/${slug}`);
    const blocks = packs.get(slug)!.locales["zh-TW"].blocks.filter(block => block.type === "code");
    const figures = page.locator("figure").filter({ has: page.locator("pre") });
    await expect(figures).toHaveCount(blocks.length);
    for (let index = 0; index < blocks.length; index++) {
      await figures.nth(index).getByRole("button", { name: "複製", exact: true }).click();
      await expect(figures.nth(index).getByRole("status")).toHaveText("已複製");
      expect(await page.evaluate(() => Reflect.get(window, "lastClipboardInput"))).toBe(blocks[index].code);
      // Windows native text clipboard uses CRLF. Preserve all content and line breaks;
      // the raw browser API input above must still match exactly before OS conversion.
      expect((await page.evaluate(() => navigator.clipboard.readText())).replaceAll("\r\n", "\n")).toBe(blocks[index].code);
    }
  }
});

test("fixed life entry, unavailable directory retry and missing locale", async ({ page }) => {
  await page.goto(site.origin + "/zh-TW/life?cursor=preview-page-two");
  await expect(page.locator(`h2 a[href="${hubPath}"]`).first()).toBeVisible();
  site.state.seriesAvailable = false;
  await page.goto(site.origin + hubPath);
  await expect(page.getByText("暫時無法載入教學目錄，請稍後重試。")).toBeVisible();
  site.state.seriesAvailable = true;
  await page.getByRole("link", { name: "重新載入" }).click();
  await expect(page.getByRole("searchbox")).toBeVisible();
  await page.goto(site.origin + "/en/life/claude-code-claude-md-guide");
  await expect(page.locator('a[href="/en/life/claude-code-tutorials"]')).toHaveCount(0);
  await expect(page.locator("pre")).toHaveCount(0);
});

test("preview download links stay local and serve the exact reviewed ZIP bytes", async ({ page }) => {
  await page.goto(site.origin + "/zh-TW/life/claude-code-project-rules-workshop");
  // Anchored on the href, not the link's words: the label is content and is being rewritten
  // to stop naming a lesson by number (2026-09-16-content-packs-counts-in-hub-titles).
  await expect(page.locator(`a[href="${site.origin}/tutorials/claude-code/advanced/lesson-61.zip"]`)).toHaveCount(1);
  const paths = new Set<string>();
  for (const pack of packs.values()) for (const block of pack.locales["zh-TW"].blocks) {
    for (const inline of block.inlines ?? []) if (inline.type === "link" && inline.url?.startsWith("https://mokaair.com/tutorials/claude-code/advanced/")) paths.add(new URL(inline.url).pathname);
  }
  expect(paths.size).toBe(42);
  for (const pathname of paths) {
    const response = await page.request.get(site.origin + pathname);
    expect(response.status()).toBe(200);
    const expected = readFileSync(new URL(`../public${pathname}`, import.meta.url));
    expect(createHash("sha256").update(await response.body()).digest("hex")).toBe(createHash("sha256").update(expected).digest("hex"));
  }
});
