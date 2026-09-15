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
try {
  for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
    for (const width of [390, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      console.log(`Checking ${locale} ${width}px`);
      await page.goto(`${base}/${locale}/life/codex-learning-hub`, { waitUntil: "domcontentloaded" });
      await page.getByRole("searchbox").waitFor();
      console.log("Hub loaded");
      assert.equal(await page.locator("main h1").count(), 1);
      assert.equal(await page.locator("main ol li h2 a").count(), 32);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.getByRole("searchbox").fill("/plan");
      console.log("Search entered");
      await expect.poll(() => page.locator("main ol li h2 a").count(), { timeout: 15000 }).toBeLessThan(32);
      assert(await page.locator("main ol li h2 a").count() > 0);
      assert(await page.locator('main a[href$="/life/codex-plan-mode"]').count() >= 1);
      if (locale === "zh-TW") await page.screenshot({ path: resolve(out, `hub-${width}.png`), fullPage: false });
      await page.goto(`${base}/${locale}/life/codex-website-workshop`, { waitUntil: "domcontentloaded" });
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      assert(await page.locator(`main a[href$="/life/codex-learning-hub"]`).count() >= 2);
      for (const other of ["zh-TW", "zh-CN", "en", "ja", "ko"].filter((l) => l !== locale)) {
        assert(await page.locator(`main a[hreflang="${other}"][href="/${other}/life/codex-website-workshop"]`).count() === 1);
      }
      report.checks.push(`${locale} ${width}px: 32 links, search, article, reciprocal language links, no page overflow`);
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
