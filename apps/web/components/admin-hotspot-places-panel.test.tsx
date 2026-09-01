import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotPlacesPanel } from "./admin-hotspot-places-panel";

const profiles = {
  items: [{
    hotspot_id: "11111111-1111-4111-8111-111111111111",
    name: "原子彈爆炸圓頂屋",
    city_name: "廣島",
    country_code: "JP",
    google_place_id: "ChIJqQAn28yiWjURlsDG4Hrn5jQ",
    place_id_source: "legacy",
    match_status: "approved",
    match_confidence: 1,
    candidate: null,
    website_review_status: "approved",
    provider_website_url: "https://www.city.hiroshima.lg.jp/atomicbomb-peace/",
    manual_official_website_url: null,
    address: "1-10 Otemachi, Naka Ward, Hiroshima",
    refresh_after: "2026-09-22T00:00:00Z",
    expires_at: "2026-10-01T00:00:00Z",
    summary: {
      status: "ready",
      google_maps_url: "https://www.google.com/maps/place/?q=place_id:ChIJqQAn28yiWjURlsDG4Hrn5jQ",
      official_website_url: "https://www.city.hiroshima.lg.jp/atomicbomb-peace/",
    },
  }],
  total: 450,
  page: 1,
  pages: 5,
  overview: {
    configured: true,
    total: 450,
    ready: 1,
    pending: 0,
    unmatched: 0,
    failed: 0,
    expired: 0,
    missing_place_ids: 120,
    usage: {
      period: "2026-09",
      used: 12,
      free_remaining: 988,
      available: true,
      sku_usage: [{ sku: "place_details_enterprise", used: 12, free_limit: 1000, percentage: 1.2 }],
    },
  },
};

afterEach(() => vi.unstubAllGlobals());

describe("AdminHotspotPlacesPanel", () => {
  it("shows complete coverage and requires an API usage confirmation", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST" && url.endsWith("/place-enrichment/runs")) {
        return Promise.resolve(new Response(JSON.stringify({
          run_id: "run-1",
          status: "completed",
          progress: 100,
          counts: { total: 450, processed: 450, published: 440, pending: 5, unmatched: 3, failed: 2 },
          usage: { estimated_google_calls: 570, actual_google_calls: 570 },
        }), { status: 202 }));
      }
      return Promise.resolve(new Response(JSON.stringify(profiles)));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotPlacesPanel />);

    expect(await screen.findByText("首輪約 570 次呼叫；實際數量依既有 Place ID 而定。")).toBeTruthy();
    expect(screen.getByText("原子彈爆炸圓頂屋")).toBeTruthy();
    const start = screen.getByRole("button", { name: "開始補齊" });
    expect((start as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByLabelText("我已確認預估 Google API 用量"));
    expect((start as HTMLButtonElement).disabled).toBe(false);
    fireEvent.click(start);

    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(
      "/api/travel/admin/hotspots/place-enrichment/runs",
      expect.objectContaining({ method: "POST" }),
    ));
    expect(await screen.findByText("更新狀態：completed")).toBeTruthy();
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(post?.[1]?.body))).toMatchObject({
      scope: "all",
      mode: "missing_or_expired",
      confirm_usage: true,
    });
  });
});
