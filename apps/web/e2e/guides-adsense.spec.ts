import { expect, test as base, type Route } from "@playwright/test";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { defaultUsageCatalog } from "../lib/usage-catalog";
import { siteFeatureKeys } from "../lib/site-features";
import { ADSENSE_SCRIPT_ORIGIN } from "../lib/adsense";
import { ADS_TXT_FALLBACK_PUBLISHER_ID } from "../app/ads.txt/ads-txt";

/**
 * Advertising is decided on the server, cached per process, and gated on the production
 * origin — so it cannot be toggled through the shared e2e fixture without leaking into every
 * other spec. This file spawns its own Next server and its own API double, the way
 * `stay22-script.spec.ts` does, and drives it through the canonical host.
 */
const canonical = "https://mokaair.com";
// Google's shape, and deliberately not the account `/ads.txt` falls back to: the ads.txt case
// below can then only pass when the file is built from what this double answers.
const PUBLISHER = "ca-pub-1234567890123456";
const SLOT = "1234567890";
const articlePath = "/zh-TW/guides/howto/tokyo-esim";
const hubPath = "/zh-TW/guides/howto";
const AD_LABEL = "廣告";

const paragraph = (text: string) => ({ type: "paragraph", text });
const article = {
  slug: "tokyo-esim", kind: "howto", locale: "zh-TW", status: "published",
  destination_id: null, destination_label: null, topics: [], valid_until: null, expired: false,
  published_locales: ["zh-TW"],
  document: {
    title: "東京 eSIM 怎麼選", description: "三家方案比較", version: 1,
    published_at: "2026-09-10T00:00:00Z", modified_at: null, hero: null, sources: [],
    blocks: [
      { type: "heading", text: "先看流量", level: 2 }, paragraph("先決定一天要用多少。"),
      ...Array.from({ length: 8 }, (_, index) => paragraph(`第 ${index + 1} 段內文。`)),
    ],
  },
};

const longPath = "/zh-TW/guides/howto/tokyo-long";
const longArticle = {
  ...article,
  slug: "tokyo-long",
  document: {
    ...article.document,
    title: "東京長篇攻略",
    blocks: Array.from({ length: 4 }, (_, section) => [
      { type: "heading", text: `第 ${section + 1} 節`, level: 2 },
      // Several lines each, so the later units start well below the lazy-loading margin.
      ...Array.from({ length: 10 }, (_, index) => paragraph(`第 ${section + 1} 節第 ${index + 1} 段內文。`.repeat(12))),
    ]).flat(),
  },
};

// An article that links to another, so a reader can move on without leaving the document.
const linkedPath = "/zh-TW/guides/howto/tokyo-linked";
const linkedArticle = {
  ...article,
  slug: "tokyo-linked",
  document: { ...article.document, title: "東京 eSIM 延伸閱讀" },
  related: [{ kind: "howto", slug: "tokyo-long", title: longArticle.document.title }],
};
// What a video description links to: tools/video/core/metadata.mjs `articleUrl`.
const campaign = "?utm_source=youtube&utm_medium=video&utm_campaign=tokyo-linked";

const faqPath = "/zh-TW/guides/howto/tokyo-faq";
const faqArticle = {
  ...article,
  slug: "tokyo-faq",
  document: {
    ...article.document,
    title: "東京常見問題閱讀順序測試",
    blocks: [
      { type: "heading", text: "選擇交通", level: 2 }, paragraph("先核對機場與入住區域。"),
      { type: "heading", text: "出發前的問答", level: 2 },
      { type: "faq", items: [
        { question: "機場到住宿怎麼確認？", answer: "先查官方交通路線，再核對住宿附近的車站出口。" },
        { question: "需要先確定車站出口嗎？", answer: "核對住宿地址與適合拖行李的出口。" },
      ] },
      { type: "heading", text: "抵達以後", level: 2 }, paragraph("留意末班車與行李。"),
      { type: "faq", items: [
        { question: "行李可以提前寄放嗎？", answer: "直接向住宿業者確認可寄放的時段與條件。" },
        { question: "晚到需要通知住宿嗎？", answer: "確認可入住的時間與晚到聯絡方式。" },
      ] },
    ],
  },
  related: [{ kind: "howto", slug: "tokyo-long", title: longArticle.document.title }],
};

