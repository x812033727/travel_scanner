import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SharedTripView } from "./shared-trip-view";

afterEach(() => vi.unstubAllGlobals());

describe("SharedTripView", () => {
  it("gives the recipient a way onward instead of a dead end", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      id: "trip-1",
      name: "京都五天",
      mode: "manual",
      total_price: 0,
      currency: "TWD",
      data: {},
      version: 1,
      destination_name: "京都",
      timezone: "Asia/Tokyo",
      items: [],
      route_segments: [],
      updated_at: "2026-09-01T00:00:00Z",
    }))));
    render(<SharedTripView token="abc" />);
    await screen.findByRole("heading", { name: "京都五天" });
    expect(screen.getByRole("link", { name: "用 Mokaair 規劃你的旅行" }).getAttribute("href")).toBe("/");
  });

  it("explains a revoked link without offering the onward call to action", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "missing" }), { status: 404 })));
    render(<SharedTripView token="gone" />);
    expect((await screen.findByRole("alert")).textContent).toContain("已被撤銷");
    expect(screen.queryByRole("link", { name: "用 Mokaair 規劃你的旅行" })).toBeNull();
  });
});
