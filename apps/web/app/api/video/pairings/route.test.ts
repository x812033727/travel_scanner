import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as poll } from "./poll/route";
import { POST as start } from "./route";

describe("video tool pairing proxy", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
  });

  it("forwards the body and the caller's address, never cookies or authorization", async () => {
    vi.stubEnv("INTERNAL_PROXY_TOKEN", "proxy-secret");
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toMatch(/\/api\/v1\/video\/pairings$/);
      const headers = new Headers(init?.headers);
      expect(headers.has("cookie")).toBe(false);
      expect(headers.has("authorization")).toBe(false);
      expect(headers.get("x-travel-client-ip")).toBe("203.0.113.9");
      expect(headers.get("x-travel-proxy-token")).toBe("proxy-secret");
      expect(new TextDecoder().decode(init?.body as ArrayBuffer)).toBe('{"client_name":"laptop"}');
      return new Response('{"user_code":"BCDF-GHJK"}', { status: 201, headers: { "Content-Type": "application/json", "Set-Cookie": "x=1" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await start(
      new NextRequest("https://mokaair.com/api/video/pairings", {
        method: "POST",
        headers: {
          Cookie: "travel_access=session",
          Authorization: "Bearer mkv_whatever",
          "X-Forwarded-For": "198.51.100.1, 203.0.113.9",
        },
        body: '{"client_name":"laptop"}',
      }),
    );
    expect(response.status).toBe(201);
    expect(await response.json()).toEqual({ user_code: "BCDF-GHJK" });
    expect(response.headers.get("set-cookie")).toBeNull();
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(fetchMock).toHaveBeenCalledOnce();
  });

  it("returns the collecting poll uncached", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url: string) => {
        expect(url).toMatch(/\/api\/v1\/video\/pairings\/poll$/);
        return new Response('{"status":"approved","token":"mkv_x"}', { status: 200, headers: { "Content-Type": "application/json" } });
      }),
    );
    const response = await poll(new NextRequest("https://mokaair.com/api/video/pairings/poll", { method: "POST", body: '{"device_code":"d"}' }));
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect((await response.json()).status).toBe("approved");
  });

  it("refuses an oversized body before forwarding and reports an unreachable API", async () => {
    const fetchMock = vi.fn(async () => {
      throw new Error("down");
    });
    vi.stubGlobal("fetch", fetchMock);
    const big = await start(new NextRequest("https://mokaair.com/api/video/pairings", { method: "POST", body: "x".repeat(5000) }));
    expect(big.status).toBe(413);
    expect(fetchMock).not.toHaveBeenCalled();
    const down = await poll(new NextRequest("https://mokaair.com/api/video/pairings/poll", { method: "POST", body: "{}" }));
    expect(down.status).toBe(502);
  });
});
