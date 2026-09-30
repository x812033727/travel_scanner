import { expect, test } from "@playwright/test";

// Crawlers read alternates from both the HTTP `Link` header and the page's <head>. The locale
// middleware used to emit a header naming all five locales with an unprefixed x-default on every
// page, while article metadata names only published languages with x-default on English (unit
// tests in the article pages' page.test.tsx cover that). Only the page's own set may exist.
test.use({ javaScriptEnabled: false, userAgent: "Twitterbot/1.0" });

const routes = [
  "/zh-TW",
  "/en/guides/howto/synthetic-airport-transfer",
  "/ja/guides/intel/synthetic-fare-notice",
  "/zh-TW/life/synthetic-ai-notes",
];

for (const path of routes) {
  test(`${path}: the response carries no hreflang Link header`, async ({ request }) => {
    const response = await request.get(path, { maxRedirects: 0 });
    expect(response.status()).toBe(200);
    expect(response.headers()["link"] ?? "").not.toMatch(/hreflang/i);
  });
}

test("a fully localized static page keeps its complete reciprocal set with x-default on English", async ({ page }) => {
  const response = await page.goto("/zh-TW");
  expect(response?.status()).toBe(200);
  const languages = await page.locator('head link[rel="alternate"][hreflang]').evaluateAll((links) =>
    links.map((link) => link.getAttribute("hreflang") ?? "").sort(),
  );
  expect(languages).toEqual(["en", "ja", "ko", "x-default", "zh-CN", "zh-TW"]);
  const xDefault = await page.locator('head link[rel="alternate"][hreflang="x-default"]').getAttribute("href");
  expect(new URL(xDefault ?? "").pathname).toBe("/en");
});
