import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { LanguageSwitcher } from "./language-switcher";

const mocks = vi.hoisted(() => ({ replace: vi.fn(), api: vi.fn(), guard: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({ usePathname: () => "/trips/fixture", useRouter: () => ({ replace: mocks.replace }) }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams("view=map&content=hotel%3Afixture") }));
vi.mock("@/lib/api", async (original) => ({ ...await original<object>(), api: mocks.api }));
vi.mock("@/lib/navigation-guard", () => ({ requestNavigation: mocks.guard }));
beforeEach(() => { mocks.replace.mockReset(); mocks.api.mockReset().mockResolvedValue({}); mocks.guard.mockReset(); window.sessionStorage.clear(); });

describe("LanguageSwitcher draft protection", () => {
  it("does not change locale, storage or account until leaving is allowed", async () => {
    let proceed: (() => void) | undefined;
    mocks.guard.mockImplementation((run: () => void) => { proceed = run; return false; });
    render(<LanguageSwitcher compact />);
    fireEvent.change(screen.getByRole("combobox", { name: "語言" }), { target: { value: "en" } });
    expect(mocks.replace).not.toHaveBeenCalled(); expect(mocks.api).not.toHaveBeenCalled();
    expect(window.sessionStorage.getItem("travel-locale-picked")).toBeNull();
    proceed?.();
    await waitFor(() => expect(mocks.api).toHaveBeenCalledOnce());
    expect(mocks.replace).toHaveBeenCalledWith("/trips/fixture?view=map&content=hotel%3Afixture", { locale: "en" });
  });

  it("does nothing when the current locale is chosen", () => {
    render(<LanguageSwitcher />); fireEvent.change(screen.getByRole("combobox", { name: "語言" }), { target: { value: "zh-TW" } });
    expect(mocks.guard).not.toHaveBeenCalled(); expect(mocks.api).not.toHaveBeenCalled();
  });
});
