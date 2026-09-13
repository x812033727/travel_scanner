import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { disabledAdsense } from "./adsense";
import { fetchAdsenseConfig, resetAdsenseConfigCache } from "./adsense-config";

const PUBLISHER = "ca-pub-4140966684432854";
const SLOT = "1234567890";
const enabled = { enabled: true, publisher_id: PUBLISHER, slot_id: SLOT, cmp_enabled: false };

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
    ["a payload that would not render", () => vi.mocked(fetch).mockResolvedValue(reply({ enabled: true, publisher_id: PUBLISHER, slot_id: null, cmp_enabled: false }))],
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

  it("stops trusting a stale answer instead of riding out an outage forever", async () => {
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    const now = Date.now();
    await fetchAdsenseConfig(now);
    vi.mocked(fetch).mockRejectedValue(new Error("ECONNREFUSED"));
    // Each failure must leave the original timestamp alone. Restamping here would reset the
    // clock on every attempt, so "enabled" would outlive any outage and the owner could
    // never switch advertising off while the API was unwell.
    expect(await fetchAdsenseConfig(now + 61_000)).toEqual(enabled);
    expect(await fetchAdsenseConfig(now + 300_000)).toEqual(enabled);
    expect(await fetchAdsenseConfig(now + 600_001)).toEqual(disabledAdsense);
  });

  it("survives an impossible failure rather than taking every page down with it", async () => {
    // proxy.ts awaits this on every request, so a rejection left in the in-flight slot would
    // be handed to every later caller as well.
    vi.mocked(fetch).mockImplementation(() => { throw { toString() { throw new Error("hostile"); } }; });
    expect(await fetchAdsenseConfig()).toEqual(disabledAdsense);
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    expect(await fetchAdsenseConfig(Date.now() + 120_000)).toEqual(enabled);
  });

  it("recovers as soon as the API answers again", async () => {
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    const now = Date.now();
    await fetchAdsenseConfig(now);
    vi.mocked(fetch).mockRejectedValue(new Error("ECONNREFUSED"));
    expect(await fetchAdsenseConfig(now + 700_000)).toEqual(disabledAdsense);
    vi.mocked(fetch).mockResolvedValue(reply(enabled));
    expect(await fetchAdsenseConfig(now + 800_000)).toEqual(enabled);
  });
});
