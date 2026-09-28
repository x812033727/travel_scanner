import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";

const jar = new Map<string, string>();
vi.mock("next/headers", () => ({ cookies: async () => ({ get: (name: string) => (jar.has(name) ? { value: jar.get(name) } : undefined) }) }));

const { GET } = await import("./route");
const ADDRESS = "https://mokaair.com/api/admin-video-shorts/batch";

describe("the batch of Shorts to upload", () => {
  afterEach(() => { vi.unstubAllGlobals(); jar.clear(); });

  it("streams the archive with the admin session, keeps the file name, and never caches it", async () => {
    jar.set("travel_access", "session-token");
    jar.set("admin_step_up", "step");
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe("http://localhost:8000/api/v1/admin/video-shorts/uploads/batch.zip");
      const headers = new Headers(init?.headers);
      expect(headers.get("cookie")).toBe("travel_access=session-token; admin_step_up=step");
      expect(init?.redirect).toBe("manual");
      return new Response(new Uint8Array([80, 75, 3, 4]), {
        status: 200,
        headers: { "Content-Type": "application/zip", "Content-Length": "4", "Content-Disposition": 'attachment; filename="mokaair-shorts.zip"', "Set-Cookie": "x=1" },
      });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest(ADDRESS));
    expect(response.status).toBe(200);
    expect(new Uint8Array(await response.arrayBuffer())).toEqual(new Uint8Array([80, 75, 3, 4]));
    expect(response.headers.get("content-type")).toBe("application/zip");
    expect(response.headers.get("content-disposition")).toBe('attachment; filename="mokaair-shorts.zip"');
    expect(response.headers.get("cache-control")).toBe("private, no-store");
    expect(response.headers.get("x-content-type-options")).toBe("nosniff");
    expect(response.headers.get("set-cookie")).toBeNull();
  });

  it("passes the API's refusal back by its kind and without its body", async () => {
    jar.set("travel_access", "session-token");
    const answers: Array<[number, string]> = [[404, "video_shorts_nothing_to_upload"], [403, "video_shorts_batch_forbidden"], [401, "video_shorts_batch_forbidden"], [500, "video_shorts_batch_unavailable"]];
    for (const [status, code] of answers) {
      vi.stubGlobal("fetch", vi.fn(async () => Response.json({ detail: "the API's own words" }, { status })));
      const response = await GET(new NextRequest(ADDRESS));
      expect(response.status).toBe(status);
      expect(await response.json()).toEqual({ status, code });
    }
  });

  it("asks for a session before calling the API, and says so when the API is away", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const anonymous = await GET(new NextRequest(ADDRESS));
    expect(anonymous.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
    jar.set("travel_access", "session-token");
    vi.stubGlobal("fetch", vi.fn(async () => { throw new Error("connect ECONNREFUSED"); }));
    const away = await GET(new NextRequest(ADDRESS));
    expect(away.status).toBe(502);
    expect((await away.json()).code).toBe("upstream_unavailable");
  });
});
