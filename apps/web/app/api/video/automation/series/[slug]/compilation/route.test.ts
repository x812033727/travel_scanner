import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as done } from "./done/route";
import { POST as start } from "./start/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const BASE = "https://mokaair.com/api/video/automation/series";
const params = (slug: string) => ({ params: Promise.resolve({ slug }) });
const post = (url: string, body?: unknown) => new NextRequest(url, {
  method: "POST", headers: { ...auth, "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body),
});

describe("video series compilation proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("starts and finishes a compilation by series slug with the token, never the cookies", async () => {
    const calls: { url: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      calls.push({ url, body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      return Response.json({ ok: true });
    }));
    const started = await start(post(`${BASE}/wenjian/compilation/start`, { slug: "wenjian-full" }), params("wenjian"));
    const finished = await done(post(`${BASE}/wenjian/compilation/done`), params("wenjian"));
    expect([started.status, finished.status]).toEqual([200, 200]);
    expect(calls.map((call) => call.url.replace(/^.*\/api\/v1\/video\//, ""))).toEqual([
      "automation/series/wenjian/compilation/start",
      "automation/series/wenjian/compilation/done",
    ]);
    expect(calls[0].body).toBe(JSON.stringify({ slug: "wenjian-full" }));
  });

  it("refuses a slug that is not one, and a browser session without a token, before reaching the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const stray = await start(post(`${BASE}/../settings/compilation/start`, {}), params("../settings"));
    const upper = await done(post(`${BASE}/Wenjian/compilation/done`), params("Wenjian"));
    const browser = await done(new NextRequest(`${BASE}/wenjian/compilation/done`, { method: "POST", headers: { Cookie: "travel_access=session" } }), params("wenjian"));
    expect([stray.status, upper.status, browser.status]).toEqual([404, 404, 401]);
    expect((await stray.json()).code).toBe("video_series_not_found");
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
