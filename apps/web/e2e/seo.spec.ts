import { expect, test } from "@playwright/test";

// Real production Next output, not mocked metadata objects or hydration-only assertions.
// The existing isolated API supplies synthetic site documents and public feature flags.
// Next chooses blocking versus streamed metadata from User-Agent, not JS capability.
// Exercise its supported HTML-only crawler path at both configured viewport sizes.
test.use({ javaScriptEnabled: false, userAgent: "Twitterbot/1.0" });
const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;

for (const locale of locales) {
  test(`${locale}: marketing content and destination links exist without JavaScript`, async ({ page }) => {
    const response = await page.goto(`/${locale}`);
    expect(response?.status()).toBe(200);
    await expect(page.locator("main h1")).toHaveCount(1);
    await expect(page.locator(`main a[href="/${locale}/destinations/tokyo"]`)).toBeVisible();
    const graphs = await page.locator('script[type="application/ld+json"]').allTextContents();
    expect(graphs.flatMap((value) => JSON.parse(value)).map((graph) => graph["@type"]))
      .toEqual(expect.arrayContaining(["Organization", "WebSite"]));
  });

  test(`${locale}: filtered public URLs have page-specific canonical, alternates and social copy`, async ({ page }) => {
    const response = await page.goto(`/${locale}/foods?destination_id=tokyo&q=sushi`);
    expect(response?.status()).toBe(200);
    const canonical = await page.locator('head link[rel="canonical"]').getAttribute("href");
    expect(new URL(canonical!).pathname).toBe(`/${locale}/foods`);
    expect(new URL(canonical!).search).toBe("");
    for (const language of locales) {
      const url = await page.locator(`head link[rel="alternate"][hreflang="${language}"]`).getAttribute("href");
      expect(new URL(url!).pathname).toBe(`/${language}/foods`);
    }
    const fallback = await page.locator('head link[rel="alternate"][hreflang="x-default"]').getAttribute("href");
    expect(new URL(fallback!).pathname).toBe("/en/foods");
    await expect(page.locator('head meta[property="og:title"]')).toHaveAttribute("content", await page.title());
    await expect(page.locator('head meta[name="twitter:title"]')).toHaveAttribute("content", await page.title());
    const description = await page.locator('head meta[name="description"]').getAttribute("content");
    expect(description).toBeTruthy();
    await expect(page.locator('head meta[property="og:description"]')).toHaveAttribute("content", description!);
  });

  test(`${locale}: an article hub is indexable only where the section has something published`, async ({ page }) => {
    // The fixture publishes intel in zh-TW and ja, how-to in en and lifestyle in zh-TW, the
    // way the live site publishes one language at a time. A hub with nothing in it still
    // answers 200 with its header and its language switcher, so it stays `follow`: the point
    // is to keep an empty page out of the index, not to cut the crawler off from the rest.
    const published: Record<string, string[]> = {
      "/guides": ["zh-TW", "ja", "en"], "/guides/intel": ["zh-TW", "ja"],
      "/guides/howto": ["en"], "/life": ["zh-TW"],
    };
    for (const [path, locales_] of Object.entries(published)) {
      const response = await page.goto(`/${locale}${path}`);
      expect(response?.status()).toBe(200);
      const robots = page.locator('head meta[name="robots"]');
      if (locales_.includes(locale)) {
        await expect(robots).toHaveCount(0);
      } else {
        await expect(robots).toHaveAttribute("content", /noindex/);
        await expect(robots).toHaveAttribute("content", /(?<!no)follow/);
      }
    }
  });

  test(`${locale}: independently published CMS content does not inherit unverified translations`, async ({ page }) => {
    await page.goto(`/${locale}/privacy`);
    await expect(page.getByRole("heading", { name: `Synthetic privacy (${locale})` })).toBeVisible();
    await expect(page.locator('head link[rel="alternate"][hreflang]')).toHaveCount(0);
    const canonical = await page.locator('head link[rel="canonical"]').getAttribute("href");
    expect(new URL(canonical!).pathname).toBe(`/${locale}/privacy`);
    await page.goto(`/${locale}/terms`);
    await expect(page.locator('head meta[name="robots"]')).toHaveAttribute("content", /noindex/);
    await expect(page.locator('head link[rel="alternate"][hreflang]')).toHaveCount(0);
    await page.goto(`/${locale}/login`);
    await expect(page.locator('head meta[name="robots"]')).toHaveAttribute("content", /noindex/);
  });
}

