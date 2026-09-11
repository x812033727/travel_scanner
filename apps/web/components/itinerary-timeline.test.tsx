import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { RouteSegment, TripItem } from "@/lib/trip-types";
import { ItineraryTimeline } from "./itinerary-timeline";

function item(id: string, title: string, position: number, patch: Partial<TripItem> = {}): TripItem {
  return {
    id,
    item_type: "activity",
    day_date: "2026-11-10",
    position,
    title,
    start_time: `2026-11-10T${String(9 + position).padStart(2, "0")}:00:00+09:00`,
    locked: false,
    is_estimated: false,
    data: {},
    ...patch,
  };
}

const directRoute: RouteSegment = {
  from_item_id: "activity",
  to_item_id: "dinner",
  status: "resolved",
  travel_mode: "walk",
  provider: "google_routes",
  attribution: "Google Maps",
  generated_at: "2026-09-01T00:00:00Z",
  schedule_mode: "scheduled",
  preference: "FEWER_TRANSFERS",
  duration_minutes: 18,
  steps: [],
  details_available: [],
  warnings: [],
};

describe("readonly itinerary timeline", () => {
  it("lets share recipients open both map identities and a clearly labelled position reference without editing", () => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    const items = [item("palace", "景福宮", 0, {
      location_map_links: [
        { provider: "naver", url: "https://map.naver.com/p/entry/place/11571707" },
        { provider: "google", url: "https://www.google.com/maps/search/?api=1&query=37.5796,126.977", position_only: true },
      ],
    })];
    render(<ItineraryTimeline items={items} timezone="Asia/Seoul" />);
    const naver = screen.getByRole("link", { name: "NAVER Maps: 景福宮" });
    const google = screen.getByRole("link", { name: "Google Maps · 位置參考: 景福宮" });
    expect(naver.getAttribute("href")).toContain("/entry/place/11571707");
    expect(google.getAttribute("href")).toContain("query=37.5796,126.977");
    expect(google.getAttribute("target")).toBe("_blank");
    expect(screen.queryByRole("button")).toBeNull();
    expect(screen.queryByRole("textbox")).toBeNull();
    expect(fetcher).not.toHaveBeenCalled();
    vi.unstubAllGlobals();
  });

  it("uses only verified legacy identities and rejects unsafe or mismatched map hosts", () => {
    const items = [item("palace", "景福宮", 0, { map_identities: {
      naver_maps: { provider: "naver_maps", place_id: "11571707", map_url: "https://map.naver.com/p/entry/place/11571707", status: "verified" },
      google_places: { provider: "google_places", place_id: "ChIJ-pending", map_url: "https://www.google.com/maps/search/?api=1&query_place_id=ChIJ-pending&query=place", status: "pending" },
    } }), item("unsafe", "Unsafe", 1, { location_map_links: [
      { provider: "google", url: "javascript:alert(1)" },
      { provider: "naver", url: "https://attacker.example/naver" },
    ] })];
    render(<ItineraryTimeline items={items} />);
    expect(screen.getAllByRole("link")).toHaveLength(1);
    expect(screen.getByRole("link", { name: "NAVER Maps: 景福宮" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: /Google Maps/ })).toBeNull();
  });

  it("keeps an explicit empty server map list authoritative over cached identities", () => {
    render(<ItineraryTimeline items={[item("palace", "景福宮", 0, { location_map_links: [], map_identities: {
      google_places: { provider: "google_places", place_id: "ChIJ-old", map_url: "https://www.google.com/maps/search/?api=1&query=place&query_place_id=ChIJ-old", status: "verified" },
    } })]} />);
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("hides skipped meals, keeps hotel anchors, and separates logistics", () => {
    const items = [
      item("flight-out", "長榮航空 BR 198", 0, { item_type: "flight", system_role: "outbound_flight", fixed_time: true, locked: true, data: { flight_info: { airline: "長榮航空", flight_number: "BR 198", origin: "TPE", destination: "NRT", departure_local: "2026-11-10T08:50", arrival_local: "2026-11-10T13:10" } } }),
      item("hotel-start", "從丸之內飯店出發", 0, { item_type: "hotel_anchor", system_role: "hotel_start", locked: true }),
      item("activity", "淺草寺", 1, {
        latitude: 35.7148,
        longitude: 139.7967,
        names: { title: { "zh-TW": "淺草寺", en: "Sensō-ji", original: "浅草寺", original_locale: "ja" } },
      }),
      item("lunch", "已跳過午餐", 2, { item_type: "meal", system_role: "lunch", is_skipped: true, locked: true }),
      item("dinner", "銀座晚餐", 3, { item_type: "meal", system_role: "dinner", locked: true, latitude: 35.6717, longitude: 139.765 }),
      item("hotel-end", "返回丸之內飯店", 4, { item_type: "hotel_anchor", system_role: "hotel_end", locked: true }),
      item("flight-return", "回程航班尚未設定", 5, { item_type: "flight", system_role: "return_flight", fixed_time: true, locked: true, data: { flight_info: null } }),
      item("flight", "抵達羽田機場", 5, { item_type: "flight", data: { timeline_section: "logistics" } }),
    ];

    render(<ItineraryTimeline items={items} routes={[directRoute]} />);

    expect(screen.queryByText("已跳過午餐")).toBeNull();
    expect(screen.getByText("淺草寺")).toBeTruthy();
    expect(screen.getByText("浅草寺").getAttribute("lang")).toBe("ja");
    expect(screen.getByText("從丸之內飯店出發")).toBeTruthy();
    expect(screen.getByText("返回丸之內飯店")).toBeTruthy();
    expect(screen.getByText("交通與住宿資訊")).toBeTruthy();
    expect(screen.getByText("抵達羽田機場")).toBeTruthy();
    expect(screen.getByText("去程航班")).toBeTruthy();
    expect(screen.getByText("回程航班尚未設定")).toBeTruthy();
    expect(screen.getByText("步行 · 18 分鐘")).toBeTruthy();
  });
});

/**
 * The timeline is the whole reason a share link gets opened, and the recipient may
 * read no Chinese at all. activeLocale() reads the document language, so this suite
 * sets it and asserts against the real English catalog rather than a stub.
 *
 * Fixtures here carry no Chinese of their own: anything Han on screen is the
 * component's. FlightAnchorCard and RouteSegmentCard are left out on purpose —
 * they still hold literals of their own and belong to other tasks.
 */
describe("the timeline in a language that is not Chinese", () => {
  const han = () => document.body.textContent?.match(/\p{Script=Han}+/u)?.[0];

  beforeEach(() => {
    document.documentElement.lang = "en";
  });
  afterEach(() => {
    document.documentElement.lang = "zh-TW";
  });

  it("writes no Chinese of its own across meals, hotels, badges and missing places", () => {
    const items = [
      item("hotel-start", "Leaving the hotel", 0, { item_type: "hotel_anchor", system_role: "hotel_start", locked: true, start_time: null }),
      item("activity", "Sensō-ji", 1, { locked: true, is_estimated: true, location_name: undefined }),
      item("lunch", "Lunch", 2, { item_type: "meal", system_role: "lunch", location_name: undefined }),
      item("dinner", "Ginza dinner", 3, { item_type: "meal", system_role: "dinner", fixed_time: true, end_time: "2026-11-10T20:00:00+09:00", location_name: "Ginza" }),
      item("transfer", "Airport transfer", 4, { start_time: null, data: { timeline_section: "logistics" } }),
    ];
    render(<ItineraryTimeline items={items} />);

    expect(screen.getByText("Transfers and accommodation")).toBeTruthy();
    expect(screen.getByText("3 stop(s)")).toBeTruthy();
    expect(screen.getByText("Estimated")).toBeTruthy();
    expect(screen.getByText("No location set")).toBeTruthy();
    expect(screen.getByText("Restaurant not chosen")).toBeTruthy();
    expect(screen.getByText("No main hotel set")).toBeTruthy();
    // formatTime's own fallback is a Chinese literal; the transfer has no time and
    // must not reach it.
    expect(document.body.textContent).toContain("Flexible time");
    expect(han(), "hardcoded copy on the shared timeline").toBeUndefined();
  });

  it("tells a share recipient that an empty trip is empty, in their language", () => {
    render(<ItineraryTimeline items={[]} />);

    expect(screen.getByText("This trip has no stops yet")).toBeTruthy();
    expect(han(), "hardcoded copy on the empty state").toBeUndefined();
  });
});
