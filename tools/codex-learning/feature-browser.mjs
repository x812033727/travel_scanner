import { chromium, expect } from "@playwright/test";
import { createServer } from "node:http";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve } from "node:path";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";

const author = await readFile("docs/codex-learning/deep/modules/47.json", "utf8");
const module = JSON.parse(author);
const fix = module.blocks.filter(b => b.type === "code" && b.language === "javascript")[1].code.trimEnd();
const names = ["index.html", "style.css", "app.js", "core.mjs", "core.test.mjs"];
const files = new Map(await Promise.all(names.map(async name => [
  "/" + name, await readFile(resolve("docs/codex-learning/practice/start", name), "utf8"),
])));
const before = files.get("/core.mjs");
assert.equal((before.match(/export function visibleTasks/g) ?? []).length, 1);
files.set("/core.mjs", before.replace(/export function visibleTasks\(tasks, filter\) \{[\s\S]*?\r?\n\}/, fix));
const mime = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript" };
const server = createServer((request, response) => {
  const pathname = new URL(request.url, "http://localhost").pathname;
  const key = pathname === "/" ? "/index.html" : pathname;
  if (!files.has(key)) { response.writeHead(404).end(); return; }
  response.writeHead(200, { "Content-Type": mime[key.slice(key.lastIndexOf("."))] }).end(files.get(key));
});
await new Promise(done => server.listen(0, "127.0.0.1", done));
const browser = await chromium.launch({ channel: "msedge", headless: true });
const checks = [];
try {
  const origin = "http://127.0.0.1:" + server.address().port;
  await mkdir("apps/web/public/guides/codex-implement-feature", { recursive: true });
  for (const width of [360, 390, 1280]) {
    const context = await browser.newContext({ viewport: { width, height: 900 } });
    const page = await context.newPage();
    await page.goto(origin);
    for (const title of ["Read", "Build", "Read"]) {
      await page.getByLabel("New task").fill(title);
      await page.getByRole("button", { name: "Add task" }).click();
    }
    const boxes = page.locator("#tasks input[type=checkbox]");
    const originalIds = await boxes.evaluateAll(items => items.map(el => el.dataset.taskId));
    assert.equal(new Set(originalIds).size, 3);
    await boxes.nth(0).check();
    await boxes.nth(2).check();
    const shownIds = () => boxes.evaluateAll(items => items.map(el => el.dataset.taskId));
    await page.getByLabel("Show").selectOption("active");
    assert.deepEqual(await shownIds(), [originalIds[1]]);
    await page.getByLabel("Show").selectOption("completed");
    assert.deepEqual(await shownIds(), [originalIds[0], originalIds[2]]);
    await expect(page.locator("#tasks li span")).toHaveText(["Read", "Read"]);
    await boxes.nth(0).focus();
    await page.screenshot({
      path: "apps/web/public/guides/codex-implement-feature/reference-" + width + ".png",
      fullPage: true,
    });
    await page.getByLabel("Show").selectOption("all");
    assert.deepEqual(await shownIds(), originalIds);
    await boxes.nth(0).uncheck();
    await page.getByLabel("Show").selectOption("completed");
    assert.deepEqual(await shownIds(), [originalIds[2]]);
    await page.getByLabel("Show").selectOption("active");
    assert.deepEqual(await shownIds(), [originalIds[0], originalIds[1]]);
    await page.getByLabel("Show").selectOption("all");
    await page.reload();
    assert.deepEqual(await shownIds(), originalIds);
    assert.deepEqual(await boxes.evaluateAll(items => items.map(el => el.checked)), [false, false, true]);
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    checks.push(width + "px: duplicate-title identity, both matrix rows, ordering, reload persistence and no overflow");
    await page.getByText("About this exercise", { exact: true }).click();
    await page.getByRole("button", { name: "Reset practice data" }).click();
    for (const filter of ["all", "active", "completed"]) {
      await page.getByLabel("Show").selectOption(filter);
      await expect(boxes).toHaveCount(0);
      await expect(page.locator("#empty")).toBeVisible();
    }
    checks.push(width + "px: all three empty-filter cases after the scoped reset");
    await context.close();
  }
  const report = {
    checkedAt: new Date().toISOString(),
    environment: "Windows / Edge " + browser.version(),
    method: "Serve the original start files with only the exact authored visibleTasks repair applied in memory.",
    limitations: "Fictional local reference; no Codex model execution, deployment or physical mobile device.",
    moduleHash: createHash("sha256").update(author).digest("hex"),
    servedFileHashes: Object.fromEntries([...files].map(([name, contents]) => [
      name, createHash("sha256").update(contents).digest("hex"),
    ])),
    checks,
  };
  await writeFile("docs/codex-learning/evidence/feature-browser.json", JSON.stringify(report, null, 2) + "\n");
  console.log("Passed " + checks.length + " feature-browser checks");
} finally {
  await browser.close();
  await new Promise(done => server.close(done));
}
