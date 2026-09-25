import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;

describe("video automation settings proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the worker's token, never its cookies, and returns the settings", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toMatch(/\/api\/v1\/video\/automation\/settings$/);
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      return Response.json({ enabled: true, draft_interval_hours: 72 });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest("https://mokaair.com/api/video/automation/settings", {
      headers: { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" },
    }));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ enabled: true, draft_interval_hours: 72 });
  });

  it("refuses a browser session without a video tool token", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest("https://mokaair.com/api/video/automation/settings", {
      headers: { Cookie: "travel_access=session" },
    }));
    expect(response.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
