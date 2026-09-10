import { expect, test, type Locator, type Page } from "@playwright/test";
import type { RouteExternalNavigation, RouteMapCapabilities, RouteSegment, TravelMode, Trip } from "../lib/trip-types";
import { editorFixture } from "./fixtures/itinerary-editor";
import { pretendSignedIn } from "./session";

const mapSummary = "查看地圖（起終點參考）";
const googleSteps: RouteSegment["steps"] = [
  { travel_mode: "WALK", instruction: "步行至景福宮站 4 號出口（合成測試資料）", duration_minutes: 4, distance_meters: 280 },
  { travel_mode: "TRANSIT", instruction: "搭乘地鐵 3 號線（合成測試資料）", duration_minutes: 10,
    departure_stop: "景福宮站 경복궁역", arrival_stop: "安國站 안국역", departure_time: "2026-11-11T00:04:00Z", arrival_time: "2026-11-11T00:14:00Z",
    line_name: "首爾地鐵 3 號線", line_short_name: "3 號線", line_color: "#EF7C1C", headsign: "大化 대화", stop_count: 3, platform: "2" },
  { travel_mode: "TRANSIT", instruction: "轉乘綠色公車 11 號（合成測試資料）", duration_minutes: 6,
    departure_stop: "安國站公車站 안국역", arrival_stop: "北村入口 북촌입구", departure_time: "2026-11-11T00:14:00Z", arrival_time: "2026-11-11T00:20:00Z",
    line_name: "綠色公車 11 號", line_short_name: "11", line_color: "#42A54A", headsign: "北村 북촌", stop_count: 2, exit_name: "3", recommended_car: "前車廂" },
  { travel_mode: "WALK", instruction: "步行抵達北村韓屋村（合成測試資料）", duration_minutes: 4, distance_meters: 250 },
];

