import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { PALETTE_STORAGE_KEY, THEME_STORAGE_KEY } from "@/lib/theme";
import { PaletteSwitcher } from "./palette-switcher";
import { ThemeProvider, useTheme } from "./theme-provider";
import { ThemeSwitcher } from "./theme-switcher";

function StateReader() {
  const { palette, resolvedTheme } = useTheme();
  return <output data-testid="shared-theme">{palette}/{resolvedTheme}</output>;
}
beforeEach(() => {
  localStorage.clear();
  document.documentElement.removeAttribute("data-palette");
  document.documentElement.dataset.themePreference = "system";
  vi.stubGlobal("matchMedia", vi.fn(() => ({ matches: false, addEventListener: vi.fn(), removeEventListener: vi.fn() })));
});
function display() {
  return render(<ThemeProvider><ThemeSwitcher /><PaletteSwitcher /><StateReader /></ThemeProvider>);
}
describe("PaletteSwitcher", () => {
  it("restores a palette independently of the old mode key and synchronises consumers", async () => {
    localStorage.setItem(THEME_STORAGE_KEY, "dark");
    localStorage.setItem(PALETTE_STORAGE_KEY, "lagoon");
    display();
    const lagoon = screen.getByRole("radio", { name: "海島藍" }) as HTMLInputElement;
    await waitFor(() => expect(lagoon.checked).toBe(true));
    expect(document.documentElement.dataset.palette).toBe("lagoon");
    expect(screen.getByTestId("shared-theme").textContent).toBe("lagoon/dark");
    fireEvent.click(screen.getByRole("radio", { name: "森旅綠" }));
    expect(localStorage.getItem(PALETTE_STORAGE_KEY)).toBe("forest");
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe("dark");
    expect(screen.getByTestId("shared-theme").textContent).toBe("forest/dark");
    fireEvent.change(screen.getByRole("combobox", { name: "外觀主題" }), { target: { value: "light" } });
    expect(screen.getByTestId("shared-theme").textContent).toBe("forest/light");
    expect(document.querySelectorAll('[data-preview-theme="light"]')).toHaveLength(3);
  });
  it("handles cross-tab palette/mode changes and clearing storage without a reload", async () => {
    display();
    await waitFor(() => expect((screen.getByRole("group", { name: "全站配色" }) as HTMLFieldSetElement).disabled).toBe(false));
    act(() => {
      window.dispatchEvent(new StorageEvent("storage", { key: PALETTE_STORAGE_KEY, newValue: "forest" }));
      window.dispatchEvent(new StorageEvent("storage", { key: THEME_STORAGE_KEY, newValue: "dark" }));
    });
    expect(screen.getByTestId("shared-theme").textContent).toBe("forest/dark");
    act(() => window.dispatchEvent(new StorageEvent("storage", { key: null })));
    expect(screen.getByTestId("shared-theme").textContent).toBe("mocha/light");
  });
  it("ignores invalid persisted palettes and still works with storage unavailable", async () => {
    localStorage.setItem(PALETTE_STORAGE_KEY, "unknown");
    display();
    await waitFor(() => expect(document.documentElement.dataset.palette).toBe("mocha"));
    const write = vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => { throw new Error("blocked"); });
    fireEvent.click(screen.getByRole("radio", { name: "海島藍" }));
    expect(screen.getByTestId("shared-theme").textContent).toBe("lagoon/light");
    write.mockRestore();
  });
});
