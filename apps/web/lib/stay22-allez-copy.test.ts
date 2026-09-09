import { describe, expect, it } from "vitest";
import { stay22AllezCopy, stay22AllezText } from "./stay22-allez-copy";

describe("Stay22 Allez localized copy", () => {
  it.each(["en", "zh-TW", "zh-CN", "ja", "ko"])("has matching nonempty keys and placeholders for %s", (locale) => {
    const reference = stay22AllezCopy("en");
    const copy = stay22AllezCopy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(reference).sort());
    for (const key of Object.keys(reference) as (keyof typeof reference)[]) {
      expect(copy[key].trim().length).toBeGreaterThan(0);
      expect(copy[key].match(/\{\w+\}/g)).toEqual(reference[key].match(/\{\w+\}/g));
    }
  });
  it("falls back safely and only interpolates declared text placeholders", () => {
    expect(stay22AllezCopy("unknown")).toEqual(stay22AllezCopy("en"));
    expect(stay22AllezText(stay22AllezCopy("zh-TW").openPlatform, { platform: "Booking.com" })).toBe("前往 Booking.com 查價格");
  });
});
