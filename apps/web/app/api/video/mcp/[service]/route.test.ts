import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET, POST } from "./route";

const TOKEN = `mkv_${"f".repeat(44)}`;

describe("/api/video/mcp/[service] BFF proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("rejects unknown service names with 404 before touching upstream", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const req = new NextRequest("https://mokaair.com/api/video/mcp/other", {
      method: "POST",
      headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "ping" }),
    });
    const res = await POST(req, { params: Promise.resolve({ service: "other" }) });
    expect(res.status).toBe(404);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("forwards flow and flow-music JSON-RPC POSTs with Bearer mkv_ token and no-store", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toContain("/api/v1/video/mcp/flow-music");
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.get("cookie")).toBeNull();
      return new Response(JSON.stringify({ jsonrpc: "2.0", id: 1, result: {} }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    const req = new NextRequest("https://mokaair.com/api/video/mcp/flow-music", {
      method: "POST",
      headers: { Authorization: `Bearer ${TOKEN}`, Cookie: "session=secret", "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "ping" }),
    });
    const res = await POST(req, { params: Promise.resolve({ service: "flow-music" }) });
    expect(res.status).toBe(200);
    expect(res.headers.get("cache-control")).toBe("no-store");
    expect(await res.json()).toEqual({ jsonrpc: "2.0", id: 1, result: {} });
  });

  it("forwards GET /api/video/mcp/health and rejects other GET services", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url: string) => {
        expect(url).toContain("/api/v1/video/mcp/health");
        return new Response(JSON.stringify({ ok: true, enabled: true, reachable: true }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        });
      }),
    );

    const bad = await GET(
      new NextRequest("https://mokaair.com/api/video/mcp/flow", { headers: { Authorization: `Bearer ${TOKEN}` } }),
      { params: Promise.resolve({ service: "flow" }) },
    );
    expect(bad.status).toBe(404);

    const ok = await GET(
      new NextRequest("https://mokaair.com/api/video/mcp/health", { headers: { Authorization: `Bearer ${TOKEN}` } }),
      { params: Promise.resolve({ service: "health" }) },
    );
    expect(ok.status).toBe(200);
    expect(await ok.json()).toEqual({ ok: true, enabled: true, reachable: true });
  });
});
