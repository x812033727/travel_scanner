import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { siteUrl } from "@/lib/seo";
import robots from "./robots";

const LOCALE_APP = join(import.meta.dirname, "[locale]");

/** robots.txt globbing: `*` is any run of characters, and a rule matches by prefix. */
function disallows(path: string): boolean {
  const rules = robots().rules;
  const disallow = (Array.isArray(rules) ? rules[0] : rules).disallow ?? [];
  const patterns = Array.isArray(disallow) ? disallow : [disallow];
  return patterns.some((pattern) =>
    new RegExp(`^${pattern.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*")}`).test(path),
  );
}

/** Every route under app/[locale] whose page source asks not to be indexed. */
function noindexRoutes(): string[] {
  const found: string[] = [];
  const walk = (directory: string, prefix: string) => {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const next = join(directory, entry.name);
      const route = `${prefix}/${entry.name}`;
      if (readdirSync(next).includes("page.tsx")) {
        const source = readFileSync(join(next, "page.tsx"), "utf8");
        if (/index:\s*false/.test(source)) found.push(route);
      }
      walk(next, route);
    }
  };
  walk(LOCALE_APP, "");
  return found;
}

describe("robots", () => {
  it("points at the sitemap on the canonical origin", () => {
    expect(robots().sitemap).toBe(`${siteUrl}/sitemap.xml`);
  });

  it("blocks the BFF, the console and every token URL", () => {
    for (const path of [
      "/api/travel/foods",
      "/en/admin",
      "/zh-TW/admin/users",
      "/en/out/guides/abc",
      "/ja/share/some-token",
      "/ko/share-target",
      "/en/line/link",
      "/en/account/confirm",
    ]) {
      expect(disallows(path), `${path} should be disallowed`).toBe(true);
    }
  });

  it("leaves public content crawlable", () => {
    for (const path of ["/en", "/en/hotspots", "/zh-TW/foods", "/en/pricing", "/ja/destinations/tokyo/services"]) {
      expect(disallows(path), `${path} should be crawlable`).toBe(false);
    }
  });

  // The rule this file exists to protect. A blocked URL is never fetched, so its `noindex` is
  // never read and the page can linger in results as a bare URL. Anything relying on `noindex`
  // to be removed has to stay crawlable.
  it("never blocks a page that relies on noindex to be de-indexed", () => {
    // These carry both on purpose: they were never indexable, so there is nothing to remove.
    const intentional = ["/admin", "/share", "/share-target", "/line", "/account/confirm"];
    const routes = noindexRoutes().filter(
      (route) => !intentional.some((prefix) => route === prefix || route.startsWith(`${prefix}/`)),
    );
    expect(routes.length).toBeGreaterThan(0);
    for (const route of routes) {
      expect(disallows(`/en${route}`), `${route} is noindex, so it must stay crawlable`).toBe(false);
    }
  });
});
