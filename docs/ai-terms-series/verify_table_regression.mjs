// Bounded, unauthenticated production regression check for shared ContentBlocks.
// --plan reads local sources only. --run is the only network/browser entry point.
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const origin = "https://mokaair.com";
const chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "desktop", width: 1440, height: 1000 },
];
const limits = { durationMs: 300_000, requests: 1200, tablesPerPage: 8, imagesPerPage: 20 };
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const relative = file => path.relative(here, file).replaceAll("\\", "/");
const args = process.argv.slice(2);

if (args.length !== 1 || !["--plan", "--run", "--resume", "--help"].includes(args[0])) {
  console.error("Choose exactly one of --plan, --run, --resume, --help.");
  process.exitCode = 2;
} else if (args[0] === "--help") {
  console.log("Read-only shared ContentBlocks regression checks.\n" +
    "--plan: inspect local sources and print exact scope; no network, browser, or output files.\n" +
    "--run: after deployment, visit the two fixed articles and one shared legal page at 375/1440px.\n" +
    "--resume: preserve passed checks with identical source evidence and rerun only incomplete checks.\n" +
    "Uses fresh headless Chrome; blocks non-GET/HEAD, prefetch and out-of-scope navigation.\n" +
    "Stops on HTTP 403/429, the request cap or the five-minute deadline; no retries.\n" +
    "Report: docs/ai-terms-series/table-live-regression.json\n" +
    "PNG evidence: docs/ai-terms-series/qa/table-live/<run>/");
} else {
  await main(args[0]).catch(error => {
    console.error("Table regression check stopped: " + error.message);
    process.exitCode = 1;
  });
}

async function localScope() {
  const sourceEvidence = [];
  async function readSource(file) {
    const bytes = await fs.readFile(path.join(root, file));
    sourceEvidence.push({ file, sha256: sha256(bytes) });
    return bytes.toString("utf8");
  }
  const pages = [];
  for (const [slug, route] of [
    ["bangkok-airport-to-city", "/zh-TW/guides/howto/bangkok-airport-to-city"],
    ["ai-model-tiers-explained", "/zh-TW/life/ai-model-tiers-explained"],
  ]) {
    const pack = JSON.parse(await readSource("apps/api/app/guides/content/" + slug + ".json"));
    const doc = pack.locales["zh-TW"];
    const tables = doc.blocks.filter(block => block.type === "table");
    if (pack.slug !== slug || !tables.length) throw new Error(slug + ": expected a local article with tables.");
    pages.push({
      slug, route, url: origin + route, kind: "table_article", selector: "main article",
      expectedColumns: tables.map(table => table.header.length),
      expectedImagePaths: [doc.hero?.src, ...doc.blocks.filter(block => block.type === "image").map(block => block.src)].filter(Boolean),
    });
  }
  const renderer = await readSource("apps/web/components/content-blocks.tsx");
  const article = await readSource("apps/web/components/guides/article.tsx");
  const information = await readSource("apps/web/components/site-information-page.tsx");
  const content = await readSource("apps/web/components/site-page-content.tsx");
  const privacy = await readSource("apps/web/app/[locale]/privacy/page.tsx");
  const terms = await readSource("apps/web/app/[locale]/terms/page.tsx");
  if (!renderer.includes("export function ContentBlocks") || !article.includes("<ContentBlocks")) {
    throw new Error("Could not confirm the shared article ContentBlocks renderer locally.");
  }
  const legalRoutes = [
    { route: "/zh-TW/privacy", confirmed: privacy.includes('<SiteInformationPage slug="privacy"') },
    { route: "/zh-TW/terms", confirmed: terms.includes('<SiteInformationPage slug="terms"') },
  ];
  if (legalRoutes.some(route => !route.confirmed)) throw new Error("Legal route source differs from the inspected route chain.");
  const legalShared = information.includes("<SitePageContent") && content.includes("<ContentBlocks");
  if (legalShared) pages.push({
    slug: "privacy", route: "/zh-TW/privacy", url: origin + "/zh-TW/privacy",
    kind: "shared_legal_page", selector: "main article", expectedColumns: null, expectedImagePaths: [],
  });
  return { pages, legal: { routes: legalRoutes, sharesContentBlocks: legalShared, selected: legalShared ? "/zh-TW/privacy" : null }, sourceEvidence };
}

