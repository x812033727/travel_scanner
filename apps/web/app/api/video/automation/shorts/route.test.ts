import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as done } from "./[slug]/done/route";
import { POST as start } from "./[slug]/start/route";
import { GET as next } from "./next/route";
import { POST as plan } from "./plan/route";
import { POST as report } from "./report/route";
import { GET as settings } from "./settings/route";
import { POST as tick } from "./tick/route";
import { POST as topics } from "./topics/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const BASE = "https://mokaair.com/api/video/automation/shorts";
const params = (slug: string) => ({ params: Promise.resolve({ slug }) });
const get = (path: string, headers: Record<string, string> = auth) => new NextRequest(`${BASE}/${path}`, { headers });
const post = (path: string, body?: unknown, headers: Record<string, string> = auth) => new NextRequest(`${BASE}/${path}`, {
  method: "POST", headers: { ...headers, "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body),
});

describe("video shorts proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards every Shorts route to its API path with the token, never the cookies", async () => {
    const calls: { url: string; method: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      calls.push({
        url: url.replace(/^.*\/api\/v1\/video\//, ""),
        method: String(init?.method),
        body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "",
      });
      return Response.json({ ok: true });
    }));
    const responses = [
      await settings(get("settings")),
      await tick(post("tick")),
      await next(get("next?line=lab")),
      await plan(post("plan", { week_start: "2026-10-05", slots: [] })),
      await topics(post("topics", { topics: [] })),
      await report(post("report", { week_start: "2026-10-05", body_md: "# 上週" })),
      await start(post("receipt-total/start", { topic: "receipt-total" }), params("receipt-total")),
      await done(post("receipt-total/done"), params("receipt-total")),
    ];
    expect(responses.map((response) => response.status)).toEqual(Array(8).fill(200));
    expect(calls.map((call) => `${call.method} ${call.url}`)).toEqual([
      "GET automation/shorts/settings",
      "POST automation/shorts/tick",
      "GET automation/shorts/next",
      "POST automation/shorts/plan",
      "POST automation/shorts/topics",
      "POST automation/shorts/report",
      "POST automation/shorts/receipt-total/start",
      "POST automation/shorts/receipt-total/done",
    ]);
    expect(calls[3].body).toBe(JSON.stringify({ week_start: "2026-10-05", slots: [] }));
    expect(calls[6].body).toBe(JSON.stringify({ topic: "receipt-total" }));
    expect(calls[1].body).toBe("");
  });

  it("refuses a slug that is not a Short's before reaching the API", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const stray = await start(post("x/start", {}), params("../settings"));
    const upper = await done(post("x/done"), params("Receipt"));
    const short = await start(post("x/start", {}), params("ab"));
    const digit = await done(post("x/done"), params("1-receipt"));
    const long = await start(post("x/start", {}), params(`a${"b".repeat(80)}`));
    expect([stray.status, upper.status, short.status, digit.status, long.status]).toEqual([404, 404, 404, 404, 404]);
    expect((await stray.json()).code).toBe("video_shorts_not_found");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("refuses a browser session without a video tool token on every route", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const cookie = { Cookie: "travel_access=session" };
    const responses = [
      await settings(get("settings", cookie)),
      await tick(post("tick", undefined, cookie)),
      await next(get("next", cookie)),
      await plan(post("plan", {}, cookie)),
      await topics(post("topics", {}, cookie)),
      await report(post("report", {}, cookie)),
      await start(post("receipt-total/start", {}, cookie), params("receipt-total")),
      await done(post("receipt-total/done", undefined, cookie), params("receipt-total")),
    ];
    expect(responses.map((response) => response.status)).toEqual(Array(8).fill(401));
    expect((await responses[0].json()).code).toBe("video_tool_token_invalid");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("caps a plan at one mebibyte and the small routes at sixty-four kibibytes", async () => {
    const fetchMock = vi.fn(async () => Response.json({ ok: true }));
    vi.stubGlobal("fetch", fetchMock);
    const within = await plan(post("plan", { body_md: "x".repeat(1024 * 1024 - 64) }));
    const beyond = await report(post("report", { body_md: "x".repeat(1024 * 1024) }));
    const fat = await tick(post("tick", { note: "x".repeat(64 * 1024) }));
    const heavy = await start(post("receipt-total/start", { note: "x".repeat(64 * 1024) }), params("receipt-total"));
    expect([within.status, beyond.status, fat.status, heavy.status]).toEqual([200, 413, 413, 413]);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
