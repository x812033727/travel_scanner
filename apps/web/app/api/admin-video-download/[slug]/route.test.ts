import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";

const jar = new Map<string, string>();
vi.mock("next/headers", () => ({ cookies: async () => ({ get: (name: string) => (jar.has(name) ? { value: jar.get(name) } : undefined) }) }));

const { GET } = await import("./route");
const context = (slug: string) => ({ params: Promise.resolve({ slug }) });

describe("admin compilation download", () => {
  afterEach(() => { vi.unstubAllGlobals(); jar.clear(); });

  it("streams a byte range with the admin session, keeps the file name, and never caches it", async () => {
    jar.set("travel_access", "session-token");
    jar.set("admin_step_up", "step");
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe("http://localhost:8000/api/v1/admin/videos/wenjian-full/download");
      const headers = new Headers(init?.headers);
      expect(headers.get("cookie")).toBe("travel_access=session-token; admin_step_up=step");
      expect(headers.get("range")).toBe("bytes=0-3");
      return new Response(new Uint8Array([9, 8, 7, 6]), {
        status: 206,
        headers: {
          "Content-Type": "video/mp4", "Content-Range": "bytes 0-3/100", "Content-Length": "4", "Accept-Ranges": "bytes",
          "Content-Disposition": 'attachment; filename="wenjian-full.mp4"', "Set-Cookie": "x=1",
        },
      });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest("https://mokaair.com/api/admin-video-download/wenjian-full", { headers: { Range: "bytes=0-3" } }), context("wenjian-full"));
    expect(response.status).toBe(206);
    expect(new Uint8Array(await response.arrayBuffer())).toEqual(new Uint8Array([9, 8, 7, 6]));
    expect(response.headers.get("content-range")).toBe("bytes 0-3/100");
    expect(response.headers.get("content-disposition")).toBe('attachment; filename="wenjian-full.mp4"');
    expect(response.headers.get("cache-control")).toBe("private, no-store");
    expect(response.headers.get("set-cookie")).toBeNull();
  });

  it("passes the API's refusal back without its body", async () => {
    jar.set("travel_access", "session-token");
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ detail: "not there yet" }, { status: 404 })));
    const response = await GET(new NextRequest("https://mokaair.com/api/admin-video-download/wenjian-full"), context("wenjian-full"));
    expect(response.status).toBe(404);
    expect((await response.json()).code).toBe("video_download_unavailable");
  });

  it("asks for a session and refuses odd names before calling the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const anonymous = await GET(new NextRequest("https://mokaair.com/api/admin-video-download/v"), context("v"));
    jar.set("travel_access", "session-token");
    const traversal = await GET(new NextRequest("https://mokaair.com/api/admin-video-download/x"), context(".."));
    expect([anonymous.status, traversal.status]).toEqual([401, 404]);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