async function main(mode) {
  const scope = await localScope();
  const plan = {
    origin, pages: scope.pages, viewportChecks: scope.pages.length * viewports.length, viewports,
    legal: scope.legal, sourceEvidence: scope.sourceEvidence, limits,
    assertions: [
      "Nonempty document title, article H1, and article body; all expected article images loaded.",
      "Every rendered table column is at least 112 CSS px (0.01px subpixel tolerance).",
      "Tables wider than their mobile wrapper scroll internally while the page stays fixed horizontally.",
      "document/body scrollWidth <= innerWidth before and during internal table scrolling.",
      "Desktop tables fit their container, allowing 1px collapsed-border rounding.",
      "The selected legal page must render its shared article content; tables are optional there.",
    ],
  };
  if (mode === "--plan") {
    console.log(JSON.stringify({ mode: "plan", browserLaunched: false, networkRequests: 0, filesWritten: 0, ...plan }, null, 2));
    return;
  }

  // Dynamic import keeps even browser-package initialization outside --plan.
  const { chromium } = await import("@playwright/test");
  await fs.access(chrome);
  const startedAt = new Date().toISOString();
  const screenshotDir = path.join(here, "qa/table-live", startedAt.replace(/[:.]/g, "-"));
  const reportPath = path.join(here, "table-live-regression.json");
  await fs.mkdir(screenshotDir, { recursive: true });
  const report = {
    mode: "run", startedAt, finishedAt: null, status: "running", ...plan,
    scope: "Unauthenticated production browser layout observations for three fixed public pages; no login or site writes.",
    limitations: [
      "Screenshots are capture evidence, not a claim of human visual review.",
      "No assertion about legal accuracy, article factual accuracy, publication, or authenticated flows.",
      "A legal fallback/status page does not exercise ContentBlocks and therefore cannot pass this check.",
    ],
    browserVersion: null, attemptedRequests: 0, blockedNonReadRequests: 0,
    blockedPrefetchRequests: 0, blockedNavigations: 0, fatalError: null, results: [],
  };
  if (mode === "--resume") {
    const previousBytes = await fs.readFile(reportPath);
    const previous = JSON.parse(previousBytes);
    if (previous.status !== "failed" || previous.fatalError ||
        JSON.stringify(previous.sourceEvidence) !== JSON.stringify(scope.sourceEvidence) ||
        JSON.stringify(previous.pages) !== JSON.stringify(scope.pages) ||
        previous.origin !== origin) throw new Error("Resume requires an incomplete run with identical scope and no fatal stop.");
    await fs.writeFile(path.join(screenshotDir, "previous-report.json"), previousBytes);
    report.startedAt = previous.startedAt;
    report.resumedAt = startedAt;
    report.previousAttempt = { sha256: sha256(previousBytes), report: relative(path.join(screenshotDir, "previous-report.json")), finishedAt: previous.finishedAt, summary: previous.summary };
    report.results = previous.results.filter(result => result.status === "passed");
  }
  async function save() {
    // This is a replaceable QA checkpoint, not the publication journal. Windows
    // preview/indexing handles can deny rename-overwrite of an existing report.
    await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + "\n", "utf8");
  }
  await save();
  let browser;
  let page;
  let activeUrl = null;
  let deadline;
  function stop(message) {
    report.fatalError ??= message;
    // Closing the current page interrupts a pending navigation/image wait immediately.
    if (page && !page.isClosed()) void page.close().catch(() => {});
  }
  try {
    deadline = setTimeout(() => {
      stop("Five-minute run deadline reached; remaining checks stopped without retry.");
      if (browser) void browser.close().catch(() => {});
    }, limits.durationMs);
    browser = await chromium.launch({ executablePath: chrome, headless: true, timeout: 30_000 });
    report.browserVersion = browser.version();
    const context = await browser.newContext({ locale: "zh-TW", serviceWorkers: "block" });
    // No persistent profile, storageState, credentials, login, forms or clicks.
    await context.route("**/*", route => {
      const request = route.request();
      report.attemptedRequests++;
      if (report.attemptedRequests > limits.requests) stop("Request limit reached; remaining checks stopped without retry.");
      if (report.fatalError) return route.abort("blockedbyclient");
      if (!["GET", "HEAD"].includes(request.method())) {
        report.blockedNonReadRequests++;
        return route.abort("blockedbyclient");
      }
      const headers = request.headers();
      if (headers["next-router-prefetch"] === "1" || headers.purpose?.includes("prefetch") || headers["sec-purpose"]?.includes("prefetch")) {
        report.blockedPrefetchRequests++;
        return route.abort("blockedbyclient");
      }
      if (request.isNavigationRequest() && request.frame().parentFrame() === null && request.url() !== activeUrl) {
        report.blockedNavigations++;
        return route.abort("blockedbyclient");
      }
      return route.continue();
    });
    context.on("response", response => {
      if ([403, 429].includes(response.status())) {
        stop("HTTP " + response.status() + " at " + response.url() + "; all remaining checks stopped without retry.");
      }
    });
    for (const target of scope.pages) {
      for (const viewport of viewports) {
        if (report.fatalError) break;
        if (report.results.some(result => result.slug === target.slug && result.viewport === viewport.name && result.status === "passed")) continue;
        const result = {
          slug: target.slug, kind: target.kind, viewport: viewport.name, width: viewport.width, height: viewport.height,
          url: target.url, checkedAt: new Date().toISOString(), status: "failed", failures: [], screenshots: [],
        };
        try {
          activeUrl = target.url;
          page = await context.newPage();
          page.setDefaultTimeout(12_000);
          await page.setViewportSize({ width: viewport.width, height: viewport.height });
          const response = await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 30_000 });
          result.httpStatus = response?.status() ?? null;
          result.finalUrl = page.url();
          if (result.httpStatus !== 200) throw new Error("Expected HTTP 200; got " + result.httpStatus);
          if (result.finalUrl !== target.url) throw new Error("Unexpected final URL: " + result.finalUrl);
          await page.waitForSelector(target.selector + " h1");
          await page.evaluate(async () => {
            await Promise.race([document.fonts.ready, new Promise(resolve => setTimeout(resolve, 3000))]);
            await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          });
          await inspect(page, target, viewport, result);
          await capture(page, target, viewport, result, screenshotDir);
        } catch (error) {
          result.failures.push(error.message);
        } finally {
          if (page && !page.isClosed()) await page.close().catch(() => {});
          page = null;
        }
        result.status = result.failures.length ? "failed" : "passed";
        report.results.push(result);
        await save();
        console.log(target.slug + " " + viewport.name + ": " + result.status);
      }
      if (report.fatalError) break;
    }
  } catch (error) {
    report.fatalError ??= error.message;
  } finally {
    clearTimeout(deadline);
    if (browser) await browser.close().catch(() => {});
    const checked = new Set(report.results.map(result => result.slug + ":" + result.viewport));
    for (const target of scope.pages) for (const viewport of viewports) {
      if (!checked.has(target.slug + ":" + viewport.name)) report.results.push({
        slug: target.slug, kind: target.kind, viewport: viewport.name, width: viewport.width, height: viewport.height,
        url: target.url, status: "not_run", failures: ["Run stopped before this viewport."], screenshots: [],
      });
    }
    report.finishedAt = new Date().toISOString();
    report.summary = {
      passed: report.results.filter(result => result.status === "passed").length,
      failed: report.results.filter(result => result.status === "failed").length,
      notRun: report.results.filter(result => result.status === "not_run").length,
    };
    report.status = report.fatalError || report.summary.failed || report.summary.notRun ? "failed" : "passed";
    await save();
  }
  console.log(JSON.stringify({ report: relative(reportPath), status: report.status, ...report.summary }));
  if (report.status !== "passed") process.exitCode = 1;
}

