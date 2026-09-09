import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { RouteModePanel } from "./route-mode-panel";

const items = [
  { id: "from", item_type: "suggestion", day_date: "2026-11-10", position: 0, title: "上野", latitude: 35.7, longitude: 139.7, locked: false, is_estimated: false, data: {} },
  { id: "to", item_type: "suggestion", day_date: "2026-11-10", position: 1, title: "淺草", latitude: 35.71, longitude: 139.8, locked: false, is_estimated: false, data: {} },
];

const initialSegment = {
  from_item_id: "from",
  to_item_id: "to",
  status: "resolved",
  travel_mode: "transit" as const,
  is_override: false,
  provider: "google_routes",
  attribution: "Google Maps",
  generated_at: "2026-09-01T00:00:00Z",
  schedule_mode: "scheduled" as const,
  preference: "FEWER_TRANSFERS",
  duration_minutes: 24,
  buffer_minutes: 10,
  steps: [],
  details_available: [],
  warnings: [],
};

const trip = {
  id: "trip",
  name: "東京",
  mode: "manual",
  total_price: 0,
  currency: "TWD",
  data: {},
  version: 3,
  items,
  route_segments: [initialSegment],
  routing: {
    status: "complete" as const,
    total: 1,
    completed: 1,
    day_settings: [{ day_date: "2026-11-10", default_travel_mode: "transit" as const, default_buffer_minutes: 10, route_preference: "FEWER_TRANSFERS" as const, auto_compute: true }],
  },
};

function ok(payload: unknown) {
  return new Response(JSON.stringify(payload), { status: 200, headers: { "Content-Type": "application/json" } });
}

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers(); });

