import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

describe("hotspot source redirect", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the login cookie and redirects only to a safe source", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      expect(new Headers(init?.headers).get("cookie")).toBe("session=member");
      return new Response(JSON.stringify({ url: "https://example.com/source" }));
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest("https://mocair.io/zh-TW/out/hotspots/11111111-1111-1111-1111-111111111111/source", {
      headers: { cookie: "session=member" },
    });

    const response = await GET(request, { params: Promise.resolve({ locale: "zh-TW", hotspotId: "11111111-1111-1111-1111-111111111111" }) });

    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe("https://example.com/source");
  });
});