// These labelled SDK and API fixtures verify the UI contract, not live provider coverage.
async function koreanWorkspace(page: Page, city: "首爾" | "釜山", transitProvider: "odsay" | "google_routes" = "odsay") {
  let trip: Trip = structuredClone(editorFixture);
  trip = { ...trip, destination_name: city, destination_country_code: "KR", timezone: "Asia/Seoul", name: `${city}雙地圖測試`, end_date: trip.start_date, route_segments: [], items: trip.items.filter((item) => item.day_date === trip.start_date) };
  const names = city === "首爾" ? ["首爾飯店 서울 호텔", "景福宮 경복궁", "北村韓屋村 북촌한옥마을"] : ["釜山飯店 부산 호텔", "海雲臺 해운대", "海東龍宮寺 해동용궁사"];
  trip.items = trip.items.map((item, index) => ({ ...item, title: names[index % names.length], location_name: names[index % names.length], latitude: (city === "首爾" ? 37.57 : 35.16) + index * .002, longitude: (city === "首爾" ? 126.97 : 129.16) + index * .002 }));
  trip.routing = { status: "idle", total: 4, completed: 0, day_settings: [{ day_date: trip.start_date!, default_travel_mode: "transit", default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS", auto_compute: false }] };
  const previews: Array<Record<string, unknown>> = [];
  const writes: Array<Record<string, unknown>> = [];
  const unexpected: string[] = [];
  const errors: string[] = [];
  const navigationReads: string[] = [];
  const previewSegments = new Map<string, RouteSegment>();
  const mapCapabilities = (mode: TravelMode): RouteMapCapabilities => ({
    providers: mode === "walk" ? ["naver_maps", "google_maps"] : [mode === "transit" ? "google_maps" : "naver_maps"],
    default_provider: mode === "transit" ? "google_maps" : "naver_maps",
  });
  const navigations = (mode: TravelMode): RouteExternalNavigation[] => {
    const links: RouteExternalNavigation[] = [
    { provider: "naver_maps", label: "NAVER Maps", travel_mode: mode, web_url: `https://map.naver.com/p/directions/fixture/${mode}`, app_url: `nmap://route/${mode === "transit" ? "public" : mode}` },
    ...(mode === "drive" ? [] : [{ provider: "google_maps" as const, label: "Google Maps", travel_mode: mode, web_url: `https://www.google.com/maps/dir/?api=1&travelmode=${mode === "walk" ? "walking" : "transit"}`, app_url: "https://www.google.com/maps/dir/?api=1" }]),
    ];
    return mode === "transit" ? links.reverse() : links;
  };
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });
  page.on("response", (response) => {
    const url = new URL(response.url());
    if (["localhost", "127.0.0.1"].includes(url.hostname) && response.status() >= 400) errors.push(`${response.status()} ${url.pathname}`);
  });
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
    if (path.endsWith("/runtime/public-config")) return route.fulfill({ json: { google_maps_browser_key: "fixture", google_maps_javascript_enabled: true, naver_maps_browser_client_id: "fixture", naver_dynamic_map_enabled: true, odsay_enabled: transitProvider === "odsay" } });
    if (path.endsWith("/routes/navigation")) {
      navigationReads.push(url.search);
      const mode = url.searchParams.get("travel_mode") as TravelMode;
      return route.fulfill({ json: { external_navigations: navigations(mode), map_capabilities: mapCapabilities(mode),
        route_availability: { status: mode === "walk" ? "external_only" : "available", provider: mode === "walk" ? null : mode === "transit" ? transitProvider : "naver_maps", can_query: mode !== "walk" } } });
    }
    if (path.endsWith("/routes/preview")) {
      const body = request.postDataJSON();
      previews.push(body);
      if (body.travel_mode === "walk") {
        unexpected.push("Unsupported Korean walking preview POST");
        return route.fulfill({ status: 422, json: { detail: "Walking must use read-only navigation, not a timing query" } });
      }
      const mode = body.travel_mode as TravelMode;
      const links = navigations(mode);
      const departure = new Date(`${trip.start_date}T00:00:00Z`);
      const arrival = new Date(departure.getTime() + 24 * 60_000);
      const ready = new Date(arrival.getTime() + body.buffer_minutes * 60_000);
      const provider = mode === "transit" ? transitProvider : "naver_maps";
      const segment: RouteSegment = { from_item_id: body.from_item_id, to_item_id: body.to_item_id, travel_mode: mode, status: "complete", provider, attribution: provider === "odsay" ? "ODsay" : provider === "google_routes" ? "Google Maps" : "NAVER Maps", duration_minutes: 24, buffer_minutes: body.buffer_minutes, departure_time: departure.toISOString(), arrival_time: arrival.toISOString(), ready_time: ready.toISOString(), generated_at: "2026-09-10T00:00:00Z", expires_at: "2100-01-01T00:00:00Z", schedule_mode: "preview", preference: "FEWER_TRANSFERS", encoded_polyline: null, distance_meters: 3200, fare: 1550, currency: "KRW", steps: provider === "google_routes" ? googleSteps : [], details_available: provider === "google_routes" ? ["line", "platform", "exit", "recommended_car"] : [], warnings: ["合成測試資料；不代表真實班次、路線或票價。"], external_navigations: links, map_capabilities: mapCapabilities(mode) };
      const previewId = `korea-route-preview-${previews.length}`;
      previewSegments.set(previewId, segment);
      return route.fulfill({ json: { kind: "provider", preview_id: previewId, expires_at: "2100-01-01T00:00:00Z", segment, external_navigations: links, map_capabilities: mapCapabilities(mode), schedule_impact: { affected_items: [{ item_id: body.to_item_id, title: trip.items.find((item) => item.id === body.to_item_id)?.title, old_start_time: `${trip.start_date}T09:00:00`, new_start_time: ready.toISOString(), delta_minutes: 24 + body.buffer_minutes, fixed_time: false }], conflicts: [] } } });
    }
    if (path.endsWith("/routes/apply")) {
      const body = request.postDataJSON();
      writes.push(body);
      const segment = previewSegments.get(body.preview_id);
      if (!segment || body.version !== trip.version || !request.headers()["idempotency-key"]) return route.fulfill({ status: 409, json: { detail: "Invalid preview, version or missing idempotency fixture" } });
      trip = { ...trip, version: trip.version + 1, route_segments: [{ ...segment, is_override: !body.inherit_day_default }],
        items: trip.items.map((item) => item.id === segment.to_item_id && !item.fixed_time ? { ...item, start_time: segment.ready_time } : item) };
      return route.fulfill({ json: trip });
    }
    if (path === "/api/travel/trips/intuitive-trip" && request.method() === "GET") return route.fulfill({ json: trip });
    if (path.endsWith("/health")) return route.fulfill({ json: { days: [], issues: [] } });
    if (/\/community\/status$|\/discovery\/status$|\/analytics\/config$/.test(path)) return route.fulfill({ json: { enabled: false } });
    if (path.endsWith("/usage")) return route.fulfill({ json: {} });
    if (/\/saved-items$|\/trips$/.test(path)) return route.fulfill({ json: [] });
    unexpected.push(`${request.method()} ${path}`);
    return route.fulfill({ status: 503, json: { detail: "Unstubbed request" } });
  });
  await page.goto("/zh-TW/trips/intuitive-trip");
  await expect(page.getByRole("heading", { name: trip.name })).toBeVisible();
  await expect(page.locator(".calm-connection").getByText("尚未查詢", { exact: true })).toHaveCount(4);
  await page.locator(".premium-day-settings > summary").click();
  await page.locator(".route-day-settings").getByRole("button", { name: "查詢路線", exact: true }).click();
  return { previews, writes, navigationReads, unexpected, errors, current: () => trip };
}

