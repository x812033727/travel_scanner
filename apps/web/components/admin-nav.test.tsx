import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AdminBootstrap, AdminNavigationItem } from "@/lib/admin-operations";
import { AdminNav } from "./admin-nav";
import { AdminOperationsProvider } from "./admin-operations-provider";

function bootstrap(navigation: AdminNavigationItem[], overrides: Partial<AdminBootstrap> = {}): AdminBootstrap {
  return {
    user: { id: "admin", email: "admin@example.com" },
    admin_roles: ["viewer"],
    admin_capabilities: ["admin.access", "dashboard.read"],
    navigation,
    pending_counts: {},
    system_status: {},
    environment: "test",
    can_deploy: false,
    can_manage_database: false,
    ...overrides,
  };
}

function renderNav(value: AdminBootstrap, current = "dashboard") {
  return render(<AdminOperationsProvider bootstrap={value}><AdminNav current={current} /></AdminOperationsProvider>);
}

describe("AdminNav", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("renders only the destinations granted by backend navigation", () => {
    renderNav(bootstrap([
      { key: "dashboard", href: "/admin", group: "overview" },
      { key: "hotspots", href: "/admin/hotspots", group: "content" },
      { key: "users", href: "/admin/users", group: "operations" },
    ]));
    expect(screen.getByRole("img", { name: "Mokaair" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "營運總覽" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "景點" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "使用者" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "資料庫" })).toBeNull();
  });

  it("marks the current destination and preserves backend labels", () => {
    renderNav(bootstrap([
      { key: "dashboard", href: "/admin", group: "overview" },
      { key: "system", label: "系統控制", href: "/admin/system-settings", group: "system" },
      { key: "providers", href: "/admin/settings", group: "system" },
    ]), "system");
    expect(screen.getByRole("link", { name: "系統控制" }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("link", { name: "Provider 與金鑰" })).toBeTruthy();
  });

  it("only reveals deployment center when backend navigation grants it", () => {
    const value = bootstrap([
      { key: "dashboard", href: "/admin", group: "overview" },
      { key: "deployments", href: "/admin/deployments", group: "system" },
    ], { can_deploy: true, admin_capabilities: ["admin.access", "deploy.read", "deploy.execute"] });
    renderNav(value, "deployments");
    const link = screen.getByRole("link", { name: "部署中心" });
    expect(link.getAttribute("href")).toBe("/admin/deployments");
    expect(link.getAttribute("aria-current")).toBe("page");
  });

  it("filters the authorized navigation without revealing hidden destinations", () => {
    renderNav(bootstrap([
      { key: "dashboard", href: "/admin", group: "overview" },
      { key: "hotspots", href: "/admin/hotspots", group: "content" },
      { key: "hotels", href: "/admin/hotels", group: "content" },
    ]));
    fireEvent.change(screen.getByRole("searchbox", { name: "搜尋頁面與操作" }), { target: { value: "飯店" } });
    expect(screen.getAllByRole("link").map((link) => link.getAttribute("href"))).toEqual(["/admin", "/admin/hotels"]);
    expect(screen.queryByRole("link", { name: "景點" })).toBeNull();
  });

  it("restores focus after Escape closes the phone drawer", () => {
    renderNav(bootstrap([
      { key: "dashboard", href: "/admin", group: "overview" },
      { key: "hotspots", href: "/admin/hotspots", group: "content" },
    ]), "hotspots");
    const trigger = screen.getByRole("button", { name: "開啟營運選單" });
    trigger.focus();
    fireEvent.click(trigger);
    expect(trigger.getAttribute("aria-expanded")).toBe("true");
    expect(document.activeElement).not.toBe(trigger);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(trigger.getAttribute("aria-expanded")).toBe("false");
    expect(document.activeElement).toBe(trigger);
  });
});
