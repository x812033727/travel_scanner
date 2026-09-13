import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { disabledAdsense } from "./adsense";
import { fetchAdsenseConfig, resetAdsenseConfigCache } from "./adsense-config";

const PUBLISHER = "ca-pub-4140966684432854";
const SLOT = "1234567890";
const enabled = { enabled: true, publisher_id: PUBLISHER, slot_id: SLOT };

function reply(body: unknown, ok = true) {
  return { ok, json: async () => body } as Response;
}

describe("reading the advertising configuration", () => {
  beforeEach(() => {
    resetAdsenseConfigCache();
    vi.stubGlobal("fetch", vi.fn());
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("asks the API once and serves the rest of the minute from memory", async () => {
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    const now = Date.now();
    expect(await fetchAdsenseConfig(now)).toEqual(enabled);
    expect(await fetchAdsenseConfig(now + 59_000)).toEqual(enabled);
    // proxy.ts calls this on every matched request; it must not be a round trip per page view.
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("asks again once the cached answer has expired", async () => {
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    const now = Date.now();
    await fetchAdsenseConfig(now);
    vi.mocked(fetch).mockResolvedValue(reply(disabledAdsense));
    expect(await fetchAdsenseConfig(now + 61_000)).toEqual(disabledAdsense);
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it("collapses a burst on a cold cache into one call", async () => {
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    const answers = await Promise.all([fetchAdsenseConfig(), fetchAdsenseConfig(), fetchAdsenseConfig()]);
    expect(answers).toEqual([enabled, enabled, enabled]);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it.each([
    ["an unreachable API", () => vi.mocked(fetch).mockRejectedValue(new Error("ECONNREFUSED"))],
    ["an error response", () => vi.mocked(fetch).mockResolvedValue(reply(enabled, false))],
    ["a payload that would not render", () => vi.mocked(fetch).mockResolvedValue(reply({ enabled: true, publisher_id: PUBLISHER, slot_id: null }))],
    ["a payload that is not an object", () => vi.mocked(fetch).mockResolvedValue(reply("off"))],
  ])("fails closed on %s", async (_label, arrange) => {
    arrange();
    expect(await fetchAdsenseConfig()).toEqual(disabledAdsense);
  });

  it("keeps the last good answer while the API is briefly unreachable", async () => {
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    const now = Date.now();
    await fetchAdsenseConfig(now);
    vi.mocked(fetch).mockRejectedValue(new Error("ETIMEDOUT"));
    // Otherwise one slow response flips every article page's policy for a full minute.
    expect(await fetchAdsenseConfig(now + 61_000)).toEqual(enabled);
  });
});
