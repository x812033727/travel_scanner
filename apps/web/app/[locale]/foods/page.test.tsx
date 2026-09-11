import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import FoodsPage from "./page";

const load = vi.hoisted(() => vi.fn().mockResolvedValue({ cities: null, categories: null, merchants: { items: [] } }));
vi.mock("@/lib/foods.server", () => ({ getInitialFoods: load }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/components/explore-switch", () => ({ ExploreSwitch: () => null }));
vi.mock("@/components/food-browser", () => ({
  FoodBrowser: ({ initialFilters }: { initialFilters: unknown }) => <output>{JSON.stringify(initialFilters)}</output>,
}));

describe("foods SSR filter identity", () => {
  it("uses matching normalized filters for both the API and first-rendered controls", async () => {
    const expected = { destinationId: "tokyo", area: "shibuya", category: "ramen", style: "artsy", query: "tea & cakes" };
    render(await FoodsPage({
      params: Promise.resolve({ locale: "en" }),
      searchParams: Promise.resolve({ destination_id: [" tokyo ", "seoul"], area: "shibuya", category: "ramen", style: "artsy", q: " tea & cakes ", unused: "ignore" }),
    }));
    expect(load).toHaveBeenCalledWith("en", expected);
    expect(screen.getByRole("status").textContent).toBe(JSON.stringify(expected));
  });
});
