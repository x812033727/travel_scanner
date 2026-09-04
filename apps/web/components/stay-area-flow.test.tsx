import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { StayAreaFlow, type StayAreasResponse, type StayHotel, type StayHotelsResponse } from "./stay-area-flow";

const tripId = "00000000-0000-4000-8000-000000000001";
const future = new Date(Date.now() + 10 * 60_000).toISOString();

const areas: StayAreasResponse = {
  trip_id: tripId,
  version: 1,
  destination_name: "東京",
  city_code: "NRT",
  status: "recommended",
  pricing: { available: true, provider: "booking", mode: "live", message: null },
  current_lodging_area_code: null,
  located_item_count: 4,
  unassigned_item_count: 0,
  excluded_extension: {},
  warnings: [],
  areas: [
    { code: "asakusa", name: "淺草", latitude: 35.71, longitude: 139.79, radius_km: 2, is_day_trip: false, score: 0.8, item_count: 3, dwell_minutes: 300, day_count: 2, sample_titles: ["淺草寺", "晴空塔"], reasons: ["most_items", "most_days"] },
    { code: "shinjuku", name: "新宿", latitude: 35.69, longitude: 139.7, radius_km: 2, is_day_trip: false, score: 0.4, item_count: 1, dwell_minutes: 90, day_count: 1, sample_titles: ["新宿御苑"], reasons: ["central"] },
  ],
};

function hotel(overrides: Partial<StayHotel> & { id: string; hotel_id: string; hotel_name: string }): StayHotel {
  return {
    provider: "booking",
    latitude: 35.71,
    longitude: 139.79,
    currency: "TWD",
    nights: 5,
    nightly_price: 3200,
    total_price: 16000,
    rating: 4,
    review_score: 8.6,
    review_count: 1200,
    breakfast_included: true,
    refundable: true,
    distance_km: 0.4,
    in_area: true,
    is_current_lodging: false,
    preference_gaps: [],
    partners: [
      { partner: "agoda", display_name: "Agoda", kind: "hotel_search" },
      { partner: "booking", display_name: "Booking.com", kind: "deep_link" },
    ],
    address: "台東區淺草 1-1",
    expires_at: future,
    ...overrides,
  };
}

const hotels: StayHotelsResponse = {
  trip_id: tripId,
  version: 1,
  area: { code: "asakusa", name: "淺草", latitude: 35.71, longitude: 139.79, radius_km: 2 },
  check_in: "2026-11-10",
  check_out: "2026-11-15",
  nights: 5,
  date_notes: [],
  travelers: { adults: 2, children: 0, rooms: 1 },
  warnings: [],
  pricing: { status: "live", provider: "booking", message: null, retrieved_at: new Date().toISOString(), expires_at: future, cached: false },
  filters: { applied: { hotel_min_rating: 4 }, relaxed: [{ code: "breakfast", label: "含早餐" }], excluded_by_hard_filter: 1 },
  hotels: [
    hotel({ id: "offer-pricey", hotel_id: "200", hotel_name: "淺草景觀飯店", nightly_price: 5200, preference_gaps: ["nightly_max"] }),
    hotel({ id: "offer-cheap", hotel_id: "100", hotel_name: "淺草河畔飯店", nightly_price: 3200 }),
    hotel({ id: "offer-jpy", hotel_id: "300", hotel_name: "淺草和風旅館", currency: "JPY", nightly_price: 12000, price_estimate_unavailable: true, distance_km: 1.2 }),
  ],
  nearby: [],
  area_partners: [{ partner: "agoda", display_name: "Agoda", kind: "area_search" }],
  disclosure: "透過合作連結預訂，本站可能獲得分潤，價格不因此增加。",
};

function jsonResponse(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

function stubFetch(resolver: (url: string, init?: RequestInit) => unknown) {
  const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL, init?: RequestInit) => Promise.resolve(jsonResponse(resolver(String(input), init))));
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

