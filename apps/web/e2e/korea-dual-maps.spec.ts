import { expect, test, type Page } from "@playwright/test";
import type { RouteExternalNavigation, RouteSegment, TravelMode, Trip } from "../lib/trip-types";
import { editorFixture } from "./fixtures/itinerary-editor";
import { pretendSignedIn } from "./session";

// These labelled SDK and API fixtures verify the UI contract, not live provider coverage.
async function koreanWorkspace(page: Page, city: "首爾" | "釜山") {
  let trip: Trip = structuredClone(editorFixture);
  trip = { ...trip, destination_country_code: "KR", timezone: "Asia/Seoul", name: `${city}雙地圖測試`, end_date: trip.start_date, route_segments: [], items: trip.items.filter((item) => item.day_date === trip.start_date) };
  const names = city === "首爾" ? ["首爾飯店 서울 호텔", "景福宮 경복궁", "北村韓屋村 북촌한옥마을"] : ["釜山飯店 부산 호텔", "海雲臺 해운대", "海東龍宮寺 해동용궁사"];
  trip.items = trip.items.map((item, index) => ({ ...item, title: names[index % names.length], location_name: names[index % names.length], latitude: (city === "首爾" ? 37.57 : 35.16) + index * .002, longitude: (city === "首爾" ? 126.97 : 129.16) + index * .002 }));
  trip.routing = { status: "idle", total: 4, completed: 0, day_settings: [{ day_date: trip.start_date!, default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: false }] };
  const previews: Array<Record<string, unknown>> = [];
  const writes: Array<Record<string, unknown>> = [];
  const unexpected: string[] = [];
  const navigationReads: string[] = [];
  let segment: RouteSegment | undefined;
  const navigations = (mode: TravelMode): RouteExternalNavigation[] => {
    const links: RouteExternalNavigation[] = [
    { provider: "naver_maps", label: "NAVER Maps", travel_mode: mode, web_url: `https://map.naver.com/p/directions/fixture/${mode}`, app_url: `nmap://route/${mode === "transit" ? "public" : mode}` },
    ...(mode === "drive" ? [] : [{ provider: "google_maps" as const, label: "Google Maps", travel_mode: mode, web_url: `https://www.google.com/maps/dir/?api=1&travelmode=${mode === "walk" ? "walking" : "transit"}`, app_url: "https://www.google.com/maps/dir/?api=1" }]),
    ];
    return mode === "transit" ? links.reverse() : links;
  };
  await pretendSignedIn(page);
  await page.addInitScript(() => {
    const render = (element: HTMLElement, provider: string) => {
      element.textContent = `${provider} local SDK fixture`;
      element.style.background = "#dce8ec";
      element.style.color = "#243d44";
      element.style.padding = "24px";
    };
    class GoogleMap { constructor(element: HTMLElement) { render(element, "Google"); } fitBounds() {} }
    class NaverMap { constructor(element: HTMLElement) { render(element, "NAVER"); } fitBounds() {} destroy() {} }
    class Overlay { setMap() {} addListener() {} }
    class Bounds { extend() {} }
    class Point {}
    Object.assign(window, {
      google: { maps: { Map: GoogleMap, Marker: Overlay, Polyline: Overlay, LatLngBounds: Bounds, event: { clearInstanceListeners() {} } } },
      naver: { maps: { Map: NaverMap, Marker: Overlay, Polyline: Overlay, LatLng: Point, LatLngBounds: Bounds, Event: { addListener() {}, clearInstanceListeners() {} } } },
    });
  });
  await page.route("**/*", (route) => {
    const url = new URL(route.request().url());
    if (["localhost", "127.0.0.1"].includes(url.hostname)) return route.continue();
    if (url.hostname === "oapi.map.naver.com" && url.pathname === "/openapi/v3/maps.js") return route.fulfill({ contentType: "application/javascript", body: "/* Labelled local SDK fixture installed before hydration. */" });
    unexpected.push(url.origin);
    return route.abort();
  });
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    const path = url.pathname;
    if (path.endsWith("/auth/me")) return route.fulfill({ json: { id: "korea-map-fixture", email: "korea@example.test", role: "user", is_active: true } });
    if (path.endsWith("/runtime/public-config")) return route.fulfill({ json: { google_maps_browser_key: "fixture", google_maps_javascript_enabled: true, naver_maps_browser_client_id: "fixture", naver_dynamic_map_enabled: true, odsay_enabled: true } });
    if (path.endsWith("/routes/navigation")) {
      navigationReads.push(url.search);
      return route.fulfill({ json: { external_navigations: navigations(url.searchParams.get("travel_mode") as TravelMode) } });
    }
    if (path.endsWith("/routes/preview")) {
      const body = request.postDataJSON();
      previews.push(body);
      const links = navigations(body.travel_mode);
      if (body.travel_mode === "walk") return route.fulfill({ json: { kind: "external_only", preview_id: null, expires_at: null, segment: null, schedule_impact: null, external_navigations: links } });
      segment = { from_item_id: body.from_item_id, to_item_id: body.to_item_id, travel_mode: body.travel_mode, status: "complete", provider: body.travel_mode === "transit" ? "odsay" : "naver_maps", attribution: body.travel_mode === "transit" ? "ODsay" : "NAVER Maps", duration_minutes: 24, buffer_minutes: body.buffer_minutes, generated_at: "2026-09-10T00:00:00Z", schedule_mode: "preview", preference: "FEWER_TRANSFERS", encoded_polyline: null, steps: [], details_available: [], warnings: [], external_navigations: links };
      return route.fulfill({ json: { kind: "provider", preview_id: "korea-route-preview", expires_at: "2100-01-01T00:00:00Z", segment, external_navigations: links, schedule_impact: { affected_items: [], conflicts: [] } } });
    }
    if (path.endsWith("/routes/apply")) {
      const body = request.postDataJSON();
      writes.push(body);
      if (!segment) return route.fulfill({ status: 409, json: { detail: "No route fixture" } });
      trip = { ...trip, version: trip.version + 1, route_segments: [segment] };
      return route.fulfill({ json: trip });
    }
    if (path === "/api/travel/trips/intuitive-trip") return route.fulfill({ json: trip });
    if (path.endsWith("/health")) return route.fulfill({ json: { days: [], issues: [] } });
    if (/\/community\/status$|\/discovery\/status$|\/analytics\/config$/.test(path)) return route.fulfill({ json: { enabled: false } });
    if (path.endsWith("/usage")) return route.fulfill({ json: {} });
    if (/\/saved-items$|\/trips$/.test(path)) return route.fulfill({ json: [] });
    unexpected.push(`${request.method()} ${path}`);
    return route.fulfill({ status: 503, json: { detail: "Unstubbed request" } });
  });
  await page.goto("/zh-TW/trips/intuitive-trip");
  await expect(page.getByRole("heading", { name: trip.name })).toBeVisible();
  await page.locator(".premium-day-settings > summary").click();
  await page.locator(".route-day-settings").getByRole("button", { name: "查詢路線", exact: true }).click();
  return { previews, writes, navigationReads, unexpected, current: () => trip };
}

