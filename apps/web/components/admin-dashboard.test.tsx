import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminDashboard } from "./admin-dashboard";
import { api } from "@/lib/api";
vi.mock("@/lib/api", () => ({ api: vi.fn() }));
describe("domain overview", () => {
  it("shows three independent catalogs and no fabricated publication percentage", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { hotspots_total: 10, foods_total: 4, merchants_total: 6, hotels_total: 3, hotels_pending: 1, hotels_without_options: 2 }, can_deploy: false });
    render(<AdminDashboard />);
    const hotels = await screen.findByRole("region", { name: "飯店" });
    expect(within(hotels).getByText("3")).toBeTruthy();
    expect(within(hotels).getByRole("link", { name: /飯店待審/ }).getAttribute("href")).toBe("/admin/hotels?tab=review&section=products");
    const food = screen.getByRole("region", { name: "美食" });
    expect(within(food).getByText("精選店家")).toBeTruthy();
    expect(within(food).getByText("料理")).toBeTruthy();
    expect(screen.queryByText(/%/)).toBeNull();
    expect(api).toHaveBeenCalledWith("/admin/dashboard");
  });
});
