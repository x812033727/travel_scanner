import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import PricingPage from "./page";

const registrationState = vi.hoisted(() => ({ value: "open" as "open" | "closed" | "unavailable" }));

vi.mock("@/lib/registration", () => ({
  getRegistrationAvailability: () => Promise.resolve(registrationState.value),
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/pricing",
  useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }),
}));

afterEach(() => vi.unstubAllGlobals());

describe("usage-pack pricing", () => {
  beforeEach(() => { registrationState.value = "open"; });

  it("shows one-time, non-expiring packages and disabled purchase actions", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(await PricingPage());

    expect(screen.getByRole("heading", { name: /不綁月租的旅遊查價次數/ })).toBeTruthy();
    expect(screen.getByText(/註冊先送 3 次/)).toBeTruthy();
    expect(screen.getByText("NT$199")).toBeTruthy();
    expect(screen.getByText("NT$499")).toBeTruthy();
    expect(screen.getByText("NT$1,299")).toBeTruthy();
    expect(screen.getAllByText(/次數永久有效並可累加/)).toHaveLength(3);
    expect(screen.getAllByRole("button", { name: "購買即將開放" })).toHaveLength(3);
    expect(screen.queryByText(/每月.*(?:次|credit)/i)).toBeNull();
  });

  it("replaces the free registration link when registration is closed", async () => {
    registrationState.value = "closed";
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(await PricingPage());

    expect(screen.getByText("目前暫停開放註冊")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "免費取得 3 次" })).toBeNull();
  });

  it("does not expose registration when status cannot be confirmed", async () => {
    registrationState.value = "unavailable";
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(await PricingPage());

    expect(screen.getByText("暫時無法確認註冊狀態")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "免費取得 3 次" })).toBeNull();
  });
});