const newsTopics = [
  { slug: "ai-news", label: "AI 新聞", section: "life", count: 2 },
  { slug: "tech-news", label: "科技新聞", section: "life", count: 3 },
];
const newsHero = {
  src: "/guides/adobe-podcast-audio/hero.jpg", alt: "音訊工具示意圖", width: 1600, height: 900, credit: null,
};
const newsStories = [
  { slug: "fixture-news-lead", title: "AI 工具的新功能，先看使用條件", news_date: "2026-11-08", topics: newsTopics, hero: newsHero },
  { slug: "fixture-news-audio", title: "錄音工具更新：如何確認處理結果", news_date: "2026-11-07", topics: [newsTopics[0]], hero: newsHero },
  { slug: "fixture-news-no-image", title: "沒有圖片的科技新聞仍然可以閱讀", news_date: "2026-11-06", topics: [newsTopics[1]], hero: null },
  { slug: "fixture-news-older", title: "上一頁新聞之後的較早報導", news_date: "2026-11-05", topics: [newsTopics[1]], hero: null },
].map((story) => ({
  ...story, kind: "life", destination_id: null, destination_label: null,
  description: `${story.title}，以官方說明核對適用範圍與限制。`,
  published_at: "2026-11-10T05:00:00Z", valid_until: null, featured: false,
}));
const newsArticle = (slug: string) => {
  const story = newsStories.find((entry) => entry.slug === slug)!;
  return {
    ...article, ...story, locale: "zh-TW", published_locales: ["zh-TW"],
    document: {
      ...article.document, title: story.title, description: story.description, hero: story.hero,
      blocks: [
        { type: "summary", items: ["先核對適用範圍。", "保留原始檔案以便比較。"] },
        ...["這次更新的內容", "使用前先確認", "接下來可以怎麼做"].flatMap((heading, section) => [
          { type: "heading", level: 2, text: heading },
          ...(section === 1 ? [paragraph(`Reference: https://example.test/${"long-reference-segment".repeat(12)}`)] : []),
          ...Array.from({ length: 5 }, (_, index) => paragraph(`第 ${section + 1} 節第 ${index + 1} 段：先閱讀官方說明，再以自己的工作流程確認差異。`.repeat(5))),
        ]),
      ],
    },
    related: [{ kind: "life", slug: newsStories[2].slug, title: newsStories[2].title }],
  };
};

type Fixture = { origin: string; enabled: boolean; cmp: boolean; adRequests: string[] };

/**
 * Forward a canonical-host request to the isolated server.
 *
 * Router prefetches for other routes keep arriving while a test finishes, and a reset or a
 * closed context must not be reported as a failure of what the test was actually checking.
 */
async function proxyToSite(route: Route, origin: string) {
  const url = new URL(route.request().url());
  const headers = {
    ...await route.request().allHeaders(),
    host: url.host, "x-forwarded-host": url.host, "x-forwarded-proto": url.protocol.slice(0, -1),
  };
  try {
    const response = await route.fetch({ url: `${origin}${url.pathname}${url.search}`, headers, maxRedirects: 0 });
    return await route.fulfill({ response });
  } catch {
    return route.abort().catch(() => undefined);
  }
}

