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
  document.getElementById("google-route-maps-js")?.remove();
  window.gm_authFailure = undefined;
  window.mokaairGoogleMapsAuthFailed = undefined;
  window.__mokaairGoogleMapsReady = undefined;
  window.google = undefined;
  window.naver = undefined;
});

describe("RouteMap", () => {
  it.each(["transit", "walk", "drive"] as const)("identifies the selected Korean %s map even when both browser keys are disabled", async (travelMode) => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false, naver_dynamic_map_enabled: false })));
    const { container } = render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" travelMode={travelMode} />);
    expect(await screen.findByText("瀏覽器地圖服務尚未啟用")).toBeTruthy();
    expect(screen.getByText(`站內地圖 · ${travelMode === "transit" ? "Google Maps" : "NAVER Maps"}`)).toBeTruthy();
    expect(screen.queryByRole("region", { name: /路線地圖/ })).toBeNull();
    expect(container.querySelector("iframe")).toBeNull();
    expect(document.getElementById("google-route-maps-js")).toBeNull();
    expect(screen.queryByTestId("next-script")).toBeNull();
    if (travelMode === "walk") {
      fireEvent.change(screen.getByRole("combobox", { name: "顯示地圖" }), { target: { value: "google_maps" } });
      expect(screen.getByText("站內地圖 · Google Maps")).toBeTruthy();
      expect(screen.getByText("瀏覽器地圖服務尚未啟用")).toBeTruthy();
      expect(screen.queryByRole("region", { name: /路線地圖/ })).toBeNull();
    }
  });

  it("loads NAVER Dynamic Map for Korean trips in a fixed map frame", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      naver_maps_browser_client_id: "browser-client-id",
      naver_dynamic_map_enabled: true,
      google_maps_embed_enabled: false,
    })));
    const { container } = render(
      <RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" travelMode="walk" />,
    );

    const script = await screen.findByTestId("next-script");
    expect(script.getAttribute("data-src")).toBe(
      "https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=browser-client-id",
    );
    expect(screen.getByRole("region", { name: /景福宮到北村韓屋村的NAVER Maps路線地圖/ })).toBeTruthy();
    expect(screen.getByText("示意連線，非實際路線")).toBeTruthy();
    expect(container.querySelector(".route-map-frame")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();
  });

  it("keeps Korean driving on NAVER when that map is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
      naver_dynamic_map_enabled: false,
    })));
    const { container } = render(<RouteMap items={items} segment={segment} fromItemId="from" toItemId="to" countryCode="KR" travelMode="drive" />);

    expect(await screen.findByText("瀏覽器地圖服務尚未啟用")).toBeTruthy();
    expect(screen.getByText("請在管理設定啟用 NAVER Dynamic Map。")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();
    expect(screen.queryByTestId("next-script")).toBeNull();
    expect(document.getElementById("google-route-maps-js")).toBeNull();
    expect(screen.queryByRole("combobox")).toBeNull();
  });

  it("loads a Google JavaScript basemap with endpoints before a provider route exists", async () => {
    const mapOptions: Array<Record<string, unknown>> = [];
    class TestMap {
      constructor(_element: HTMLElement, options: Record<string, unknown>) { mapOptions.push(options); }
      fitBounds() { return undefined; }
    }
    class TestBounds {
      extend() { return undefined; }
    }
    class TestOverlay {
      setMap() { return undefined; }
      addListener() { return undefined; }
    }
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
      naver_dynamic_map_enabled: false,
    })));
    const { container } = render(
      <RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />,
    );

    await waitFor(() => expect(document.getElementById("google-route-maps-js")).toBeTruthy());
    const script = document.getElementById("google-route-maps-js") as HTMLScriptElement;
    expect(script.src).toContain("https://maps.googleapis.com/maps/api/js");
    expect(script.src).toContain("key=google-browser-key");
    expect(script.src).toContain("v=quarterly");
    expect(script.src).toContain("loading=async");
    expect(script.src).toContain("callback=__mokaairGoogleMapsReady");
    expect(script.src).toContain("auth_referrer_policy=origin");
    expect(screen.getByRole("region", { name: /景福宮到北村韓屋村的Google Maps路線地圖/ })).toBeTruthy();
    expect(screen.getByText("示意連線，非實際路線")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();

    window.google = { maps: {
      RenderingType: { RASTER: "RASTER" },
      Map: TestMap,
      LatLngBounds: TestBounds,
      Marker: TestOverlay,
      Polyline: TestOverlay,
    } };
    act(() => window.__mokaairGoogleMapsReady?.());
    await waitFor(() => expect(mapOptions).toHaveLength(1));
    expect(mapOptions[0].renderingType).toBe("RASTER");
  });

  it("does not load Google Maps when a browser key exists without the explicit safety gate", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_embed_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    expect(await screen.findByText("瀏覽器地圖已安全停用")).toBeTruthy();
    expect(screen.getByText(/再開啟安全閘門/)).toBeTruthy();
    expect(document.getElementById("google-route-maps-js")).toBeNull();
  });

  it("fails closed when public runtime config cannot be loaded", async () => {
    vi.stubEnv("NEXT_PUBLIC_GOOGLE_MAPS_BROWSER_KEY", "baked-browser-key");
    vi.stubGlobal("fetch", vi.fn(async () => { throw new Error("runtime unavailable"); }));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    expect(await screen.findByText("瀏覽器地圖服務尚未啟用")).toBeTruthy();
    expect(document.getElementById("google-route-maps-js")).toBeNull();
  });

  it("shows an actionable state when Google rejects the current referrer", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    expect(await screen.findByRole("region", { name: /Google Maps路線地圖/ })).toBeTruthy();
    expect(window.gm_authFailure).toBeTypeOf("function");
    act(() => window.gm_authFailure?.());

    expect(await screen.findByText("地圖載入失敗")).toBeTruthy();
    expect(screen.getByText(/尚未允許目前網站網域/)).toBeTruthy();
    expect(screen.queryByRole("region", { name: /Google Maps路線地圖/ })).toBeNull();
    expect(window.mokaairGoogleMapsAuthFailed).toBe(true);
  });

  it("installs the Google authorization guard before the public config enables the SDK", async () => {
    let releaseConfig: ((response: Response) => void) | undefined;
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>((resolve) => {
      releaseConfig = resolve;
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    await waitFor(() => expect(window.gm_authFailure).toBeTypeOf("function"));
    expect(document.getElementById("google-route-maps-js")).toBeNull();
    act(() => releaseConfig?.(ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_javascript_enabled: true,
    })));

    await waitFor(() => expect(document.getElementById("google-route-maps-js")).toBeTruthy());
  });

  it("does not let an earlier Google authorization failure disable NAVER Maps", async () => {
    window.mokaairGoogleMapsAuthFailed = true;
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      naver_maps_browser_client_id: "browser-client-id",
      naver_dynamic_map_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" travelMode="walk" />);

    expect((await screen.findByTestId("next-script")).getAttribute("data-src"))
      .toContain("oapi.map.naver.com");
    expect(screen.queryByText("地圖載入失敗")).toBeNull();
  });

  it("draws every provider option and makes each line selectable", async () => {
    const lineOptions: Array<Record<string, unknown>> = [];
    const lineClicks: Array<() => void> = [];
    const mapConstructed = vi.fn();
    class TestMap {
      constructor() { mapConstructed(); }
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

    const { rerender } = render(<RouteMap items={items} segments={options} selectedSegmentIndex={1} onSelectSegment={onSelect} fromItemId="from" toItemId="to" countryCode="JP" />);

    await waitFor(() => expect(lineOptions).toHaveLength(3));
    expect(lineOptions.map((option) => option.strokeOpacity)).toEqual([0.3, 0.96, 0.3]);
    expect(mapConstructed).toHaveBeenCalledTimes(1);
    rerender(<RouteMap items={items} segments={options} selectedSegmentIndex={2} onSelectSegment={onSelect} fromItemId="from" toItemId="to" countryCode="JP" />);
    await waitFor(() => expect(lineOptions).toHaveLength(6));
    expect(mapConstructed).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole("region", { name: /Google Maps路線地圖/ }));
    lineClicks[5]();
    expect(onSelect).toHaveBeenCalledWith(2);
  });

  it("uses Google for Korean transit while clearly attributing the independent ODsay time", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_browser_key: "google", google_maps_javascript_enabled: true, naver_maps_browser_client_id: "naver", naver_dynamic_map_enabled: true })));
    render(<RouteMap items={items} segment={{ ...segment, provider: "odsay", attribution: "ODsay" }} countryCode="KR" />);
    expect(await screen.findByRole("region", { name: /Google Maps路線地圖/ })).toBeTruthy();
    expect(screen.getByText("交通時間來源：ODsay")).toBeTruthy();
    expect(screen.getByText("示意連線，非實際路線")).toBeTruthy();
    expect(screen.queryByTestId("next-script")).toBeNull();
    expect(screen.queryByRole("combobox")).toBeNull();
  });

  it("switches walking maps without requests or paths, disposes old overlays, and keeps failures independent", async () => {
    const destroyed = vi.fn();
    const naverCleared = vi.fn();
    const googleCleared = vi.fn();
    const detached = vi.fn();
    const naverLines: Array<Record<string, unknown>> = [];
    const googleLines: Array<Record<string, unknown>> = [];
    class NaverMap { fitBounds() {} destroy() { destroyed(); } }
    class GoogleMap { fitBounds() {} }
    class Bounds { extend() {} }
    class Point {}
    class Marker { setMap(value: unknown) { detached(value); } }
    class NaverLine extends Marker { constructor(options: Record<string, unknown>) { super(); naverLines.push(options); } }
    class GoogleLine extends Marker { constructor(options: Record<string, unknown>) { super(); googleLines.push(options); } addListener() {} }
    window.naver = { maps: { Map: NaverMap, LatLng: Point, LatLngBounds: Bounds, Marker, Polyline: NaverLine, Event: { addListener() {}, clearInstanceListeners: naverCleared } } };
    window.google = { maps: { Map: GoogleMap, LatLngBounds: Bounds, Marker, Polyline: GoogleLine, event: { clearInstanceListeners: googleCleared } } };
    const fetchMock = vi.fn(async () => ok({ google_maps_browser_key: "google", google_maps_javascript_enabled: true, naver_maps_browser_client_id: "naver", naver_dynamic_map_enabled: true }));
    vi.stubGlobal("fetch", fetchMock);
    const props = { items, countryCode: "KR", segment: { ...segment, travel_mode: "walk" as const, encoded_polyline: "_p~iF~ps|U_ulLnnqC" } };
    const { rerender, unmount } = render(<RouteMap {...props} />);
    const select = screen.getByRole("combobox", { name: "顯示地圖" });
    expect((select as HTMLSelectElement).value).toBe("naver_maps");
    await waitFor(() => expect(naverLines).toHaveLength(1));
    expect(naverLines[0].strokeStyle).toBe("shortdash");
    fireEvent.change(select, { target: { value: "google_maps" } });
    await waitFor(() => expect(googleLines).toHaveLength(1));
    expect(googleLines[0].icons).toBeTruthy();
    expect(destroyed).toHaveBeenCalledTimes(1);
    expect(naverCleared).toHaveBeenCalledTimes(3);
    expect(detached).toHaveBeenCalledWith(null);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    act(() => window.gm_authFailure?.());
    expect(await screen.findByText("地圖載入失敗")).toBeTruthy();
    fireEvent.change(select, { target: { value: "naver_maps" } });
    expect(await screen.findByRole("region", { name: /NAVER Maps路線地圖/ })).toBeTruthy();
    expect(screen.queryByText("地圖載入失敗")).toBeNull();
    fireEvent.change(select, { target: { value: "google_maps" } });
    expect(await screen.findByText("地圖載入失敗")).toBeTruthy();
    rerender(<RouteMap {...props} travelMode="drive" />);
    expect(screen.queryByRole("combobox")).toBeNull();
    expect(await screen.findByRole("region", { name: /NAVER Maps路線地圖/ })).toBeTruthy();
    // A legacy Google geometry must never be painted on the driving NAVER map.
    expect(naverLines.every((line) => line.strokeStyle === "shortdash")).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    unmount();
    expect(googleCleared).toHaveBeenCalled();
  });

  it("marks the selected missing path schematic even when another real option can be drawn", async () => {
    const lineOptions: Array<Record<string, unknown>> = [];
    class TestMap { fitBounds() {} }
    class TestBounds { extend() {} }
    class TestMarker { setMap() {} }
    class TestPolyline {
      constructor(options: Record<string, unknown>) { lineOptions.push(options); }
      setMap() {}
      addListener() {}
    }
    window.google = { maps: { Map: TestMap, LatLngBounds: TestBounds, Marker: TestMarker, Polyline: TestPolyline } };
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_browser_key: "test", google_maps_javascript_enabled: true })));
    const options = [
      { ...segment, encoded_polyline: "_p~iF~ps|U_ulLnnqC_mqNvxq`@" },
      { ...segment, encoded_polyline: null },
    ];
    const props = { items, segments: options, fromItemId: "from", toItemId: "to", countryCode: "JP" };
    const { rerender } = render(<RouteMap {...props} selectedSegmentIndex={1} />);
    await waitFor(() => expect(lineOptions).toHaveLength(2));
    expect(lineOptions[0]).toMatchObject({ strokeOpacity: 0.3, strokeWeight: 4 });
    expect(lineOptions[1].icons).toBeTruthy();
    expect(screen.getByText("示意連線，非實際路線")).toBeTruthy();
    rerender(<RouteMap {...props} selectedSegmentIndex={0} />);
    await waitFor(() => expect(lineOptions).toHaveLength(3));
    expect(lineOptions[2]).toMatchObject({ strokeOpacity: 0.96, strokeWeight: 6 });
    expect(screen.queryByText("示意連線，非實際路線")).toBeNull();
  });
});

