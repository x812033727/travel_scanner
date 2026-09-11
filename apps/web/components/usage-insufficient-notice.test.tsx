import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { UsageInsufficientNotice } from "./usage-insufficient-notice";
import { SiteVisibilityProvider } from "./site-visibility-provider";
import { closedSiteVisibility } from "@/lib/site-features";

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

  it("stops pointing at the plans page when the owner has switched it off", async () => {
    // "Go and buy more uses" next to a page that says "temporarily closed" is the
    // other half of the dead end. With pricing off the reader gets a way to ask a
    // human instead.
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      remaining_uses: 0, reserved_uses: 0, available_uses: 0, limits: {}, counts: {},
    }))));
    render(
      <SiteVisibilityProvider state={{ status: "ready", features: closedSiteVisibility }}>
        <UsageInsufficientNotice chargeLabel="消耗 1 次" />
      </SiteVisibilityProvider>,
    );

    expect(await screen.findByRole("link", { name: "聯絡我們" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "查看方案" })).toBeNull();
  });

  it("does not invent a balance when the usage request fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "down" }), { status: 503 })));
    render(<UsageInsufficientNotice chargeLabel="消耗 1 次" />);

    expect(await screen.findByText(/暫時無法確認剩餘次數/)).toBeTruthy();
  });
});