test("runtime sitemap exposes only public routes and stable localized alternate URLs", async ({ request }) => {
  const response = await request.get("/sitemap.xml");
  expect(response.status()).toBe(200);
  // Next's metadata route handler may retain its explicit max-age=0/must-revalidate
  // header even for force-dynamic routes. Both forms require a fresh response.
  const cacheControl = response.headers()["cache-control"];
  expect(cacheControl).toMatch(/no-store|no-cache|max-age=0/);
  if (!/no-store|no-cache/.test(cacheControl)) expect(cacheControl).toContain("must-revalidate");
  expect(cacheControl).not.toMatch(/(?:s-maxage|max-age)=[1-9]\d*/);
  const xml = await response.text();
  // Seven unconditional base routes, 33 destination guides and 33 services pages, times five
  // locales, with the fixture's public switches all enabled; plus the four article hubs, which
  // are listed per language rather than per route -- /guides wherever either travel kind
  // publishes (zh-TW, ja, en), /guides/intel in zh-TW and ja, /guides/howto in en and /life in
  // zh-TW, which is seven of their twenty possible URLs; plus the four synthetic article
  // translations the fixture API publishes (three travel, one lifestyle).
  expect(xml.match(/<url>/g)).toHaveLength(5 * (7 + 33 + 33) + 7 + 4);
  for (const path of ["/guides", "/guides/intel", "/guides/howto", "/life"]) {
    expect(xml).toContain(`/zh-TW${path}</loc>`);
    // Nothing is published in Korean, so every hub of it is an empty page: not listed here,
    // and `noindex` on the page itself.
    expect(xml).not.toContain(`/ko${path}</loc>`);
  }
  expect(xml).toContain("/en/guides</loc>");
  expect(xml).not.toContain("/en/guides/intel</loc>");
  expect(xml).toContain("/en/destinations/tokyo</loc>");
  expect(xml).toContain('hreflang="x-default"');
  expect(xml).not.toMatch(/<loc>[^<]*\/(?:admin|account|trips|login|privacy)(?:\/|<)/);
  // Articles are the only entries with a date, and each names only its own published
  // translations. This is the one place either is rendered into the XML Next actually emits:
  // no static entry carries a lastmod, and every static entry carries all five locales.
  expect(xml.match(/<lastmod>/g)).toHaveLength(4);
  const notice = sitemapUrl(xml, "/zh-TW/guides/intel/synthetic-fare-notice");
  expect(notice).toContain("<lastmod>2026-09-08T09:30:00.000Z</lastmod>");
  expect(hreflangs(notice)).toEqual(["ja", "zh-TW"]); // never written in English, so no x-default
  expect(hreflangs(sitemapUrl(xml, "/en/guides/howto/synthetic-airport-transfer"))).toEqual(["en", "x-default"]);
  // A lifestyle article lives under /life/, never /guides/life/, and names only its own locale.
  expect(hreflangs(sitemapUrl(xml, "/zh-TW/life/synthetic-ai-notes"))).toEqual(["zh-TW"]);
  expect(xml).not.toContain("/guides/life/");
  expect(xml).not.toContain("/ko/guides/intel/synthetic-fare-notice</loc>");
  const robots = await request.get("/robots.txt");
  expect(robots.status()).toBe(200);
  expect(await robots.text()).toMatch(/Sitemap: https?:\/\/[^\s]+\/sitemap.xml/);
});

/** The `<url>` block whose `<loc>` ends with this path. */
function sitemapUrl(xml: string, path: string): string {
  const block = xml.split("<url>").find((part) => part.includes(`${path}</loc>`));
  expect(block, `${path} is not in the sitemap`).toBeDefined();
  return block ?? "";
}

function hreflangs(block: string): string[] {
  return [...block.matchAll(/hreflang="([^"]+)"/g)].map((match) => match[1]).sort();
}
