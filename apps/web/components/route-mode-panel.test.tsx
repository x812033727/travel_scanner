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
  it.each([
    { status: "unconfigured", provider: "odsay", mode: "transit" as const },
    { status: "external_only", provider: null, mode: "walk" as const },
    { status: "unconfigured", provider: "naver_maps", mode: "drive" as const },
  ])("uses direct external actions without a route query for $status $mode", async ({ status, provider, mode }) => {
    const fetchMock = vi.fn(async (url: string) => {
      if (!url.includes("/routes/navigation?")) throw new Error("Unexpected provider or SDK request");
      return ok({ route_availability: { status, provider, can_query: false }, external_navigations: [
        { provider: "naver_maps", label: "NAVER Maps", travel_mode: mode, web_url: "https://map.naver.com/p/directions/owned", app_url: "nmap://route/walk" },
      ] });
    });
    vi.stubGlobal("fetch", fetchMock);
    const { container } = render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" initialTravelMode={mode} onApplied={vi.fn()} onError={vi.fn()} />);
    const action = await screen.findByRole("link", { name: "前往 NAVER Maps 查看（離開本站）" });
    expect(action.getAttribute("href")).toBe("https://map.naver.com/p/directions/owned");
    expect(screen.getByText(mode === "transit" ? "目前未取得乘車步驟" : "目前未取得移動步驟")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "查詢交通方案" })).toBeNull();
    expect(screen.queryByRole("button", { name: "外部導航，無法套用" })).toBeNull();
    expect(container.querySelector("[data-map-provider]")).toBeNull();
    expect(screen.getByRole("combobox", { name: "移動緩衝時間" })).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("supports the available Google transit fallback and exposes its actual steps before the optional map", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      if (url.includes("/routes/navigation?")) return ok({ external_navigations: [], route_availability: { status: "available", provider: "google_routes", can_query: true } });
      return ok({ kind: "provider", preview_id: "google-fallback", expires_at: "2100-01-01T00:00:00Z", segment: { ...initialSegment,
        steps: [{ travel_mode: "TRANSIT", instruction: "搭乘1號線", departure_stop: "首爾站", arrival_stop: "市廳站", line_name: "1號線" },
          { travel_mode: "TRANSIT", instruction: "轉乘2號線", departure_stop: "市廳站", arrival_stop: "乙支路入口", line_name: "2號線" }],
      }, schedule_impact: { affected_items: [], conflicts: [] } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const { container } = render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    await screen.findByRole("button", { name: "套用此路線" });
    expect(screen.getByText("上車：首爾站")).toBeTruthy();
    expect(screen.getByText("轉乘上車：市廳站")).toBeTruthy();
    expect(screen.getByText("下車：乙支路入口")).toBeTruthy();
    expect(screen.getByText("交通時間來源：Google Maps")).toBeTruthy();
    expect(screen.queryByText("步行 0 分")).toBeNull();
    const detail = container.querySelector(".route-panel-detail")!;
    const map = container.querySelector(".route-panel-map")!;
    expect(document.activeElement).toBe(detail);
    expect(screen.queryByRole("listbox")).toBeNull();
    expect(screen.queryByText("選擇路線")).toBeNull();
    expect(Boolean(detail.compareDocumentPosition(map) & Node.DOCUMENT_POSITION_FOLLOWING)).toBe(true);
    expect((map as HTMLDetailsElement).open).toBe(false);
  });

  it("keeps a verified preview applicable when a later availability response disables new queries", async () => {
    let resolveNavigation!: (response: Response) => void;
    const navigationResponse = new Promise<Response>((resolve) => { resolveNavigation = resolve; });
    const applied = vi.fn();
    const fetchMock = vi.fn(async (url: string) => {
      if (url.includes("/routes/navigation?")) return navigationResponse;
      if (url.endsWith("/routes/apply")) return ok({ ...trip, version: 4 });
      return ok({ kind: "provider", preview_id: "verified-preview", expires_at: "2100-01-01T00:00:00Z",
        segment: initialSegment, schedule_impact: { affected_items: [], conflicts: [] } });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" onApplied={applied} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    const apply = await screen.findByRole("button", { name: "套用此路線" });
    await act(async () => resolveNavigation(ok({ external_navigations: [], route_availability: { status: "unconfigured", provider: "google_routes", can_query: false } })));
    expect((apply as HTMLButtonElement).disabled).toBe(false);
    expect(screen.queryByText("目前未取得乘車步驟")).toBeNull();
    fireEvent.click(apply);
    await waitFor(() => expect(applied).toHaveBeenCalledOnce());
    expect(fetchMock.mock.calls.filter(([url]) => url.endsWith("/routes/preview"))).toHaveLength(1);
  });

  it("does not request another query after switching from a transit preview to external-only walking", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      if (url.includes("/routes/navigation?")) {
        const walking = new URL(url, "http://localhost").searchParams.get("travel_mode") === "walk";
        return ok({ route_availability: { status: walking ? "external_only" : "available", provider: walking ? null : "google_routes", can_query: !walking },
          external_navigations: walking ? [{ provider: "naver_maps", label: "NAVER Maps", travel_mode: "walk", web_url: "https://map.naver.com/p/directions/owned", app_url: "nmap://route/walk" }] : [] });
      }
      return ok({ kind: "provider", preview_id: "transit-preview", expires_at: "2100-01-01T00:00:00Z",
        segment: initialSegment, schedule_impact: { affected_items: [], conflicts: [] } });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    await screen.findByRole("button", { name: "套用此路線" });
    fireEvent.click(screen.getByRole("tab", { name: "步行" }));
    await screen.findByRole("link", { name: "前往 NAVER Maps 查看（離開本站）" });
    expect(screen.getByText("目前未取得移動步驟")).toBeTruthy();
    expect(screen.queryByText("設定已變更，請重新查詢後再套用。")).toBeNull();
    expect(screen.queryByRole("button", { name: "查詢交通方案" })).toBeNull();
    expect(fetchMock.mock.calls.filter(([url]) => url.endsWith("/routes/preview"))).toHaveLength(1);
    fireEvent.click(screen.getByRole("tab", { name: "大眾運輸" }));
    expect((screen.getByRole("button", { name: "套用此路線" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("requires user-entered manual time and saves it explicitly without querying a provider", async () => {
    const bodies: Array<Record<string, unknown>> = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toContain("/routes/apply");
      bodies.push(JSON.parse(String(init?.body)));
      return ok({ ...trip, version: 4 });
    }));
    render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "手動輸入時間" }));
    const input = screen.getByRole("spinbutton");
    expect((input as HTMLInputElement).value).toBe("");
    const apply = screen.getByRole("button", { name: "套用手動時間" });
    expect((apply as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(input, { target: { value: "35" } });
    fireEvent.change(screen.getByRole("combobox", { name: "移動緩衝時間" }), { target: { value: "5" } });
    fireEvent.click(apply);
    await waitFor(() => expect(bodies).toEqual([expect.objectContaining({ source: "manual", duration_minutes: 35, buffer_minutes: 5 })]));
  });

  it("preserves a saved manual duration as manual, without calling it a map route option", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false })));
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={{ ...initialSegment, provider: "manual", status: "manual", duration_minutes: 35 }} onApplied={vi.fn()} onError={vi.fn()} />);
    expect(container.querySelector(".route-apply-selection")?.textContent).toContain("手動預留");
    expect(screen.getByText("排程出發")).toBeTruthy();
    expect(screen.queryByText("轉乘 0 次")).toBeNull();
    fireEvent.click(screen.getByText("查看地圖（起終點參考）"));
    await screen.findByText("瀏覽器地圖服務尚未啟用");
    expect(screen.queryByText(/方案 1 · 約 35/)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "修改手動預留時間" }));
    expect((screen.getByRole("spinbutton") as HTMLInputElement).value).toBe("35");
  });

  it("loads server navigation before querying and switches walking basemaps without requests or trip writes", async () => {
    const navigations = [
      { provider: "naver_maps", label: "NAVER Maps", travel_mode: "walk", web_url: "https://map.naver.com/p/directions/server-walk", app_url: "nmap://route/walk" },
      { provider: "google_maps", label: "Google Maps", travel_mode: "walk", web_url: "https://www.google.com/maps/dir/?api=1&travelmode=walking", app_url: "https://www.google.com/maps/dir/?api=1&travelmode=walking" },
    ];
    const fetchMock = vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_javascript_enabled: false });
      if (url.includes("/routes/navigation?")) return ok({ external_navigations: navigations });
      return ok({ kind: "external_only", preview_id: null, segment: null, external_navigations: navigations });
    });
    vi.stubGlobal("fetch", fetchMock);
    const applied = vi.fn();
    const { container } = render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" initialTravelMode="walk" onApplied={applied} onError={vi.fn()} />);
    const google = await screen.findByRole("link", { name: "用 Google Maps 導航" });
    expect(google.getAttribute("href")).toContain("travelmode=walking");
    expect(screen.getByRole("link", { name: "用 NAVER Maps 導航" }).getAttribute("href")).toContain("server-walk");
    expect(fetchMock.mock.calls.filter(([url]) => url.includes("/routes/navigation?"))).toHaveLength(1);
    fireEvent.click(screen.getByText("查看地圖（起終點參考）"));
    const selector = await screen.findByRole("combobox", { name: "顯示地圖" });
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => url.endsWith("/runtime/public-config"))).toBe(true));
    const callsBeforeSwitch = fetchMock.mock.calls.length;
    fireEvent.change(selector, { target: { value: "google_maps" } });
    expect(container.querySelector("[data-map-provider='google_maps']")).toBeTruthy();
    fireEvent.change(selector, { target: { value: "naver_maps" } });
    expect(fetchMock).toHaveBeenCalledTimes(callsBeforeSwitch);
    expect(applied).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    expect(await screen.findByRole("link", { name: "前往 NAVER Maps 查看（離開本站）" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "用 Google Maps 導航" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "用 NAVER Maps 導航" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "外部導航，無法套用" })).toBeNull();
    expect(container.querySelector(".route-apply-selection")?.textContent).not.toContain("分鐘");
    fireEvent.change(selector, { target: { value: "google_maps" } });
    expect(fetchMock.mock.calls.filter(([url]) => url.endsWith("/routes/preview"))).toHaveLength(1);
    expect(fetchMock.mock.calls.filter(([url]) => url.endsWith("/routes/apply"))).toHaveLength(0);
  });

  it("keeps both navigation choices on an applicable Korean transit preview", async () => {
    const navigations = [
      { provider: "naver_maps" as const, label: "NAVER Maps", travel_mode: "transit" as const, web_url: "https://map.naver.com/p/directions/server", app_url: "nmap://route/public" },
      { provider: "google_maps" as const, label: "Google Maps", travel_mode: "transit" as const, web_url: "https://www.google.com/maps/dir/?api=1", app_url: "https://www.google.com/maps/dir/?api=1" },
    ];
    vi.stubGlobal("fetch", vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_javascript_enabled: false });
      if (url.includes("/routes/navigation?")) return ok({ external_navigations: navigations });
      return ok({ kind: "provider", preview_id: "odsay-preview", expires_at: "2100-01-01T00:00:00Z", segment: { ...initialSegment, provider: "odsay", attribution: "ODsay" }, schedule_impact: { affected_items: [], conflicts: [] }, external_navigations: navigations });
    }));
    render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    expect(await screen.findByRole("button", { name: "套用此路線" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "用 NAVER Maps 導航" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "用 Google Maps 導航" })).toBeTruthy();
    expect(screen.getByText("交通時間來源：ODsay")).toBeTruthy();
  });

  it("keeps server navigation available when a Korean transit query fails", async () => {
    vi.stubGlobal("fetch", vi.fn(async (url: string) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_javascript_enabled: false });
      if (url.includes("/routes/navigation?")) return ok({ external_navigations: [
        { provider: "naver_maps", label: "NAVER Maps", travel_mode: "transit", web_url: "https://map.naver.com/p/directions/server", app_url: "nmap://route/public" },
        { provider: "google_maps", label: "Google Maps", travel_mode: "transit", web_url: "https://www.google.com/maps/dir/?api=1", app_url: "https://www.google.com/maps/dir/?api=1" },
      ] });
      return new Response(JSON.stringify({ detail: "Routing unavailable" }), { status: 503 });
    }));
    render(<RouteModePanel trip={{ ...trip, destination_country_code: "KR" }} items={items} fromItemId="from" toItemId="to" onApplied={vi.fn()} onError={vi.fn()} />);
    await screen.findByRole("link", { name: "用 Google Maps 導航" });
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    await screen.findByRole("alert");
    expect(screen.getByRole("link", { name: "用 Google Maps 導航" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "用 NAVER Maps 導航" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
  });

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

  it.each(["failed", "unavailable", "pending"])("does not label a %s saved route as applied or display its placeholder zero minutes", async (status) => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false })));
    let container!: HTMLElement;
    await act(async () => {
      ({ container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={{ ...initialSegment, status, duration_minutes: 0 }} onApplied={vi.fn()} onError={vi.fn()} />));
    });
    expect(container.querySelector("[data-route-state='unavailable']")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "目前已套用" })).toBeNull();
    expect(container.querySelector(".route-apply-selection")?.textContent).not.toContain("0 分鐘");
    expect(container.querySelector(".route-mode-tabs")?.textContent).not.toContain("0 分鐘");
    expect(container.querySelector(".route-panel-detail")).toBeNull();
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

  it("retains a provider route with a fixed-time conflict for explicit review and apply", async () => {
    const conflicting = { ...initialSegment, status: "conflict", warnings: ["固定預約可能遲到 12 分鐘"] };
    const applyBodies: Array<Record<string, unknown>> = [];
    const onApplied = vi.fn();
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_javascript_enabled: false });
      if (url.endsWith("/routes/apply")) {
        applyBodies.push(JSON.parse(String(init?.body)));
        return ok({ ...trip, version: 4, route_segments: [conflicting] });
      }
      return ok({ preview_id: "conflicting-provider", expires_at: "2100-01-01T00:00:00Z", segment: conflicting, schedule_impact: {
        affected_items: [],
        conflicts: [{ item_id: "to", title: "淺草預約", late_minutes: 12, suggestions: ["提早出發"] }],
      } });
    }));
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" onApplied={onApplied} onError={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" }));
    const applyButton = await screen.findByRole("button", { name: "套用此路線" });
    expect(container.querySelector("[data-route-state='preview']")).toBeTruthy();
    expect(screen.getByText("可能遲到 12 分鐘")).toBeTruthy();
    expect(screen.getByText("固定預約可能遲到 12 分鐘")).toBeTruthy();
    expect((applyButton as HTMLButtonElement).disabled).toBe(false);
    expect(applyBodies).toHaveLength(0);
    fireEvent.click(applyButton);
    await waitFor(() => expect(onApplied).toHaveBeenCalledOnce());
    expect(applyBodies[0]).toMatchObject({ source: "provider", preview_id: "conflicting-provider" });
  });

  it.each([
    { provider: "google_routes", state: "applied", label: "已套用路線，請留意預約衝突" },
    { provider: "manual", state: "manual", label: "已套用手動時間，未經地圖服務確認" },
  ])("preserves saved $provider conflict timing and its warning", async ({ provider, state, label }) => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ google_maps_javascript_enabled: false })));
    let container!: HTMLElement;
    await act(async () => {
      ({ container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={{ ...initialSegment, provider, status: "conflict", warnings: ["固定預約可能遲到 12 分鐘"] }} onApplied={vi.fn()} onError={vi.fn()} />));
    });
    expect(container.querySelector(`[data-route-state='${state}']`)).toBeTruthy();
    expect(screen.getByRole("status").textContent).toContain(label);
    expect(screen.getByText("固定預約可能遲到 12 分鐘")).toBeTruthy();
    expect((screen.getByRole("button", { name: "目前已套用" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
  });

  it.each([
    { provider: "estimate", schedule_mode: "scheduled" as const },
    { provider: "google_routes", schedule_mode: "estimate" as typeof initialSegment.schedule_mode },
  ])("does not treat a conflicted estimate as confirmed provider timing ($provider/$schedule_mode)", async ({ provider, schedule_mode }) => {
    const estimatedConflict = { ...initialSegment, provider, schedule_mode, status: "conflict", warnings: ["固定預約可能遲到 12 分鐘"] };
    const applyBodies: Array<unknown> = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/runtime/public-config")) return ok({ google_maps_javascript_enabled: false });
      if (url.endsWith("/routes/apply")) applyBodies.push(init?.body);
      return ok({ preview_id: "estimated-conflict", expires_at: "2100-01-01T00:00:00Z", segment: estimatedConflict, schedule_impact: { affected_items: [], conflicts: [] } });
    }));
    let container!: HTMLElement;
    await act(async () => {
      ({ container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={estimatedConflict} onApplied={vi.fn()} onError={vi.fn()} />));
    });
    expect(container.querySelector("[data-route-state='estimated']")).toBeTruthy();
    expect(screen.getByRole("status").textContent).toContain("估算移動時間");
    expect(screen.getByText("固定預約可能遲到 12 分鐘")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "目前已套用" })).toBeNull();
    await act(async () => { fireEvent.click(screen.getByRole("button", { name: "查詢交通方案" })); });
    expect(screen.queryByRole("button", { name: "套用此路線" })).toBeNull();
    expect(applyBodies).toHaveLength(0);
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
    const expandDetails = screen.getByRole("button", { name: /大眾運輸 · 24 分鐘/ });
    expect(expandDetails.getAttribute("aria-expanded")).toBe("true");
    expect(screen.getByText("步行至東京晴空塔站")).toBeTruthy();
    expect(screen.getByText("上車：TOKYO SKYTREE Sta.")).toBeTruthy();
    expect(screen.getByText("下車：言問橋")).toBeTruthy();
    expect(screen.getByText("月台 1")).toBeTruthy();
    const map = container.querySelector(".route-panel-map");
    const details = container.querySelector(".route-panel-detail");
    expect(map && details && Boolean(details.compareDocumentPosition(map) & Node.DOCUMENT_POSITION_FOLLOWING)).toBe(true);
    expect((map as HTMLDetailsElement).open).toBe(false);
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

    const externalLink = await screen.findByRole("link", { name: "前往 NAVER Maps 查看（離開本站）" });
    expect(externalLink.getAttribute("href")).toContain("https://map.naver.com/");
    expect(screen.queryByRole("button", { name: "外部導航，無法套用" })).toBeNull();
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

    const externalLink = await screen.findByRole("link", { name: "前往 Google Maps 查看（離開本站）" });
    expect(externalLink.getAttribute("href")).toContain("origin_place_id=from");
    expect(screen.getByRole("region", { name: "外部導航服務" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "開啟 NAVER App" })).toBeNull();
    expect(screen.queryByRole("button", { name: "外部導航，無法套用" })).toBeNull();
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

  it("keeps buffer visible and manual input blank without fetching on disclosure", async () => {
    const fetchMock = vi.fn(async (url: string) => url.endsWith("/runtime/public-config")
      ? ok({ google_maps_browser_key: null, google_maps_javascript_enabled: false })
      : ok({ ...trip, version: 4 }));
    vi.stubGlobal("fetch", fetchMock);
    const { container } = render(<RouteModePanel trip={trip} items={items} fromItemId="from" toItemId="to" initialSegment={initialSegment} onApplied={() => undefined} onError={() => undefined} />);
    expect(container.querySelector(".route-advanced-settings")).toBeNull();
    expect(screen.getByRole("combobox", { name: "移動緩衝時間" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "手動輸入時間" }));
    const input = screen.getByRole("spinbutton");
    expect(document.activeElement).toBe(input);
    expect((input as HTMLInputElement).value).toBe("");
    expect((screen.getByRole("button", { name: "套用手動時間" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(input, { target: { value: "35" } });
    fireEvent.click(screen.getByRole("button", { name: "取消自訂時間" }));
    expect(screen.queryByRole("spinbutton")).toBeNull();
    await waitFor(() => expect(document.activeElement).toBe(screen.getByRole("button", { name: "手動輸入時間" })));
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
