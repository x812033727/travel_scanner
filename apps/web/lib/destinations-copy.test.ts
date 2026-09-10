import { describe, expect, it } from "vitest";
import { locales } from "@/i18n/routing";
import { destinationsCopy } from "./destinations-copy";

describe("destinationsCopy", () => {
  const english = destinationsCopy("en");

  it.each(locales)("covers every key in %s", (locale) => {
    const copy = destinationsCopy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(english).sort());
    for (const [key, value] of Object.entries(copy)) {
      expect(value.trim(), `${locale}.${key} is empty`).not.toBe("");
    }
  });

  it.each(locales.filter((locale) => locale !== "en"))("is actually translated in %s", (locale) => {
    // A copied English string would pass the key check above and still ship an untranslated page.
    const copy = destinationsCopy(locale);
    const shared = Object.keys(english).filter((key) => copy[key as keyof typeof english] === english[key as keyof typeof english]);
    expect(shared, `${locale} still shares English text for ${shared.join(", ")}`).toHaveLength(0);
  });

  it("falls back to English for a locale it does not carry", () => {
    expect(destinationsCopy("pt-BR")).toBe(english);
  });
});
