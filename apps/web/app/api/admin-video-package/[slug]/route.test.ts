import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";

const jar = new Map<string, string>();
vi.mock("next/headers", () => ({ cookies: async () => ({ get: (name: string) => (jar.has(name) ? { value: jar.get(name) } : undefined) }) }));

const { GET } = await import("./route");
const SHA = "c".repeat(64);
const context = (slug: string) => ({ params: Promise.resolve({ slug }) });

describe("admin video package zip stream", () => {
  afterEach(() => { vi.unstubAllGlobals(); jar.clear(); });

  it("streams the archive with the admin session, passing every entry through and never caching it", async () => {
    jar.set("travel_access", "session-token");
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe(`http://localhost:8000/api/v1/admin/videos/ai-model-choice/package.zip?file=${SHA}%3Afinal.mp4&file=${"d".repeat(64)}%3Athumbnail.en.jpg`);
      const headers = new Headers(init?.headers);
      expect(headers.get("cookie")).toBe("travel_access=session-token");
      return new Response(new Uint8Array([80, 75, 3, 4]), {
        status: 200,
        headers: { "Content-Type": "application/zip", "Content-Disposition": 'attachment; filename="ai-model-choice-upload.zip"', "Set-Cookie": "x=1" },
      });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest(`https://mokaair.com/api/admin-video-package/ai-model-choice?file=${SHA}:final.mp4&file=${"d".repeat(64)}:thumbnail.en.jpg`), context("ai-model-choice"));
    expect(response.status).toBe(200);
    expect(new Uint8Array(await response.arrayBuffer())).toEqual(new Uint8Array([80, 75, 3, 4]));
    expect(response.headers.get("content-disposition")).toContain("ai-model-choice-upload.zip");
    expect(response.headers.get("cache-control")).toBe("private, no-store");
    expect(response.headers.get("set-cookie")).toBeNull();
  });

  it("asks for a session and refuses odd names or entries before calling the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const anonymous = await GET(new NextRequest(`https://mokaair.com/api/admin-video-package/v?file=${SHA}:final.mp4`), context("v"));
    jar.set("travel_access", "session-token");
    const traversal = await GET(new NextRequest(`https://mokaair.com/api/admin-video-package/v?file=${SHA}:final.mp4`), context(".."));
    const empty = await GET(new NextRequest("https://mokaair.com/api/admin-video-package/v"), context("v"));
    const badName = await GET(new NextRequest(`https://mokaair.com/api/admin-video-package/v?file=${SHA}:../x.mp4`), context("v"));
    const badHash = await GET(new NextRequest("https://mokaair.com/api/admin-video-package/v?file=abc:final.mp4"), context("v"));
    expect([anonymous.status, traversal.status, empty.status, badName.status, badHash.status]).toEqual([401, 404, 422, 422, 422]);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("reports a refusal apart from a missing file", async () => {
    jar.set("travel_access", "session-token");
    vi.stubGlobal("fetch", vi.fn(async () => new Response("no", { status: 403 })));
    const refused = await GET(new NextRequest(`https://mokaair.com/api/admin-video-package/v?file=${SHA}:final.mp4`), context("v"));
    expect(refused.status).toBe(403);
    expect((await refused.json()).code).toBe("video_package_forbidden");
  });
});
