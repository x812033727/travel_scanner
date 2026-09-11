import { describe, expect, it } from "vitest";
import { translateWarnings } from "./warnings";

const known = new Set(["walk_route_beta", "weather_beyond_forecast", "provider_fallback"]);
const translate = (key: string, values?: Record<string, string>) =>
  `translated:${key}${values ? ` ${JSON.stringify(values)}` : ""}`;

describe("translateWarnings", () => {
  it("says a known code in the reader's language", () => {
    expect(translateWarnings(["walk_route_beta"], known, translate))
      .toEqual(["translated:warning.walk_route_beta"]);
  });

  it("says nothing at all about a code this build does not know", () => {
    // A server ahead of this deployment must not put its identifiers on screen.
    expect(translateWarnings(["a_code_from_a_newer_server"], known, translate)).toEqual([]);
  });

  it("keeps provider text that was never a code", () => {
    // Google's weather API is asked for the reader's language and answers with its
    // own advisories; dropping them for not being in the catalog loses real content.
    const advisory = "山區天氣變化較快，請留意即時資訊。";
    expect(translateWarnings([advisory], known, translate)).toEqual([advisory]);
  });

  it("handles a mixed array and a missing one", () => {
    expect(translateWarnings(["weather_beyond_forecast", "Heavy rain advisory", "nope_unknown"], known, translate))
      .toEqual(["translated:warning.weather_beyond_forecast", "Heavy rain advisory"]);
    expect(translateWarnings(undefined, known, translate)).toEqual([]);
  });
});

describe("translateWarnings with parameters", () => {
  it("hands a parameterised code's values to the catalog", () => {
    expect(translateWarnings(["provider_fallback?module=flights&provider=Amadeus"], known, translate))
      .toEqual([`translated:warning.provider_fallback {"module":"flights","provider":"Amadeus"}`]);
  });

  it("decodes values that had to be escaped to survive the string", () => {
    expect(translateWarnings(["provider_fallback?provider=Trip.com+%26+co"], known, translate))
      .toEqual([`translated:warning.provider_fallback {"provider":"Trip.com & co"}`]);
  });

  it("says nothing about a parameterised code this build does not know", () => {
    expect(translateWarnings(["newer_code?day=2026-11-10"], known, translate)).toEqual([]);
  });

  it("still passes a sentence through even when it contains a question mark", () => {
    // A provider advisory is free text, and free text can look like anything.
    const advisory = "Is the pass open? Check before you travel.";
    expect(translateWarnings([advisory], known, translate)).toEqual([advisory]);
  });
});
