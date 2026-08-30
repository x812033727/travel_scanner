import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import PricingPage from "./page";

vi.mock("next/navigation", () => ({
  usePathname: () => "/pricing",
  useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }),
}));

afterEach(() => vi.unstubAllGlobals());

describe("usage-pack pricing", () => {
  it("shows one-time, non-expiring packages and disabled purchase actions", () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(<PricingPage />);

    expect(screen.getByRole("heading", { name: /不綁月租的旅遊查價次數/ })).toBeTruthy();
    expect(screen.getByText(/註冊先送 3 次/)).toBeTruthy();
    expect(screen.getByText("NT$199")).toBeTruthy();
    expect(screen.getByText("NT$499")).toBeTruthy();
    expect(screen.getByText("NT$1,299")).toBeTruthy();
    expect(screen.getAllByText(/次數永久有效並可累加/)).toHaveLength(3);
    expect(screen.getAllByRole("button", { name: "購買即將開放" })).toHaveLength(3);
    expect(screen.queryByText(/每月.*(?:次|credit)/i)).toBeNull();
  });
});
