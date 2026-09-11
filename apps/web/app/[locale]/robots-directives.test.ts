import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * Which routes may be indexed, asserted from the sources.
 *
 * Reading the files rather than rendering them is the same trade-off metadata.test.ts makes: a
 * directive can be declared on the page or inherited from any layout above it, and what this
 * needs to catch is someone deleting the declaration -- not whether Next merges parent metadata,
 * which is Next's own contract and was checked once against a production build.
 */

const APP = import.meta.dirname;
const declaresNoindex = (source: string) => /index:\s*false/.test(source);

/** The page plus every layout between it and app/[locale], nearest last. */
function chain(route: string): string[] {
  const segments = route.split("/").filter(Boolean);
  const files = [join(APP, "layout.tsx")];
  let directory = APP;
  for (const segment of segments) {
    directory = join(directory, segment);
    const layout = join(directory, "layout.tsx");
    if (existsSync(layout)) files.push(layout);
  }
  files.push(join(directory, "page.tsx"));
  return files.filter((file) => existsSync(file));
}

const covered = (route: string) => chain(route).some((file) => declaresNoindex(readFileSync(file, "utf8")));

// Signed-in surfaces, auth forms, and URLs whose only key is an unguessable token.
const PRIVATE = [
  "/search", "/search/new",
  "/login", "/register", "/forgot-password",
  "/account", "/account/confirm",
  "/my",
  "/trips", "/trips/new", "/trips/[id]", "/trips/[id]/print",
  "/alerts",
  "/share/[token]", "/share-target",
  "/line/link",
  "/admin", "/admin/users", "/admin/settings", "/admin/deployments", "/admin/database",
];

// Public content. A noindex here is a bug, not a policy.
const PUBLIC = ["/", "/hotspots", "/foods", "/pricing", "/flights/status", "/labs/airlines"];

describe("index directives", () => {
  it.each(PRIVATE)("%s is kept out of the index", (route) => {
    expect(covered(route), `${route} has no noindex on its page or any layout above it`).toBe(true);
  });

  it.each(PUBLIC)("%s stays indexable", (route) => {
    // The gated routes declare noindex inside a conditional, so match the unconditional form
    // that would actually close them: a bare `robots` export or a literal on the page.
    const page = join(APP, ...route.split("/").filter(Boolean), "page.tsx");
    expect(existsSync(page), `${route} has no page`).toBe(true);
    expect(declaresNoindex(readFileSync(page, "utf8")), `${route} declares noindex on its page`).toBe(false);
  });

  it("would notice a route that lost its directive", () => {
    // A guard on the guard: if `chain` stopped resolving files, every case above would pass
    // vacuously. /foods is the control -- no layout of its own, and nothing above it declares a
    // directive. (/hotspots would not do: its layout carries a noindex inside a conditional, and
    // reading sources cannot tell that apart from an unconditional one.)
    expect(chain("/login").length).toBeGreaterThanOrEqual(2);
    expect(chain("/foods")).toHaveLength(2);
    expect(covered("/foods")).toBe(false);
  });
});
