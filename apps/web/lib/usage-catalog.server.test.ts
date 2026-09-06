import { afterEach, describe, expect, it, vi } from "vitest";
import { usageOperations } from "./usage-catalog";
import { loadUsageCatalog } from "./usage-catalog.server";

afterEach(() => vi.unstubAllGlobals());

describe("loadUsageCatalog", () => {
  it("loads the localized public catalog without caching", async () => {
    const payload = {
      trial_uses: 6,
      packages: [],
      operation_costs: Object.fromEntries(usageOperations.map((operation) => [operation, 1])),
    };
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(payload), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    await expect(loadUsageCatalog("ja")).resolves.toEqual({ status: "ready", catalog: payload });
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/usage-catalog?locale=ja",
      expect.objectContaining({ cache: "no-store" }),
    );
  });

  it("prices an operation the API does not know at the default cost and says so", async () => {
    const older: Record<string, number> = Object.fromEntries(
      usageOperations.map((operation) => [operation, 2]),
    );
    delete older.ai_itinerary_refine;
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ trial_uses: 3, packages: [], operation_costs: older }), { status: 200 }),
    ));
    const warn = vi.spyOn(console, "warn").mockImplementation(() => {});

    const state = await loadUsageCatalog("en");

    expect(state.status).toBe("ready");
    expect(state.catalog?.operation_costs.ai_itinerary_refine).toBe(1);
    expect(state.catalog?.operation_costs.travel_search).toBe(2);
    expect(warn).toHaveBeenCalledTimes(1);
    expect(String(warn.mock.calls[0][0])).toContain("ai_itinerary_refine");
    warn.mockRestore();
  });

  it("fails closed on transport and schema errors", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(loadUsageCatalog("zh-TW")).resolves.toEqual({
      status: "unavailable",
      catalog: null,
    });

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ trial_uses: 3, packages: [] }), { status: 200 }),
    ));
    await expect(loadUsageCatalog("zh-TW")).resolves.toEqual({
      status: "unavailable",
      catalog: null,
    });
  });
});
