import { expect, test, type Locator, type Page } from "@playwright/test";
import type { DiscoveryItem } from "../lib/discovery";
import type { FoodMerchant } from "../lib/foods";
import { getDiscoveryCopy } from "../lib/discovery-copy";
import { getFrontendFlowCopy } from "../lib/frontend-flow-copy";
import enFoods from "../messages/en/foods.json" with { type: "json" };
import jaFoods from "../messages/ja/foods.json" with { type: "json" };
import koFoods from "../messages/ko/foods.json" with { type: "json" };
import twFoods from "../messages/zh-TW/foods.json" with { type: "json" };
import cnFoods from "../messages/zh-CN/foods.json" with { type: "json" };

// Isolated synthetic UI data, not production moderation evidence. All map,
// restaurant and booking navigations (including popups) are intercepted locally.
const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
type Locale = typeof locales[number];
const foodsCopy = { en: enFoods, ja: jaFoods, ko: koFoods, "zh-TW": twFoods, "zh-CN": cnFoods };
const dishId = "63000000-0000-4000-8000-000000000001";
const sakaiId = "63000000-0000-4000-8000-000000000002";
const koreanId = "63000000-0000-4000-8000-000000000003";
const noReservationId = "63000000-0000-4000-8000-000000000004";
const dishTitle = "壽司 · Sushi · synthetic fixture";
const sakaiTitle = "鮨さかい · Sakai · synthetic fixture";
const googleUrl = "https://www.google.com/maps/search/?api=1&query=Synthetic+Sakai&query_place_id=ChIJ-mokaair-synthetic-sakai";
const naverUrl = "https://map.naver.com/p/entry/place/99999999";
const koreanGoogleUrl = "https://www.google.com/maps/search/?api=1&query=Synthetic+Seoul&query_place_id=ChIJ-mokaair-synthetic-seoul";
const tablecheckUrl = "https://www.tablecheck.com/en/shops/mokaair-synthetic-sakai/reserve";
const officialUrl = "https://restaurant.fixture.test/sakai";
const noReservationGoogleUrl = "https://www.google.com/maps/search/?api=1&query=Synthetic+Kyoto&query_place_id=ChIJ-mokaair-synthetic-kyoto";
const externalUrls = new Set([googleUrl, naverUrl, koreanGoogleUrl, tablecheckUrl, officialUrl, noReservationGoogleUrl]);

function merchant(id: string, name: string, overrides: Partial<FoodMerchant> = {}): FoodMerchant {
  return {
    id, slug: `fixture-${id}`, name, local_name: name,
    destination_id: "tokyo", destination_name: "Tokyo · fixture", country_code: "JP",
    area: null, categories: [], signature_dishes: [],
    address: "1 Synthetic Branch Street · not a real address", latitude: null, longitude: null,
    coordinate_source: { type: null, url: null, verified_at: null },
    official_website_url: null, verified_at: "2026-09-10T00:00:00Z", sources: [],
    map_links: [{ provider: "google", label: "Google Maps", url: googleUrl, primary: true }],
    reservation_links: [], ...overrides,
  };
}

function content(locale: Locale) {
  const sakai = merchant(sakaiId, sakaiTitle, {
    official_website_url: officialUrl,
    reservation_links: [{ provider: "tablecheck", label: "TableCheck", url: tablecheckUrl, verified_at: "2026-09-10T00:00:00Z", language_code: "en" }],
  });
  const korean = merchant(koreanId, "서울 음식점 · 長い店名と分店情報を確認するための合成テスト · synthetic fixture", {
    country_code: "KR", destination_id: "seoul", destination_name: "Seoul · fixture",
    map_links: [
      { provider: "naver", label: "Naver Map", url: naverUrl, primary: true },
      { provider: "google", label: "Google Maps", url: koreanGoogleUrl, primary: false },
    ],
  });
  const empty = merchant(noReservationId, "未提供訂位資料 · synthetic fixture", {
    map_links: [{ provider: "google", label: "Google Maps", url: noReservationGoogleUrl, primary: true }],
  });
  const dish: DiscoveryItem = {
    id: `food:${dishId}`, kind: "food", title: dishTitle,
    summary: "Synthetic dish introduction. No copied provider content or reservation availability.",
    locale, href: `/foods?food=${dishId}`, destination: { id: "tokyo", name: "Tokyo · fixture" },
    source: { kind: "editorial", label: "Synthetic editorial source", url: null },
    published_at: null, updated_at: null, thumbnail_url: null,
    collection_ref: { kind: "food", id: dishId },
    detail: {
      guides: [], merchants: [sakai, korean, empty], planning: null,
      intro: { body: "Synthetic reading paragraph for a scrollable food detail. ".repeat(12), locale, source: "fixture" },
    },
  };
  const own: DiscoveryItem = {
    ...dish, id: `merchant:${sakaiId}`, kind: "merchant", title: sakai.name,
    href: `/foods?merchant=${sakaiId}`, collection_ref: { kind: "merchant", id: sakaiId },
    detail: { guides: [], merchants: [sakai], planning: null },
  };
  const filler = Array.from({ length: 9 }, (_, index): DiscoveryItem => {
    const id = `64000000-0000-4000-8000-${String(index + 1).padStart(12, "0")}`;
    return { ...dish, id: `food:${id}`, title: `Synthetic food ${index + 1}`, detail: null, collection_ref: { kind: "food", id } };
  });
  return { dish, own, sakai, korean, empty, listing: [...filler, dish] };
}