function byPath(overrides: { areas?: unknown; hotels?: unknown } = {}) {
  return (url: string) => {
    if (url.includes("/hotels")) return overrides.hotels ?? hotels;
    return overrides.areas ?? areas;
  };
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("stay area flow", () => {
  it("lists recommended areas, then prices the chosen area with owner-ordered partner links", async () => {
    const fetchMock = stubFetch(byPath());
    const onSelectHotel = vi.fn().mockResolvedValue("ok");

    render(<StayAreaFlow tripId={tripId} busy={false} onSelectHotel={onSelectHotel} onManualLodging={vi.fn()} />);

    expect(await screen.findByText("淺草")).toBeTruthy();
    expect(screen.getByText("景點最多")).toBeTruthy();
    expect(screen.getByText("3 個安排 · 停留約 5 小時 · 2 天到訪")).toBeTruthy();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/hotels"))).toBe(false);

    fireEvent.click(screen.getAllByRole("button", { name: /看這區的飯店/ })[0]);

    expect(await screen.findByText("淺草河畔飯店")).toBeTruthy();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes(`/api/travel/trips/${tripId}/stay-areas/asakusa/hotels`))).toBe(true);
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/affiliates/options"))).toBe(false);
    expect(screen.getByText("5 晚 · 2 位成人 · 1 間房", { exact: false })).toBeTruthy();
    expect(screen.getByText("找不到完全符合條件的飯店，已放寬：含早餐")).toBeTruthy();
    const names = screen.getAllByRole("heading", { level: 4 }).map((heading) => heading.textContent);
    expect(names).toEqual(["淺草河畔飯店", "淺草景觀飯店", "淺草和風旅館"]);
    expect(screen.getByText("未符合：每晚最高價格")).toBeTruthy();

    const cheap = screen.getByText("淺草河畔飯店").closest("article") as HTMLElement;
    const forms = within(cheap).getAllByRole("button", { name: /Agoda|Booking\.com/ }).map((button) => button.closest("form")?.getAttribute("action"));
    expect(forms).toEqual([
      `/api/travel/trips/${tripId}/stay-areas/asakusa/clickout?partner=agoda&hotel_id=100`,
      `/api/travel/trips/${tripId}/stay-areas/asakusa/clickout?partner=booking&hotel_id=100`,
    ]);
    expect(within(cheap).getByRole("button", { name: "在 Agoda 搜尋此飯店" })).toBeTruthy();
    expect(within(cheap).getByRole("button", { name: "到 Booking.com 預訂" })).toBeTruthy();
    expect(within(cheap).getByText("NT$3,200")).toBeTruthy();
    expect(screen.getByRole("button", { name: "到 Agoda 查看淺草住宿" }).closest("form")?.getAttribute("action")).toBe(`/api/travel/trips/${tripId}/stay-areas/asakusa/clickout?partner=agoda`);
    expect(document.querySelector("a[href*='agoda.com'], a[href*='booking.com']")).toBeNull();

    fireEvent.click(within(cheap).getByRole("button", { name: "設為主要飯店" }));
    await waitFor(() => expect(onSelectHotel).toHaveBeenCalledTimes(1));
    expect(onSelectHotel.mock.calls[0][0].code).toBe("asakusa");
    expect(onSelectHotel.mock.calls[0][1].hotel_id).toBe("100");
  });

  it("renders foreign-currency rows in their own currency and hides gapped hotels on request", async () => {
    stubFetch(byPath());
    render(<StayAreaFlow tripId={tripId} busy={false} onSelectHotel={vi.fn().mockResolvedValue("ok")} onManualLodging={vi.fn()} />);
    fireEvent.click((await screen.findAllByRole("button", { name: /看這區的飯店/ }))[0]);

    const foreign = (await screen.findByText("淺草和風旅館")).closest("article") as HTMLElement;
    expect(within(foreign).queryByText(/NT\$/)).toBeNull();
    expect(within(foreign).getByText(/12,000/)).toBeTruthy();
    expect(within(foreign).getByText("無法換算為新台幣")).toBeTruthy();

    fireEvent.click(screen.getByRole("checkbox", { name: "只看完全符合" }));
    expect(screen.queryByText("淺草景觀飯店")).toBeNull();
    expect(screen.getByText("淺草河畔飯店")).toBeTruthy();
  });

  it("keeps partner links when pricing is not configured", async () => {
    stubFetch(byPath({ hotels: { ...hotels, hotels: [], pricing: { status: "not_configured", provider: null, message: null } } }));
    render(<StayAreaFlow tripId={tripId} busy={false} onSelectHotel={vi.fn()} onManualLodging={vi.fn()} />);
    fireEvent.click((await screen.findAllByRole("button", { name: /看這區的飯店/ }))[0]);

    expect(await screen.findByText("尚未設定飯店報價供應商")).toBeTruthy();
    expect(screen.getByRole("button", { name: "到 Agoda 查看淺草住宿" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "設為主要飯店" })).toBeNull();
  });

  it("offers the manual editor when the destination has no area catalog", async () => {
    stubFetch(byPath({ areas: { ...areas, status: "unsupported", city_code: null, areas: [] } }));
    const onManualLodging = vi.fn();
    render(<StayAreaFlow tripId={tripId} busy={false} onSelectHotel={vi.fn()} onManualLodging={onManualLodging} />);

    expect(await screen.findByText("這個目的地還沒有住宿熱區資料，可以手動輸入飯店。")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "手動輸入飯店" }));
    expect(onManualLodging).toHaveBeenCalledTimes(1);
  });

  it("refreshes the area when the chosen offer expired server-side", async () => {
    const fetchMock = stubFetch(byPath());
    const onSelectHotel = vi.fn().mockResolvedValueOnce("expired").mockResolvedValue("ok");
    render(<StayAreaFlow tripId={tripId} busy={false} onSelectHotel={onSelectHotel} onManualLodging={vi.fn()} />);
    fireEvent.click((await screen.findAllByRole("button", { name: /看這區的飯店/ }))[0]);
    const cheap = (await screen.findByText("淺草河畔飯店")).closest("article") as HTMLElement;

    fireEvent.click(within(cheap).getByRole("button", { name: "設為主要飯店" }));

    expect(await screen.findByText("報價已更新，請再確認一次。")).toBeTruthy();
    await waitFor(() => expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/hotels?refresh=true"))).toBe(true));
  });

  it("disables choosing and partner links once the quote has expired", async () => {
    const past = new Date(Date.now() - 60_000).toISOString();
    stubFetch(byPath({ hotels: { ...hotels, pricing: { ...hotels.pricing, expires_at: past } } }));
    render(<StayAreaFlow tripId={tripId} busy={false} onSelectHotel={vi.fn()} onManualLodging={vi.fn()} />);
    fireEvent.click((await screen.findAllByRole("button", { name: /看這區的飯店/ }))[0]);

    const cheap = (await screen.findByText("淺草河畔飯店")).closest("article") as HTMLElement;
    expect((within(cheap).getByRole("button", { name: "設為主要飯店" }) as HTMLButtonElement).disabled).toBe(true);
    expect((within(cheap).getByRole("button", { name: "在 Agoda 搜尋此飯店" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByText(/報價已過期/)).toBeTruthy();
  });
});
