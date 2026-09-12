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

describe("a share link that will not open", () => {
  /**
   * Every failure — a 500, a dropped connection, a link the owner really did turn
   * off — used to say "this link does not exist", and returned early, taking the
   * page's own way onward with it. A recipient gave up on a trip that was still there.
   */
  function stubStatus(status: number) {
    return vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).includes("/shared-trips/")) {
        return new Response(JSON.stringify({ detail: "nope" }), { status, headers: { "Content-Type": "application/json" } });
      }
      return new Response("{}", { status: 200, headers: { "Content-Type": "application/json" } });
    });
  }

  it("offers a retry when the trip simply could not be fetched", async () => {
    const fetchMock = stubStatus(500);
    vi.stubGlobal("fetch", fetchMock);
    render(<SharedTripView token="abc" />);

    expect(await screen.findByText("現在打不開這個行程")).toBeTruthy();
    const before = fetchMock.mock.calls.filter(([url]) => String(url).includes("/shared-trips/")).length;

    fireEvent.click(screen.getByRole("button", { name: "重試一次" }));

    await waitFor(() => expect(
      fetchMock.mock.calls.filter(([url]) => String(url).includes("/shared-trips/")).length,
    ).toBeGreaterThan(before));
  });

  it("says a revoked link is revoked, and does not pretend it can be retried", async () => {
    vi.stubGlobal("fetch", stubStatus(404));
    render(<SharedTripView token="abc" />);

    expect(await screen.findByText(/這個分享連結已經失效/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: "重試一次" })).toBeNull();
  });
});

describe("SharedTripView partner entrances", () => {
  it("offers the destination's partners when the share surface has something ready", async () => {
    const fetchMock = vi.fn(async (url: string) => {
      if (String(url).includes("/affiliates/destination-offers")) {
        return new Response(JSON.stringify({
          destination_id: "osaka-kyoto", module: "activities", disclosure: "Disclosure",
          options: [{ id: "offer-1", brand: "klook", display_name: "Klook", destination_id: "osaka-kyoto", module: "activities", cta: "Klook activities", clickout_url: "/api/travel/affiliates/destination-offers/offer-1/clickout?placement=share" }],
        }));
      }
      return new Response(JSON.stringify({ ...sharedTrip, partner_offers: { destination_id: "osaka-kyoto", modules: ["activities"] } }));
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<SharedTripView token="abc" />);
    expect(await screen.findByRole("button", { name: /Klook activities/ })).toBeTruthy();
    const offerCalls = fetchMock.mock.calls.map(([url]) => String(url)).filter((url) => url.includes("/affiliates/destination-offers"));
    expect(offerCalls).toEqual(["/api/travel/affiliates/destination-offers?destination_id=osaka-kyoto&module=activities&placement=share"]);
  });

  it("asks for nothing when the share surface has nothing ready", async () => {
    const fetchMock = vi.fn<(url: string) => Promise<Response>>(async () => new Response(JSON.stringify({ ...sharedTrip, partner_offers: { destination_id: "osaka-kyoto", modules: [] } })));
    vi.stubGlobal("fetch", fetchMock);
    render(<SharedTripView token="abc" />);
    await screen.findByRole("heading", { name: "京都五天" });
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/affiliates/"))).toBe(false);
  });
});
