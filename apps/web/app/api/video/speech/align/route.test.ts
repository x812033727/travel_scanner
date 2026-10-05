import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const URL = "https://mokaair.com/api/video/speech/align";

// What Node's fetch throws: a TypeError whose cause carries the socket's code.
const failed = (code: string) => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error(code), { code }) });

describe("video speech align proxy", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("forwards the token and the JSON body to the align route and returns its answer", async () => {
    const answer = { source: "azure", model: "zh-TW-HsiaoChenNeural", chars: [{ text: "你", start_ms: 10, end_ms: 200 }], audio: "UklGRg==", billable_characters: 2 };
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toMatch(/\/api\/v1\/video\/speech\/align$/);
      expect(init?.method).toBe("POST");
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      expect(new TextDecoder().decode(init?.body as ArrayBuffer)).toBe('{"speech":{"voice":"v"}}');
      return new Response(JSON.stringify(answer), { status: 200, headers: { "Content-Type": "application/json", "Set-Cookie": "x=1" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await POST(
      new NextRequest(URL, { method: "POST", headers: { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session", "Content-Type": "application/json" }, body: '{"speech":{"voice":"v"}}' }),
    );
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual(answer);
    expect(response.headers.get("set-cookie")).toBeNull();
    expect(response.headers.get("cache-control")).toBe("no-store");
  });

  it("refuses a request without a video tool token before forwarding", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const response = await POST(new NextRequest(URL, { method: "POST", body: "{}" }));
    expect(response.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("lets a clip through at the transcription's cap and passes the API's refusal back", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "video_align_unavailable", detail: "no aligner" }, { status: 503 })));
    const clip = `{"audio":"${"A".repeat(1024 * 1024)}","text":"你好"}`;
    const response = await POST(new NextRequest(URL, { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: clip }));
    expect(response.status).toBe(503);
    expect((await response.json()).code).toBe("video_align_unavailable");
  });

  it("answers 504 video_speech_answer_lost when the connection drops after the request went out, and 502 when it never reached the API", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw failed("ECONNRESET");
    }));
    const lost = await POST(new NextRequest(URL, { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: "{}" }));
    expect(lost.status).toBe(504);
    expect((await lost.json()).code).toBe("video_speech_answer_lost");
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw failed("ECONNREFUSED");
    }));
    const unreachable = await POST(new NextRequest(URL, { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: "{}" }));
    expect(unreachable.status).toBe(502);
    expect((await unreachable.json()).code).toBe("upstream_unavailable");
  });
});
