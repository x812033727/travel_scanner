import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { THEME_STORAGE_KEY } from "@/lib/theme";
import { ThemeProvider } from "./theme-provider";
import { ThemeSwitcher } from "./theme-switcher";

function mockColorScheme(initialMatches: boolean) {
  let matches = initialMatches;
  const listeners = new Set<(event: MediaQueryListEvent) => void>();
  const media = {
    get matches() {
      return matches;
    },
    media: "(prefers-color-scheme: dark)",
    onchange: null,
    addEventListener: (_type: string, listener: (event: MediaQueryListEvent) => void) => listeners.add(listener),
    removeEventListener: (_type: string, listener: (event: MediaQueryListEvent) => void) => listeners.delete(listener),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
  } as MediaQueryList;
  vi.stubGlobal("matchMedia", vi.fn(() => media));
  return (next: boolean) => {
    matches = next;
    listeners.forEach((listener) => listener({ matches: next, media: media.media } as MediaQueryListEvent));
  };
}

beforeEach(() => {
  localStorage.clear();
  document.documentElement.removeAttribute("data-theme");
  document.documentElement.dataset.themePreference = "system";
  document.documentElement.style.colorScheme = "";
});

describe("ThemeSwitcher", () => {
  it("restores and persists an explicit theme", async () => {
    mockColorScheme(false);
    localStorage.setItem(THEME_STORAGE_KEY, "dark");
    render(<ThemeProvider><ThemeSwitcher /></ThemeProvider>);

    const select = screen.getByRole("combobox", { name: "外觀主題" });
    await waitFor(() => expect((select as HTMLSelectElement).value).toBe("dark"));
    expect(document.documentElement.dataset.theme).toBe("dark");

    fireEvent.change(select, { target: { value: "light" } });
    expect((select as HTMLSelectElement).value).toBe("light");
    expect(document.documentElement.dataset.theme).toBe("light");
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe("light");
  });

  it("follows operating-system changes while system mode is selected", async () => {
    const changeColorScheme = mockColorScheme(false);
    render(<ThemeProvider><ThemeSwitcher /></ThemeProvider>);

    await waitFor(() => expect(document.documentElement.dataset.theme).toBe("light"));
    act(() => changeColorScheme(true));
    await waitFor(() => expect(document.documentElement.dataset.theme).toBe("dark"));
    expect((screen.getByRole("combobox", { name: "外觀主題" }) as HTMLSelectElement).value).toBe("system");
  });
});
