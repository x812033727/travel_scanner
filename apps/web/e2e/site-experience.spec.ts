import { expect, test, type Locator, type Page } from "@playwright/test";
import type { DiscoveryItem } from "../lib/discovery";
import { getDiscoveryCopy } from "../lib/discovery-copy";

// Local synthetic UI evidence only. No production content, accounts, API writes,
// provider calls, or injected theme attributes are used to prove user interaction.
const id = "61000000-0000-4000-8000-000000000001";
const articleUrl = "https://reading.fixture.test/article";
const videoUrl = "https://reading.fixture.test/video";
const item: DiscoveryItem = {
  id: `hotspot:${id}`, kind: "hotspot", title: "Synthetic riverside reading stop",
  summary: "A local fixture for reading, topics and source links.", locale: "en",
  href: `/hotspots?hotspot=${id}`, destination: { id: "tokyo", name: "Tokyo fixture" },
  source: { kind: "official", label: "Synthetic city publisher", url: "https://city.fixture.test/source" },
  published_at: null, updated_at: null, thumbnail_url: null,
  collection_ref: { kind: "hotspot", id },
  display_topics: [
    { id: "category:culture", label: "Historic walks and local cultural experiences through the city's everyday architecture" },
    { id: "theme:evening", label: "Evening walks" },
    { id: "theme:coast", label: "Coastal scenery" },
  ],
  detail: {
    intro: { body: "This is synthetic read-only content, not private itinerary data.", locale: "en", source: "fixture" },
    merchants: [],
    guides: [
      { id: "article:61000000-0000-4000-8000-000000000002", kind: "article", title: "Before you go article", summary: "", locale: "en", href: "/hotspots", destination: null, source: { kind: "editorial", label: "Article publisher", url: articleUrl }, published_at: null, updated_at: null, thumbnail_url: null },
      { id: "video:61000000-0000-4000-8000-000000000003", kind: "video", title: "Before you go video", summary: "", locale: "en", href: "/hotspots", destination: null, source: { kind: "editorial", label: "Video publisher", url: videoUrl }, published_at: null, updated_at: null, thumbnail_url: null },
    ],
    place: { status: "ready", address: "1 Synthetic Walk, Tokyo", coordinates: { latitude: 34.395483, longitude: 132.453592, source: "fixture" } },
  },
};

async function fixtures(page: Page, baseURL: string | undefined, discovery = true) {
  const origin = new URL(baseURL || "http://127.0.0.1:3000");
  expect(["localhost", "127.0.0.1", "[::1]"]).toContain(origin.hostname);
  const writes: string[] = [], external: string[] = [];
  await page.context().route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin === origin.origin) return route.fallback();
    if ([articleUrl, videoUrl].includes(url.href)) return route.fulfill({ contentType: "text/html", body: "<title>Isolated reading fixture</title><p>Isolated source, not an external request.</p>" });
    external.push(url.origin + url.pathname); return route.abort("blockedbyclient");
  });
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request(), url = new URL(request.url()), path = url.pathname.replace("/api/travel", "");
    const send = (json: unknown, status = 200) => route.fulfill({ status, json });
    if (request.method() !== "GET") { writes.push(`${request.method()} ${path}`); return send({ code: "unexpected_fixture_write" }, 405); }
    if (path === "/discovery/status") return send({ enabled: discovery });
    if (path === "/community/status") return send({ enabled: false });
    if (path === "/analytics/config") return send({ first_party_enabled: false, ga4_enabled: false });
    if (path === "/auth/me") return send({ code: "authentication_required" }, 401);
    if (path === "/runtime/site-visibility") return send({ hotspots_enabled: true, trips_enabled: true, alerts_enabled: true, flight_status_enabled: true, airline_fares_enabled: true, pricing_enabled: true });
    if (path === "/discovery/suggestions") return send({ query: "", items: [], destinations: [], topics: [] });
    if (["/discovery/feed", "/discovery/search"].includes(path)) return send({ enabled: true, items: [item], next_cursor: null, filters: { kinds: [], destinations: [], topics: [] } });
    if (path === `/discovery/content/hotspot/${id}`) return send(item);
    if (["/saved-items", "/saved-items/states", "/discovery/collections"].includes(path)) return send({ items: [] });
    if (path === "/trips") return send([]);
    return send({ code: "fixture_endpoint_unavailable" }, 404);
  });
  return { writes, external };
}

/** Composite CSS alpha through the real ancestor chain. Opaque cards stop the
 * chain before decorative gradients; unsupported images are rejected, not guessed. */
async function contrast(target: Locator, outline = false) {
  return target.evaluate((element, focus) => {
    const canvas = document.createElement("canvas"); canvas.width = 1; canvas.height = 1;
    const context = canvas.getContext("2d")!;
    const rgba = (value: string) => {
      context.clearRect(0, 0, 1, 1); context.fillStyle = value; context.fillRect(0, 0, 1, 1);
      return [...context.getImageData(0, 0, 1, 1).data].map((channel, index) => index === 3 ? channel / 255 : channel);
    };
    const over = (foreground: number[], background: number[]) => foreground.slice(0, 3).map((channel, index) => channel * foreground[3] + background[index] * (1 - foreground[3]));
    const layers: number[][] = [];
    let node: Element | null = focus ? element.parentElement : element;
    while (node) {
      const style = getComputedStyle(node), layer = rgba(style.backgroundColor);
      if (layer[3] > 0) layers.push(layer);
      if (layer[3] === 1) break;
      if (style.backgroundImage !== "none") throw new Error("Contrast sample must have an opaque surface before an image/gradient");
      node = node.parentElement;
    }
    let background = [255, 255, 255];
    for (const layer of layers.reverse()) background = over(layer, background);
    const style = getComputedStyle(element), foreground = over(rgba(focus ? style.outlineColor : style.color), background);
    const luminance = (rgb: number[]) => rgb.map((channel) => { const v = channel / 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }).reduce((sum, channel, index) => sum + channel * [.2126, .7152, .0722][index], 0);
    const values = [luminance(foreground), luminance(background)];
    return { ratio: (Math.max(...values) + .05) / (Math.min(...values) + .05), color: style.color, background, outline: style.outlineColor, outlineWidth: parseFloat(style.outlineWidth) };
  }, outline);
}

