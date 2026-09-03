import { afterEach, describe, expect, it } from "vitest";
import { formatCurrency } from "./locale-format";

describe("formatCurrency", () => {
  afterEach(() => {
    document.documentElement.lang = "";
  });

  it("pins the NT$ prefix for TWD in every locale", () => {
    for (const lang of ["zh-TW", "zh-CN", "ja", "ko", "en"]) {
      document.documentElement.lang = lang;
      expect(formatCurrency(120000)).toBe("NT$120,000");
    }
  });

  it("keeps the sign in front of the prefix", () => {
    document.documentElement.lang = "zh-TW";
    expect(formatCurrency(-450)).toBe("-NT$450");
  });

  it("leaves other currencies to Intl", () => {
    document.documentElement.lang = "zh-TW";
    expect(formatCurrency(5000, "JPY")).toContain("5,000");
    expect(formatCurrency(5000, "JPY")).not.toContain("NT$");
  });
});
