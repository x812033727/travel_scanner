import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MobileNav } from "./mobile-nav";


describe("MobileNav", () => {
  it("keeps My Trips visible without opening the mobile menu", () => {
    render(<MobileNav />);
    expect(screen.getByRole("link", { name: "我的旅行" }).getAttribute("href")).toBe("/trips");
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });

  it("opens with all account routes and closes with Escape", () => {
    render(<MobileNav />);
    const trigger = screen.getByRole("button", { name: "開啟導覽選單" });
    fireEvent.click(trigger);
    expect(screen.getByRole("navigation", { name: "手機主要導覽" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "我的旅程" }).getAttribute("href")).toBe("/trips");
    expect(screen.getByRole("link", { name: "價格通知" }).getAttribute("href")).toBe("/alerts");
    expect(screen.getByRole("link", { name: "會員帳號" }).getAttribute("href")).toBe("/account");
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("navigation", { name: "手機主要導覽" })).toBeNull();
  });
});

