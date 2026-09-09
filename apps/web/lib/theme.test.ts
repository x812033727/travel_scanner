import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";
import { isPalette, isThemePreference, palettes, PALETTE_STORAGE_KEY, resolveTheme, THEME_BOOTSTRAP_SCRIPT, THEME_STORAGE_KEY, themePreferences } from "./theme";

describe("theme helpers", () => {
  it("accepts only supported preferences", () => {
    expect(isThemePreference("system")).toBe(true);
    expect(isThemePreference("light")).toBe(true);
    expect(isThemePreference("dark")).toBe(true);
    expect(isThemePreference("sepia")).toBe(false);
    expect(isThemePreference(null)).toBe(false);
  });

  it("resolves system preferences without changing explicit choices", () => {
    expect(resolveTheme("system", true)).toBe("dark");
    expect(resolveTheme("system", false)).toBe("light");
    expect(resolveTheme("dark", false)).toBe("dark");
    expect(resolveTheme("light", true)).toBe("light");
  });

  it("accepts only the three independent palette families", () => {
    palettes.forEach((palette) => expect(isPalette(palette)).toBe(true));
    [null, "dark", "ocean", "", {}].forEach((value) => expect(isPalette(value)).toBe(false));
  });

  it.each(themePreferences.flatMap((preference) => palettes.map((palette) => ({ preference, palette }))))(
    "bootstraps $preference / $palette before React without overwriting storage",
    ({ preference, palette }) => {
      const root = { dataset: {} as Record<string, string>, style: {} as Record<string, string> };
      runInNewContext(THEME_BOOTSTRAP_SCRIPT, {
        document: { documentElement: root },
        localStorage: { getItem: (key: string) => key === THEME_STORAGE_KEY ? preference : palette },
        window: { matchMedia: () => ({ matches: true }) },
      });
      expect(root.dataset).toEqual({ theme: preference === "light" ? "light" : "dark", themePreference: preference, palette });
      expect(root.style.colorScheme).toBe(root.dataset.theme);
    },
  );

  it.each(["invalid", "blocked"])("safely bootstraps defaults with %s storage", (mode) => {
    const root = { dataset: {} as Record<string, string>, style: {} };
    runInNewContext(THEME_BOOTSTRAP_SCRIPT, {
      document: { documentElement: root },
      localStorage: { getItem: () => { if (mode === "blocked") throw new Error("blocked"); return "invalid"; } },
      window: {},
    });
    expect(root.dataset).toEqual({ theme: "light", themePreference: "system", palette: "mocha" });
    expect(PALETTE_STORAGE_KEY).not.toBe(THEME_STORAGE_KEY);
  });
});

