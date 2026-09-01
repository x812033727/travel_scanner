import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import PricingPage from "./page";

const registrationState = vi.hoisted(() => ({ value: "open" as "open" | "closed" | "unavailable" }));
const { defaultPackages, usageState } = vi.hoisted(() => {
  const packages = [
    { code: "PACK_10", name: "輕量包", uses: 10, price_twd: 199, display_order: 10, is_featured: false, expires: false, purchasable: false },
    { code: "PACK_30", name: "常用包", uses: 30, price_twd: 499, display_order: 20, is_featured: true, expires: false, purchasable: false },
    { code: "PACK_100", name: "大量包", uses: 100, price_twd: 1299, display_order: 30, is_featured: false, expires: false, purchasable: false },
  ];
  return {
    defaultPackages: packages,
    usageState: {
      value: {
        status: "ready" as const,
        catalog: { trial_uses: 3, packages, operation_costs: {} },
      },
    },
  };
});

vi.mock("@/lib/registration", () => ({
  getRegistrationAvailability: () => Promise.resolve(registrationState.value),
}));
vi.mock("@/lib/usage-catalog.server", () => ({
  getUsageCatalog: () => Promise.resolve(usageState.value),
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/pricing",
  useSearchParams: () => new URLSearchParams(),
  useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }),
}));

afterEach(() => vi.unstubAllGlobals());

describe("usage-pack pricing", () => {
  beforeEach(() => {
    registrationState.value = "open";
    usageState.value.catalog.packages = [...defaultPackages];
  });

  it("shows one-time, non-expiring packages and disabled purchase actions", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(await PricingPage({ params: Promise.resolve({ locale: "zh-TW" }) }));

    expect(screen.getByRole("heading", { name: /不綁月租的旅遊查價次數/ })).toBeTruthy();
    expect(screen.getByText(/註冊先送 3 次/)).toBeTruthy();
    expect(screen.getByText(/199/)).toBeTruthy();
    expect(screen.getByText(/499/)).toBeTruthy();
    expect(screen.getByText(/1,299/)).toBeTruthy();
    expect(screen.getAllByText(/次數永久有效並可累加/)).toHaveLength(3);
    expect(screen.getAllByRole("button", { name: "購買即將開放" })).toHaveLength(3);
    expect(screen.queryByText(/每月.*(?:次|credit)/i)).toBeNull();
  });

  it("replaces the free registration link when registration is closed", async () => {
    registrationState.value = "closed";
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(await PricingPage({ params: Promise.resolve({ locale: "zh-TW" }) }));

    expect(screen.getByText("目前暫停開放註冊")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "免費取得 3 次" })).toBeNull();
  });

  it("does not expose registration when status cannot be confirmed", async () => {
    registrationState.value = "unavailable";
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => undefined)));
    render(await PricingPage({ params: Promise.resolve({ locale: "zh-TW" }) }));

    expect(screen.getByText("暫時無法確認註冊狀態")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "免費取得 3 次" })).toBeNull();
  });

  it.each([
    ["zh-TW", "繁體方案"], ["zh-CN", "简体方案"], ["en", "English pack"],
    ["ja", "日本語パック"], ["ko", "한국어 팩"],
  ])("renders the localized package returned for %s", async (locale, name) => {
    usageState.value.catalog.packages = [{ ...defaultPackages[0], name }];
    render(await PricingPage({ params: Promise.resolve({ locale }) }));
    expect(screen.getByText(name)).toBeTruthy();
  });
});