const test = base.extend<{ site: Fixture }>({
  site: async ({ context, request }, runTest) => {
    test.skip(!existsSync(new URL("../.next/BUILD_ID", import.meta.url)), "Run next build for isolated AdSense coverage");
    const site: Fixture = { origin: "", enabled: true, cmp: false, adRequests: [] };
    const upstream = createServer((incoming, outgoing) => {
      incoming.resume();
      const url = new URL(incoming.url || "/", "http://127.0.0.1");
      let result: unknown = {};
      if (url.pathname === "/api/v1/ads/config") {
        // The server double applies the same privacy rule the real endpoint does.
        const tracking = incoming.headers.dnt !== "1" && incoming.headers["sec-gpc"] !== "1";
        result = site.enabled && tracking
          ? { enabled: true, publisher_id: PUBLISHER, slot_id: SLOT, cmp_enabled: site.cmp }
          : { enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false };
      } else if (url.pathname === "/api/v1/guides/howto/tokyo-esim") result = article;
      else if (url.pathname === "/api/v1/guides/howto/tokyo-long") result = longArticle;
      else if (url.pathname === "/api/v1/guides/howto/tokyo-linked") result = linkedArticle;
      else if (url.pathname === "/api/v1/guides/howto/tokyo-faq") result = faqArticle;
      else if (url.pathname.startsWith("/api/v1/guides/life/fixture-news-")) result = newsArticle(url.pathname.split("/").at(-1)!);
      else if (url.pathname.startsWith("/api/v1/guides/topics")) result = { topics: url.searchParams.get("section") === "life" ? newsTopics : [] };
      else if (url.pathname === "/api/v1/guides" && (url.searchParams.get("kind") === "life" || url.searchParams.get("section") === "life")) {
        const topic = url.searchParams.get("topic");
        // A separate curated result keeps the news lead from also appearing in the all-article grid.
        const rows = url.searchParams.has("cursor") ? newsStories.slice(3)
          : topic ? newsStories.slice(0, 3).filter((story) => story.topics.some((entry) => entry.slug === topic)) : [];
        result = { articles: rows, next_cursor: topic === "tech-news" && !url.searchParams.has("cursor") ? "older+fixture" : null };
      }
      else if (url.pathname.startsWith("/api/v1/guides")) result = { articles: [], total: 0 };
      else if (url.pathname === "/api/v1/runtime/site-visibility") result = Object.fromEntries(siteFeatureKeys.map((key) => [`${key}_enabled`, true]));
      else if (url.pathname === "/api/v1/usage-catalog") result = defaultUsageCatalog;
      else if (url.pathname === "/api/v1/analytics/config") result = { first_party_enabled: false, ga4_enabled: false };
      else if (url.pathname === "/api/v1/community/status") result = { enabled: false };
      else if (url.pathname === "/api/v1/discovery/status") result = { enabled: false };
      else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) result = { locale: "zh-TW", version: "fixture", entries: {} };
      else if (url.pathname === "/api/v1/auth/me") { outgoing.statusCode = 401; result = { detail: "anonymous" }; }
      outgoing.setHeader("Content-Type", "application/json");
      outgoing.setHeader("Cache-Control", "no-store");
      outgoing.end(JSON.stringify(result));
    });
    const probe = createServer();
    await new Promise<void>((resolve) => upstream.listen(0, "127.0.0.1", resolve));
    await new Promise<void>((resolve) => probe.listen(0, "127.0.0.1", resolve));
    const port = (probe.address() as { port: number }).port;
    await new Promise<void>((resolve) => probe.close(() => resolve()));
    site.origin = `http://127.0.0.1:${port}`;
    const server = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
      cwd: fileURLToPath(new URL("../", import.meta.url)),
      env: { ...process.env, NODE_ENV: "production", API_INTERNAL_URL: `http://127.0.0.1:${(upstream.address() as { port: number }).port}`, NEXT_TELEMETRY_DISABLED: "1" },
      stdio: ["ignore", "pipe", "pipe"], windowsHide: true,
    });
    try {
      await expect.poll(async () => {
        try { return (await request.get(`${site.origin}${hubPath}`, { timeout: 1_000, maxRedirects: 0 })).status(); }
        catch { return 0; }
      }, { timeout: 30_000 }).toBe(200);
      // Offline is an independent transport guard: nothing this page asks for may leave.
      await context.setOffline(true);
      await context.route("**/*", async (route) => {
        const url = new URL(route.request().url());
        if (url.origin === ADSENSE_SCRIPT_ORIGIN) {
          site.adRequests.push(url.href);
          return route.fulfill({ contentType: "application/javascript", body: "/* isolated inert AdSense fixture */" });
        }
        if (["mokaair.com", "www.mokaair.com"].includes(url.hostname) || url.origin === site.origin) {
          return proxyToSite(route, site.origin);
        }
        return route.abort().catch(() => undefined);
      });
      await runTest(site);
      await context.unrouteAll({ behavior: "ignoreErrors" });
    } finally {
      server.kill("SIGKILL");
      await new Promise<void>((resolve) => upstream.close(() => resolve()));
    }
  },
});

