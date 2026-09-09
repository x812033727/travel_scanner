import { expect, test, type Locator, type Page } from "@playwright/test";
import type { RouteSegment, Trip } from "../lib/trip-types";
import { dayTimelineCopy } from "../components/planner/day-timeline-copy";
import { editorFixture } from "./fixtures/itinerary-editor";
import { pretendSignedIn } from "./session";
import zhTW from "../messages/zh-TW/trips.json" with { type: "json" };
import zhCN from "../messages/zh-CN/trips.json" with { type: "json" };
import en from "../messages/en/trips.json" with { type: "json" };
import ja from "../messages/ja/trips.json" with { type: "json" };
import ko from "../messages/ko/trips.json" with { type: "json" };

const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
const tones = ["hotel", "lunch", "dinner"] as const;
const messages = { "zh-TW": zhTW, "zh-CN": zhCN, en, ja, ko };
type Theme = "light" | "dark";

// All API requests are local fixtures. The map double is deliberately labelled:
// these screenshots prove layout, not a live Google map or provider response.
async function workspace(page: Page, locale = "zh-TW", optional = false) {
  let trip: Trip = structuredClone(editorFixture);
  trip.items = trip.items.filter((item) => item.day_date === trip.start_date);
  trip.end_date = trip.start_date;
  trip.routing = {
    status: "idle", total: 4, completed: 0,
    day_settings: [{ day_date: trip.start_date!, default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: false }],
  };
  if (optional) {
    trip.primary_lodging = undefined;
    trip.items = trip.items.map((item) => item.system_role ? {
      ...item, latitude: null, longitude: null, location_name: "", location_source: null,
      is_skipped: item.system_role === "dinner", data: { meal_selection_source: "unset", needs_place_confirmation: true },
    } : item);
  }
  const writes: Array<{ path: string; body: Record<string, unknown> }> = [];
  const previews: Array<Record<string, unknown>> = [];
  const unexpected: string[] = [];
  let lastSegment: RouteSegment | undefined;
  await pretendSignedIn(page);
  await page.route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (["127.0.0.1", "localhost"].includes(url.hostname)) return route.continue();
    unexpected.push(`External network blocked: ${url.origin}`);
    return route.abort();
  });
  await page.addInitScript(() => {
    class LocalMap {
      constructor(element: HTMLElement) {
        element.dataset.testid = "local-route-map";
        element.textContent = "Local map fixture · no provider request";
        element.style.background = "#dce8ec";
        element.style.color = "#243d44";
        element.style.padding = "24px";
      }
      fitBounds() {}
    }
    class Overlay { setMap() {} addListener() {} }
    class Bounds { extend() {} }
    Object.assign(window, { google: { maps: { Map: LocalMap, Marker: Overlay, Polyline: Overlay, LatLngBounds: Bounds, event: { clearInstanceListeners() {} } } } });
  });
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (path.endsWith("/auth/me")) return route.fulfill({ json: { id: "route-tones-fixture", email: "route-tones@example.test", role: "user", is_active: true } });
    if (path.endsWith("/routes/preview") && request.method() === "POST") {
      const body = request.postDataJSON();
      previews.push(body);
      lastSegment = {
        from_item_id: body.from_item_id, to_item_id: body.to_item_id,
        status: "complete", travel_mode: body.travel_mode, buffer_minutes: body.buffer_minutes,
        provider: "google_routes", attribution: "Local route fixture", generated_at: "2026-09-09T00:00:00Z",
        schedule_mode: "preview", preference: "FEWER_TRANSFERS", duration_minutes: 12,
        distance_meters: 850, encoded_polyline: null, steps: [], details_available: [], warnings: [],
      };
      return route.fulfill({ json: { kind: "provider", preview_id: "fixture-walk-15", expires_at: "2100-01-01T00:00:00Z", segment: lastSegment, schedule_impact: { affected_items: [], conflicts: [] } } });
    }
    if (path.endsWith("/routes/apply") && request.method() === "POST") {
      writes.push({ path, body: request.postDataJSON() });
      if (!lastSegment) return route.fulfill({ status: 409, json: { detail: "No fixture preview" } });
      trip = { ...trip, version: trip.version + 1, route_segments: [lastSegment] };
      return route.fulfill({ json: trip });
    }
    if (path === "/api/travel/trips/intuitive-trip" && request.method() === "GET") return route.fulfill({ json: trip });
    if (path.endsWith("/runtime/public-config") && request.method() === "GET") return route.fulfill({ json: { google_maps_browser_key: "fixture-not-a-key", google_maps_javascript_enabled: true } });
    if (request.method() === "GET" && /\/health$/.test(path)) return route.fulfill({ json: { days: [], issues: [] } });
    if (request.method() === "GET" && /\/community\/status$|\/discovery\/status$|\/analytics\/config$/.test(path)) return route.fulfill({ json: { enabled: false } });
    if (request.method() === "GET" && /\/usage$/.test(path)) return route.fulfill({ json: {} });
    if (request.method() === "GET" && /\/saved-items$|\/trips$/.test(path)) return route.fulfill({ json: [] });
    unexpected.push(`${request.method()} ${path}`);
    return route.fulfill({ status: 503, json: { detail: "Unstubbed request blocked" } });
  });
  await page.goto(`/${locale}/trips/intuitive-trip`);
  await expect(page.getByRole("heading", { name: trip.name })).toBeVisible();
  return { writes, previews, unexpected, current: () => trip };
}

