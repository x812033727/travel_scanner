import { describe, expect, it } from "vitest";
import { defaultLocale, isLocale, normalizeLocale } from "./routing";

describe("locale routing", () => {
  it.each([
    ["en-US", "en"],
    ["ja-JP", "ja"],
    ["ko-KR", "ko"],
    ["zh-Hant", "zh-TW"],
    ["zh-HK", "zh-TW"],
    ["zh-MO", "zh-TW"],
    ["zh-Hans", "zh-CN"],
    ["zh-CN", "zh-CN"],
    ["zh-SG", "zh-CN"],
    ["fr-FR", "zh-TW"],
  ])("maps %s to %s", (input, expected) => {
    expect(normalizeLocale(input)).toBe(expected);
  });

  it("keeps the supported locale whitelist strict", () => {
    expect(defaultLocale).toBe("zh-TW");
    expect(isLocale("ko")).toBe(true);
    expect(isLocale("zh-Hant")).toBe(false);
  });
});
