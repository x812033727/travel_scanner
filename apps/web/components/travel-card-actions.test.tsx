import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { isTopModalLayer } from "@/lib/modal-sheet";
import { SavedItemsProvider } from "./saved-items-provider";
import { TravelCardActions } from "./travel-card-actions";

function stubFetch(savedItems: () => Promise<Response> | Response) {
  return vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.includes("/saved-items")) return savedItems();
    return new Response(JSON.stringify({ items: [] }));
  });
}

function card(resumeAfterLogin = false) {
  return (
    <SavedItemsProvider>
      <TravelCardActions
        type="hotspot"
        id="abc-123"
        title="淺草寺"
        selectionPath="/hotspots/abc-123/trip-selections"
        resumeAfterLogin={resumeAfterLogin}
      />
    </SavedItemsProvider>
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.location.hash = "";
  window.history.replaceState(null, "", "/");
});

describe("travel card actions", () => {
  it("puts only an explicit card intent in the authenticated return URL", async () => {
    window.history.replaceState(null, "", "/explore?destination=tokyo");
    vi.stubGlobal("fetch", stubFetch(() => new Response(JSON.stringify({ code: "authentication_required" }), { status: 401 })));
    render(card(true));
    await waitFor(() => { fireEvent.click(screen.getByRole("button", { name: "加入行程" })); expect(screen.getByRole("dialog")).toBeTruthy(); });
    const href = screen.getByRole("link", { name: "前往登入" }).getAttribute("href") || "";
    const next = new URL(href, "https://example.test").searchParams.get("next")!;
    expect(next).toContain("destination=tokyo"); expect(next).toContain("resume_action=trip"); expect(next).toContain("resume_item=hotspot%3Aabc-123");
  });
  it("resumes a save with confirmation and never toggles an existing saved item off", async () => {
    window.history.replaceState(null, "", "/explore?resume_action=save&resume_item=hotspot%3Aabc-123");
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ items: [{ type: "hotspot", id: "abc-123" }] }))));
    render(card(true));
    const dialog = await screen.findByRole("dialog", { name: "收藏" });
    expect(vi.mocked(fetch).mock.calls.some(([, init]) => init?.method === "PUT")).toBe(false);
    fireEvent.click(within(dialog).getByRole("button", { name: "已收藏" }));
    await waitFor(() => expect(vi.mocked(fetch).mock.calls.some(([, init]) => init?.method === "PUT")).toBe(true));
    expect(vi.mocked(fetch).mock.calls.some(([, init]) => init?.method === "DELETE")).toBe(false);
  });
  it("resumes trip selection without committing and keeps keyboard focus inside the sheet", async () => {
    window.history.replaceState(null, "", "/explore?resume_action=trip&resume_item=hotspot%3Aabc-123");
    vi.stubGlobal("fetch", stubFetch(() => new Response(JSON.stringify({ items: [] }))));
    render(card(true));
    const dialog = await screen.findByRole("dialog");
    expect(vi.mocked(fetch).mock.calls.some(([path]) => String(path).includes("trip-selections"))).toBe(false);
    const close = within(dialog).getByRole("button", { name: "關閉" });
    close.focus(); fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(dialog.contains(document.activeElement)).toBe(true);
    fireEvent.keyDown(document, { key: "Escape" });
    // Red once under a loaded full run. The sheet opens on a resolved request, and
    // useModalSheet used to attach its Escape listener in a passive effect, which React runs
    // a scheduler task after that commit; `findByRole` could hand back control in between,
    // and this Escape then reached no listener at all. It attaches in a layout effect now,
    // and `lib/modal-sheet.test.tsx` holds that gap open on purpose. The state printed below
    // stays, so anything else that ever fails here says what it saw.
    expect(screen.queryByRole("dialog"), [
      `dialogs in DOM: ${document.querySelectorAll('[role="dialog"]').length}`,
      `sheet still the top layer: ${isTopModalLayer(dialog)}`,
      `sheet connected: ${dialog.isConnected}`,
      `native dialog[open] anywhere: ${document.querySelectorAll("dialog[open]").length}`,
      `body overflow: ${document.body.style.overflow || "(unset)"}`,
    ].join("; ")).toBeNull();
    expect(document.body.style.overflow).not.toBe("hidden");
  });
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
    const body = JSON.parse(String(selection?.[1]?.body));
    expect(body).toMatchObject({ trip_id: "trip-1", version: 3, day_date: "2026-11-10" });
    // Appending is the API's default; a hotspot sends no mode unless the reader picks a meal.
    expect(body).not.toHaveProperty("mode"); expect(body).not.toHaveProperty("meal_role");
  });

  function tripFetch(onSelection: () => Response) {
    return vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/saved-items")) return new Response(JSON.stringify({ items: [] }));
      if (url.includes("/trips/options")) {
        return new Response(JSON.stringify({ items: [
          { trip_id: "trip-1", name: "東京五日", version: 3, start_date: "2026-11-10", end_date: "2026-11-14" },
        ] }));
      }
      if (url.includes("/trip-selections")) return onSelection();
      return new Response(JSON.stringify({ items: [] }));
    });
  }
  function selectionBodies() {
    return vi.mocked(fetch).mock.calls.filter(([input]) => String(input).includes("/trip-selections")).map(([, init]) => JSON.parse(String(init?.body)));
  }

  it("offers lunch and dinner placement and sends it as mode and meal, never meal_role", async () => {
    vi.stubGlobal("fetch", tripFetch(() => new Response(JSON.stringify({ ok: true }))));
    render(card());

    await waitFor(() => {
      fireEvent.click(screen.getByRole("button", { name: "加入行程" }));
      expect(screen.getByRole("dialog")).toBeTruthy();
    });
    const placement = (await screen.findByLabelText("加入方式")) as HTMLSelectElement;
    expect(placement.value).toBe("append");
    expect([...placement.options].map((option) => option.textContent)).toEqual(["接在這天最後", "當作午餐", "當作晚餐"]);
    fireEvent.change(placement, { target: { value: "lunch" } });
    fireEvent.click(screen.getByRole("button", { name: "加入" }));

    await screen.findByRole("link", { name: "查看旅程" });
    expect(selectionBodies()).toEqual([{ trip_id: "trip-1", version: 3, day_date: "2026-11-10", mode: "replace_meal", meal: "lunch" }]);
  });

  it("explains an occupied meal card and overwrites only on a second, explicit tap", async () => {
    let attempts = 0;
    vi.stubGlobal("fetch", tripFetch(() => {
      attempts += 1;
      if (attempts === 1) return new Response(JSON.stringify({ code: "meal_slot_occupied", detail: "occupied" }), { status: 409 });
      return new Response(JSON.stringify({ ok: true }));
    }));
    render(card());

    await waitFor(() => {
      fireEvent.click(screen.getByRole("button", { name: "加入行程" }));
      expect(screen.getByRole("dialog")).toBeTruthy();
    });
    fireEvent.change(await screen.findByLabelText("加入方式"), { target: { value: "dinner" } });
    fireEvent.click(screen.getByRole("button", { name: "加入" }));

    expect(await screen.findByText("這一餐已經有你選好的店家，要換成這個地點嗎？")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "查看旅程" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "換成這個" }));

    await screen.findByRole("link", { name: "查看旅程" });
    const bodies = selectionBodies();
    expect(bodies).toHaveLength(2);
    expect(bodies[0]).toEqual({ trip_id: "trip-1", version: 3, day_date: "2026-11-10", mode: "replace_meal", meal: "dinner" });
    expect(bodies[1]).toEqual({ ...bodies[0], overwrite: true });
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
