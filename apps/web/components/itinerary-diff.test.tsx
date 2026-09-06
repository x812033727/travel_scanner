import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { Trip } from "@/lib/trip-types";
import { ItineraryDiff, type IntentPreview } from "./itinerary-diff";

vi.mock("@/components/usage-catalog-provider", () => ({
  useOperationCharge: (operation: string) =>
    operation === "ai_itinerary_refine"
      ? { status: "ready", uses: 0, label: "免費", unavailableHelp: "" }
      : { status: "ready", uses: 1, label: "1 次", unavailableHelp: "" },
}));

const trip: Trip = {
  id: "t1",
  name: "東京五日",
  mode: "manual",
  total_price: 0,
  currency: "TWD",
  data: {},
  version: 7,
  start_date: "2026-11-10",
  end_date: "2026-11-14",
  timezone: "Asia/Tokyo",
  items: [],
  route_segments: [],
};

function preview(overrides: Partial<IntentPreview> = {}): IntentPreview {
  return {
    preview_id: "p1",
    base_version: 7,
    expires_at: "2026-11-01T00:15:00Z",
    scope: "day",
    day_date: "2026-11-12",
    planning: {
      status: "live",
      readiness: "ready",
      provider: "openai",
      generated_at: "2026-11-01T00:00:00Z",
      warnings: [],
    },
    intent: { text: "這天下雨，改室內" },
    usage_operation: "ai_itinerary_refine",
    diff: {
      changed: [],
      removed: [
        {
          candidate_key: "hotspot:0",
          title: "戶外庭園",
          day_date: "2026-11-12",
          start_time: "10:00",
          reason: "原本的推薦理由",
        },
      ],
      added: [
        {
          candidate_key: "hotspot:9",
          title: "東京國立博物館",
          day_date: "2026-11-12",
          start_time: "10:00",
          reason: "室內展館，雨天也能安排",
        },
      ],
      moved: [
        {
          candidate_key: "hotspot:3",
          title: "淺草寺",
          from: { day_date: "2026-11-12", start_time: "13:30" },
          to: { day_date: "2026-11-12", start_time: "17:00" },
          reason: "配合新的順序",
        },
      ],
      meals: [
        {
          system_role: "lunch",
          day_date: "2026-11-12",
          before_title: "午餐尚未安排",
          after_title: "淺草老舖",
          cleared: false,
        },
      ],
      unchanged_count: 1,
      has_changes: true,
      ...(overrides.diff || {}),
    },
    exhaustion: {
      exhausted: false,
      reason: null,
      alternative_candidate_count: 5,
      alternative_merchant_count: 3,
      pool_spent: false,
      meal_pool_spent: false,
      activity_delta: 0,
      fewer_stops_without_alternatives: false,
      ...(overrides.exhaustion || {}),
    },
    ...overrides,
  } as IntentPreview;
}

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

function calls(fetchMock: ReturnType<typeof vi.fn>) {
  return fetchMock.mock.calls as unknown as Array<[string, RequestInit]>;
}

afterEach(() => vi.unstubAllGlobals());

function sheetFooter() {
  const footer = document.querySelector(".planner-sheet-footer");
  if (!footer) throw new Error("the diff sheet is not open");
  return within(footer as HTMLElement);
}

function applyButton() {
  return sheetFooter().getByRole("button", { name: /^套用/ });
}

async function submit(intent: string) {
  fireEvent.change(screen.getByLabelText("想改什麼？"), { target: { value: intent } });
  fireEvent.click(screen.getByRole("button", { name: /看看會怎麼改/ }));
}

