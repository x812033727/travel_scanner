import { describe, expect, it } from "vitest";
import { plannerCopy, plannerLocales } from "./planner-copy";

describe("premium planner copy", () => {
  it("covers every site language without missing labels or interpolation variables", () => {
    expect(plannerLocales.sort()).toEqual(["en", "ja", "ko", "zh-CN", "zh-TW"]);
    const baseline = plannerCopy("en");
    for (const locale of plannerLocales) {
      const copy = plannerCopy(locale);
      expect(Object.keys(copy)).toEqual(Object.keys(baseline));
      for (const key of Object.keys(copy) as (keyof typeof copy)[]) {
        expect(copy[key].trim()).not.toBe("");
        expect(copy[key].match(/\{\w+\}/g)).toEqual(baseline[key].match(/\{\w+\}/g));
      }
    }
    expect(plannerCopy("unknown")).toEqual(baseline);
  });
});
