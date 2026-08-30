import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AirbnbSearchPanel, buildAirbnbSearchUrl } from "./airbnb-search-panel";

const criteria = {
  location: "新宿, 東京, 日本",
  checkIn: "2026-11-10",
  checkOut: "2026-11-15",
  adults: 2,
  children: 1,
};

describe("AirbnbSearchPanel", () => {
  it("builds an official Airbnb search with dates and guest counts", () => {
    const url = new URL(buildAirbnbSearchUrl(criteria));
    expect(url.origin).toBe("https://www.airbnb.com");
    expect(decodeURIComponent(url.pathname)).toBe("/s/新宿, 東京, 日本/homes");
    expect(url.searchParams.get("checkin")).toBe("2026-11-10");
    expect(url.searchParams.get("checkout")).toBe("2026-11-15");
    expect(url.searchParams.get("adults")).toBe("2");
    expect(url.searchParams.get("children")).toBe("1");
  });

  it("labels the result as an external search instead of a live quote", () => {
    render(<AirbnbSearchPanel criteria={criteria} />);
    expect(screen.getByText(/不擷取 Airbnb 報價/)).toBeTruthy();
    expect(screen.getByText(/此入口不扣 Travel Scanner 搜尋次數/)).toBeTruthy();
    expect(screen.getByRole("link", { name: /前往 Airbnb 搜尋/ }).getAttribute("href")).toContain("airbnb.com");
  });
});