async function theme(page: Page, value: Theme) {
  await page.evaluate((selected) => {
    document.documentElement.dataset.theme = selected;
    document.documentElement.style.colorScheme = selected;
  }, value);
  await expect(page.locator("html")).toHaveAttribute("data-theme", value);
}

async function paintedContrast(target: Locator) {
  return target.evaluate((element) => {
    const canvas = document.createElement("canvas");
    canvas.width = canvas.height = 1;
    const context = canvas.getContext("2d")!;
    const rgba = (value: string) => {
      context.clearRect(0, 0, 1, 1);
      context.fillStyle = value;
      context.fillRect(0, 0, 1, 1);
      return Array.from(context.getImageData(0, 0, 1, 1).data).map((channel, index) => index === 3 ? channel / 255 : channel);
    };
    const over = (front: number[], back: number[]) => [...front.slice(0, 3).map((channel, index) => channel * front[3] + back[index] * (1 - front[3])), 1];
    const luminance = (color: number[]) => {
      const linear = color.slice(0, 3).map((channel) => channel / 255 <= .04045 ? channel / 255 / 12.92 : ((channel / 255 + .055) / 1.055) ** 2.4);
      return linear[0] * .2126 + linear[1] * .7152 + linear[2] * .0722;
    };
    const layers: number[][] = [];
    const images: string[] = [];
    for (let node: Element | null = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.backgroundImage !== "none") images.push(style.backgroundImage);
      const paint = rgba(style.backgroundColor);
      layers.push(paint);
      if (paint[3] >= .999) break;
    }
    const background = layers.reverse().reduce((back, front) => over(front, back), [255, 255, 255, 1]);
    const style = getComputedStyle(element);
    const foreground = rgba(style.color);
    foreground[3] *= Number(style.opacity);
    const a = luminance(over(foreground, background));
    const b = luminance(background);
    return { contrast: (Math.max(a, b) + .05) / (Math.min(a, b) + .05), background: background.join(","), luminance: b, images };
  });
}

async function readable(target: Locator, dark: boolean) {
  await expect(target).toBeVisible();
  await expect.poll(async () => (await paintedContrast(target)).contrast).toBeGreaterThanOrEqual(4.5);
  const paint = await paintedContrast(target);
  expect(paint.images, "Do not ignore gradients when measuring contrast").toEqual([]);
  if (dark) expect(paint.luminance, "Dark cards keep a dark tinted surface").toBeLessThan(.25);
  return paint.background;
}

async function noHorizontalOverflow(page: Page) {
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(page.viewportSize()!.width);
}

async function resetPageScroll(page: Page) {
  await page.evaluate(() => window.scrollTo({ top: 0, left: 0, behavior: "instant" }));
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);
}

