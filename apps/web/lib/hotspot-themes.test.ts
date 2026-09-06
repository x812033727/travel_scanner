import { describe, expect, it } from "vitest";
import { isInSeason, monthRangeLabel, monthRuns, normalizeMonths } from "./hotspot-themes";

describe("hotspot theme months", () => {
  it("normalizes what the API sends", () => {
    expect(normalizeMonths([4, 3, 3])).toEqual([3, 4]);
    expect(normalizeMonths([0, 13, 4.5, 5])).toEqual([5]);
    expect(normalizeMonths(undefined)).toEqual([]);
  });

  it("joins a run that wraps the year", () => {
    expect(monthRuns([11, 12, 1, 2])).toEqual([[11, 12, 1, 2]]);
    expect(monthRuns([3, 4, 10, 11])).toEqual([
      [3, 4],
      [10, 11],
    ]);
    expect(monthRuns([1, 12])).toEqual([[12, 1]]);
  });

  it("labels a range in the reader's language", () => {
    expect(monthRangeLabel([3, 4], "zh-TW")).toBe("3月–4月");
    expect(monthRangeLabel([3, 4], "zh-CN")).toBe("3月–4月");
    expect(monthRangeLabel([3, 4], "ja")).toBe("3月–4月");
    expect(monthRangeLabel([3, 4], "ko")).toBe("3월–4월");
    expect(monthRangeLabel([3, 4], "en")).toBe("Mar–Apr");
    expect(monthRangeLabel([7], "en")).toBe("Jul");
  });

  it("labels an illumination season that crosses new year, however it arrives", () => {
    expect(monthRangeLabel([11, 12, 1, 2], "zh-TW")).toBe("11月–2月");
    expect(monthRangeLabel([1, 12, 11], "en")).toBe("Nov–Jan");
  });

  it("says nothing for no months and for all year", () => {
    expect(monthRangeLabel([], "en")).toBe("");
    expect(monthRangeLabel([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "en")).toBe("");
  });

  it("marks only season themes as in season", () => {
    expect(isInSeason({ kind: "season", months: [3, 4] }, 4)).toBe(true);
    expect(isInSeason({ kind: "season", months: [3, 4] }, 5)).toBe(false);
    expect(isInSeason({ kind: "shop", months: [] }, 4)).toBe(false);
    expect(isInSeason({ kind: "season", months: [12, 1, 2] }, 1)).toBe(true);
  });
});
