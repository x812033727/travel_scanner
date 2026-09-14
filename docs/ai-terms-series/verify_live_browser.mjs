// Read-only post-publication QA. No login, forms, account state, or site writes.
// Usage: node docs/ai-terms-series/verify_live_browser.mjs --plan
//        node docs/ai-terms-series/verify_live_browser.mjs --smoke
//        node docs/ai-terms-series/verify_live_browser.mjs --full
// --smoke checks only the existing glossary against the reviewed pack; it never
// counts as series acceptance. --plan and --help do not launch Chrome or use a network.
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const origin = "https://mokaair.com";
const chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "desktop", width: 1440, height: 1000 },
];
const representatives = new Set([
  "ai-terms-index", "ai-term-loop-engineering", "ai-glossary-50-terms",
  "ai-term-model-context-protocol", "ai-term-retrieval-augmented-generation",
  "ai-term-diffusion-model",
]);
const digest = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const normalizeText = value => String(value ?? "").replace(/\s+/g, " ").trim();
const args = process.argv.slice(2);
if (args.length !== 1 || !["--help", "--plan", "--smoke", "--full"].includes(args[0])) {
  console.error("Choose exactly one of --help, --plan, --smoke, --full.");
  process.exitCode = 2;
} else if (args[0] === "--help") {
  console.log("Read-only production QA using installed headless Chrome.\n" +
    "--plan: local source/manifest check and scope only; no browser/network.\n" +
    "--smoke: glossary only, both widths, same assertions; not full acceptance.\n" +
    "--full: all 83 pages, 166 viewport observations, one sequential page.\n" +
    "Reports: docs/ai-terms-series/live-browser-{check,smoke}.json\n" +
    "Representative screenshots: docs/ai-terms-series/qa/live/<run>/\n" +
    "Run only after root has completed the relevant publication step.");
} else {
  await main(args[0]).catch(error => {
    console.error("Browser verification stopped: " + error.message);
    process.exitCode = 1;
  });
}

async function expectedArticles() {
  const catalogue = JSON.parse(await fs.readFile(path.join(here, "catalogue.json"), "utf8"));
  const slugs = [...catalogue.terms.map(term => term.slug), "ai-terms-index", "ai-glossary-50-terms"];
  if (catalogue.terms.length !== 81 || slugs.length !== 83 || new Set(slugs).size !== 83) {
    throw new Error("Expected exactly 81 terms, one index, and one glossary.");
  }
  const manifestBytes = await fs.readFile(path.join(here, "release-manifest.json"));
  const manifest = JSON.parse(manifestBytes);
  if (manifest.locale !== "zh-TW" || manifest.slugs.length !== 83 ||
      new Set(manifest.slugs).size !== 83 || slugs.some(slug => !manifest.slugs.includes(slug))) {
    throw new Error("Release manifest scope differs from the exact 83 zh-TW pages.");
  }
  const articles = [];
  for (const slug of slugs) {
    const relative = "apps/api/app/guides/content/" + slug + ".json";
    const bytes = await fs.readFile(path.join(root, relative));
    if (manifest.files[relative] !== digest(bytes)) throw new Error(slug + ": pack SHA256 mismatch");
    const pack = JSON.parse(bytes);
    if (pack.slug !== slug || pack.kind !== "life" || Object.keys(pack.locales).join() !== "zh-TW") {
      throw new Error(slug + ": unexpected pack identity/locale");
    }
    const doc = pack.locales["zh-TW"];
    const imagePaths = [doc.hero?.src, ...doc.blocks.filter(block => block.type === "image").map(block => block.src)];
    if (imagePaths.some(src => !src?.startsWith("/guides/"))) throw new Error(slug + ": missing/local image expected");
    articles.push({
      slug, url: origin + "/zh-TW/life/" + slug,
      title: doc.title, description: doc.description, imagePaths,
      tableCount: doc.blocks.filter(block => block.type === "table").length,
      packSha256: digest(bytes),
    });
  }
  return { articles, manifestSha256: digest(manifestBytes) };
}

