import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderSessionProvider } from "./header-session";
import { MobileNav } from "./mobile-nav";
import { ThemeProvider } from "./theme-provider";

afterEach(() => vi.unstubAllGlobals());

describe("MobileNav", () => {
  it("keeps compact language and sign-in controls in the top bar", () => {
    render(<ThemeProvider><MobileNav /></ThemeProvider>);
    expect(screen.getByRole("combobox", { name: "外觀主題" })).toBeTruthy();
    expect(screen.getByRole("combobox", { name: "語言" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "登入／切換帳號" }).getAttribute("href")).toBe("/login");
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });

  it("links to the account after authentication", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "user-1", email: "user@example.com" }), { status: 200 })));
    render(<ThemeProvider><HeaderSessionProvider><MobileNav /></HeaderSessionProvider></ThemeProvider>);
    expect((await screen.findByRole("link", { name: "會員帳號" })).getAttribute("href")).toBe("/account");
    expect(screen.queryByRole("link", { name: "管理後台" })).toBeNull();
  });

  it("gives an administrator a way into the control centre", async () => {
    // The desktop nav that carries this link is hidden below md, so without it an
    // administrator on a phone has to type the URL by hand.
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "user-1", email: "admin@example.com", is_admin: true }), { status: 200 })));
    render(<ThemeProvider><HeaderSessionProvider><MobileNav /></HeaderSessionProvider></ThemeProvider>);
    expect((await screen.findByRole("link", { name: "管理後台" })).getAttribute("href")).toBe("/admin");
  });

  it("opens a full menu with the destinations the tab bar cannot hold", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "signed out" }), { status: 401 })));
    render(<ThemeProvider><HeaderSessionProvider><MobileNav /></HeaderSessionProvider></ThemeProvider>);

    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));

    const menu = screen.getByRole("dialog");
    // 航班動態 and 航空票價 have no other mobile entry point at all.
    expect(within(menu).getByRole("link", { name: "航班動態" })).toBeTruthy();
    expect(within(menu).getByRole("link", { name: "航空票價" })).toBeTruthy();
    expect(within(menu).getByRole("link", { name: "方案" })).toBeTruthy();

    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
  });
});
