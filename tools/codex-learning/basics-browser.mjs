import { chromium, expect } from "@playwright/test";
import { createServer } from "node:http";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve } from "node:path";
import assert from "node:assert/strict";

const root = resolve("docs/codex-learning/practice/expected");
const names = ["index.html", "style.css", "app.js", "core.mjs"];
const original = Object.fromEntries(await Promise.all(names.map(async name => [name, await readFile(resolve(root, name), "utf8")])));
const variants = {
  project: { ...original, "index.html": original["index.html"].replace("Make room for one small task.", "Small steps, clear progress."), "style.css": original["style.css"].replace("#f2f5ef", "#fff8ed") },
  prompt: { ...original, "index.html": original["index.html"].replace(">Add task</button>", ">Save task</button>").replace('placeholder="Read the project README"', 'placeholder="Plan one small step"') },
};
assert.notEqual(variants.project["index.html"], original["index.html"]);
assert.notEqual(variants.prompt["index.html"], original["index.html"]);
const server = createServer((request, response) => {
  const [, variant, file = ""] = new URL(request.url, "http://localhost").pathname.split("/");
  const name = file || "index.html";
  if (!Object.hasOwn(variants, variant) || !names.includes(name)) { response.writeHead(404).end(); return; }
  const type = name.endsWith("html") ? "text/html" : name.endsWith("css") ? "text/css" : "text/javascript";
  response.writeHead(200, { "Content-Type": `${type}; charset=utf-8` });
  response.end(variants[variant][name]);
});
await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
const browser = await chromium.launch({ channel: "msedge", headless: true });
const report = { checkedAt: new Date().toISOString(), environment: `Windows / Edge ${browser.version()}`, method: "Reference edits applied to the original practice files, then tested in a real browser. No Codex model execution or physical phone test is claimed.", checks: [], errors: [] };
try {
  for (const [variant, slug] of [["project", "codex-first-project"], ["prompt", "codex-prompting"]]) {
    const output = resolve("apps/web/public/guides", slug);
    await mkdir(output, { recursive: true });
    for (const width of [360, 390, 1280]) {
      const context = await browser.newContext({ viewport: { width, height: 900 } });
      const page = await context.newPage();
      page.on("pageerror", error => report.errors.push(error.message));
      await page.goto(`http://127.0.0.1:${server.address().port}/${variant}/`);
      if (variant === "project") {
        await expect(page.getByRole("heading", { level: 1 })).toHaveText("Small steps, clear progress.");
        assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).backgroundColor), "rgb(255, 248, 237)");
      } else {
        await expect(page.getByPlaceholder("Plan one small step")).toBeVisible();
        await expect(page.getByRole("button", { name: "Save task", exact: true })).toBeVisible();
        assert.equal(await page.locator("#task-title").getAttribute("name"), "title");
        assert.equal(await page.locator("#task-title").getAttribute("maxlength"), "100");
        assert.equal(await page.locator("#task-form button").getAttribute("type"), "submit");
      }
      const input = page.getByRole("textbox", { name: "New task", exact: true });
      for (const title of ["Read", "Build"]) {
        await input.fill(title);
        await input.press("Enter");
      }
      await page.getByRole("checkbox", { name: "Read", exact: true }).check();
      await page.locator("#filter").selectOption("completed");
      await expect(page.locator("#tasks li")).toHaveCount(1);
      await expect(page.locator("#tasks li span")).toHaveText("Read");
      await page.reload();
      await expect(page.getByRole("checkbox", { name: "Read", exact: true })).toBeChecked();
      await input.fill("   ");
      await input.press("Enter");
      await expect(page.locator("#tasks li")).toHaveCount(2);
      await input.fill("<img src=x>");
      await input.press("Enter");
      await expect(page.locator("#tasks li")).toHaveCount(3);
      await expect(page.locator("#tasks img")).toHaveCount(0);
      await expect(page.locator("#tasks li span").last()).toHaveText("<img src=x>");
      await input.focus();
      await page.keyboard.press("Tab");
      await expect(page.locator("#task-form button")).toBeFocused();
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({ path: resolve(output, `reference-${width}.png`) });
      report.checks.push(`${variant}/${width}: exact requested changes, preserved form hooks, add, complete, filter, reload, whitespace rejection, inert markup, keyboard focus and no page overflow`);
      await context.close();
    }
  }
  assert.deepEqual(report.errors, []);
} finally {
  await writeFile("docs/codex-learning/evidence/basics-browser.json", JSON.stringify(report, null, 2) + "\n");
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
console.log(`${report.checks.length} foundational exercise browser checks passed`);
