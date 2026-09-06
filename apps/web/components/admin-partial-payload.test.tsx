import { render, screen, waitFor } from "@testing-library/react";
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
    // The page still renders; before the guard React unmounted the whole subtree.
    expect((await screen.findAllByText(/待審|營運|摘要|載入/)).length).toBeGreaterThan(0);
  });

  it("keeps the taxonomy panel on screen when items are missing", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ({ ok: true, status: 200, json: async () => ({}) })));

    expect(() => render(<AdminFoodAreasPanel />)).not.toThrow();

    await waitFor(() => expect(vi.mocked(fetch)).toHaveBeenCalled());
    expect(screen.queryByText(/Cannot read properties/)).toBeNull();
  });
});
