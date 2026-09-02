"use client";

import { MonitorCog, Moon, Sun } from "lucide-react";
import { useTranslations } from "next-intl";
import { useTheme } from "@/components/theme-provider";
import { themePreferences, type ThemePreference } from "@/lib/theme";

const labels = {
  system: "themeSystem",
  light: "themeLight",
  dark: "themeDark",
} as const;

export function ThemeSwitcher() {
  const t = useTranslations("navigation");
  const { preference, resolvedTheme, ready, setPreference } = useTheme();
  const Icon = preference === "system" ? MonitorCog : resolvedTheme === "dark" ? Moon : Sun;
  const current = t(labels[preference]);

  return (
    <label className="theme-switcher" title={t("themeCurrent", { theme: current })}>
      <Icon aria-hidden size={19} />
      <span className="sr-only">{t("themeLabel")}</span>
      <select
        aria-label={t("themeLabel")}
        disabled={!ready}
        value={preference}
        onChange={(event) => setPreference(event.target.value as ThemePreference)}
      >
        {themePreferences.map((value) => (
          <option key={value} value={value}>{t(labels[value])}</option>
        ))}
      </select>
    </label>
  );
}
