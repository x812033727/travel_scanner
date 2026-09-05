import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { UsageInsufficientNotice } from "./usage-insufficient-notice";

afterEach(() => vi.unstubAllGlobals());

describe("UsageInsufficientNotice", () => {
  it("tells the member the balance and where to look instead of redirecting", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      remaining_uses: 0, reserved_uses: 0, available_uses: 0, limits: {}, counts: {},
    }))));
    render(<UsageInsufficientNotice chargeLabel="消耗 1 次" />);

    expect(await screen.findByText(/目前可用 0 次/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "查看使用紀錄" }).getAttribute("href")).toBe("/account");
    expect(screen.getByRole("link", { name: "查看方案" }).getAttribute("href")).toBe("/pricing");
  });

  it("does not invent a balance when the usage request fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "down" }), { status: 503 })));
    render(<UsageInsufficientNotice chargeLabel="消耗 1 次" />);

    expect(await screen.findByText(/暫時無法確認剩餘次數/)).toBeTruthy();
  });
});
