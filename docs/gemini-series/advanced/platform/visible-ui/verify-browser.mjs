/** Real Chromium + React SSR/hydration with product components/CSS, outside Next routing. */
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createHash } from "node:crypto";

const here = path.dirname(fileURLToPath(import.meta.url));
const workspace = path.resolve(here, "../../../../..");
const web = path.join(workspace, "apps/web");
const require = createRequire(path.join(web, "package.json"));
const { build } = await import(pathToFileURL(require.resolve("vite")));
const { chromium } = require("playwright");
const postcss = require("postcss");
const tailwind = require("@tailwindcss/postcss");
const output = path.join(here, ".build");
const evidence = path.join(here, "evidence");
await mkdir(evidence, { recursive: true });
const modules = [];
const config = { configFile: false, root: web, logLevel: "error", define: { "process.env.NODE_ENV": '"production"' }, resolve: { alias: { "@": web } } };
await build({ ...config, build: { ssr: path.join(here, "server.tsx"), outDir: path.join(output, "server"),
  rollupOptions: { output: { entryFileNames: "server.mjs" } } } });
await build({ ...config, plugins: [{ name: "check-client-boundary", generateBundle() {
  for (const id of this.getModuleIds()) modules.push(id.replaceAll("\\", "/"));
  assert.ok(!modules.some(id => /guide-series\.json|curriculum\.json|fixture\.test-data|gemini-series\.server/.test(id)), "Client imported unfiltered catalogue");
} }], build: { outDir: path.join(output, "client"), lib: { entry: path.join(here, "client.tsx"), name: "VisibleGeminiFixture", formats: ["iife"], fileName: () => "client.js" } } });
const cssFile = path.join(web, "app/globals.css");
const css = await postcss([tailwind({ base: web })]).process(await readFile(cssFile, "utf8"), { from: cssFile });
const script = await readFile(path.join(output, "client/client.js"));
const fixture = await import(pathToFileURL(path.join(output, "server/server.mjs")));
const browser = await chromium.launch({ headless: true });
const report = { checkedAt: new Date().toISOString(), method: "isolated product-component SSR + hydration, actual site CSS; not Next routing/RSC or production", browser: browser.version(),
  clientHasCatalogue: false, clientSha256: createHash("sha256").update(script).digest("hex"), scenarios: [], sourceFiles: [] };
