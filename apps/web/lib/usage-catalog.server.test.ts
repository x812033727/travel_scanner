import { afterEach, describe, expect, it, vi } from "vitest";
import { usageOperations } from "./usage-catalog";
import { loadSharedUsageCatalog, loadUsageCatalog, resetUsageCatalogCache } from "./usage-catalog.server";

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
  resetUsageCatalogCache();
});

function catalogResponse(trialUses: number) {
  const payload = {
    trial_uses: trialUses,
    packages: [],
    operation_costs: Object.fromEntries(usageOperations.map((operation) => [operation, 1])),
  };
  return new Response(JSON.stringify(payload), { status: 200 });
}

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

describe("loadSharedUsageCatalog", () => {
  it("asks the API once per locale until the entry expires", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(catalogResponse(3)));
    vi.stubGlobal("fetch", fetchMock);

    await Promise.all([loadSharedUsageCatalog("en"), loadSharedUsageCatalog("en")]);
    await loadSharedUsageCatalog("en");
    expect(fetchMock).toHaveBeenCalledTimes(1);

    await loadSharedUsageCatalog("ja");
    expect(fetchMock).toHaveBeenCalledTimes(2);

    vi.advanceTimersByTime(31_000);
    await loadSharedUsageCatalog("en");
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it("keeps serving the last good catalog while the API fails, and backs off", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn().mockImplementation(() => Promise.resolve(catalogResponse(4)));
    vi.stubGlobal("fetch", fetchMock);
    await loadSharedUsageCatalog("en");

    vi.advanceTimersByTime(31_000);
    fetchMock.mockImplementation(() => Promise.resolve(new Response("{}", { status: 500 })));
    const stale = await loadSharedUsageCatalog("en");
    expect(stale.status).toBe("ready");
    expect(stale.catalog?.trial_uses).toBe(4);

    await loadSharedUsageCatalog("en");
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