for (const { width, city } of [{ width: 390, city: "首爾" }, { width: 1280, city: "釜山" }] as const) {
  test(`${width}px ${city} separates map selection, external navigation and applicable time`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 844 });
    const state = await koreanWorkspace(page, city);
    const panel = page.locator(".route-panel-layout");
    await expect(panel.locator(".route-endpoints")).toContainText(city === "首爾" ? "서울" : "부산");
    await expect(panel.locator('[data-map-provider="google_maps"]')).toBeVisible();
    await expect(panel.getByRole("link", { name: "用 NAVER Maps 導航", exact: true })).toBeVisible();
    await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toBeVisible();
    await panel.getByRole("button", { name: "查詢交通方案", exact: true }).click();
    await expect(panel.getByText("交通時間來源：ODsay")).toBeVisible();
    await expect(panel.getByRole("button", { name: "套用此路線", exact: true })).toBeEnabled();
    expect(state.current().version).toBe(1);
    await panel.getByRole("tab", { name: "步行", exact: true }).click();
    const selector = panel.getByRole("combobox", { name: "顯示地圖", exact: true });
    await expect(selector).toHaveValue("naver_maps");
    await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toHaveAttribute("href", /travelmode=walking/);
    const navigationCount = state.navigationReads.length;
    await selector.selectOption("google_maps");
    await expect(panel.locator('[data-map-provider="google_maps"]')).toBeVisible();
    await selector.selectOption("naver_maps");
    await expect(panel.locator('[data-map-provider="naver_maps"]')).toBeVisible();
    expect(state.navigationReads).toHaveLength(navigationCount);
    expect(state.previews).toHaveLength(1);
    expect(state.writes).toEqual([]);
    await panel.getByRole("button", { name: "查詢交通方案", exact: true }).click();
    await expect(panel.getByRole("button", { name: "外部導航，無法套用", exact: true })).toBeDisabled();
    await expect(panel.getByRole("link", { name: "用 Google Maps 規劃", exact: true })).toBeVisible();
    await expect(panel.locator(".route-apply-selection")).not.toContainText("分鐘");
    const disclaimer = panel.getByText("示意連線，非實際路線", { exact: true });
    await expect(disclaimer).toBeInViewport();
    expect((await disclaimer.boundingBox())!.y + (await disclaimer.boundingBox())!.height).toBeLessThan((await panel.locator(".route-apply-bar").boundingBox())!.y);
    await page.screenshot({ path: info.outputPath(`korea-walking-${width}-fixture.png`) });
    await panel.getByRole("tab", { name: "汽車", exact: true }).click();
    await expect(panel.locator('[data-map-provider="naver_maps"]')).toBeVisible();
    await expect(selector).toHaveCount(0);
    await expect(panel.getByRole("link", { name: "用 NAVER Maps 導航", exact: true })).toHaveAttribute("href", /drive/);
    await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toHaveCount(0);
    expect(state.previews).toHaveLength(2);
    expect(state.writes).toEqual([]);
    expect(state.current().version).toBe(1);
    expect(state.unexpected).toEqual([]);
    expect(await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)).toBe(false);
  });
}
