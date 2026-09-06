import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripEditor } from "./trip-editor";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }) }));

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

    fireEvent.click((await screen.findAllByRole("button", { name: "設定主要飯店" }))[0]);
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

  it("shows Ekispert and ODsay as the regional transit providers without exposing keys", async () => {
    const runtime = {
      ekispert_enabled: true,
      odsay_enabled: true,
      navitime_enabled: true,
      naver_directions_enabled: true,
      google_routes_enabled: true,
    };
    const fetchMock = vi.fn().mockImplementation((url: string) => Promise.resolve(response(
      url.includes("/runtime/public-config") ? runtime : { ...trip, destination_country_code: "JP" },
    )));
    vi.stubGlobal("fetch", fetchMock);

    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByText("Ekispert · 日本大眾運輸")).toBeTruthy();
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

    expect(await screen.findByText("已確認")).toBeTruthy();
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
    expect(screen.getByText("尚未設定主要飯店")).toBeTruthy();
    expect(screen.getByText("設定一次後，會建立每天的出發與返回路線")).toBeTruthy();
    expect(screen.queryByText("返回 尚未設定飯店")).toBeNull();
    expect(screen.getByText("午餐尚未安排")).toBeTruthy();
  });

  it("opens mobile trip tools and remembers the selected color theme", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    const { container } = render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findByRole("button", { name: "開啟旅程工具" }));
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
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(twoStopTrip))));
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByRole("heading", { name: "晴空塔" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "在 晴空塔 前插入新安排" }));
    fireEvent.change(screen.getByLabelText("安排名稱"), { target: { value: "雷門" } });
    fireEvent.click(screen.getByRole("button", { name: "加入行程" }));

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

    fireEvent.click(await screen.findByRole("button", { name: "撤銷" }));
    fireEvent.click(await screen.findByRole("button", { name: "撤銷連結" }));

    expect(await screen.findByRole("alert")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "關閉錯誤訊息" }));
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("offers the trip tools from the desktop hero as well", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    render(<TripEditor tripId={trip.id} />);

    await screen.findAllByText("東京五日");
    // One trigger in the mobile app bar, one in the desktop hero row.
    expect(screen.getAllByRole("button", { name: /旅程工具|開啟旅程工具/ }).length).toBeGreaterThanOrEqual(2);
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
    fireEvent.blur(box);

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

    const aiButtons = await screen.findAllByRole("button", { name: /^AI 幫我安排/ });
    fireEvent.click(aiButtons[0]);
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
    expect(screen.getByText("AI 建議")).toBeTruthy();
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

    const aiButtons = await screen.findAllByRole("button", { name: /^AI 幫我安排/ });
    fireEvent.click(aiButtons[0]);
    const fullTrip = screen.getByRole("radio", { name: /\u5168\u884c\u7a0b\u5b89\u6392/ });
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

    fireEvent.click(await screen.findByRole("button", { name: "新增安排" }));
    expect(screen.getByRole("dialog", { name: "新增安排" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "加入行程" }).hasAttribute("disabled")).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "取消" }));
    expect(screen.queryByRole("dialog", { name: "新增安排" })).toBeNull();
    expect(fetchMock.mock.calls.some(([, init]) => init?.method === "PUT")).toBe(false);

    fireEvent.click(screen.getByRole("button", { name: "新增安排" }));
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

    fireEvent.click(await screen.findByRole("button", { name: "新增安排" }));
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
    fireEvent.click(await screen.findByRole("button", { name: "編輯 淺草散步" }));
    const title = screen.getByLabelText("安排名稱");
    fireEvent.change(title, { target: { value: "淺草與晴空塔" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));
    expect(await screen.findByText("行程已儲存")).toBeTruthy();
    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([, init]) => init?.method === "PUT");
      expect(call).toBeTruthy();
      const body = JSON.parse(String(call?.[1]?.body));
      expect(body.version).toBe(1);
      expect(body.items[0].title).toBe("淺草與晴空塔");
    });
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

    fireEvent.click(await screen.findByRole("button", { name: "編輯 淺草散步" }));
    expect(screen.getByRole("radio", { name: "接續前站" }).getAttribute("aria-checked")).toBe("true");
    fireEvent.click(screen.getByRole("radio", { name: "固定時間" }));
    fireEvent.change(screen.getByLabelText("固定開始時間"), { target: { value: "15:20" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));

    await waitFor(() => expect(savedBody).toBeTruthy());
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
        return response({
          module: "hotel",
          disclosure: "本站可能因此獲得分潤。",
          options: [{ partner: "travelpayouts", display_name: "Travelpayouts", module: "hotel", cta: "查看住宿", clickout_url: "/api/travel/affiliates/click" }],
        });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findAllByRole("button", { name: /旅程工具/ }).then((buttons) => buttons[0]));

    const print = await screen.findByRole("link", { name: "開啟列印版" });
    expect(print.getAttribute("href")).toBe(`/trips/${trip.id}/print`);
    await waitFor(() => expect(screen.getAllByRole("button", { name: /查看住宿/ }).length).toBeGreaterThan(0));
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes(`trip_id=${trip.id}`))).toBe(true);
  });

  it("flushes the newest revision before requesting an optimization", async () => {
    let resolveFirstSave: ((value: ReturnType<typeof response>) => void) | undefined;
    const firstSave = new Promise<ReturnType<typeof response>>((resolve) => {
      resolveFirstSave = resolve;
    });
    const putBodies: Array<{ version: number; items: typeof trip.items }> = [];
    const preview = {
      preview_id: "00000000-0000-4000-8000-000000000098",
      expires_at: "2026-11-01T10:10:00Z",
      base_version: 3,
      route_preference: "FEWER_TRANSFERS",
      changed: false,
      warnings: [],
      segments: [],
      total_duration_before_minutes: 0,
      total_duration_after_minutes: 0,
      charge_on_apply: 1,
      days: [],
    };
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body));
        putBodies.push(body);
        if (putBodies.length === 1) return firstSave;
        return response({ ...trip, version: 3, items: body.items });
      }
      if (url.includes("/optimize/preview")) return response(preview);
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);
    fireEvent.click(await screen.findByRole("button", { name: "編輯 淺草散步" }));
    const title = screen.getByLabelText("安排名稱");
    fireEvent.change(title, { target: { value: "第一次修改" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存變更" }));
    await waitFor(() => expect(putBodies).toHaveLength(1));

    fireEvent.change(title, { target: { value: "最後一次修改" } });
    fireEvent.click(screen.getByRole("button", { name: /^最佳化動線/ }));
    resolveFirstSave?.(response({ ...trip, version: 2, items: putBodies[0].items }));

    await waitFor(() => expect(putBodies).toHaveLength(2));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/optimize/preview"))).toBe(true));
    expect(putBodies[1].version).toBe(2);
    expect(putBodies[1].items[0].title).toBe("最後一次修改");
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

    fireEvent.click(await screen.findByRole("button", { name: /^最佳化動線/ }));

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
    const aiButtons = await screen.findAllByRole("button", { name: /^AI 幫我安排/ });
    fireEvent.click(aiButtons[0]);
    fireEvent.click(screen.getByRole("button", { name: /只調整現有動線/ }));
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
    fireEvent.click(await screen.findByRole("button", { name: "編輯 淺草散步" }));
    fireEvent.click(screen.getByRole("button", { name: "刪除這個安排" }));
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

  it("opens the mobile route sheet on demand, expands it, and closes it on back", async () => {
    const destination = {
      ...trip.items[0],
      id: "00000000-0000-4000-8000-000000000003",
      position: 1,
      title: "晴空塔",
      location_name: "押上",
    };
    const routedTrip = {
      ...trip,
      items: [trip.items[0], destination],
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
      { name: "查看前往 晴空塔 的路線" },
      { timeout: 5_000 },
    );
    fireEvent.click(routeButton);
    expect(await screen.findByRole("dialog", { name: "這段路怎麼走" })).toBeTruthy();
    const collapse = screen.getByRole("button", { name: "縮小路線面板" });
    expect(collapse.getAttribute("aria-pressed")).toBe("true");
    fireEvent.click(collapse);
    const expand = screen.getByRole("button", { name: "全螢幕顯示路線面板" });
    expect(expand.getAttribute("aria-pressed")).toBe("false");
    fireEvent.click(expand);
    expect(screen.getByRole("button", { name: "縮小路線面板" }).getAttribute("aria-pressed")).toBe("true");
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

    expect(await screen.findByText(/預定 .*／預計 .*，可能遲到 18 分鐘/)).toBeTruthy();
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

  it("still offers the leg out of the hotel when the lodging has no confirmed place yet", async () => {
    const stop = { ...trip.items[0], position: 1, duration_minutes: 60 };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, stop] }),
    )));
    render(<TripEditor tripId={trip.id} />);

    expect(await screen.findByText("先設定飯店地點")).toBeTruthy();
    expect(screen.getByText("設定後才能算出前往 淺草散步 的移動時間")).toBeTruthy();
  });

  it("shows a running estimate for chained stops before any route has been computed", async () => {
    const stop = { ...trip.items[0], position: 1, duration_minutes: 60 };
    const later = { ...trip.items[0], id: "00000000-0000-4000-8000-000000000011", position: 2, title: "晴空塔", duration_minutes: 60 };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, stop, later] }),
    )));
    render(<TripEditor tripId={trip.id} />);

    // 飯店 09:00 出發，預設緩衝 10 分：第一站約 09:10，停留 60 分後第二站約 10:20。
    expect(await screen.findByText("接續前站 · 約 09:10")).toBeTruthy();
    expect(screen.getByText("接續前站 · 約 10:20")).toBeTruthy();
  });

  it("saves a new daily departure time from the trip tools panel", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, { ...trip.items[0], position: 1 }] }),
    ));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findByRole("button", { name: "開啟旅程工具" }));
    const departure = screen.getByLabelText("每日從飯店出發時間") as HTMLInputElement;
    expect(departure.value).toBe("09:00");

    fireEvent.change(departure, { target: { value: "08:15" } });
    fireEvent.click(screen.getByRole("button", { name: /套用到所有日期/ }));

    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(true));
    const [, request] = fetchMock.mock.calls.find(([url]) => String(url).includes("/schedule-defaults")) as [string, RequestInit];
    expect(JSON.parse(String(request.body)).day_start_time).toBe("08:15");
  });

  it("changes the daily departure time straight from the hotel card", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, { ...trip.items[0], position: 1 }] }),
    ));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    const departure = await screen.findByLabelText("每天從飯店出發的時間") as HTMLInputElement;
    expect(departure.value).toBe("09:00");
    expect(screen.getByText("套用到每一天")).toBeTruthy();

    fireEvent.change(departure, { target: { value: "08:15" } });
    // Typing alone must not save — half-typed times used to fire real requests.
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
    fireEvent.blur(departure);

    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(true));
    const [, request] = fetchMock.mock.calls.find(([url]) => String(url).includes("/schedule-defaults")) as [string, RequestInit];
    expect(JSON.parse(String(request.body)).day_start_time).toBe("08:15");
  });

  it("refuses a hotel departure time that would land after lunch without calling the API", async () => {
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(
      response({ ...trip, items: [hotelStart, { ...trip.items[0], position: 1 }] }),
    ));
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    const lateDeparture = await screen.findByLabelText("每天從飯店出發的時間");
    fireEvent.change(lateDeparture, { target: { value: "13:00" } });
    fireEvent.blur(lateDeparture);

    expect(await screen.findByText("出發時間必須早於午餐時間（12:00）。")).toBeTruthy();
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/schedule-defaults"))).toBe(false);
  });

  it("blocks a departure time that would land after lunch", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findByRole("button", { name: "開啟旅程工具" }));
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

  it("asks for routes without forcing a refresh from the day header and the mode picker", async () => {
    const routed = { ...trip, items: stops.slice(0, 2), route_segments: [leg(0, 1, 20)] };
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL) => {
      if (String(input).includes("/routes/compute-day")) {
        return Promise.resolve(response({ version: 2, status: "complete", total: 1, completed: 1 }));
      }
      return Promise.resolve(response(routed));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findByRole("button", { name: "計算當日路線" }));
    await waitFor(() => expect(computeCalls(fetchMock)).toHaveLength(1));
    fireEvent.click(screen.getByRole("radio", { name: "步行" }));
    await waitFor(() => expect(computeCalls(fetchMock)).toHaveLength(2));

    // Neither button bypasses the caches: the backend reuses saved legs and only
    // asks providers for the pairs that are missing.
    const bodies = computeCalls(fetchMock).map(([, init]) => JSON.parse(String((init as RequestInit).body)));
    expect(bodies.map((body) => body.refresh)).toEqual([false, false]);
    expect(bodies[1].default_travel_mode).toBe("walk");
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
    fireEvent.click(screen.getByRole("button", { name: "上移 東京車站" }));

    expect(screen.getByText("20 分")).toBeTruthy();
    expect(screen.queryByText("25 分")).toBeNull();
    expect(screen.queryByText("40 分")).toBeNull();
    expect(screen.getAllByText("選擇這段交通方式")).toHaveLength(2);
    expect(screen.getByText("有 2 段移動尚未查路")).toBeTruthy();
  });
});
