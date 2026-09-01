import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { RouteMap } from "./route-map";

vi.mock("next/script", () => ({
  default: ({ src }: { src: string }) => <div data-testid="next-script" data-src={src} />,
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

function ok(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => vi.unstubAllGlobals());

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
    expect(screen.getByRole("img", { name: /景福宮到北村韓屋村的 NAVER 地圖/ })).toBeTruthy();
    expect(container.querySelector(".route-map-frame")).toBeTruthy();
    expect(container.querySelector("iframe")).toBeNull();
  });

  it("falls back to Google Embed with coordinates instead of NAVER place IDs", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({
      google_maps_browser_key: "google-browser-key",
      google_maps_embed_enabled: true,
      naver_dynamic_map_enabled: false,
    })));
    render(<RouteMap items={items} fromItemId="from" toItemId="to" countryCode="KR" />);

    await waitFor(() => expect(screen.getByTitle("行程路線地圖")).toBeTruthy());
    const src = screen.getByTitle("行程路線地圖").getAttribute("src") || "";
    expect(src).toContain("origin=37.5796%2C126.977");
    expect(src).toContain("destination=37.5826%2C126.985");
    expect(src).not.toContain("naver-origin-id");
    expect(src).not.toContain("naver-destination-id");
  });
});
