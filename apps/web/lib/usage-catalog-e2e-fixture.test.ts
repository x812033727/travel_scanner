import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { isUsageCatalog, usageOperations } from "./usage-catalog";

// tools/e2e-runtime-api.mjs hardcodes its own copy of the operation list. When
// the two drift, the browser suite prices the missing operation at the default
// cost and logs it (see normalizeUsageCatalog), which hides a fixture that is
// missing key, every metered surface renders its "unavailable" branch, and the
// browser suite fails on pages that have nothing to do with the change — a
// cascade that reads as flakiness. Fail here instead, with the name in hand.
// vitest runs with apps/web as its root.
const fixtureSource = readFileSync(
  resolve(process.cwd(), "../../tools/e2e-runtime-api.mjs"),
  "utf8",
);

describe("the e2e runtime fixture and the usage catalog", () => {
  it("lists every operation the catalog validator requires", () => {
    const missing = usageOperations.filter(
      (operation) => !fixtureSource.includes(`"${operation}"`),
    );
    expect(missing).toEqual([]);
  });

  it("produces a catalog the validator accepts", () => {
    const listed = [...fixtureSource.matchAll(/^\s+"([a-z_]+)",$/gm)].map((match) => match[1]);
    const operationCosts = Object.fromEntries(
      listed.filter((name) => (usageOperations as readonly string[]).includes(name)).map((name) => [name, 1]),
    );
    expect(isUsageCatalog({ trial_uses: 3, packages: [], operation_costs: operationCosts })).toBe(true);
  });
});
