import { afterEach, describe, expect, it } from "vitest";
import { currencies, currencyName, isCurrency, normalizeCurrency } from "./currency";
import { destinations } from "./destinations";

describe("currency list", () => {
  it("covers every currency a published destination is priced in", () => {
    // If a destination lands with a currency the member cannot select, its trip
    // ledger has no honest default. The API rejects anything outside this list.
    for (const destination of destinations) {
      expect(currencies).toContain(destination.currency);
    }
  });

  it("rejects anything the API would reject", () => {
    expect(isCurrency("JPY")).toBe(true);
    expect(isCurrency("EUR")).toBe(false);
    expect(isCurrency("twd")).toBe(false);
    expect(normalizeCurrency("EUR")).toBe("TWD");
    expect(normalizeCurrency(null)).toBe("TWD");
    expect(normalizeCurrency("KRW")).toBe("KRW");
  });
});

describe("currencyName", () => {
  afterEach(() => {
    document.documentElement.lang = "";
  });

  it("names every currency in the reader's language", () => {
    document.documentElement.lang = "ja";
    expect(currencyName("JPY")).toBe("日本円");
    document.documentElement.lang = "zh-TW";
    expect(currencyName("JPY")).toBe("日圓");
    // Never leave the reader with a bare code when Intl does know the name.
    for (const currency of currencies) {
      expect(currencyName(currency)).not.toBe(currency);
    }
  });
});
