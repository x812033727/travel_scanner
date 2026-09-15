/** Render only the selected authoring batch; never publish or change the runtime catalogue. */
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import path from "node:path";
import { contract } from "./advanced/platform/release-contract.mjs";

const root = fileURLToPath(new URL("../../", import.meta.url));
const require = createRequire(path.join(root, "apps/web/package.json"));
const { chromium } = require("@playwright/test");

export async function renderArt({ track, outputRoot = root, numbers } = {}) {
  const series = JSON.parse(await readFile(path.join(root, "apps/web/lib/guide-series.json"), "utf8"));
  let selected = track ? contract.articles.filter((entry) => entry.stage === 2 && entry.track === track)
    : [{ number: 0, slug: series.hubSlug }, ...series.articles];
  if (!selected.length) throw new Error("Unknown authoring track: " + track);
  if (numbers) {
    if (!numbers.length || new Set(numbers).size !== numbers.length || numbers.some((n) => !selected.some((entry) => entry.number === n))) throw new Error("Invalid selected lesson numbers.");
    selected = selected.filter((entry) => numbers.includes(entry.number));
  }
  const reportRoot = track ? path.join(outputRoot, "docs/gemini-series/advanced/content", track, "verification")
    : path.join(outputRoot, "docs/gemini-series");
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1, javaScriptEnabled: false });
  const page = await context.newPage();
  await page.route("**/*", (route) => route.abort());
  const records = [];
  try {
    for (const { number, slug } of selected) {
      const assets = path.join(outputRoot, "apps/web/public/guides", slug);
      const renders = path.join(reportRoot, "renders", slug);
      await mkdir(renders, { recursive: true });
      for (const name of ["hero", "diagram-1"]) {
        const svg = await readFile(path.join(assets, name + ".svg"), "utf8");
        await page.setViewportSize({ width: 1600, height: 900 });
        await page.setContent('<meta charset="utf-8"><style>html,body{margin:0}svg{display:block;width:100vw;height:56.25vw}</style>' + svg);
        await page.evaluate(async () => { await document.fonts.ready; });
        const clipped = await page.locator("svg text").evaluateAll((texts) => texts.filter((text) => {
          const box = text.getBoundingClientRect();
          return box.left < 0 || box.right > 1600 || box.top < 0 || box.bottom > 900;
        }).map((text) => text.textContent));
        if (clipped.length) throw new Error(slug + "/" + name + ": clipped labels " + clipped.join(", "));
        await page.screenshot({ path: path.join(renders, name + ".png") });
        if (name === "hero") await page.screenshot({ path: path.join(assets, "hero.jpg"), type: "jpeg", quality: 90 });
        await page.setViewportSize({ width: 360, height: 203 });
        await page.screenshot({ path: path.join(renders, name + "-mobile.png") });
        records.push({ number, slug, name, width: 1600, height: 900, clippedLabels: [], mobilePreviewWidth: 360 });
      }
    }
    await mkdir(reportRoot, { recursive: true });
    const report = { renderedAt: new Date().toISOString(), renderer: "Playwright Chromium", track: track || null,
      status: "rendered-awaiting-human-review", records };
    await writeFile(path.join(reportRoot, "art-verification.json"), JSON.stringify(report, null, 2) + "\n");
    return report;
  } finally { await browser.close(); }
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  const { values } = parseArgs({ options: { track: { type: "string" }, "output-root": { type: "string" }, numbers: { type: "string" } } });
  renderArt({ track: values.track, outputRoot: values["output-root"] ? path.resolve(values["output-root"]) : root,
    numbers: values.numbers ? values.numbers.split(",").map(Number) : undefined })
    .then((report) => console.log(JSON.stringify(report, null, 2)))
    .catch((error) => { console.error(error.message); process.exitCode = 1; });
}
