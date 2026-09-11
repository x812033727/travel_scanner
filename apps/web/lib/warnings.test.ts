import { describe, expect, it } from "vitest";
import { translateWarnings } from "./warnings";

const known = new Set(["walk_route_beta", "weather_beyond_forecast"]);
const translate = (key: string) => `translated:${key}`;

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
