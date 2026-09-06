import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CurrencySwitcher } from "./currency-switcher";
import { HeaderSessionProvider } from "./header-session";

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

// The layout wraps the whole page in this; the switcher reads the currency from it
// rather than asking /auth/me for a second copy of the same profile.
function renderSwitcher() {
  return render(
    <HeaderSessionProvider>
      <CurrencySwitcher />
    </HeaderSessionProvider>,
  );
}

afterEach(() => vi.unstubAllGlobals());

describe("currency switcher", () => {
  it("shows the saved currency and a sample formatted with it", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ id: "u1", preferred_currency: "JPY" })));
    renderSwitcher();

    const select = (await screen.findByLabelText("幣別")) as HTMLSelectElement;
    expect(select.value).toBe("JPY");
    expect(screen.getByText(/顯示範例/).textContent).toContain("1,234");
    // JPY has no minor unit, so the sample must not carry decimals.
    expect(screen.getByText(/顯示範例/).textContent).not.toContain("1,234.00");
  });

  it("saves the chosen currency without touching the locale", async () => {
    const fetchMock = vi.fn<(url: string, init?: RequestInit) => Promise<unknown>>(async () =>
      ok({ id: "u1", preferred_currency: "TWD" }),
    );
    vi.stubGlobal("fetch", fetchMock);
    renderSwitcher();

    const select = await screen.findByLabelText("幣別");
    fireEvent.change(select, { target: { value: "KRW" } });

    await waitFor(() => {
      const patch = fetchMock.mock.calls.find(([, init]) => init?.method === "PATCH");
      expect(patch).toBeTruthy();
      expect(JSON.parse(String(patch?.[1]?.body))).toEqual({ preferred_currency: "KRW" });
    });
  });

  it("puts the saved currency back when the request fails", async () => {
    const fetchMock = vi.fn(async (_url: string, init?: RequestInit) =>
      init?.method === "PATCH"
        ? { ok: false, status: 500, json: async () => ({ detail: "boom" }) }
        : ok({ id: "u1", preferred_currency: "TWD" }),
    );
    vi.stubGlobal("fetch", fetchMock);
    renderSwitcher();

    const select = (await screen.findByLabelText("幣別")) as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "THB" } });

    await waitFor(() => expect(screen.getByRole("status").textContent).toContain("還原"));
    expect(select.value).toBe("TWD");
  });

  it("renders nothing for a signed-out visitor", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({ ok: false, status: 401, json: async () => ({ detail: "請先登入" }) })),
    );
    const { container } = renderSwitcher();

    await waitFor(() => expect(container.querySelector("section")).toBeNull());
    expect(screen.queryByLabelText("幣別")).toBeNull();
  });

  it("still offers the control when the profile request fails for any other reason", async () => {
    // Only 401 means "nowhere to store this". A 500 must not delete the whole
    // section from a signed-in member's account page.
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({ ok: false, status: 503, json: async () => ({ detail: "維護中" }) })),
    );
    renderSwitcher();

    const select = (await screen.findByLabelText("幣別")) as HTMLSelectElement;
    expect(select.value).toBe("TWD");
  });

  it("does not let a late failure undo a newer choice that saved", async () => {
    const pendingPatches: Array<(value: unknown) => void> = [];
    vi.stubGlobal(
      "fetch",
      vi.fn(async (_url: string, init?: RequestInit) => {
        if (init?.method !== "PATCH") return ok({ id: "u1", preferred_currency: "TWD" });
        if (pendingPatches.length === 0) {
          // Hold the first save open so the second one can overtake it.
          return new Promise((_resolve, reject) => pendingPatches.push(reject));
        }
        return ok({});
      }),
    );
    renderSwitcher();

    const select = (await screen.findByLabelText("幣別")) as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "JPY" } });
    await waitFor(() => expect(select.value).toBe("JPY"));
    fireEvent.change(select, { target: { value: "KRW" } });
    await waitFor(() => expect(select.value).toBe("KRW"));

    pendingPatches[0]?.(new Error("the first save finally gave up"));

    await waitFor(() => expect(select.value).toBe("KRW"));
    expect(screen.queryByRole("status")).toBeNull();
  });

  it("asks /auth/me once, not once per component on the page", async () => {
    const fetchMock = vi.fn<(url: string) => Promise<unknown>>(async () =>
      ok({ id: "u1", preferred_currency: "JPY" }),
    );
    vi.stubGlobal("fetch", fetchMock);
    renderSwitcher();

    await screen.findByLabelText("幣別");
    expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith("/auth/me"))).toHaveLength(1);
  });
});
