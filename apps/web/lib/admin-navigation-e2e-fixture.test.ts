import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { fallbackAdminNavigation } from "./admin-operations";

const fixtureSource = readFileSync(
  resolve(process.cwd(), "../../tools/e2e-runtime-api.mjs"),
  "utf8",
);

describe("the e2e runtime fixture and admin navigation", () => {
  it("contains the same hrefs as the fallback navigation", () => {
    // Limit extraction to the registry, so an unrelated route cannot hide a missing entry.
    const registry = fixtureSource.match(/const adminNavigation = \[([\s\S]*?)\r?\n\]\.map\(/);
    expect(registry, "The e2e adminNavigation registry must be readable").not.toBeNull();
    const fixtureHrefs = new Set(
      [...(registry?.[1] ?? "").matchAll(/^\s+\["[^"]+",\s*"[^"]+",\s*"([^"]+)"/gm)]
        .map((match) => match[1]),
    );
    const expectedHrefs = new Set(fallbackAdminNavigation.map((item) => item.href));
    // The registries group a few entries differently; only their complete sets must agree.
    expect({
      missing: [...expectedHrefs].filter((href) => !fixtureHrefs.has(href)).sort(),
      unexpected: [...fixtureHrefs].filter((href) => !expectedHrefs.has(href)).sort(),
    }, "Update the e2e adminNavigation registry when admin routes change").toEqual({
      missing: [], unexpected: [],
    });
  });
});
