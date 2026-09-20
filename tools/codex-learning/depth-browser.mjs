import { chromium, expect } from "@playwright/test";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve } from "node:path";
import assert from "node:assert/strict";
import { parseArgs } from "node:util";
import { createHash } from "node:crypto";

const { values } = parseArgs({ options: { slugs: { type: "string" }, report: { type: "string", default: "depth-browser.json" } } });
assert(/^[a-z0-9-]+\.json$/.test(values.report), "Report must be a JSON filename");

const base = "http://127.0.0.1:3123";
const out = resolve("docs/codex-learning/evidence");
await mkdir(out, { recursive: true });
const browser = await chromium.launch({ channel: "msedge", headless: true });
const context = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
const page = await context.newPage();
page.setDefaultNavigationTimeout(60000);
const report = { status: "running", checkedAt: new Date().toISOString(), environment: `Windows / Edge ${browser.version()} / synthetic local publication`, checks: [], errors: [] };
page.on("pageerror", error => report.errors.push(error.message));
page.on("console", message => {
  if (message.type() === "error" && /hydrat/i.test(message.text())) report.errors.push(message.text());
});
const catalog = JSON.parse(await readFile("apps/web/lib/codex-learning/catalog.json", "utf8"));
const availableSlugs = catalog.filter(row => row.deepDraft).map(row => row.slug);
const slugs = values.slugs ? values.slugs.split(",") : availableSlugs;
assert(slugs.length > 0 && new Set(slugs).size === slugs.length && slugs.every(slug => availableSlugs.includes(slug)), "Select existing complete drafts");
const readyCount = catalog.filter(row => row.ready).length;
const packs = Object.fromEntries(await Promise.all(slugs.map(async slug => [slug, JSON.parse(await readFile(`apps/api/app/guides/content/${slug}.json`, "utf8"))])));
const hubPack = JSON.parse(await readFile("apps/api/app/guides/content/codex-learning-hub.json", "utf8"));
report.packHashes = Object.fromEntries(await Promise.all([...slugs, "codex-learning-hub"].map(async slug => [slug, createHash("sha256").update(await readFile(`apps/api/app/guides/content/${slug}.json`)).digest("hex")])));
async function navigateToHub(label, navigate) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    await navigate(attempt);
    if (await page.getByRole("searchbox").waitFor({ timeout: 10000 }).then(() => true).catch(() => false)) return;
    report.checks.push(`${label}: transient fetch failed on attempt ${attempt}; retrying`);
  }
  assert.fail(`${label} did not load after three attempts`);
}
async function openHub(locale) {
  const url = `${base}/${locale}/life/codex-learning-hub`;
  await navigateToHub(`${locale} hub`, () => page.goto(url, { waitUntil: "load" }));
}
try {
  for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
    console.log(`Deep preview: ${locale}`);
    for (const width of [360, 390, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      await openHub(locale);
      await expect(page.getByRole("searchbox")).toBeEnabled({ timeout: 30000 });
      await expect(page.locator("main ol li h2")).toHaveCount(60);
      await expect(page.locator("main ol li h2 a")).toHaveCount(readyCount);
      const hubText = (await page.locator("main").innerText()).replace(/\s+/g, "");
      const hubSummary = hubPack.locales[locale].blocks.filter(block => block.type === "summary");
      assert.equal(hubSummary.length, 1, `${locale} hub: expected one summary block`);
      for (const item of hubSummary[0].items) assert(hubText.includes(item.replace(/\s+/g, "")), `${locale} hub: summary item is missing`);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.getByRole("searchbox").fill("AGENTS.md");
      await page.locator("main select").nth(3).selectOption("D");
      await expect(page).toHaveURL(/unit=D/);
      const filteredUrl = page.url();
      await navigateToHub(`${locale} hub URL reload`, attempt => attempt === 1
        ? page.reload({ waitUntil: "load" })
        : page.goto(filteredUrl, { waitUntil: "load" }));
      await expect(page.getByRole("searchbox")).toHaveValue("AGENTS.md", { timeout: 15000 });
      await expect(page.locator("main select").nth(3)).toHaveValue("D", { timeout: 15000 });
      assert(await page.locator("main ol li h2").count() > 0);
      if (locale === "zh-TW") await page.screenshot({ caret: "initial", path: resolve(out, `deep-hub-${width}.png`) });
      // A history entry for a changed unit must be reversible without a reload.
      const unitDUrl = page.url();
      await page.locator("main select").nth(3).selectOption("E");
      await navigateToHub(`${locale} hub history`, attempt => attempt === 1
        ? page.goBack({ waitUntil: "load" })
        : page.goto(unitDUrl, { waitUntil: "load" }));
      await expect(page.locator("main select").nth(3)).toHaveValue("D", { timeout: 15000 });
      for (const slug of slugs) {
        report.currentPage = { locale, slug, width };
        let articleLoaded = false;
        for (let attempt = 1; attempt <= 3; attempt += 1) {
          await page.goto(`${base}/${locale}/life/${slug}`, { waitUntil: "load" });
          articleLoaded = await page.locator("main pre code").first().waitFor({ timeout: 10000 }).then(() => true).catch(() => false);
          if (articleLoaded) break;
          report.checks.push(`${locale}/${slug} ${width}px: transient article fetch failed on attempt ${attempt}; retrying`);
        }
        assert(articleLoaded, `${locale}/${slug}: article did not load after three attempts`);
        const codeBlocks = packs[slug].locales[locale].blocks.filter(block => block.type === "code");
        assert.deepEqual(await page.locator("main pre code").allTextContents(), codeBlocks.map(block => block.code));
        // Also catch a stale fixture or SSR cache when prose changed but code did not.
        const normalize = text => text.replace(/\s+/g, "");
        const rendered = normalize(await page.locator("main").innerText());
        const summaries = packs[slug].locales[locale].blocks.filter(block => block.type === "summary");
        assert.equal(summaries.length, 1, `${locale}/${slug}: expected one summary block`);
        for (const item of summaries[0].items) assert(rendered.includes(normalize(item)), `${locale}/${slug}: summary item is missing`);
        for (const block of packs[slug].locales[locale].blocks) {
          const prose = block.type === "paragraph" ? block.text : block.type === "rich_paragraph" ? block.inlines.map(span => span.text).join("") : null;
          if (prose) assert(rendered.includes(normalize(prose)), `${locale}/${slug}: current authored paragraph is missing`);
        }
        assert(await page.locator(`main a[href$="/life/codex-learning-hub"]`).count() >= 2);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${locale}/${slug} overflows at ${width}`);
        for (const other of ["zh-TW", "zh-CN", "en", "ja", "ko"].filter(value => value !== locale)) {
          const alternate = page.locator(`head link[rel="alternate"][hreflang="${other}"]`);
          assert.equal(await alternate.count(), 1);
          assert.equal(new URL(await alternate.getAttribute("href")).pathname, `/${other}/life/${slug}`);
        }
        const firstSample = page.locator("main figure").filter({ has: page.locator("pre code") }).first();
        await firstSample.locator("button").click();
        // Windows clipboard converts LF to CRLF; compare content after that OS conversion.
        await expect.poll(() => page.evaluate(async () => (await navigator.clipboard.readText()).replace(/\r\n/g, "\n"))).toBe(codeBlocks[0].code);
        if (locale === "zh-TW" && ["codex-agents-md", "codex-skills", "codex-markdown-basics", "codex-mobile-ios", "codex-ide-getting-started"].includes(slug)) {
          await firstSample.scrollIntoViewIfNeeded();
          await page.screenshot({ caret: "initial", path: resolve(out, `deep-${slug}-${width}.png`) });
        }
        report.checks.push(`${locale}/${slug} ${width}px: exact rendered code, clipboard after Windows CRLF normalization, locale links, hub returns, no horizontal overflow`);
      }
      report.checks.push(`${locale} hub ${width}px: 60 entries, ${readyCount} links, URL reload and history filters`);
    }
  }
  const download = await context.request.get(`${base}/guides/codex-skills/todo-acceptance.zip`);
  assert.equal(download.status(), 200);
  assert.equal((await download.body()).subarray(0, 2).toString(), "PK");
  assert.deepEqual(report.errors, []);
  report.status = "passed";
} catch (error) {
  report.status = "failed";
  report.failure = error.message;
  report.failureUrl = page.url();
  report.failureMainText = await page.locator("main").innerText({ timeout: 3000 }).catch(() => "main unavailable");
  await page.screenshot({ caret: "initial", path: resolve(out, values.report.replace(/\.json$/, "-failure.png")), timeout: 10000 }).catch(() => {});
  throw error;
} finally {
  await writeFile(resolve(out, values.report), JSON.stringify(report, null, 2) + "\n");
  await browser.close();
}
console.log(`Passed ${report.checks.length} browser checks`);
