import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET, PART_MAX_BYTES, POST, PUT, reviewRoute } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const SHA = "b".repeat(64);
const context = (...path: string[]) => ({ params: Promise.resolve({ path }) });

describe("video review proxy for the pipeline", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("knows exactly the three pipeline routes", () => {
    expect(reviewRoute(["ai-model-choice"], "PUT")?.kind).toBe("project");
    expect(reviewRoute(["ai-model-choice"], "GET")?.kind).toBe("project");
    expect(reviewRoute(["ai-model-choice", "reviews"], "POST")?.kind).toBe("review");
    expect(reviewRoute(["ai-model-choice", "files", SHA], "PUT")?.maxBytes).toBe(PART_MAX_BYTES);
    for (const [path, method] of [[["ai-model-choice", "files", SHA], "GET"], [["..", "reviews"], "POST"], [["Upper"], "GET"], [["v", "files", "not-a-hash"], "PUT"], [["v", "reviews", "x"], "POST"]] as const) {
      expect(reviewRoute([...path], method)).toBeNull();
    }
  });

  it("forwards a part as bytes with its query, the token and no cookies", async () => {
    const part = new Uint8Array([0, 1, 2, 255]);
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      expect(url).toBe(`http://localhost:8000/api/v1/video/reviews/ai-model-choice/files/${SHA}?part=0&parts=1&size=4`);
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.get("content-type")).toBe("application/octet-stream");
      expect(headers.has("cookie")).toBe(false);
      expect(new Uint8Array(init?.body as ArrayBuffer)).toEqual(part);
      return Response.json({ received: [0], complete: true });
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest(`https://mokaair.com/api/video/reviews/ai-model-choice/files/${SHA}?part=0&parts=1&size=4&extra=1`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" },
      body: part,
    });
    const response = await PUT(request, context("ai-model-choice", "files", SHA));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ received: [0], complete: true });
  });

  it("refuses before forwarding: no token, an unknown route, a part without its query", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const noToken = await GET(new NextRequest("https://mokaair.com/api/video/reviews/v"), context("v"));
    const unknown = await POST(new NextRequest("https://mokaair.com/api/video/reviews/v/other", { method: "POST", headers: { Authorization: `Bearer ${TOKEN}` }, body: "{}" }), context("v", "other"));
    const noQuery = await PUT(new NextRequest(`https://mokaair.com/api/video/reviews/v/files/${SHA}`, { method: "PUT", headers: { Authorization: `Bearer ${TOKEN}` }, body: "x" }), context("v", "files", SHA));
    expect([noToken.status, unknown.status, noQuery.status]).toEqual([401, 404, 422]);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("refuses a part larger than one upload slice", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest(`https://mokaair.com/api/video/reviews/v/files/${SHA}?part=0&parts=2&size=9000000`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${TOKEN}` },
      body: new Uint8Array(PART_MAX_BYTES + 1),
    });
    expect((await PUT(request, context("v", "files", SHA))).status).toBe(413);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
