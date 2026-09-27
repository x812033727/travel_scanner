import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";

const jar = new Map<string, string>();
vi.mock("next/headers", () => ({ cookies: async () => ({ get: (name: string) => (jar.has(name) ? { value: jar.get(name) } : undefined) }) }));

const { GET } = await import("./route");
const SHA = "c".repeat(64);
const context = (slug: string, sha256: string) => ({ params: Promise.resolve({ slug, sha256 }) });

describe("admin video preview stream", () => {
  afterEach(() => { vi.unstubAllGlobals(); jar.clear(); });

  it("streams a byte range with the admin session and never caches it", async () => {
    jar.set("travel_access", "session-token");
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe(`http://localhost:8000/api/v1/admin/videos/ai-model-choice/files/${SHA}`);
      const headers = new Headers(init?.headers);
      expect(headers.get("cookie")).toBe("travel_access=session-token");
      expect(headers.get("range")).toBe("bytes=0-3");
      return new Response(new Uint8Array([9, 8, 7, 6]), {
        status: 206,
        headers: { "Content-Type": "video/mp4", "Content-Range": "bytes 0-3/100", "Content-Length": "4", "Accept-Ranges": "bytes", "Set-Cookie": "x=1" },
      });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest(`https://mokaair.com/api/admin-video-files/ai-model-choice/${SHA}`, { headers: { Range: "bytes=0-3" } }), context("ai-model-choice", SHA));
    expect(response.status).toBe(206);
    expect(new Uint8Array(await response.arrayBuffer())).toEqual(new Uint8Array([9, 8, 7, 6]));
    expect(response.headers.get("content-range")).toBe("bytes 0-3/100");
    expect(response.headers.get("cache-control")).toBe("private, no-store");
    expect(response.headers.get("set-cookie")).toBeNull();
  });

  it("asks for a session and refuses odd names before calling the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const anonymous = await GET(new NextRequest(`https://mokaair.com/api/admin-video-files/v/${SHA}`), context("v", SHA));
    jar.set("travel_access", "session-token");
    const traversal = await GET(new NextRequest("https://mokaair.com/api/admin-video-files/v/x"), context("..", "x"));
    expect([anonymous.status, traversal.status]).toEqual([401, 404]);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
