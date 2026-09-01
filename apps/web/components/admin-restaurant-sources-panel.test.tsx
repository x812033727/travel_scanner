import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminRestaurantSourcesPanel } from "./admin-restaurant-sources-panel";

afterEach(() => vi.unstubAllGlobals());

describe("AdminRestaurantSourcesPanel", () => {
  it("shows direct-source and official-website progress by country", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL) => {
        const url = String(input);
        if (url.includes("/coverage")) {
          return new Response(
            JSON.stringify({
              items: [
                {
                  hotspot_id: "11111111-1111-4111-8111-111111111111",
                  name: "台北 101",
                  city_name: "台北",
                },
              ],
            }),
          );
        }
        return new Response(
          JSON.stringify({
            items: [],
            restaurant_places: { listed: 0, approved: 0, missing: 0 },
            food_merchants: {
              total: 155,
              destination_context: 155,
              direct_merchant_evidence: 47,
              official_website: 21,
              by_country: [
                {
                  country_code: "TW",
                  total: 32,
                  destination_context: 32,
                  direct_merchant_evidence: 14,
                  official_website: 7,
                },
                {
                  country_code: "JP",
                  total: 31,
                  destination_context: 31,
                  direct_merchant_evidence: 0,
                  official_website: 0,
                },
              ],
              disclosure: "Destination context is not merchant evidence.",
            },
          }),
        );
      }),
    );

    render(<AdminRestaurantSourcesPanel />);

    expect(await screen.findByText("台灣")).toBeTruthy();
    expect(screen.getByText("14/32")).toBeTruthy();
    expect(screen.getByText("14 家直接佐證・7 家官網")).toBeTruthy();
    expect(screen.getByText("日本")).toBeTruthy();
    expect(screen.getByText("0/31")).toBeTruthy();
  });
});
