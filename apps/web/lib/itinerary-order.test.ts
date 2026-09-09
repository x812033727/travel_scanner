import { describe, expect, it } from "vitest";
import { dayTimeline, insertionNeighbors, insertionPoints, normalizeOrder, placeAt } from "./itinerary-order";
import { type TripItem } from "./trip-types";
import { itineraryCopy, itineraryText } from "./itinerary-copy";

it("keeps all five itinerary catalogs and interpolation parameters complete", () => {
  const reference = itineraryCopy("en");
  const parameters = (value: string) => [...value.matchAll(/\{(\w+)\}/g)].map((match) => match[1]).sort();
  for (const locale of ["en", "ja", "ko", "zh-TW", "zh-CN"]) {
    const copy = itineraryCopy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(reference).sort());
    for (const key of Object.keys(reference) as (keyof typeof reference)[]) {
      expect(copy[key].trim()).not.toBe("");
      expect(parameters(copy[key])).toEqual(parameters(reference[key]));
    }
  }
  expect(itineraryText(reference.context, { day: 2, before: "A", after: "B" })).toBe("Day 2 · A → B");
});

const day = "2026-11-11";
function stop(id: string, position: number, system_role?: TripItem["system_role"]): TripItem {
  return { id, position, system_role, day_date: day, item_type: "custom", title: id,
    data: {}, locked: Boolean(system_role), is_estimated: false };
}
const rows = [stop("flight", 0, "outbound_flight"), stop("hotel", 1, "hotel_start"),
  stop("a", 2), stop("lunch", 3, "lunch"), stop("b", 4),
  stop("dinner", 5, "dinner"), stop("end", 6, "hotel_end"), stop("return", 7, "return_flight")];
const ids = (items: TripItem[]) => items.map((item) => item.id);

describe("itinerary insertion positions", () => {
  it("offers all city-route gaps, including between anchors, but no flight/hotel exterior", () => {
    expect(insertionPoints(rows, day).map((point) => point.beforeId)).toEqual(["a", "lunch", "b", "dinner", "end"]);
    expect(insertionPoints(rows, day, "a").map((point) => point.beforeId)).toEqual(["lunch", "b", "dinner", "end"]);
  });
  it("moves a single ordinary stop across meals without moving anchors or fixed time", () => {
    const a = { ...rows[2], fixed_time: true, start_time: day + "T10:00:00+09:00" };
    const next = placeAt(rows.filter((row) => row.id !== "b"), a, { day, beforeId: "end" });
    expect(ids(next)).toEqual(["flight", "hotel", "lunch", "dinner", "a", "end", "return"]);
    expect(next.find((row) => row.id === "a")?.start_time).toBe(a.start_time);
    expect(ids(normalizeOrder(next))).toEqual(ids(next));
  });
  it("inserts repeated picks in the selected gap, not at the end", () => {
    const point = { day, beforeId: "lunch" };
    const first = placeAt(rows, stop("c", 0), point);
    expect(ids(placeAt(first, stop("d", 0), point))).toEqual(["flight", "hotel", "a", "c", "d", "lunch", "b", "dinner", "end", "return"]);
  });
  it("moves between days, preserving unique positions on both and the final hotel", () => {
    const nextDay = "2026-11-12";
    const other = [stop("hotel2", 0, "hotel_start"), stop("end2", 1, "hotel_end")]
      .map((row) => ({ ...row, day_date: nextDay }));
    const next = placeAt([...rows, ...other], rows[2], { day: nextDay });
    expect(ids(dayTimeline(next, nextDay))).toEqual(["hotel2", "a", "end2"]);
    expect(dayTimeline(next, day).map((row) => row.position)).toEqual([0, 1, 2, 3, 4, 5, 6]);
  });
  it("ignores skipped meals and flights when finding reference locations", () => {
    const located = rows.map((row) => ({ ...row, latitude: 35, longitude: 139, is_skipped: row.id === "lunch" }));
    const neighbors = insertionNeighbors(located, { day, beforeId: "b" });
    expect(neighbors.before?.id).toBe("a");
    expect(neighbors.reference?.id).toBe("a");
    expect(neighbors.after?.id).toBe("b");
  });
});
