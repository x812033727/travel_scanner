import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripEditor } from "./trip-editor";
import type { Trip } from "@/lib/trip-types";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }), useSearchParams: () => new URLSearchParams() }));

const trip = {
  id: "00000000-0000-4000-8000-000000000001",
  name: "東京五日",
  mode: "balanced",
  total_price: 52000,
  currency: "TWD",
  data: {},
  version: 1,
  share_enabled: false,
  items: [
    {
      id: "00000000-0000-4000-8000-000000000002",
      item_type: "activity",
      day_date: "2026-11-11",
      position: 0,
      title: "淺草散步",
      location_name: "淺草",
      locked: false,
      is_estimated: false,
      data: {},
    },
  ],
};

function response(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

async function openToolsSection(section: "旅行準備" | "旅程設定" | "分享與匯出") {
  fireEvent.click(await screen.findByRole("button", { name: "開啟旅程工具" }));
  const dialog = screen.getByRole("dialog", { name: "旅程工具" });
  fireEvent.click(within(dialog).getByRole("button", { name: new RegExp(`^${section}`) }));
  return dialog;
}

async function openStopEditor(title: string) {
  const summary = await screen.findByLabelText(`${title} 的更多操作`);
  fireEvent.click(summary);
  const menu = summary.closest("details")!;
  expect(menu.open).toBe(true);
  fireEvent.click(within(menu).getByRole("button", { name: `編輯 ${title}` }));
  expect(menu.open).toBe(false);
  return await screen.findByRole("dialog", { name: "編輯安排" });
}

async function saveEditor(editor: HTMLElement) {
  fireEvent.click(within(editor).getByRole("button", { name: "儲存修改" }));
  await waitFor(() => expect(screen.queryByRole("dialog", { name: "編輯安排" })).toBeNull());
}

async function openAI() {
  const toolbar = await screen.findByRole("toolbar", { name: "行程快速操作" });
  fireEvent.click(within(toolbar).getByRole("button", { name: "AI 助手" }));
  return await screen.findByRole("dialog", { name: "AI 幫我安排" });
}

async function openAddFromToolbar() {
  const toolbar = await screen.findByRole("toolbar", { name: "行程快速操作" });
  fireEvent.click(within(toolbar).getByRole("button", { name: "新增安排" }));
}

function openOptionalStop(title: string) {
  const existing = screen.queryByText(title, { selector: "summary strong" })?.closest("details");
  if (existing) { if (!existing.open) fireEvent.click(existing.querySelector("summary")!); return existing; }
  const summary = screen.getByText("補充安排", { selector: "summary span" }).closest("summary")!;
  const disclosure = summary.closest("details")!;
  if (!disclosure.open) fireEvent.click(summary);
  expect(disclosure.open).toBe(true);
  const entry = within(disclosure).queryByRole("button", { name: title });
  if (entry) fireEvent.click(entry);
  return disclosure;
}

function itineraryPreview(scope: "day" | "trip") {
  return {
    preview_id: `preview-${scope}`,
    base_version: 1,
    expires_at: "2026-11-01T10:15:00Z",
    scope,
    day_date: scope === "day" ? "2026-11-11" : null,
    planning: { status: "live", readiness: "ready", provider: "minimax", model: "MiniMax-M2.1", generated_at: "2026-11-01T10:00:00Z", warnings: [] },
    days: [{ date: "2026-11-11", label: "2026-11-11", items: [{ ...trip.items[0], title: "MiniMax 安排的淺草寺", location_name: "淺草寺", latitude: 35.7148, longitude: 139.7967, data: { generated_by: "ai_planner", hotspot_id: "hotspot-1" } }] }],
    unscheduled_slots: [],
    readiness: { status: "ready", has_lodging: false, exact_item_count: 1, hotspot_candidate_count: 16, merchant_candidate_count: 6, preserved_item_count: 1, assumptions: ["尚未設定飯店；本次只依景點區域分組，不建立飯店往返路線。"] },
    routing_summary: { exact_items: 1, eligible_pairs: 0, hotel_pairs_deferred: 2 },
  };
}

function intentPreview(version: number) {
  return {
    preview_id: "intent-preview", base_version: version, scope: "day", day_date: "2026-11-11",
    expires_at: "2026-11-01T10:15:00Z", planning: itineraryPreview("day").planning,
    intent: { text: "保留手動安排，新增室內展館" }, usage_operation: "ai_itinerary_refine",
    diff: { removed: [], changed: [], moved: [], meals: [], unchanged_count: 1, has_changes: true,
      added: [{ candidate_key: "hotspot:museum", title: "東京國立博物館", day_date: "2026-11-11", start_time: "14:00", reason: "室內展館" }] },
    exhaustion: { exhausted: false, reason: null, alternative_candidate_count: 4, activity_delta: 1, fewer_stops_without_alternatives: false },
  };
}

afterEach(() => {
  window.localStorage.clear();
  window.history.replaceState({}, "", window.location.href);
  vi.unstubAllGlobals();
});
describe("trip editor", () => {
  it("does not load affiliate options or stay areas until the member opens the stay flow", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(response(trip)));
    vi.stubGlobal("fetch", fetchMock);

    render(<TripEditor tripId={trip.id} />);

    expect((await screen.findAllByText("東京五日")).length).toBeGreaterThan(0);
    expect(screen.queryByText("這趟旅程的合作平台")).toBeNull();
    expect(
      fetchMock.mock.calls.some(([input]) => String(input).includes("/affiliates/options")),
    ).toBe(false);
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/stay-areas"))).toBe(false);
  });

  it("keeps the itinerary first and mounts preparation services only inside their tool section", async () => {
    const datedTrip = { ...trip, destination_name: "東京", start_date: "2026-11-11", end_date: "2026-11-11" };
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/affiliates/options")) return response({ module: new URL(url, "https://mokaair.com").searchParams.get("module"), options: [], disclosure: "" });
      if (url.endsWith("/places")) return response({ items: [] });
      if (url.endsWith("/weather")) return { ok: false, status: 503, json: async () => ({ detail: "weather_not_configured" }) };
      if (url.endsWith("/travel-services/config")) return response({ enabled_kinds: [] });
      return response(datedTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByRole("heading", { name: "淺草散步" })).toBeTruthy();
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.queryByRole("heading", { name: "旅伴與旅行偏好" })).toBeNull();
    const preparationCalls = () => fetchMock.mock.calls.filter(([input]) => /\/affiliates\/options|\/weather$|\/places$|\/travel-services\/config$/.test(String(input)));
    expect(preparationCalls()).toHaveLength(0);

    fireEvent.click(screen.getByRole("button", { name: "開啟旅程工具" }));
    const tools = screen.getByRole("dialog", { name: "旅程工具" });
    expect(within(tools).getByRole("button", { name: /^旅行準備/ })).toBeTruthy();
    expect(within(tools).getByRole("button", { name: /^旅程設定/ })).toBeTruthy();
    expect(within(tools).getByRole("button", { name: /^分享與匯出/ })).toBeTruthy();
    expect(preparationCalls()).toHaveLength(0);
    fireEvent.click(within(tools).getByRole("button", { name: /^分享與匯出/ }));
    expect(within(tools).getByRole("link", { name: "開啟列印版" })).toBeTruthy();
    expect(preparationCalls()).toHaveLength(0);

    fireEvent.click(within(tools).getByRole("button", { name: "返回" }));
    fireEvent.click(within(tools).getByRole("button", { name: /^旅行準備/ }));
    await waitFor(() => {
      expect(fetchMock.mock.calls.some(([input]) => String(input).endsWith("/weather"))).toBe(true);
      expect(fetchMock.mock.calls.some(([input]) => String(input).endsWith("/places"))).toBe(true);
      expect(fetchMock.mock.calls.filter(([input]) => String(input).includes("/affiliates/options"))).toHaveLength(4);
    });
    expect(screen.getAllByRole("dialog")).toHaveLength(1);
    fireEvent.click(within(tools).getByRole("button", { name: "返回" }));
    expect(screen.queryByRole("region", { name: "旅程天氣" })).toBeNull();
    expect(screen.queryByRole("link", { name: "開啟列印版" })).toBeNull();
  });

  it("opens editing from the stop title and exposes move only through its dismissible More menu", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(trip));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const title = await screen.findByRole("heading", { name: "淺草散步" });
    const summary = screen.getByLabelText("淺草散步 的更多操作");
    const menu = summary.closest("details")!;
    expect(menu.open).toBe(false);
    fireEvent.click(title.closest("button")!);
    let editor = await screen.findByRole("dialog", { name: "編輯安排" });
    expect((within(editor).getByLabelText("安排名稱") as HTMLInputElement).value).toBe("淺草散步");
    fireEvent.click(within(editor).getByRole("button", { name: "關閉" }));

    fireEvent.click(summary);
    expect(menu.open).toBe(true);
    fireEvent.keyDown(summary, { key: "Escape" });
    expect(menu.open).toBe(false);
    expect(document.activeElement).toBe(summary);
    editor = await openStopEditor("淺草散步");
    fireEvent.click(within(editor).getByRole("button", { name: "關閉" }));
    fireEvent.click(summary);
    fireEvent.click(within(menu).getByRole("button", { name: "移動 淺草散步" }));
    expect(menu.open).toBe(false);
    const move = screen.getByRole("dialog", { name: "移動這個行程" });
    expect(screen.getAllByRole("dialog")).toHaveLength(1);
    expect(within(move).getByLabelText("插入位置")).toBeTruthy();
    fireEvent.click(within(move).getByRole("button", { name: "取消" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.getByRole("heading", { name: "淺草散步" })).toBeTruthy();
    expect(fetchMock.mock.calls.some(([, init]) => (init as RequestInit | undefined)?.method === "PUT")).toBe(false);
  });

  it("keeps arrange and text adjustments in a single AI panel without starting provider work", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(trip));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    await openAI();
    const assistant = screen.getByRole("dialog");
    expect(within(assistant).getByRole("radio", { name: /^單日安排/ }).getAttribute("aria-checked")).toBe("true");
    fireEvent.click(within(assistant).getByRole("button", { name: "調整現有行程" }));
    expect(screen.getAllByRole("dialog")).toHaveLength(1);
    expect((within(assistant).getByRole("button", { name: "看看會怎麼改" }) as HTMLButtonElement).disabled).toBe(true);
    expect(within(assistant).getByRole("radio", { name: "這一天" }).getAttribute("aria-checked")).toBe("true");
    expect(within(assistant).queryByRole("button", { name: "產生預覽 · 不扣次" })).toBeNull();
    fireEvent.click(within(assistant).getByRole("button", { name: "安排景點" }));
    expect(screen.getAllByRole("dialog")).toHaveLength(1);
    expect(within(assistant).getByRole("button", { name: "產生預覽 · 不扣次" })).toBeTruthy();
    expect(fetchMock.mock.calls.some(([input]) => /\/itinerary\/preview|\/optimize\/preview|\/intent/.test(String(input)))).toBe(false);
  });

  it("holds the AI panel during delayed intent apply and preserves the flushed manual edit", async () => {
    let stored = structuredClone(trip);
    let finishApply!: (value: ReturnType<typeof response>) => void;
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/intents")) return response(intentPreview(stored.version));
      if (url.endsWith("/itinerary/apply")) return new Promise<ReturnType<typeof response>>((resolve) => { finishApply = resolve; });
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        stored = { ...stored, version: stored.version + 1, items: body.items };
      }
      return response(stored);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.change(within(editor).getByLabelText("安排名稱"), { target: { value: "我手動保留的淺草散步" } });
    await saveEditor(editor);
    await openAI();
    const assistant = await screen.findByRole("dialog", { name: "AI 幫我安排" });
    fireEvent.click(within(assistant).getByRole("button", { name: "調整現有行程" }));
    fireEvent.change(within(assistant).getByLabelText("想改什麼？"), { target: { value: "保留手動安排，新增室內展館" } });
    fireEvent.click(within(assistant).getByRole("button", { name: "看看會怎麼改" }));
    const review = await within(assistant).findByRole("region", { name: "確認這次調整" });
    expect(stored.items[0].title).toBe("我手動保留的淺草散步");
    expect(stored.version).toBe(2);
    const intentCall = fetchMock.mock.calls.find(([input]) => String(input).endsWith("/intents"))!;
    expect(JSON.parse(String(intentCall[1]?.body))).toMatchObject({ version: 2 });

    const apply = within(review).getByRole("button", { name: /^套用/ });
    fireEvent.click(apply);
    await waitFor(() => expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/itinerary/apply"))).toHaveLength(1));
    const arrange = within(assistant).getByRole("button", { name: "安排景點" });
    const adjust = within(assistant).getByRole("button", { name: "調整現有行程" });
    expect((arrange as HTMLButtonElement).disabled).toBe(true);
    expect((adjust as HTMLButtonElement).disabled).toBe(true);
    expect((apply as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(arrange);
    fireEvent.click(within(assistant).getByRole("button", { name: "關閉" }));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.getAllByRole("dialog")).toEqual([assistant]);
    expect(within(assistant).getByRole("region", { name: "確認這次調整" })).toBe(review);
    expect(within(assistant).queryByRole("button", { name: /^產生預覽/ })).toBeNull();
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/itinerary/apply"))).toHaveLength(1);
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/intents"))).toHaveLength(1);

    stored = { ...stored, version: 3, items: [...stored.items, { ...trip.items[0], id: "museum", position: 1, title: "東京國立博物館" }] };
    await act(async () => finishApply(response(stored)));
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.getByRole("heading", { name: "我手動保留的淺草散步" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "東京國立博物館" })).toBeTruthy();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "PUT")).toHaveLength(1);
    expect(fetchMock.mock.calls.some(([input]) => String(input).endsWith("/itinerary/preview"))).toBe(false);
  });

  it("disables arrange and adjustment navigation until itinerary generation finishes", async () => {
    let finishPreview!: (value: ReturnType<typeof response>) => void;
    const fetchMock = vi.fn((input: RequestInfo | URL) => String(input).endsWith("/itinerary/preview")
      ? new Promise<ReturnType<typeof response>>((resolve) => { finishPreview = resolve; }) : Promise.resolve(response(trip)));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    await openAI();
    const assistant = await screen.findByRole("dialog", { name: "AI 幫我安排" });
    fireEvent.click(within(assistant).getByRole("button", { name: /^產生預覽/ }));
    await waitFor(() => expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/itinerary/preview"))).toHaveLength(1));
    const adjust = within(assistant).getByRole("button", { name: "調整現有行程" });
    expect((adjust as HTMLButtonElement).disabled).toBe(true);
    expect((within(assistant).getByRole("button", { name: "安排景點" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(adjust);
    fireEvent.click(within(assistant).getByRole("button", { name: "關閉" }));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.getAllByRole("dialog")).toEqual([assistant]);
    expect(within(assistant).queryByLabelText("想改什麼？")).toBeNull();
    await act(async () => finishPreview(response(itineraryPreview("day"))));
    expect(screen.getByRole("dialog", { name: "確認 AI 行程預覽" })).toBeTruthy();
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/itinerary/preview"))).toHaveLength(1);
    expect(fetchMock.mock.calls.some(([input]) => String(input).endsWith("/itinerary/apply"))).toBe(false);
    expect(screen.getByRole("heading", { name: "淺草散步" })).toBeTruthy();
  });

  it("keeps settings mounted and noneditable during preference saving and preserves manual edits", async () => {
    let stored = { ...trip, data: { travelers: { adults: 2, children: 0, rooms: 1 } } };
    let finishSave!: (value: ReturnType<typeof response>) => void;
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "PATCH") return new Promise<ReturnType<typeof response>>((resolve) => { finishSave = resolve; });
      if (init?.method === "PUT") stored = { ...stored, version: stored.version + 1, items: JSON.parse(String(init.body)).items };
      return response(stored);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.change(within(editor).getByLabelText("安排名稱"), { target: { value: "手動安排先保留" } });
    await saveEditor(editor);
    const tools = await openToolsSection("旅程設定");
    expect(within(tools).getByText("旅伴與旅行偏好")).toBeTruthy();
    fireEvent.change(within(tools).getByLabelText("成人"), { target: { value: "3" } });
    fireEvent.click(within(tools).getByRole("button", { name: "儲存偏好" }));
    await waitFor(() => expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "PATCH")).toHaveLength(1));
    expect(stored.items[0].title).toBe("手動安排先保留");
    const saveCall = fetchMock.mock.calls.find(([, init]) => init?.method === "PATCH")!;
    expect(JSON.parse(String(saveCall[1]?.body))).toEqual({ version: 2, travelers: { adults: 3 } });
    const back = within(tools).getByRole("button", { name: "返回" });
    expect((back as HTMLButtonElement).disabled).toBe(true);
    expect(within(tools).getByLabelText("每日從飯店出發時間").matches(":disabled")).toBe(true);
    expect(within(tools).getByLabelText("成人").matches(":disabled")).toBe(true);
    fireEvent.click(back);
    fireEvent.click(within(tools).getByRole("button", { name: "關閉" }));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.getAllByRole("dialog")).toEqual([tools]);
    expect(within(tools).queryByRole("button", { name: /^旅行準備/ })).toBeNull();
    expect(screen.queryByRole("dialog", { name: "編輯安排" })).toBeNull();

    stored = { ...stored, version: 3, data: { travelers: { adults: 3, children: 0, rooms: 1 } } };
    await act(async () => finishSave(response(stored)));
    expect((back as HTMLButtonElement).disabled).toBe(false);
    expect(within(tools).getByLabelText("每日從飯店出發時間").matches(":disabled")).toBe(false);
    fireEvent.click(within(tools).getByRole("button", { name: "關閉" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(screen.getByRole("heading", { name: "手動安排先保留" })).toBeTruthy();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "PUT")).toHaveLength(1);
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "PATCH")).toHaveLength(1);
  });

  it("links each flight anchor to a search for this trip", async () => {
    const outbound = {
      ...trip.items[0],
      id: "00000000-0000-4000-8000-000000000003",
      item_type: "flight",
      title: "去程航班尚未設定",
      location_name: null,
      system_role: "outbound_flight" as const,
      fixed_time: true,
      locked: true,
      data: { flight_selection_source: "unset", flight_info: null },
    };
    const flightTrip = { ...trip, start_date: "2026-11-11", end_date: "2026-11-11", items: [trip.items[0], outbound] };
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(response(flightTrip)));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    openOptionalStop("去程航班尚未設定");
    // An unset flight remains available inside the compact optional anchor.
    const link = await screen.findByRole("link", { name: /^查機票 · / });
    expect(link.getAttribute("href")).toBe(`/search?trip_id=${trip.id}`);
  });

  it("opens the stay-area flow from the hotel card and sets the chosen hotel as primary lodging", async () => {
    const hotelStart = {
      ...trip.items[0],
      id: "00000000-0000-4000-8000-000000000010",
      position: -1,
      item_type: "hotel_anchor",
      title: "從 尚未設定飯店 出發",
      location_name: null,
      system_role: "hotel_start" as const,
      fixed_time: true,
      data: { needs_place_confirmation: true },
    };
    const stayTrip = {
      ...trip,
      start_date: "2026-11-11",
      end_date: "2026-11-12",
      primary_lodging: null,
      items: [{ ...trip.items[0], latitude: 35.7148, longitude: 139.7967, location_source: "hotspot_catalog" }, hotelStart],
    };
    const chosenTrip = {
      ...stayTrip,
      version: 2,
      primary_lodging: { name: "淺草河畔飯店", location_name: "台東區淺草 1-1", latitude: 35.71, longitude: 139.79, location_source: "provider", selection_source: "user", hotel_id: "100", provider: "booking" },
      items: [stayTrip.items[0], { ...hotelStart, title: "從 淺草河畔飯店 出發", location_name: "台東區淺草 1-1", latitude: 35.71, longitude: 139.79, location_source: "provider", data: { needs_place_confirmation: false } }],
      routing: { status: "complete", total: 1, completed: 1, day_settings: [] },
    };
    const future = new Date(Date.now() + 10 * 60_000).toISOString();
    const areasPayload = {
      trip_id: trip.id, version: 1, status: "recommended", city_code: "NRT", pricing: { available: true, provider: "booking", mode: "live" }, current_lodging_area_code: null,
      located_item_count: 1, unassigned_item_count: 0, excluded_extension: {}, warnings: [],
      areas: [{ code: "asakusa", name: "淺草", latitude: 35.71, longitude: 139.79, radius_km: 2, is_day_trip: false, score: 0.9, item_count: 1, dwell_minutes: 60, day_count: 1, sample_titles: ["淺草散步"], reasons: ["most_items"] }],
    };
    const hotelsPayload = {
      trip_id: trip.id, version: 1, area: { code: "asakusa", name: "淺草", latitude: 35.71, longitude: 139.79, radius_km: 2 }, check_in: "2026-11-11", check_out: "2026-11-12", nights: 1, date_notes: [],
      travelers: { adults: 1, children: 0, rooms: 1 }, warnings: [], pricing: { status: "live", provider: "booking", expires_at: future }, filters: { applied: {}, relaxed: [], excluded_by_hard_filter: 0 },
      hotels: [{ id: "offer-1", hotel_id: "100", hotel_name: "淺草河畔飯店", provider: "booking", latitude: 35.71, longitude: 139.79, currency: "TWD", nights: 1, nightly_price: 3200, total_price: 3200, rating: 4, review_score: 8.6, review_count: 1200, breakfast_included: true, refundable: true, distance_km: 0.4, in_area: true, is_current_lodging: false, preference_gaps: [], partners: [{ partner: "agoda", display_name: "Agoda", kind: "hotel_search" }], expires_at: future }],
      nearby: [], area_partners: [], disclosure: "",
    };
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/stay-areas/asakusa/select")) return Promise.resolve(response(chosenTrip));
      if (url.includes("/stay-areas/asakusa/hotels")) return Promise.resolve(response(hotelsPayload));
      if (url.includes("/stay-areas")) return Promise.resolve(response(areasPayload));
      if (url.includes("/routes/status")) return Promise.resolve(response({ version: 2, status: "complete" }));
      return Promise.resolve(response(init?.method === "PUT" ? stayTrip : stayTrip));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    openOptionalStop("從 尚未設定飯店 出發");
    const dialog = await screen.findByRole("dialog", { name: "住宿熱區" });
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes(`/trips/${trip.id}/stay-areas`))).toBe(true);
    fireEvent.click(await within(dialog).findByRole("button", { name: /看這區的飯店/ }));
    fireEvent.click(await within(dialog).findByRole("button", { name: "設為主要飯店" }));

    await waitFor(() => {
      const selectCall = fetchMock.mock.calls.find(([input]) => String(input).includes("/stay-areas/asakusa/select"));
      expect(selectCall).toBeTruthy();
      expect(selectCall?.[1]?.method).toBe("POST");
      expect(JSON.parse(String(selectCall?.[1]?.body))).toEqual({ version: 1, provider: "booking", hotel_id: "100" });
    });
    expect(await screen.findByText("已將 淺草河畔飯店 設為主要飯店，正在重新計算每日路線。")).toBeTruthy();
    expect(screen.queryByRole("dialog", { name: "住宿熱區" })).toBeNull();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes("/affiliates/options"))).toBe(false);
  });

  it.each([
    ["JP", "Ekispert 大眾運輸"],
    ["KR", "ODsay 大眾運輸"],
  ])("shows the %s regional transit provider in settings without exposing keys", async (country, label) => {
    const runtime = {
      ekispert_enabled: true,
      odsay_enabled: true,
      navitime_enabled: true,
      naver_directions_enabled: true,
      google_routes_enabled: true,
    };
    const fetchMock = vi.fn().mockImplementation((url: string) => Promise.resolve(response(
      url.includes("/runtime/public-config") ? runtime : { ...trip, destination_country_code: country },
    )));
    vi.stubGlobal("fetch", fetchMock);

    render(<TripEditor tripId={trip.id} />);

    await openToolsSection("旅程設定");
    expect(await screen.findByText(label)).toBeTruthy();
    expect(screen.queryByText("NAVITIME · 日本備援")).toBeNull();
    expect(JSON.stringify(fetchMock.mock.calls)).not.toContain("server-key");
  });

  it("surfaces fallback warnings and jumps to a day from an unscheduled slot", async () => {
    const fallbackTrip = {
      ...trip,
      start_date: "2026-11-11",
      end_date: "2026-11-12",
      items: [
        trip.items[0],
        { ...trip.items[0], id: "00000000-0000-4000-8000-000000000011", day_date: "2026-11-12", title: "晴空塔" },
      ],
      planning: {
        status: "fallback" as const,
        readiness: "partial" as const,
        provider: "catalog" as const,
        model: null,
        generated_at: "2026-11-01T10:00:00Z",
        scope: "trip" as const,
        // Codes now, plus one sentence in the shape trips planned before this change
        // still carry in storage.
        warnings: [
          "planner_provider_failed",
          "planner_fallback_used",
          // Two sentences in the shape trips planned before this change still carry in
          // storage. Both collapse onto the generic line, which must appear once.
          "minimax 暫時無法產生有效行程（HTTPStatusError）",
          "有 11 個時段因正式地點不足而保留空白",
        ],
        unscheduled_slots: [{ date: "2026-11-12", slot: "lunch" as const }],
      },
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(fallbackTrip))));

    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByText("AI 暫時無法使用，已套用核准目錄備援行程")).toBeTruthy();
    const reminders = screen.getByRole("list", { name: "AI 安排提醒" });
    expect(within(reminders).getByText("AI 這次沒排出行程")).toBeTruthy();
    expect(within(reminders).getByText("已改用審核過的景點目錄先排一版，你可以直接調整")).toBeTruthy();
    // A traveller never sees our provider code or an httpx exception class, including on
    // trips planned before the API started sending codes.
    expect(within(reminders).queryByText(/minimax/)).toBeNull();
    expect(within(reminders).queryByText(/HTTPStatusError/)).toBeNull();
    expect(within(reminders).getAllByText("這次安排有一項提醒，重新產生行程通常就會消失")).toHaveLength(1);

    fireEvent.click(screen.getByRole("button", { name: "11/12 午餐" }));
    await waitFor(() => {
      const dayChip = screen.getAllByRole("button", { pressed: true }).find((button) => button.textContent?.includes("11/12"));
      expect(dayChip).toBeTruthy();
    });
  });

  it("shows durable catalog coordinates as a confirmed place", async () => {
    const exactCatalogTrip = {
      ...trip,
      items: [{
        ...trip.items[0],
        title: "淺草寺",
        location_name: "淺草寺",
        latitude: 35.7148,
        longitude: 139.7967,
        location_source: "hotspot_catalog",
        data: { needs_place_confirmation: false, hotspot_id: "hotspot-1" },
      }],
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(exactCatalogTrip))));

    render(<TripEditor tripId={trip.id} />);

    await openStopEditor("淺草寺");
    expect(await screen.findByText("地點已確認，可計算路線")).toBeTruthy();
    expect(screen.queryByText("尚未設定")).toBeNull();
  });

  it("shows a catalog stop's original-script name under the localized title", async () => {
    const localizedTrip = {
      ...trip,
      items: [{
        ...trip.items[0],
        title: "淺草寺",
        location_name: "淺草寺",
        names: {
          title: { "zh-TW": "淺草寺", en: "Sensō-ji", ja: "浅草寺", original: "浅草寺", original_locale: "ja" },
          location_name: { "zh-TW": "淺草寺", en: "Sensō-ji", ja: "浅草寺", original: "浅草寺", original_locale: "ja" },
        },
        data: { hotspot_id: "hotspot-1" },
      }],
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(localizedTrip))));

    render(<TripEditor tripId={trip.id} />);

    const editor = await openStopEditor("淺草寺");
    fireEvent.click(within(editor).getByText("地點詳情", { selector: "summary" }));
    expect(await screen.findByText("浅草寺")).toBeTruthy();
    expect(screen.getByText("浅草寺").getAttribute("lang")).toBe("ja");
    expect(screen.getByRole("heading", { name: "淺草寺" })).toBeTruthy();
  });

  it("uses one honest count and one compact lodging prompt before a hotel is set", async () => {
    const unsetLodgingTrip = {
      ...trip,
      start_date: "2026-11-11",
      end_date: "2026-11-11",
      primary_lodging: null,
      items: [
        {
          ...trip.items[0],
          latitude: 35.7148,
          longitude: 139.7967,
          location_source: "hotspot_catalog",
        },
        {
          ...trip.items[0],
          id: "00000000-0000-4000-8000-000000000010",
          position: -1,
          item_type: "hotel_anchor",
          title: "從 尚未設定飯店 出發",
          location_name: null,
          system_role: "hotel_start" as const,
          fixed_time: true,
          data: { needs_place_confirmation: true },
        },
        {
          ...trip.items[0],
          id: "00000000-0000-4000-8000-000000000011",
          position: 99,
          item_type: "hotel_anchor",
          title: "返回 尚未設定飯店",
          location_name: null,
          system_role: "hotel_end" as const,
          data: { needs_place_confirmation: true },
        },
        {
          ...trip.items[0],
          id: "00000000-0000-4000-8000-000000000012",
          position: 3,
          item_type: "meal",
          title: "午餐尚未安排",
          location_name: null,
          system_role: "lunch" as const,
          fixed_time: true,
          data: { needs_place_confirmation: true },
        },
      ],
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(unsetLodgingTrip))));

    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findAllByText("1 個已安排")).not.toHaveLength(0);
    const extras = screen.getByText("補充安排", { selector: "summary span" }).closest("details")!;
    expect(extras.open).toBe(false);
    expect(screen.queryByText("先設定飯店地點")).toBeNull();
    expect(screen.queryByText("交通待確認")).toBeNull();
    fireEvent.click(extras.querySelector("summary")!);
    expect(within(extras).getByRole("button", { name: "從 尚未設定飯店 出發" })).toBeTruthy();
    expect(screen.queryByText("返回 尚未設定飯店")).toBeNull();
    expect(within(extras).getByRole("button", { name: "午餐尚未安排" })).toBeTruthy();
    expect(screen.getAllByRole("heading", { level: 3 }).map((node) => node.textContent)).toEqual(["淺草散步"]);
  });

  it("opens mobile trip tools and remembers the selected color theme", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    const { container } = render(<TripEditor tripId={trip.id} />);

    await openToolsSection("旅程設定");
    expect(screen.getByRole("dialog", { name: "旅程工具" })).toBeTruthy();
    expect(screen.getByRole("group", { name: "路線偏好" })).toBeTruthy();

    fireEvent.click(screen.getByRole("radio", { name: /海岸/ }));
    expect(container.querySelector("[data-planner-theme='ocean']")).toBeTruthy();
    expect(window.localStorage.getItem("travel-planner-theme")).toBe("ocean");
  }, 10_000);

  it("inserts a new stop at the chosen position, not at the end", async () => {
    const twoStopTrip = {
      ...trip,
      items: [
        trip.items[0],
        {
          ...trip.items[0],
          id: "00000000-0000-4000-8000-000000000003",
          position: 1,
          title: "晴空塔",
          location_name: "押上",
        },
      ],
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation((_input, init) => Promise.resolve(response(init?.method === "PUT" ? { ...twoStopTrip, version: 2, items: JSON.parse(String(init.body)).items } : twoStopTrip))));
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByRole("heading", { name: "晴空塔" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "排序行程" }));
    fireEvent.click(screen.getAllByRole("button", { name: "在 晴空塔 前插入新安排" })[0]);
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    fireEvent.change(screen.getByLabelText("安排名稱"), { target: { value: "雷門" } });
    fireEvent.click(screen.getByRole("button", { name: "加入行程" }));

    await screen.findByRole("heading", { name: "雷門" });
    const headings = screen.getAllByRole("heading", { level: 3 }).map((node) => node.textContent);
    expect(headings.indexOf("雷門")).toBeGreaterThan(headings.indexOf("淺草散步"));
    expect(headings.indexOf("雷門")).toBeLessThan(headings.indexOf("晴空塔"));
  });

  it("does nothing at all when moving the first item up", async () => {
    const twoStopTrip = {
      ...trip,
      items: [
        trip.items[0],
        {
          ...trip.items[0],
          id: "00000000-0000-4000-8000-000000000003",
          position: 1,
          title: "晴空塔",
          location_name: "押上",
        },
      ],
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(twoStopTrip))));
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "晴空塔" });
    fireEvent.click(screen.getByRole("button", { name: "排序行程" }));
    // The arrows at the edges are disabled — a no-op tap used to wipe the
    // day's computed routes and mark the trip dirty.
    expect((screen.getByRole("button", { name: "上移 淺草散步" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "下移 晴空塔" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "下移 淺草散步" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("lets the reader dismiss an error toast", async () => {
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "DELETE") {
        return Promise.resolve({ ok: false, status: 500, json: async () => ({ detail: "撤銷失敗" }) });
      }
      return Promise.resolve(response({ ...trip, share_enabled: true }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openToolsSection("分享與匯出");
    fireEvent.click(screen.getByRole("button", { name: "撤銷目前分享連結" }));
    fireEvent.click(await screen.findByRole("button", { name: "撤銷連結" }));

    expect(await screen.findByRole("alert")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "關閉錯誤訊息" }));
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("offers one responsive trip-tools entry in the shared header", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    render(<TripEditor tripId={trip.id} />);

    await screen.findAllByText("東京五日");
    const header = screen.getByRole("heading", { name: "東京五日" }).closest("header")!;
    expect(screen.getAllByRole("button", { name: "開啟旅程工具" })).toHaveLength(1);
    fireEvent.click(within(header).getByRole("button", { name: "開啟旅程工具" }));
    expect(screen.getByRole("dialog", { name: "旅程工具" })).toBeTruthy();
  });

  it("saves a day note against the trip version", async () => {
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL) => {
      if (String(input).includes("/days/")) {
        return Promise.resolve(response({ ...trip, version: 2, day_notes: { "2026-11-11": "這天要先訂位" } }));
      }
      return Promise.resolve(response(trip));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findByText("加上這天的備註"));
    const box = screen.getByLabelText("這天的備註");
    fireEvent.change(box, { target: { value: "這天要先訂位" } });
    fireEvent.click(within(box.closest("details")!).getByRole("button", { name: "儲存" }));

    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([url]) => String(url).includes("/days/2026-11-11/notes"));
      expect(call).toBeTruthy();
      expect((call?.[1] as RequestInit).method).toBe("PUT");
      expect(JSON.parse(String((call?.[1] as RequestInit).body))).toEqual({
        version: 1,
        notes: "這天要先訂位",
      });
    });
  });

  it("keeps the toolbar during reordering, swapping it for a done button", async () => {
    const twoStopTrip = {
      ...trip,
      items: [
        trip.items[0],
        {
          ...trip.items[0],
          id: "00000000-0000-4000-8000-000000000003",
          position: 1,
          title: "晴空塔",
          location_name: "押上",
        },
      ],
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(twoStopTrip))));
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByRole("toolbar", { name: "行程快速操作" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "排序行程" }));

    // The dock stays: reordering must not hide the save indicator, and the way
    // out is an explicit 完成排序 in the same thumb-reach spot.
    const toolbar = screen.getByRole("toolbar", { name: "行程快速操作" });
    expect(within(toolbar).getByRole("button", { name: "完成排序" })).toBeTruthy();
    expect(within(toolbar).queryByRole("button", { name: "新增安排" })).toBeNull();
    expect(screen.getByRole("button", { name: "上移 晴空塔" })).toBeTruthy();
    fireEvent.click(within(toolbar).getByRole("button", { name: "完成排序" }));
    expect(within(toolbar).getByRole("button", { name: "新增安排" })).toBeTruthy();
  });

  it("lets the user ask MiniMax to arrange only the selected day", async () => {
    let previewBody: Record<string, unknown> | undefined;
    let applyBody: Record<string, unknown> | undefined;
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.includes("/itinerary/preview")) {
        previewBody = JSON.parse(String(init?.body));
        return response(itineraryPreview("day"));
      }
      if (url.includes("/itinerary/apply")) {
        applyBody = JSON.parse(String(init?.body));
        return response({
          ...trip,
          version: 2,
          planning: {
            status: "live", readiness: "ready",
            provider: "minimax",
            model: "MiniMax-M2.1",
            generated_at: "2026-11-01T10:00:00Z",
            warnings: [],
            scope: "day",
            day_date: "2026-11-11",
          },
          usage: { status: "charged", uses: 1, reference: "ai-day-1" },
          items: [{
            ...trip.items[0],
            title: "MiniMax 安排的淺草寺",
            location_name: "淺草寺",
            latitude: 35.7148,
            longitude: 139.7967,
            data: { generated_by: "ai_planner", hotspot_id: "hotspot-1" },
          }],
        });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openAI();
    expect(screen.getByRole("dialog", { name: "AI 幫我安排" })).toBeTruthy();
    const singleDay = screen.getByRole("radio", { name: /\u55ae\u65e5\u5b89\u6392/ });
    fireEvent.click(singleDay);
    expect(singleDay.className).toContain("text-violet-950");
    expect(within(singleDay).getByText(/目前 1 個已安排/).className).toContain("text-violet-700");
    fireEvent.click(screen.getByRole("button", { name: /^產生預覽/ }));

    await waitFor(() => expect(previewBody).toEqual({
      version: 1,
      scope: "day",
      day_date: "2026-11-11",
    }));
    expect(screen.getByText("淺草散步")).toBeTruthy();
    expect(await screen.findByRole("dialog", { name: "確認 AI 行程預覽" })).toBeTruthy();
    expect(screen.getByText("MiniMax 安排的淺草寺")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /^套用行程/ }));
    await waitFor(() => expect(applyBody).toEqual({ version: 1, preview_id: "preview-day" }));
    expect(await screen.findByText(/MiniMax 已套用.*並扣除 1 次/)).toBeTruthy();
    expect(screen.getByText("MiniMax 安排的淺草寺")).toBeTruthy();
    const editor = await openStopEditor("MiniMax 安排的淺草寺");
    fireEvent.click(within(editor).getByText("地點詳情", { selector: "summary" }));
    expect(within(editor).getByText("AI 建議")).toBeTruthy();
  });

  it("offers a full-trip AI arrangement from the same menu", async () => {
    let previewBody: Record<string, unknown> | undefined;
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.includes("/itinerary/preview")) {
        previewBody = JSON.parse(String(init?.body));
        return response(itineraryPreview("trip"));
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openAI();
    const fullTrip = screen.getByRole("radio", { name: /\u5168\u884c\u7a0b\u5b89\u6392/ });
    fireEvent.click(fullTrip);
    expect(fullTrip.getAttribute("aria-checked")).toBe("true");
    fireEvent.click(screen.getByRole("button", { name: /^產生預覽/ }));

    await waitFor(() => expect(previewBody).toEqual({
      version: 1,
      scope: "trip",
      day_date: null,
    }));
    expect(await screen.findByRole("dialog", { name: "確認 AI 行程預覽" })).toBeTruthy();
  });

  it("keeps a new stop as a draft until the user confirms it", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        return response({ ...trip, version: 2, items: body.items });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openAddFromToolbar();
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    expect(screen.getByRole("dialog", { name: "新增安排" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "加入行程" }).hasAttribute("disabled")).toBe(true);
    fireEvent.click(within(screen.getByRole("dialog", { name: "新增安排" })).getByRole("button", { name: "取消" }));
    expect(screen.queryByRole("dialog", { name: "新增安排" })).toBeNull();
    expect(fetchMock.mock.calls.some(([, init]) => init?.method === "PUT")).toBe(false);

    await openAddFromToolbar();
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    fireEvent.change(screen.getByLabelText("安排名稱"), { target: { value: "銀座午餐" } });
    fireEvent.click(screen.getByRole("button", { name: "加入行程" }));
    expect(await screen.findByText("銀座午餐")).toBeTruthy();
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "PUT")).toBe(true), { timeout: 2_000 });
  });

  it("supports short, half-day, and full-day stop durations", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        return response({ ...trip, version: 2, items: body.items });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openAddFromToolbar();
    fireEvent.click(screen.getByRole("button", { name: "自行填寫行程" }));
    fireEvent.change(screen.getByLabelText("安排名稱"), { target: { value: "輕井澤一日遊" } });
    const duration = screen.getByLabelText("停留時間");
    expect(within(duration).getByRole("option", { name: "20 分鐘" })).toBeTruthy();
    expect(within(duration).getByRole("option", { name: "2.5 小時" })).toBeTruthy();
    expect(within(duration).getByRole("option", { name: "4 小時" })).toBeTruthy();
    fireEvent.change(duration, { target: { value: "540" } });
    fireEvent.click(screen.getByRole("button", { name: "加入行程" }));

    expect(await screen.findByText("停留 540 分鐘")).toBeTruthy();
    await waitFor(() => {
      expect(fetchMock.mock.calls.some(([, init]) => {
        if (init?.method !== "PUT") return false;
        const body = JSON.parse(String(init.body)) as { items: Array<{ title: string; duration_minutes?: number }> };
        return body.items.some((item) => item.title === "輕井澤一日遊" && item.duration_minutes === 540);
      })).toBe(true);
    }, { timeout: 2_000 });
  });

  it("edits and saves an itinerary with the current version", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        return response({ ...trip, version: 2, items: body.items });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    const title = screen.getByLabelText("安排名稱");
    fireEvent.change(title, { target: { value: "淺草與晴空塔" } });
    await saveEditor(editor);
    expect(screen.queryByRole("dialog", { name: "編輯安排" })).toBeNull();
    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([, init]) => init?.method === "PUT");
      expect(call).toBeTruthy();
      const body = JSON.parse(String(call?.[1]?.body));
      expect(body.version).toBe(1);
      expect(body.items[0].title).toBe("淺草與晴空塔");
    }, { timeout: 2_000 });
  });

  it("switches an activity from chained timing to a fixed local time", async () => {
    let savedBody: { items: Array<{ fixed_time?: boolean; start_time?: string | null }> } | undefined;
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        savedBody = JSON.parse(String(init.body));
        return response({ ...trip, version: 2, items: savedBody?.items });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    const editor = await openStopEditor("淺草散步");
    expect(screen.getByRole("radio", { name: "接續前站" }).getAttribute("aria-checked")).toBe("true");
    fireEvent.click(screen.getByRole("radio", { name: "固定時間" }));
    fireEvent.change(screen.getByLabelText("固定開始時間"), { target: { value: "15:20" } });
    await saveEditor(editor);

    await waitFor(() => expect(savedBody).toBeTruthy(), { timeout: 2_000 });
    expect(savedBody?.items[0].fixed_time).toBe(true);
    expect(savedBody?.items[0].start_time).toContain("T15:20:00");
  });

  it("saves a manual outbound flight without sending it through itinerary autosave", async () => {
    const outbound = {
      id: "00000000-0000-4000-8000-000000000010",
      item_type: "flight",
      day_date: "2026-11-11",
      position: 0,
      title: "去程航班尚未設定",
      locked: true,
      fixed_time: true,
      is_estimated: true,
      system_role: "outbound_flight" as const,
      data: { flight_info: null },
    };
    const flightTrip = { ...trip, items: [outbound, { ...trip.items[0], position: 1 }] };
    let flightBody: Record<string, unknown> | undefined;
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.includes("/flight-anchors/outbound")) {
        flightBody = JSON.parse(String(init?.body));
        const flight = (flightBody?.flight || {}) as Record<string, unknown>;
        return response({
          ...flightTrip,
          version: 2,
          items: [{
            ...outbound,
            title: "長榮航空 BR 198",
            is_estimated: false,
            data: { flight_selection_source: "manual", flight_info: flight },
          }, flightTrip.items[1]],
        });
      }
      return response(flightTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    openOptionalStop("去程航班尚未設定");
    fireEvent.click(await screen.findByRole("button", { name: "設定去程航班" }));
    fireEvent.change(screen.getByLabelText("航空公司"), { target: { value: "長榮航空" } });
    fireEvent.change(screen.getByLabelText("班號"), { target: { value: "BR 198" } });
    fireEvent.change(screen.getByLabelText("出發機場"), { target: { value: "tpe" } });
    fireEvent.change(screen.getByLabelText("抵達機場"), { target: { value: "nrt" } });
    fireEvent.change(screen.getByLabelText("當地起飛時間"), { target: { value: "2026-11-11T08:50" } });
    fireEvent.change(screen.getByLabelText("當地抵達時間"), { target: { value: "2026-11-11T13:10" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存航班" }));

    await waitFor(() => expect(flightBody).toBeTruthy());
    expect(flightBody).toMatchObject({
      version: 1,
      flight: { airline: "長榮航空", flight_number: "BR 198", origin: "TPE", destination: "NRT" },
    });
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("/itinerary"))).toBe(false);
    expect(await screen.findByText("長榮航空 BR 198")).toBeTruthy();
  });

  it("offers the printable itinerary and the partner platforms from the tools drawer", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      if (String(url).includes("/affiliates/options")) {
        const affiliateModule = new URL(url, "https://mokaair.com").searchParams.get("module");
        return response({
          module: affiliateModule,
          disclosure: "本站可能因此獲得分潤。",
          options: affiliateModule === "hotel" ? [{ partner: "travelpayouts", display_name: "Travelpayouts", module: "hotel", cta: "查看住宿", clickout_url: "/api/travel/affiliates/click" }] : [],
        });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    const tools = await openToolsSection("分享與匯出");

    const print = await screen.findByRole("link", { name: "開啟列印版" });
    expect(print.getAttribute("href")).toBe(`/trips/${trip.id}/print`);
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/affiliates/options"))).toBe(false);
    fireEvent.click(within(tools).getByRole("button", { name: "返回" }));
    fireEvent.click(within(tools).getByRole("button", { name: /^旅行準備/ }));
    await waitFor(() => expect(screen.getAllByRole("button", { name: /查看住宿/ }).length).toBeGreaterThan(0));
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes(`trip_id=${trip.id}`))).toBe(true);
  });

  it("saves the final draft explicitly before requesting optimization with its new version", async () => {
    const editableTrip = { ...trip, items: [...trip.items, { ...trip.items[0], id: "other", position: 1, title: "晴空塔" }] };
    let finishSave!: (value: ReturnType<typeof response>) => void;
    const putBodies: Array<{ version: number; items: typeof trip.items }> = [];
    const preview = { preview_id: "optimization-1", expires_at: "2026-11-01T10:10:00Z", base_version: 2,
      route_preference: "FEWER_TRANSFERS", changed: false, warnings: [], segments: [],
      total_duration_before_minutes: 0, total_duration_after_minutes: 0, charge_on_apply: 1, days: [] };
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        putBodies.push(JSON.parse(String(init.body)));
        return new Promise<ReturnType<typeof response>>((resolve) => { finishSave = resolve; });
      }
      if (url.includes("/optimize/preview")) return response(preview);
      return response(editableTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    const title = within(editor).getByLabelText("安排名稱");
    fireEvent.change(title, { target: { value: "第一次修改" } });
    fireEvent.change(title, { target: { value: "最後一次修改" } });
    expect(putBodies).toHaveLength(0);
    fireEvent.click(within(editor).getByRole("button", { name: "儲存修改" }));
    await waitFor(() => expect(putBodies).toHaveLength(1));
    expect((title as HTMLInputElement).matches(":disabled")).toBe(true);
    fireEvent.click(within(editor).getByRole("button", { name: "關閉" }));
    expect(screen.getByRole("dialog", { name: "編輯安排" })).toBeTruthy();
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/optimize/preview"))).toBe(false);
    await act(async () => finishSave(response({ ...editableTrip, version: 2, items: putBodies[0].items })));
    await openAI();
    fireEvent.click(screen.getByRole("button", { name: "只順路排序" }));
    fireEvent.click(screen.getByRole("button", { name: "產生預覽 · 不扣次" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/optimize/preview"))).toBe(true));
    expect(putBodies).toHaveLength(1);
    expect(putBodies[0].version).toBe(1);
    expect(putBodies[0].items[0].title).toBe("最後一次修改");
    const [, request] = fetchMock.mock.calls.find(([url]) => String(url).includes("/optimize/preview"))!;
    expect(JSON.parse(String(request?.body)).version).toBe(2);
  });

  it("offers to lock the extra stops instead of letting the optimiser refuse the day", async () => {
    const crowdedDay = {
      ...trip,
      items: [
        trip.items[0],
        ...Array.from({ length: 12 }, (_, index) => ({
          ...trip.items[0],
          id: `00000000-0000-4000-8000-0000000001${String(index).padStart(2, "0")}`,
          position: index + 1,
          title: `停留點 ${index + 1}`,
          latitude: 35.7 + index / 1000,
          longitude: 139.8 + index / 1000,
        })),
      ],
      optimization: { movable_limit: 12, days: [{ date: "2026-11-11", movable_count: 13 }] },
    };
    const fetchMock = vi.fn(async (url: string) => (url ? response(crowdedDay) : response(crowdedDay)));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openAI();
    fireEvent.click(screen.getByRole("button", { name: "只順路排序" }));
    fireEvent.click(screen.getByRole("button", { name: "產生預覽 · 不扣次" }));

    expect(await screen.findByText(/一次最多排 12 個/)).toBeTruthy();
    expect(screen.getByText(/鎖定 1 個之後就能最佳化/)).toBeTruthy();
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/optimize/preview"))).toBe(false);

    fireEvent.click(screen.getByRole("button", { name: "鎖定當天最後 1 個" }));
    expect(await screen.findByText("已鎖定 1 個停留點，可以再按一次最佳化。")).toBeTruthy();
  });

  it("previews an optimization before applying and charging it", async () => {
    const twoStopTrip = {
      ...trip,
      items: [
        trip.items[0],
        { ...trip.items[0], id: "00000000-0000-4000-8000-000000000003", position: 1, title: "晴空塔", location_name: "押上" },
      ],
    };
    const preview = {
      preview_id: "00000000-0000-4000-8000-000000000099",
      expires_at: "2026-11-01T10:10:00Z",
      base_version: 1,
      route_preference: "FEWER_TRANSFERS",
      changed: true,
      warnings: [],
      segments: [],
      total_duration_before_minutes: 45,
      total_duration_after_minutes: 25,
      charge_on_apply: 1,
      days: [{
        date: "2026-11-11", duration_before_minutes: 45, duration_after_minutes: 25, saved_minutes: 20,
        before: twoStopTrip.items.map((item, index) => ({ id: item.id, title: item.title, position: index, locked: false, fixed_time: false })),
        after: [...twoStopTrip.items].reverse().map((item, index) => ({ id: item.id, title: item.title, position: index, locked: false, fixed_time: false })),
      }],
    };
    let applyAttempts = 0;
    const fetchMock = vi.fn(async (url: string, _init?: RequestInit) => {
      void _init;
      if (url.includes("/optimize/preview")) return response(preview);
      if (url.includes("/optimize/apply")) {
        applyAttempts += 1;
        if (applyAttempts === 1) throw new TypeError("連線中斷");
        return response({ ...twoStopTrip, version: 2, usage: { status: "charged", uses: 1, reference: "use-1" } });
      }
      return response(twoStopTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    await openAI();
    fireEvent.click(screen.getByRole("button", { name: "只順路排序" }));
    fireEvent.click(screen.getByRole("button", { name: "產生預覽 · 不扣次" }));
    expect(await screen.findByRole("dialog", { name: "最佳化預覽" })).toBeTruthy();
    expect(screen.getByText("預計節省")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /^套用 · 消耗 1 次/ }));
    expect(await screen.findByText(/結果尚未確認/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /^套用 · 消耗 1 次/ }));
    expect(await screen.findByText(/已套用最佳動線並扣除 1 次/)).toBeTruthy();
    const applyCalls = fetchMock.mock.calls.filter(([url]) => String(url).includes("/optimize/apply"));
    expect(applyCalls).toHaveLength(2);
    expect((applyCalls[0][1]?.headers as Record<string, string>)["Idempotency-Key"])
      .toBe((applyCalls[1][1]?.headers as Record<string, string>)["Idempotency-Key"]);
  });

  it("keeps delete recoverable from the mobile-friendly editor", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.click(within(editor).getByRole("button", { name: "刪除這個安排" }));
    expect(screen.getByText(/8 秒內復原/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "復原" }));
    expect(await screen.findByText("淺草散步")).toBeTruthy();
  });

  it("restores an unsynced local draft for the same server version", async () => {
    window.localStorage.setItem(`trip-planner-draft:${trip.id}`, JSON.stringify({
      baseVersion: 1,
      savedAt: new Date().toISOString(),
      items: [{ ...trip.items[0], title: "離線保存的淺草行程" }],
      routePreference: "FEWER_TRANSFERS",
    }));
    vi.stubGlobal("fetch", vi.fn().mockImplementation((_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        return Promise.resolve(response({ ...trip, version: 2, items: body.items }));
      }
      return Promise.resolve(response(trip));
    }));
    render(<TripEditor tripId={trip.id} />);
    expect(await screen.findByText("離線保存的淺草行程")).toBeTruthy();
    expect(screen.getByText(/已復原尚未同步的本機草稿/)).toBeTruthy();
  });

  it("opens the mobile route sheet expanded for its map, allows collapse, and closes on back", async () => {
    const destination = {
      ...trip.items[0],
      id: "00000000-0000-4000-8000-000000000003",
      position: 1,
      title: "晴空塔",
      location_name: "押上",
    };
    const routedTrip = {
      ...trip,
      items: [{ ...trip.items[0], latitude: 35.71, longitude: 139.79 }, { ...destination, latitude: 35.71, longitude: 139.8 }],
      route_segments: [{
        from_item_id: trip.items[0].id,
        to_item_id: destination.id,
        status: "available",
        provider: "google",
        attribution: "Google Maps",
        generated_at: "2026-11-01T10:00:00Z",
        schedule_mode: "scheduled",
        preference: "FEWER_TRANSFERS",
        duration_minutes: 18,
        steps: [],
        details_available: [],
        warnings: [],
      }],
    };
    vi.stubGlobal("matchMedia", vi.fn((query: string) => ({
      matches: query.includes("max-width"),
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })));
    vi.stubGlobal("fetch", vi.fn().mockImplementation((url: string) => Promise.resolve(
      response(url.includes("/runtime/public-config") ? { google_maps_browser_key: null } : routedTrip),
    )));
    render(<TripEditor tripId={trip.id} />);
    const routeButton = await screen.findByRole(
      "button",
      { name: /^查看前往 晴空塔 的路線/ },
      { timeout: 5_000 },
    );
    fireEvent.click(routeButton);
    expect(await screen.findByRole("dialog", { name: "這段路怎麼走" })).toBeTruthy();
    const collapse = screen.getByRole("button", { name: "縮小面板" });
    expect(collapse.getAttribute("aria-expanded")).toBe("true");
    fireEvent.click(collapse);
    expect(screen.getByRole("button", { name: "展開面板" }).getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(screen.getByRole("button", { name: "展開面板" }));
    expect(screen.getByRole("button", { name: "縮小面板" }).getAttribute("aria-expanded")).toBe("true");
    fireEvent.popState(window);
    await waitFor(() => expect(screen.queryByRole("dialog", { name: "這段路怎麼走" })).toBeNull());
  });

  it("shows the scheduled and projected time when a fixed booking will be late", async () => {
    const fixed = {
      ...trip.items[0],
      id: "00000000-0000-4000-8000-000000000004",
      position: 1,
      title: "壽司預約",
      fixed_time: true,
      start_time: "2026-11-11T05:00:00Z",
    };
    const conflictTrip = {
      ...trip,
      items: [trip.items[0], fixed],
      routing: {
        status: "complete",
        total: 1,
        completed: 1,
        day_settings: [],
        conflicts: [{
          item_id: fixed.id,
          title: fixed.title,
          scheduled_start_time: "2026-11-11T05:00:00Z",
          projected_start_time: "2026-11-11T05:18:00Z",
          late_minutes: 18,
          suggestions: ["提早離開前一站", "改用汽車"],
        }],
      },
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(conflictTrip))));
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "壽司預約" });
    fireEvent.click(screen.getByText("檢查這一天", { selector: "summary" }));
    const warning = await screen.findByRole("button", { name: /預定 .*／預計 .*，可能遲到 18 分鐘/ });
    fireEvent.click(warning);
    const editor = await screen.findByRole("dialog", { name: "編輯安排" });
    expect((within(editor).getByLabelText("安排名稱") as HTMLInputElement).value).toBe("壽司預約");
  });

  const hotelStart = {
    id: "00000000-0000-4000-8000-000000000010",
    item_type: "hotel_anchor",
    system_role: "hotel_start",
    day_date: "2026-11-11",
    position: 0,
    title: "從 尚未設定飯店 出發",
    location_name: null,
    fixed_time: true,
    start_time: "2026-11-11T09:00:00",
    duration_minutes: 0,
    locked: true,
    is_estimated: true,
    data: { needs_place_confirmation: true },
  };

  it("keeps an unset hotel optional instead of inventing its departure leg", async () => {
    const stop = { ...trip.items[0], position: 1, duration_minutes: 60 };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, stop] }),
    )));
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByRole("heading", { name: "淺草散步" })).toBeTruthy();
    expect(screen.queryByText("先設定飯店地點")).toBeNull();
    expect(screen.queryByRole("button", { name: /查看前往 淺草散步 的路線/ })).toBeNull();
    const extras = screen.getByText("補充安排", { selector: "summary span" }).closest("details")!;
    expect(extras.open).toBe(false);
    fireEvent.click(extras.querySelector("summary")!);
    expect(within(extras).getByRole("button", { name: "從 尚未設定飯店 出發" })).toBeTruthy();
  });

  it("does not label chained times as certain when coordinates and movement are unknown", async () => {
    const stop = { ...trip.items[0], position: 1, duration_minutes: 60 };
    const later = { ...trip.items[0], id: "00000000-0000-4000-8000-000000000011", position: 2, title: "晴空塔", duration_minutes: 60 };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, stop, later] }),
    )));
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "晴空塔" });
    expect(screen.getAllByText("時間待確認")).toHaveLength(2);
    expect(screen.getByText("交通待確認")).toBeTruthy();
    expect(screen.queryByText("接續前站 · 約 09:10")).toBeNull();
    expect(screen.queryByText("接續前站 · 約 10:20")).toBeNull();
  });

  it("saves a new daily departure time from the trip tools panel", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, { ...trip.items[0], position: 1 }] }),
    ));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await openToolsSection("旅程設定");
    const departure = screen.getByLabelText("每日從飯店出發時間") as HTMLInputElement;
    expect(departure.value).toBe("09:00");

    fireEvent.change(departure, { target: { value: "08:15" } });
    fireEvent.click(screen.getByRole("button", { name: /套用到所有日期/ }));

    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(true));
    const [, request] = fetchMock.mock.calls.find(([url]) => String(url).includes("/schedule-defaults")) as [string, RequestInit];
    expect(JSON.parse(String(request.body)).day_start_time).toBe("08:15");
  });

  it("keeps route preferences as a guarded draft and saves without querying routes", async () => {
    const preferenceTrip = { ...trip, route_preference: "FEWER_TRANSFERS" };
    const fetchMock = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => {
      if (String(url).endsWith("/itinerary") && init?.method === "PUT") {
        const payload = JSON.parse(String(init.body));
        return response({ ...preferenceTrip, version: 2, route_preference: payload.route_preference });
      }
      return response(preferenceTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const tools = await openToolsSection("旅程設定");
    const choices = within(tools).getByRole("group", { name: "路線偏好" });
    const section = choices.closest("section")!;
    const fastest = within(choices).getByRole("button", { name: "最快" });
    const writes = () => fetchMock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET");

    fireEvent.click(fastest);
    expect(fastest.getAttribute("aria-pressed")).toBe("true");
    expect(writes()).toHaveLength(0);
    fireEvent.click(within(tools).getByRole("button", { name: "返回" }));
    const guard = await screen.findByRole("dialog", { name: "保留這次修改嗎？" });
    fireEvent.click(within(guard).getByRole("button", { name: "繼續編輯" }));
    expect(within(tools).getByRole("group", { name: "路線偏好" })).toBe(choices);
    expect(fastest.getAttribute("aria-pressed")).toBe("true");
    fireEvent.click(within(section).getByRole("button", { name: "取消" }));
    expect(within(choices).getByRole("button", { name: "少轉乘" }).getAttribute("aria-pressed")).toBe("true");
    expect(writes()).toHaveLength(0);

    fireEvent.click(fastest);
    fireEvent.click(within(section).getByRole("button", { name: "儲存修改" }));
    await waitFor(() => expect(writes()).toHaveLength(1));
    expect(writes()[0][0]).toContain(`/trips/${trip.id}/itinerary`);
    expect(JSON.parse(String(writes()[0][1]?.body))).toMatchObject({ version: 1, route_preference: "FASTEST", items: trip.items });
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/"))).toBe(false);
  });

  it("keeps the tools and unsaved trip note open after saving the trip name", async () => {
    let currentTrip = { ...trip, notes: "已儲存的提醒" };
    const fetchMock = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => {
      if (String(url).endsWith(`/trips/${trip.id}`) && init?.method === "PATCH") {
        currentTrip = { ...currentTrip, ...JSON.parse(String(init.body)), version: currentTrip.version + 1 };
      }
      return response(currentTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const tools = await openToolsSection("旅程設定");
    const note = within(tools).getByLabelText("旅程備註") as HTMLTextAreaElement;
    fireEvent.change(note, { target: { value: "未儲存的訂位提醒" } });
    fireEvent.click(within(tools).getByRole("button", { name: /旅程資訊/ }));
    const meta = await screen.findByRole("dialog", { name: "旅程資訊" });
    fireEvent.change(within(meta).getByLabelText("旅程名稱"), { target: { value: "東京安心旅行" } });
    fireEvent.click(within(meta).getByRole("button", { name: "儲存變更" }));

    await waitFor(() => expect(screen.queryByRole("dialog", { name: "旅程資訊" })).toBeNull());
    expect(screen.getByRole("dialog", { name: "旅程工具" })).toBe(tools);
    expect(within(tools).getByLabelText("旅程備註")).toBe(note);
    expect(note.value).toBe("未儲存的訂位提醒");
    expect(currentTrip.notes).toBe("已儲存的提醒");
    expect(currentTrip.name).toBe("東京安心旅行");
    const writes = fetchMock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET");
    expect(writes).toHaveLength(1);
    expect(JSON.parse(String(writes[0][1]?.body))).toEqual({ version: 1, name: "東京安心旅行" });
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/"))).toBe(false);
  });

  it("saves a route preference draft after another setting advanced the trip version", async () => {
    let currentTrip = { ...trip, route_preference: "FEWER_TRANSFERS", notes: "" };
    const fetchMock = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => {
      if ((String(url).endsWith(`/trips/${trip.id}`) && init?.method === "PATCH")
        || (String(url).endsWith("/itinerary") && init?.method === "PUT")) {
        currentTrip = { ...currentTrip, ...JSON.parse(String(init.body)), version: currentTrip.version + 1 };
      }
      return response(currentTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const tools = await openToolsSection("旅程設定");
    const choices = within(tools).getByRole("group", { name: "路線偏好" });
    const fastest = within(choices).getByRole("button", { name: "最快" });
    fireEvent.click(fastest);
    const note = within(tools).getByLabelText("旅程備註");
    fireEvent.change(note, { target: { value: "已確認訂位" } });
    fireEvent.click(within(note.closest("section")!).getByRole("button", { name: "儲存" }));
    await waitFor(() => expect(currentTrip.version).toBe(2));
    expect(fastest.getAttribute("aria-pressed")).toBe("true");
    expect(currentTrip.route_preference).toBe("FEWER_TRANSFERS");
    fireEvent.click(within(choices.closest("section")!).getByRole("button", { name: "儲存修改" }));

    await waitFor(() => expect(currentTrip.route_preference).toBe("FASTEST"));
    expect(currentTrip.version).toBe(3);
    expect(currentTrip.notes).toBe("已確認訂位");
    const writes = fetchMock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET");
    expect(writes).toHaveLength(2);
    expect(JSON.parse(String(writes[1][1]?.body))).toMatchObject({ version: 2, route_preference: "FASTEST", items: trip.items });
    expect(fetchMock.mock.calls.some(([url]) => /\/routes\/|\/preview|\/searches/.test(String(url)))).toBe(false);
  });

  it("saves hotel departure time only after explicit confirmation, never on blur", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [{ ...hotelStart, title: "從 已確認飯店 出發", location_name: "正式飯店", latitude: 35.71, longitude: 139.79, location_source: "confirmed", data: { needs_place_confirmation: false } }, { ...trip.items[0], position: 1 }] }),
    ));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    openOptionalStop("從 已確認飯店 出發");
    const departure = await screen.findByLabelText("每天從飯店出發的時間") as HTMLInputElement;
    expect(departure.value).toBe("09:00");
    expect(screen.getByText("儲存後套用到每一天")).toBeTruthy();
    const field = departure.closest(".planner-departure-field")! as HTMLElement;

    fireEvent.change(departure, { target: { value: "08:15" } });
    // Typing alone must not save — half-typed times used to fire real requests.
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
    fireEvent.blur(departure);
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
    fireEvent.keyDown(departure, { key: "Enter" });
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
    fireEvent.click(within(field).getByRole("button", { name: "儲存" }));

    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(true));
    const [, request] = fetchMock.mock.calls.find(([url]) => String(url).includes("/schedule-defaults")) as [string, RequestInit];
    expect(JSON.parse(String(request.body)).day_start_time).toBe("08:15");
  });

  it("refuses a hotel departure time that would land after lunch without calling the API", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [{ ...hotelStart, title: "從 已確認飯店 出發", location_name: "正式飯店", latitude: 35.71, longitude: 139.79, location_source: "confirmed", data: { needs_place_confirmation: false } }, { ...trip.items[0], position: 1 }] }),
    ));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    openOptionalStop("從 已確認飯店 出發");
    const lateDeparture = await screen.findByLabelText("每天從飯店出發的時間");
    fireEvent.change(lateDeparture, { target: { value: "13:00" } });
    fireEvent.blur(lateDeparture);
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
    fireEvent.click(within(lateDeparture.closest(".planner-departure-field")! as HTMLElement).getByRole("button", { name: "儲存" }));

    expect(await screen.findByText("出發時間必須早於午餐時間（12:00）。")).toBeTruthy();
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
  });

  it("retains a failed hotel departure draft and retries only the explicit save", async () => {
    const confirmedHotel = { ...hotelStart, title: "從 已確認飯店 出發", location_name: "正式飯店", latitude: 35.71, longitude: 139.79, location_source: "confirmed", data: { needs_place_confirmation: false } };
    const defaults = { day_start_time: "09:00", lunch_start_time: "12:00", lunch_duration_minutes: 60, dinner_start_time: "18:00", dinner_duration_minutes: 60, default_activity_duration_minutes: 60, transfer_buffer_minutes: 10 };
    const hotelTrip = { ...trip, schedule_defaults: defaults, items: [confirmedHotel, { ...trip.items[0], position: 1 }] };
    let saveCount = 0;
    const fetchMock = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => {
      if (String(url).includes("/schedule-defaults") && init?.method === "PUT") {
        saveCount += 1;
        if (saveCount === 1) return { ok: false, status: 503, json: async () => ({ detail: "暫時無法儲存" }) };
        return response({ ...hotelTrip, version: 2, schedule_defaults: { ...defaults, day_start_time: "08:15" } });
      }
      return response(hotelTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    openOptionalStop("從 已確認飯店 出發");
    const departure = await screen.findByLabelText("每天從飯店出發的時間") as HTMLInputElement;
    const field = departure.closest(".planner-departure-field")! as HTMLElement;
    fireEvent.change(departure, { target: { value: "08:15" } });
    fireEvent.blur(departure);
    expect(saveCount).toBe(0);
    fireEvent.click(within(field).getByRole("button", { name: "儲存" }));

    expect((await within(field).findByRole("alert")).textContent).toBe("儲存失敗，內容已保留，請重試。");
    expect(departure.value).toBe("08:15");
    expect(saveCount).toBe(1);
    fireEvent.blur(departure);
    expect(saveCount).toBe(1);
    fireEvent.click(within(field).getByRole("button", { name: "儲存" }));
    await waitFor(() => expect(within(field).getByRole("status").textContent).toBe("已儲存"));
    const writes = fetchMock.mock.calls.filter(([url, init]) => String(url).includes("/schedule-defaults") && init?.method === "PUT");
    expect(writes).toHaveLength(2);
    expect(writes[1][1]?.body).toBe(writes[0][1]?.body);
    expect(JSON.parse(String(writes[1][1]?.body))).toMatchObject({ version: 1, day_start_time: "08:15" });
    expect(departure.value).toBe("08:15");
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/"))).toBe(false);
  });

  it("restores a skipped confirmed meal from supplemental arrangements without losing its place", async () => {
    const meal = { ...trip.items[0], id: "00000000-0000-4000-8000-000000000030", item_type: "meal", system_role: "lunch", position: 1, title: "鰻魚飯午餐", location_name: "淺草鰻魚老舖", latitude: 35.7119, longitude: 139.7953, location_source: "confirmed", provider_place_id: "verified-merchant-place", fixed_time: true, start_time: "2026-11-11T12:00:00", duration_minutes: 60, is_skipped: false, locked: true, data: { food_id: "food-unagi", merchant_id: "merchant-asakusa", needs_place_confirmation: false } };
    let currentTrip = { ...trip, items: [trip.items[0], meal] as [typeof trip.items[number], typeof meal] };
    const fetchMock = vi.fn(async (url: RequestInfo | URL, init?: RequestInit) => {
      if (String(url).endsWith(`/items/${meal.id}/skip`) && init?.method === "PATCH") {
        const payload = JSON.parse(String(init.body));
        currentTrip = { ...currentTrip, version: currentTrip.version + 1, items: [trip.items[0], { ...meal, is_skipped: payload.skipped }] };
      }
      return response(currentTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    await screen.findByRole("heading", { name: "東京五日" });
    const activeMeal = openOptionalStop(meal.title);
    fireEvent.click(within(activeMeal).getByRole("button", { name: "跳過" }));
    const extrasSummary = await screen.findByText("補充安排", { selector: "summary span" });
    const extras = extrasSummary.closest("details")!;
    fireEvent.click(extras.querySelector("summary")!);
    expect(within(extras).getByRole("button", { name: meal.title })).toBeTruthy();
    fireEvent.click(within(extras).getByRole("button", { name: "恢復用餐" }));

    await waitFor(() => expect(screen.queryByText("補充安排", { selector: "summary span" })).toBeNull());
    const restored = openOptionalStop(meal.title);
    expect(within(restored).getByRole("heading", { name: meal.title })).toBeTruthy();
    expect(within(restored).getByText("淺草鰻魚老舖")).toBeTruthy();
    expect(within(restored).getByRole("button", { name: "跳過" })).toBeTruthy();
    const writes = fetchMock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET");
    expect(writes).toHaveLength(2);
    expect(writes.map(([, init]) => JSON.parse(String(init?.body)))).toEqual([{ version: 1, skipped: true }, { version: 2, skipped: false }]);
    expect(currentTrip.items[1]).toEqual(meal);
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/"))).toBe(false);
  });

  it("blocks a departure time that would land after lunch", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    render(<TripEditor tripId={trip.id} />);

    await openToolsSection("旅程設定");
    fireEvent.change(screen.getByLabelText("每日從飯店出發時間"), { target: { value: "13:00" } });

    expect(screen.getByText("出發時間必須早於午餐時間。")).toBeTruthy();
    expect(screen.getByRole("button", { name: /套用到所有日期/ }).hasAttribute("disabled")).toBe(true);
  });
});

describe("trip editor route requests", () => {
  const stops = ["淺草寺", "晴空塔", "上野公園", "東京車站"].map((title, index) => ({
    ...trip.items[0],
    id: `00000000-0000-4000-8000-00000000002${index}`,
    position: index,
    title,
    location_name: title,
    latitude: 35.7 + index / 100,
    longitude: 139.77 + index / 100,
    duration_minutes: 60,
  }));
  const leg = (from: number, to: number, minutes: number) => ({
    from_item_id: stops[from].id,
    to_item_id: stops[to].id,
    status: "resolved",
    travel_mode: "transit" as const,
    provider: "google_routes",
    attribution: "Google Maps",
    generated_at: "2026-09-01T00:00:00Z",
    schedule_mode: "scheduled" as const,
    preference: "FEWER_TRANSFERS",
    duration_minutes: minutes,
    buffer_minutes: 10,
    departure_time: "2026-11-11T09:00:00+09:00",
    arrival_time: "2026-11-11T09:20:00+09:00",
    ready_time: "2026-11-11T09:30:00+09:00",
    steps: [],
    details_available: [],
    warnings: [],
  });
  const computeCalls = (fetchMock: ReturnType<typeof vi.fn>) =>
    fetchMock.mock.calls.filter(([input]) => String(input).includes("/routes/compute-day"));

  it.each(["provider", "manual"])("keeps the applied %s mode and buffer after daily-entry remount", async (source) => {
    const originalLeg = leg(0, 1, 20);
    const appliedLeg = { ...originalLeg, status: source === "manual" ? "manual" : "resolved", provider: source === "manual" ? "manual" : "google_routes",
      travel_mode: "walk" as const, buffer_minutes: 15, duration_minutes: 12 };
    let current: Trip = { ...trip, items: stops.slice(0, 2), route_segments: [originalLeg] };
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/runtime/public-config")) return Promise.resolve(response({ google_maps_embed_enabled: false }));
      if (url.includes("/routes/preview")) return Promise.resolve(response({
        preview_id: "walk-15", expires_at: "2100-01-01T00:00:00Z", segment: appliedLeg,
        schedule_impact: { affected_items: [], conflicts: [] },
      }));
      if (url.includes("/routes/apply")) {
        expect(JSON.parse(String(init?.body))).toMatchObject(source === "provider"
          ? { version: 1, source, preview_id: "walk-15" }
          : { version: 1, source, travel_mode: "walk", buffer_minutes: 15, duration_minutes: 12 });
        current = { ...current, version: 2, route_segments: [appliedLeg] };
      }
      return Promise.resolve(response(current));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    await screen.findByRole("heading", { name: "晴空塔" });
    fireEvent.click(screen.getByText("當日設定", { selector: "summary" }));
    const settings = screen.getByText("當日設定", { selector: "summary" }).closest("details")!;
    fireEvent.click(within(settings).getByRole("button", { name: "查詢路線" }));
    const panel = await screen.findByRole("dialog", { name: "這段路怎麼走" });
    expect(within(panel).getByRole("tab", { name: "大眾運輸" }).getAttribute("aria-selected")).toBe("true");
    fireEvent.click(within(panel).getByRole("tab", { name: "步行" }));
    fireEvent.click(within(panel).getByText("進階路線設定"));
    fireEvent.change(await within(panel).findByRole("combobox"), { target: { value: "15" } });
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/preview"))).toHaveLength(0);
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/apply"))).toHaveLength(0);
    if (source === "provider") {
      fireEvent.click(within(panel).getByRole("button", { name: "查詢交通方案" }));
      fireEvent.click(await within(panel).findByRole("button", { name: "套用此路線" }));
    } else {
      fireEvent.click(within(panel).getByRole("button", { name: "手動輸入時間" }));
      fireEvent.change(within(panel).getByRole("spinbutton"), { target: { value: "12" } });
      fireEvent.click(within(panel).getByRole("button", { name: "套用手動時間" }));
    }
    await waitFor(() => expect(current.version).toBe(2));
    await waitFor(() => expect(within(panel).getByRole("tab", { name: "步行" }).getAttribute("aria-selected")).toBe("true"));
    expect(within(panel).queryByRole("button", { name: "套用此路線" })).toBeNull();
    fireEvent.click(within(panel).getByText("進階路線設定"));
    expect((await within(panel).findByRole("combobox") as HTMLSelectElement).value).toBe("15");
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/preview"))).toHaveLength(source === "provider" ? 1 : 0);
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/apply"))).toHaveLength(1);
    expect(computeCalls(fetchMock)).toHaveLength(0);
  });

  it("queries route previews only after an explicit request, never on preference changes", async () => {
    const routed = { ...trip, items: stops.slice(0, 2), route_segments: [leg(0, 1, 20)] };
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL) => {
      if (String(input).includes("/routes/preview")) return Promise.resolve(response({
        kind: "external_only", options: [], segment: null, preview_id: null, expires_at: null, schedule_impact: null, warnings: [],
        external_navigation: { provider: "google", url: "https://www.google.com/maps/dir/?api=1", label: "Google Maps" },
      }));
      return Promise.resolve(response(routed));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    await screen.findByRole("heading", { name: "晴空塔" });
    fireEvent.click(screen.getByText("當日設定", { selector: "summary" }));
    const settings = screen.getByText("當日設定", { selector: "summary" }).closest("details")!;
    fireEvent.click(within(settings).getByRole("radio", { name: "步行" }));
    expect(computeCalls(fetchMock)).toHaveLength(0);
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/preview"))).toBe(false);
    fireEvent.click(within(settings).getByRole("button", { name: "查詢路線" }));
    const panel = await screen.findByRole("dialog", { name: "這段路怎麼走" });
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/preview"))).toBe(false);
    fireEvent.click(within(panel).getByRole("button", { name: "查詢交通方案" }));
    await waitFor(() => expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/preview"))).toHaveLength(1));
    const [, request] = fetchMock.mock.calls.find(([url]) => String(url).includes("/routes/preview"))!;
    expect(JSON.parse(String(request.body))).toMatchObject({ travel_mode: "walk", include_alternatives: true, max_options: 3 });
    expect(computeCalls(fetchMock)).toHaveLength(0);
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/routes/apply"))).toBe(false);
  });

  it("keeps the legs a reorder did not touch and counts only the missing ones", async () => {
    const routed = { ...trip, items: stops, route_segments: [leg(0, 1, 20), leg(1, 2, 25), leg(2, 3, 40)] };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(routed))));
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByText("20 分")).toBeTruthy();
    expect(screen.getByText("25 分")).toBeTruthy();
    expect(screen.getByText("40 分")).toBeTruthy();
    expect(screen.queryByText(/段移動尚未查路/)).toBeNull();

    // 東京車站 moves above 上野公園: only the two legs around it lose their routes.
    fireEvent.click(screen.getByRole("button", { name: "排序行程" }));
    fireEvent.click(screen.getByRole("button", { name: "上移 東京車站" }));

    expect(screen.getByText("20 分")).toBeTruthy();
    expect(screen.queryByText("25 分")).toBeNull();
    expect(screen.queryByText("40 分")).toBeNull();
    expect(screen.getAllByText(/^(約 \d+ 分|查看交通)$/)).toHaveLength(2);
    expect(screen.getByText("有 2 段移動尚未查路")).toBeTruthy();
  });
});

