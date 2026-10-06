import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as outline } from "./outline/route";
import { POST as policy } from "./policy/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session", "Content-Type": "application/json" };

// What Node's fetch throws: a TypeError whose cause carries the socket's code.
const failed = (code: string) => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error(code), { code }) });

// Each judgement takes one call off the daily Jev budget before the API asks Jev.
const JUDGES = [
  { path: "automation/judge/policy", send: policy },
  { path: "automation/judge/outline", send: outline },
];
const judgeRequest = (path: string) =>
  new NextRequest(`https://mokaair.com/api/video/${path}`, { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: "{}" });

describe("video judge proxy", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("forwards the outline and policy judgements with the token, never its cookies", async () => {
    const calls: { url: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      calls.push({ url, body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      return Response.json({ passed: true });
    }));
    const pick = JSON.stringify({ slug: "ai-agent-permissions", brief: "# 企劃", options: [{ key: "A", title: "a" }, { key: "B", title: "b" }] });
    const picked = await outline(new NextRequest("https://mokaair.com/api/video/automation/judge/outline", { method: "POST", headers: auth, body: pick }));
    const verdict = await policy(new NextRequest("https://mokaair.com/api/video/automation/judge/policy", { method: "POST", headers: auth, body: '{"slug":"x","script":"旁白","viewpoint":""}' }));
    expect([picked.status, verdict.status]).toEqual([200, 200]);
    expect(calls[0].url).toMatch(/\/api\/v1\/video\/automation\/judge\/outline$/);
    expect(calls[0].body).toBe(pick);
    expect(calls[1].url).toMatch(/\/api\/v1\/video\/automation\/judge\/policy$/);
  });

  it("refuses a browser session without a video tool token", async () => {
    const fetchSpy = vi.fn();
    vi.stubGlobal("fetch", fetchSpy);
    const refused = await outline(new NextRequest("https://mokaair.com/api/video/automation/judge/outline", { method: "POST", headers: { Cookie: "travel_access=session" }, body: "{}" }));
    expect(refused.status).toBe(401);
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("answers 504 video_judge_answer_lost when a judgement outlives the deadline, which the API may still finish and count", async () => {
    vi.useFakeTimers();
    for (const { path, send } of JUDGES) {
      let signal: AbortSignal | undefined;
      // The API is still waiting on Jev: it answers only when the route gives up waiting.
      vi.stubGlobal("fetch", vi.fn((_url: string, init?: RequestInit) => new Promise<Response>((_resolve, reject) => {
        signal = init?.signal ?? undefined;
        signal?.addEventListener("abort", () => reject(new DOMException("This operation was aborted", "AbortError")));
      })));
      const pending = send(judgeRequest(path));
      await vi.advanceTimersByTimeAsync(179_999);
      expect(signal?.aborted, path).toBe(false);
      await vi.advanceTimersByTimeAsync(1);
      const response = await pending;
      expect(signal?.aborted, path).toBe(true);
      expect(response.status, path).toBe(504);
      expect(response.headers.get("cache-control"), path).toBe("no-store");
      expect((await response.json()).code, path).toBe("video_judge_answer_lost");
    }
  });

  it("answers 504 video_judge_answer_lost when the connection drops after a judgement went out", async () => {
    for (const { path, send } of JUDGES) {
      for (const code of ["UND_ERR_SOCKET", "ECONNRESET", "UND_ERR_HEADERS_TIMEOUT"]) {
        vi.stubGlobal("fetch", vi.fn(async () => {
          throw failed(code);
        }));
        const response = await send(judgeRequest(path));
        expect(response.status, `${path} ${code}`).toBe(504);
        expect((await response.json()).code, `${path} ${code}`).toBe("video_judge_answer_lost");
      }
    }
  });

  it("keeps 502 upstream_unavailable for an API a judgement never reached, where no Jev call was counted", async () => {
    for (const { path, send } of JUDGES) {
      for (const code of ["ECONNREFUSED", "ENOTFOUND", "EAI_AGAIN", "UND_ERR_CONNECT_TIMEOUT"]) {
        vi.stubGlobal("fetch", vi.fn(async () => {
          throw failed(code);
        }));
        const response = await send(judgeRequest(path));
        expect(response.status, `${path} ${code}`).toBe(502);
        expect((await response.json()).code, `${path} ${code}`).toBe("upstream_unavailable");
      }
    }
  });

  it("passes the API's own 502 after a failed Jev call through untouched", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "video_judge_upstream_failed", detail: "Jev 暫時無法判斷" }, { status: 502 })));
    for (const { path, send } of JUDGES) {
      const response = await send(judgeRequest(path));
      expect(response.status, path).toBe(502);
      expect((await response.json()).code, path).toBe("video_judge_upstream_failed");
    }
  });
});
