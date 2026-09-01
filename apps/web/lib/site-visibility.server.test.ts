import { afterEach, describe, expect, it, vi } from "vitest";

import { loadSiteVisibility } from "./site-visibility.server";
import { closedSiteVisibility } from "./site-features";

afterEach(() => vi.unstubAllGlobals());

describe("loadSiteVisibility", () => {
  it("loads the six public flags without caching", async () => {
    const payload = {
      hotspots_enabled: true,
      trips_enabled: false,
      alerts_enabled: true,
      flight_status_enabled: false,
      airline_fares_enabled: true,
      pricing_enabled: false,
    };
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(payload), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    await expect(loadSiteVisibility()).resolves.toEqual({ status: "ready", features: payload });
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/runtime/site-visibility",
      expect.objectContaining({ cache: "no-store" }),
    );
  });

  it("fails closed when the service errors or returns an invalid payload", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(loadSiteVisibility()).resolves.toEqual({
      status: "unavailable",
      features: closedSiteVisibility,
    });

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ trips_enabled: true }), { status: 200 }),
    ));
    await expect(loadSiteVisibility()).resolves.toEqual({
      status: "unavailable",
      features: closedSiteVisibility,
    });
  });
});
