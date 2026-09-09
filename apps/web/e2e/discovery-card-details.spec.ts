import { expect, test, type Locator, type Page } from "@playwright/test";
import type { DiscoveryItem } from "../lib/discovery";
import { getDiscoveryCopy } from "../lib/discovery-copy";
import { getFrontendFlowCopy } from "../lib/frontend-flow-copy";
import { frontendCopy } from "../lib/frontend-navigation";

// Synthetic, isolated UI fixtures. These are not real venues, licensed provider
// photographs, production moderation evidence, or proof of backend permissions.
const placeId = "51000000-0000-4000-8000-000000000001";
const imageId = "51000000-0000-4000-8000-000000000002";
const mediaId = "51000000-0000-4000-8000-000000000003";
const unsafeImageId = "51000000-0000-4000-8000-000000000004";
const guideUrl = "https://guide.fixture.test/read-before-trip";
const fallbackGuideUrl = "http://fallback-guide.fixture.test/city-walk";
const imageUrl = "https://images.fixture.test/authorized-thumbnail.svg";
const signedImageUrl = "https://images.fixture.test/authorized-media.svg";
const imageFixture = '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360"><rect width="640" height="360" fill="#0D6B68"/><text x="32" y="180" fill="#F7F1E8" font-size="28">Synthetic image fixture</text></svg>';
const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
type Locale = typeof locales[number];
type FixtureItem = DiscoveryItem & { display_topics: Array<{ id: string; label: string }> };
const topicLabels: Record<Locale, readonly [string, string, string]> = {
  "zh-TW": ["歷史街區散步與在地文化體驗，以及適合慢慢探索的城市建築故事", "夜間散步", "海岸景觀"],
  "zh-CN": ["历史街区散步与在地文化体验，以及适合慢慢探索的城市建筑故事", "夜间散步", "海岸景观"],
  en: ["Historic neighborhood walks and local cultural experiences with stories of architecture and everyday city life", "Evening walks", "Coastal scenery"],
  ja: ["歴史ある街並みの散策と地域文化の体験、建築と日常の物語をゆっくり楽しむ旅", "夜の散策", "海岸の風景"],
  ko: ["역사적인 동네 산책과 지역 문화 체험을 통해 건축과 일상 속 도시 이야기를 천천히 만나는 여행", "저녁 산책", "해안 풍경"],
};

function guide(index: number, title: string, url: string | null, label: string): DiscoveryItem {
  const id = `52000000-0000-4000-8000-${String(index).padStart(12, "0")}`;
  return {
    id: `article:${id}`, kind: "article", title, summary: "Synthetic source-link fixture.",
    locale: "en", href: `/hotspots?guide=${id}`, destination: null,
    source: { kind: "editorial", label, url }, published_at: null, updated_at: null,
    thumbnail_url: null, collection_ref: { kind: "guide", id },
  };
}

