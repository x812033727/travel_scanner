import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const guideId = "11111111-1111-1111-1111-111111111111";
const params = Promise.resolve({ locale: "zh-TW", guideId });

function request(headers: Record<string, string>) {
  return new NextRequest(`https://mokaair.com/zh-TW/out/guides/${guideId}`, { headers });
}

function upstream(url: unknown) {
  return vi.fn(async () => new Response(JSON.stringify({ url })));
}

describe("hotspot guide redirect", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards only the session token and the right-most proxy address", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe("Bearer member-token");
      expect(headers.has("cookie")).toBe(false);
      expect(headers.get("x-travel-client-ip")).toBe("198.51.100.8");
      expect(init?.method).toBe("POST");
      return new Response(JSON.stringify({ url: "https://example.com/guide" }));
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(
      request({
        cookie: "travel_locale=ja; travel_access=member-token; _ga=GA1.1.tracking",
        "x-forwarded-for": "192.0.2.1, 198.51.100.8",
      }),
      { params },
    );

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe("https://example.com/guide");
  });

  it("refuses to redirect to non-HTTPS, credentialed, or malformed upstream URLs", async () => {
    for (const url of ["http://example.com/guide", "https://user:secret@example.com/", "not a url", 42]) {
      vi.stubGlobal("fetch", upstream(url));
      const response = await GET(request({ cookie: "travel_access=member-token" }), { params });
      expect(response.status).toBe(502);
      expect((await response.json()).code).toBe("unsafe_upstream_redirect");
    }
  });

  it("rejects malformed identifiers before contacting the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(
      new NextRequest("https://mokaair.com/zh-TW/out/guides/../ready"),
      { params: Promise.resolve({ locale: "zh-TW", guideId: "../ready" }) },
    );
    expect(response.status).toBe(404);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