async function expectIdleContentExposed(page: Page, panel: Locator) {
  const instruction = panel.locator('[data-route-instruction="idle"]');
  const map = page.getByTestId("local-route-map");
  const bar = panel.locator(".route-apply-bar");
  await expect(instruction).toBeInViewport({ ratio: 1 });
  await expect(bar).toBeInViewport({ ratio: 1 });
  await expect.poll(async () => {
    const [mapBounds, barBounds] = await Promise.all([map.boundingBox(), bar.boundingBox()]);
    if (!mapBounds || !barBounds) return 0;
    return Math.min(mapBounds.y + mapBounds.height, barBounds.y, page.viewportSize()!.height) - Math.max(mapBounds.y, 0);
  }, { message: "A useful portion of the actual map must be on screen above the apply bar without scrolling" }).toBeGreaterThanOrEqual(80);
  const barBounds = (await bar.boundingBox())!;
  const schematicNotice = panel.locator(".route-map-schematic-notice");
  await expect(schematicNotice).toBeInViewport({ ratio: 1 });
  const noticeBounds = (await schematicNotice.boundingBox())!;
  expect(noticeBounds.y + noticeBounds.height, "The schematic disclaimer must remain above the fixed apply bar").toBeLessThanOrEqual(barBounds.y);
  const instructionBounds = (await instruction.boundingBox())!;
  expect(instructionBounds.y + instructionBounds.height, "The instruction must not sit behind the fixed apply bar").toBeLessThanOrEqual(barBounds.y);
  expect(await instruction.evaluate((element) => {
    const bounds = element.getBoundingClientRect();
    return element.contains(document.elementFromPoint(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2));
  }), "The initial instruction is not occluded by another overlay").toBe(true);
  expect(await map.evaluate((element, bottom) => {
    const bounds = element.getBoundingClientRect();
    const top = Math.max(bounds.y, 0);
    const visibleBottom = Math.min(bounds.bottom, bottom, window.innerHeight);
    const hit = document.elementFromPoint(bounds.x + bounds.width / 2, (top + visibleBottom) / 2);
    return Boolean(hit?.closest(".route-map-frame"));
  }, barBounds.y), "The visible map area is not hidden behind another panel").toBe(true);
}

for (const locale of locales) {
  test(`${locale}: role colors remain distinct, readable and labelled in both themes`, async ({ page }, info) => {
    if (info.project.name === "mobile-chromium") await page.setViewportSize({ width: 390, height: 844 });
    await page.emulateMedia({ reducedMotion: "reduce" });
    const state = await workspace(page, locale);
    for (const mode of ["light", "dark"] as const) {
      await theme(page, mode);
      const backgrounds: string[] = [];
      for (const tone of tones) {
        const stop = page.locator(`.premium-optional-stop[data-stop-tone="${tone}"]`).first();
        const summary = stop.locator(":scope > summary");
        const roleLabel = tone === "hotel" ? messages[locale].systemStop.hotelStart : messages[locale].editor.slot[tone];
        await expect(stop).not.toHaveAttribute("open", "");
        await expect(summary.getByText(roleLabel, { exact: true })).toBeVisible();
        backgrounds.push(await readable(summary.locator("strong"), mode === "dark"));
        await readable(summary.locator("small"), mode === "dark");
        expect((await summary.boundingBox())!.height).toBeGreaterThanOrEqual(44);
        await summary.click();
        const card = stop.locator(`.planner-system-card[data-stop-tone="${tone}"]`);
        await expect(card.getByText(roleLabel, { exact: true })).toBeVisible();
        await readable(card.getByRole("heading"), mode === "dark");
        for (const paragraph of await card.locator("p").all()) await readable(paragraph, mode === "dark");
        await expect(card.getByRole("button").first()).toBeVisible();
        await summary.click();
      }
      expect(new Set(backgrounds).size, "Hotel, lunch and dinner have three distinct painted surfaces").toBe(3);
      await noHorizontalOverflow(page);
      if (locale === "zh-TW") {
        await resetPageScroll(page);
        await page.screenshot({ path: info.outputPath(`roles-${mode}.png`), fullPage: true });
        if (page.viewportSize()!.width < 600) await page.screenshot({ path: info.outputPath(`roles-first-screen-${mode}.png`) });
      }
    }
    expect(state.writes).toEqual([]);
    expect(state.previews).toEqual([]);
    expect(state.unexpected).toEqual([]);
  });
}

test("unset and skipped arrangements retain role labels without misleading status colors", async ({ page }, info) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  const state = await workspace(page, "zh-TW", true);
  await page.locator(".calm-optional-arrangements > summary").click();
  for (const mode of ["light", "dark"] as const) {
    await theme(page, mode);
    for (const tone of tones) {
      const entry = page.locator(`.calm-optional-entry[data-stop-tone="${tone}"]`).first();
      await readable(entry, mode === "dark");
      expect((await entry.boundingBox())!.height).toBeGreaterThanOrEqual(44);
    }
    const skipped = page.locator('.calm-optional-entry[data-stop-tone="dinner"]');
    await expect(skipped).toHaveAttribute("data-stop-skipped", "true");
    await expect(page.getByRole("button", { name: "恢復用餐", exact: true })).toBeVisible();
    await noHorizontalOverflow(page);
    await resetPageScroll(page);
    await page.screenshot({ path: info.outputPath(`optional-390-${mode}.png`), fullPage: true });
  }
  expect(state.writes).toEqual([]);
  expect(state.previews).toEqual([]);
  expect(state.unexpected).toEqual([]);
});

