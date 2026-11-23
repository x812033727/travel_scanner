import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminGeminiPool, type GeminiPoolKey } from "./admin-gemini-pool";

const ENDPOINT = "/api/travel/admin/provider-settings/ai_vendors/gemini-pool";

function key(overrides: Partial<GeminiPoolKey>): GeminiPoolKey {
  return {
    fingerprint_tail: "abcd",
    position: 0,
    site_key: false,
    active: false,
    resting: null,
    rest_seconds: 0,
    month_usd: 0,
    budget_usd: null,
    ...overrides,
  };
}

function json(value: unknown, status = 200) {
  return Promise.resolve(
    new Response(JSON.stringify(value), {
      status,
      headers: { "Content-Type": "application/json" },
    }),
  );
}

describe("AdminGeminiPool", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("lists each key in order with its state, current turn badge and estimated spend", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) => {
        expect(url).toContain(ENDPOINT);
        return json({
          redis_ok: true,
          current_turn_slot: "B",
          keys: [
            key({
              slot: "A",
              fingerprint_tail: "aaaa",
              position: 0,
              resting: "exhausted",
              rest_seconds: 3600,
              month_usd: 100.2,
            }),
            key({
              slot: "B",
              fingerprint_tail: "bbbb",
              position: 1,
              active: true,
              is_turn: true,
              month_usd: 12.5,
              budget_usd: 95,
            }),
            key({ slot: "SITE", fingerprint_tail: "cccc", position: 2, site_key: true }),
          ],
        });
      }),
    );
    render(<AdminGeminiPool />);
    expect(await screen.findByText("…aaaa")).toBeTruthy();
    expect(screen.getByTestId("gemini-pool-current-turn").textContent).toContain("帳號 B");
    expect(screen.getByText(/額度用完，休息到/)).toBeTruthy();
    expect(screen.getByText("使用中")).toBeTruthy();
    expect(screen.getByText("US$95.00")).toBeTruthy();
    expect(screen.getByText("網站金鑰")).toBeTruthy();
    expect(screen.getByRole("link", { name: /AI Studio/ }).getAttribute("href")).toBe(
      "https://aistudio.google.com/billing",
    );
  });

  it("saves a single slot individually, switches starting turn slot, and expands new slots", async () => {
    const calls: Array<{ url: string; method: string; body?: string }> = [];
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string, init?: RequestInit) => {
        const method = init?.method ?? "GET";
        calls.push({ url, method, body: init?.body as string | undefined });
        return json({
          redis_ok: true,
          current_turn_slot: "C",
          slot_count: 4,
          keys: [
            key({ slot: "A", fingerprint_tail: "aaaa", position: 0 }),
            key({ slot: "C", fingerprint_tail: "cccc", position: 1, active: true, is_turn: true, budget_usd: 80 }),
            key({ slot: "SITE", fingerprint_tail: "ffff", position: 2, site_key: true }),
          ],
        });
      }),
    );
    render(<AdminGeminiPool />);
    expect(await screen.findByText("…aaaa")).toBeTruthy();

    // Save slot C individually with its own key and budget
    fireEvent.change(screen.getByTestId("gemini-slot-key-C"), {
      target: { value: "AIzaSySlotCKey" },
    });
    fireEvent.change(screen.getByTestId("gemini-slot-budget-C"), {
      target: { value: "80" },
    });
    fireEvent.click(screen.getByTestId("gemini-slot-save-C"));

    await waitFor(() => {
      expect(calls.some((c) => c.method === "PUT" && c.url.endsWith("/slots/C"))).toBe(true);
    });
    const putCall = calls.find((c) => c.method === "PUT" && c.url.endsWith("/slots/C"))!;
    expect(JSON.parse(putCall.body!)).toEqual({ api_key: "AIzaSySlotCKey", budget_usd: 80 });

    // Switch starting turn to slot A
    fireEvent.click(screen.getByTestId("gemini-slot-turn-A"));
    await waitFor(() => {
      expect(calls.some((c) => c.method === "POST" && c.url.endsWith("/turn"))).toBe(true);
    });
    const turnCall = calls.find((c) => c.method === "POST" && c.url.endsWith("/turn"))!;
    expect(JSON.parse(turnCall.body!)).toEqual({ slot: "A" });

    // Click "+ 新增帳號槽 (E)" to expand slot E
    expect(screen.queryByTestId("gemini-slot-row-E")).toBeNull();
    fireEvent.click(screen.getByTestId("gemini-slot-add"));
    expect(screen.getByTestId("gemini-slot-row-E")).toBeTruthy();
  });

  it("explains how to add keys when there is only one", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => json({ redis_ok: true, keys: [key({ site_key: true, active: true })] })),
    );
    render(<AdminGeminiPool />);
    expect(await screen.findByText(/目前只有一把 Gemini 金鑰/)).toBeTruthy();
  });
});
