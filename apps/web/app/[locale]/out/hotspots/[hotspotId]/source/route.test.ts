import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const hotspotId = "11111111-1111-1111-1111-111111111111";
const params = Promise.resolve({ locale: "zh-TW", hotspotId });

function request(headers: Record<string, string>) {
  return new NextRequest(`https://mokaair.com/zh-TW/out/hotspots/${hotspotId}/source`, { headers });
}

describe("hotspot source redirect", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards only the session token and redirects to a safe source", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe("Bearer member-token");
      expect(headers.has("cookie")).toBe(false);
      return new Response(JSON.stringify({ url: "https://example.com/source" }));
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(
      request({ cookie: "travel_access=member-token; travel_locale=zh-TW" }),
      { params },
    );

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe("https://example.com/source");
  });

  it("refuses to redirect to non-HTTPS, credentialed, or malformed upstream URLs", async () => {
    for (const url of ["http://example.com/source", "https://user:secret@example.com/", "javascript:alert(1)", "not a url"]) {
      vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ url }))));
      const response = await GET(request({ cookie: "travel_access=member-token" }), { params });
      expect(response.status).toBe(502);
      expect((await response.json()).code).toBe("unsafe_upstream_redirect");
    }
  });
});