async function inspect(page, target, viewport, result) {
  const article = page.locator(target.selector);
  result.documentTitle = (await page.title()).trim();
  result.headings = (await article.locator("h1").allTextContents()).map(text => text.trim());
  result.bodyCharacters = await article.evaluate(node => {
    const copy = node.cloneNode(true);
    copy.querySelectorAll("header, h1, script, style").forEach(element => element.remove());
    return (copy.textContent ?? "").replace(/\s/g, "").length;
  });
  if (!result.documentTitle || !result.headings.length || result.headings.some(title => !title)) result.failures.push("Empty document title or article heading.");
  if (!result.bodyCharacters) result.failures.push("Article content is empty.");
  // ContentBlocks and the guide hero render figure images; ad/partner UI is outside this scope.
  const images = article.locator("figure img");
  const imageCount = await images.count();
  if (imageCount > limits.imagesPerPage) throw new Error("Image count exceeds bounded inspection scope.");
  for (let index = 0; index < imageCount; index++) {
    const image = images.nth(index);
    await image.scrollIntoViewIfNeeded();
    await image.evaluate(img => new Promise(resolve => {
      if (img.complete) return resolve();
      const finish = () => { clearTimeout(timeout); img.removeEventListener("load", finish); img.removeEventListener("error", finish); resolve(); };
      const timeout = setTimeout(finish, 10_000);
      img.addEventListener("load", finish, { once: true });
      img.addEventListener("error", finish, { once: true });
    }));
  }
  result.images = await images.evaluateAll(nodes => nodes.map(img => ({
    path: new URL(img.currentSrc || img.src, location.href).pathname,
    loaded: img.complete && img.naturalWidth > 0 && img.getBoundingClientRect().width > 0,
    naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight,
  })));
  if (result.images.some(image => !image.loaded)) result.failures.push("Article image did not load.");
  for (const expected of target.expectedImagePaths) {
    if (!result.images.some(image => image.path === expected && image.loaded)) result.failures.push("Missing expected article image: " + expected);
  }
  if (await article.locator("table").count() > limits.tablesPerPage) throw new Error("Table count exceeds bounded inspection scope.");
  result.layout = await article.evaluate(node => {
    const width = () => Math.max(document.documentElement.scrollWidth, document.body?.scrollWidth ?? 0);
    const tables = [...node.querySelectorAll("table")].map(table => {
      const wrapper = table.parentElement;
      const container = wrapper.parentElement;
      const before = wrapper.scrollLeft;
      const windowX = scrollX;
      const wrapperRect = wrapper.getBoundingClientRect();
      const parentRect = container.getBoundingClientRect();
      const tableWidth = table.getBoundingClientRect().width;
      const columns = [...(table.tHead?.rows[0]?.cells ?? table.rows[0]?.cells ?? [])].map(cell => ({
        label: cell.textContent.trim(), width: cell.getBoundingClientRect().width / cell.colSpan,
      }));
      const overflowX = getComputedStyle(wrapper).overflowX;
      const requiresScroll = wrapper.scrollWidth > wrapper.clientWidth + 1;
      wrapper.scrollLeft = 0;
      wrapper.scrollLeft = wrapper.scrollWidth;
      const scrolledTo = wrapper.scrollLeft;
      const pageWidthDuringScroll = width();
      const pageStayedFixed = scrollX === windowX;
      wrapper.scrollLeft = before;
      return {
        columns, tableWidth, wrapperWidth: wrapperRect.width,
        clientWidth: wrapper.clientWidth, scrollWidth: wrapper.scrollWidth, overflowX,
        wrapperInsideContainer: wrapperRect.left >= parentRect.left - 1 && wrapperRect.right <= parentRect.right + 1,
        requiresScroll, scrolledTo, pageStayedFixed, pageWidthDuringScroll,
        internalScrollWorks: !requiresScroll || (["auto", "scroll"].includes(overflowX) && scrolledTo > 0 && pageStayedFixed),
        fitsContainer: tableWidth <= wrapper.clientWidth + 1 && wrapper.scrollWidth <= wrapper.clientWidth + 1,
      };
    });
    return { innerWidth, pageScrollWidth: width(), tables };
  });
  const { layout } = result;
  if (layout.pageScrollWidth > layout.innerWidth) result.failures.push("Whole-page horizontal overflow.");
  if (target.expectedColumns && layout.tables.length !== target.expectedColumns.length) result.failures.push("Table count differs from the local article.");
  for (const [index, table] of layout.tables.entries()) {
    const prefix = "Table " + (index + 1) + ": ";
    if (!table.columns.length || table.columns.some(column => column.width + 0.01 < 112)) result.failures.push(prefix + "a column is narrower than 112px.");
    if (target.expectedColumns && table.columns.length !== target.expectedColumns[index]) result.failures.push(prefix + "column count differs from the local article.");
    if (!table.wrapperInsideContainer) result.failures.push(prefix + "scroll wrapper extends outside its container.");
    if (!table.internalScrollWorks || !table.pageStayedFixed || table.pageWidthDuringScroll > layout.innerWidth) result.failures.push(prefix + "internal scrolling fails or causes page overflow.");
    if (viewport.name === "mobile" && table.columns.length * 112 > table.clientWidth + 1 && !table.requiresScroll) result.failures.push(prefix + "wide mobile table is not internally scrollable.");
    if (viewport.name === "desktop" && !table.fitsContainer) result.failures.push(prefix + "desktop table does not fit its container.");
  }
}

async function capture(page, target, viewport, result, directory) {
  async function screenshot(suffix) {
    const file = path.join(directory, target.slug + "-" + viewport.name + "-" + suffix + ".png");
    const bytes = await page.screenshot({ path: file, animations: "disabled", timeout: 45_000 });
    result.screenshots.push({ path: relative(file), sha256: sha256(bytes) });
  }
  await page.evaluate(() => scrollTo(0, 0));
  await screenshot("top");
  const tables = page.locator(target.selector + " table");
  for (let index = 0; index < await tables.count(); index++) {
    const table = tables.nth(index);
    await table.scrollIntoViewIfNeeded();
    await table.evaluate(node => { node.parentElement.scrollLeft = 0; });
    await screenshot("table-" + (index + 1) + "-left");
    if (viewport.name === "mobile" && result.layout.tables[index].requiresScroll) {
      await table.evaluate(node => { node.parentElement.scrollLeft = node.parentElement.scrollWidth; });
      await screenshot("table-" + (index + 1) + "-right");
      await table.evaluate(node => { node.parentElement.scrollLeft = 0; });
    }
  }
}
