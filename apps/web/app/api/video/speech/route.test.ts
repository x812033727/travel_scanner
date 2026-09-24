import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as judge } from "./judge/route";
import { POST } from "./route";
import { GET } from "./status/route";
import { POST as transcribe } from "./transcribe/route";

const TOKEN = `mkv_${"a".repeat(43)}`;

describe("video speech proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the token and the JSON body, and returns the audio bytes untouched", async () => {
    const audio = new Uint8Array([0x52, 0x49, 0x46, 0x46, 0x00, 0xff, 0x80, 0x01]);
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toMatch(/\/api\/v1\/video\/speech$/);
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      expect(new TextDecoder().decode(init?.body as ArrayBuffer)).toBe('{"voice":"v"}');
      return new Response(audio, {
        status: 200,
        headers: { "Content-Type": "audio/wav", "X-Billable-Characters": "42", "Set-Cookie": "x=1" },
      });
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest("https://mokaair.com/api/video/speech", {
      method: "POST",
      headers: { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session", "Content-Type": "application/json" },
      body: '{"voice":"v"}',
    });
    const response = await POST(request);
    expect(response.status).toBe(200);
    expect(new Uint8Array(await response.arrayBuffer())).toEqual(audio);
    expect(response.headers.get("x-billable-characters")).toBe("42");
    expect(response.headers.get("set-cookie")).toBeNull();
  });

  it("refuses a request without a video tool token before forwarding", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    for (const authorization of [undefined, "Bearer eyJhbGciOi.session.jwt", `Basic ${TOKEN}`]) {
      const request = new NextRequest("https://mokaair.com/api/video/speech", {
        method: "POST",
        headers: authorization ? { Authorization: authorization } : {},
        body: "{}",
      });
      expect((await POST(request)).status).toBe(401);
    }
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("passes a throttling answer back with its Retry-After", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response('{"code":"video_speech_upstream_busy"}', { status: 429, headers: { "Retry-After": "7", "Content-Type": "application/json" } })),
    );
    const response = await POST(
      new NextRequest("https://mokaair.com/api/video/speech", { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: "{}" }),
    );
    expect(response.status).toBe(429);
    expect(response.headers.get("retry-after")).toBe("7");
  });

  it("serves the status endpoint with GET and no body", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toMatch(/\/api\/v1\/video\/speech\/status$/);
      expect(init?.method).toBe("GET");
      expect(init?.body).toBeUndefined();
      return new Response('{"configured":true}', { status: 200, headers: { "Content-Type": "application/json" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const response = await GET(new NextRequest("https://mokaair.com/api/video/speech/status", { headers: { Authorization: `Bearer ${TOKEN}` } }));
    expect(await response.json()).toEqual({ configured: true });
  });

  it("lets a transcription carry a clip, while speech keeps its smaller cap", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      expect(url).toMatch(/\/api\/v1\/video\/speech\/(transcribe|judge)$/);
      return new Response('{"text":"你好"}', { status: 200, headers: { "Content-Type": "application/json" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const clip = `{"audio":"${"A".repeat(1024 * 1024)}"}`;
    const headers = { Authorization: `Bearer ${TOKEN}` };
    const transcribed = await transcribe(new NextRequest("https://mokaair.com/api/video/speech/transcribe", { method: "POST", headers, body: clip }));
    expect(transcribed.status).toBe(200);
    const judged = await judge(new NextRequest("https://mokaair.com/api/video/speech/judge", { method: "POST", headers, body: '{"lines":[]}' }));
    expect(judged.status).toBe(200);
    expect(fetchMock).toHaveBeenCalledTimes(2);
    const tooBig = await POST(new NextRequest("https://mokaair.com/api/video/speech", { method: "POST", headers, body: clip }));
    expect(tooBig.status).toBe(413);
  });
});
