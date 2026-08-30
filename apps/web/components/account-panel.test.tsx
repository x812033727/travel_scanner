import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AccountPanel } from "./account-panel";

const me = { id: "u1", email: "user@example.com", plan: "PRO" };
const usage = { plan: "PRO", credits_remaining: 180, monthly_credits: 200, period_start: "2026-08-01", period_end: "2026-09-01" };

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

function stubApi(responses: Record<string, unknown>) {
  return vi.fn(async (url: string) => {
    for (const [suffix, payload] of Object.entries(responses)) {
      if (url.endsWith(suffix)) return ok(payload);
    }
    return { ok: false, status: 404, json: async () => ({ detail: "not found" }) };
  });
}

afterEach(() => vi.unstubAllGlobals());

describe("account panel", () => {
  it("shows account info and credit usage", async () => {
    vi.stubGlobal("fetch", stubApi({ "/auth/me": me, "/usage": usage }));
    render(<AccountPanel />);
    expect(await screen.findByText("user@example.com")).toBeTruthy();
    expect(screen.getByText("PRO")).toBeTruthy();
    expect(await screen.findByText("180 / 200")).toBeTruthy();
  });

  it("asks the visitor to sign in when unauthenticated", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ detail: "請先登入" }) }));
    render(<AccountPanel />);
    expect(await screen.findByRole("link", { name: "登入" })).toBeTruthy();
  });

  it("rejects mismatched new passwords without calling the API", async () => {
    const fetchMock = stubApi({ "/auth/me": me, "/usage": usage });
    vi.stubGlobal("fetch", fetchMock);
    render(<AccountPanel />);
    await screen.findByText("user@example.com");
    fireEvent.change(screen.getByLabelText(/目前密碼/), { target: { value: "old-password-1" } });
    fireEvent.change(screen.getByLabelText(/^新密碼/), { target: { value: "new-password-12" } });
    fireEvent.change(screen.getByLabelText(/確認新密碼/), { target: { value: "different-pw-12" } });
    fireEvent.click(screen.getByRole("button", { name: "更新密碼" }));
    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalledWith(expect.stringContaining("change-password"), expect.anything());
  });

  it("submits a password change and reports success", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      if (url.endsWith("/auth/me")) return ok(me);
      if (url.endsWith("/usage")) return ok(usage);
      if (url.endsWith("/auth/change-password") && init?.method === "POST") return { ok: true, status: 204, json: async () => null };
      return { ok: false, status: 404, json: async () => ({ detail: "not found" }) };
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AccountPanel />);
    await screen.findByText("user@example.com");
    fireEvent.change(screen.getByLabelText(/目前密碼/), { target: { value: "old-password-1" } });
    fireEvent.change(screen.getByLabelText(/^新密碼/), { target: { value: "new-password-12" } });
    fireEvent.change(screen.getByLabelText(/確認新密碼/), { target: { value: "new-password-12" } });
    fireEvent.click(screen.getByRole("button", { name: "更新密碼" }));
    expect(await screen.findByRole("status")).toBeTruthy();
    await waitFor(() => {
      const call = fetchMock.mock.calls.find(([url]) => (url as string).endsWith("/auth/change-password"));
      expect(call).toBeTruthy();
      expect(JSON.parse((call?.[1] as RequestInit).body as string)).toEqual({ current_password: "old-password-1", new_password: "new-password-12" });
    });
  });
});
