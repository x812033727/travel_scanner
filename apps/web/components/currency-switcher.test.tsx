import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CurrencySwitcher } from "./currency-switcher";

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

afterEach(() => vi.unstubAllGlobals());

describe("currency switcher", () => {
  it("shows the saved currency and a sample formatted with it", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok({ id: "u1", preferred_currency: "JPY" })));
    render(<CurrencySwitcher />);

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
    render(<CurrencySwitcher />);

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
    render(<CurrencySwitcher />);

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
    const { container } = render(<CurrencySwitcher />);

    await waitFor(() => expect(container.querySelector("section")).toBeNull());
    expect(screen.queryByLabelText("幣別")).toBeNull();
  });
});
