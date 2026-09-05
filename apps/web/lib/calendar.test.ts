import { describe, expect, it } from "vitest";
import { addDays, addMonths, clampToMonth, dayCount, daysInMonth, formatTripDay, monthGrid, monthTitle, weekStartFor, weekdayLabels } from "./calendar";

describe("calendar helpers", () => {
  it("adds days across month, year and leap boundaries", () => {
    expect(addDays("2026-09-30", 1)).toBe("2026-10-01");
    expect(addDays("2026-12-31", 1)).toBe("2027-01-01");
    expect(addDays("2028-02-28", 1)).toBe("2028-02-29");
    expect(addDays("2026-03-01", -1)).toBe("2026-02-28");
    expect(addDays("2026-11-10", 60)).toBe("2027-01-09");
  });

  it("moves between months and clamps the day of month", () => {
    expect(addMonths("2026-12", 1)).toBe("2027-01");
    expect(addMonths("2026-01", -1)).toBe("2025-12");
    expect(daysInMonth("2026-02")).toBe(28);
    expect(daysInMonth("2028-02")).toBe(29);
    expect(daysInMonth("2026-09")).toBe(30);
    expect(clampToMonth("2026-01-31", "2026-02")).toBe("2026-02-28");
    expect(clampToMonth("2026-01-15", "2026-02")).toBe("2026-02-15");
  });

  it("counts inclusive trip days and treats empty or inverted ranges as zero", () => {
    expect(dayCount("2026-11-10", "2026-11-15")).toBe(6);
    expect(dayCount("2026-11-10", "2026-11-10")).toBe(1);
    expect(dayCount("2026-11-15", "2026-11-10")).toBe(0);
    expect(dayCount("", "2026-11-10")).toBe(0);
  });

  it("lays out a month grid from the locale's first weekday", () => {
    const sundayFirst = monthGrid("2026-09", 7);
    expect(sundayFirst[0]).toEqual([null, null, "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05"]);
    expect(sundayFirst).toHaveLength(5);
    expect(sundayFirst.every((row) => row.length === 7)).toBe(true);
    expect(sundayFirst.flat().filter(Boolean)).toHaveLength(30);
    expect(sundayFirst[4]).toEqual(["2026-09-27", "2026-09-28", "2026-09-29", "2026-09-30", null, null, null]);

    const mondayFirst = monthGrid("2026-09", 1);
    expect(mondayFirst[0]).toEqual([null, "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05", "2026-09-06"]);
    expect(monthGrid("2026-11", 7)[0][0]).toBe("2026-11-01");
  });

  it("starts the week on Monday only for simplified Chinese", () => {
    expect(weekStartFor("zh-CN")).toBe(1);
    expect(weekStartFor("zh-TW")).toBe(7);
    expect(weekStartFor("en")).toBe(7);
    expect(weekStartFor("")).toBe(7);
  });

  it("formats headers, titles and days with Intl for every locale", () => {
    const sunday = new Intl.DateTimeFormat("en", { weekday: "short", timeZone: "UTC" }).format(new Date("2024-01-07T00:00:00Z"));
    const monday = new Intl.DateTimeFormat("en", { weekday: "long", timeZone: "UTC" }).format(new Date("2024-01-08T00:00:00Z"));
    expect(weekdayLabels("en", 7)[0].short).toBe(sunday);
    expect(weekdayLabels("en", 1)[0].long).toBe(monday);
    expect(weekdayLabels("zh-TW", 7)).toHaveLength(7);
    expect(monthTitle("zh-TW", "2026-11")).toBe("2026年11月");
    expect(monthTitle("en", "2026-11")).toBe("November 2026");
    expect(formatTripDay("zh-TW", "2026-11-10")).toContain("2026年11月10日");
    expect(formatTripDay("en", "2026-11-10")).toContain("November 10, 2026");
    expect(formatTripDay("ja", "2026-11-10")).toContain("2026年11月10日");
    expect(formatTripDay("ko", "")).toBe("");
  });
});
