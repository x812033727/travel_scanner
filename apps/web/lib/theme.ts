export const THEME_STORAGE_KEY = "mokaair-theme";
export const PALETTE_STORAGE_KEY = "mokaair-palette";
export const palettes = ["mocha", "lagoon", "forest"] as const;
export type Palette = (typeof palettes)[number];
export const DEFAULT_PALETTE: Palette = "mocha";

export function isPalette(value: unknown): value is Palette {
  return typeof value === "string" && palettes.includes(value as Palette);
}

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

// Parser-blocking, nonce-protected root script: both attributes are set before first paint.
// Keep the existing mode key independent so previously saved choices remain compatible.
export const THEME_BOOTSTRAP_SCRIPT = `(function(){var r=document.documentElement;var p="system";var c="${DEFAULT_PALETTE}";try{var s=localStorage.getItem("${THEME_STORAGE_KEY}");if(s==="system"||s==="light"||s==="dark")p=s}catch(e){}try{var a=localStorage.getItem("${PALETTE_STORAGE_KEY}");if(a==="mocha"||a==="lagoon"||a==="forest")c=a}catch(e){}var d=p==="dark"||(p==="system"&&window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches);var t=d?"dark":"light";r.dataset.palette=c;r.dataset.theme=t;r.dataset.themePreference=p;r.style.colorScheme=t})()`;
