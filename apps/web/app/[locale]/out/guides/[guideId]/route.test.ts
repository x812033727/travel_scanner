import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

describe("hotspot guide redirect", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the login cookie to the protected guide endpoint", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      expect(new Headers(init?.headers).get("cookie")).toBe("session=member");
      return new Response(JSON.stringify({ url: "https://example.com/guide" }));
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest("https://mokaair.com/zh-TW/out/guides/11111111-1111-1111-1111-111111111111", {
      headers: { cookie: "session=member" },
    });

    const response = await GET(request, { params: Promise.resolve({ locale: "zh-TW", guideId: "11111111-1111-1111-1111-111111111111" }) });

    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe("https://example.com/guide");
  });
});