describe("trip editor explicit drafts", () => {
  it.each([undefined, "forest", "ocean", "sunset", "lavender"])("uses site palette by default without replacing saved custom palette %s", async (theme) => {
    if (theme) window.localStorage.setItem("travel-planner-theme", theme);
    vi.stubGlobal("fetch", vi.fn(async () => response(trip)));
    const view = render(<TripEditor tripId={trip.id} />);
    await screen.findByRole("heading", { name: trip.name });
    await waitFor(() => expect(view.container.querySelector("main")?.getAttribute("data-planner-theme")).toBe(theme || "site"));
    expect(screen.getByRole("combobox", { name: "語言" })).toBeTruthy();
    expect(window.localStorage.getItem("travel-planner-theme")).toBe(theme || null);
  });

  it("keeps the editor and prevents locale writes when language navigation is cancelled", async () => {
    const fetchMock = vi.fn<(url: string, init?: RequestInit) => Promise<Response>>(async () => response(trip)); vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.change(within(editor).getByLabelText("安排名稱"), { target: { value: "尚未儲存" } });
    // Trigger the same guarded callback used by the visible mobile language control.
    fireEvent.change(screen.getByRole("combobox", { name: "語言", hidden: true }), { target: { value: "en" } });
    const guard = await screen.findByRole("dialog", { name: "保留這次修改嗎？" });
    fireEvent.click(within(guard).getByRole("button", { name: "繼續編輯" }));
    expect((within(editor).getByLabelText("安排名稱") as HTMLInputElement).value).toBe("尚未儲存");
    expect(fetchMock.mock.calls.some(([, init]) => (init as RequestInit | undefined)?.method === "PATCH")).toBe(false);
  });
  const preciseItem = {
    ...trip.items[0], location_source: "hotspot_catalog", provider_place_id: "verified-place-1",
    latitude: 35.7148, longitude: 139.7967, duration_minutes: 90,
    data: { hotspot_id: "catalog-1", catalog_selection: { kind: "hotspot", id: "catalog-1" },
      needs_place_confirmation: false, coordinate_source_type: "wikidata", source_mode: "manual" },
  };
  const fixedItem = { ...preciseItem, id: "fixed-booking", position: 1, title: "保留的預約",
    locked: true, fixed_time: true, start_time: "2026-11-11T15:00:00+09:00" };
  const exactTrip = { ...trip, items: [preciseItem, fixedItem] };
  const writes = (mock: ReturnType<typeof vi.fn>) => mock.mock.calls.filter(([, init]) => init?.method && init.method !== "GET");

  it("keeps typed name, location and coordinates local until save and discards without any write", async () => {
    const fetchMock = vi.fn(async () => response(exactTrip));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.change(within(editor).getByLabelText("安排名稱"), { target: { value: "未儲存的名稱" } });
    fireEvent.change(within(editor).getByLabelText("地點"), { target: { value: "另一個地點" } });
    expect(writes(fetchMock)).toHaveLength(0);
    expect(screen.getByRole("heading", { name: "淺草散步" })).toBeTruthy();
    fireEvent.click(within(editor).getByRole("button", { name: "取消" }));
    const guard = await screen.findByRole("dialog", { name: "保留這次修改嗎？" });
    fireEvent.click(within(guard).getByRole("button", { name: "捨棄修改" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    const reopened = await openStopEditor("淺草散步");
    expect((within(reopened).getByLabelText("安排名稱") as HTMLInputElement).value).toBe("淺草散步");
    expect((within(reopened).getByLabelText("地點") as HTMLInputElement).value).toBe("淺草");
    expect(within(reopened).getByText("地點已確認，可計算路線")).toBeTruthy();
    fireEvent.click(within(reopened).getByRole("button", { name: "儲存修改" }));
    await waitFor(() => expect(writes(fetchMock)).toHaveLength(1));
    const body = JSON.parse(String(writes(fetchMock)[0][1].body));
    expect(body.items[0]).toMatchObject(preciseItem);
    expect(body.items[1]).toMatchObject(fixedItem);
  });

  it("retains a failed save draft and its stable POI identity for an explicit retry", async () => {
    let saves = 0;
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        saves += 1;
        if (saves === 1) return { ok: false, status: 503, json: async () => ({ detail: "temporary offline" }) };
        return response({ ...exactTrip, version: 2, items: JSON.parse(String(init.body)).items });
      }
      return response(exactTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.change(within(editor).getByLabelText("安排名稱"), { target: { value: "我的淺草寺" } });
    fireEvent.change(within(editor).getByLabelText("停留時間"), { target: { value: "120" } });
    fireEvent.click(within(editor).getByRole("button", { name: "儲存修改" }));
    await within(editor).findByRole("alert");
    expect((within(editor).getByLabelText("安排名稱") as HTMLInputElement).value).toBe("我的淺草寺");
    expect(screen.getByRole("heading", { name: "淺草散步" })).toBeTruthy();
    expect(writes(fetchMock)).toHaveLength(1);
    await saveEditor(editor);
    const bodies = writes(fetchMock).map(([, init]) => JSON.parse(String(init.body)));
    expect(bodies).toHaveLength(2);
    expect(bodies[1]).toEqual(bodies[0]);
    expect(bodies[1].items[0]).toMatchObject({ ...preciseItem, title: "我的淺草寺", duration_minutes: 120 });
    expect(bodies[1].items[1]).toMatchObject(fixedItem);
    expect(screen.getByRole("heading", { name: "我的淺草寺" })).toBeTruthy();
  });

  it("supports keep-editing and discard on dirty close without publishing a draft", async () => {
    const fetchMock = vi.fn(async () => response(exactTrip));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    const editor = await openStopEditor("淺草散步");
    fireEvent.change(within(editor).getByLabelText("安排名稱"), { target: { value: "我的草稿" } });
    fireEvent.click(within(editor).getByRole("button", { name: "關閉" }));
    let guard = await screen.findByRole("dialog", { name: "保留這次修改嗎？" });
    fireEvent.click(within(guard).getByRole("button", { name: "繼續編輯" }));
    expect((within(editor).getByLabelText("安排名稱") as HTMLInputElement).value).toBe("我的草稿");
    fireEvent.keyDown(document, { key: "Escape" });
    guard = await screen.findByRole("dialog", { name: "保留這次修改嗎？" });
    fireEvent.click(within(guard).getByRole("button", { name: "捨棄修改" }));
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(writes(fetchMock)).toHaveLength(0);
    expect(screen.getByRole("heading", { name: "淺草散步" })).toBeTruthy();
  });

  it("opens a selected catalog POI as a draft and waits for Add before writing its identity", async () => {
    const selected = { ...preciseItem, title: "東京國立博物館", location_name: "東京國立博物館",
      provider_place_id: "museum-place", latitude: 35.7188, longitude: 139.7765,
      data: { ...preciseItem.data, hotspot_id: "museum", catalog_selection: { kind: "hotspot", id: "museum" } } };
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.includes("/place-options?")) return response({ items: [{ key: "hotspot:museum", id: "museum", kind: "hotspot",
        title: selected.title, subtitle: "東京", distance_km: 1, is_saved: false, item: selected }], next_offset: null, context: "nearby" });
      if (init?.method === "PUT") return response({ ...exactTrip, version: 2, items: JSON.parse(String(init.body)).items });
      return response(exactTrip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    await openAddFromToolbar();
    fireEvent.click(await screen.findByRole("button", { name: "選擇 東京國立博物館" }));
    const editor = await screen.findByRole("dialog", { name: "新增安排" });
    expect((within(editor).getByLabelText("安排名稱") as HTMLInputElement).value).toBe(selected.title);
    expect(writes(fetchMock)).toHaveLength(0);
    expect(screen.queryByRole("heading", { name: selected.title })).toBeNull();
    fireEvent.click(within(editor).getByRole("button", { name: "加入行程" }));
    await screen.findByRole("heading", { name: selected.title });
    expect(writes(fetchMock)).toHaveLength(1);
    const saved = JSON.parse(String(writes(fetchMock)[0][1].body)).items;
    expect(saved.find((row: { title: string }) => row.title === selected.title)).toMatchObject({
      provider_place_id: selected.provider_place_id, latitude: selected.latitude, longitude: selected.longitude,
      data: { hotspot_id: "museum", catalog_selection: { kind: "hotspot", id: "museum" } },
    });
    expect(saved.find((row: { id: string }) => row.id === fixedItem.id)).toMatchObject(fixedItem);
  });
});
