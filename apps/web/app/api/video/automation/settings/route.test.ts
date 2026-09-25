import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as run } from "../run/route";
import { GET as topics } from "../topics/route";
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

  it("sends a stage run and a topic lookup to their API routes with the token", async () => {
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      urls.push(url);
      expect(new Headers(init?.headers).get("authorization")).toBe(`Bearer ${TOKEN}`);
      return Response.json({ ok: true });
    }));
    const body = JSON.stringify({ stage: "writer", slug: "v", instructions: "Write.", payload: { pages: "x".repeat(1_000_000) } });
    const ran = await run(new NextRequest("https://mokaair.com/api/video/automation/run", {
      method: "POST", headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" }, body,
    }));
    const listed = await topics(new NextRequest("https://mokaair.com/api/video/automation/topics", {
      headers: { Authorization: `Bearer ${TOKEN}` },
    }));
    expect([ran.status, listed.status]).toEqual([200, 200]);
    expect(urls[0]).toMatch(/\/api\/v1\/video\/automation\/run$/);
    expect(urls[1]).toMatch(/\/api\/v1\/video\/automation\/topics$/);
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
