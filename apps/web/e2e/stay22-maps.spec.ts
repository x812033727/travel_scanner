import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";
import { pretendSignedIn } from "./session";
import type { Stay22Copy } from "../lib/stay22-copy";

const tripId = "stay22-pilot-test";
const mapContext = { destination_id: "tokyo", country_code: "JP", city_code: "NRT", check_in: "2099-11-11", check_out: "2099-11-15", travelers: { adults: 2, children: 1, rooms: 1 }, currency: "TWD" };
const area = { code: "asakusa", name: "Asakusa", latitude: 35.71, longitude: 139.79, radius_km: 2, is_day_trip: false, score: 1, item_count: 1, dwell_minutes: 60, day_count: 1, sample_titles: [], reasons: ["most_items"] };
const trip = {
  id: tripId, name: "Stay22 pilot private trip", mode: "manual", total_price: 0, currency: "TWD", data: {}, version: 1,
  destination_name: "東京", start_date: "2099-11-11", end_date: "2099-11-15", timezone: "Asia/Tokyo", route_preference: "FEWER_TRANSFERS",
  primary_lodging: null, share_enabled: false, items: [{
    id: "00000000-0000-4000-8000-000000000010", item_type: "hotel_anchor", day_date: "2099-11-11", position: -1,
    title: "Hotel departure", location_name: null, latitude: null, longitude: null, location_source: null,
    locked: false, is_estimated: false, system_role: "hotel_start", fixed_time: true, data: { needs_place_confirmation: true },
  }], route_segments: [],
  routing: { status: "idle", total: 0, completed: 0, warnings: [], day_settings: [] },
};

for (const { locale, width } of [
  ...["zh-TW", "zh-CN", "en", "ja", "ko"].map((locale) => ({ locale, width: 390 })),
  { locale: "en", width: 1280 },
]) {
  test(`${locale}: map is opt-in, contextual and leaves trip unchanged at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 844 });
    await pretendSignedIn(page);
    const externalRequests: string[] = [];
    const hotelRequests: string[] = [];
    const writes: string[] = [];
    await page.route("https://www.stay22.com/**", async (route) => {
      externalRequests.push(route.request().url());
      // No live provider calls or affiliate test traffic in CI; this tests our embedding boundary.
      await route.fulfill({ contentType: "text/html", body: "<!doctype html><html><body><main>External map test fixture</main></body></html>" });
    });
    await page.route("**/api/travel/**", async (route) => {
      const req = route.request();
      const path = new URL(req.url()).pathname.replace("/api/travel", "");
      if (!["GET", "HEAD"].includes(req.method()) && path.includes(`/trips/${tripId}`)) writes.push(path);
      if (path.includes("/hotels")) hotelRequests.push(path);
      let body: unknown = {};
      if (path === "/auth/me") body = { id: "00000000-0000-4000-8000-000000000001", email: "tester@example.com" };
      else if (path === `/trips/${tripId}`) body = trip;
      else if (path === `/trips/${tripId}/stay-areas`) body = { trip_id: tripId, version: 1, status: "recommended", city_code: "NRT", map_context: mapContext, pricing: { available: false }, current_lodging_area_code: null, located_item_count: 1, unassigned_item_count: 0, excluded_extension: {}, warnings: [], areas: [area] };
      else if (path.endsWith("/routes/status")) body = { version: 1, status: "idle" };
      else if (path.includes("/saved-items")) body = { items: [], total: 0, has_more: false };
      else if (path === "/travel-services/config") body = { enabled: false, kinds: [], destination_catalog: [], destinations: [], booking_partners: [] };
      else if (path.includes("/travel-services")) body = { items: [], total: 0, has_more: false };
      else if (path.includes("/affiliates/options")) body = { options: [] };
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(body) });
    });
    await page.goto(`/${locale}/trips/${tripId}`);
    // The existing SystemItineraryCard still uses this legacy label in every locale.
    await page.getByRole("button", { name: "設定主要飯店", exact: true }).first().click();
    const copy: Stay22Copy = JSON.parse(readFileSync(new URL(`../lib/stay22-messages/${locale}.json`, import.meta.url), "utf8"));
    const panel = page.getByRole("region", { name: copy.title });
    await expect(panel).toBeVisible();
    expect(externalRequests).toEqual([]);
    expect(hotelRequests).toEqual([]);
    const load = panel.getByRole("button", { name: copy.load, exact: true });
    await load.scrollIntoViewIfNeeded();
    const bounds = await load.boundingBox();
    expect(bounds!.height).toBeGreaterThanOrEqual(44);
    await load.focus();
    await page.keyboard.press("Enter");
    const frame = panel.locator("iframe");
    await expect(frame).toHaveCount(1);
    await frame.scrollIntoViewIfNeeded();
    await expect.poll(() => externalRequests.length).toBe(1);
    const sent = new URL(externalRequests[0]);
    expect(sent.searchParams.get("checkin")).toBe("2099-11-11");
    expect(sent.searchParams.get("children")).toBe("1");
    expect(sent.searchParams.get("campaign")).toBe("mokaair_stays_tokyo");
    expect(sent.href).not.toContain(tripId);
    await expect(frame).toHaveAttribute("referrerpolicy", "no-referrer");
    const panelBounds = await panel.boundingBox();
    expect(panelBounds!.x).toBeGreaterThanOrEqual(0);
    expect(panelBounds!.x + panelBounds!.width).toBeLessThanOrEqual(width + 1);
    if (locale === "zh-TW") await page.screenshot({ path: test.info().outputPath("stay22-loaded-fixture-390px.png") });
    expect(writes).toEqual([]);
    expect(hotelRequests).toEqual([]);
    await panel.getByRole("button", { name: copy.close, exact: true }).click();
    await expect(frame).toHaveCount(0);
    await expect(load).toBeFocused();
    if (locale === "zh-TW") await page.screenshot({ path: test.info().outputPath("stay22-390px.png") });
  });
}
