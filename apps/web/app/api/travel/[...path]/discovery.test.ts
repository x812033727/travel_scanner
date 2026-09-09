import { afterEach, describe, expect, it, vi } from "vitest";
import { NextRequest } from "next/server";
import { GET, PUT, POST } from "./route";

vi.mock("next/headers", () => ({ cookies: async () => new Map() }));
afterEach(() => vi.unstubAllGlobals());

describe("discovery BFF boundary", () => {
  it("allows anonymous curated search and preserves its locale and filters without caching", async () => {
    const fetcher = vi.fn(async () => new Response(JSON.stringify({ items: [], next_cursor: null }), { headers: { "Content-Type": "application/json" } }));
    vi.stubGlobal("fetch", fetcher);
    const response = await GET(new NextRequest("https://mokaair.test/api/travel/discovery/search?q=Kyoto&type=video", { headers: { "X-Travel-Locale": "zh-TW" } }), { params: Promise.resolve({ path: ["discovery", "search"] }) });
    expect(response.status).toBe(200);
    expect(response.headers.get("cache-control")).toContain("no-store");
    const [url, options] = (fetcher.mock.calls as unknown as [string, RequestInit][])[0];
    expect(url).toContain("/api/v1/discovery/search?q=Kyoto&type=video");
    expect(new Headers(options.headers).get("X-Travel-Locale")).toBe("zh-TW");
    expect(new Headers(options.headers).has("Authorization")).toBe(false);
  });

  it.each(["preferences", "dismiss"])("rejects cross-site %s changes before upstream access", async (endpoint) => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    const method = endpoint === "preferences" ? "PUT" : "POST";
    const response = await (method === "PUT" ? PUT : POST)(new NextRequest(`https://mokaair.test/api/travel/discovery/${endpoint}`, { method, headers: { Origin: "https://foreign.test", "Content-Type": "application/json" }, body: "{}" }), { params: Promise.resolve({ path: ["discovery", endpoint] }) });
    expect(response.status).toBe(403);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it.each([401, 403, 409, 503])("preserves API status %s for private actions and paused discovery", async (status) => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ code: "discovery_unavailable", status }), { status, headers: { "Content-Type": "application/json" } })));
    const response = await PUT(new NextRequest("https://mokaair.test/api/travel/discovery/preferences", { method: "PUT", headers: { Origin: "https://mokaair.test", "Content-Type": "application/json" }, body: JSON.stringify({ version: 1, destinations: ["tyo"] }) }), { params: Promise.resolve({ path: ["discovery", "preferences"] }) });
    expect(response.status).toBe(status);
    expect(response.headers.get("cache-control")).toContain("no-store");
  });
});
