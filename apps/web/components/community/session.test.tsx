import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { HeaderSessionProvider, useHeaderSession, type HeaderUser } from "../header-session";

const mock = vi.hoisted(() => ({ api: vi.fn(), router: { push: vi.fn(), replace: vi.fn(), refresh: vi.fn() },
  query: new URLSearchParams() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("next/navigation", () => ({ useSearchParams: () => mock.query }));
vi.mock("@/i18n/navigation", () => ({ usePathname: () => "/account/confirm", useRouter: () => mock.router }));
function Controls() {
  const { status, user, clearSession, setUser } = useHeaderSession();
  return <><p>{status}:{user?.email || "no member"}</p>
    <button onClick={clearSession}>Clear</button>
    <button onClick={() => setUser({ id: "new-member", email: "new@example.com" })}>Authenticate</button></>;
}
beforeEach(() => { vi.clearAllMocks(); });
afterEach(cleanup);

it("a delayed auth lookup cannot repopulate an explicitly revoked session", async () => {
  let resolve!: (user: HeaderUser) => void;
  mock.api.mockImplementation(() => new Promise((done) => { resolve = done; }));
  render(<HeaderSessionProvider><Controls /></HeaderSessionProvider>);
  await waitFor(() => expect(mock.api).toHaveBeenCalledTimes(1));
  fireEvent.click(screen.getByRole("button", { name: "Clear" }));
  expect(screen.getByText("signed_out:no member")).toBeTruthy();
  await act(async () => { resolve({ id: "old-member", email: "private@example.com" }); });
  expect(screen.queryByText(/private@example.com/)).toBeNull();
  expect(screen.getByText("signed_out:no member")).toBeTruthy();
});

it("successful explicit authentication updates both identity and status", () => {
  render(<HeaderSessionProvider hasSession={false}><Controls /></HeaderSessionProvider>);
  fireEvent.click(screen.getByRole("button", { name: "Authenticate" }));
  expect(screen.getByText("authenticated:new@example.com")).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "Clear" }));
  expect(screen.getByText("signed_out:no member")).toBeTruthy();
  expect(mock.api).not.toHaveBeenCalled();
});