describe("intent bar", () => {
  it("sends the sentence, the day and the current version, then shows the diff without writing", async () => {
    const fetchMock = vi.fn(async () => ok(preview()));
    vi.stubGlobal("fetch", fetchMock);
    const onApplied = vi.fn();
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={onApplied} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(screen.getByText("確認這次調整")).toBeTruthy());
    const [url, init] = calls(fetchMock)[0];
    expect(url).toBe("/api/travel/trips/t1/intents");
    expect(init.method).toBe("POST");
    expect(JSON.parse(String(init.body))).toEqual({
      version: 7,
      text: "這天下雨，改室內",
      scope: "day",
      day_date: "2026-11-12",
    });
    // Only the preview call ran; nothing was applied.
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(onApplied).not.toHaveBeenCalled();
  });

  it("renders removed, added, moved and meal groups with the planner's reasons", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok(preview())));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(screen.getByText("移除（1）")).toBeTruthy());
    expect(screen.getByText("新增（1）")).toBeTruthy();
    expect(screen.getByText("移動（1）")).toBeTruthy();
    expect(screen.getByText("餐食（1）")).toBeTruthy();
    expect(screen.getByText("東京國立博物館")).toBeTruthy();
    expect(screen.getByText("室內展館，雨天也能安排")).toBeTruthy();
    expect(screen.getByText("午餐尚未安排 → 淺草老舖")).toBeTruthy();
    expect(screen.getByText("你的要求：這天下雨，改室內")).toBeTruthy();
    expect(screen.getByText("有 1 個安排維持不變。")).toBeTruthy();
  });

  it("applies through the existing apply endpoint with the envelope's base version", async () => {
    const applied: Trip = { ...trip, version: 8 };
    const fetchMock = vi.fn(async (url: string) =>
      url.endsWith("/intents") ? ok(preview()) : ok(applied),
    );
    vi.stubGlobal("fetch", fetchMock);
    const onApplied = vi.fn();
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={onApplied} />);

    await submit("這天下雨，改室內");
    await waitFor(() => expect(applyButton()).toBeTruthy());
    fireEvent.click(applyButton());

    await waitFor(() => expect(onApplied).toHaveBeenCalled());
    const [url, init] = calls(fetchMock)[1];
    expect(url).toBe("/api/travel/trips/t1/itinerary/apply");
    expect(JSON.parse(String(init.body))).toEqual({ version: 7, preview_id: "p1" });
    expect(onApplied.mock.calls[0]).toEqual([applied, "day", "2026-11-12"]);
  });

  it("mints a new idempotency key per sentence so a second ask is not a replay", async () => {
    const fetchMock = vi.fn(async () => ok(preview()));
    vi.stubGlobal("fetch", fetchMock);
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");
    await waitFor(() => expect(screen.getByText("確認這次調整")).toBeTruthy());
    fireEvent.click(sheetFooter().getByRole("button", { name: "先不套用" }));
    await submit("走路少一點");
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));

    const keys = calls(fetchMock).map(([, init]) => (init.headers as Record<string, string>)["Idempotency-Key"]);
    expect(keys[0]).toBeTruthy();
    expect(keys[0]).not.toBe(keys[1]);
  });

  it("states the area is exhausted and offers no apply when nothing can change", async () => {
    vi.stubGlobal("fetch", vi.fn(async () =>
      ok(
        preview({
          diff: { removed: [], added: [], moved: [], meals: [], unchanged_count: 2, has_changes: false },
          exhaustion: {
            exhausted: true,
            reason: "no_alternatives",
            alternative_candidate_count: 0,
            activity_delta: 0,
            fewer_stops_without_alternatives: false,
          },
        }),
      ),
    ));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("再換一個景點");

    await waitFor(() => expect(screen.getByText("這區已經沒有其他選擇了")).toBeTruthy());
    expect(sheetFooter().queryByRole("button", { name: /^套用/ })).toBeNull();
    expect(sheetFooter().getByRole("button", { name: "關閉" })).toBeTruthy();
  });

  it("separates an unchanged plan from a spent candidate pool", async () => {
    vi.stubGlobal("fetch", vi.fn(async () =>
      ok(
        preview({
          diff: { removed: [], added: [], moved: [], meals: [], unchanged_count: 2, has_changes: false },
          exhaustion: {
            exhausted: true,
            reason: "no_change",
            alternative_candidate_count: 6,
            activity_delta: 0,
            fewer_stops_without_alternatives: false,
          },
        }),
      ),
    ));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("再換一個景點");

    await waitFor(() =>
      expect(screen.getByText(/目前的安排已經是這樣了/)).toBeTruthy(),
    );
  });

  it("warns when the day loses a stop and nothing verified is left to replace it", async () => {
    vi.stubGlobal("fetch", vi.fn(async () =>
      ok(
        preview({
          diff: {
            removed: [
              { candidate_key: "hotspot:0", title: "戶外庭園", day_date: "2026-11-12", start_time: "10:00" },
            ],
            added: [],
            moved: [],
            meals: [],
            unchanged_count: 1,
            has_changes: true,
          },
          exhaustion: {
            exhausted: false,
            reason: null,
            alternative_candidate_count: 0,
            activity_delta: -1,
            fewer_stops_without_alternatives: true,
          },
        }),
      ),
    ));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(screen.getByText(/這天會少 1 個安排/)).toBeTruthy());
  });

  it("falls back to whole-trip scope when no day is selected", async () => {
    const fetchMock = vi.fn(async () => ok(preview({ scope: "trip", day_date: null })));
    vi.stubGlobal("fetch", fetchMock);
    render(<ItineraryDiff trip={trip} onApplied={vi.fn()} />);

    await submit("走路少一點");

    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    expect(JSON.parse(String(calls(fetchMock)[0][1].body))).toMatchObject({
      scope: "trip",
      day_date: null,
    });
  });

  it("reports an apply failure and closes the review rather than offering a stale retry", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      if (url.endsWith("/intents")) return ok(preview());
      return {
        ok: false,
        status: 409,
        json: async () => ({ code: "trip_version_conflict", detail: "旅程已更新，請重新預覽後再套用" }),
      };
    });
    vi.stubGlobal("fetch", fetchMock);
    const onError = vi.fn();
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} onError={onError} />);

    await submit("這天下雨，改室內");
    await waitFor(() => expect(applyButton()).toBeTruthy());
    fireEvent.click(applyButton());

    await waitFor(() => expect(onError).toHaveBeenCalledWith("旅程已更新，請重新預覽後再套用"));
    expect(screen.queryByText("確認這次調整")).toBeNull();
  });

  it("flushes pending edits before asking, and stops when the flush hits a conflict", async () => {
    const fetchMock = vi.fn(async () => ok(preview()));
    vi.stubGlobal("fetch", fetchMock);
    const prepare = vi.fn(async () => undefined);
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" prepare={prepare} onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(prepare).toHaveBeenCalled());
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("reuses the key when the same failed ask is retried, so it replays instead of re-billing", async () => {
    let attempt = 0;
    const fetchMock = vi.fn(async () => {
      attempt += 1;
      if (attempt === 1) return { ok: false, status: 504, json: async () => ({ code: "upstream_timeout", detail: "逾時" }) };
      return ok(preview());
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} onError={vi.fn()} />);

    await submit("這天下雨，改室內");
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    fireEvent.click(screen.getByRole("button", { name: /看看會怎麼改/ }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));

    const keys = calls(fetchMock).map(([, init]) => (init.headers as Record<string, string>)["Idempotency-Key"]);
    expect(keys[0]).toBe(keys[1]);
  });

  it("says plainly when the plan came from the catalog, and refuses to apply it", async () => {
    vi.stubGlobal("fetch", vi.fn(async () =>
      ok(
        preview({
          planning: {
            status: "fallback",
            readiness: "fallback",
            provider: "catalog",
            generated_at: "2026-11-01T00:00:00Z",
            warnings: [],
          },
        }),
      ),
    ));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(screen.getByText(/AI 規劃器暫時無法使用/)).toBeTruthy());
    expect(sheetFooter().queryByRole("button", { name: /^套用/ })).toBeNull();
  });

  it("names the fields a re-plan would overwrite instead of calling the row unchanged", async () => {
    vi.stubGlobal("fetch", vi.fn(async () =>
      ok(
        preview({
          diff: {
            removed: [],
            added: [],
            moved: [],
            changed: [
              {
                candidate_key: "hotspot:0",
                title: "淺草寺",
                day_date: "2026-11-12",
                start_time: "10:00",
                fields: ["place", "notes"],
              },
            ],
            meals: [],
            unchanged_count: 0,
            has_changes: true,
          },
        }),
      ),
    ));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(screen.getByText("同時更新（1）")).toBeTruthy());
    expect(screen.getByText("會被覆蓋：地點、你的備註")).toBeTruthy();
  });

  it("reports a spent pool even when the re-plan only reordered the same stops", async () => {
    vi.stubGlobal("fetch", vi.fn(async () =>
      ok(
        preview({
          exhaustion: {
            exhausted: false,
            reason: null,
            alternative_candidate_count: 0,
            alternative_merchant_count: 0,
            pool_spent: true,
            meal_pool_spent: true,
            activity_delta: 0,
            fewer_stops_without_alternatives: false,
          },
        }),
      ),
    ));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("換別的地方");

    await waitFor(() => expect(screen.getByText(/這一帶已驗證的地點都已經在你的行程裡了/)).toBeTruthy());
    expect(screen.getByText(/沒有其他已驗證的餐廳/)).toBeTruthy();
  });

  it("prices a whole-trip intent as a generation rather than a free refinement", async () => {
    const fetchMock = vi.fn(async () =>
      ok(preview({ scope: "trip", day_date: null, usage_operation: "ai_itinerary_generation" })),
    );
    vi.stubGlobal("fetch", fetchMock);
    render(<ItineraryDiff trip={trip} onApplied={vi.fn()} />);

    await submit("走路少一點");

    await waitFor(() => expect(applyButton()).toBeTruthy());
    expect(applyButton().textContent).toContain("1 次");
  });

  it("keeps a day-scoped refinement free", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok(preview())));
    render(<ItineraryDiff trip={trip} activeDay="2026-11-12" onApplied={vi.fn()} />);

    await submit("這天下雨，改室內");

    await waitFor(() => expect(applyButton()).toBeTruthy());
    expect(applyButton().textContent).toContain("免費");
  });
});
