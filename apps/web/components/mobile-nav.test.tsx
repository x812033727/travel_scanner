import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderSessionProvider } from "./header-session";
import { MobileNav } from "./mobile-nav";
import { ThemeProvider } from "./theme-provider";

afterEach(() => vi.unstubAllGlobals());

describe("MobileNav", () => {
  it("keeps the top bar down to the account and the menu", () => {
    render(<ThemeProvider><MobileNav /></ThemeProvider>);
    // Appearance, language and text size are display preferences with a word
    // beside them inside the menu, not four unlabelled icons in the bar.
    expect(screen.queryByRole("combobox", { name: "外觀主題" })).toBeNull();
    expect(screen.queryByRole("combobox", { name: "語言" })).toBeNull();
    expect(screen.getByRole("link", { name: "登入／切換帳號" }).getAttribute("href")).toBe("/login");
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });

  it("gathers the display preferences in the menu, each with a label", () => {
    render(<ThemeProvider><MobileNav /></ThemeProvider>);

    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));

    const menu = screen.getByRole("dialog");
    expect(within(menu).getByRole("radiogroup", { name: "文字大小" })).toBeTruthy();
    expect(within(menu).getByRole("combobox", { name: "外觀主題" })).toBeTruthy();
    expect(within(menu).getByRole("combobox", { name: "語言" })).toBeTruthy();
    // The switchers carry the same words in a sr-only span; these are the ones a
    // reader can actually see next to the control.
    for (const label of ["外觀主題", "語言"]) {
      expect(within(menu).getAllByText(label).some((node) => !node.className.includes("sr-only"))).toBe(true);
    }
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

  it("puts the sheet on the body, out of the header's containing block", () => {
    render(<ThemeProvider><MobileNav /></ThemeProvider>);

    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));

    // The header paints with backdrop-filter, which makes it the containing block
    // for fixed descendants: rendered in place, the whole sheet was laid out
    // inside a 68px strip and only its last row was on screen.
    const dialog = screen.getByRole("dialog");
    const overlay = dialog.parentElement;
    expect(overlay?.parentElement).toBe(document.body);
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
