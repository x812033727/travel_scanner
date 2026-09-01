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
    expect(previewBody).toMatchObject({ version: 3, travel_mode: "walk", buffer_minutes: 10 });
    fireEvent.click(screen.getByRole("button", { name: "套用此路線" }));
    await waitFor(() => expect(applied).toHaveBeenCalledOnce());
    expect(applyBody).toMatchObject({ version: 3, source: "provider", preview_id: "preview-1" });
  });
});