async function fixtures(page: Page, locale: Locale, baseURL?: string) {
  const origin = new URL(baseURL || `http://127.0.0.1:${process.env.PLAYWRIGHT_PORT || "3000"}`);
  expect(["127.0.0.1", "localhost", "[::1]"]).toContain(origin.hostname);
  const data = content(locale);
  const writes: string[] = [], unexpectedExternal: string[] = [], detailReads: string[] = [], requests: string[] = [];
  await page.context().route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin === origin.origin) return route.fallback();
    if (externalUrls.has(url.href)) return route.fulfill({
      contentType: "text/html",
      body: "<!doctype html><title>Synthetic external destination</title><p>Local map or reservation fixture; no provider request.</p>",
    });
    unexpectedExternal.push(url.origin + url.pathname);
    return route.abort("blockedbyclient");
  });
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request(), url = new URL(request.url()), path = url.pathname.replace("/api/travel", "");
    const send = (body: unknown, status = 200) => route.fulfill({ status, json: body });
    if (request.method() !== "GET") { writes.push(`${request.method()} ${path}`); return send({ code: "unexpected_fixture_write" }, 405); }
    if (path === "/discovery/status") return send({ enabled: true });
    if (path === "/community/status") return send({ enabled: false });
    if (path === "/analytics/config") return send({ first_party_enabled: false, ga4_enabled: false });
    if (path === "/auth/me") return send({ code: "authentication_required" }, 401);
    if (path === "/auth/providers") return send({ providers: [] });
    if (path === "/runtime/site-visibility") return send({ hotspots_enabled: true, trips_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true });
    if (path === "/discovery/suggestions") return send({ query: url.searchParams.get("q"), items: [], destinations: [{ id: "tokyo", name: "Tokyo · fixture" }], topics: [] });
    if (["/discovery/feed", "/discovery/search"].includes(path)) {
      requests.push(url.search);
      return send({ enabled: true, query: url.searchParams.get("q") || "", items: data.listing, next_cursor: null, filters: { kinds: [], destinations: [], topics: [], category: "foods" } });
    }
    if (path.startsWith("/discovery/content/")) {
      detailReads.push(path);
      const item = [data.dish, data.own].find((entry) => path === `/discovery/content/${entry.kind}/${entry.id.split(":").at(-1)}`);
      return send(item || { code: "not_found" }, item ? 200 : 404);
    }
    if (["/saved-items", "/saved-items/states", "/discovery/collections"].includes(path)) return send({ items: [] });
    if (path === "/trips") return send([]);
    return send({ code: "fixture_endpoint_unavailable" }, 404);
  });
  return { ...data, writes, unexpectedExternal, detailReads, requests };
}

function byHref(container: Locator, href: string) {
  return container.locator(`a[href=${JSON.stringify(href)}]`);
}

async function safeExternal(link: Locator, url: string, brand: RegExp) {
  await expect(link).toHaveCount(1);
  await expect(link).toHaveAttribute("href", url);
  await expect(link).toHaveAttribute("target", "_blank");
  await expect(link).toHaveAttribute("rel", /\bnoopener\b/);
  await expect(link).toHaveAttribute("rel", /\bnoreferrer\b/);
  await expect(link).toHaveAccessibleName(brand);
  expect((await link.boundingBox())!.height).toBeGreaterThanOrEqual(44);
}

async function scrollPosition(link: Locator) {
  return link.evaluate((element) => {
    let node = element.parentElement;
    while (node && node.tagName !== "DIALOG") {
      if (node.scrollHeight > node.clientHeight + 1 && ["auto", "scroll"].includes(getComputedStyle(node).overflowY)) return node.scrollTop;
      node = node.parentElement;
    }
    return 0;
  });
}