// Test the shipped CSS rather than a duplicate runtime colour table.
const css = readFileSync(`${import.meta.dirname}/../app/globals.css`, "utf8").replace(/\r\n/g, "\n");
const tokenNames = ["bg", "card", "text", "muted", "primary", "primary-text", "border", "focus"];
const expectedTokens = [
  ["mocha", "light", "f7f1e8 fffcf8 102a2b 5e6864 0d6b68 ffffff 7e8276 6b4a3a"],
  ["mocha", "dark", "171412 241f1b f7f1e8 c0b3a6 78d1c7 112c29 8b7c6e e0b091"],
  ["lagoon", "light", "f0f6fa ffffff 112c3b 506777 155e80 ffffff 718998 075985"],
  ["lagoon", "dark", "0d1820 142630 eaf5fa a7bcc8 83cce8 082d40 658998 b7e8f8"],
  ["forest", "light", "f2f5ed fcfdf8 223127 5b6959 3e6348 ffffff 7d8873 385b3e"],
  ["forest", "dark", "111a14 1d2a21 edf4e8 b1c2aa a6d3a0 1b341f 778d74 d8e8a3"],
];
function luminance(hex: string) {
  const channels = hex.match(/\w\w/g)!.map((part) => {
    const value = parseInt(part, 16) / 255;
    return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return channels[0] * 0.2126 + channels[1] * 0.7152 + channels[2] * 0.0722;
}
function contrast(a: string, b: string) {
  const values = [luminance(a), luminance(b)];
  return (Math.max(...values) + 0.05) / (Math.min(...values) + 0.05);
}
function mixHex(a: string, b: string, weight: number) {
  const parts = (hex: string) => hex.match(/\w\w/g)!.map((part) => parseInt(part, 16));
  const first = parts(a), second = parts(b);
  return first.map((channel, index) => Math.round(channel * weight + second[index] * (1 - weight)).toString(16).padStart(2, "0")).join("");
}
function cssBlock(selector: string) {
  expect(css).toContain(selector);
  return css.slice(css.indexOf(selector)).split("}")[0];
}
describe("approved palette CSS", () => {
  it.each(expectedTokens)("ships exact accessible %s / %s tokens", (palette, theme, values) => {
    const selector = `.palette-preview[data-preview-palette="${palette}"][data-preview-theme="${theme}"]`;
    const body = css.slice(css.indexOf(selector)).split("}")[0];
    const tokens = tokenNames.map((name) => body.match(new RegExp(`--palette-${name}: #([0-9a-f]{6});`))?.[1]);
    expect(tokens).toEqual(values.split(" "));
    const [bg, card, text, muted, primary, primaryText, border, focus] = values.split(" ");
    for (const surface of [bg, card]) {
      expect(contrast(surface, text)).toBeGreaterThanOrEqual(4.5);
      expect(contrast(surface, muted)).toBeGreaterThanOrEqual(4.5);
      expect(contrast(surface, border)).toBeGreaterThanOrEqual(3);
      expect(contrast(surface, focus)).toBeGreaterThanOrEqual(3);
    }
    expect(contrast(primary, primaryText)).toBeGreaterThanOrEqual(4.5);
    // The active admin link uses a primary-on-soft fill, not primary-on-black.
    expect(contrast(primary, mixHex(primary, card, .08))).toBeGreaterThanOrEqual(4.5);
    const hover = mixHex(primary, theme === "dark" ? "ffffff" : "000000", .92);
    // Flight hero copy spans the paired-fill gradient, including both endpoints.
    for (let step = 0; step <= 10; step++) {
      expect(contrast(mixHex(primary, hover, step / 10), primaryText)).toBeGreaterThanOrEqual(4.5);
    }
  });
  it("keeps brand colours independent and planner customisations out of site mode", () => {
    expect(css).toContain(".mokaair-wordmark-air {\n  color: var(--brand-air);");
    expect(css).not.toContain(':root[data-theme="dark"] .planner-app-shell[data-planner-theme] {');
    expect(css).toContain('--primary-text: var(--palette-primary-text)');
  });

  it("maps the legacy dark utility to its paired fill and foreground without descendant rules", () => {
    expect(cssBlock(':where([class~="bg-[var(--teal-dark)]"]) {')).toContain("background-color: var(--teal-fill-hover) !important;");
    const foreground = css.split("}").find((rule) => rule.includes('[class~="text-white"]') && rule.includes("color: var(--primary-text)"));
    expect(foreground).toContain('[class~="bg-[var(--teal-dark)]"]');
    expect(foreground).not.toContain(" *");
  });

  it("uses the accessible control border for the theme and language selectors in both states", () => {
    expect(cssBlock(".theme-switcher {")).toContain("border: 1px solid var(--control-border);");
    expect(cssBlock(".theme-switcher:hover {")).toContain("border-color: var(--control-border);");
    expect(cssBlock(".theme-switcher:focus-within {")).toContain("outline: 3px solid var(--focus);");
    const nativeControl = cssBlock(".theme-switcher select {");
    expect(nativeControl).toContain("inset: -1px;");
    expect(nativeControl).toContain("width: calc(100% + 2px);");
    expect(nativeControl).toContain("height: calc(100% + 2px);");
  });

  it("does not leave a colour-transition frame when reduced motion is requested", () => {
    const reducedMotion = cssBlock("@media (prefers-reduced-motion: reduce) {\n  *,");
    expect(reducedMotion).toContain("transition: none !important;");
    expect(reducedMotion).not.toContain("transition-duration: 0.01ms");
  });

  it("contains admin action text within shrinkable boxes while preserving compact controls", () => {
    expect(cssBlock(".admin-topbar-heading {")).toContain("min-width: 0;");
    expect(cssBlock(".admin-topbar-actions {")).toContain("flex: 0 1 44rem;");
    expect(cssBlock(".admin-command-trigger {")).toContain("flex: 1 1 15rem;");
    expect(cssBlock(".admin-account-control {")).toContain("flex: 0 1 14rem;");
    expect(cssBlock(".admin-account-trigger {")).toContain("width: 100%;");
    expect(cssBlock(".admin-health > span {")).toContain("text-overflow: ellipsis;");
    expect(css).toContain(".admin-topbar-actions, .admin-command-trigger { flex: none; }");
    expect(css).toContain(".admin-account-control { min-width: 2.75rem; flex: none; }");
    expect(css).toContain(".admin-mobile-menu { max-width: 9.5rem; }");
  });

  it("pairs flight hero, selected dates, holiday dots and hotspot hints explicitly", () => {
    const source = (file: string) => readFileSync(`${import.meta.dirname}/../components/${file}`, "utf8");
    const hero = cssBlock(".flight-status-hero {");
    expect(hero).toContain("linear-gradient(135deg, var(--teal-fill-hover), var(--teal-fill))");
    expect(hero).toContain("color: var(--primary-text);");
    const flightHero = source("flight-status-search.tsx").split('className="flight-status-hero')[1]?.split("</section>")[0];
    expect(flightHero).toBeDefined();
    expect(flightHero).not.toContain("text-white");
    const calendar = source("date-range-picker.tsx");
    expect(calendar).toContain("data-[range=edge]:text-[var(--primary-text)]");
    expect(calendar).toContain("data-[range=edge]:after:bg-[var(--primary-text)]");
    expect(calendar).not.toContain("data-[range=edge]:text-white");
    expect(calendar).not.toContain("data-[range=edge]:after:bg-white");
    const hotspotHints = source("hotspot-explorer.tsx").split("\n").filter((line) => line.includes('bg-[var(--teal)]') && line.includes("openDetails(item)"));
    expect(hotspotHints).toHaveLength(2);
    hotspotHints.forEach((line) => {
      expect(line).toContain("text-[var(--primary-text)]");
      expect(line).not.toMatch(/text-white\/\d+/);
    });
  });
});
