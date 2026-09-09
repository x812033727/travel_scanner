import { describe, expect, it } from "vitest";
import { ADMIN_CATALOG_BUDGET_COPY, adminCatalogBudgetCopy, validCatalogCallLimit } from "./admin-catalog-budget-copy";

describe("catalog review budget copy", () => {
  it("provides all five locales with matching interpolation fields", () => {
    expect(Object.keys(ADMIN_CATALOG_BUDGET_COPY).sort()).toEqual(["en", "ja", "ko", "zh-CN", "zh-TW"]);
    for (const copy of Object.values(ADMIN_CATALOG_BUDGET_COPY)) {
      expect(Object.keys(copy).sort()).toEqual(Object.keys(ADMIN_CATALOG_BUDGET_COPY.en).sort());
      for (const key of Object.keys(copy) as (keyof typeof copy)[]) {
        expect(copy[key].trim()).not.toBe("");
        expect(copy[key].match(/\{[^}]+\}/g)).toEqual(ADMIN_CATALOG_BUDGET_COPY.en[key].match(/\{[^}]+\}/g));
      }
    }
    expect(adminCatalogBudgetCopy("unknown")).toBe(ADMIN_CATALOG_BUDGET_COPY.en);
  });

  it.each([1, 80, 150, 1000])("accepts bounded whole-number cap %s", (value) => {
    expect(validCatalogCallLimit(value)).toBe(true);
  });

  it.each([null, undefined, "80", 0, -1, 1.5, 1001, NaN, Infinity])("rejects invalid cap %s", (value) => {
    expect(validCatalogCallLimit(value)).toBe(false);
  });
});
