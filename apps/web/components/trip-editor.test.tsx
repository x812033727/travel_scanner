import { fireEvent, render, screen, waitFor } from "@testing-library/react";
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

afterEach(() => {
  window.localStorage.clear();
  window.history.replaceState({}, "", window.location.href);
  vi.unstubAllGlobals();
});
describe("trip editor", () => {
  it("opens mobile trip tools and remembers the selected color theme", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(response(trip))));
    const { container } = render(<TripEditor tripId={trip.id} />);

    fireEvent.click(await screen.findByRole("button", { name: "開啟旅程工具" }));
    expect(screen.getByRole("dialog", { name: "旅程工具" })).toBeTruthy();
    expect(screen.getByRole("group", { name: "路線偏好" })).toBeTruthy();

    fireEvent.click(screen.getByRole("radio", { name: /海岸/ }));
    expect(container.querySelector("[data-planner-theme='ocean']")).toBeTruthy();
    expect(window.localStorage.getItem("travel-planner-theme")).toBe("ocean");
  });

  it("lets the user ask MiniMax to arrange only the selected day", async () => {
    let generationBody: Record<string, unknown> | undefined;
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.includes("/itinerary/generate")) {
        generationBody = JSON.parse(String(init?.body));
        return response({
          ...trip,
          version: 2,
          planning: {
            status: "live",
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
            title: "MiniMax 安排的淺草散步",
            data: { generated_by: "ai_planner" },
          }],
        });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    const aiButtons = await screen.findAllByRole("button", { name: "AI 幫我安排" });
    fireEvent.click(aiButtons[0]);
    expect(screen.getByRole("dialog", { name: "AI 幫我安排" })).toBeTruthy();
    fireEvent.click(screen.getByRole("radio", { name: /\u55ae\u65e5\u5b89\u6392/ }));
    fireEvent.click(screen.getByRole("button", { name: "安排這一天" }));

    await waitFor(() => expect(generationBody).toEqual({
      version: 1,
      scope: "day",
      day_date: "2026-11-11",
    }));
    expect(await screen.findByText(/MiniMax 已完成.*並扣除 1 次/)).toBeTruthy();
    expect(screen.getByText("MiniMax 安排的淺草散步")).toBeTruthy();
    expect(screen.getByText("AI 建議")).toBeTruthy();
  });

  it("offers a full-trip AI arrangement from the same menu", async () => {
    let generationBody: Record<string, unknown> | undefined;
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.includes("/itinerary/generate")) {
        generationBody = JSON.parse(String(init?.body));
        return response({
          ...trip,
          version: 2,
          planning: {
            status: "live",
            provider: "minimax",
            model: "MiniMax-M2.1",
            generated_at: "2026-11-01T10:00:00Z",
            warnings: [],
            scope: "trip",
            day_date: null,
          },
          usage: { status: "charged", uses: 1, reference: "ai-trip-1" },
        });
      }
      return response(trip);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<TripEditor tripId={trip.id} />);

    const aiButtons = await screen.findAllByRole("button", { name: "AI 幫我安排" });
    fireEvent.click(aiButtons[0]);
    const fullTrip = screen.getByRole("radio", { name: /\u5168\u884c\u7a0b\u5b89\u6392/ });
    expect(fullTrip.getAttribute("aria-checked")).toBe("true");
    fireEvent.click(screen.getByRole("button", { name: "安排全行程" }));

    await waitFor(() => expect(generationBody).toEqual({
      version: 1,
      scope: "trip",
      day_date: null,
    }));
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
    fireEvent.click(screen.getByRole("button", { name: "最佳化動線" }));
    resolveFirstSave?.(response({ ...trip, version: 2, items: putBodies[0].items }));

    await waitFor(() => expect(putBodies).toHaveLength(2));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/optimize/preview"))).toBe(true));
    expect(putBodies[1].version).toBe(2);
    expect(putBodies[1].items[0].title).toBe("最後一次修改");
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
    const aiButtons = await screen.findAllByRole("button", { name: "AI 幫我安排" });
    fireEvent.click(aiButtons[0]);
    fireEvent.click(screen.getByRole("button", { name: /只調整現有動線/ }));
    expect(await screen.findByRole("dialog", { name: "最佳化預覽" })).toBeTruthy();
    expect(screen.getByText("預計節省")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "套用並扣 1 次" }));
    expect(await screen.findByText(/結果尚未確認/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "套用並扣 1 次" }));
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
    const expand = screen.getByRole("button", { name: "全螢幕顯示路線面板" });
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
});
