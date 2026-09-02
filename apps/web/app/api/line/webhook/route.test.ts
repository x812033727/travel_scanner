import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "./route";

describe("LINE webhook proxy", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("preserves the exact body and signature", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) => {
      expect(init?.body).toBeInstanceOf(ArrayBuffer);
      expect(new TextDecoder().decode(init?.body as ArrayBuffer)).toBe('{"events":[]}\n');
      expect(new Headers(init?.headers).get("x-line-signature")).toBe("signed-value");
      expect(new Headers(init?.headers).has("authorization")).toBe(false);
      return new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest("https://mokaair.com/api/line/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Line-Signature": "signed-value" },
      body: '{"events":[]}\n',
    });
    const response = await POST(request);
    expect(response.status).toBe(200);
    expect(fetchMock).toHaveBeenCalledOnce();
  });

  it("rejects unsigned requests before forwarding", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const request = new NextRequest("https://mokaair.com/api/line/webhook", {
      method: "POST",
      body: "{}",
    });
    const response = await POST(request);
    expect(response.status).toBe(401);
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
