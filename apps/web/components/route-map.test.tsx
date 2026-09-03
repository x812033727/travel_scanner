import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { RouteMap } from "./route-map";

vi.mock("next/script", () => ({
  default: ({ src, onReady }: { src: string; onReady?: () => void }) => {
    if (onReady) setTimeout(onReady, 0);
    return <div data-testid="next-script" data-src={src} />;
  },
}));

const items = [
  {
    id: "from",
    item_type: "suggestion",
    day_date: "2026-11-10",
    position: 0,
    title: "景福宮",
    latitude: 37.5796,
    longitude: 126.977,
    provider_place_id: "naver-origin-id",
    location_provider: "naver_local",
    locked: false,
    is_estimated: false,
    data: { place_provider: "naver_local" },
  },
  {
    id: "to",
    item_type: "suggestion",
    day_date: "2026-11-10",
    position: 1,
    title: "北村韓屋村",
    latitude: 37.5826,
    longitude: 126.985,
    provider_place_id: "naver-destination-id",
    location_provider: "naver_local",
    locked: false,
    is_estimated: false,
    data: { place_provider: "naver_local" },
  },
];

const segment = {
  from_item_id: "from",
  to_item_id: "to",
  status: "resolved",
  travel_mode: "transit" as const,
  provider: "google_routes",
  attribution: "Google Maps",
  generated_at: "2026-09-03T00:00:00Z",
  schedule_mode: "preview" as const,
  preference: "FEWER_TRANSFERS",
  duration_minutes: 24,
  steps: [],
  details_available: [],
  warnings: [],
};

function ok(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
  window.gm_authFailure = undefined;
  window.mokaairGoogleMapsAuthFailed = undefined;
  window.google = undefined;
  window.naver = undefined;
});

describe("RouteMap", () => {
  it("loads NAVER Dynamic Map for Korean trips in a fixed map frame", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      naver_maps_browser_client_id: "browser-client-id",
      naver_dynamic_map_enabled: true,
      google_maps_embed_enabled: false,
    })));
    const { container } = render(
      <RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" />,
    );

    const script = await screen.findByTestId("next-script");
    expect(script.getAttribute("data-src")).toBe(
      "https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=browser-client-id",
    );
    expect(screen.getByRole("img", { name: /景福宮到北村韓屋村的NAVER Maps路線地圖/ })).toBeTruthy();
    expect(screen.getByText("示意連線，非實際路線")).toBeTruthy();
    expect(container.querySelector(".route-map-frame")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();
  });

  it("does not load Google Maps for a Korean trip when NAVER Dynamic Map is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
      naver_dynamic_map_enabled: false,
    })));
    const { container } = render(<RouteMap items={items} segment={segment} fromItemId="from" toItemId="to" countryCode="KR" />);

    expect(await screen.findByText("瀏覽器地圖服務尚未啟用")).toBeTruthy();
    expect(screen.getByText("請在管理設定啟用 NAVER Dynamic Map。")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();
    expect(screen.queryByTestId("next-script")).toBeNull();
  });

  it("loads a Google JavaScript basemap with endpoints before a provider route exists", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
      naver_dynamic_map_enabled: false,
    })));
    const { container } = render(
      <RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />,
    );

    const script = await screen.findByTestId("next-script");
    expect(script.getAttribute("data-src")).toContain("https://maps.googleapis.com/maps/api/js");
    expect(script.getAttribute("data-src")).toContain("key=google-browser-key");
    expect(script.getAttribute("data-src")).toContain("loading=async");
    expect(screen.getByRole("img", { name: /景福宮到北村韓屋村的Google Maps路線地圖/ })).toBeTruthy();
    expect(screen.getByText("示意連線，非實際路線")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();
  });

  it("does not load Google Maps when a browser key exists without the explicit safety gate", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_embed_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    expect(await screen.findByText("瀏覽器地圖已安全停用")).toBeTruthy();
    expect(screen.getByText(/再開啟安全閘門/)).toBeTruthy();
    expect(screen.queryByTestId("next-script")).toBeNull();
  });

  it("fails closed when public runtime config cannot be loaded", async () => {
    vi.stubEnv("NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY", "baked-browser-key");
    vi.stubGlobal("fetch", vi.fn(async () => { throw new Error("runtime unavailable"); }));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    expect(await screen.findByText("瀏覽器地圖服務尚未啟用")).toBeTruthy();
    expect(screen.queryByTestId("next-script")).toBeNull();
  });

  it("shows an actionable state when Google rejects the current referrer", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    expect(await screen.findByRole("img", { name: /Google Maps路線地圖/ })).toBeTruthy();
    expect(window.gm_authFailure).toBeTypeOf("function");
    act(() => window.gm_authFailure?.());

    expect(await screen.findByText("地圖載入失敗")).toBeTruthy();
    expect(screen.getByText(/尚未允許目前網站網域/)).toBeTruthy();
    expect(screen.queryByRole("img", { name: /Google Maps路線地圖/ })).toBeNull();
    expect(screen.queryByTestId("next-script")).toBeNull();
  });

  it("installs the Google authorization guard before the public config enables the SDK", async () => {
    let releaseConfig: ((response: Response) => void) | undefined;
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>((resolve) => {
      releaseConfig = resolve;
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    await waitFor(() => expect(window.gm_authFailure).toBeTypeOf("function"));
    expect(screen.queryByTestId("next-script")).toBeNull();
    act(() => releaseConfig?.(ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
    })));

    expect(await screen.findByTestId("next-script")).toBeTruthy();
  });

  it("does not let an earlier Google authorization failure disable NAVER Maps", async () => {
    window.mokaairGoogleMapsAuthFailed = true;
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      naver_maps_browser_client_id: "browser-client-id",
      naver_dynamic_map_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" />);

    expect((await screen.findByTestId("next-script")).getAttribute("data-src"))
      .toContain("oapi.map.naver.com");
    expect(screen.queryByText("地圖載入失敗")).toBeNull();
  });

  it("draws every provider option and makes each line selectable", async () => {
    const lineOptions: Array<Record<string, unknown>> = [];
    const lineClicks: Array<() => void> = [];
    class TestMap {
      fitBounds() { return undefined; }
    }
    class TestBounds {
      extend() { return undefined; }
    }
    class TestMarker {
      constructor() {}
      setMap() { return undefined; }
    }
    class TestPolyline {
      constructor(options: Record<string, unknown>) { lineOptions.push(options); }
      setMap() { return undefined; }
      addListener(_eventName: string, handler: () => void) { lineClicks.push(handler); }
    }
    window.google = { maps: {
      Map: TestMap,
      LatLngBounds: TestBounds,
      Marker: TestMarker,
      Polyline: TestPolyline,
    } };
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
    })));
    const onSelect = vi.fn();
    const options = [18, 21, 25].map((duration, index) => ({
      ...segment,
      duration_minutes: duration,
      encoded_polyline: index === 0
        ? "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
        : index === 1 ? "_p~iF~ps|U_mqNvxq`@" : "_p~iF~ps|U_ulLnnqC",
    }));

    render(<RouteMap items={items} segments={options} selectedSegmentIndex={1} onSelectSegment={onSelect} fromItemId="from" toItemId="to" countryCode="JP" />);

    await waitFor(() => expect(lineOptions).toHaveLength(3));
    expect(lineOptions.map((option) => option.strokeOpacity)).toEqual([0.3, 0.96, 0.3]);
    fireEvent.click(screen.getByRole("img", { name: /Google Maps路線地圖/ }));
    lineClicks[2]();
    expect(onSelect).toHaveBeenCalledWith(2);
  });
});