function content(locale: Locale, invalidGuidesOnly = false): FixtureItem[] {
  const [first, second, third] = topicLabels[locale];
  const invalidGuides = [
    guide(3, "Missing source fixture", null, "Missing publisher"),
    guide(4, "Unsafe script fixture", "javascript:void(0)", "Unsafe publisher"),
    guide(5, "Unsafe data fixture", "data:text/html,fixture", "Unsafe publisher"),
  ];
  const item: FixtureItem = {
    id: `hotspot:${placeId}`, kind: "hotspot", title: "Riverside walk · synthetic fixture",
    summary: "An image-free editorial fixture with verifiable reading controls.",
    locale, href: `/hotspots?hotspot=${placeId}`, destination: { id: "tokyo", name: "Tokyo · fixture" },
    source: { kind: "official", label: "Synthetic city source", url: "https://city.fixture.test/source" },
    published_at: null, updated_at: "2026-09-09T00:00:00Z", thumbnail_url: null,
    collection_ref: { kind: "hotspot", id: placeId },
    display_topics: [
      { id: "category:culture", label: first },
      { id: "theme:evening", label: second },
      { id: "theme:coast", label: third },
      { id: "theme:duplicate", label: `  ${first}  ` },
      { id: "theme:empty", label: "   " },
      { id: "category:kind-duplicate", label: getDiscoveryCopy(locale).kinds.hotspot },
    ],
    detail: {
      intro: { body: "Synthetic public introduction. No copied private itinerary information.", locale, source: "fixture" },
      merchants: [],
      guides: invalidGuidesOnly ? invalidGuides : [
        guide(1, "A city walk · synthetic guide", guideUrl, "  Synthetic travel publisher  "),
        guide(2, "A coastal walk · synthetic guide", fallbackGuideUrl, "   "),
        ...invalidGuides,
      ],
      place: {
        status: "ready", address: "1 Synthetic Walk, Tokyo · not a real address",
        opening_hours: { weekday_descriptions: ["Monday: fixture opening hours"] },
        google_maps_url: "https://maps.fixture.test/place",
        official_website_url: "https://city.fixture.test/venue", official_website_verified: true,
        // Existing API coordinate data must not leak into the new reading UI.
        coordinates: { latitude: 34.395483, longitude: 132.453592, source: "synthetic fixture" },
      },
      planning: { kind: "hotspot", id: placeId, destination_id: "tokyo", selection_path: `/hotspots/${placeId}/trip-selections`, merchants: [] },
    },
  };
  const photo: FixtureItem = {
    ...item, id: `hotspot:${imageId}`, title: "Authorized thumbnail · synthetic fixture",
    thumbnail_url: imageUrl, display_topics: [], detail: null,
    collection_ref: { kind: "hotspot", id: imageId },
  };
  const media: FixtureItem = {
    ...photo, id: `hotspot:${mediaId}`, title: "Authorized media · synthetic fixture",
    thumbnail_url: null, collection_ref: { kind: "hotspot", id: mediaId },
    content: { text: "Synthetic authorized-media fixture", media: [{ id: mediaId, alt: "Authorized community image fixture", width: 640, height: 360 }] },
  };
  const unsafe: FixtureItem = {
    ...photo, id: `hotspot:${unsafeImageId}`, title: "Unsafe thumbnail · synthetic fixture",
    thumbnail_url: "javascript:void(0)", collection_ref: { kind: "hotspot", id: unsafeImageId },
  };
  return [item, photo, media, unsafe];
}

async function fixtures(page: Page, locale: Locale, baseURL: string | undefined, invalidGuidesOnly = false) {
  const origin = new URL(baseURL || "http://127.0.0.1:3000");
  expect(["127.0.0.1", "localhost", "[::1]"]).toContain(origin.hostname);
  const items = content(locale, invalidGuidesOnly);
  const writes: string[] = [], detailReads: string[] = [], unexpectedExternal: string[] = [], mediaReads: string[] = [];
  // Context routes also intercept the first navigation in a target=_blank popup.
  await page.context().route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin === origin.origin) return route.fallback();
    if ([imageUrl, signedImageUrl].includes(url.href)) return route.fulfill({ contentType: "image/svg+xml", body: imageFixture });
    if ([guideUrl, fallbackGuideUrl].includes(url.href)) return route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Synthetic guide source</title><p>Isolated guide source fixture. No external publisher request.</p>" });
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
    if (path === "/runtime/site-visibility") return send({ hotspots_enabled: true, trips_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true });
    if (path === "/discovery/suggestions") return send({ query: url.searchParams.get("q"), items: [], destinations: [{ id: "tokyo", name: "Tokyo · fixture" }], topics: [] });
    if (["/discovery/feed", "/discovery/search"].includes(path)) return send({ enabled: true, query: url.searchParams.get("q") || "", items, next_cursor: null, filters: { kinds: [], destinations: [], topics: [] } });
    if (path.startsWith("/discovery/content/")) {
      detailReads.push(path);
      const item = items.find((entry) => path === `/discovery/content/${entry.kind}/${entry.id.split(":").at(-1)}`);
      return send(item || { code: "not_found" }, item ? 200 : 404);
    }
    if (path === `/community/media/${mediaId}`) { mediaReads.push(url.search); return send({ url: signedImageUrl }); }
    if (["/saved-items", "/saved-items/states", "/discovery/collections"].includes(path)) return send({ items: [] });
    if (path === "/trips") return send([]);
    return send({ code: "fixture_endpoint_unavailable" }, 404);
  });
  return { items, writes, detailReads, unexpectedExternal, mediaReads };
}

