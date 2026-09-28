import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const BASE = "https://mokaair.com/api/video/automation/videos";
const list = (query = "") => GET(new NextRequest(`${BASE}${query}`, { headers: auth }));

describe("video list proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("asks as before when no filter is given", async () => {
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      urls.push(url);
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      return Response.json([]);
    }));
    const response = await list();
    expect(response.status).toBe(200);
    expect(urls[0]).toMatch(/\/api\/v1\/video\/automation\/videos$/);
  });

  it("forwards the filters the API knows and leaves the rest behind", async () => {
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string) => {
      urls.push(url.replace(/^.*\/api\/v1\/video\//, ""));
      return Response.json([]);
    }));
    const others = await list("?shorts=exclude&debug=1");
    const mine = await list("?shorts=only&state=library&limit=200&format=shorts");
    const older = await list(`?shorts=only&state=published&before=${encodeURIComponent("2026-10-01T19:30:00+08:00")}`);
    expect([others.status, mine.status, older.status]).toEqual([200, 200, 200]);
    expect(urls).toEqual([
      "automation/videos?shorts=exclude",
      "automation/videos?format=shorts&shorts=only&state=library&limit=200",
      "automation/videos?shorts=only&state=published&before=2026-10-01T19%3A30%3A00%2B08%3A00",
    ]);
  });

  it("refuses a filter value the list does not take instead of answering with every video", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const responses = await Promise.all([
      list("?shorts=some"),
      list("?shorts="),
      list("?state=public"),
      list("?limit=0"),
      list("?limit=201"),
      list("?format=reels"),
      list("?before=yesterday"),
      list("?before=2026-10-01T19:30:00"),
    ]);
    expect(responses.map((response) => response.status)).toEqual(Array(8).fill(422));
    expect((await responses[0].json()).code).toBe("video_list_filter_invalid");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("refuses a browser session without a video tool token", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest(`${BASE}?shorts=only`, { headers: { Cookie: "travel_access=session" } }));
    expect(response.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
