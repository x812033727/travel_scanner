"use client";

import { createContext, useCallback, useContext, useEffect, useLayoutEffect, useState } from "react";
import {
  DEFAULT_PALETTE,
  isPalette,
  isThemePreference,
  PALETTE_STORAGE_KEY,
  resolveTheme,
  THEME_STORAGE_KEY,
  type ResolvedTheme,
  type ThemePreference,
  type Palette,
} from "@/lib/theme";

type ThemeContextValue = Readonly<{
  preference: ThemePreference;
  resolvedTheme: ResolvedTheme;
  palette: Palette;
  ready: boolean;
  setPreference: (preference: ThemePreference) => void;
  setPalette: (palette: Palette) => void;
}>;

const ThemeContext = createContext<ThemeContextValue | null>(null);

function systemPrefersDark() {
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false;
}

function applyTheme(preference: ThemePreference): ResolvedTheme {
  const resolved = resolveTheme(preference, systemPrefersDark());
  const root = document.documentElement;
  root.dataset.theme = resolved;
  root.dataset.themePreference = preference;
  root.style.colorScheme = resolved;
  return resolved;
}

export function ThemeProvider({ children }: Readonly<{ children: React.ReactNode }>) {
  const [preference, setPreferenceState] = useState<ThemePreference>("system");
  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>("light");
  const [palette, setPaletteState] = useState<Palette>(DEFAULT_PALETTE);
  const [ready, setReady] = useState(false);

  const updatePreference = useCallback((next: ThemePreference, persist: boolean) => {
    const resolved = applyTheme(next);
    if (persist) {
      try {
        localStorage.setItem(THEME_STORAGE_KEY, next);
      } catch {
        // The in-page theme still works when storage is unavailable.
      }
    }
    setPreferenceState(next);
    setResolvedTheme(resolved);
    setReady(true);
  }, []);

  const updatePalette = useCallback((next: Palette, persist: boolean) => {
    document.documentElement.dataset.palette = next;
    if (persist) {
      try {
        localStorage.setItem(PALETTE_STORAGE_KEY, next);
      } catch {
        // Palette changes still work for this page when storage is blocked.
      }
    }
    setPaletteState(next);
  }, []);

  useLayoutEffect(() => {
    const bootstrapped = document.documentElement.dataset.themePreference;
    let initial: ThemePreference = isThemePreference(bootstrapped) ? bootstrapped : "system";
    const bootstrappedPalette = document.documentElement.dataset.palette;
    let initialPalette = isPalette(bootstrappedPalette) ? bootstrappedPalette : DEFAULT_PALETTE;
    try {
      const stored = localStorage.getItem(THEME_STORAGE_KEY);
      if (isThemePreference(stored)) initial = stored;
    } catch {
      // Use the bootstrapped system preference when storage is unavailable.
    }
    try {
      const stored = localStorage.getItem(PALETTE_STORAGE_KEY);
      if (isPalette(stored)) initialPalette = stored;
    } catch {
      // Preserve the pre-paint palette if storage cannot be read.
    }
    let cancelled = false;
    queueMicrotask(() => {
      if (!cancelled) {
        updatePalette(initialPalette, false);
        updatePreference(initial, false);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [updatePalette, updatePreference]);

  useEffect(() => {
    if (preference !== "system") return;
    const media = window.matchMedia?.("(prefers-color-scheme: dark)");
    if (!media) return;
    const handleChange = () => setResolvedTheme(applyTheme("system"));
    media.addEventListener("change", handleChange);
    return () => media.removeEventListener("change", handleChange);
  }, [preference]);

  useEffect(() => {
    const handleStorage = (event: StorageEvent) => {
      if (event.storageArea && event.storageArea !== localStorage) return;
      if (event.key === null || event.key === THEME_STORAGE_KEY) {
        updatePreference(isThemePreference(event.newValue) ? event.newValue : "system", false);
      }
      if (event.key === null || event.key === PALETTE_STORAGE_KEY) {
        updatePalette(isPalette(event.newValue) ? event.newValue : DEFAULT_PALETTE, false);
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [updatePalette, updatePreference]);

  const setPreference = useCallback(
    (next: ThemePreference) => updatePreference(next, true),
    [updatePreference],
  );

  const setPalette = useCallback((next: Palette) => updatePalette(next, true), [updatePalette]);

  return (
    <ThemeContext.Provider value={{ preference, resolvedTheme, palette, ready, setPreference, setPalette }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error("useTheme must be used within ThemeProvider");
  return value;
}