test("the news desk keeps event dates and one lead while opening real article links", async ({ page, site }, testInfo) => {
  site.enabled = false;
  await page.goto(`${canonical}/zh-TW/life`);
  const desk = page.getByTestId("news-desk");
  const list = desk.getByTestId("news-list");
  const lead = list.getByTestId("news-lead");
  await expect(lead.getByRole("link", { name: newsStories[0].title, exact: true })).toBeVisible();
  await expect(list.getByRole("link", { name: newsStories[0].title, exact: true })).toHaveCount(1);
  await expect(list.locator("time")).toHaveText(["2026-11-08", "2026-11-07", "2026-11-06"]);
  await expect(list).not.toContainText("2026-11-10");
  await expect(list).toContainText(newsStories[1].description);
  await expect(lead.locator("img")).toBeVisible();
  await expect.poll(() => lead.locator("img").evaluate((node) => (node as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
  await expect(lead.locator("img")).toHaveCSS("object-fit", "contain");
  const width = page.viewportSize()!.width;
  if (width < 768) {
    const headline = await lead.getByRole("heading").boundingBox();
    const artwork = await lead.locator("img").boundingBox();
    expect(headline!.y + headline!.height).toBeLessThanOrEqual(artwork!.y);
  }
  expect(await page.evaluate(() => window.innerWidth)).toBeLessThanOrEqual(width);
  expect(await list.evaluate((node) => node.getBoundingClientRect().right)).toBeLessThanOrEqual(width);
  const leadLink = lead.getByRole("link", { name: newsStories[0].title, exact: true });
  await leadLink.focus();
  await page.keyboard.press("Shift+Tab");
  await page.keyboard.press("Tab");
  await expect(leadLink).toBeFocused();
  const outline = await leadLink.evaluate((node) => {
    const style = getComputedStyle(node), box = node.getBoundingClientRect();
    const extent = parseFloat(style.outlineOffset) + parseFloat(style.outlineWidth);
    const clippedBy: string[] = [];
    for (let ancestor = node.parentElement; ancestor; ancestor = ancestor.parentElement) {
      const parentStyle = getComputedStyle(ancestor), bounds = ancestor.getBoundingClientRect();
      if ((["hidden", "clip"].includes(parentStyle.overflowX) && (box.left - extent < bounds.left || box.right + extent > bounds.right))
        || (["hidden", "clip"].includes(parentStyle.overflowY) && (box.top - extent < bounds.top || box.bottom + extent > bounds.bottom))) clippedBy.push(ancestor.tagName);
    }
    return { style: style.outlineStyle, clippedBy };
  });
  expect(outline.style).not.toBe("none");
  expect(outline.clippedBy).toEqual([]);
  await testInfo.attach("news-lead-keyboard-focus", { body: await page.screenshot(), contentType: "image/png" });
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(`${canonical}/zh-TW/life/${newsStories[0].slug}`);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(newsStories[0].title);
});

test("news category navigation and its cursor keep text-only articles reachable", async ({ page, site }) => {
  site.enabled = false;
  await page.goto(`${canonical}/zh-TW/life`);
  await page.getByTestId("news-desk").locator('a[href="/zh-TW/life/topics/tech-news"]').first().click();
  await expect(page).toHaveURL(`${canonical}/zh-TW/life/topics/tech-news`);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("科技新聞");
  const list = page.getByTestId("news-list");
  await expect(list.getByRole("link", { name: newsStories[2].title, exact: true })).toBeVisible();
  await expect(list.getByRole("link", { name: newsStories[1].title, exact: true })).toHaveCount(0);
  await page.locator('main a[href$="?cursor=older%2Bfixture"]').click();
  await expect(page).toHaveURL(`${canonical}/zh-TW/life/topics/tech-news?cursor=older%2Bfixture`);
  await expect(page.getByTestId("news-lead")).toHaveCount(0);
  await expect(page.getByTestId("news-list").getByRole("link", { name: newsStories[3].title, exact: true })).toBeVisible();
  await expect(page.getByTestId("news-list").locator("time")).toHaveText(["2026-11-05"]);
  await page.goBack();
  await page.getByTestId("news-list").getByRole("link", { name: newsStories[2].title, exact: true }).click();
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(newsStories[2].title);
  await expect(page.locator("article > figure")).toHaveCount(0);
});

test("life article contents remain usable after reader scrolling on desktop and narrow mobile", async ({ page, site }) => {
  site.enabled = false;
  await page.goto(`${canonical}/zh-TW/life/${newsStories[0].slug}`);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(newsStories[0].title);
  await expect(page.locator("#article-summary")).toContainText("保留原始檔案以便比較。");
  const desktop = page.getByTestId("article-contents-desktop");
  const mobile = page.getByTestId("article-contents-mobile");
  if (page.viewportSize()!.width >= 1024) {
    await expect(desktop).toBeVisible();
    await expect(mobile).toBeHidden();
    // Scroll where a reader does, then use the sticky contents without scrolling back up.
    await page.mouse.move(300, 450);
    await page.mouse.wheel(0, 1000);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(500);
    const contentsBox = await desktop.locator("nav").boundingBox();
    expect(contentsBox!.y).toBeGreaterThanOrEqual(0);
    expect(contentsBox!.y).toBeLessThan(page.viewportSize()!.height / 2);
    await desktop.locator('a[href="#section-3"]').click();
  } else {
    await expect(desktop).toBeHidden();
    await mobile.locator("summary").click();
    await mobile.locator('a[href="#section-3"]').click();
  }
  await expect(page).toHaveURL(/#section-3$/);
  const target = page.locator("h2#section-3");
  await expect(target).toBeInViewport();
  expect(await target.evaluate((node) => {
    const box = node.getBoundingClientRect();
    return node.contains(document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2));
  })).toBe(true);

  await page.setViewportSize({ width: 320, height: 740 });
  await page.evaluate(() => { document.documentElement.dataset.textSize = "largest"; });
  await expect(desktop).toBeHidden();
  await mobile.locator("summary").scrollIntoViewIfNeeded();
  if (!(await mobile.evaluate((node) => (node as HTMLDetailsElement).open))) await mobile.locator("summary").click();
  await mobile.locator('a[href="#section-2"]').click();
  await expect(page).toHaveURL(/#section-2$/);
  await expect(page.locator("h2#section-2")).toBeInViewport();
  expect(await page.evaluate(() => window.innerWidth)).toBeLessThanOrEqual(320);
  const body = await page.locator("article").boundingBox();
  expect(body!.x).toBeGreaterThanOrEqual(0);
  expect(body!.x + body!.width).toBeLessThanOrEqual(320);
  // The article box can fit while its text escapes. Measure rendered text fragments,
  // including an unbroken reference URL, and the actual contents controls separately.
  for (const locator of [page.locator("h2#section-2"), page.locator("h2#section-2 + p"), mobile.locator("summary"), mobile.locator('a[href="#section-2"]')]) {
    const edges = await locator.evaluate((node) => {
      const range = document.createRange();
      range.selectNodeContents(node);
      return Array.from(range.getClientRects(), rect => ({ left: rect.left, right: rect.right }));
    });
    expect(edges.length).toBeGreaterThan(0);
    for (const edge of edges) {
      expect(edge.left).toBeGreaterThanOrEqual(0);
      expect(edge.right).toBeLessThanOrEqual(320);
    }
  }
});

test("FAQ contents links reach the authored questions before related reading", async ({ page, site }) => {
  site.enabled = false;
  await page.goto(`${canonical}${faqPath}`);
  const authored = page.locator("h2#section-2");
  await expect(authored).toHaveText("出發前的問答");
  await expect(page.locator("h2", { hasText: "出發前的問答" })).toHaveCount(1);
  const faqLink = page.locator('a[href="#section-2"]');
  await faqLink.click();
  await expect(page).toHaveURL(/#section-2$/);
  expect(await authored.evaluate((node) => node.nextElementSibling?.id)).toBe("article-faq");
  const firstFaq = page.locator("#article-faq");
  await firstFaq.getByText("機場到住宿怎麼確認？", { exact: true }).click();
  await expect(firstFaq.getByText("先查官方交通路線，再核對住宿附近的車站出口。", { exact: true })).toBeVisible();
  const secondFaq = page.locator("#article-faq-2");
  await secondFaq.getByText("行李可以提前寄放嗎？", { exact: true }).click();
  await expect(secondFaq.getByText("直接向住宿業者確認可寄放的時段與條件。", { exact: true })).toBeVisible();
  const related = page.getByRole("link", { name: longArticle.document.title, exact: true });
  expect(await related.evaluate((node) => {
    const faq = document.getElementById("article-faq-2");
    return Boolean(faq && (faq.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING));
  })).toBe(true);
  expect(await page.locator("main").evaluate((node) => node.scrollWidth <= window.innerWidth)).toBe(true);
});

test("a short article carries one labelled slot with its box already reserved", async ({ page, site }) => {
  await page.goto(`${canonical}${articlePath}`);
  const slot = page.locator("ins.adsbygoogle");
  await expect(slot).toHaveCount(1);
  await expect(page.getByText(AD_LABEL, { exact: true })).toBeVisible();
  await expect(slot).toHaveAttribute("data-ad-client", PUBLISHER);
  await expect(slot).toHaveAttribute("data-ad-slot", SLOT);
  // Reserved before the ad arrives: an unreserved box is a layout shift on every page view.
  expect(await slot.evaluate((node) => node.getBoundingClientRect().height)).toBeGreaterThan(100);
  // Below the headline, never the first thing in the body.
  const heading = await page.locator("h1").boundingBox();
  expect((await slot.boundingBox())!.y).toBeGreaterThan(heading!.y);
  await expect.poll(() => site.adRequests.length, { timeout: 10_000 }).toBeGreaterThan(0);
  expect(site.adRequests.every((url) => url.includes(`client=${PUBLISHER}`))).toBe(true);
});

test("a long article carries more units, and only the first asks for an ad before the reader scrolls", async ({ page, site }) => {
  await page.goto(`${canonical}${longPath}`);
  const slots = page.locator("ins.adsbygoogle");
  await expect(slots).toHaveCount(3);
  await expect(page.getByText(AD_LABEL, { exact: true })).toHaveCount(3);
  expect(await slots.evaluateAll((nodes) => nodes.map((node) => node.getAttribute("data-ad-slot"))))
    .toEqual([SLOT, SLOT, SLOT]);
  // The inert fixture never drains the queue, so its length is the number of requests made.
  await expect.poll(() => page.evaluate(() => window.adsbygoogle?.length)).toBe(1);
  // Scrolled to the way a reader gets there: each unit asks as it comes near.
  await slots.nth(1).scrollIntoViewIfNeeded();
  await expect.poll(() => page.evaluate(() => window.adsbygoogle?.length)).toBe(2);
  await slots.nth(2).scrollIntoViewIfNeeded();
  await expect.poll(() => page.evaluate(() => window.adsbygoogle?.length)).toBe(3);
  expect(site.adRequests.every((url) => url.includes(`client=${PUBLISHER}`))).toBe(true);
  // A unit Google leaves unfilled folds away, label and reserved box included.
  const labels = page.getByText(AD_LABEL, { exact: true });
  await slots.nth(2).evaluate((node) => node.setAttribute("data-ad-status", "unfilled"));
  await expect(labels.nth(2)).toBeHidden();
  await expect(labels.nth(1)).toBeVisible();
});

test("an anchor ad pushes the mobile navigation up instead of covering it", async ({ browser, site }) => {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await context.newPage();
  await page.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin === ADSENSE_SCRIPT_ORIGIN) {
      return route.fulfill({ contentType: "application/javascript", body: "/* isolated inert AdSense fixture */" });
    }
    if (["mokaair.com", "www.mokaair.com"].includes(url.hostname) || url.origin === site.origin) {
      return proxyToSite(route, site.origin);
    }
    return route.abort().catch(() => undefined);
  });
  await page.goto(`${canonical}${articlePath}`);
  const nav = page.locator(".app-bottom-nav");
  await expect(nav).toBeVisible();
  const before = (await nav.boundingBox())!;
  // What the tag inserts for an anchor: a fixed unit on the bottom edge, above everything.
  await page.evaluate(() => {
    const anchor = document.createElement("ins");
    anchor.className = "adsbygoogle adsbygoogle-noablate";
    anchor.setAttribute("style", "display:block; position:fixed; left:0; right:0; bottom:0; height:90px; z-index:2147483647;");
    document.body.append(anchor);
  });
  await expect.poll(async () => (await nav.boundingBox())!.y).toBeLessThanOrEqual(before.y - 90);
  const after = (await nav.boundingBox())!;
  expect(after.y + after.height).toBeLessThanOrEqual(844 - 90);
  // Gone again, and the navigation returns to the edge.
  await page.evaluate(() => document.querySelector("ins.adsbygoogle-noablate")?.remove());
  await expect.poll(async () => (await nav.boundingBox())!.y).toBe(before.y);
  await page.unrouteAll({ behavior: "ignoreErrors" });
  await context.close();
});

test("without a consent message the tag is told to serve non-personalised ads", async ({ page, site }) => {
  await page.goto(`${canonical}${articlePath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(1);
  // Personalised ads in the EEA, the UK or Switzerland need a certified CMP; with none
  // published, this flag is the only thing keeping the page inside the policy.
  await expect.poll(() => page.evaluate(() => window.adsbygoogle?.requestNonPersonalizedAds))
    .toBe(1);
  expect(site.adRequests.every((url) => url.includes(`client=${PUBLISHER}`))).toBe(true);
});

test("a published consent message leaves personalisation to the reader's answer", async ({ page, site }) => {
  site.cmp = true;
  await page.goto(`${canonical}${articlePath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(1);
  // Forcing the flag here would override whatever the reader chose in Google's message.
  expect(await page.evaluate(() => window.adsbygoogle?.requestNonPersonalizedAds)).toBeUndefined();
});

test("a browser asking not to be tracked gets no slot and no request", async ({ browser, site }) => {
  const context = await browser.newContext({ extraHTTPHeaders: { "Sec-GPC": "1" } });
  const page = await context.newPage();
  await page.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin === ADSENSE_SCRIPT_ORIGIN) {
      site.adRequests.push(url.href);
      return route.abort().catch(() => undefined);
    }
    return proxyToSite(route, site.origin);
  });
  site.adRequests.length = 0;
  await page.goto(`${canonical}${articlePath}`);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  // Not even the reserved space: the page is exactly the page it is with advertising off.
  await expect(page.getByText(AD_LABEL, { exact: true })).toHaveCount(0);
  expect(site.adRequests).toEqual([]);
  await page.unrouteAll({ behavior: "ignoreErrors" });
  await context.close();
});

test("an article-shaped URL with no article behind it carries nothing", async ({ page, site }) => {
  site.adRequests.length = 0;
  // The fixture has no such slug, so this renders the "article unavailable" screen. The
  // layout decides whether to load the tag before the page gets to say that, so it has to
  // check the article really exists — advertising on a no-content screen is what the
  // programme policies forbid.
  await page.goto(`${canonical}/zh-TW/guides/howto/does-not-exist`);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  await expect(page.getByText(AD_LABEL, { exact: true })).toHaveCount(0);
  expect(site.adRequests).toEqual([]);
});

test("a hub is a listing, not an article, so it carries nothing", async ({ page, site }) => {
  site.adRequests.length = 0;
  await page.goto(`${canonical}${hubPath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  expect(site.adRequests).toEqual([]);
});

test("a campaign-tagged link keeps its tags, and the document it opens stays ad-free", async ({ page, site }) => {
  site.adRequests.length = 0;
  const response = await page.goto(`${canonical}${linkedPath}${campaign}`);
  // Answered where it was asked. It used to 307 to the bare path, and the tags never reached
  // analytics. The ad tag can read location.href, so this document does without it instead.
  expect(response?.status()).toBe(200);
  expect(response?.request().redirectedFrom()).toBeNull();
  expect(page.url()).toBe(`${canonical}${linkedPath}${campaign}`);
  expect(response?.headers()["content-security-policy-report-only"]).not.toContain("'unsafe-eval'");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(linkedArticle.document.title);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  await expect(page.getByText(AD_LABEL, { exact: true })).toHaveCount(0);

  // Moving on to another article keeps this document, and the root layout that decided
  // against the tag is not rendered again. The next article must not reserve boxes that
  // nothing in this document will ever fill.
  await page.evaluate(() => Object.assign(window, { sameDocument: true }));
  await page.getByRole("link", { name: longArticle.document.title }).click();
  await expect(page).toHaveURL(`${canonical}${longPath}`);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(longArticle.document.title);
  expect(await page.evaluate(() => "sameDocument" in window)).toBe(true);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(0);
  await expect(page.getByText(AD_LABEL, { exact: true })).toHaveCount(0);
  expect(site.adRequests).toEqual([]);
});

test("the same article opened without a query still carries its ad", async ({ page, site }) => {
  // The other half of the rule above: only the query takes the tag away.
  await page.goto(`${canonical}${linkedPath}`);
  await expect(page.locator("ins.adsbygoogle")).toHaveCount(1);
  await expect.poll(() => site.adRequests.length, { timeout: 10_000 }).toBeGreaterThan(0);
});

test("a capitalised slug is sent to its canonical address for good, tags and all", async ({ request, site }) => {
  const response = await request.get(`${site.origin}/zh-TW/guides/howto/Tokyo-Linked${campaign}`, {
    headers: { host: "mokaair.com", "x-forwarded-host": "mokaair.com", "x-forwarded-proto": "https" },
    maxRedirects: 0,
  });
  expect(response.status()).toBe(308);
  expect(new URL(response.headers().location, canonical).href).toBe(`${canonical}${linkedPath}${campaign}`);
});

test("only an article route relaxes the content security policy", async ({ request, site }) => {
  const article = await request.get(`${site.origin}${articlePath}`, { headers: { host: "mokaair.com", "x-forwarded-host": "mokaair.com", "x-forwarded-proto": "https" } });
  const hub = await request.get(`${site.origin}${hubPath}`, { headers: { host: "mokaair.com", "x-forwarded-host": "mokaair.com", "x-forwarded-proto": "https" } });
  expect(article.headers()["content-security-policy-report-only"]).toContain("'unsafe-eval'");
  expect(hub.headers()["content-security-policy-report-only"]).not.toContain("'unsafe-eval'");
  expect(hub.headers()["content-security-policy-report-only"]).toContain("frame-src https://www.google.com https://www.stay22.com https://www.youtube-nocookie.com;");
});

test("ads.txt names the configured publisher and is not sent through locale routing", async ({ request, site }) => {
  // The fixture's id is not the one the route falls back to, so this can only pass when the
  // file is built from what the API answered rather than from anything checked in.
  expect(PUBLISHER).not.toBe(ADS_TXT_FALLBACK_PUBLISHER_ID);
  const response = await request.get(`${site.origin}/ads.txt`, { maxRedirects: 0 });
  expect(response.status()).toBe(200);
  expect(response.headers()["content-type"]).toContain("text/plain");
  expect((await response.text()).trim()).toBe(`google.com, ${PUBLISHER.replace(/^ca-/, "")}, DIRECT, f08c47fec0942fa0`);
});
