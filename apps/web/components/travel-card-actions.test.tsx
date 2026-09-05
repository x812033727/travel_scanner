import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SavedItemsProvider } from "./saved-items-provider";
import { TravelCardActions } from "./travel-card-actions";

function stubFetch(savedItems: () => Promise<Response> | Response) {
  return vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.includes("/saved-items")) return savedItems();
    return new Response(JSON.stringify({ items: [] }));
  });
}

function card() {
  return (
    <SavedItemsProvider>
      <TravelCardActions
        type="hotspot"
        id="abc-123"
        title="淺草寺"
        selectionPath="/hotspots/abc-123/trip-selections"
      />
    </SavedItemsProvider>
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.location.hash = "";
});

describe("travel card actions", () => {
  it("shares a link that comes back to this card, not the bare list", async () => {
    vi.stubGlobal("fetch", stubFetch(() => new Response(JSON.stringify({ items: [] }))));
    const writeText = vi.fn();
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
    render(card());

    fireEvent.click(await screen.findByRole("button", { name: "分享" }));

    await waitFor(() => expect(writeText).toHaveBeenCalled());
    const url = String(writeText.mock.calls[0][0]);
    expect(url).toContain("#hotspot-abc-123");
    expect(await screen.findByText("已複製連結")).toBeTruthy();
  });

  it("does not throw a signed-in reader into the login sheet while auth is still loading", async () => {
    // Keep /saved-items pending forever: the provider stays in "loading".
    vi.stubGlobal("fetch", stubFetch(() => new Promise<Response>(() => undefined)));
    render(card());

    fireEvent.click(await screen.findByRole("button", { name: "收藏" }));

    expect(screen.queryByText("登入後繼續使用此功能")).toBeNull();
  });

  it("links to the trip after a place is added instead of ending on a toast", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      if (url.includes("/trips/options")) {
        return new Response(JSON.stringify({ items: [
          { trip_id: "trip-1", name: "東京五日", version: 3, start_date: "2026-11-10", end_date: "2026-11-14" },
        ] }));
      }
      if (url.includes("/trip-selections")) return new Response(JSON.stringify({ ok: true }));
      return new Response(JSON.stringify({ items: [] }));
    }));
    render(card());

    // The provider settles asynchronously; taps while it is loading are ignored on purpose.
    await waitFor(() => {
      fireEvent.click(screen.getByRole("button", { name: "加入行程" }));
      expect(screen.getByRole("dialog")).toBeTruthy();
    });
    fireEvent.click(await screen.findByRole("button", { name: "加入" }));

    const link = await screen.findByRole("link", { name: "查看旅程" });
    expect(link.getAttribute("href")).toBe("/trips/trip-1");
    const selection = vi.mocked(fetch).mock.calls.find(([input]) => String(input).includes("/trip-selections"));
    expect(JSON.parse(String(selection?.[1]?.body))).toMatchObject({ trip_id: "trip-1", version: 3, day_date: "2026-11-10" });
  });

  it("offers to create a trip when the member has none yet", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      return new Response(JSON.stringify({ items: [] }));
    }));
    render(card());

    await waitFor(() => {
      fireEvent.click(screen.getByRole("button", { name: "加入行程" }));
      expect(screen.getByRole("dialog")).toBeTruthy();
    });

    const link = await screen.findByRole("link", { name: "建立旅程" });
    expect(link.getAttribute("href")).toBe("/trips/new");
  });

  it("still asks a signed-out visitor to sign in", async () => {
    vi.stubGlobal(
      "fetch",
      stubFetch(() => new Response(JSON.stringify({ detail: "請先登入" }), { status: 401 })),
    );
    render(card());

    // Wait for the provider to settle into signed_out before tapping.
    await waitFor(() => expect(vi.mocked(fetch)).toHaveBeenCalled());
    fireEvent.click(await screen.findByRole("button", { name: "收藏" }));

    expect(await screen.findByText("登入後繼續使用此功能")).toBeTruthy();
  });
});
