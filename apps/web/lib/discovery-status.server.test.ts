import { afterEach, describe, expect, it, vi } from "vitest";
import { loadDiscoveryStatus } from "./discovery-status.server";

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

describe("loadDiscoveryStatus", () => {
  it("reports the switch and does not cache it", async () => {
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ enabled: true })));
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test/");

    expect(await loadDiscoveryStatus()).toEqual({ enabled: true });
    // Switches stay fresh and never delay the marketing fallback indefinitely.
    expect(fetch).toHaveBeenCalledWith(
      "http://api.test/api/v1/discovery/status",
      expect.objectContaining({ cache: "no-store", headers: { Accept: "application/json" }, signal: expect.any(AbortSignal) }),
    );
  });

  it("reports the switch when it is off", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ enabled: false }))));
    expect(await loadDiscoveryStatus()).toEqual({ enabled: false });
  });

  it("bounds a hung status request and recovers to the marketing snapshot", async () => {
    const controller = new AbortController();
    const timeout = vi.spyOn(AbortSignal, "timeout").mockReturnValue(controller.signal);
    vi.stubGlobal("fetch", vi.fn((_url, options: RequestInit) => new Promise((_resolve, reject) => {
      options.signal?.addEventListener("abort", () => reject(new Error("timed out")), { once: true });
    })));
    try {
      const result = loadDiscoveryStatus();
      expect(timeout).toHaveBeenCalledWith(3_000);
      controller.abort();
      expect(await result).toEqual({ enabled: false });
    } finally {
      timeout.mockRestore();
    }
  });

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
