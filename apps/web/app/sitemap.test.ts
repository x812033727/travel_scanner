import { readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { locales } from "@/i18n/routing";
import { siteUrl } from "@/lib/seo";
import sitemap, { SITEMAP_ROUTES } from "./sitemap";

const APP = import.meta.dirname;
// Both trees serve /{locale}/…: the second is a route group with its own root layout.
const ROOTS = [join(APP, "[locale]"), join(APP, "(stay22-public)", "[locale]")];

function directories(parent: string): string[] {
  try {
    return readdirSync(parent, { withFileTypes: true }).filter((entry) => entry.isDirectory()).map((entry) => entry.name);
  } catch {
    return [];
  }
}

/** Walks a sitemap path down the app directory, letting a `[dynamic]` folder stand in for a
 *  literal segment, and reports whether it lands on a real page.tsx. */
function routeExists(path: string): boolean {
  const segments = path.split("/").filter(Boolean);
  const walk = (directory: string, rest: string[]): boolean => {
    if (!rest.length) return readdirSync(directory).includes("page.tsx");
    const [head, ...tail] = rest;
    const names = directories(directory);
    const candidates = names.includes(head) ? [head] : names.filter((name) => name.startsWith("["));
    return candidates.some((name) => walk(join(directory, name), tail));
  };
  return ROOTS.some((root) => walk(root, segments));
}

describe("sitemap", () => {
  const entries = sitemap();

  it("publishes one entry per locale per route", () => {
    expect(entries).toHaveLength(SITEMAP_ROUTES.length * locales.length);
  });

  it("has no duplicate URLs", () => {
    const urls = entries.map((entry) => entry.url);
    expect(new Set(urls).size).toBe(urls.length);
  });

  it("uses absolute URLs on the canonical origin", () => {
    for (const entry of entries) expect(entry.url.startsWith(`${siteUrl}/`)).toBe(true);
  });

  it("gives every entry all five locales plus x-default", () => {
    for (const entry of entries) {
      const languages = entry.alternates?.languages ?? {};
      expect(Object.keys(languages).sort()).toEqual([...locales, "x-default"].sort());
    }
  });

  // The guard that matters: without it a rename quietly turns the sitemap into a list of 404s,
  // and nothing else in the suite would notice.
  it.each(SITEMAP_ROUTES.map((route) => route.path))("%s resolves to a real page", (path) => {
    expect(routeExists(path), `${path} has no page.tsx under app/`).toBe(true);
  });

  it("would notice a path that has no page", () => {
    // A guard on the guard: if the walk stopped matching the app directory, the check above
    // would pass by testing nothing. Same reasoning as app/[locale]/metadata.test.ts.
    expect(routeExists("/hotspots")).toBe(true);
    expect(routeExists("/not-a-route")).toBe(false);
    expect(routeExists("/destinations/tokyo/nope")).toBe(false);
  });

  it("leaves out routes that are still noindex", () => {
    // Managed documents are noindex until published; explore, pet-friendly and community send an
    // empty shell. Listing any of them would only collect "Excluded by noindex".
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    for (const path of ["/about", "/privacy", "/terms", "/contact", "/explore", "/explore/collections", "/pet-friendly"]) {
      expect(paths).not.toContain(path);
    }
  });

  it("carries every public destination", () => {
    const paths = SITEMAP_ROUTES.map((route) => route.path);
    expect(paths).toContain("/destinations/tokyo/services");
    expect(paths.filter((path) => path.startsWith("/destinations/")).length).toBeGreaterThanOrEqual(33);
  });
});
