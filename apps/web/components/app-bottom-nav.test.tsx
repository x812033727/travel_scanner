import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppBottomNav } from "./app-bottom-nav";

describe("AppBottomNav", () => {
  it("provides the five thumb-friendly app destinations", () => {
    render(<AppBottomNav />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual(["探索", "規劃", "旅程", "通知", "我的"]);
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      "/hotspots", "/#trip-search", "/trips", "/alerts", "/account",
    ]);
    for (const link of links) expect(link.className).toContain("app-bottom-nav-item");
  });
});