async function assertContained(page: Page, panel: Locator) {
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
  expect(await panel.evaluate((element) => element.scrollWidth <= element.clientWidth)).toBe(true);
  expect(await page.getByRole("dialog").evaluate((element) => element.scrollWidth <= element.clientWidth)).toBe(true);
}

for (const city of ["首爾", "釜山"] as const) {
  test(`${city} separates map selection, external navigation and applicable time`, async ({ page }, info) => {
    const width = info.project.name === "mobile-chromium" ? 412 : 1464;
    await page.setViewportSize({ width, height: 915 });
    const state = await koreanWorkspace(page, city);
    const panel = page.locator(".route-panel-layout");
    const map = panel.locator(".route-panel-map");
    await expect(panel.locator(".route-endpoints")).toContainText(city === "首爾" ? "서울" : "부산");
    await expect(map).not.toHaveAttribute("open", "");
    await expect(panel.locator("[data-map-provider]")).toHaveCount(0);
    await expect(panel.getByRole("link", { name: "用 NAVER Maps 導航", exact: true })).toBeVisible();
    await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toBeVisible();
    expect(state.previews).toEqual([]);
    await panel.getByRole("button", { name: "查詢交通方案", exact: true }).click();
    await expect(panel.locator(".route-panel-detail").getByText("交通時間來源：ODsay")).toBeVisible();
    await expect(panel.getByRole("button", { name: "套用此路線", exact: true })).toBeEnabled();
    expect(state.current().version).toBe(1);
    await map.getByText(mapSummary, { exact: true }).click();
    await expect(panel.locator('[data-map-provider="google_maps"]')).toBeVisible();
    await expect(panel.locator(".route-panel-detail").getByText("交通時間來源：ODsay")).toBeVisible();
    await panel.getByRole("tab", { name: "步行", exact: true }).click();
    const selector = panel.getByRole("combobox", { name: "顯示地圖", exact: true });
    await expect(selector).toHaveValue("naver_maps");
    await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toHaveAttribute("href", /travelmode=walking/);
    await expect(panel.getByRole("button", { name: "查詢交通方案", exact: true })).toHaveCount(0);
    await expect(panel.getByRole("button", { name: "套用此路線", exact: true })).toHaveCount(0);
    await expect(panel.locator(".route-apply-bar").getByRole("link", { name: "前往 NAVER Maps 查看（離開本站）", exact: true })).toBeVisible();
    const navigationCount = state.navigationReads.length;
    await selector.selectOption("google_maps");
    await expect(panel.locator('[data-map-provider="google_maps"]')).toBeVisible();
    const frameHeight = (await panel.locator(".route-map-frame").boundingBox())!.height;
    await selector.selectOption("naver_maps");
    await expect(panel.locator('[data-map-provider="naver_maps"]')).toBeVisible();
    expect((await panel.locator(".route-map-frame").boundingBox())!.height).toBe(frameHeight);
    expect(state.navigationReads).toHaveLength(navigationCount);
    expect(state.previews).toHaveLength(1);
    expect(state.writes).toEqual([]);
    await expect(panel.locator(".route-apply-selection")).not.toContainText("分鐘");
    await expect(panel.locator(".route-availability-notice")).toContainText("本站未取得可套用的交通時間");
    const manual = panel.getByRole("button", { name: "手動輸入時間", exact: true });
    await manual.click();
    await expect(panel.getByRole("spinbutton", { name: "移動分鐘", exact: true })).toHaveValue("");
    await expect(panel.getByRole("spinbutton", { name: "移動分鐘", exact: true })).toBeFocused();
    await expect(panel.getByRole("button", { name: "套用手動時間", exact: true })).toBeDisabled();
    await panel.getByRole("button", { name: "取消自訂時間", exact: true }).click();
    await expect(manual).toBeFocused();
    expect(state.previews).toHaveLength(1);
    expect(state.writes).toEqual([]);
    await panel.locator(".route-map-frame").scrollIntoViewIfNeeded();
    const disclaimer = panel.getByText("示意連線，非實際路線", { exact: true });
    await expect(disclaimer).toBeInViewport();
    const disclaimerBox = (await disclaimer.boundingBox())!;
    expect(disclaimerBox.y + disclaimerBox.height).toBeLessThan((await panel.locator(".route-apply-bar").boundingBox())!.y);
    await assertContained(page, panel);
    await page.screenshot({ path: info.outputPath(`korea-walking-${city}-${width}-fixture.png`) });
    await panel.getByRole("tab", { name: "汽車", exact: true }).click();
    await expect(panel.locator('[data-map-provider="naver_maps"]')).toBeVisible();
    await expect(selector).toHaveCount(0);
    await expect(panel.getByRole("link", { name: "用 NAVER Maps 導航", exact: true })).toHaveAttribute("href", /drive/);
    await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toHaveCount(0);
    await expect(panel.getByRole("button", { name: "查詢交通方案", exact: true })).toBeEnabled();
    expect(state.previews).toHaveLength(1);
    expect(state.writes).toEqual([]);
    expect(state.current().version).toBe(1);
    await assertContained(page, panel);
    expect(state.unexpected).toEqual([]);
    expect(state.errors).toEqual([]);
  });
}

