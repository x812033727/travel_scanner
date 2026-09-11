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
  // 380 static URLs with every public switch open in the fixture, plus the three synthetic guide
  // translations tools/e2e-runtime-api.mjs publishes.
  expect(xml.match(/<url>/g)).toHaveLength(383);
  expect(xml).toContain("/en/destinations/tokyo</loc>");
  expect(xml).toContain("/ko/guides/howto</loc>");
  expect(xml).toContain('hreflang="x-default"');
  expect(xml).not.toMatch(/<loc>[^<]*\/(?:admin|account|trips|login|privacy)(?:\/|<)/);
  // Only guide articles have a real date, and each lists only its own published translations.
  expect(xml.match(/<lastmod>/g)).toHaveLength(3);
  const notice = sitemapUrl(xml, "/zh-TW/guides/intel/synthetic-fare-notice");
  expect(notice).toContain("<lastmod>2026-09-08T09:30:00.000Z</lastmod>");
  expect(hreflangs(notice)).toEqual(["ja", "zh-TW"]); // never written in English, so no x-default
  expect(hreflangs(sitemapUrl(xml, "/en/guides/howto/synthetic-airport-transfer"))).toEqual(["en", "x-default"]);
  expect(xml).not.toContain("/en/guides/intel/synthetic-fare-notice</loc>");
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
