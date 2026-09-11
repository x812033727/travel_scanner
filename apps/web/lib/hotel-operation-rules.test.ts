import { describe, expect, it } from "vitest";
import {
  evaluateHotelOperatingStay, hotelOperatingRulesError, isHotelOperationDate,
  readHotelOperationDraft, writeHotelOperationDraft, type HotelOperatingRules,
} from "./hotel-operation-rules";

const range = { start_date: "2026-11-03", end_date: "2026-11-06", reason: "Scheduled closure", source_url: "https://hotel.example.com/notice" };
const rules: HotelOperatingRules = { unavailable_stays: [range] };

describe("hotel accommodation nights", () => {
  it.each([
    ["2026-11-02", "2026-11-03", "allowed"],
    ["2026-11-06", "2026-11-07", "allowed"],
    ["2026-11-02", "2026-11-07", "unavailable"],
    ["2026-11-03", "2026-11-04", "unavailable"],
    ["2026-11-05", "2026-11-06", "unavailable"],
  ])("checks %s to %s at the exclusive boundaries", (start, end, expected) => {
    expect(evaluateHotelOperatingStay(rules, start, end)).toBe(expected);
  });

  it("allows checkout on the hotel's final checkout date, but not afterward", () => {
    const cutoff = { unavailable_stays: [], last_checkout_date: "2026-12-20", last_checkout_reason: "Final day", last_checkout_source_url: range.source_url };
    expect(evaluateHotelOperatingStay(cutoff, "2026-12-19", "2026-12-20")).toBe("allowed");
    expect(evaluateHotelOperatingStay(cutoff, "2026-12-19", "2026-12-21")).toBe("unavailable");
    expect(evaluateHotelOperatingStay(cutoff, "2026-12-20", "2026-12-21")).toBe("unavailable");
  });

  it("requires complete valid dates only when an operating policy exists", () => {
    expect(evaluateHotelOperatingStay(null)).toBe("allowed");
    expect(evaluateHotelOperatingStay(undefined)).toBe("allowed");
    expect(evaluateHotelOperatingStay(rules)).toBe("dates_required");
    expect(evaluateHotelOperatingStay(rules, "2026-11-01")).toBe("dates_required");
    expect(evaluateHotelOperatingStay(rules, "2026-02-30", "2026-03-02")).toBe("invalid");
    expect(evaluateHotelOperatingStay(rules, "2026-11-01", "2026-11-01")).toBe("invalid");
  });
});

describe("operating policy drafts", () => {
  it("accepts adjacent periods and rejects overlapping or duplicate periods", () => {
    expect(hotelOperatingRulesError({ unavailable_stays: [range, { ...range, start_date: range.end_date, end_date: "2026-11-07" }] })).toBeNull();
    expect(hotelOperatingRulesError({ unavailable_stays: [range, { ...range, start_date: "2026-11-05", end_date: "2026-11-07" }] })).toBe("overlappingDates");
    expect(hotelOperatingRulesError({ unavailable_stays: [range, range] })).toBe("overlappingDates");
  });

  it("requires source-backed complete rules without coercing invalid calendars", () => {
    expect(isHotelOperationDate("2028-02-29")).toBe(true);
    expect(isHotelOperationDate("2026-02-29")).toBe(false);
    expect(isHotelOperationDate("0000-01-01")).toBe(false);
    expect(hotelOperatingRulesError({})).toBe("emptyRules");
    expect(hotelOperatingRulesError({ unavailable_stays: [{ ...range, reason: " " }] })).toBe("invalidReason");
    expect(hotelOperatingRulesError({ unavailable_stays: [{ ...range, source_url: "javascript:alert(1)" }] })).toBe("invalidSource");
    expect(hotelOperatingRulesError({ last_checkout_date: "2026-12-20" })).toBe("invalidReason");
    expect(hotelOperatingRulesError({ unavailable_stays: Array.from({ length: 51 }, () => range) })).toBe("tooManyRanges");
  });

  it("preserves unrelated product JSON and clears the policy explicitly with null", () => {
    const product = { title: "Hotel", names_json: { ja: "ホテル" }, facts: { latitude: 25.1, source_credits: [{ name: "Government" }], hotel_operating_rules: rules } };
    const updated = JSON.parse(writeHotelOperationDraft(JSON.stringify(product), { unavailable_stays: [{ ...range, reason: "New notice" }] }));
    expect(updated).toEqual({ ...product, facts: { ...product.facts, hotel_operating_rules: { unavailable_stays: [{ ...range, reason: "New notice" }] } } });
    expect(JSON.parse(writeHotelOperationDraft(JSON.stringify(updated), { unavailable_stays: [] })).facts).toEqual({ ...product.facts, hotel_operating_rules: null });
  });

  it("keeps malformed JSON uneditable and reads changes made in the original JSON editor", () => {
    expect(readHotelOperationDraft('{"facts":')).toEqual({ rules: null, error: "invalidJson", editable: false });
    expect(readHotelOperationDraft('{"facts":{"hotel_operating_rules":[]}}').editable).toBe(false);
    expect(readHotelOperationDraft(JSON.stringify({ facts: { hotel_operating_rules: rules } })).rules).toEqual(rules);
    expect(readHotelOperationDraft(JSON.stringify({ facts: { hotel_operating_rules: null } })).rules).toBeNull();
  });
});
