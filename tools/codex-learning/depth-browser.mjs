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
const report = { checkedAt: new Date().toISOString(), environment: `Windows / Edge ${browser.version()} / synthetic local publication`, checks: [], errors: [] };
page.on("pageerror", error => report.errors.push(error.message));
const catalog = JSON.parse(await readFile("apps/web/lib/codex-learning/catalog.json", "utf8"));
const availableSlugs = catalog.filter(row => row.deepDraft).map(row => row.slug);
const slugs = values.slugs ? values.slugs.split(",") : availableSlugs;
assert(slugs.length > 0 && new Set(slugs).size === slugs.length && slugs.every(slug => availableSlugs.includes(slug)), "Select existing complete drafts");
const readyCount = catalog.filter(row => row.ready).length;
const packs = Object.fromEntries(await Promise.all(slugs.map(async slug => [slug, JSON.parse(await readFile(`apps/api/app/guides/content/${slug}.json`, "utf8"))])));
report.packHashes = Object.fromEntries(await Promise.all([...slugs, "codex-learning-hub"].map(async slug => [slug, createHash("sha256").update(await readFile(`apps/api/app/guides/content/${slug}.json`)).digest("hex")])));
try {
  for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
    console.log(`Deep preview: ${locale}`);
    for (const width of [360, 390, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(`${base}/${locale}/life/codex-learning-hub`, { waitUntil: "domcontentloaded" });
      await expect(page.getByRole("searchbox")).toBeEnabled({ timeout: 30000 });
      await expect(page.locator("main ol li h2")).toHaveCount(60);
      await expect(page.locator("main ol li h2 a")).toHaveCount(readyCount);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.getByRole("searchbox").fill("AGENTS.md");
      await page.locator("main select").nth(3).selectOption("D");
      await expect(page).toHaveURL(/unit=D/);
      await page.reload({ waitUntil: "domcontentloaded" });
      await expect(page.getByRole("searchbox")).toHaveValue("AGENTS.md");
      await expect(page.locator("main select").nth(3)).toHaveValue("D");
      assert(await page.locator("main ol li h2").count() > 0);
      if (locale === "zh-TW") await page.screenshot({ path: resolve(out, `deep-hub-${width}.png`) });
      // A history entry for a changed unit must be reversible without a reload.
      await page.locator("main select").nth(3).selectOption("E");
      await page.goBack();
      await expect(page.locator("main select").nth(3)).toHaveValue("D");
      for (const slug of slugs) {
        await page.goto(`${base}/${locale}/life/${slug}`, { waitUntil: "domcontentloaded" });
        await page.locator("main pre code").first().waitFor();
        const codeBlocks = packs[slug].locales[locale].blocks.filter(block => block.type === "code");
        assert.deepEqual(await page.locator("main pre code").allTextContents(), codeBlocks.map(block => block.code));
        // Also catch a stale fixture or SSR cache when prose changed but code did not.
        const normalize = text => text.replace(/\s+/g, "");
        const rendered = normalize(await page.locator("main").innerText());
        for (const block of packs[slug].locales[locale].blocks) {
          const prose = block.type === "paragraph" ? block.text : block.type === "rich_paragraph" ? block.spans.map(span => span.text).join("") : null;
          if (prose) assert(rendered.includes(normalize(prose)), `${locale}/${slug}: current authored paragraph is missing`);
        }
        assert(await page.locator(`main a[href$="/life/codex-learning-hub"]`).count() >= 2);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${locale}/${slug} overflows at ${width}`);
        for (const other of ["zh-TW", "zh-CN", "en", "ja", "ko"].filter(value => value !== locale)) {
          assert.equal(await page.locator(`main a[hreflang="${other}"][href="/${other}/life/${slug}"]`).count(), 1);
        }
        const firstSample = page.locator("main figure").filter({ has: page.locator("pre code") }).first();
        await firstSample.locator("button").click();
        // Windows clipboard converts LF to CRLF; compare content after that OS conversion.
        await expect.poll(() => page.evaluate(async () => (await navigator.clipboard.readText()).replace(/\r\n/g, "\n"))).toBe(codeBlocks[0].code);
        if (locale === "zh-TW" && ["codex-agents-md", "codex-skills", "codex-markdown-basics", "codex-mobile-ios", "codex-ide-getting-started"].includes(slug)) {
          await firstSample.scrollIntoViewIfNeeded();
          await page.screenshot({ path: resolve(out, `deep-${slug}-${width}.png`) });
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
} finally {
  await writeFile(resolve(out, values.report), JSON.stringify(report, null, 2) + "\n");
  await browser.close();
}
console.log(`Passed ${report.checks.length} browser checks`);
