import { describe, expect, it } from "vitest";
import { buildStay22Map, type Stay22MapContext } from "./stay22";
import { stay22Copy, stay22Text } from "./stay22-copy";

const now = new Date("2026-09-08T08:00:00Z");
const area = { latitude: 35.71, longitude: 139.79 };
const context: Stay22MapContext = { destination_id: "tokyo", country_code: "JP", city_code: "NRT", check_in: "2026-11-10", check_out: "2026-11-15", travelers: { adults: 2, children: 0, rooms: 1 } };
const mapFor = (changes: Partial<Stay22MapContext> = {}) => buildStay22Map({ ...context, ...changes }, area, now)!;

describe("Stay22 Maps URL contract", () => {
  it("uses only the fixed affiliate, public center and supported search fields", () => {
    const extendedArea = { ...area, name: "private name" };
    const map = buildStay22Map({ ...context, trip_id: "private-id", title: "secret title", token: "private-token" } as Stay22MapContext, extendedArea, now)!;
    const url = new URL(map.url);
    expect(url.origin + url.pathname).toBe("https://www.stay22.com/embed/gm");
    expect(Object.fromEntries(url.searchParams)).toEqual({ aid: "mokaair", lat: "35.71000", lng: "139.79000", campaign: "mokaair_stays_tokyo", currency: "TWD", showhotels: "true", priceper: "nightly", unitsystem: "metric", maincolor: "0F6F6C", fontcolor: "FFFFFF", zoom: "14", viewmode: "map", scroll: "disabled", checkin: "2026-11-10", checkout: "2026-11-15", adults: "2", children: "0", rooms: "1" });
    expect(map.datesProvided && map.guestsProvided).toBe(true);
    expect(map.hasChildren).toBe(false);
    expect(map.url).not.toMatch(/private|secret|token/);
  });
  it("requires a canonical pilot and plausible public area coordinates", () => {
    expect(buildStay22Map(null, area, now)).toBeNull();
    expect(buildStay22Map(context, undefined, now)).toBeNull();
    for (const changes of [{ destination_id: "seoul" }, { destination_id: "__proto__" }, { city_code: "TPE" }, { country_code: "KR" }]) expect(mapFor(changes)).toBeNull();
    for (const invalid of [{ latitude: NaN, longitude: 139 }, { latitude: Infinity, longitude: 139 }, { latitude: 35.7, longitude: 181 }, { latitude: 25, longitude: 121 }]) expect(buildStay22Map(context, invalid, now)).toBeNull();
    const taipei = buildStay22Map({ ...context, destination_id: "taipei", country_code: "TW", city_code: "TPE" }, { latitude: 25.17, longitude: 121.44 }, now)!;
    expect(new URL(taipei.url).searchParams.get("campaign")).toBe("mokaair_stays_taipei");
  });
  it.each([
    [null, null], ["2026-11-10", null], ["2026-09-07", "2026-09-09"],
    ["2026-11-10", "2026-11-10"], ["2026-11-15", "2026-11-10"],
    ["2027-02-29", "2027-03-02"], ["2026-04-31", "2026-05-02"],
    ["2026-1-01", "2026-11-15"], ["2026-11-10&aid=evil", "2026-11-15"],
  ])("does not send missing, invalid or past dates (%s, %s)", (check_in, check_out) => {
    const map = mapFor({ check_in, check_out });
    expect(map.datesProvided).toBe(false);
    expect(map.checkIn).toBeNull();
    expect(new URL(map.url).searchParams.has("checkin")).toBe(false);
    expect(new URL(map.url).searchParams.has("checkout")).toBe(false);
  });
  it("accepts leap dates and long stays without silently shortening them", () => {
    const map = mapFor({ check_in: "2028-02-29", check_out: "2028-04-01" });
    expect(map.checkOut).toBe("2028-04-01");
    expect(map.datesProvided).toBe(true);
  });
  it("uses destination midnight instead of UTC to reject past check-in", () => {
    expect(buildStay22Map({ ...context, check_in: "2026-09-08" }, area, new Date("2026-09-08T15:01:00Z"))?.datesProvided).toBe(false);
    expect(buildStay22Map({ ...context, check_in: "2026-09-09" }, area, new Date("2026-09-08T15:01:00Z"))?.datesProvided).toBe(true);
  });
  it.each([null, { adults: 0, children: 0, rooms: 1 }, { adults: 2.5, children: 0, rooms: 1 }, { adults: 10, children: 0, rooms: 1 }, { adults: 2, children: -1, rooms: 1 }, { adults: 2, children: 0, rooms: 5 }, { adults: NaN, children: 0, rooms: 1 }])("omits incomplete/invalid party data without inventing counts", (travelers) => {
    const map = mapFor({ travelers });
    expect(map.guestsProvided).toBe(false);
    for (const key of ["adults", "children", "rooms"]) expect(new URL(map.url).searchParams.has(key)).toBe(false);
  });
  it("passes children separately from adults", () => {
    const map = mapFor({ travelers: { adults: 2, children: 2, rooms: 2 } });
    expect(map.hasChildren).toBe(true);
    expect(new URL(map.url).searchParams.get("adults")).toBe("2");
    expect(new URL(map.url).searchParams.get("children")).toBe("2");
  });
});

describe("Stay22 five-language copy", () => {
  const reference = stay22Copy("en");
  it.each(["zh-TW", "zh-CN", "en", "ja", "ko"])("keeps keys, placeholders and disclosure complete in %s", (locale) => {
    const copy = stay22Copy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(reference).sort());
    for (const key of Object.keys(reference) as Array<keyof typeof reference>) {
      expect(copy[key].trim().length).toBeGreaterThan(0);
      expect(copy[key].match(/\{\w+\}/g)?.sort()).toEqual(reference[key].match(/\{\w+\}/g)?.sort());
    }
    expect(stay22Text(copy.guests, { adults: 2, children: 1, rooms: 2 })).not.toMatch(/[{}]/);
  });
});
