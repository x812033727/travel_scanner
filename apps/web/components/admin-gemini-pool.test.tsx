import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminGeminiPool, type GeminiPoolKey } from "./admin-gemini-pool";

const ENDPOINT = "/api/travel/admin/provider-settings/ai_vendors/gemini-pool";

function key(overrides: Partial<GeminiPoolKey>): GeminiPoolKey {
  return { fingerprint_tail: "abcd", position: 0, site_key: false, active: false, resting: null, rest_seconds: 0, month_usd: 0, budget_usd: null, ...overrides };
}

function json(value: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }));
}

describe("AdminGeminiPool", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("lists each key in order with its state and estimated spend", async () => {
    vi.stubGlobal("fetch", vi.fn((url: string) => {
      expect(url).toContain(ENDPOINT);
      return json({
        redis_ok: true,
        keys: [
          key({ fingerprint_tail: "aaaa", position: 0, resting: "exhausted", rest_seconds: 3600, month_usd: 100.2 }),
          key({ fingerprint_tail: "bbbb", position: 1, active: true, month_usd: 12.5, budget_usd: 95 }),
          key({ fingerprint_tail: "cccc", position: 2, site_key: true }),
        ],
      });
    }));
    render(<AdminGeminiPool />);
    expect(await screen.findByText("…aaaa")).toBeTruthy();
    expect(screen.getByText(/額度用完，休息到/)).toBeTruthy();
    expect(screen.getByText("使用中")).toBeTruthy();
    expect(screen.getByText("US$95.00")).toBeTruthy();
    expect(screen.getByText("網站金鑰")).toBeTruthy();
    expect(screen.getByRole("link", { name: /AI Studio/ }).getAttribute("href")).toBe("https://aistudio.google.com/billing");
  });

  it("explains how to add keys when there is only one", async () => {
    vi.stubGlobal("fetch", vi.fn(() => json({ redis_ok: true, keys: [key({ site_key: true, active: true })] })));
    render(<AdminGeminiPool />);
    expect(await screen.findByText(/目前只有一把 Gemini 金鑰/)).toBeTruthy();
  });
});
