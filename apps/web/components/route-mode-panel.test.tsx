import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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

afterEach(() => vi.unstubAllGlobals());

describe("route mode panel", () => {
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
    expect(screen.getByText("步行至東京晴空塔站")).toBeTruthy();
    expect(screen.getByText(/TOKYO SKYTREE Sta\. → 言問橋/)).toBeTruthy();
    expect(screen.getByText("月台 1")).toBeTruthy();
    const map = container.querySelector(".route-panel-map");
    const details = container.querySelector(".route-panel-detail");
    expect(map && details && Boolean(map.compareDocumentPosition(details) & Node.DOCUMENT_POSITION_FOLLOWING)).toBe(true);
  });

  it("auto-previews the default mode when no route has been applied", async () => {
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
        expires_at: "2026-09-01T00:15:00Z",
        segment: initialSegment,
        schedule_impact: { affected_items: [], conflicts: [] },
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<RouteModePanel trip={noRouteTrip} items={items} fromItemId="from" toItemId="to" onApplied={() => undefined} onError={() => undefined} />);

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

    const externalLink = await screen.findByRole("link", { name: /用 Google Maps 規劃/ });
    expect(externalLink.getAttribute("href")).toContain("origin_place_id=from");
    expect(screen.getByRole("region", { name: "Google Maps 外部導航" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "開啟 NAVER App" })).toBeNull();
    expect((screen.getByRole("button", { name: "外部導航，無法套用" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("resolves missing endpoints and opens the correct item editor when unresolved", async () => {
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

    fireEvent.click(await screen.findByRole("button", { name: "補上地點" }));
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
        return ok({ preview_id: "preview-1", expires_at: "2026-09-01T00:15:00Z", segment: walking, schedule_impact: { affected_items: [], conflicts: [] } });
      }
      applyBody = JSON.parse(String(init?.body));
      return ok({ ...trip, version: 4, route_segments: [walking] });
    });
    vi.stubGlobal("fetch", fetchMock);
    const applied = vi.fn();
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={applied} onError={() => undefined} />);

    fireEvent.click(screen.getByRole("tab", { name: "步行" }));
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
      expires_at: "2026-09-01T00:15:00Z",
      segment: {
        ...initialSegment,
        travel_mode: "walk" as const,
        duration_minutes: duration,
        route_option_rank: index + 1,
        encoded_polyline: `_p~iF~ps|U_ulLnnqC_mqNvxq\`${index}`,
      },
      schedule_impact: { affected_items: [], conflicts: [] },
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
    const secondOption = await screen.findByRole("option", { name: /方案 2/ });
    fireEvent.click(secondOption);
    expect(secondOption.getAttribute("aria-selected")).toBe("true");
    expect(screen.getByText(/步行 · 方案 2 · 21 分鐘/)).toBeTruthy();
    expect(previewCalls).toBe(1);

    fireEvent.click(screen.getByRole("button", { name: "套用此路線" }));
    await waitFor(() => expect(applyBody).toMatchObject({ preview_id: "preview-2" }));
    expect(previewCalls).toBe(1);
  });
});
