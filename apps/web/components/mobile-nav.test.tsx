import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderSessionProvider } from "./header-session";
import { MobileNav } from "./mobile-nav";

afterEach(() => vi.unstubAllGlobals());

describe("MobileNav", () => {
  it("keeps compact language and sign-in controls in the top bar", () => {
    render(<MobileNav />);
    expect(screen.getByRole("combobox", { name: "語言" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Sign in" }).getAttribute("href")).toBe("/login");
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });

  it("links to the account after authentication", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "user-1", email: "user@example.com" }), { status: 200 })));
    render(<HeaderSessionProvider><MobileNav /></HeaderSessionProvider>);
    expect((await screen.findByRole("link", { name: "Account" })).getAttribute("href")).toBe("/account");
  });
});
