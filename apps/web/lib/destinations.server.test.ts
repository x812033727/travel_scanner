import { afterEach, describe, expect, it, vi } from "vitest";
import { loadDestination, loadDestinations, loadMerchants, loadPlaces } from "./destinations.server";
import enHotspots from "@/messages/en/hotspots.json";
import zhTwHotspots from "@/messages/zh-TW/hotspots.json";
import zhCnHotspots from "@/messages/zh-CN/hotspots.json";
import jaHotspots from "@/messages/ja/hotspots.json";
import koHotspots from "@/messages/ko/hotspots.json";

vi.mock("next-intl/server", () => ({
  getTranslations: async ({ locale }: { locale: string }) => {
    const catalogs = { en: enHotspots, "zh-TW": zhTwHotspots, "zh-CN": zhCnHotspots, ja: jaHotspots, ko: koHotspots };
    const categories = (catalogs[locale as keyof typeof catalogs] ?? enHotspots).categories as Record<string, string>;
    return Object.assign((key: string) => categories[key.replace("categories.", "")], {
      has: (key: string) => Object.hasOwn(categories, key.replace("categories.", "")),
    });
  },
}));

const tokyo = {
  id: "tokyo", code: "NRT", city: "東京", local_name: "東京", english_name: "Tokyo",
  country: "日本", country_code: "JP", role: "primary", parent_destination_id: null,
  extension_ids: ["yokohama", "kamakura"], areas: ["新宿", "澀谷"],
  recommended_days: { min: 4, max: 6 }, timezone: "Asia/Tokyo", currency: "JPY",
  center: { latitude: 35.68, longitude: 139.76 }, reason: "第一次去日本最順的城市。", searchable: true,
};

const respond = (payload: unknown) => vi.fn().mockImplementation(async () => new Response(JSON.stringify(payload)));

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

describe("loadDestinations", () => {
  it("asks the API in the reader's locale and caches instead of going back every request", async () => {
    const fetch = respond({ total: 1, items: [tokyo] });
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test/");

    const rows = await loadDestinations("ja");
    expect(rows).toHaveLength(1);
    expect(rows?.[0]).toMatchObject({
      id: "tokyo", city: "東京", country: "日本", localName: "東京", englishName: "Tokyo",
      areas: ["新宿", "澀谷"], recommendedDays: { min: 4, max: 6 },
      center: { latitude: 35.68, longitude: 139.76 }, extensionIds: ["yokohama", "kamakura"],
    });
    // None of this is personalized, and a round trip per request lands in TTFB and so in LCP.
    expect(fetch).toHaveBeenCalledWith(
      "http://api.test/api/v1/destinations",
      expect.objectContaining({
        next: { revalidate: 3600 },
        headers: { Accept: "application/json", "X-Travel-Locale": "ja" },
      }),
    );
  });

  it("drops rows with no id or no name rather than rendering a blank card", async () => {
    vi.stubGlobal("fetch", respond({ items: [tokyo, { id: "broken" }, { city: "No id" }] }));
    expect(await loadDestinations("en")).toHaveLength(1);
  });

  it.each([
    ["a transport failure", vi.fn().mockRejectedValue(new Error("offline"))],
    ["an error status", vi.fn().mockResolvedValue(new Response("nope", { status: 503 }))],
    ["an empty catalog", respond({ items: [] })],
    ["an unexpected shape", respond({ items: "not-an-array" })],
  ])("reports %s as no catalog, so the caller can decide", async (_label, fetch) => {
    vi.stubGlobal("fetch", fetch);
    expect(await loadDestinations("en")).toBeNull();
  });
});

describe("loadDestination", () => {
  it("finds one destination and reports an unknown id as missing", async () => {
    vi.stubGlobal("fetch", respond({ items: [tokyo] }));
    expect((await loadDestination("ja", "tokyo"))?.city).toBe("東京");
    expect(await loadDestination("ja", "atlantis")).toBeNull();
  });
});

