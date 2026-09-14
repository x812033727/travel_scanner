/** Render original vector assets with one browser; no network or product screenshots. */
import { createRequire } from "node:module";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
const root = fileURLToPath(new URL("../../", import.meta.url));
const require = createRequire(path.join(root, "apps/web/package.json"));
const { chromium } = require("@playwright/test");
const series = JSON.parse(await readFile(path.join(root, "apps/web/lib/guide-series.json"), "utf8"));
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
await page.route("**/*", (route) => route.abort());
const records = [];
try {
  for (const [number, slug] of [[0, series.hubSlug], ...series.articles.map((a) => [a.number, a.slug])]) {
    const assets = path.join(root, "apps/web/public/guides", slug);
    const renders = path.join(root, "docs/gemini-series/renders", slug);
    await mkdir(renders, { recursive: true });
    for (const name of ["hero", "diagram-1"]) {
      const svg = await readFile(path.join(assets, `${name}.svg`), "utf8");
      await page.setContent(`<meta charset="utf-8"><style>html,body{margin:0}svg{display:block}</style>${svg}`);
      await page.evaluate(() => document.fonts.ready);
      const clipped = await page.locator("svg text").evaluateAll((texts) => texts.filter((text) => {
        const box = text.getBoundingClientRect();
        return box.left < 0 || box.right > 1600 || box.top < 0 || box.bottom > 900;
      }).map((text) => text.textContent));
      if (clipped.length) throw new Error(`${slug}/${name}: clipped labels ${clipped.join(", ")}`);
      await page.screenshot({ path: path.join(renders, `${name}.png`) });
      if (name === "hero") await page.screenshot({ path: path.join(assets, "hero.jpg"), type: "jpeg", quality: 90 });
      records.push({ number, slug, name, width: 1600, height: 900, clippedLabels: [] });
    }
    console.log(`${String(number).padStart(2, "0")} ${slug}`);
  }
  await writeFile(path.join(root, "docs/gemini-series/art-verification.json"), JSON.stringify({ renderedAt: new Date().toISOString(), renderer: "Playwright Chromium", records }, null, 2) + "\n");
} finally { await browser.close(); }
