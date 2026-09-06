import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * Nine of thirteen public pages once shared one <title> and one meta description, in every
 * locale. Tabs were indistinguishable from each other and the pages competed with themselves
 * in search results.
 *
 * This reads the page sources rather than rendering them: the point is that each page asks
 * for its own metadata keys and that those keys exist and differ, none of which needs a DOM.
 * Rendering would also need `metadata` added to the catalogues in vitest.setup.tsx, which
 * belongs to someone else's change right now.
 */

const LOCALES = ["en", "ja", "ko", "zh-TW", "zh-CN"] as const;
const APP = join(import.meta.dirname);
const MESSAGES = join(import.meta.dirname, "..", "..", "messages");

// Route segments that are not public pages.
const NOT_PUBLIC = new Set(["admin", "line", "out", "share-target"]);
// The home page is the one page the site-wide title and description are written for. It is
// never in `routes` because the walk only descends into subdirectories, but its keys are what
// every other page must not reuse.
const SITE_WIDE = ["title", "description"] as const;

function publicPages(): string[] {
  const found: string[] = [];
  const walk = (directory: string, prefix: string) => {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      if (prefix === "" && NOT_PUBLIC.has(entry.name)) continue;
      // Dynamic segments ([id]) render one saved object, not a listing page.
      if (entry.name.startsWith("[")) continue;
      const next = join(directory, entry.name);
      const route = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (readdirSync(next).includes("page.tsx")) found.push(route);
      walk(next, route);
    }
  };
  walk(APP, "");
  return found.sort();
}

function metadataKeys(route: string): { title: string; description: string } | null {
  const source = readFileSync(join(APP, route, "page.tsx"), "utf8");
  const title = /title:\s*t\("([A-Za-z]+)"\)/.exec(source);
  const description = /description:\s*t\("([A-Za-z]+)"\)/.exec(source);
  if (!title || !description) return null;
  return { title: title[1], description: description[1] };
}

function catalog(locale: string): Record<string, string> {
  return JSON.parse(readFileSync(join(MESSAGES, locale, "metadata.json"), "utf8"));
}

describe("public page metadata", () => {
  const routes = publicPages();

  it("finds the public pages", () => {
    // A guard on the guard: if the walk stops matching the app directory this whole file
    // would pass by testing nothing.
    expect(routes.length).toBeGreaterThanOrEqual(12);
  });

  it.each(routes)("%s asks for its own title and description", (route) => {
    const keys = metadataKeys(route);
    expect(keys, `${route}/page.tsx has no generateMetadata`).not.toBeNull();
    // Falling back to the site-wide keys is the defect itself, not a way of satisfying it.
    expect(SITE_WIDE, `${route} reuses the site-wide title`).not.toContain(keys!.title);
    expect(SITE_WIDE, `${route} reuses the site-wide description`).not.toContain(keys!.description);
    for (const locale of LOCALES) {
      const messages = catalog(locale);
      expect(messages[keys!.title], `${locale} is missing ${keys!.title}`).toBeTruthy();
      expect(messages[keys!.description], `${locale} is missing ${keys!.description}`).toBeTruthy();
    }
  });

  it.each(LOCALES)("gives every page a distinct title in %s", (locale) => {
    const messages = catalog(locale);
    const titles = routes.map((route) => messages[metadataKeys(route)!.title]);
    expect(new Set(titles).size).toBe(titles.length);
    expect(titles).not.toContain(messages.title);
  });

  it.each(LOCALES)("gives every page a distinct description in %s", (locale) => {
    const messages = catalog(locale);
    const descriptions = routes.map((route) => messages[metadataKeys(route)!.description]);
    expect(new Set(descriptions).size).toBe(descriptions.length);
    expect(descriptions).not.toContain(messages.description);
  });
});
