import { afterEach, describe, expect, it } from "vitest";
import { formatCurrency, formatMoney } from "./locale-format";

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

describe("formatMoney", () => {
  afterEach(() => {
    document.documentElement.lang = "";
  });

  it("keeps the minor unit a ledger entry was typed with", () => {
    document.documentElement.lang = "zh-TW";
    expect(formatMoney(1234.5)).toBe("NT$1,234.50");
    expect(formatMoney(1234.5, "USD")).toContain("1,234.50");
  });

  it("drops decimals for currencies that have no minor unit", () => {
    document.documentElement.lang = "zh-TW";
    for (const currency of ["JPY", "KRW", "VND"]) {
      expect(formatMoney(1234, currency)).toContain("1,234");
      expect(formatMoney(1234, currency)).not.toContain("1,234.00");
    }
  });

  it("pins NT$ the same way formatCurrency does", () => {
    for (const lang of ["zh-TW", "zh-CN", "ja", "ko", "en"]) {
      document.documentElement.lang = lang;
      expect(formatMoney(120000)).toBe("NT$120,000.00");
      expect(formatMoney(-450)).toBe("-NT$450.00");
    }
  });

  it("does not change what formatCurrency renders", () => {
    document.documentElement.lang = "zh-TW";
    expect(formatCurrency(120000)).toBe("NT$120,000");
    expect(formatCurrency(1234.5)).toBe("NT$1,235");
  });
});
