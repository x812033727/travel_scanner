import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { AccountConfirmation } from "./accounts";
import type { AnchorHTMLAttributes } from "react";

const mock = vi.hoisted(() => ({ api: vi.fn(), clearSession: vi.fn(), setUser: vi.fn(), refresh: vi.fn(),
  replace: vi.fn(), routerRefresh: vi.fn() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: { id: "member", email: "member@example.com" },
  setUser: mock.setUser, clearSession: mock.clearSession }) }));
vi.mock("./provider", () => ({ useCommunity: () => ({ refresh: mock.refresh }) }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: AnchorHTMLAttributes<HTMLAnchorElement>) => <a href={href} {...props}>{children}</a>,
  useRouter: () => ({ replace: mock.replace, refresh: mock.routerRefresh }) }));

beforeEach(() => {
  vi.clearAllMocks(); mock.api.mockResolvedValue({});
  window.history.replaceState(null, "", "/account/confirm#token=one-time-test-token");
});
afterEach(() => { cleanup(); window.history.replaceState(null, "", "/"); });

it.each(["reset", "delete"])("clears private client state after successful %s and removes the URL token", async (purpose) => {
  render(<AccountConfirmation purpose={purpose} />);
  expect(window.location.hash).toBe("");
  if (purpose === "reset") fireEvent.change(screen.getByLabelText("新密碼"), { target: { value: "new-password-for-test" } });
  else fireEvent.change(screen.getByLabelText("輸入 DELETE 確認刪除"), { target: { value: "DELETE" } });
  fireEvent.click(screen.getByRole("button", { name: "確認" }));
  await waitFor(() => expect(mock.clearSession).toHaveBeenCalledTimes(1));
  expect(mock.replace).toHaveBeenCalledWith("/login");
  expect(mock.clearSession.mock.invocationCallOrder[0]).toBeLessThan(mock.replace.mock.invocationCallOrder[0]);
  expect(JSON.parse(mock.api.mock.calls[0][1].body).token).toBe("one-time-test-token");
});

it("keeps an active session intact on a rejected confirmation", async () => {
  mock.api.mockRejectedValue(new Error("expired"));
  render(<AccountConfirmation purpose="delete" />);
  fireEvent.change(screen.getByLabelText("輸入 DELETE 確認刪除"), { target: { value: "DELETE" } });
  fireEvent.click(screen.getByRole("button", { name: "確認" }));
  await screen.findByRole("alert");
  expect(mock.clearSession).not.toHaveBeenCalled();
  expect(mock.replace).not.toHaveBeenCalled();
});

it("refreshes verified account capabilities without signing out", async () => {
  render(<AccountConfirmation purpose="verify" />);
  fireEvent.click(screen.getByRole("button", { name: "確認" }));
  await screen.findByText(/已完成帳號操作/);
  expect(mock.setUser).toHaveBeenCalledWith(expect.objectContaining({ email_verified: true }));
  expect(mock.refresh).toHaveBeenCalledTimes(1);
  expect(mock.clearSession).not.toHaveBeenCalled();
});
