import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { HeaderSessionProvider } from "./header-session";
import { MobileNav } from "./mobile-nav";
import { SiteVisibilityProvider } from "./site-visibility-provider";
import { closedSiteVisibility } from "@/lib/site-features";

afterEach(() => vi.unstubAllGlobals());

describe("MobileNav", () => {
  it("keeps My Trips visible without opening the mobile menu", () => {
    render(<MobileNav />);
    expect(screen.getByRole("link", { name: "我的旅行" }).getAttribute("href")).toBe("/trips");
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });

  it("opens with all account routes and closes with Escape", () => {
    render(<MobileNav />);
    const trigger = screen.getByRole("button", { name: "開啟導覽選單" });
    fireEvent.click(trigger);
    expect(screen.getByRole("navigation", { name: "手機主要導覽" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "我的旅程" }).getAttribute("href")).toBe("/trips");
    expect(screen.getByRole("link", { name: "熱門景點" }).getAttribute("href")).toBe("/hotspots");
    expect(screen.getByRole("link", { name: "價格通知" }).getAttribute("href")).toBe("/alerts");
    expect(screen.getByRole("link", { name: "會員帳號" }).getAttribute("href")).toBe("/account");
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });

  it("shows the admin entry for an effective administrator", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      id: "admin-1",
      email: "admin@example.com",
      is_admin: true,
    }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<HeaderSessionProvider><MobileNav /></HeaderSessionProvider>);
    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));
    expect((await screen.findByRole("link", { name: "管理後台" })).getAttribute("href")).toBe("/admin/users");
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("hides controlled mobile links and the trips shortcut in conservative mode", () => {
    render(
      <SiteVisibilityProvider state={{ status: "unavailable", features: closedSiteVisibility }}>
        <MobileNav />
      </SiteVisibilityProvider>,
    );
    expect(screen.queryByRole("link", { name: "我的旅行" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "開啟導覽選單" }));
    expect(screen.queryByRole("link", { name: "熱門景點" })).toBeNull();
    expect(screen.queryByRole("link", { name: "價格通知" })).toBeNull();
    expect(screen.getByRole("link", { name: "會員帳號" })).toBeTruthy();
  });
});
