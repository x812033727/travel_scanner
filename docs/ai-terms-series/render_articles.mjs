// Render the repository's real ContentBlocks component to offline HTML.
// No listening HTTP server, API credentials, or production writes.
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createServer } from "vite";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { chromium } from "@playwright/test";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const web = path.join(root, "apps/web");
const server = await createServer({
  root: web, configFile: false,
  resolve: { alias: { "@": web } },
  esbuild: { jsx: "automatic" },
  server: { middlewareMode: true, hmr: false, watch: null },
  optimizeDeps: { noDiscovery: true, include: [] },
});
const output = path.join(here, "qa/articles");
await fs.mkdir(output, { recursive: true });
const { ContentBlocks } = await server.ssrLoadModule("/components/content-blocks.tsx");
const catalogue = JSON.parse(await fs.readFile(path.join(here, "catalogue.json"), "utf8"));
const slugs = process.argv.slice(2).length ? process.argv.slice(2) : [...catalogue.terms.map(t => t.slug), "ai-terms-index", "ai-glossary-50-terms"];
const chunkDir = path.join(web, ".next/static/chunks");
const cssFiles = (await fs.readdir(chunkDir)).filter(f => f.endsWith(".css"));
const css = (await Promise.all(cssFiles.map(f => fs.readFile(path.join(chunkDir, f), "utf8")))).join("\n");
const labels = { imageCredit: "圖片：", tip: "小提醒", warning: "注意", info: "補充" };
const browser = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
const results = [];
try {
  for (const slug of slugs) {
    const pack = JSON.parse(await fs.readFile(path.join(root, "apps/api/app/guides/content", slug + ".json"), "utf8"));
    const doc = pack.locales["zh-TW"];
    const body = renderToStaticMarkup(React.createElement(ContentBlocks, { blocks: doc.blocks, labels, headingStart: 0 }));
    const heading = renderToStaticMarkup(React.createElement("header", null,
      React.createElement("h1", { className: "text-3xl font-bold" }, doc.title),
      React.createElement("p", { className: "mt-3 leading-7" }, doc.description)));
    const hero = renderToStaticMarkup(React.createElement("img", { ...doc.hero, credit: undefined, className: "h-auto w-full rounded-2xl" }));
    const html = '<!doctype html><html lang="zh-TW"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>' + css + '</style><body><main class="mx-auto max-w-3xl px-5 py-10"><article class="space-y-6 break-words [overflow-wrap:anywhere]">' + heading + hero + body + '</article></main></body></html>';
    await fs.writeFile(path.join(output, slug + ".html"), html);
    for (const [name, width, height] of [["mobile", 375, 812], ["desktop", 1440, 1000]]) {
      const page = await browser.newPage({ viewport: { width, height } });
      await page.route("**/*", async route => {
        const url = new URL(route.request().url());
        if (url.hostname === "local-preview.invalid" && url.pathname.startsWith("/guides/")) {
          const file = path.resolve(web, "public", "." + url.pathname);
          if (!file.startsWith(path.resolve(web, "public/guides") + path.sep)) return route.abort();
          try { return await route.fulfill({ body: await fs.readFile(file), contentType: file.endsWith(".svg") ? "image/svg+xml" : "image/jpeg" }); }
          catch { return route.abort(); }
        }
        return route.abort();
      });
      await page.setContent(html.replace("<meta charset", '<base href="https://local-preview.invalid/"><meta charset'), { waitUntil: "load" });
      await page.evaluate(async () => {
        document.querySelectorAll("img").forEach(img => img.loading = "eager");
        await document.fonts.ready;
        await Promise.all([...document.images].map(img => img.decode()));
      });
      const metrics = await page.evaluate(() => ({
        pageWidth: innerWidth, contentWidth: document.documentElement.scrollWidth,
        images: [...document.images].map(i => ({ src: i.getAttribute("src"), loaded: i.naturalWidth > 0 })),
        tables: [...document.querySelectorAll("table")].map(t => ({
          widths: [...t.querySelectorAll("th")].map(c => c.getBoundingClientRect().width),
          scrollWidth: t.parentElement.scrollWidth, clientWidth: t.parentElement.clientWidth,
          wrap: getComputedStyle(t).overflowWrap,
        })),
      }));
      if (metrics.contentWidth > width) throw new Error(slug + " " + name + " page overflow");
      if (metrics.images.some(i => !i.loaded)) throw new Error(slug + " broken image");
      await page.screenshot({ path: path.join(output, slug + "-" + name + "-top.png") });
      const table = page.locator("table").first();
      if (await table.count()) {
        await table.scrollIntoViewIfNeeded();
        await page.screenshot({ path: path.join(output, slug + "-" + name + "-table.png") });
      }
      results.push({ slug, viewport: name, ...metrics });
      await page.close();
    }
    console.log("Checked offline article components " + slug);
  }
} finally { await browser.close(); await server.close(); }
await fs.writeFile(path.join(here, "article-layout-check.json"), JSON.stringify({ scope: "Offline real ContentBlocks with production CSS and article-width wrapper; no page routing or API integration", results }, null, 2));
