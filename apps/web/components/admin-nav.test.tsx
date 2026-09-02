import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminNav } from "./admin-nav";

describe("AdminNav", () => {
  afterEach(() => vi.unstubAllGlobals());
  it("groups analytics and daily content work ahead of configuration", () => {
    render(<AdminNav current="system" />);
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual([
      "營運總覽",
      "流量與分析",
      "會員與次數",
      "景點候選審核",
      "美食目錄管理",
      "方案與扣次",
      "版面管理",
      "系統設定",
      "API 與金鑰",
    ]);
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      "/admin",
      "/admin/analytics",
      "/admin/users",
      "/admin/hotspots",
      "/admin/foods",
      "/admin/usage-settings",
      "/admin/layout-settings",
      "/admin/system-settings",
      "/admin/settings",
    ]);
    expect(
      screen
        .getByRole("link", { name: "系統設定" })
        .getAttribute("aria-current"),
    ).toBe("page");
  });

  it("only reveals deployment center when the backend grants can_deploy", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() =>
        Promise.resolve(
          new Response(JSON.stringify({ can_deploy: true }), { status: 200 }),
        ),
      ),
    );
    render(<AdminNav current="deployments" />);
    const link = await screen.findByRole("link", { name: "部署中心" });
    expect(link.getAttribute("href")).toBe("/admin/deployments");
    expect(link.getAttribute("aria-current")).toBe("page");
  });

  it("filters admin destinations without navigating away", () => {
    render(<AdminNav current="hotspots" />);
    fireEvent.change(screen.getByRole("searchbox", { name: "搜尋後台功能" }), {
      target: { value: "景點" },
    });
    expect(screen.getAllByRole("link").map((link) => link.textContent)).toEqual(
      ["景點候選審核"],
    );
  });
});
