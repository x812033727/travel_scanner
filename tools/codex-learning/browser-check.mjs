import { chromium, expect } from "@playwright/test";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import assert from "node:assert/strict";

const base = "http://127.0.0.1:3123";
const out = resolve("docs/codex-learning/evidence");
await mkdir(out, { recursive: true });
const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage();
page.setDefaultNavigationTimeout(60000);
const report = { environment: `Windows / ${browser.version()} / synthetic local publication API`, checks: [], errors: [] };
page.on("pageerror", (error) => report.errors.push(error.message));
async function openArticle(locale, slug) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    await page.goto(`${base}/${locale}/life/${slug}`, { waitUntil: "load" });
    if (await page.locator(`main a[href$="/life/codex-learning-hub"]`).count() >= 2) return;
    report.checks.push(`${locale}/${slug}: transient article fetch failed on attempt ${attempt}; retrying`);
  }
  assert.fail(`${locale}/${slug}: article did not load after three attempts`);
}
async function openHub(locale) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    await page.goto(`${base}/${locale}/life/codex-learning-hub`, { waitUntil: "load" });
    if (await page.getByRole("searchbox").waitFor({ timeout: 10000 }).then(() => true).catch(() => false)) return;
    report.checks.push(`${locale}/codex-learning-hub: transient fetch failed on attempt ${attempt}; retrying`);
  }
  assert.fail(`${locale}/codex-learning-hub: hub did not load after three attempts`);
}
try {
  for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
    for (const width of [390, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      console.log(`Checking ${locale} ${width}px`);
      await openHub(locale);
      console.log("Hub loaded");
      assert.equal(await page.locator("main h1").count(), 1);
      assert.equal(await page.locator("main ol li h2 a").count(), 60);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.getByRole("searchbox").fill("/plan");
      console.log("Search entered");
      await expect.poll(() => page.locator("main ol li h2 a").count(), { timeout: 15000 }).toBeLessThan(60);
      assert(await page.locator("main ol li h2 a").count() > 0);
      assert(await page.locator('main a[href$="/life/codex-plan-mode"]').count() >= 1);
      if (locale === "zh-TW") await page.screenshot({ path: resolve(out, `hub-${width}.png`), fullPage: false });
      await openArticle(locale, "codex-website-workshop");
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      for (const other of ["zh-TW", "zh-CN", "en", "ja", "ko"].filter((l) => l !== locale)) {
        const alternate = page.locator(`head link[rel="alternate"][hreflang="${other}"]`);
        assert.equal(await alternate.count(), 1);
        assert.equal(new URL(await alternate.getAttribute("href")).pathname, `/${other}/life/codex-website-workshop`);
      }
      report.checks.push(`${locale} ${width}px: 60 links, search, article, reciprocal language links, no page overflow`);
    }
  }
  const html = await readFile("docs/codex-learning/examples/index.html", "utf8");
  for (const width of [390, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    await page.setContent(html);
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.keyboard.press("Tab");
    assert.equal(await page.evaluate(() => document.activeElement.tagName), "A");
    await page.screenshot({ path: resolve(`apps/web/public/guides/codex-website-workshop/workshop-${width}.png`), fullPage: true });
    report.checks.push(`Standalone website ${width}px: keyboard link focus and no page overflow`);
  }
  assert.deepEqual(report.errors, []);
} finally {
  await writeFile(resolve(out, "browser-check.json"), JSON.stringify(report, null, 2) + "\n");
  await browser.close();
}
console.log(JSON.stringify(report, null, 2));
