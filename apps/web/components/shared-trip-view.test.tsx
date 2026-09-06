import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SharedTripView } from "./shared-trip-view";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) =>
    React.createElement("a", { href, ...props }, children),
  usePathname: () => "/",
  useRouter: () => ({ push, replace: vi.fn(), refresh: vi.fn() }),
}));
vi.mock("qrcode", () => ({ default: { toDataURL: async () => "data:image/png;base64,QR" } }));

const sharedTrip = {
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
};

afterEach(() => {
  vi.unstubAllGlobals();
  push.mockReset();
});

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

  it("copies the trip into the reader's own account and opens it", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "POST") {
        return new Response(JSON.stringify({ ...sharedTrip, id: "trip-copy" }), { status: 201 });
      }
      return new Response(JSON.stringify(sharedTrip));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<SharedTripView token="abc" />);

    fireEvent.click(await screen.findByRole("button", { name: "存成我的行程" }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/trips/trip-copy"));
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("/shared-trips/abc/fork"))).toBe(true);
  });

  it("sends a signed-out reader to sign in and back to the same link", async () => {
    vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
      if (init?.method === "POST") {
        return new Response(JSON.stringify({ detail: "unauthorized" }), { status: 401 });
      }
      return new Response(JSON.stringify(sharedTrip));
    }));
    render(<SharedTripView token="abc" />);

    fireEvent.click(await screen.findByRole("button", { name: "存成我的行程" }));

    await waitFor(() => expect(push).toHaveBeenCalledWith("/login?next=%2Fshare%2Fabc"));
  });

  it("shows the share link as a QR code drawn in the browser", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(sharedTrip))));
    render(<SharedTripView token="abc" />);
    const image = await screen.findByRole("img", { name: "這個分享連結的 QR code" });
    expect(image.getAttribute("src")).toContain("data:image/png");
  });

  it("explains a revoked link without offering the onward call to action", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "missing" }), { status: 404 })));
    render(<SharedTripView token="gone" />);
    expect((await screen.findByRole("alert")).textContent).toContain("已被撤銷");
    expect(screen.queryByRole("link", { name: "用 Mokaair 規劃你的旅行" })).toBeNull();
  });
});