test("six palettes use actual controls, accessible colours and independent persisted mode", async ({ page, baseURL }, info) => {
  test.setTimeout(90_000);
  info.annotations.push({ type: "evidence", description: "Local synthetic API fixtures; real palette controls, no dataset injection." });
  const state = await fixtures(page, baseURL);
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });
  await page.goto("/en/my");
  const mode = page.getByRole("main").getByRole("combobox", { name: "Appearance", exact: true });
  const paletteGroup = page.getByRole("group", { name: "Colour palette", exact: true });
  await expect(mode).toBeEnabled();
  await expect(page.getByRole("banner").locator('select[aria-label="Language"]:visible')).toHaveCount(1);
  await expect(page.getByRole("contentinfo").getByRole("combobox", { name: "Language" })).toHaveCount(0);
  const observations: unknown[] = [];
  for (const [palette, name] of [["mocha", "Classic Mocha"], ["lagoon", "Lagoon Blue"], ["forest", "Forest Green"]]) {
    await paletteGroup.getByRole("radio", { name, exact: true }).check();
    for (const theme of ["light", "dark"]) {
      await mode.selectOption(theme);
      await expect(page.locator("html")).toHaveAttribute("data-palette", palette);
      await expect(page.locator("html")).toHaveAttribute("data-theme", theme);
      const body = await contrast(page.getByRole("main").getByRole("heading", { level: 1 }));
      const muted = await contrast(paletteGroup.locator("p"));
      const link = await contrast(page.getByRole("contentinfo").getByRole("link", { name: "Privacy policy", exact: true }));
      const button = await contrast(page.getByRole("radiogroup", { name: "Text size" }).getByRole("radio", { name: "Standard", exact: true }));
      for (const sample of [body, muted, link, button]) expect(sample.ratio).toBeGreaterThanOrEqual(4.5);
      await mode.focus();
      const focus = await contrast(mode.locator(".."), true);
      expect(focus.outlineWidth).toBeGreaterThanOrEqual(3);
      expect(focus.ratio).toBeGreaterThanOrEqual(3);
      observations.push({ palette, theme, body, muted, link, button, focus });
      await expect.poll(() => page.locator("html").evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
      await page.screenshot({ path: info.outputPath(`synthetic-palette-${palette}-${theme}.png`), fullPage: true });
    }
  }
  await info.attach("composited-palette-contrast", { body: JSON.stringify(observations, null, 2), contentType: "application/json" });
  await page.reload();
  await expect(mode).toHaveValue("dark");
  await expect(paletteGroup.getByRole("radio", { name: "Forest Green" })).toBeChecked();
  await mode.selectOption("system");
  await page.emulateMedia({ colorScheme: "light" });
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await page.emulateMedia({ colorScheme: "dark" });
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(page.locator("html")).toHaveAttribute("data-palette", "forest");
  await page.reload();
  await expect(mode).toHaveValue("system");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(page.locator("html")).toHaveAttribute("data-palette", "forest");
  expect(state.writes).toEqual([]); expect(state.external).toEqual([]);
});

test("top language stays reachable with discovery off and never duplicates inside the mobile drawer", async ({ page, baseURL, isMobile }) => {
  const state = await fixtures(page, baseURL, false);
  await page.goto("/en/my");
  const header = page.getByRole("banner");
  await expect(header.locator('select[aria-label="Language"]:visible')).toHaveCount(1);
  await expect(page.getByRole("group", { name: "Colour palette" })).toBeVisible();
  if (isMobile) {
    const trigger = header.getByRole("button", { name: "Open navigation menu" });
    await trigger.click();
    const drawer = page.getByRole("dialog");
    await expect(drawer).toBeVisible();
    await expect(drawer.getByRole("combobox", { name: "Language" })).toHaveCount(0);
    await page.keyboard.press("Escape");
    await expect(drawer).toHaveCount(0);
    await expect(trigger).toBeFocused();
  }
  expect(state.writes).toEqual([]); expect(state.external).toEqual([]);
});

test("read-only details retain all topics and distinguish article and video source links", async ({ page, baseURL }) => {
  const state = await fixtures(page, baseURL);
  await page.goto("/en/explore?destination=tokyo");
  const card = page.locator(`article[id="${item.id}"]`);
  for (const topic of item.display_topics!) await expect(card.getByText(topic.label, { exact: true })).toBeVisible();
  await expect(card.locator("img")).toHaveCount(0);
  await card.getByRole("link", { name: item.title, exact: true }).click();
  const dialog = page.getByRole("dialog", { name: getDiscoveryCopy("en").details, exact: true });
  await expect(dialog).not.toContainText("34.395483");
  await expect(dialog).not.toContainText("132.453592");
  for (const [name, href] of [["Before you go article (Article publisher)", articleUrl], ["Before you go video (Video publisher)", videoUrl]]) {
    const source = dialog.getByRole("link", { name, exact: true });
    await expect(source).toHaveAttribute("href", href);
    await expect(source).toHaveAttribute("target", "_blank");
    await expect(source).toHaveAttribute("rel", /noopener/);
    await expect(source).toHaveAttribute("rel", /noreferrer/);
  }
  expect(state.writes).toEqual([]); expect(state.external).toEqual([]);
});
