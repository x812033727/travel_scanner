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
