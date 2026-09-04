import { expect, test } from "@playwright/test";

const tripId = "stay-trip";
const future = () => new Date(Date.now() + 10 * 60_000).toISOString();

const baseItem = {
  id: "00000000-0000-4000-8000-000000000002",
  item_type: "activity",
  day_date: "2026-11-11",
  position: 0,
  title: "淺草散步",
  location_name: "淺草寺",
  latitude: 35.7148,
  longitude: 139.7967,
  location_source: "hotspot_catalog",
  locked: false,
  is_estimated: false,
  data: { needs_place_confirmation: false },
};
const hotelStart = {
  ...baseItem,
  id: "00000000-0000-4000-8000-000000000010",
  position: -1,
  item_type: "hotel_anchor",
  title: "從 尚未設定飯店 出發",
  location_name: null,
  latitude: null,
  longitude: null,
  location_source: null,
  system_role: "hotel_start",
  fixed_time: true,
  data: { needs_place_confirmation: true },
};
const trip = {
  id: tripId,
  name: "東京兩日",
  mode: "manual",
  total_price: 0,
  currency: "TWD",
  data: {},
  version: 1,
  destination_name: "東京",
  start_date: "2026-11-11",
  end_date: "2026-11-12",
  timezone: "Asia/Tokyo",
  route_preference: "FEWER_TRANSFERS",
  primary_lodging: null,
  share_enabled: false,
  items: [baseItem, hotelStart],
  route_segments: [],
  routing: { status: "idle", total: 0, completed: 0, warnings: [], day_settings: [] },
};
const chosenTrip = {
  ...trip,
  version: 2,
  primary_lodging: { name: "淺草河畔飯店", location_name: "台東區淺草 1-1", latitude: 35.71, longitude: 139.79, location_source: "provider", selection_source: "user" },
  items: [baseItem, { ...hotelStart, title: "從 淺草河畔飯店 出發", location_name: "台東區淺草 1-1", latitude: 35.71, longitude: 139.79, location_source: "provider", data: { needs_place_confirmation: false } }],
  routing: { status: "complete", total: 1, completed: 1, warnings: [], day_settings: [] },
};
const areas = {
  trip_id: tripId,
  version: 1,
  status: "recommended",
  city_code: "NRT",
  pricing: { available: true, provider: "booking", mode: "live", message: null },
  current_lodging_area_code: null,
  located_item_count: 1,
  unassigned_item_count: 0,
  excluded_extension: {},
  warnings: [],
  areas: [
    { code: "asakusa", name: "淺草", latitude: 35.71, longitude: 139.79, radius_km: 2, is_day_trip: false, score: 0.9, item_count: 1, dwell_minutes: 60, day_count: 1, sample_titles: ["淺草散步"], reasons: ["most_items"] },
    { code: "shinjuku", name: "新宿", latitude: 35.69, longitude: 139.7, radius_km: 2, is_day_trip: false, score: 0.3, item_count: 0, dwell_minutes: 0, day_count: 0, sample_titles: [], reasons: ["central"] },
  ],
};
const hotels = {
  trip_id: tripId,
  version: 1,
  area: { code: "asakusa", name: "淺草", latitude: 35.71, longitude: 139.79, radius_km: 2 },
  check_in: "2026-11-11",
  check_out: "2026-11-12",
  nights: 1,
  date_notes: [],
  travelers: { adults: 1, children: 0, rooms: 1 },
  warnings: [],
  pricing: { status: "live", provider: "booking", message: null, expires_at: future(), cached: false },
  filters: { applied: {}, relaxed: [], excluded_by_hard_filter: 0 },
  hotels: [
    { id: "offer-1", hotel_id: "100", hotel_name: "淺草河畔飯店", provider: "booking", latitude: 35.71, longitude: 139.79, currency: "TWD", nights: 1, nightly_price: 3200, total_price: 3200, rating: 4, review_score: 8.6, review_count: 1200, breakfast_included: true, refundable: true, distance_km: 0.4, in_area: true, is_current_lodging: false, preference_gaps: [], partners: [{ partner: "agoda", display_name: "Agoda", kind: "hotel_search" }, { partner: "booking", display_name: "Booking.com", kind: "deep_link" }], expires_at: future() },
    { id: "offer-2", hotel_id: "200", hotel_name: "淺草景觀飯店", provider: "booking", latitude: 35.712, longitude: 139.79, currency: "TWD", nights: 1, nightly_price: 5200, total_price: 5200, rating: 5, review_score: 9.1, review_count: 800, breakfast_included: true, refundable: false, distance_km: 0.6, in_area: true, is_current_lodging: false, preference_gaps: [], partners: [{ partner: "agoda", display_name: "Agoda", kind: "hotel_search" }], expires_at: future() },
  ],
  nearby: [],
  area_partners: [{ partner: "agoda", display_name: "Agoda", kind: "area_search" }],
  disclosure: "透過合作連結預訂，本站可能獲得分潤，價格不因此增加。",
};

