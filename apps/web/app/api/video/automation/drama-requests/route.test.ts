import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as done } from "./[id]/done/route";
import { POST as start } from "./[id]/start/route";
import { GET as next } from "./next/route";
import { GET } from "./route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const ID = "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b";
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const params = (id: string) => ({ params: Promise.resolve({ id }) });

describe("video drama requests proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the worker's queue and next-request reads with the token, never its cookies", async () => {
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      urls.push(url);
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      return Response.json({ requests: [] });
    }));
    const queue = await GET(new NextRequest("https://mokaair.com/api/video/automation/drama-requests", { headers: auth }));
    const oldest = await next(new NextRequest("https://mokaair.com/api/video/automation/drama-requests/next", { headers: auth }));
    expect([queue.status, oldest.status]).toEqual([200, 200]);
    expect(urls[0]).toMatch(/\/api\/v1\/video\/automation\/drama-requests$/);
    expect(urls[1]).toMatch(/\/api\/v1\/video\/automation\/drama-requests\/next$/);
  });

  it("claims and finishes a request by its id, and refuses an id that is not a UUID", async () => {
    const calls: { url: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      calls.push({ url, body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      return Response.json({ id: ID, status: "started" });
    }));
    const claimed = await start(
      new NextRequest(`https://mokaair.com/api/video/automation/drama-requests/${ID.toUpperCase()}/start`, {
        method: "POST", headers: { ...auth, "Content-Type": "application/json" }, body: JSON.stringify({ slug: "jingwei-fills-the-sea" }),
      }),
      params(ID.toUpperCase()),
    );
    const finished = await done(
      new NextRequest(`https://mokaair.com/api/video/automation/drama-requests/${ID}/done`, { method: "POST", headers: auth }),
      params(ID),
    );
    const stray = await start(
      new NextRequest("https://mokaair.com/api/video/automation/drama-requests/../settings/start", { method: "POST", headers: auth }),
      params("../settings"),
    );
    expect([claimed.status, finished.status, stray.status]).toEqual([200, 200, 404]);
    expect(calls).toHaveLength(2);
    expect(calls[0].url).toMatch(new RegExp(`/api/v1/video/automation/drama-requests/${ID}/start$`));
    expect(calls[0].body).toBe(JSON.stringify({ slug: "jingwei-fills-the-sea" }));
    expect(calls[1].url).toMatch(new RegExp(`/api/v1/video/automation/drama-requests/${ID}/done$`));
    expect((await stray.json()).code).toBe("video_drama_request_not_found");
  });

  it("refuses a browser session without a video tool token", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const response = await next(new NextRequest("https://mokaair.com/api/video/automation/drama-requests/next", {
      headers: { Cookie: "travel_access=session" },
    }));
    expect(response.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
