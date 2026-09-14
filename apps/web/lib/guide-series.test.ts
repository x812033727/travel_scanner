import { describe, expect, it } from "vitest";
import { filterSeries, isGuideSeries, readSeriesFilters, type GuideSeries } from "./guide-series";

const series: GuideSeries = {
  slug: "claude-code", locale: "zh-TW", hub: { slug: "claude-code-tutorials", kind: "life", title: "目錄" },
  groups: [{ id: "D", title: "MD 設定" }], paths: [{ id: "md", title: "規則", slugs: ["claude-code-memory", "claude-code-md"] }],
  entries: [
    { kind: "life", slug: "claude-code-md", title: "CLAUDE.md 設定", description: "規則", number: 20, group: "D", level: "beginner", platforms: ["cli"], aliases: ["MD", "記憶"], minutes: 4 },
    { kind: "life", slug: "claude-code-memory", title: "上下文", description: "整理", number: 28, group: "E", level: "intermediate", platforms: ["cli", "desktop"], aliases: ["/compact", "記憶"], minutes: 5 },
  ],
};
const empty = readSeriesFilters(new URLSearchParams());
describe("series lookup", () => {
  it("searches Chinese, commands, filenames and full-width Latin text", () => {
    for (const q of ["MD", "CLAUDE.md", "ＣＬＡＵＤＥ.md"]) expect(filterSeries(series, { ...empty, q }).map(x => x.number)).toEqual([20]);
    expect(filterSeries(series, { ...empty, q: "/compact" }).map(x => x.number)).toEqual([28]);
    expect(filterSeries(series, { ...empty, q: "記憶" })).toHaveLength(2);
  });
  it("combines filters and preserves recommended path order", () => {
    expect(filterSeries(series, { ...empty, q: "記憶", platform: "desktop", level: "beginner" })).toEqual([]);
    expect(filterSeries(series, { ...empty, path: "md" }).map(x => x.number)).toEqual([28, 20]);
    expect(filterSeries(series, { ...empty, group: "D" }).map(x => x.number)).toEqual([20]);
  });
  it("rejects malformed upstream responses", () => {
    expect(isGuideSeries(series)).toBe(true);
    expect(isGuideSeries({ ...series, entries: [{ ...series.entries[0], slug: "../secret" }] })).toBe(false);
    expect(isGuideSeries({ ...series, paths: [{ id: "md", title: "MD", slugs: [12] }] })).toBe(false);
  });
});
