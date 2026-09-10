import { afterEach, describe, expect, it, vi } from "vitest";
import { loadDiscoveryStatus } from "./discovery-status.server";

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

describe("loadDiscoveryStatus", () => {
  it("reports the switch and does not cache it", async () => {
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ enabled: true })));
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test/");

    expect(await loadDiscoveryStatus()).toEqual({ enabled: true });
    // A switch has to take effect when it is flipped, so this one stays no-store even though the
    // listings around it are cached.
    expect(fetch).toHaveBeenCalledWith(
      "http://api.test/api/v1/discovery/status",
      expect.objectContaining({ cache: "no-store", headers: { Accept: "application/json" } }),
    );
  });

  it("reports the switch when it is off", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ enabled: false }))));
    expect(await loadDiscoveryStatus()).toEqual({ enabled: false });
  });

  // Falling back to "off" is what keeps app/[locale]/page.test.tsx passing: that test stubs
  // fetch to answer 401 for everything, and the home page must still render its marketing body.
  it.each([
    ["a transport failure", vi.fn().mockRejectedValue(new Error("offline"))],
    ["an unauthorized answer", vi.fn().mockResolvedValue(new Response("no", { status: 401 }))],
    ["a server error", vi.fn().mockResolvedValue(new Response("no", { status: 503 }))],
    ["a payload with no flag", vi.fn().mockResolvedValue(new Response(JSON.stringify({})))],
    ["a non-boolean flag", vi.fn().mockResolvedValue(new Response(JSON.stringify({ enabled: "yes" })))],
    ["a null payload", vi.fn().mockResolvedValue(new Response("null"))],
  ])("falls back to off on %s", async (_label, fetch) => {
    vi.stubGlobal("fetch", fetch);
    expect(await loadDiscoveryStatus()).toEqual({ enabled: false });
  });
});