describe("route mode panel", () => {
  it("uses one neutral idle instruction and a single query action without a repeated empty card", () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false })));
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    expect(container.querySelector("[data-route-state='idle']")).toBeTruthy();
    expect(screen.getAllByText("選好交通方式後，按「查詢交通方案」比較路線；確認套用前不會修改行程。")).toHaveLength(1);
    expect(screen.getAllByRole("button", { name: "查詢交通方案" })).toHaveLength(1);
    expect(screen.queryByText("尚未取得路線")).toBeNull();
    expect(screen.queryByText(/Provider/)).toBeNull();
    expect(container.querySelector(".route-empty-state")).toBeNull();
    expect(container.querySelector(".route-panel-detail")).toBeNull();
  });

  it.each(["failed", "unavailable", "pending"])("does not label a %s saved route as applied or display its placeholder zero minutes", (status) => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false })));
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={{ ...initialSegment, status, duration_minutes: 0 }} onApplied={vi.fn()} onError={vi.fn()} />);
    expect(container.querySelector("[data-route-state='unavailable']")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "目前已套用" })).toBeNull();
    expect(screen.queryByText("0 分鐘")).toBeNull();
    expect((screen.getByRole("button", { name: "查詢交通方案" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it.each([
    { status: "stale", state: "stale", label: "已存路線需重新查詢" },
    { status: "estimated", state: "estimated", label: "估算移動時間" },
    { status: "manual", state: "manual", label: "已套用手動時間，未經地圖服務確認" },
  ])("labels $status timing truthfully", ({ status, state, label }) => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false })));
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={{ ...initialSegment, status, provider: status === "manual" ? "manual" : initialSegment.provider }} onApplied={vi.fn()} onError={vi.fn()} />);
    expect(container.querySelector(`[data-route-state='${state}']`)).toBeTruthy();
    expect(screen.getByRole("status").textContent).toContain(label);
    if (status !== "manual") expect(screen.queryByRole("button", { name: "目前已套用" })).toBeNull();
  });

  it("preserves the saved route while a failed refresh offers a working retry", async () => {
    vi.stubGlobal("fetch", vi.fn(async (url: string) => url.endsWith("/runtime/public-config")
      ? ok({ google_maps_javascript_enabled: false })
      : new Response(JSON.stringify({ detail: "Unable to refresh" }), { status: 503 })));
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={vi.fn()} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "重新查詢" }));
    await screen.findByRole("alert");
    expect(container.querySelector("[data-route-state='error']")).toBeTruthy();
    expect(screen.getByRole("button", { name: /大眾運輸 · 24 分鐘/ })).toBeTruthy();
    expect((screen.getByRole("button", { name: "重試" }) as HTMLButtonElement).disabled).toBe(false);
    expect(screen.queryByRole("button", { name: "目前已套用" })).toBeNull();
  });
  it("keeps initial mode, tab and buffer choices local until an explicit query", async () => {
    const requests: Array<Record<string, unknown>> = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_embed_enabled: false });
      requests.push(JSON.parse(String(init?.body)));
      return ok({ preview_id: "explicit", expires_at: "2100-01-01T00:00:00Z", segment: { ...initialSegment, travel_mode: "walk", buffer_minutes: 15 }, schedule_impact: { affected_items: [], conflicts: [] } });
    }));
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialTravelMode="drive" initialBufferMinutes={30} onApplied={() => undefined} onError={() => undefined} />);
    expect(screen.getByRole("tab", { name: "汽車" }).getAttribute("aria-selected")).toBe("true");
    fireEvent.click(screen.getByRole("tab", { name: "步行" }));
    fireEvent.click(screen.getByText("進階路線設定"));
    const buffer = await screen.findByRole("combobox");
    expect((buffer as HTMLSelectElement).value).toBe("30");
    fireEvent.change(buffer, { target: { value: "15" } });
    expect(requests).toHaveLength(0);
    const queryButton = screen.getByRole("button", { name: "查詢交通方案" });
    fireEvent.click(queryButton);
    fireEvent.click(queryButton);
    await screen.findByRole("button", { name: "套用此路線" });
    expect(requests).toHaveLength(1);
    expect(requests[0]).toMatchObject({ version: 3, travel_mode: "walk", buffer_minutes: 15 });
  });

  it("never applies a preview from a different buffer or trip version", async () => {
    let queries = 0;
    const applyBodies: Array<Record<string, unknown>> = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_embed_enabled: false });
      const body = JSON.parse(String(init?.body));
      if (url.endsWith("/routes/preview")) {
        queries += 1;
        return ok({ preview_id: `preview-${queries}`, expires_at: "2100-01-01T00:00:00Z", segment: { ...initialSegment, buffer_minutes: body.buffer_minutes }, schedule_impact: { affected_items: [], conflicts: [] } });
      }
      applyBodies.push(body);
      return ok({ ...trip, version: 4 });
    }));
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    await screen.findByRole("button", { name: "套用此路線" });
    fireEvent.click(screen.getByText("進階路線設定"));
    fireEvent.change(await screen.findByRole("combobox"), { target: { value: "15" } });
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    expect(screen.getByRole("status").textContent).toContain("設定已變更");
    expect(queries).toBe(1);
    expect(applyBodies).toHaveLength(0);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    fireEvent.click(await screen.findByRole("button", { name: "套用此路線" }));
    await waitFor(() => expect(applyBodies).toHaveLength(1));
    expect(applyBodies[0]).toMatchObject({ source: "provider", preview_id: "preview-2" });
  });

  it("discards an old in-flight preview after the trip version changes", async () => {
    let finish!: (response: Response) => void;
    const onBusy = vi.fn();
    const fetchMock = vi.fn((url: string) => url.endsWith("/runtime/public-config")
      ? Promise.resolve(ok({ google_maps_embed_enabled: false }))
      : new Promise<Response>((resolve) => { finish = resolve; }));
    vi.stubGlobal("fetch", fetchMock);
    const props = { trip, items, fromItemId: "from", toItemId: "to", onApplied: vi.fn(), onError: vi.fn(), onBusy };
    const view = render(<RouteModePanel {...props} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    view.rerender(<RouteModePanel {...props} trip={{ ...trip, version: 4 }} />);
    finish(ok({ preview_id: "old", expires_at: "2100-01-01T00:00:00Z", segment: initialSegment, schedule_impact: { affected_items: [], conflicts: [] } }));
    await waitFor(() => expect(onBusy).toHaveBeenLastCalledWith(false));
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    expect(props.onApplied).not.toHaveBeenCalled();
  });

  it("does not replace newer parent state with an old apply response", async () => {
    let finish!: (response: Response) => void;
    const applied = vi.fn();
    const onBusy = vi.fn();
    vi.stubGlobal("fetch", vi.fn((url: string) => {
      if (url.endsWith("/runtime/public-config")) return Promise.resolve(ok({ google_maps_embed_enabled: false }));
      if (url.endsWith("/routes/preview")) return Promise.resolve(ok({ preview_id: "one", expires_at: "2100-01-01T00:00:00Z", segment: initialSegment, schedule_impact: { affected_items: [], conflicts: [] } }));
      return new Promise<Response>((resolve) => { finish = resolve; });
    }));
    const props = { trip, items, fromItemId: "from", toItemId: "to", onApplied: applied, onError: vi.fn(), onBusy };
    const view = render(<RouteModePanel {...props} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    fireEvent.click(await screen.findByRole("button", { name: "套用此路線" }));
    view.rerender(<RouteModePanel {...props} trip={{ ...trip, version: 5 }} />);
    finish(ok({ ...trip, version: 4 }));
    await waitFor(() => expect(onBusy).toHaveBeenLastCalledWith(false));
    expect(applied).not.toHaveBeenCalled();
  });

  it("requires another explicit query after a preview expires", async () => {
    const applyCalls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_embed_enabled: false });
      if (url.endsWith("/routes/apply")) applyCalls.push(url);
      return ok({ preview_id: "expired", expires_at: "2000-01-01T00:00:00Z", segment: initialSegment, schedule_impact: { affected_items: [], conflicts: [] } });
    }));
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    expect(await screen.findByRole("button", { name: "重新查詢" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    expect(screen.getByRole("status").textContent).toContain("預覽已過期");
    expect(applyCalls).toHaveLength(0);
  });

  it("replaces apply with requery when the selected preview expires while the drawer stays open", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2030-01-01T00:00:00Z"));
    const applyCalls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_javascript_enabled: false });
      if (url.endsWith("/routes/apply")) applyCalls.push(url);
      return ok({ preview_id: "soon-expired", expires_at: "2030-01-01T00:00:01Z", segment: initialSegment, schedule_impact: { affected_items: [], conflicts: [] } });
    }));
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    await act(async () => { fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" })); });
    expect(screen.getByRole("button", { name: "套用此路線" })).toBeTruthy();
    act(() => { vi.advanceTimersByTime(1001); });
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    expect(screen.getByRole("button", { name: "重新查詢" })).toBeTruthy();
    expect(applyCalls).toHaveLength(0);
  });

  it("keeps a valid timing-only preview applicable without inventing a map path", async () => {
    vi.stubGlobal("fetch", vi.fn(async (url: string) => url.endsWith("/runtime/public-config")
      ? ok({ google_maps_javascript_enabled: false })
      : ok({ preview_id: "timing-only", expires_at: "2100-01-01T00:00:00Z", segment: { ...initialSegment, encoded_polyline: null }, schedule_impact: { affected_items: [], conflicts: [] } })));
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    expect((await screen.findByRole("button", { name: "套用此路線" }) as HTMLButtonElement).disabled).toBe(false);
  });
  it("shows an app-style map, named endpoints and verified transit steps", async () => {
    const detailedSegment = {
      ...initialSegment,
      maps_url: "https://www.google.com/maps/dir/?api=1&origin_place_id=from&destination_place_id=to",
      departure_time: "2026-11-10T17:54:00+09:00",
      arrival_time: "2026-11-10T18:06:00+09:00",
      distance_meters: 850,
      details_available: ["steps", "stops", "headsign", "platform"],
      steps: [
        { travel_mode: "WALK", instruction: "步行至東京晴空塔站", duration_minutes: 8, distance_meters: 550 },
        { travel_mode: "TRANSIT", instruction: "搭乘都營淺草線", duration_minutes: 1, departure_stop: "TOKYO SKYTREE Sta.", arrival_stop: "言問橋", line_name: "都營淺草線", line_short_name: "A", platform: "1", stop_count: 1 },
        { travel_mode: "WALK", instruction: "步行至牛嶋神社", duration_minutes: 4, distance_meters: 300 },
      ],
    };
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_browser_key: null, google_maps_embed_enabled: false })));

    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={detailedSegment} onApplied={() => undefined} onError={() => undefined} />);

    expect(screen.getByRole("region", { name: "路線起訖與交通方式" }).textContent).toContain("上野");
    expect(screen.getByRole("region", { name: "路線起訖與交通方式" }).textContent).toContain("淺草");
    expect(screen.getByRole("link", { name: "導航：上野到淺草" }).getAttribute("href")).toContain("origin_place_id=from");
    expect(screen.queryByText("步行至東京晴空塔站")).toBeNull();
    const expandDetails = screen.getByRole("button", { name: /大眾運輸 · 24 分鐘/ });
    expect(expandDetails.getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(expandDetails);
    expect(screen.getByText("步行至東京晴空塔站")).toBeTruthy();
    expect(screen.getByText(/TOKYO SKYTREE Sta\. → 言問橋/)).toBeTruthy();
    expect(screen.getByText("月台 1")).toBeTruthy();
    const map = container.querySelector(".route-panel-map");
    const details = container.querySelector(".route-panel-detail");
    expect(map && details && Boolean(map.compareDocumentPosition(details) & Node.DOCUMENT_POSITION_FOLLOWING)).toBe(true);
  });

  it("labels provider-backed fallback schedules as near-term reference transit", () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_browser_key: null, google_maps_embed_enabled: false })));

    render(<RouteModePanel
      trip={trip}
      items={items}
      fromItemId="from"
      toItemId="to"
      initialSegment={{
        ...initialSegment,
        schedule_mode: "preview",
        warnings: ["指定日期的班次尚未開放，已改用近期相同星期與時段的參考路線。"],
      }}
      onApplied={() => undefined}
      onError={() => undefined}
    />);

    expect(screen.getByText("近期參考班次")).toBeTruthy();
    expect(screen.getByText(/指定日期的班次尚未開放/)).toBeTruthy();
  });

  it("uses POI titles in the drawer and confirmed coordinates in its fallback navigation", () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_browser_key: null, google_maps_embed_enabled: false })));
    const addressItems = [
      { ...items[0], location_name: "日本東京都台東區上野公園完整地址" },
      { ...items[1], location_name: "日本東京都台東區淺草完整地址" },
    ];

    render(<RouteModePanel trip={trip} items={addressItems} fromItemId="from" toItemId="to" initialSegment={{ ...initialSegment, maps_url: undefined }} onApplied={() => undefined} onError={() => undefined} />);

    const endpoints = screen.getByRole("region", { name: "路線起訖與交通方式" });
    expect(endpoints.textContent).toContain("上野");
    expect(endpoints.textContent).toContain("淺草");
    expect(endpoints.textContent).not.toContain("完整地址");
    const navigation = screen.getByRole("link", { name: "導航：上野到淺草" });
    expect(navigation.getAttribute("href")).toContain("origin=35.7000000%2C139.7000000");
    expect(navigation.getAttribute("href")).toContain("destination=35.7100000%2C139.8000000");
    expect(navigation.getAttribute("href")).toContain("travelmode=transit");
  });

  it("waits for explicit confirmation before previewing an unapplied route", async () => {
    const noRouteTrip = {
      ...trip,
      route_segments: [],
      routing: { ...trip.routing, status: "idle" as const, completed: 0 },
    };
    const fetchMock = vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) {
        return ok({ google_maps_browser_key: null, google_maps_embed_enabled: false });
      }
      return ok({
        preview_id: "preview-default",
        expires_at: "2100-09-01T00:15:00Z",
        segment: initialSegment,
        schedule_impact: { affected_items: [], conflicts: [] },
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<RouteModePanel trip={noRouteTrip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));

    expect((await screen.findByRole("button", { name: "套用此路線" }) as HTMLButtonElement).disabled).toBe(false);
    expect(screen.queryByText("目前已套用")).toBeNull();
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("/routes/preview"))).toBe(true);
  });

  it("stops showing a loading summary after the route provider fails", async () => {
    const noRouteTrip = {
      ...trip,
      route_segments: [],
      routing: { ...trip.routing, status: "idle" as const, completed: 0 },
    };
    vi.stubGlobal("fetch", vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) {
        return ok({ google_maps_browser_key: null, google_maps_embed_enabled: false });
      }
      return new Response(JSON.stringify({ detail: "目前找不到這個交通方式的可用路線" }), {
        status: 503,
        headers: { "Content-Type": "application/json" },
      });
    }));

    render(<RouteModePanel trip={noRouteTrip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));

    expect(await screen.findByText("路線暫時無法取得")).toBeTruthy();
    expect(screen.queryByText("正在取得路線")).toBeNull();
    expect(screen.getByRole("button", { name: "重試" })).toBeTruthy();
  });

  it("offers NAVER external navigation without enabling apply when Korean transit has no internal route", async () => {
    const koreanTrip = {
      ...trip,
      destination_country_code: "KR",
      route_segments: [],
      routing: { ...trip.routing, status: "idle" as const, completed: 0 },
    };
    const fetchMock = vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) {
        return ok({ google_maps_embed_enabled: false, naver_dynamic_map_enabled: false });
      }
      return ok({
        kind: "external_only",
        preview_id: null,
        expires_at: null,
        segment: null,
        schedule_impact: null,
        external_navigation: {
          provider: "naver_maps",
          label: "NAVER Maps",
          travel_mode: "transit",
          app_url: "nmap://route/public?slat=35.7&slng=139.7&dlat=35.71&dlng=139.8",
          web_url: "https://map.naver.com/p/directions/35.7,139.7,上野/35.71,139.8,淺草/-/transit",
          reason: "NAVER 官方 Directions API 不提供可保存的大眾運輸班次；請到 NAVER Maps 查看。",
        },
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<RouteModePanel trip={koreanTrip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));

    const externalLink = await screen.findByRole("link", { name: /用 NAVER Maps 規劃/ });
    expect(externalLink.getAttribute("href")).toContain("https://map.naver.com/");
    expect((screen.getByRole("button", { name: "外部導航，無法套用" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    expect(screen.getByText(/外部結果不會自動套用/)).toBeTruthy();
  });

  it("offers exact Google navigation when an internal route is unavailable", async () => {
    const noRouteTrip = {
      ...trip,
      destination_country_code: "JP",
      route_segments: [],
      routing: { ...trip.routing, status: "idle" as const, completed: 0 },
    };
    const fetchMock = vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) {
        return ok({ google_maps_embed_enabled: false });
      }
      return ok({
        kind: "external_only",
        preview_id: null,
        expires_at: null,
        segment: null,
        schedule_impact: null,
        external_navigation: {
          provider: "google_maps",
          label: "Google Maps",
          travel_mode: "transit",
          app_url: "https://www.google.com/maps/dir/?api=1&origin_place_id=from&destination_place_id=to",
          web_url: "https://www.google.com/maps/dir/?api=1&origin_place_id=from&destination_place_id=to",
          reason: "目前無法取得可套用的站內大眾運輸班次。",
        },
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<RouteModePanel trip={noRouteTrip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));

    const externalLink = await screen.findByRole("link", { name: /用 Google Maps 規劃/ });
    expect(externalLink.getAttribute("href")).toContain("origin_place_id=from");
    expect(screen.getByRole("region", { name: "Google Maps 外部導航" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "開啟 NAVER App" })).toBeNull();
    expect((screen.getByRole("button", { name: "外部導航，無法套用" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("opens the missing endpoint editor without automatic location matching or route queries", async () => {
    const missingItems = items.map((item) => ({
      ...item,
      latitude: undefined,
      longitude: undefined,
      location_name: item.id === "from" ? "" : item.title,
    }));
    const noRouteTrip = {
      ...trip,
      items: missingItems,
      route_segments: [],
      routing: { ...trip.routing, status: "needs_locations" as const, completed: 0 },
    };
    const onEditItem = vi.fn();
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      trip: noRouteTrip,
      matched_items: [],
      unresolved_items: [{ item_id: "from", title: "上野", reason: "尚未輸入可辨識的地點名稱" }],
    })));

    render(<RouteModePanel trip={noRouteTrip} items={missingItems} fromItemId="from" toItemId="to" onApplied={() => undefined} onEditItem={onEditItem} onError={() => undefined} />);

    fireEvent.click(screen.getAllByRole("button", { name: "補上地點" })[0]);
    expect(onEditItem).toHaveBeenCalledWith("from");
    expect(screen.queryByText("目前已套用")).toBeNull();
  });

  it("previews a selected mode before applying it", async () => {
    let previewBody: Record<string, unknown> | undefined;
    let applyBody: Record<string, unknown> | undefined;
    const walking = { ...initialSegment, travel_mode: "walk" as const, duration_minutes: 31 };
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/routes/preview")) {
        previewBody = JSON.parse(String(init?.body));
        return ok({ preview_id: "preview-1", expires_at: "2100-09-01T00:15:00Z", segment: walking, schedule_impact: { affected_items: [], conflicts: [] } });
      }
      applyBody = JSON.parse(String(init?.body));
      return ok({ ...trip, version: 4, route_segments: [walking] });
    });
    vi.stubGlobal("fetch", fetchMock);
    const applied = vi.fn();
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={applied} onError={() => undefined} />);

    fireEvent.click(screen.getByRole("tab", { name: "步行" }));
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    expect(await screen.findAllByText("步行 · 31 分鐘")).not.toHaveLength(0);
    expect(previewBody).toMatchObject({ version: 3, travel_mode: "walk", buffer_minutes: 10, include_alternatives: true, max_options: 3 });
    fireEvent.click(screen.getByRole("button", { name: "套用此路線" }));
    await waitFor(() => expect(applied).toHaveBeenCalledOnce());
    expect(applyBody).toMatchObject({ version: 3, source: "provider", preview_id: "preview-1" });
  });

  it("switches among cached route options and applies only the selected preview", async () => {
    let previewCalls = 0;
    let applyBody: Record<string, unknown> | undefined;
    const routeOptions = [18, 21, 25].map((duration, index) => ({
      preview_id: `preview-${index + 1}`,
      rank: index + 1,
      provider_route_key: `route-${index + 1}`,
      expires_at: "2100-09-01T00:15:00Z",
      segment: {
        ...initialSegment,
        travel_mode: "walk" as const,
        duration_minutes: duration,
        distance_meters: 1200 + index * 100,
        route_option_rank: index + 1,
        encoded_polyline: `_p~iF~ps|U_ulLnnqC_mqNvxq\`${index}`,
      },
      schedule_impact: {
        affected_items: index === 1
          ? [{ item_id: "to", title: "淺草", delta_minutes: -65, fixed_time: false }]
          : [],
        conflicts: [],
      },
    }));
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/runtime/public-config")) {
        return ok({ google_maps_browser_key: null, google_maps_javascript_enabled: false });
      }
      if (url.endsWith("/routes/preview")) {
        previewCalls += 1;
        return ok({
          kind: "provider",
          ...routeOptions[0],
          options: routeOptions,
        });
      }
      applyBody = JSON.parse(String(init?.body));
      return ok({ ...trip, version: 4, route_segments: [routeOptions[1].segment] });
    }));

    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={() => undefined} onError={() => undefined} />);
    fireEvent.click(screen.getByRole("tab", { name: "步行" }));
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    const secondOption = await screen.findByRole("option", { name: /方案 2/ });
    const firstOption = screen.getByRole("option", { name: /方案 1/ });
    firstOption.focus();
    fireEvent.keyDown(firstOption, { key: "ArrowRight" });
    expect(document.activeElement).toBe(secondOption);
    expect(secondOption.getAttribute("aria-selected")).toBe("true");
    expect(screen.getByText(/步行 · 方案 2 · 21 分鐘/)).toBeTruthy();
    expect(screen.getAllByText("1.3 公里").length).toBeGreaterThan(0);
    expect(screen.queryByText("步行 0 分")).toBeNull();
    expect(screen.getByText("可提前 65 分鐘")).toBeTruthy();
    expect(previewCalls).toBe(1);
    expect(applyBody).toBeUndefined();

    fireEvent.click(screen.getByRole("button", { name: "套用此路線" }));
    await waitFor(() => expect(applyBody).toMatchObject({ preview_id: "preview-2" }));
    expect(previewCalls).toBe(1);
  });

  it("keeps buffer and manual editing in advanced settings without fetching on disclosure", async () => {
    const fetchMock = vi.fn(async (url: string) => url.endsWith("/runtime/public-config")
      ? ok({ google_maps_browser_key: null, google_maps_javascript_enabled: false })
      : ok({ ...trip, version: 4 }));
    vi.stubGlobal("fetch", fetchMock);
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={() => undefined} onError={() => undefined} />);
    const settings = container.querySelector(".route-advanced-settings") as HTMLDetailsElement;
    expect(settings.open).toBe(false);
    expect(screen.queryByRole("combobox")).toBeNull();
    fireEvent.click(screen.getByText("進階路線設定"));
    await waitFor(() => expect(settings.open).toBe(true));
    expect(screen.getByRole("combobox")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "手動輸入時間" }));
    const input = screen.getByRole("spinbutton");
    expect(document.activeElement).toBe(input);
    fireEvent.change(input, { target: { value: "35" } });
    fireEvent.click(screen.getByRole("button", { name: "取消自訂時間" }));
    expect(screen.queryByRole("spinbutton")).toBeNull();
    expect(document.activeElement).toBe(settings.querySelector("summary"));
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/"))).toHaveLength(0);
  });

  it("uses manual-activation keyboard tabs without querying while moving focus", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      expect(url).toContain("/runtime/public-config");
      return ok({ google_maps_browser_key: null, google_maps_javascript_enabled: false });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={() => undefined} onError={() => undefined} />);
    const transit = screen.getByRole("tab", { name: "大眾運輸" });
    const walking = screen.getByRole("tab", { name: "步行" });
    transit.focus();
    fireEvent.keyDown(transit, { key: "ArrowRight" });
    expect(document.activeElement).toBe(walking);
    expect(transit.getAttribute("aria-selected")).toBe("true");
    const panel = screen.getByRole("tabpanel");
    expect(transit.getAttribute("aria-controls")).toBe(panel.id);
    expect(panel.getAttribute("aria-labelledby")).toBe(transit.id);
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/routes/"))).toHaveLength(0);
  });
});