test("Google transit fixture shows detailed steps first and applies a 15-minute buffer only on confirmation", async ({ page }, info) => {
  const width = info.project.name === "mobile-chromium" ? 412 : 1464;
  await page.setViewportSize({ width, height: 915 });
  const state = await koreanWorkspace(page, "首爾", "google_routes");
  const before = structuredClone(state.current());
  const panel = page.locator(".route-panel-layout");
  const buffer = panel.getByRole("combobox", { name: "移動緩衝時間", exact: true });
  await expect(buffer).toBeVisible();
  await expect(buffer).toHaveValue("10");
  await expect(panel.locator("[data-map-provider]")).toHaveCount(0);
  await expect(panel.getByRole("link", { name: "用 Google Maps 導航", exact: true })).toBeVisible();
  await buffer.selectOption("15");
  expect(state.previews).toEqual([]);
  expect(state.writes).toEqual([]);
  expect(state.current()).toEqual(before);
  await panel.getByRole("button", { name: "查詢交通方案", exact: true }).click();
  await expect(panel.getByText("交通時間來源：Google Maps")).toBeVisible();
  await expect(panel.getByText("已取得方案，尚未套用", { exact: true })).toBeVisible();
  await expect(panel.locator(".route-panel-detail")).toBeFocused();
  await expect(panel.getByRole("listbox")).toHaveCount(0);
  const steps = panel.getByRole("list", { name: "詳細移動步驟", exact: true });
  await expect(steps.getByRole("listitem")).toHaveCount(4);
  await expect(steps.getByText("上車：景福宮站 경복궁역", { exact: true })).toBeVisible();
  await expect(steps.getByText("下車：安國站 안국역", { exact: true })).toBeVisible();
  await expect(steps.getByText("轉乘上車：安國站公車站 안국역", { exact: true })).toBeVisible();
  await expect(steps.getByText("下車：北村入口 북촌입구", { exact: true })).toBeVisible();
  await expect(steps.getByText("09:04 → 09:14", { exact: true })).toBeVisible();
  await expect(steps.getByText("09:14 → 09:20", { exact: true })).toBeVisible();
  await expect(panel.locator(".route-time-grid")).toContainText("09:00");
  await expect(panel.locator(".route-time-grid")).toContainText("09:24");
  await expect(panel.locator(".route-time-grid")).toContainText("09:39");
  await expect(panel.locator(".route-buffer-summary")).toContainText("＋15 分");
  await expect(panel.locator("[data-map-provider]")).toHaveCount(0);
  expect(await panel.locator(".route-panel-detail").evaluate((detail) => Boolean(detail.compareDocumentPosition(document.querySelector(".route-panel-map")!) & Node.DOCUMENT_POSITION_FOLLOWING))).toBe(true);
  expect(state.previews).toHaveLength(1);
  expect(state.previews[0]).toMatchObject({ version: 1, travel_mode: "transit", buffer_minutes: 15 });
  expect(state.writes).toEqual([]);
  expect(state.current()).toEqual(before);
  await assertContained(page, panel);
  await panel.locator(".route-panel-detail").scrollIntoViewIfNeeded();
  await page.screenshot({ path: info.outputPath(`korea-google-transit-${width}-fixture.png`) });
  await panel.getByRole("button", { name: "套用此路線", exact: true }).click();
  await expect(panel.getByRole("button", { name: "目前已套用", exact: true })).toBeDisabled();
  expect(state.writes).toHaveLength(1);
  expect(state.writes[0]).toMatchObject({ source: "provider", version: 1, preview_id: "korea-route-preview-1", inherit_day_default: false });
  expect(state.current().version).toBe(2);
  expect(state.current().route_segments?.[0]).toMatchObject({ provider: "google_routes", buffer_minutes: 15, ready_time: "2026-11-11T00:39:00.000Z" });
  await expect(buffer).toHaveValue("15");
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.locator(".route-day-settings").getByRole("button", { name: "查詢路線", exact: true })).toBeFocused();
  const connector = page.locator(".calm-connection").getByRole("button", { name: /24 分/ });
  await expect(connector).toContainText("＋緩衝 15 分");
  await expect(page.locator('[data-stop-id="asakusa"]')).toContainText("09:39");
  await page.reload();
  await expect(page.getByRole("heading", { name: state.current().name })).toBeVisible();
  await expect(connector).toContainText("＋緩衝 15 分");
  await connector.click();
  await expect(panel.getByText("交通時間來源：Google Maps")).toBeVisible();
  await expect(panel.getByRole("list", { name: "詳細移動步驟", exact: true }).getByRole("listitem")).toHaveCount(4);
  await expect(buffer).toHaveValue("15");
  await expect(panel.getByRole("button", { name: "目前已套用", exact: true })).toBeDisabled();
  expect(state.previews).toHaveLength(1);
  expect(state.writes).toHaveLength(1);
  await assertContained(page, panel);
  expect(state.unexpected).toEqual([]);
  expect(state.errors).toEqual([]);
});
