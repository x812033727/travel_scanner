import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderAuth } from "./header-auth";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }) }));

function ok(payload: unknown) {
  return { ok: true, status: 200, json: async () => payload };
}

afterEach(() => vi.unstubAllGlobals());

describe("header auth", () => {
  it("shows the login link when the visitor is not authenticated", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ detail: "未登入" }) }));
    render(<HeaderAuth />);
    expect(await screen.findByRole("link", { name: "登入" })).toBeTruthy();
  });

  it("does not disguise a server failure as a signed-out visitor", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500, json: async () => ({ detail: "資料庫錯誤" }) }));
    render(<HeaderAuth />);
    expect((await screen.findByRole("status")).textContent).toContain("登入狀態異常");
    expect(screen.queryByRole("link", { name: "登入" })).toBeNull();
  });

  it("shows the account email and logout button when authenticated", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok({ id: "u1", email: "user@example.com" })));
    render(<HeaderAuth />);
    expect(await screen.findByRole("button", { name: "登出" })).toBeTruthy();
    expect(screen.getByText("user@example.com")).toBeTruthy();
  });

  it("shows the admin link only for administrators", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(ok({
      id: "u1", email: "admin@example.com", is_admin: true,
    })));
    render(<HeaderAuth />);
    expect((await screen.findByRole("link", { name: "管理後台" })).getAttribute("href")).toBe("/admin/settings");
  });
});