test.beforeEach(async ({ page }) => {
  await page.route("**/api/travel/auth/me", (route) => route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ id: "00000000-0000-4000-8000-000000000001", email: "tester@example.com" }),
  }));
  await page.route("**/api/travel/runtime/public-config", (route) => route.fulfill({ status: 200, contentType: "application/json", body: "{}" }));
  await page.route("**/api/travel/affiliates/options**", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ options: [] }) }));
  let selected = false;
  await page.route(`**/api/travel/trips/${tripId}**`, async (route) => {
    const url = new URL(route.request().url());
    const json = (body: unknown) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(body) });
    if (url.pathname.endsWith("/stay-areas/asakusa/select")) {
      selected = true;
      return json(chosenTrip);
    }
    if (url.pathname.endsWith("/stay-areas/asakusa/hotels")) return json(hotels);
    if (url.pathname.endsWith("/stay-areas")) return json(areas);
    if (url.pathname.endsWith("/routes/status")) return json({ version: selected ? 2 : 1, status: selected ? "complete" : "idle" });
    if (url.pathname.endsWith(`/trips/${tripId}`)) return json(selected ? chosenTrip : trip);
    return route.fulfill({ status: 404, contentType: "application/json", body: JSON.stringify({ code: "not_found" }) });
  });
});

test("recommends stay areas, compares prices and sets the chosen hotel as primary lodging", async ({ page }) => {
  await page.goto(`/zh-TW/trips/${tripId}`);
  await page.getByRole("button", { name: "設定主要飯店" }).first().click();

  const dialog = page.getByRole("dialog", { name: "住宿熱區" });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByText("淺草", { exact: true })).toBeVisible();
  await expect(dialog.getByText("景點最多")).toBeVisible();
  await dialog.getByRole("button", { name: /看這區的飯店/ }).first().click();

  await expect(dialog.getByText("淺草河畔飯店")).toBeVisible();
  await expect(dialog.getByText("NT$3,200")).toBeVisible();
  const agoda = dialog.getByRole("button", { name: "在 Agoda 搜尋此飯店" }).first();
  await expect(agoda).toBeVisible();
  await expect(agoda.locator("xpath=ancestor::form")).toHaveAttribute("action", `/api/travel/trips/${tripId}/stay-areas/asakusa/clickout?partner=agoda&hotel_id=100`);
  await expect(dialog.locator("a[href*='agoda.com'], a[href*='booking.com']")).toHaveCount(0);

  await dialog.getByRole("button", { name: "設為主要飯店" }).first().click();

  await expect(page.getByText("已將 淺草河畔飯店 設為主要飯店，正在重新計算每日路線。")).toBeVisible();
  await expect(page.getByRole("dialog", { name: "住宿熱區" })).toHaveCount(0);
  await expect(page.getByText("從 淺草河畔飯店 出發")).toBeVisible();
});
