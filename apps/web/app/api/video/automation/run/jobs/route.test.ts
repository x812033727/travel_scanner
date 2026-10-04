import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";
import { GET } from "./[id]/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const ID = "e97d80b6-6508-485d-a193-a7f8ead62623";
const HASH = "a".repeat(64);
const headers = { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" };

describe("durable video writing transport", () => {
  afterEach(() => { vi.useRealTimers(); vi.unstubAllGlobals(); });

  it("passes the persistent request identity through and returns promptly without waiting for writing", async () => {
    const body = { request_key: ID, stage: "writer", slug: "long-video", instructions: "Write.", payload: {} };
    const fetch = vi.fn<(url: string, init?: RequestInit) => Promise<Response>>(async () => Response.json({ id: ID, input_hash: HASH, status: "queued" }));
    vi.stubGlobal("fetch", fetch);
    const response = await POST(new NextRequest("https://mokaair.com/api/video/automation/run/jobs", { method: "POST", headers, body: JSON.stringify(body) }));
    expect(await response.json()).toEqual({ id: ID, input_hash: HASH, status: "queued" });
    expect(fetch.mock.calls[0][0]).toContain("/video/automation/run/jobs");
    const init = fetch.mock.calls[0][1] as RequestInit;
    expect(new Headers(init.headers).get("authorization")).toBe(`Bearer ${TOKEN}`);
    expect(JSON.parse(new TextDecoder().decode(init.body as ArrayBuffer))).toEqual(body);
  });

  it("reads only the requested receipt/hash using token authorization and no browser cookies", async () => {
    const fetch = vi.fn<(url: string, init?: RequestInit) => Promise<Response>>(async () => Response.json({ id: ID, status: "succeeded", result: { text: "saved answer" } }));
    vi.stubGlobal("fetch", fetch);
    const response = await GET(new NextRequest(`https://mokaair.com/api/video/automation/run/jobs/${ID}?input_hash=${HASH}&ignored=1`, { headers: { ...headers, Cookie: "owner=session" } }), { params: Promise.resolve({ id: ID }) });
    expect((await response.json()).result.text).toBe("saved answer");
    expect(fetch.mock.calls[0][0]).toContain(`/video/automation/run/jobs/${ID}?input_hash=${HASH}`);
    expect(fetch.mock.calls[0][0]).not.toContain("ignored");
    expect(new Headers((fetch.mock.calls[0][1] as RequestInit).headers).has("cookie")).toBe(false);
  });

  it("rejects malformed receipt IDs and hash parameters before contacting the API", async () => {
    const fetch = vi.fn();
    vi.stubGlobal("fetch", fetch);
    for (const [id, hash] of [["../other", HASH], [ID, `${HASH}&other=1`]]) {
      const response = await GET(new NextRequest(`https://mokaair.com/api/video/automation/run/jobs/${ID}?input_hash=${encodeURIComponent(hash)}`, { headers }), { params: Promise.resolve({ id }) });
      expect(response.status).toBe(400);
    }
    expect(fetch).not.toHaveBeenCalled();
  });

  it("bounds lost submission responses to 30 seconds; reconnect may use the same request key", async () => {
    vi.useFakeTimers();
    vi.stubGlobal("fetch", vi.fn((_url: string, init?: RequestInit) => new Promise<Response>((_resolve, reject) => {
      init?.signal?.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")));
    })));
    const pending = POST(new NextRequest("https://mokaair.com/api/video/automation/run/jobs", { method: "POST", headers, body: JSON.stringify({ request_key: ID }) }));
    await vi.advanceTimersByTimeAsync(30_000);
    const response = await pending;
    expect(response.status).toBe(502);
    expect((await response.json()).code).toBe("upstream_unavailable");
  });
});
