import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminNav } from "./admin-nav";
import { HeaderSessionProvider } from "./header-session";

describe("AdminNav", () => {
  afterEach(() => vi.unstubAllGlobals());
  it("keeps only overview and the three domains primary", () => {
    render(<AdminNav current="dashboard" />);
    expect(screen.getByRole("img", { name: "Mokaair" })).toBeTruthy();
    expect(screen.getAllByRole("link").map((link) => link.textContent)).toEqual(["總覽", "景點", "美食", "飯店"]);
    expect(screen.getByRole("button", { name: "營運管理" }).getAttribute("aria-expanded")).toBe("false");
    fireEvent.click(screen.getByRole("button", { name: "營運管理" }));
    expect(screen.getByRole("link", { name: "會員與次數" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "合作夥伴" }).getAttribute("href")).toBe("/admin/partners");
    expect(screen.getByRole("link", { name: "其他旅行服務" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "營運管理" }));
    expect(screen.queryByRole("link", { name: "會員與次數" })).toBeNull();
  });
  it("expands the active system group and preserves every secondary destination", () => {
    render(<AdminNav current="system" />);
    expect(screen.getByRole("button", { name: "系統管理" }).getAttribute("aria-expanded")).toBe("true");
    expect(screen.getByRole("link", { name: "系統設定" }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("link", { name: "API 與金鑰" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "版面管理" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "部署中心" })).toBeNull();
  });
  it("only reveals deployment center when the backend grants can_deploy", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(new Response(JSON.stringify({ can_deploy: true }), { status: 200 }))));
    render(<HeaderSessionProvider><AdminNav current="deployments" /></HeaderSessionProvider>);
    const link = await screen.findByRole("link", { name: "部署中心" });
    expect(link.getAttribute("href")).toBe("/admin/deployments");
    expect(link.getAttribute("aria-current")).toBe("page");
  });
  it.each([
    ["餐廳掃描", "/admin/foods?tab=nearby&section=scans"],
    ["飯店供應模式", "/admin/hotels?tab=settings&section=providers&provider=runtime&field=hotel_provider_mode"],
  ])("finds the real child destination for %s", (query, href) => {
    render(<AdminNav current="hotspots" />);
    fireEvent.change(screen.getByRole("searchbox", { name: "搜尋後台功能" }), { target: { value: query } });
    expect(screen.getAllByRole("link").map((link) => link.getAttribute("href"))).toEqual([href]);
  });
  it("keeps AI history secondary and marks it active", () => {
    render(<AdminNav current="catalogReview" />);
    expect(screen.getByRole("link", { name: "AI 工作紀錄" }).getAttribute("aria-current")).toBe("page");
  });
  it("restores focus after Escape closes the phone drawer", () => {
    render(<AdminNav current="hotspots" />);
    const trigger = screen.getByRole("button", { name: "開啟後台選單" });
    trigger.focus();
    fireEvent.click(trigger);
    expect(document.activeElement).toBe(screen.getByRole("searchbox"));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(trigger.getAttribute("aria-expanded")).toBe("false");
    expect(document.activeElement).toBe(trigger);
  });
});
