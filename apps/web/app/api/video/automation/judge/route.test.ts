import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as outline } from "./outline/route";
import { POST as policy } from "./policy/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session", "Content-Type": "application/json" };

describe("video judge proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

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
});
