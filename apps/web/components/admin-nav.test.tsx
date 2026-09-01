import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AdminNav } from "./admin-nav";

describe("AdminNav", () => {
  it("places usage management after member management", () => {
    render(<AdminNav current="system" />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual([
      "會員與次數",
      "方案與扣次",
      "系統設定",
      "版面管理",
      "API 與金鑰",
      "景點候選審核",
      "美食目錄管理",
    ]);
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      "/admin/users",
      "/admin/usage-settings",
      "/admin/system-settings",
      "/admin/layout-settings",
      "/admin/settings",
      "/admin/hotspots",
      "/admin/foods",
    ]);
    expect(screen.getByRole("link", { name: "系統設定" }).getAttribute("aria-current")).toBe("page");
  });
});
