// Local test data only. Names and coordinates are fixtures, not provider results.
import type { Trip, TripItem } from "../../lib/trip-types";
const day = "2026-11-11";
function stop(id: string, title: string, position: number, role?: TripItem["system_role"]): TripItem {
  return { id, title, position, system_role: role, item_type: "custom", day_date: day,
    latitude: 35.714, longitude: 139.79, location_name: title,
    locked: Boolean(role), fixed_time: Boolean(role && role !== "hotel_end"),
    start_time: role === "lunch" ? day + "T12:00:00" : role === "dinner" ? day + "T18:30:00" : day + "T09:00:00",
    duration_minutes: role?.startsWith("hotel_") ? 0 : 60,
    is_estimated: false, location_source: "confirmed", data: { source_mode: "manual" } };
}
export const editorFixture: Trip = {
  id: "intuitive-trip", name: "東京慢旅・編輯器測試", mode: "manual", total_price: 0,
  currency: "TWD", version: 1, share_enabled: false, data: {},
  destination_name: "日本東京", destination_country_code: "JP",
  start_date: day, end_date: "2026-11-12", timezone: "Asia/Tokyo",
  primary_lodging: { name: "淺草飯店", location_name: "淺草", latitude: 35.714, longitude: 139.79, location_source: "confirmed" },
  items: [
    stop("hotel1", "從 淺草飯店 出發", 0, "hotel_start"),
    stop("asakusa", "淺草散步", 1),
    stop("lunch1", "午餐・河畔食堂", 2, "lunch"),
    stop("dinner1", "晚餐・巷弄小店", 3, "dinner"),
    stop("end1", "返回 淺草飯店", 4, "hotel_end"),
    ...[stop("hotel2", "從 淺草飯店 出發", 0, "hotel_start"), stop("lunch2", "午餐尚未安排", 1, "lunch"),
      stop("dinner2", "晚餐尚未安排", 2, "dinner"), stop("end2", "返回 淺草飯店", 3, "hotel_end")]
      .map((row) => ({ ...row, day_date: "2026-11-12", start_time: row.start_time?.replace(day, "2026-11-12") })),
  ],
};
export const editorPlaceOptions = [
  { key: "hotspot:temple", id: "temple", kind: "hotspot", title: "淺草寺", subtitle: "東京", is_saved: true, distance_km: .4,
    item: { ...stop("temple", "淺草寺", 0), provider_place_id: "temple", duration_minutes: 90, data: { catalog_selection: { kind: "hotspot", id: "temple" } } } },
  { key: "hotspot:park", id: "park", kind: "hotspot", title: "隅田公園", subtitle: "東京", is_saved: false, distance_km: .7,
    item: { ...stop("park", "隅田公園", 0), provider_place_id: "park", data: { catalog_selection: { kind: "hotspot", id: "park" } } } },
  { key: "merchant:cafe", id: "cafe", kind: "merchant", title: "河畔咖啡", subtitle: "東京", is_saved: false, distance_km: .8,
    item: { ...stop("cafe", "河畔咖啡", 0), provider_place_id: "cafe", data: { catalog_selection: { kind: "merchant", id: "cafe" } } } },
];