for (const width of [390, 920, 1280]) {
  test(`${width}px daily route search/apply keeps the saved walk and buffer after parent remount`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 844 });
    await page.emulateMedia({ reducedMotion: "reduce" });
    const state = await workspace(page);
    await theme(page, "dark");
    await page.locator(".premium-day-settings > summary").click();
    await page.locator(".route-day-settings").getByRole("button", { name: "查詢路線", exact: true }).click();
    const panel = page.locator(".route-panel-layout");
    await expect(panel).toHaveAttribute("data-route-state", "idle");
    await expect(page.getByTestId("local-route-map")).toBeVisible();
    await expect(panel.locator(".route-empty-state")).toHaveCount(0);
    await expect(panel.locator('[data-route-instruction="idle"]')).toHaveCount(1);
    await expect(panel.locator('[data-route-instruction="idle"]')).toBeVisible();
    await expect(panel).not.toContainText("Provider");
    const modes = panel.locator(".route-panel-modes");
    const panelBounds = (await panel.boundingBox())!;
    const modesBounds = (await modes.boundingBox())!;
    expect(modesBounds.width, "An inline-size container must not collapse the transport controls").toBeGreaterThanOrEqual(240);
    if (width === 1280) {
      // A desktop viewport still presents a narrow drawer. Legacy desktop grid
      // alignment must not shrink its newer single-column flex children.
      expect(panelBounds.width).toBeLessThan(768);
      expect(modesBounds.width).toBeGreaterThanOrEqual(panelBounds.width - 2);
    }
    for (const tab of await modes.getByRole("tab").all()) {
      const bounds = (await tab.boundingBox())!;
      expect(bounds.width).toBeGreaterThanOrEqual(44);
      expect(bounds.height).toBeGreaterThanOrEqual(44);
    }
    expect(state.previews).toEqual([]);
    expect(state.writes).toEqual([]);
    const query = panel.getByRole("button", { name: dayTimelineCopy("zh-TW").query, exact: true });
    await expect(query).toBeInViewport();
    expect((await query.boundingBox())!.height).toBeGreaterThanOrEqual(44);
    await expectIdleContentExposed(page, panel);
    await noHorizontalOverflow(page);
    await page.screenshot({ path: info.outputPath(`route-idle-${width}-fixture-map.png`) });
    await panel.getByRole("tab", { name: "汽車", exact: true }).click();
    await expect(panel.getByRole("tab", { name: "汽車", exact: true })).toHaveAttribute("aria-selected", "true");
    expect(state.previews).toEqual([]);
    expect(state.writes).toEqual([]);
    await panel.getByRole("tab", { name: "步行", exact: true }).click();
    await expect(panel.getByRole("tab", { name: "步行", exact: true })).toHaveAttribute("aria-selected", "true");
    await panel.locator(".route-advanced-settings > summary").click();
    await panel.getByRole("combobox").selectOption("15");
    expect(state.previews).toEqual([]);
    expect(state.writes).toEqual([]);
    await query.click();
    await expect(panel).toHaveAttribute("data-route-state", "preview");
    expect(state.previews).toHaveLength(1);
    expect(state.previews[0]).toMatchObject({ version: 1, travel_mode: "walk", buffer_minutes: 15 });
    expect(state.current().version).toBe(1);
    expect(state.writes).toEqual([]);
    await panel.getByRole("button", { name: "套用此路線", exact: true }).click();
    await expect(panel).toHaveAttribute("data-route-state", "applied");
    await expect(panel.getByRole("tab", { name: "步行", exact: true })).toHaveAttribute("aria-selected", "true");
    await panel.locator(".route-advanced-settings > summary").click();
    await expect(panel.getByRole("combobox")).toHaveValue("15");
    expect(state.current().version).toBe(2);
    expect(state.writes).toHaveLength(1);
    expect(state.writes[0].body).toMatchObject({ source: "provider", version: 1, preview_id: "fixture-walk-15" });
    expect(state.previews).toHaveLength(1);
    expect(state.unexpected).toEqual([]);
    await noHorizontalOverflow(page);
    await page.screenshot({ path: info.outputPath(`route-applied-${width}-fixture-map.png`) });
  });
}