async function main(mode) {
  const expected = await expectedArticles();
  const articles = mode === "--smoke"
    ? expected.articles.filter(article => article.slug === "ai-glossary-50-terms")
    : expected.articles;
  if (mode === "--plan") {
    console.log(JSON.stringify({
      mode: "plan", browserLaunched: false, networkRequests: 0,
      origin, pages: articles.length, viewportChecks: articles.length * viewports.length,
      widths: viewports.map(viewport => viewport.width),
      representativeScreenshots: [...representatives],
      manifestSha256: expected.manifestSha256,
    }, null, 2));
    return;
  }
  await fs.access(chrome);
  const startedAt = new Date().toISOString();
  const runId = startedAt.replace(/[:.]/g, "-");
  const screenshotDir = path.join(here, "qa/live", runId);
  const reportPath = path.join(here, mode === "--full" ? "live-browser-check.json" : "live-browser-smoke.json");
  await fs.mkdir(screenshotDir, { recursive: true });
  const report = {
    mode: mode.slice(2), origin, startedAt, finishedAt: null, status: "running",
    scope: "Unauthenticated production DOM/browser checks only; no API publication or login.",
    limitations: [
      "POST/PUT/PATCH/DELETE and other non-GET/HEAD requests are blocked.",
      "No claim about search-engine indexing, all external links, or authenticated flows.",
      "A screenshot file is capture evidence; it is not a claim of human visual review.",
    ],
    manifestSha256: expected.manifestSha256, browserVersion: null,
    plannedPages: articles.length, plannedViewportChecks: articles.length * viewports.length,
    blockedNonReadRequests: 0, blockedPrefetchRequests: 0,
    results: [], fatalError: null, fullSeriesVerified: false,
  };
  async function save() {
    // QA checkpoints are replaceable; the server-side publication journal keeps
    // its separate atomic/fsync contract. Avoid Windows rename-overwrite locks.
    await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + "\n", "utf8");
  }
  await save();
  let browser;
  try {
    browser = await chromium.launch({ executablePath: chrome, headless: true });
    report.browserVersion = browser.version();
    const context = await browser.newContext({
      viewport: { width: viewports[0].width, height: viewports[0].height },
      locale: "zh-TW", serviceWorkers: "block",
    });
    // Fresh ephemeral context: no profile, storageState, cookies, or account login.
    await context.route("**/*", route => {
      if (!["GET", "HEAD"].includes(route.request().method())) {
        report.blockedNonReadRequests++;
        return route.abort("blockedbyclient");
      }
      const headers = route.request().headers();
      if (headers["next-router-prefetch"] === "1" || headers.purpose === "prefetch" ||
          headers["sec-purpose"]?.includes("prefetch")) {
        report.blockedPrefetchRequests++;
        return route.abort("blockedbyclient");
      }
      // Never follow an unexpected main-frame redirect into another site/account flow.
      if (route.request().isNavigationRequest() && route.request().frame().parentFrame() === null) {
        const target = new URL(route.request().url());
        if (target.origin !== origin || !target.pathname.startsWith("/zh-TW/life/")) {
          return route.abort("blockedbyclient");
        }
      }
      return route.continue();
    });
    const page = await context.newPage();
    page.setDefaultTimeout(12_000);
    for (const article of articles) {
      await page.setViewportSize({ width: viewports[0].width, height: viewports[0].height });
      let response;
      let navigationError = null;
      try {
        response = await page.goto(article.url, { waitUntil: "domcontentloaded", timeout: 30_000 });
        if ([403, 429].includes(response?.status())) {
          throw new Error("Access/rate-limit response " + response.status() + "; series stopped.");
        }
        await page.waitForSelector("article h1", { timeout: 12_000 });
      } catch (error) {
        navigationError = error.message;
        if ([403, 429].includes(response?.status())) {
          report.fatalError = navigationError;
        }
      }
      for (const viewport of viewports) {
        const result = {
          slug: article.slug, viewport: viewport.name, width: viewport.width, height: viewport.height,
          url: article.url, finalUrl: page.url(), httpStatus: response?.status() ?? null,
          packSha256: article.packSha256, checkedAt: new Date().toISOString(),
          status: "failed", failures: [], screenshots: [],
        };
        if (navigationError) result.failures.push("Navigation/article readiness: " + navigationError);
        if (result.httpStatus !== 200) result.failures.push("Expected HTTP 200");
        if (result.finalUrl !== article.url) result.failures.push("Unexpected final URL");
        try {
          if (report.fatalError) throw new Error(report.fatalError);
          await page.setViewportSize({ width: viewport.width, height: viewport.height });
          await page.evaluate(async () => {
            scrollTo(0, 0);
            await Promise.race([document.fonts.ready, new Promise(resolve => setTimeout(resolve, 3000))]);
            await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          });
          await inspect(page, article, result, response);
          if (representatives.has(article.slug)) {
            await page.evaluate(() => scrollTo(0, 0));
            const topFile = path.join(screenshotDir, article.slug + "-" + viewport.name + "-top.png");
            await page.screenshot({ path: topFile, animations: "disabled", timeout: 45_000 });
            result.screenshots.push(path.relative(here, topFile).replaceAll("\\", "/"));
            const table = page.locator("article table").first();
            if (await table.count()) {
              await table.scrollIntoViewIfNeeded();
              const tableFile = path.join(screenshotDir, article.slug + "-" + viewport.name + "-table.png");
              await page.screenshot({ path: tableFile, animations: "disabled", timeout: 45_000 });
              result.screenshots.push(path.relative(here, tableFile).replaceAll("\\", "/"));
            }
          }
        } catch (error) {
          result.failures.push("Browser inspection: " + error.message);
        }
        result.status = result.failures.length ? "failed" : "passed";
        report.results.push(result);
      }
      await save();
      console.log(article.slug + ": " + report.results.slice(-2).map(result => result.viewport + "=" + result.status).join(", "));
      if (report.fatalError) break;
      await page.waitForTimeout(200);
    }
  } catch (error) {
    report.fatalError = error.message;
  } finally {
    if (browser) await browser.close().catch(() => {});
    const checked = new Set(report.results.map(result => result.slug + ":" + result.viewport));
    for (const article of articles) for (const viewport of viewports) {
      if (!checked.has(article.slug + ":" + viewport.name)) {
        report.results.push({
          slug: article.slug, viewport: viewport.name, width: viewport.width, height: viewport.height,
          url: article.url, status: "not_run", failures: ["Run stopped before this viewport."],
        });
      }
    }
    report.finishedAt = new Date().toISOString();
    report.summary = {
      passed: report.results.filter(result => result.status === "passed").length,
      failed: report.results.filter(result => result.status === "failed").length,
      notRun: report.results.filter(result => result.status === "not_run").length,
      pagesAttempted: new Set(report.results.filter(result => result.status !== "not_run").map(result => result.slug)).size,
    };
    report.status = report.fatalError || report.summary.failed || report.summary.notRun ? "failed" : "passed";
    report.fullSeriesVerified = mode === "--full" && report.status === "passed" &&
      report.summary.passed === 166 && report.summary.pagesAttempted === 83;
    await save();
  }
  console.log(JSON.stringify({
    report: path.relative(root, reportPath), status: report.status,
    ...report.summary, fullSeriesVerified: report.fullSeriesVerified,
  }));
  if (report.status !== "passed") process.exitCode = 1;
}

