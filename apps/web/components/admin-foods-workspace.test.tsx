import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminFoodsWorkspace } from "./admin-foods-workspace";

function stubFetch() {
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/foods/cities")) {
        return new Response(JSON.stringify({ total_merchants: 0, countries: [] }));
      }
      return new Response(JSON.stringify({ items: [], total: 0, page: 1, pages: 0 }));
    }),
  );
}

describe("AdminFoodsWorkspace", () => {
  it("opens the merchants tab by default", async () => {
    stubFetch();
    window.history.replaceState({}, "", "/admin/foods");
    render(<AdminFoodsWorkspace />);

    expect(await screen.findByRole("tab", { name: "店家", selected: true })).toBeTruthy();
    expect(
      await screen.findByRole("heading", { name: "店家、地圖識別與永久座標" }),
    ).toBeTruthy();
  });

  it("opens the areas and cuisines tab from the URL", async () => {
    stubFetch();
    window.history.replaceState({}, "", "/admin/foods?tab=taxonomy");
    render(<AdminFoodsWorkspace />);

    expect(await screen.findByRole("heading", { name: "區域（商圈）" })).toBeTruthy();
    expect(await screen.findByRole("heading", { name: "美食分類" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "區域與分類", selected: true })).toBeTruthy();
  });
});
