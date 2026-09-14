import { chromium, expect } from "@playwright/test";
import { createServer } from "node:http";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
import assert from "node:assert/strict";

const root = resolve("docs/codex-learning/practice");
const mime = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript" };
const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url, "http://localhost");
    const file = resolve(root, "." + decodeURIComponent(url.pathname) + (url.pathname.endsWith("/") ? "index.html" : ""));
    if (!file.startsWith(root + sep)) { response.writeHead(403).end(); return; }
    const body = await readFile(file);
    response.writeHead(200, { "Content-Type": mime[extname(file)] ?? "text/plain" }).end(body);
  } catch { response.writeHead(404).end(); }
});
await new Promise((done) => server.listen(0, "127.0.0.1", done));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ channel: "msedge", headless: true });
const checks = [];
try {
  for (const width of [360, 390, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.goto(origin + "/expected/");
    await page.getByLabel("New task").fill("Read");
    await page.getByRole("button", { name: "Add task" }).click();
    await page.getByLabel("New task").fill("Build");
    await page.getByRole("button", { name: "Add task" }).click();
    await page.getByRole("checkbox", { name: "Read" }).check();
    await expect(page.getByRole("checkbox", { name: "Read" })).toBeFocused();
    await page.getByLabel("Show").selectOption("active");
    await expect(page.locator("#tasks li")).toHaveCount(1);
    await expect(page.getByRole("checkbox", { name: "Build" })).toBeVisible();
    await page.getByLabel("Show").selectOption("completed");
    await expect(page.getByRole("checkbox", { name: "Read" })).toBeChecked();
    await page.reload();
    await expect(page.locator("#tasks li")).toHaveCount(2);
    await expect(page.getByRole("checkbox", { name: "Read" })).toBeChecked();
    await page.getByRole("button", { name: "Delete Read", exact: true }).click();
    await expect(page.getByRole("button", { name: "Delete Build", exact: true })).toBeFocused();
    await expect(page.locator("#tasks li")).toHaveCount(1);
    await page.getByLabel("New task").fill("   ");
    await page.getByRole("button", { name: "Add task" }).click();
    await expect(page.getByRole("status")).toContainText("non-blank");
    await page.getByLabel("New task").fill('<img src=x onerror="alert(1)">');
    await page.getByRole("button", { name: "Add task" }).click();
    await expect(page.locator("#tasks li")).toHaveCount(2);
    assert.equal(await page.locator("#tasks img").count(), 0);
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.getByLabel("New task").focus();
    await page.keyboard.press("Tab");
    await expect(page.getByRole("button", { name: "Add task" })).toBeFocused();
    // Keep screenshots clean and fictional, with both active and completed tasks.
    await page.getByRole("button", { name: 'Delete <img src=x onerror="alert(1)">', exact: true }).click();
    await page.getByLabel("New task").fill("Read the AGENTS.md rules");
    await page.getByRole("button", { name: "Add task" }).click();
    await page.getByRole("checkbox", { name: "Build", exact: true }).check();
    await page.screenshot({ path: resolve(`apps/web/public/guides/codex-first-project/todo-${width}.png`), fullPage: true });
    checks.push(`${width}px: create, toggle, filter, reload persistence, delete, whitespace rejection, HTML as text, keyboard, no horizontal overflow`);
    await page.evaluate(() => localStorage.setItem("mokaair-codex-todo-v1", "corrupt"));
    await page.reload();
    await expect(page.getByRole("status")).toContainText("cannot be read");
    await page.getByLabel("New task").fill("Temporary");
    await page.getByRole("button", { name: "Add task" }).click();
    assert.equal(await page.evaluate(() => localStorage.getItem("mokaair-codex-todo-v1")), "corrupt");
    await page.getByText("About this exercise", { exact: true }).click();
    await page.getByRole("button", { name: "Reset practice data" }).click();
    assert.equal(await page.evaluate(() => localStorage.getItem("mokaair-codex-todo-v1")), null);
    checks.push(`${width}px: corrupt storage preserved until explicit reset`);
    await page.close();
  }
  const report = { date: new Date().toISOString(), environment: `Windows / Edge ${browser.version()}`, scope: "Standalone fictional practice app; mobile widths are emulated", checks };
  await mkdir("docs/codex-learning/evidence", { recursive: true });
  await writeFile("docs/codex-learning/evidence/practice-browser.json", JSON.stringify(report, null, 2) + "\n");
  console.log(JSON.stringify(report, null, 2));
} finally { await browser.close(); await new Promise(done => server.close(done)); }