describe("route map gestures and reach", () => {
  /**
   * On a phone this map sits inside .planner-sheet-body, whose overscroll-behavior
   * leaves a swallowed swipe nowhere to go: a finger dragged across the map used to
   * pan the map and freeze the page. Google is told cooperative explicitly rather
   * than left on "auto", which only degrades when it judges the page scrollable, and
   * NAVER — which has no cooperative mode at all — simply does not drag inline.
   */
  it("leaves a one-finger swipe to the page until the map is expanded", async () => {
    const naverOptions: Array<Record<string, unknown>> = [];
    const googleOptions: Array<Record<string, unknown>> = [];
    class NaverMap {
      constructor(_element: HTMLElement, options: Record<string, unknown>) { naverOptions.push(options); }
      fitBounds() {}
      destroy() {}
    }
    class GoogleMap {
      constructor(_element: HTMLElement, options: Record<string, unknown>) { googleOptions.push(options); }
      fitBounds() {}
      setOptions() {}
    }
    class Bounds { extend() {} }
    class Point {}
    class Marker { setMap() {} }
    class Line extends Marker { addListener() {} }
    window.naver = { maps: { Map: NaverMap, LatLng: Point, LatLngBounds: Bounds, Marker, Polyline: Line, Event: { addListener() {}, clearInstanceListeners() {} } } };
    window.google = { maps: { Map: GoogleMap, LatLngBounds: Bounds, Marker, Polyline: Line, event: { clearInstanceListeners() {} } } };
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      naver_maps_browser_client_id: "naver", naver_dynamic_map_enabled: true,
      google_maps_browser_key: "google", google_maps_javascript_enabled: true,
    })));

    const { container } = render(
      <RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" travelMode="walk" />,
    );
    await waitFor(() => expect(naverOptions).not.toHaveLength(0));
    expect(naverOptions.at(-1)?.draggable).toBe(false);
    expect(naverOptions.at(-1)?.pinchZoom).toBe(true);
    expect(container.querySelector(".route-map-expanded")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "放大地圖" }));

    expect(container.querySelector(".route-map-expanded")).toBeTruthy();
    await waitFor(() => expect(naverOptions.at(-1)?.draggable).toBe(true));
    expect(screen.getByRole("button", { name: "收合地圖" }).getAttribute("aria-expanded")).toBe("true");

    fireEvent.keyDown(document, { key: "Escape" });
    expect(container.querySelector(".route-map-expanded")).toBeNull();
  });

  it("never leaves Google's gesture handling to the default", async () => {
    const googleOptions: Array<Record<string, unknown>> = [];
    class GoogleMap {
      constructor(_element: HTMLElement, options: Record<string, unknown>) { googleOptions.push(options); }
      fitBounds() {}
      setOptions() {}
    }
    class Bounds { extend() {} }
    class Marker { setMap() {} }
    class Line extends Marker { addListener() {} }
    window.google = { maps: { Map: GoogleMap, LatLngBounds: Bounds, Marker, Polyline: Line, event: { clearInstanceListeners() {} } } };
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google", google_maps_javascript_enabled: true,
    })));

    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="JP" />);

    await waitFor(() => expect(googleOptions).not.toHaveLength(0));
    expect(googleOptions.at(-1)?.gestureHandling).toBe("cooperative");
  });

  it("hands the map's markers and controls to assistive technology", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      naver_maps_browser_client_id: "naver", naver_dynamic_map_enabled: true,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" travelMode="walk" />);

    // role="img" made the whole subtree presentational, so every marker, control
    // and route the SDK drew into it disappeared from a screen reader.
    const map = await screen.findByRole("region", { name: /路線地圖/ });
    expect(map.getAttribute("role")).toBe("region");
    expect(screen.queryByRole("img", { name: /路線地圖/ })).toBeNull();
  });
});
