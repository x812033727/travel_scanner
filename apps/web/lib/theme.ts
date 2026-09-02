export const THEME_STORAGE_KEY = "mokaair-theme";

export const themePreferences = ["system", "light", "dark"] as const;
export type ThemePreference = (typeof themePreferences)[number];
export type ResolvedTheme = Exclude<ThemePreference, "system">;

export function isThemePreference(value: unknown): value is ThemePreference {
  return typeof value === "string" && themePreferences.includes(value as ThemePreference);
}

export function resolveTheme(preference: ThemePreference, systemPrefersDark: boolean): ResolvedTheme {
  if (preference === "system") return systemPrefersDark ? "dark" : "light";
  return preference;
}

export const THEME_BOOTSTRAP_SCRIPT = `(function(){var r=document.documentElement;var p="system";try{var s=localStorage.getItem("${THEME_STORAGE_KEY}");if(s==="system"||s==="light"||s==="dark")p=s}catch(e){}var d=p==="dark"||(p==="system"&&window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches);var t=d?"dark":"light";r.dataset.theme=t;r.dataset.themePreference=p;r.style.colorScheme=t})()`;
