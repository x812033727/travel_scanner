import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
const { config, incoming, original, redirect } = vi.hoisted(() => ({ config: vi.fn(), incoming: vi.fn(), original: vi.fn(), redirect: vi.fn((url: string) => { throw new Error(`redirect:${url}`); }) }));
vi.mock("@/lib/stay22-script.server", () => ({ getStay22ScriptConfig: config }));
vi.mock("next/headers", () => ({ headers: incoming }));
vi.mock("next-intl", () => ({ hasLocale: (locales: string[], locale: string) => locales.includes(locale) }));
vi.mock("next/navigation", () => ({ redirect, notFound: () => { throw new Error("not found"); } }));
vi.mock("@/app/[locale]/layout", () => ({ default: original, generateMetadata: vi.fn(), generateStaticParams: vi.fn() }));
vi.mock("@/components/stay22-script", () => ({ Stay22Script: () => <span data-testid="official-script" /> }));
import PublicLayout from "./layout";
import { disabledStay22Script } from "@/lib/stay22-script";
const STAY22_SCRIPT_LMA_ID = "6aa15a455ff1d17f658d1692";

describe("separate public document root", () => {
  beforeEach(() => {
    config.mockResolvedValue({ enabled: true, integration_mode: "script", lma_id: STAY22_SCRIPT_LMA_ID });
    incoming.mockResolvedValue(new Headers({ "x-travel-pathname": "/zh-TW/destinations/tokyo/services" }));
    original.mockImplementation(({ children }) => <div data-testid="original-layout">{children}</div>);
    vi.clearAllMocks();
  });
  it("has a plain document shell without executing the private provider layout", async () => {
    const result = await PublicLayout({ children: <p>Public hotels</p>, params: Promise.resolve({ locale: "zh-TW" }) });
    // Render the body rather than nesting a second html element in jsdom's body.
    const body = (result.props.children as React.ReactElement<{ children: React.ReactNode }>[])[1];
    render(body.props.children);
    expect(original).not.toHaveBeenCalled();
    expect(screen.getByTestId("official-script")).toBeTruthy();
    expect(screen.getByRole("link", { name: "我的旅行" })).toHaveAttribute("href", "/zh-TW/trips");
    expect(document.querySelectorAll("form,input,iframe")).toHaveLength(0);
  });
  it("uses original page providers when disabled", async () => {
    config.mockResolvedValue(disabledStay22Script);
    render(await PublicLayout({ children: <p>Original page</p>, params: Promise.resolve({ locale: "zh-TW" }) }));
    expect(original).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("original-layout")).toBeTruthy();
    expect(screen.queryByTestId("official-script")).toBeNull();
  });
  it("strips URL conditions before exposing a script document", async () => {
    incoming.mockResolvedValue(new Headers({ "x-travel-pathname": "/zh-TW/destinations/tokyo/services?start_date=2027-01-01&trip_id=private" }));
    await expect(PublicLayout({ children: <p>Private query not displayed</p>, params: Promise.resolve({ locale: "zh-TW" }) })).rejects.toThrow("redirect:/zh-TW/destinations/tokyo/services");
    expect(original).not.toHaveBeenCalled();
  });
});
