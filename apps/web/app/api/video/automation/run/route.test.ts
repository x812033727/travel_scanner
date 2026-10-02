import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET as settings } from "../settings/route";
import { POST } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;

function stageRequest() {
  return new NextRequest("https://mokaair.com/api/video/automation/run", {
    method: "POST",
    headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify({ stage: "translator", slug: "long-video", instructions: "Translate.", payload: {} }),
  });
}

const failed = (code: string) => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error(code), { code }) });

describe("video automation stage run proxy", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("answers 504 video_ai_run_uncertain when the stage outlives the deadline, which the API may still finish and bill", async () => {
    vi.useFakeTimers();
    let signal: AbortSignal | undefined;
    // The API is still running the model: it answers only when the route gives up waiting.
    vi.stubGlobal("fetch", vi.fn((_url: string, init?: RequestInit) => new Promise<Response>((_resolve, reject) => {
      signal = init?.signal ?? undefined;
      signal?.addEventListener("abort", () => reject(new DOMException("This operation was aborted", "AbortError")));
    })));
    const pending = POST(stageRequest());
    await vi.advanceTimersByTimeAsync(294_999);
    expect(signal?.aborted).toBe(false);
    await vi.advanceTimersByTimeAsync(1);
    const response = await pending;
    expect(signal?.aborted).toBe(true);
    expect(response.status).toBe(504);
    expect((await response.json()).code).toBe("video_ai_run_uncertain");
  });

  it("answers 504 video_ai_run_uncertain when the connection drops after the request went out", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw failed("UND_ERR_SOCKET");
    }));
    const response = await POST(stageRequest());
    expect(response.status).toBe(504);
    expect((await response.json()).code).toBe("video_ai_run_uncertain");
  });

  it("keeps 502 upstream_unavailable for an API it never reached, where nothing ran", async () => {
    for (const code of ["ECONNREFUSED", "ENOTFOUND", "UND_ERR_CONNECT_TIMEOUT"]) {
      vi.stubGlobal("fetch", vi.fn(async () => {
        throw failed(code);
      }));
      const response = await POST(stageRequest());
      expect(response.status).toBe(502);
      expect((await response.json()).code).toBe("upstream_unavailable");
    }
  });

  it("passes the API's own answer through untouched", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "video_ai_upstream_busy", detail: "busy" }, { status: 429, headers: { "Retry-After": "30" } })));
    const response = await POST(stageRequest());
    expect(response.status).toBe(429);
    expect(response.headers.get("retry-after")).toBe("30");
    expect((await response.json()).code).toBe("video_ai_upstream_busy");
  });

  it("leaves the other automation routes as they were: a lost answer is still upstream_unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw failed("UND_ERR_SOCKET");
    }));
    const response = await settings(new NextRequest("https://mokaair.com/api/video/automation/settings", {
      headers: { Authorization: `Bearer ${TOKEN}` },
    }));
    expect(response.status).toBe(502);
    expect((await response.json()).code).toBe("upstream_unavailable");
  });
});
