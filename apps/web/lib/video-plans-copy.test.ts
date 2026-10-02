import { describe, expect, it } from "vitest";
import { videoPlansCopy, videoPlansText } from "./video-plans-copy";

function messages(value: object, prefix = ""): Record<string, string> {
  return Object.fromEntries(Object.entries(value).flatMap(([key, item]) => {
    const name = prefix ? `${prefix}.${key}` : key;
    return typeof item === "string" ? [[name, item]] : Object.entries(messages(item, name));
  }));
}

describe("planning catalog copy", () => {
  it("keeps all five locales' keys and interpolation parameters aligned", () => {
    const base = messages(videoPlansCopy("en"));
    for (const locale of ["en", "ja", "ko", "zh-TW", "zh-CN"]) {
      const translated = messages(videoPlansCopy(locale));
      expect(Object.keys(translated).sort()).toEqual(Object.keys(base).sort());
      for (const [key, text] of Object.entries(translated)) {
        expect(text.trim()).not.toBe("");
        expect([...text.matchAll(/\{(\w+)\}/g)].map((match) => match[1]).sort())
          .toEqual([...base[key].matchAll(/\{(\w+)\}/g)].map((match) => match[1]).sort());
      }
    }
    expect(videoPlansCopy("unknown")).toBe(videoPlansCopy("en"));
    expect(videoPlansText(videoPlansCopy("zh-TW").pagination, { page: 2, pages: 19 })).toBe("第 2 頁，共 19 頁");
  });
});