function card(page: Page, item: DiscoveryItem) {
  return page.locator(`article[id="${item.id}"]`);
}

async function noHorizontalOverflow(locator: Locator) {
  expect(await locator.evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
}

async function secureNewTab(link: Locator, href: string) {
  await expect(link).toHaveAttribute("href", href);
  await expect(link).toHaveAttribute("target", "_blank");
  await expect(link).toHaveAttribute("rel", /\bnoopener\b/);
  await expect(link).toHaveAttribute("rel", /\bnoreferrer\b/);
}

for (const locale of locales) {
  test(`synthetic fixtures ${locale}: compact cards and source-linked details in light/dark`, async ({ page, baseURL }, info) => {
    test.setTimeout(60_000);
    info.annotations.push({ type: "evidence", description: "Synthetic UI fixtures only; not production content or provider-licensing evidence." });
    const state = await fixtures(page, locale, baseURL);
    const c = getDiscoveryCopy(locale), f = getFrontendFlowCopy(locale), n = frontendCopy(locale);
    const [item] = state.items, [first, second, third] = topicLabels[locale];
    await page.goto(`/${locale}/explore?destination=tokyo`);
    const article = card(page, item), title = article.getByRole("link", { name: item.title, exact: true });

    for (const mode of ["light", "dark"] as const) {
      await page.emulateMedia({ colorScheme: mode, reducedMotion: "reduce" });
      await page.evaluate((theme) => { document.documentElement.dataset.theme = theme; document.documentElement.dataset.textSize = "large"; }, mode);
      await expect(title).toBeVisible();
      await expect(article.locator(":scope > a")).toHaveCount(0);
      await expect(article.locator("img")).toHaveCount(0);
      await expect(article.getByText(first, { exact: true })).toHaveCount(1);
      await expect(article.getByText(second, { exact: true })).toBeVisible();
      await expect(article.getByText(third, { exact: true })).toHaveCount(0);
      const more = article.getByText("+1", { exact: true });
      await expect(more).toHaveAttribute("aria-hidden", "true");
      const remaining = article.getByTitle(`${c.topic}: ${third}`, { exact: true });
      await expect(remaining).toContainText("+1");
      await expect(remaining.getByText(`${c.topic}: ${third}`, { exact: true })).toHaveClass(/\bsr-only\b/);
      await expect.poll(() => article.getByText(first, { exact: true }).evaluate((node) => {
        const range = document.createRange(); range.selectNodeContents(node);
        return new Set(Array.from(range.getClientRects()).map((rect) => Math.round(rect.top))).size;
      })).toBeGreaterThan(1);
      await noHorizontalOverflow(article);
      await noHorizontalOverflow(page.locator("html"));
      await page.screenshot({ path: info.outputPath(`synthetic-fixtures-cards-${locale}-${mode}.png`), fullPage: true });

      await title.click();
      const dialog = page.getByRole("dialog", { name: c.details, exact: true });
      await expect(dialog.getByRole("heading", { name: item.title, exact: true })).toBeVisible();
      await expect(dialog).toContainText(item.detail!.place!.address!);
      await expect(dialog).toContainText("Monday: fixture opening hours");
      await expect(dialog).not.toContainText("34.395483");
      await expect(dialog).not.toContainText("132.453592");
      await expect(dialog).not.toContainText(`${f.coordinates}:`);
      await expect(dialog.getByRole("button", { name: f.copy, exact: true })).toHaveCount(0);
      await expect(dialog.getByRole("link", { name: f.saveItem, exact: true })).toBeVisible();
      await expect(dialog.getByRole("button", { name: n.plan, exact: true })).toBeVisible();
      await secureNewTab(dialog.getByRole("link", { name: f.map, exact: true }), "https://maps.fixture.test/place");
      await secureNewTab(dialog.getByRole("link", { name: f.officialSite, exact: true }), "https://city.fixture.test/venue");
      await secureNewTab(dialog.getByRole("link", { name: c.source, exact: true }), "https://city.fixture.test/source");
      const source = dialog.getByRole("link", { name: "A city walk · synthetic guide (Synthetic travel publisher)", exact: true });
      const fallback = dialog.getByRole("link", { name: "A coastal walk · synthetic guide (fallback-guide.fixture.test)", exact: true });
      await secureNewTab(source, guideUrl);
      await secureNewTab(fallback, fallbackGuideUrl);
      for (const invalid of ["Missing source fixture", "Unsafe script fixture", "Unsafe data fixture"]) await expect(dialog.getByText(invalid, { exact: false })).toHaveCount(0);
      await noHorizontalOverflow(dialog);
      await page.screenshot({ path: info.outputPath(`synthetic-fixtures-details-${locale}-${mode}.png`), fullPage: true });

      if (mode === "light") {
        const before = page.url(), reads = [...state.detailReads];
        const popupReady = page.waitForEvent("popup");
        await source.click();
        const popup = await popupReady;
        await expect(popup).toHaveURL(guideUrl);
        await expect(popup.getByText("Isolated guide source fixture. No external publisher request.")).toBeVisible();
        await popup.close();
        await expect(page).toHaveURL(before);
        await expect(dialog).toBeVisible();
        expect(state.detailReads).toEqual(reads);
      }
      await page.keyboard.press("Escape");
      await expect(dialog).toHaveCount(0);
      await expect(title).toBeFocused();
      await expect(page).toHaveURL(new RegExp(`/${locale}/explore\\?destination=tokyo$`));
    }
    expect(state.writes).toEqual([]);
    expect(state.unexpectedExternal).toEqual([]);
  });
}

test("synthetic fixtures: authorized image covers remain, unsafe covers leave no link", async ({ page, baseURL }, info) => {
  const state = await fixtures(page, "en", baseURL);
  await page.goto("/en/explore");
  const [, photo, media, unsafe] = state.items;
  for (const [item, src] of [[photo, imageUrl], [media, signedImageUrl]] as const) {
    const article = card(page, item);
    await article.scrollIntoViewIfNeeded();
    const image = article.getByRole("img");
    await expect(image).toBeVisible();
    await expect(image).toHaveAttribute("src", src);
    await expect(image).toHaveAttribute("referrerpolicy", "no-referrer");
    await expect.poll(() => image.evaluate((node: HTMLImageElement) => node.complete && node.naturalWidth > 0)).toBe(true);
    await expect(article.locator(":scope > a")).toHaveCount(1);
    await expect(article.getByRole("link", { name: item.title, exact: true })).toBeVisible();
  }
  expect(state.mediaReads).toContain("?thumbnail=true");
  const noCover = card(page, unsafe);
  await expect(noCover.locator("img")).toHaveCount(0);
  await expect(noCover.locator(":scope > a")).toHaveCount(0);
  await expect(noCover.getByRole("link", { name: unsafe.title, exact: true })).toBeVisible();
  await page.screenshot({ path: info.outputPath("synthetic-fixtures-authorized-images.png"), fullPage: true });
  expect(state.writes).toEqual([]);
  expect(state.unexpectedExternal).toEqual([]);
});

test("synthetic fixtures: all unavailable guide sources omit the related-guides section", async ({ page, baseURL }) => {
  const state = await fixtures(page, "en", baseURL, true);
  await page.goto(`/en/explore?destination=tokyo&content=hotspot:${placeId}`);
  const dialog = page.getByRole("dialog", { name: getDiscoveryCopy("en").details, exact: true });
  await expect(dialog.getByRole("heading", { name: state.items[0].title, exact: true })).toBeVisible();
  await expect(dialog.getByRole("heading", { name: getFrontendFlowCopy("en").relatedGuides, exact: true })).toHaveCount(0);
  await expect(dialog.locator('a[href^="javascript:"], a[href^="data:"]')).toHaveCount(0);
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(page).toHaveURL(/\/en\/explore\?destination=tokyo$/);
  expect(state.writes).toEqual([]);
  expect(state.unexpectedExternal).toEqual([]);
});
