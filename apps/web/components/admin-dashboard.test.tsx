import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminDashboard } from "./admin-dashboard";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { api } from "@/lib/api";
vi.mock("@/lib/api", () => ({ api: vi.fn() }));
describe("domain overview", () => {
  it("shows three independent catalogs and no fabricated publication percentage", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { hotspots_total: 10, foods_total: 4, merchants_total: 6, hotels_total: 3, hotels_pending: 1, hotels_without_options: 2 }, can_deploy: false });
    render(<AdminDashboard />);
    const hotels = await screen.findByRole("region", { name: "飯店" });
    expect(hotels.textContent).toContain("3");
    expect(within(hotels).getByRole("link", { name: /飯店待審/ }).getAttribute("href")).toBe("/admin/hotels?tab=review&section=products&status=pending");
    const food = screen.getByRole("region", { name: "美食" });
    expect(food.textContent).toContain("4");
    expect(screen.queryByText(/%/)).toBeNull();
    expect(api).toHaveBeenCalledWith("/admin/dashboard");
  });

  it("never links a role to dashboard destinations absent from backend navigation", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { users: 8, hotspots_total: 10 }, can_deploy: false });
    const bootstrap = {
      user: { id: "db", email: "db@example.com" }, admin_roles: ["database_operator"], admin_capabilities: ["admin.access", "dashboard.read", "database.read"],
      navigation: [{ key: "dashboard", href: "/admin", group: "overview" as const }, { key: "database", href: "/admin/database", group: "system" as const }],
      pending_counts: {}, system_status: { database: { status: "healthy" as const }, background_jobs: { status: "degraded" as const } }, environment: "test", can_deploy: false, can_manage_database: false,
    };
    render(<AdminOperationsProvider bootstrap={bootstrap}><AdminDashboard /></AdminOperationsProvider>);
    await screen.findByText("系統狀態");
    expect(screen.queryByRole("link", { name: /使用者/ })).toBeNull();
    expect(screen.queryByRole("region", { name: "景點" })).toBeNull();
    expect(screen.getByRole("link", { name: /資料庫/ }).getAttribute("href")).toBe("/admin/database");
    expect(screen.getByText("背景工作")).toBeTruthy();
    expect(screen.getByText("部分異常")).toBeTruthy();
  });
});
