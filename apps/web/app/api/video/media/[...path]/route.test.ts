import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET, PART_MAX_BYTES, POST, PUT, mediaRoute } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const SHA = "b".repeat(64);
const JOB = "3f9a1c2e-1234-4abc-8def-0123456789ab";
const context = (...path: string[]) => ({ params: Promise.resolve({ path }) });
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };

describe("video media proxy for the pipeline", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("knows the media routes, their bodies and their deadlines", () => {
    expect(mediaRoute(["status"], "GET")?.kind).toBe("json");
    expect(mediaRoute(["images"], "POST")?.timeoutMs).toBe(90_000);
    expect(mediaRoute(["clips"], "POST")?.maxBytes).toBe(256 * 1024);
    expect(mediaRoute(["music"], "POST")?.kind).toBe("json");
    expect(mediaRoute(["judge"], "POST")?.timeoutMs).toBe(180_000);
    expect(mediaRoute(["jobs", JOB], "GET")?.timeoutMs).toBe(240_000);
    expect(mediaRoute(["files", "v", SHA], "PUT")?.maxBytes).toBe(PART_MAX_BYTES);
    expect(mediaRoute(["files", "v", SHA], "GET")?.kind).toBe("download");
    for (const [path, method] of [
      [["status"], "POST"],
      [["images"], "GET"],
      [["jobs", "not-a-uuid"], "GET"],
      [["jobs", JOB, "x"], "GET"],
      [["files", "Upper", SHA], "GET"],
      [["files", "v", "nothash"], "PUT"],
      [["files", "v", SHA], "POST"],
      [["other"], "GET"],
      [[], "GET"],
    ] as const) {
      expect(mediaRoute([...path], method)).toBeNull();
    }
  });

  it("forwards a submission as JSON with the token and no cookies, passing the status and Retry-After back", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe("http://localhost:8000/api/v1/video/media/clips");
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.get("content-type")).toBe("application/json");
      expect(headers.has("cookie")).toBe(false);
      expect(new TextDecoder().decode(init?.body as ArrayBuffer)).toBe('{"slug":"v"}');
      return new Response('{"code":"video_media_upstream_busy"}', { status: 429, headers: { "Content-Type": "application/json", "Retry-After": "30", "Set-Cookie": "x=1" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest("https://mokaair.com/api/video/media/clips", { method: "POST", headers: { ...auth, "Content-Type": "application/json" }, body: '{"slug":"v"}' });
    const response = await POST(request, context("clips"));
    expect(response.status).toBe(429);
    expect(response.headers.get("retry-after")).toBe("30");
    expect(response.headers.get("set-cookie")).toBeNull();
    expect(await response.json()).toEqual({ code: "video_media_upstream_busy" });
  });

  it("streams a download with its byte range and file headers", async () => {
    const bytes = new Uint8Array([0, 0, 0, 24, 0x66, 0x74, 0x79, 0x70]);
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe(`http://localhost:8000/api/v1/video/media/files/v/${SHA}`);
      const headers = new Headers(init?.headers);
      expect(headers.get("range")).toBe("bytes=0-7");
      expect(headers.get("accept")).toBe("*/*");
      return new Response(bytes, { status: 206, headers: { "Content-Type": "video/mp4", "Content-Range": "bytes 0-7/100", "Content-Length": "8", ETag: `"${SHA}"`, "Set-Cookie": "x=1" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest(`https://mokaair.com/api/video/media/files/v/${SHA}`, { headers: { ...auth, Range: "bytes=0-7" } });
    const response = await GET(request, context("files", "v", SHA));
    expect(response.status).toBe(206);
    expect(response.headers.get("content-range")).toBe("bytes 0-7/100");
    expect(response.headers.get("etag")).toBe(`"${SHA}"`);
    expect(response.headers.get("cache-control")).toBe("private, no-store");
    expect(response.headers.get("set-cookie")).toBeNull();
    expect(new Uint8Array(await response.arrayBuffer())).toEqual(bytes);
  });

  it("passes a download's error answer through as JSON", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "video_media_file_not_found" }, { status: 404 })));
    const response = await GET(new NextRequest(`https://mokaair.com/api/video/media/files/v/${SHA}`, { headers: auth }), context("files", "v", SHA));
    expect(response.status).toBe(404);
    expect(await response.json()).toEqual({ code: "video_media_file_not_found" });
  });

  it("forwards an upload part as bytes with its query", async () => {
    const part = new Uint8Array([1, 2, 3]);
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe(`http://localhost:8000/api/v1/video/media/files/v/${SHA}?part=0&parts=1&size=3`);
      expect(new Headers(init?.headers).get("content-type")).toBe("application/octet-stream");
      expect(new Uint8Array(init?.body as ArrayBuffer)).toEqual(part);
      return Response.json({ received: [0], complete: true });
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest(`https://mokaair.com/api/video/media/files/v/${SHA}?part=0&parts=1&size=3&extra=1`, { method: "PUT", headers: auth, body: part });
    const response = await PUT(request, context("files", "v", SHA));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ received: [0], complete: true });
  });

  it("refuses before forwarding: no token, an unknown route, a part without its query, a body too large", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const noToken = await GET(new NextRequest("https://mokaair.com/api/video/media/status"), context("status"));
    const unknown = await POST(new NextRequest("https://mokaair.com/api/video/media/other", { method: "POST", headers: auth, body: "{}" }), context("other"));
    const noQuery = await PUT(new NextRequest(`https://mokaair.com/api/video/media/files/v/${SHA}`, { method: "PUT", headers: auth, body: "x" }), context("files", "v", SHA));
    const tooBig = await PUT(new NextRequest(`https://mokaair.com/api/video/media/files/v/${SHA}?part=0&parts=2&size=9000000`, { method: "PUT", headers: auth, body: new Uint8Array(PART_MAX_BYTES + 1) }), context("files", "v", SHA));
    const bigJson = await POST(new NextRequest("https://mokaair.com/api/video/media/images", { method: "POST", headers: auth, body: "x".repeat(256 * 1024 + 1) }), context("images"));
    expect([noToken.status, unknown.status, noQuery.status, tooBig.status, bigJson.status]).toEqual([401, 404, 422, 413, 413]);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("answers 502 when the API cannot be reached", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => { throw new Error("ECONNREFUSED"); }));
    const response = await GET(new NextRequest(`https://mokaair.com/api/video/media/jobs/${JOB}`, { headers: auth }), context("jobs", JOB));
    expect(response.status).toBe(502);
    expect((await response.json()).code).toBe("upstream_unavailable");
  });
});