for (const viewport of [{ width: 320, height: 740 }, { width: 390, height: 844 }, { width: 1280, height: 900 }]) {
  test.describe(`food link acceptance ${viewport.width}px`, () => {
    test.use({ viewport, isMobile: viewport.width < 600, hasTouch: viewport.width < 600 });
    for (const locale of locales) {
      test(`${locale}: exact maps, booking pages and nested detail return in light/dark`, async ({ page, baseURL }, info) => {
        test.setTimeout(90_000);
        info.annotations.push({ type: "evidence", description: "Synthetic local UI acceptance; not verification of actual merchants or platform availability." });
        const state = await fixtures(page, locale, baseURL);
        const c = getDiscoveryCopy(locale), f = getFrontendFlowCopy(locale);
        const listingPath = `/${locale}/explore?category=foods&q=Sushi&destination=tokyo&mode=latest`;
        await page.goto(listingPath);
        const historyEvents: string[] = [];
        page.on("console", (message) => { if (message.text().startsWith("food-history:")) historyEvents.push(message.text()); });
        await page.evaluate(() => {
          const record = (event: string, target?: unknown) => console.debug(`food-history:${JSON.stringify({ event, target, url: location.href, length: history.length })}`);
          const originalBack = history.back.bind(history);
          history.back = () => { record("back"); originalBack(); };
          for (const method of ["pushState", "replaceState"] as const) {
            const original = history[method].bind(history);
            history[method] = (data, unused, url) => { record(method, url); original(data, unused, url); };
          }
          window.addEventListener("popstate", () => record("popstate"));
          document.addEventListener("cancel", () => record("cancel"), true);
          document.addEventListener("close", () => record("close"), true);
        });
        const trigger = page.locator(`article[id="${state.dish.id}"]`).getByRole("link", { name: dishTitle, exact: true });
        for (const theme of ["light", "dark"] as const) {
          await page.emulateMedia({ colorScheme: theme, reducedMotion: "reduce" });
          await page.evaluate((value) => { document.documentElement.dataset.theme = value; document.documentElement.dataset.textSize = "large"; }, theme);
          await trigger.scrollIntoViewIfNeeded();
          const initialScroll = await page.evaluate(() => window.scrollY);
          expect(initialScroll).toBeGreaterThan(0);
          await trigger.click();
          const dialog = page.getByRole("dialog", { name: c.details, exact: true });
          await expect(dialog.getByRole("heading", { name: dishTitle, exact: true })).toBeVisible();
          await expect(page.locator("body")).toHaveCSS("overflow", "hidden");
          await expect(dialog.getByRole("heading", { name: f.nearbyFood, exact: true })).toBeVisible();
          const sakai = dialog.getByRole("link", { name: sakaiTitle, exact: true });
          await sakai.scrollIntoViewIfNeeded();
          await expect(sakai).not.toHaveAttribute("target", "_blank");
          await safeExternal(byHref(dialog, googleUrl), googleUrl, /Google Maps/);
          await safeExternal(byHref(dialog, tablecheckUrl), tablecheckUrl, /TableCheck/);
          await safeExternal(byHref(dialog, naverUrl), naverUrl, /Naver Map/);
          await safeExternal(byHref(dialog, koreanGoogleUrl), koreanGoogleUrl, /Google Maps/);
          const koreanRow = dialog.getByRole("link", { name: state.korean.name, exact: true }).locator("..");
          const koreanMaps = await koreanRow.locator('a[target="_blank"]').evaluateAll((links) => links.map((link) => link.getAttribute("href")));
          expect(koreanMaps.indexOf(naverUrl)).toBeLessThan(koreanMaps.indexOf(koreanGoogleUrl));
          const emptyRow = dialog.getByRole("link", { name: state.empty.name, exact: true }).locator("..");
          await expect(emptyRow.locator('a[target="_blank"]')).toHaveCount(1);
          await expect(emptyRow.getByText(foodsCopy[locale].noVerifiedReservation, { exact: true })).toBeVisible();
          const newTabHint = foodsCopy[locale].externalLinkLabel.replace("{label}", "").trim();
          expect(await byHref(dialog, googleUrl).getAttribute("aria-label")).toContain(newTabHint);
          const languageHint = foodsCopy[locale].reservationLanguage.replace("{language}", new Intl.DisplayNames([locale], { type: "language" }).of("en")!);
          await expect(dialog.getByText(languageHint, { exact: true })).toHaveCount(locale === "en" ? 0 : 1);
          expect(await koreanRow.evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
          await sakai.scrollIntoViewIfNeeded();
          await page.screenshot({ path: info.outputPath(`food-merchant-options-${locale}-${viewport.width}-${theme}.png`), fullPage: true });
          for (const url of [googleUrl, tablecheckUrl]) {
            const before = page.url();
            const popupReady = page.waitForEvent("popup");
            await byHref(dialog, url).click();
            const popup = await popupReady;
            await expect(popup).toHaveURL(url);
            await expect(popup.getByText("Local map or reservation fixture; no provider request.")).toBeVisible();
            await popup.close();
            await expect(page).toHaveURL(before);
            await expect(dialog).toBeVisible();
          }
          await sakai.scrollIntoViewIfNeeded();
          const foodScroll = await scrollPosition(sakai);
          expect(foodScroll).toBeGreaterThan(0);
          await sakai.click();
          await expect(dialog.getByRole("heading", { name: sakaiTitle, exact: true })).toBeVisible();
          await expect(dialog.getByRole("heading", { name: f.nearbyFood, exact: true })).toHaveCount(0);
          await expect(dialog.getByRole("link", { name: sakaiTitle, exact: true })).toHaveCount(0);
          await expect(dialog).toContainText(state.sakai.address!);
          await safeExternal(byHref(dialog, googleUrl), googleUrl, /Google Maps/);
          await safeExternal(byHref(dialog, tablecheckUrl), tablecheckUrl, /TableCheck/);
          await expect(byHref(dialog, officialUrl)).toHaveAttribute("target", "_blank");
          await page.keyboard.press("Tab");
          expect(await dialog.evaluate((node) => node.contains(document.activeElement))).toBe(true);
          await page.keyboard.press("Shift+Tab");
          expect(await dialog.evaluate((node) => node.contains(document.activeElement))).toBe(true);
          expect(await dialog.evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
          expect(await page.locator("html").evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
          await page.screenshot({ path: info.outputPath(`food-map-reservations-${locale}-${viewport.width}-${theme}.png`), fullPage: true });

          // Native browser Back must pop the merchant, not lose the food/list filters.
          await page.goBack();
          await expect(dialog.getByRole("heading", { name: dishTitle, exact: true })).toBeVisible();
          await expect(sakai).toBeFocused();
          await expect.poll(async () => Math.abs(await scrollPosition(sakai) - foodScroll)).toBeLessThanOrEqual(2);
          await sakai.click();
          await expect(dialog.getByRole("heading", { name: sakaiTitle, exact: true })).toBeVisible();
          // Closing the nested merchant uses the same return stack as browser Back.
          await page.keyboard.press("Escape");
          await expect(dialog.getByRole("heading", { name: dishTitle, exact: true })).toBeVisible();
          await expect(sakai).toBeFocused();
          await page.keyboard.press("Escape");
          await expect(dialog).toHaveCount(0);
          await expect(page.locator("body")).not.toHaveCSS("overflow", "hidden");
          await info.attach(`closed-detail-${theme}.json`, {
            contentType: "application/json",
            body: JSON.stringify(await page.evaluate(() => ({
              url: location.href,
              title: document.title,
              articles: document.querySelectorAll("article").length,
              dialogs: Array.from(document.querySelectorAll("dialog")).map((node) => ({ open: node.open, connected: node.isConnected })),
              focus: document.activeElement?.outerHTML.slice(0, 600),
              body: document.body.innerText.slice(0, 600),
            }))),
          });
          await expect(page, JSON.stringify(historyEvents)).toHaveURL(new URL(listingPath, baseURL!).href);
          await expect(trigger).toBeFocused();
          await expect.poll(async () => Math.abs(await page.evaluate(() => window.scrollY) - initialScroll)).toBeLessThanOrEqual(2);
        }
        expect(state.writes).toEqual([]);
        expect(state.unexpectedExternal).toEqual([]);
        expect(state.requests.length).toBeGreaterThan(0);
        for (const query of state.requests) {
          const params = new URLSearchParams(query);
          expect(params.get("q")).toBe("Sushi");
          expect(params.get("category")).toBe("foods");
          expect(params.get("destination")).toBe("tokyo");
          expect(params.get("mode")).toBe("latest");
        }
      });
    }
  });
}

test("a direct merchant detail closes locally without navigating away from its filters", async ({ page, baseURL }) => {
  const state = await fixtures(page, "en", baseURL);
  const listing = "/en/explore?category=foods&destination=tokyo";
  await page.goto(`${listing}&content=merchant:${sakaiId}`);
  const dialog = page.getByRole("dialog", { name: getDiscoveryCopy("en").details, exact: true });
  await expect(dialog.getByRole("heading", { name: sakaiTitle, exact: true })).toBeVisible();
  await expect(dialog.getByRole("link", { name: sakaiTitle, exact: true })).toHaveCount(0);
  await safeExternal(byHref(dialog, googleUrl), googleUrl, /Google Maps/);
  await safeExternal(byHref(dialog, tablecheckUrl), tablecheckUrl, /TableCheck/);
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(page).toHaveURL(new URL(listing, page.url()).href);
  expect(state.writes).toEqual([]);
  expect(state.unexpectedExternal).toEqual([]);
});
