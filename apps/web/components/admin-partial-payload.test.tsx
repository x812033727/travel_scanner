import { render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminDashboard } from "./admin-dashboard";
import { AdminFoodAreasPanel } from "./admin-food-taxonomy-panel";

afterEach(() => vi.unstubAllGlobals());

/**
 * A degraded API answer must degrade the page, not delete it.
 *
 * These panels read `data?.items.map(...)` and `data.counts.x`, where the
 * optional chain guards only the outer object — a payload without `items` or
 * `counts` threw inside render, and React replaced the whole admin page with a
 * blank screen (a red overlay in dev).
 */
describe("admin panels against a partial payload", () => {
  it("keeps the dashboard on screen when counts are missing", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ({ ok: true, status: 200, json: async () => ({}) })));

    expect(() => render(<AdminDashboard />)).not.toThrow();

    await waitFor(() => expect(vi.mocked(fetch)).toHaveBeenCalled());
    // Each domain remains usable and missing counts are unknown, not false zeros.
    for (const [name, target] of [["景點", "hotspots"], ["美食", "foods"], ["飯店", "hotels"]]) {
      const domain = await screen.findByRole("region", { name });
      expect(within(domain).getByRole("link", { name: "進入管理" }).getAttribute("href")).toBe(`/admin/${target}`);
      expect(within(domain).getAllByText("—").length).toBeGreaterThan(0);
      expect(within(domain).queryByText("0")).toBeNull();
    }
  });

  it("retains every pending content count and its domain-specific review queue", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({
        ok: true,
        status: 200,
        json: async () => ({
          counts: {
            users: 1,
            hotspots_public: 984,
            foods_public: 87,
            hotspots_pending: 124,
            foods_pending: 13,
            merchants_pending: 245,
            guides_pending: 427,
            hotels_pending: 7,
          },
          quick_actions: [
            { id: "review_hotspots", href: "/admin/hotspots", count_key: "hotspots_pending" },
            { id: "review_foods", href: "/admin/foods#dishes", count_key: "foods_pending" },
            { id: "review_merchants", href: "/admin/foods#merchants", count_key: "merchants_pending" },
            { id: "review_guides", href: "/admin/hotspots#guides", count_key: "guides_pending" },
          ],
        }),
      })),
    );

    render(<AdminDashboard />);

    for (const [name, count, href] of [
      ["景點待審", "124", "/admin/hotspots?tab=review&section=manual&status=pending"],
      ["料理待審", "13", "/admin/foods?tab=review&section=dishes&status=pending"],
      ["店家待審", "245", "/admin/foods?tab=review&section=merchants&status=pending"],
      ["文章待審", "427", "/admin/hotspots?tab=content&section=guides&status=pending"],
      ["飯店待審", "7", "/admin/hotels?tab=review&section=products&status=pending"],
    ]) {
      const link = await screen.findByRole("link", { name: new RegExp(`${name}\\s*${count}$`) });
      expect(link.getAttribute("href")).toBe(href);
      expect(within(link).getByText(count)).toBeTruthy();
    }
  });

  it("keeps the taxonomy panel on screen when items are missing", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ({ ok: true, status: 200, json: async () => ({}) })));

    expect(() => render(<AdminFoodAreasPanel />)).not.toThrow();

    await waitFor(() => expect(vi.mocked(fetch)).toHaveBeenCalled());
    expect(await screen.findByRole("heading", { name: "區域（商圈）" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "新增區域" })).toBeTruthy();
    expect(within(screen.getByRole("table")).getAllByRole("columnheader")).toHaveLength(7);
    expect(screen.getByRole("table").querySelector("tbody")?.children).toHaveLength(0);
    expect(screen.queryByText(/Cannot read properties/)).toBeNull();
  });
});
