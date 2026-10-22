import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST as report } from "./[slug]/report/route";
import { GET as config } from "./config/route";
import { POST as lock } from "./lock/route";
import { POST as answer } from "./test/[id]/route";

const TOKEN = `mkv_${"a".repeat(43)}`;
const ID = "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b";
const auth = { Authorization: `Bearer ${TOKEN}`, Cookie: "travel_access=session" };
const json = { ...auth, "Content-Type": "application/json" };
const BASE = "https://mokaair.com/api/video/automation/backup";

describe("video backup proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("forwards the worker's reads and reports with its token, never its cookies", async () => {
    const calls: { url: string; method: string; body: string }[] = [];
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      const headers = new Headers(init?.headers);
      expect(headers.get("authorization")).toBe(`Bearer ${TOKEN}`);
      expect(headers.has("cookie")).toBe(false);
      calls.push({ url, method: init?.method ?? "GET", body: init?.body ? Buffer.from(init.body as ArrayBuffer).toString() : "" });
      return Response.json({ ok: true });
    }));
    const body = JSON.stringify({ state: "pending", folder: "奇聞檔案局/curio-h01", tier: "basic" });
    const answers = await Promise.all([
      config(new NextRequest(`${BASE}/config`, { headers: auth })),
      lock(new NextRequest(`${BASE}/lock`, { method: "POST", headers: json, body: JSON.stringify({ lock_path: "AI/備份" }) })),
      answer(
        new NextRequest(`${BASE}/test/${ID.toUpperCase()}`, { method: "POST", headers: json, body: JSON.stringify({ ok: true, message: "ok" }) }),
        { params: Promise.resolve({ id: ID.toUpperCase() }) },
      ),
      report(
        new NextRequest(`${BASE}/curio-h01/report`, { method: "POST", headers: json, body }),
        { params: Promise.resolve({ slug: "curio-h01" }) },
      ),
    ]);
    expect(answers.map((response) => response.status)).toEqual([200, 200, 200, 200]);
    const paths = calls.map((call) => `${call.method} ${new URL(call.url).pathname}`).sort();
    expect(paths).toEqual([
      "GET /api/v1/video/automation/backup/config",
      "POST /api/v1/video/automation/backup/curio-h01/report",
      "POST /api/v1/video/automation/backup/lock",
      `POST /api/v1/video/automation/backup/test/${ID}`,
    ]);
    expect(calls.find((call) => call.url.endsWith("/report"))?.body).toBe(body);
  });

  it("refuses a stray slug or id, and a request without a video tool token, before the API", async () => {
    const upstream = vi.fn();
    vi.stubGlobal("fetch", upstream);
    const stray = await report(
      new NextRequest(`${BASE}/..%2Fconfig/report`, { method: "POST", headers: json, body: "{}" }),
      { params: Promise.resolve({ slug: "../config" }) },
    );
    const badId = await answer(
      new NextRequest(`${BASE}/test/not-a-uuid`, { method: "POST", headers: json, body: "{}" }),
      { params: Promise.resolve({ id: "not-a-uuid" }) },
    );
    const browser = await config(new NextRequest(`${BASE}/config`, { headers: { Cookie: "travel_access=session" } }));
    expect([stray.status, badId.status, browser.status]).toEqual([404, 404, 401]);
    expect(upstream).not.toHaveBeenCalled();
  });
});
