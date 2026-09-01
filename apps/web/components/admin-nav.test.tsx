import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AdminNav } from "./admin-nav";

describe("AdminNav", () => {
  it("places system settings between members and provider settings", () => {
    render(<AdminNav current="system" />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual([
      "會員與次數",
      "系統設定",
      "API 與金鑰",
      "景點候選審核",
    ]);
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      "/admin/users",
      "/admin/system-settings",
      "/admin/settings",
      "/admin/hotspots",
    ]);
    expect(screen.getByRole("link", { name: "系統設定" }).getAttribute("aria-current")).toBe("page");
  });
});
