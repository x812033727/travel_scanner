import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderSessionProvider, useHeaderSession } from "./header-session";
import { SavedItemsProvider, useSavedItems } from "./saved-items-provider";

vi.mock("@/i18n/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), refresh: vi.fn(), replace: vi.fn() }),
  usePathname: () => "/account",
}));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams() }));

function SavedStatus() {
  return <p>saved:{useSavedItems().status}</p>;
}

function SessionStatus() {
  return <p>session:{useHeaderSession().status}</p>;
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.clearAllMocks();
});

describe("session providers without a session cookie", () => {
  it("asks nothing, and says signed out straight away", async () => {
    // The parameter is declared so `mock.calls` is typed, and echoed so it is used.
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL) =>
        new Response(JSON.stringify({ detail: String(input) }), { status: 401 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(
      <HeaderSessionProvider hasSession={false}>
        <SavedItemsProvider hasSession={false}>
          <SessionStatus />
          <SavedStatus />
        </SavedItemsProvider>
      </HeaderSessionProvider>,
    );

    // Both used to learn this by sending a request that could only come back 401, on
    // every page a signed-out reader opened.
    expect(screen.getByText("session:signed_out")).toBeTruthy();
    expect(screen.getByText("saved:signed_out")).toBeTruthy();
    await waitFor(() => expect(fetchMock).not.toHaveBeenCalled());
  });

  it("still verifies a cookie that is present, because it may be expired", async () => {
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL) =>
        new Response(JSON.stringify({ detail: String(input) }), { status: 401 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(
      <HeaderSessionProvider hasSession>
        <SavedItemsProvider hasSession>
          <SessionStatus />
          <SavedStatus />
        </SavedItemsProvider>
      </HeaderSessionProvider>,
    );

    await waitFor(() => expect(screen.getByText("session:signed_out")).toBeTruthy());
    await waitFor(() => expect(screen.getByText("saved:signed_out")).toBeTruthy());
    const asked = fetchMock.mock.calls.map(([input]) => String(input));
    expect(asked.some((url) => url.includes("/auth/me"))).toBe(true);
    expect(asked.some((url) => url.includes("/saved-items"))).toBe(true);
  });
});
