import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET as overview } from "./route";
import { GET as rows } from "./rows/route";
import { POST as sync } from "./sync/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const BASE = "https://mokaair.com/api/video/youtube-reports";

describe("YouTube channel reports proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the overview, a sync and the rows with the token, never the cookies", async () => {
    const calls: { url: string; method: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      calls.push({ url, method: init?.method ?? "GET", body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      return Response.json({ ok: true });
    }));
    const answers = await Promise.all([
      overview(new NextRequest(BASE, { headers: auth })),
      sync(new NextRequest(`${BASE}/sync`, { method: "POST", headers: { ...auth, "Content-Type": "application/json" }, body: JSON.stringify({ force: true }) })),
      rows(new NextRequest(`${BASE}/rows?report=channel_basic&start=2026-10-01&end=2026-10-31&video_id=vidAAAAAAA1&video_id=vidBBBBBBB2&extra=1`, { headers: auth })),
    ]);
    expect(answers.map((response) => response.status)).toEqual([200, 200, 200]);
    const forwarded = calls.map((call) => `${call.method} ${new URL(call.url).pathname}${new URL(call.url).search}`).sort();
    expect(forwarded).toEqual([
      "GET /api/v1/video/youtube-reports",
      "GET /api/v1/video/youtube-reports/rows?report=channel_basic&start=2026-10-01&end=2026-10-31&format=json&video_id=vidAAAAAAA1&video_id=vidBBBBBBB2",
      "POST /api/v1/video/youtube-reports/sync",
    ]);
    expect(calls.find((call) => call.method === "POST")?.body).toBe(JSON.stringify({ force: true }));
  });

  it("refuses a bad query or a missing token before the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const bad = await Promise.all([
      rows(new NextRequest(`${BASE}/rows?report=channel_basic&start=yesterday&end=2026-10-31`, { headers: auth })),
      rows(new NextRequest(`${BASE}/rows?report=../admin&start=2026-10-01&end=2026-10-31`, { headers: auth })),
      rows(new NextRequest(`${BASE}/rows?report=channel_basic&start=2026-10-01&end=2026-10-31&format=xml`, { headers: auth })),
      rows(new NextRequest(`${BASE}/rows?report=channel_basic&start=2026-10-01&end=2026-10-31&video_id=a%20b`, { headers: auth })),
    ]);
    expect(bad.map((response) => response.status)).toEqual([422, 422, 422, 422]);
    const anonymous = await overview(new NextRequest(BASE, { headers: { Cookie: "travel_access=session" } }));
    expect(anonymous.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
