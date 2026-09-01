import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminNav } from "./admin-nav";

describe("AdminNav", () => {
  afterEach(() => vi.unstubAllGlobals());
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

  it("only reveals deployment center when the backend grants can_deploy", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(new Response(JSON.stringify({ can_deploy: true }), { status: 200 }))));
    render(<AdminNav current="deployments" />);
    const link = await screen.findByRole("link", { name: "部署中心" });
    expect(link.getAttribute("href")).toBe("/admin/deployments");
    expect(link.getAttribute("aria-current")).toBe("page");
  });
});