describe("guide listings", () => {
  it("server-renders the ranked places, labelled by area", async () => {
    const fetch = respond({ items: [{ id: "h1", name: "淺草寺", area: { code: "asakusa", name: "上野／淺草" }, category: "landmark" }] });
    vi.stubGlobal("fetch", fetch);
    vi.stubEnv("API_INTERNAL_URL", "http://api.test");
    expect(await loadPlaces("zh-TW", "tokyo")).toEqual([{ id: "h1", name: "淺草寺", detail: "上野／淺草" }]);
    expect(fetch.mock.calls[0][0]).toBe("http://api.test/api/v1/hotspots/rankings?destination_id=tokyo&limit=12");
  });

  it("falls back to the category when a place has no area", async () => {
    vi.stubGlobal("fetch", respond({ items: [{ id: "h2", name: "Shibuya Sky", area: null, category: "viewpoint" }] }));
    expect(await loadPlaces("en", "tokyo")).toEqual([{ id: "h2", name: "Shibuya Sky", detail: enHotspots.categories.viewpoint }]);
  });

  it("labels merchants by area, then by their first category", async () => {
    vi.stubGlobal("fetch", respond({
      items: [
        { id: "m1", name: "一蘭", area: { name: "新宿" }, categories: [{ name: "拉麵" }] },
        { id: "m2", name: "Nakamura", area: null, categories: [{ name: "Sushi" }] },
        { id: "m3", name: "No name at all", area: null, categories: [] },
      ],
    }));
    expect(await loadMerchants("zh-TW", "tokyo")).toEqual([
      { id: "m1", name: "一蘭", detail: "新宿" },
      { id: "m2", name: "Nakamura", detail: "Sushi" },
      { id: "m3", name: "No name at all", detail: null },
    ]);
  });

  it("distinguishes an unreachable listing from a confirmed empty list", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    expect(await loadPlaces("en", "tokyo")).toBeNull();
    expect(await loadMerchants("en", "tokyo")).toBeNull();
    vi.stubGlobal("fetch", respond({ items: [] }));
    expect(await loadPlaces("en", "tokyo")).toEqual([]);
    expect(await loadMerchants("en", "tokyo")).toEqual([]);
  });

  it.each([
    ["en", enHotspots.categories.viewpoint], ["zh-TW", zhTwHotspots.categories.viewpoint],
    ["zh-CN", zhCnHotspots.categories.viewpoint], ["ja", jaHotspots.categories.viewpoint],
    ["ko", koHotspots.categories.viewpoint],
  ])("uses existing localized category text in %s", async (locale, detail) => {
    vi.stubGlobal("fetch", respond({ items: [{ id: "h2", name: "Shibuya Sky", category: "viewpoint" }] }));
    expect((await loadPlaces(locale, "tokyo"))?.[0].detail).toBe(detail);
  });

  it("does not expose an unknown internal category code", async () => {
    vi.stubGlobal("fetch", respond({ items: [{ id: "h2", name: "Shibuya Sky", category: "internal_test" }] }));
    expect((await loadPlaces("zh-TW", "tokyo"))?.[0].detail).toBeNull();
  });

  it("does not persist either moderated listing, and bounds network waits", async () => {
    const fetch = respond({ items: [] });
    vi.stubGlobal("fetch", fetch);
    await loadPlaces("en", "tokyo");
    await loadMerchants("en", "tokyo");
    for (const [, options] of fetch.mock.calls) {
      expect(options).toMatchObject({ cache: "no-store" });
      expect(options).not.toHaveProperty("next");
      expect(options.signal).toBeInstanceOf(AbortSignal);
    }
  });
});

describe("payloads that used to take the page down", () => {
  it("skips a null row instead of throwing", async () => {
    // toSummary ran outside the try/catch, so one null item in the array turned a page whose
    // whole design is "degrade, do not fall over" into a 500.
    vi.stubGlobal("fetch", respond({ items: [null, tokyo, "not an object", 42] }));
    const rows = await loadDestinations("en");
    expect(rows).toHaveLength(1);
    expect(rows?.[0].id).toBe("tokyo");
  });

  it("reports a partial recommended_days as absent rather than as zero", async () => {
    // {min: 3} used to render "3–0 days" on the destination index, which guards on min alone.
    vi.stubGlobal("fetch", respond({ items: [{ ...tokyo, recommended_days: { min: 3 } }] }));
    expect((await loadDestinations("en"))?.[0].recommendedDays).toBeNull();
  });

  it("drops blank areas rather than rendering an empty pill", async () => {
    vi.stubGlobal("fetch", respond({ items: [{ ...tokyo, areas: ["新宿", "", "   ", 7] }] }));
    expect((await loadDestinations("en"))?.[0].areas).toEqual(["新宿"]);
  });

  it("trims padding before it reaches the DOM and the JSON-LD", async () => {
    vi.stubGlobal("fetch", respond({ items: [{ ...tokyo, city: "  Tokyo Tower  " }] }));
    expect((await loadDestinations("en"))?.[0].city).toBe("Tokyo Tower");
  });

  it("gives same-named entries distinct keys when the API omits ids", async () => {
    // Chains share a name within one city; keying the list by name collided in React.
    vi.stubGlobal("fetch", respond({ items: [{ name: "7-Eleven" }, { name: "7-Eleven" }] }));
    const entries = await loadMerchants("en", "tokyo");
    expect(new Set(entries?.map((entry) => entry.id)).size).toBe(2);
  });
});
