import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET as context } from "./[slug]/context/route";
import { POST as docs } from "./[slug]/docs/route";
import { POST as done } from "./[slug]/episodes/[number]/done/route";
import { POST as recap } from "./[slug]/episodes/[number]/recap/route";
import { POST as start } from "./[slug]/episodes/[number]/start/route";
import { POST as answer } from "./messages/[id]/answer/route";
import { GET as nextMessage } from "./messages/next/route";
import { GET as next } from "./next/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const BASE = "https://mokaair.com/api/video/automation/series";
const params = (slug: string) => ({ params: Promise.resolve({ slug }) });
const episode = (slug: string, number: string) => ({ params: Promise.resolve({ slug, number }) });
const post = (url: string, body?: unknown) => new NextRequest(url, {
  method: "POST", headers: { ...auth, "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body),
});

describe("video series proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the worker's next-job and context reads with the token, never its cookies", async () => {
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      urls.push(url);
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      return Response.json({ job: null });
    }));
    const job = await next(new NextRequest(`${BASE}/next`, { headers: auth }));
    const whole = await context(new NextRequest(`${BASE}/xianxia/context`, { headers: auth }), params("xianxia"));
    const one = await context(new NextRequest(`${BASE}/xianxia/context?episode=12&extra=1`, { headers: auth }), params("xianxia"));
    const odd = await context(new NextRequest(`${BASE}/xianxia/context?episode=abc`, { headers: auth }), params("xianxia"));
    expect([job.status, whole.status, one.status, odd.status]).toEqual([200, 200, 200, 200]);
    expect(urls[0]).toMatch(/\/api\/v1\/video\/automation\/series\/next$/);
    expect(urls[1]).toMatch(/\/api\/v1\/video\/automation\/series\/xianxia\/context$/);
    expect(urls[2]).toMatch(/\/api\/v1\/video\/automation\/series\/xianxia\/context\?episode=12$/);
    expect(urls[3]).toMatch(/\/context$/);
  });

  it("files a document and starts, recaps and finishes an episode by slug and number", async () => {
    const calls: { url: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      calls.push({ url, body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      return Response.json({ ok: true });
    }));
    const filed = await docs(post(`${BASE}/xianxia/docs`, { kind: "setting", body_md: "# x", body_json: {} }), params("xianxia"));
    const started = await start(post(`${BASE}/xianxia/episodes/1/start`, { slug: "xianxia-e001" }), episode("xianxia", "1"));
    const told = await recap(post(`${BASE}/xianxia/episodes/1/recap`, { recap: "…", state: {} }), episode("xianxia", "1"));
    const finished = await done(post(`${BASE}/xianxia/episodes/1/done`), episode("xianxia", "1"));
    expect([filed.status, started.status, told.status, finished.status]).toEqual([200, 200, 200, 200]);
    expect(calls.map((call) => call.url.replace(/^.*\/api\/v1\/video\//, ""))).toEqual([
      "automation/series/xianxia/docs",
      "automation/series/xianxia/episodes/1/start",
      "automation/series/xianxia/episodes/1/recap",
      "automation/series/xianxia/episodes/1/done",
    ]);
    expect(calls[1].body).toBe(JSON.stringify({ slug: "xianxia-e001" }));
  });

  it("refuses a slug or a number that is not one before reaching the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const stray = await docs(post(`${BASE}/../settings/docs`, {}), params("../settings"));
    const zero = await start(post(`${BASE}/xianxia/episodes/0/start`, {}), episode("xianxia", "0"));
    const upper = await done(post(`${BASE}/Xianxia/episodes/1/done`), episode("Xianxia", "1"));
    expect([stray.status, zero.status, upper.status]).toEqual([404, 404, 404]);
    expect((await stray.json()).code).toBe("video_series_not_found");
    expect((await zero.json()).code).toBe("video_series_episode_not_found");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("hands the worker the next line to answer and forwards its answer by message id", async () => {
    const calls: { url: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      calls.push({ url, body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      return Response.json({ job: null });
    }));
    const id = "0b2c4d6e-8f01-4a2b-9c3d-5e6f7a8b9c0d";
    const waiting = await nextMessage(new NextRequest(`${BASE}/messages/next`, { headers: auth }));
    const answered = await answer(post(`${BASE}/messages/${id.toUpperCase()}/answer`, { reply_md: "改好了", revised: null }), { params: Promise.resolve({ id: id.toUpperCase() }) });
    const stray = await answer(post(`${BASE}/messages/not-an-id/answer`, { reply_md: "x" }), { params: Promise.resolve({ id: "not-an-id" }) });
    expect([waiting.status, answered.status, stray.status]).toEqual([200, 200, 404]);
    expect(calls.map((call) => call.url.replace(/^.*\/api\/v1\/video\//, ""))).toEqual([
      "automation/series/messages/next",
      `automation/series/messages/${id}/answer`,
    ]);
    expect(calls[1].body).toBe(JSON.stringify({ reply_md: "改好了", revised: null }));
    expect((await stray.json()).code).toBe("video_drama_message_not_found");
  });

  it("refuses a browser session without a video tool token", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const response = await next(new NextRequest(`${BASE}/next`, { headers: { Cookie: "travel_access=session" } }));
    expect(response.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