const errors = [];
const servers = [];
try {
  for (const advanced of [false, true]) {
    const series = fixture.fixtureSeries(advanced);
    const server = createServer((request, response) => {
      const pathname = new URL(request.url, "http://127.0.0.1").pathname;
      if (pathname === "/client.js") { response.setHeader("Content-Type", "application/javascript"); response.end(script); return; }
      if (pathname === "/style.css") { response.setHeader("Content-Type", "text/css"); response.end(css.css); return; }
      const slug = pathname.split("/").at(-1) || series.hubSlug;
      const html = fixture.renderPage(advanced, slug);
      response.statusCode = html ? 200 : 404;
      response.setHeader("Content-Type", "text/html; charset=utf-8");
      response.end(html ?? "Not found");
    });
    await new Promise(resolve => server.listen(0, "127.0.0.1", resolve)); servers.push(server);
    const origin = `http://127.0.0.1:${server.address().port}`;
    const hub = `${origin}/zh-TW/life/${series.hubSlug}`;
    for (const [index, article] of series.articles.entries()) {
      const html = fixture.renderPage(advanced, article.slug);
      for (const [rel, target] of [["prev", series.articles[index - 1]], ["next", series.articles[index + 1]]]) {
        const match = html.match(new RegExp(`rel="${rel}" href="([^"]+)"`));
        assert.equal(match?.[1], target ? `/zh-TW/life/${target.slug}` : undefined);
      }
    }
    for (const [width, javaScriptEnabled] of [[1200, true], [360, true], [360, false]]) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, javaScriptEnabled, permissions: ["clipboard-read", "clipboard-write"] });
      const page = await context.newPage();
      page.on("pageerror", error => errors.push(error.message));
      page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
      const response = await page.goto(hub);
      const html = await response.text();
      if (javaScriptEnabled) await page.waitForSelector('html[data-hydrated="true"]');
      assert.equal(await page.locator('[data-testid="series-lessons"] a').count(), series.articles.length);
      assert.equal(await page.locator('nav[aria-label="建議學習路線"] details').count(), advanced ? 11 : 5);
      if (!advanced) for (const hidden of fixture.fixtureSeries(true).articles.slice(50)) assert.ok(!html.includes(hidden.slug) && !script.includes(hidden.slug));
      const overflow = async () => assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${width}px overflow at ${page.url()}`);
      await overflow();
      const name = `${advanced ? "86" : "50"}-${width}-${javaScriptEnabled ? "js" : "no-js"}`;
      await page.screenshot({ path: path.join(evidence, `${name}.png`) });
      if (javaScriptEnabled) {
        for (const query of ["MD", "GEMINI.md", "手機", "CLI", "/memory", "NotebookLM"]) {
          await page.getByRole("searchbox").fill(query);
          await page.waitForFunction(() => document.querySelector('[role="status"]')?.textContent !== "");
          assert.ok(await page.locator('[data-testid="series-lessons"] a').count() > 0);
          await page.getByRole("button", { name: "清除篩選" }).click();
        }
        if (advanced) {
          await page.getByLabel("教學階段").selectOption("2");
          assert.equal(await page.locator('[data-testid="series-lessons"] a').count(), 36);
          await page.getByLabel("深入主題").selectOption("md");
          assert.equal(await page.locator('[data-testid="series-lessons"] a').count(), 6);
          await page.getByRole("combobox", { name: /^學習路線/ }).selectOption("advanced-md");
          await overflow();
          await page.screenshot({ path: path.join(evidence, `filtered-${width}.png`) });
          await page.getByRole("button", { name: "清除篩選" }).click();
          assert.equal(await page.locator('[data-testid="series-lessons"] a').count(), 86);
        }
        await page.getByRole("searchbox").fill("zz不存在zz");
        await page.getByText(/沒有符合的教學/).waitFor();
        await page.getByRole("button", { name: "清除篩選" }).click();
        const entry = series.articles[49];
        await page.locator('[data-testid="series-lessons"] a').filter({ hasText: entry.title }).click();
        await page.getByRole("button", { name: "複製", exact: true }).click();
        await page.getByText("已複製", { exact: true }).waitFor();
        const clipboard = await page.evaluate(() => navigator.clipboard.readText());
        assert.equal(clipboard.replaceAll("\r\n", "\n"), fixture.sample);
        report.clipboardLineEndings = clipboard.includes("\r\n") ? "Windows CRLF; only CRLF normalized for comparison" : "LF";
        assert.equal(await page.locator('a[rel="next"]').count(), advanced ? 1 : 0);
        await overflow();
        await page.screenshot({ path: path.join(evidence, `lesson-${advanced ? "86" : "50"}-${width}.png`) });
        await page.getByRole("link", { name: "返回 Gemini 教學總目錄" }).first().click();
        assert.equal(new URL(page.url()).pathname, `/zh-TW/life/${series.hubSlug}`);
      } else {
        await page.locator('[data-testid="series-lessons"] a').last().click();
        assert.equal(await page.locator('a[rel="next"]').count(), 0);
        await overflow();
        await page.getByRole("link", { name: "返回 Gemini 教學總目錄" }).first().click();
      }
      report.scenarios.push({ name, lessons: series.articles.length, routes: series.paths.length, width, javaScriptEnabled, passed: true });
      await context.close();
      console.log(`${name}: passed`);
    }
  }
  assert.deepEqual(errors, [], "Browser console/hydration errors");
  for (const relative of ["apps/web/components/gemini-series/directory.tsx", "apps/web/components/gemini-series/navigation.tsx", "apps/web/lib/gemini-series-projection.ts", "apps/web/app/globals.css", "apps/web/components/guide-code-block.tsx"]) {
    report.sourceFiles.push({ path: relative, sha256: createHash("sha256").update(await readFile(path.join(workspace, relative))).digest("hex") });
  }
  report.navigationPagesChecked = 136;
  await writeFile(path.join(evidence, "browser.json"), JSON.stringify(report, null, 2) + "\n");
} catch (error) {
  await writeFile(path.join(evidence, "failure.json"), JSON.stringify({ error: String(error), browserErrors: errors, completed: report.scenarios }, null, 2) + "\n");
  throw error;
} finally {
  await browser.close();
  await Promise.all(servers.map(server => new Promise(resolve => server.close(resolve))));
}
