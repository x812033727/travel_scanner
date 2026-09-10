import { afterEach, describe, expect, it, vi } from "vitest";
import { loadInitialFoods } from "./foods.server";

const cities = { countries: [{ code: "JP", name: "日本", cities: [] }] };
const categories = { items: [{ slug: "ramen", name: "拉麵" }] };
const merchants = { items: [{ id: "1", name: "一蘭" }], next_cursor: null };

afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); });

function stub(...payloads: unknown[]) {
  const fetch = vi.fn();
  for (const payload of payloads) fetch.mockResolvedValueOnce(new Response(JSON.stringify(payload)));
  vi.stubGlobal("fetch", fetch);
  vi.stubEnv("API_INTERNAL_URL", "http://api.test");
  return fetch;
}

describe("loadInitialFoods", () => {
  it("hands the merchant list to the server render, not just the filters", async () => {
    // /foods used to server-render the city and category pickers over an empty list: the
    // merchants themselves arrived in a useEffect, so a crawler saw filter controls and nothing
    // to filter.
    const fetch = stub(cities, categories, merchants);
    const initial = await loadInitialFoods("zh-TW");
    expect(initial.merchants).toEqual(merchants);
    expect(fetch.mock.calls.map((call) => call[0])).toEqual([
      "http://api.test/api/v1/foods/cities",
      "http://api.test/api/v1/foods/categories",
      "http://api.test/api/v1/foods/merchants?limit=20",
    ]);
  });

  it("caches the public lists instead of going back to origin every request", async () => {
    const fetch = stub(cities, categories, merchants);
    await loadInitialFoods("en");
    const options = fetch.mock.calls.map((call) => call[1]);
    expect(options[0]).toMatchObject({ next: { revalidate: 3600 } });
    expect(options[2]).toMatchObject({ next: { revalidate: 900 } });
    for (const option of options) {
      expect(option).not.toHaveProperty("cache");
      expect(option.headers).toMatchObject({ "X-Travel-Locale": "en" });
    }
  });

  it("only asks for the unfiltered page, which is the one a crawler lands on", async () => {
    const fetch = stub(cities, categories, merchants);
    await loadInitialFoods("en");
    expect(fetch.mock.calls[2][0]).not.toContain("destination_id");
    expect(fetch.mock.calls[2][0]).not.toContain("category");
  });

  it("gives up the whole seed when the city list is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    expect(await loadInitialFoods("en")).toEqual({ cities: null, categories: null, merchants: null });
  });

  it("still seeds cities and merchants when only the categories call fails", async () => {
    const fetch = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(cities)))
      .mockResolvedValueOnce(new Response("nope", { status: 500 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(merchants)));
    vi.stubGlobal("fetch", fetch);
    const initial = await loadInitialFoods("en");
    expect(initial.cities).toEqual(cities);
    expect(initial.categories).toBeNull();
    expect(initial.merchants).toEqual(merchants);
  });
});
