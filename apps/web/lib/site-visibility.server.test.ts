import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { loadSiteVisibility, resetSiteVisibilitySnapshot } from "./site-visibility.server";
import { closedSiteVisibility } from "./site-features";

const payload = {
  hotspots_enabled: true,
  trips_enabled: false,
  alerts_enabled: true,
  flight_status_enabled: false,
  airline_fares_enabled: true,
  pricing_enabled: false,
};

const ok = () => vi.fn().mockResolvedValue(new Response(JSON.stringify(payload), { status: 200 }));

// The snapshot is process state by design, so every case starts from a cold one.
beforeEach(() => resetSiteVisibilitySnapshot());
afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

describe("loadSiteVisibility", () => {
  it("loads the six public flags without caching", async () => {
    const fetchMock = ok();
    vi.stubGlobal("fetch", fetchMock);

    await expect(loadSiteVisibility()).resolves.toEqual({ status: "ready", features: payload });
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/runtime/site-visibility",
      expect.objectContaining({ cache: "no-store" }),
    );
  });

  it("fails closed when nothing has ever been read", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(loadSiteVisibility()).resolves.toEqual({
      status: "unavailable",
      features: closedSiteVisibility,
    });

    resetSiteVisibilitySnapshot();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ trips_enabled: true }), { status: 200 }),
    ));
    await expect(loadSiteVisibility()).resolves.toEqual({
      status: "unavailable",
      features: closedSiteVisibility,
    });
  });

  it("keeps the last answer the service gave when a later read fails", async () => {
    // The point of the whole snapshot: a 3 s timeout while Googlebot is reading used to put
    // `noindex` on four live pages and drop them from that request's sitemap.
    vi.stubGlobal("fetch", ok());
    await loadSiteVisibility();

    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("timeout")));
    await expect(loadSiteVisibility()).resolves.toEqual({ status: "stale", features: payload });
  });

  it("does not stand behind an answer older than the staleness limit", async () => {
    vi.stubGlobal("fetch", ok());
    await loadSiteVisibility();

    vi.useFakeTimers();
    vi.setSystemTime(Date.now() + 11 * 60 * 1000);
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("still down")));
    await expect(loadSiteVisibility()).resolves.toEqual({
      status: "unavailable",
      features: closedSiteVisibility,
    });
  });

  it("lets a successful read replace a remembered one immediately", async () => {
    // Closing a feature in the admin console must still take effect at once.
    vi.stubGlobal("fetch", ok());
    await loadSiteVisibility();

    const closed = { ...payload, hotspots_enabled: false };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify(closed), { status: 200 }),
    ));
    await expect(loadSiteVisibility()).resolves.toEqual({ status: "ready", features: closed });

    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("down")));
    await expect(loadSiteVisibility()).resolves.toEqual({ status: "stale", features: closed });
  });
});
