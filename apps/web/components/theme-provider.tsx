"use client";

import { createContext, useCallback, useContext, useEffect, useLayoutEffect, useState } from "react";
import {
  isThemePreference,
  resolveTheme,
  THEME_STORAGE_KEY,
  type ResolvedTheme,
  type ThemePreference,
} from "@/lib/theme";

type ThemeContextValue = Readonly<{
  preference: ThemePreference;
  resolvedTheme: ResolvedTheme;
  ready: boolean;
  setPreference: (preference: ThemePreference) => void;
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

  useLayoutEffect(() => {
    const bootstrapped = document.documentElement.dataset.themePreference;
    let initial: ThemePreference = isThemePreference(bootstrapped) ? bootstrapped : "system";
    try {
      const stored = localStorage.getItem(THEME_STORAGE_KEY);
      if (isThemePreference(stored)) initial = stored;
    } catch {
      // Use the bootstrapped system preference when storage is unavailable.
    }
    let cancelled = false;
    queueMicrotask(() => {
      if (!cancelled) updatePreference(initial, false);
    });
    return () => {
      cancelled = true;
    };
  }, [updatePreference]);

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
      if (event.key !== THEME_STORAGE_KEY) return;
      updatePreference(isThemePreference(event.newValue) ? event.newValue : "system", false);
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [updatePreference]);

  const setPreference = useCallback(
    (next: ThemePreference) => updatePreference(next, true),
    [updatePreference],
  );

  return (
    <ThemeContext.Provider value={{ preference, resolvedTheme, ready, setPreference }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error("useTheme must be used within ThemeProvider");
  return value;
}