async function inspect(page, article, result, response) {
  const headings = await page.locator("h1").allTextContents();
  result.h1 = headings.map(normalizeText);
  if (headings.length !== 1 || normalizeText(headings[0]) !== normalizeText(article.title)) {
    result.failures.push("H1 differs from reviewed title or H1 count is not one.");
  }
  const canonical = await page.locator('link[rel="canonical"]').evaluateAll(nodes => nodes.map(node => node.href));
  result.canonical = canonical;
  if (canonical.length !== 1 || canonical[0] !== article.url) result.failures.push("Canonical mismatch.");
  const metaRobots = await page.locator("meta[name]").evaluateAll(nodes => nodes
    .filter(node => /^(robots|googlebot|bingbot)$/i.test(node.name))
    .map(node => ({ name: node.name, content: node.content })));
  const xRobots = response ? await response.headerValue("x-robots-tag") : null;
  result.robots = { meta: metaRobots, header: xRobots };
  if ([...metaRobots.map(item => item.content), xRobots ?? ""].some(value => /\b(noindex|none)\b/i.test(value))) {
    result.failures.push("Page contains a noindex/none robots directive.");
  }
  const description = await page.locator("article header h1").evaluateAll(nodes =>
    nodes[0]?.nextElementSibling?.textContent ?? "");
  if (normalizeText(description) !== normalizeText(article.description)) {
    result.failures.push("Visible article description differs from reviewed pack.");
  }
  const images = page.locator("article figure img");
  for (let index = 0; index < await images.count(); index++) {
    const image = images.nth(index);
    await image.scrollIntoViewIfNeeded();
    await image.evaluate(img => new Promise(resolve => {
      if (img.complete && img.naturalWidth > 0) return resolve();
      const timeout = setTimeout(resolve, 12_000);
      img.addEventListener("load", () => { clearTimeout(timeout); resolve(); }, { once: true });
    }));
  }
  result.images = await images.evaluateAll(nodes => nodes.map(img => ({
    path: new URL(img.currentSrc || img.src, location.href).pathname,
    loaded: img.complete && img.naturalWidth > 0 && img.getBoundingClientRect().width > 0,
    naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight,
  })));
  for (const src of article.imagePaths) {
    const matches = result.images.filter(image => image.path === src);
    if (matches.length !== 1 || !matches[0].loaded) result.failures.push("Missing/broken article image: " + src);
  }
  if (result.images.some(image => !image.loaded)) result.failures.push("An article figure image failed to load.");
  result.layout = await page.evaluate(() => {
    const root = document.documentElement;
    const globalWidth = () => Math.max(root.scrollWidth, document.body?.scrollWidth ?? 0);
    const tables = [...document.querySelectorAll("article table")].map(table => {
      const wrapper = table.parentElement;
      const before = wrapper.scrollLeft;
      const windowX = scrollX;
      const overflowX = getComputedStyle(wrapper).overflowX;
      const requiresScroll = wrapper.scrollWidth > wrapper.clientWidth + 1;
      wrapper.scrollLeft = wrapper.scrollWidth;
      const internalScrollWorks = !requiresScroll ||
        (["auto", "scroll"].includes(overflowX) && wrapper.scrollLeft > 0 && scrollX === windowX);
      const contentWidthDuringScroll = globalWidth();
      wrapper.scrollLeft = before;
      return {
        clientWidth: wrapper.clientWidth, scrollWidth: wrapper.scrollWidth, overflowX,
        requiresScroll, internalScrollWorks, contentWidthDuringScroll,
      };
    });
    return { viewportWidth: innerWidth, clientWidth: root.clientWidth, contentWidth: globalWidth(), tables };
  });
  if (result.layout.contentWidth > result.layout.clientWidth + 1) result.failures.push("Whole-page horizontal overflow.");
  if (result.layout.tables.length !== article.tableCount) result.failures.push("Rendered table count differs from pack.");
  if (result.layout.tables.some(table => !table.internalScrollWorks ||
      table.contentWidthDuringScroll > result.layout.clientWidth + 1)) {
    result.failures.push("Table does not scroll internally without whole-page overflow.");
  }
}
