import { describe, expect, it } from "vitest";
import {
  activeFilterCount,
  findCity,
  foodBrowserSearch,
  merchantsQuery,
  primaryMapLink,
  readFoodBrowserFilters,
  sortCitiesByMerchants,
  type FoodCity,
} from "./foods";

function city(id: string, merchantCount: number): FoodCity {
  return {
    id,
    name: id,
    local_name: null,
    english_name: null,
    country_code: "JP",
    role: "primary",
    parent_destination_id: null,
    merchant_count: merchantCount,
    area_count: 4,
  };
}

describe("food browser filters", () => {
  it("reads and writes the query string in a stable order", () => {
    const filters = readFoodBrowserFilters(
      "?category=ramen&q=%20noodles%20&destination_id=tokyo&area=tokyo-shinjuku",
    );
    expect(filters).toEqual({
      destinationId: "tokyo",
      area: "tokyo-shinjuku",
      category: "ramen",
      query: "noodles",
    });
    expect(foodBrowserSearch(filters)).toBe(
      "destination_id=tokyo&area=tokyo-shinjuku&category=ramen&q=noodles",
    );
    expect(foodBrowserSearch({ destinationId: "", area: "", category: "", query: "" })).toBe("");
    expect(activeFilterCount(filters)).toBe(4);
    expect(activeFilterCount(readFoodBrowserFilters(""))).toBe(0);
  });

  it("builds merchant queries with the limit and cursor", () => {
    expect(merchantsQuery({ destinationId: "tokyo", area: "", category: "", query: "" })).toBe(
      "destination_id=tokyo&limit=20",
    );
    expect(
      merchantsQuery({ destinationId: "", area: "", category: "", query: "" }, "MjA", 10),
    ).toBe("limit=10&cursor=MjA");
  });

  it("prefers the primary map link and lists cities with merchants first", () => {
    expect(
      primaryMapLink([
        { provider: "google", label: "Google Maps", url: "https://g", primary: false },
        { provider: "naver", label: "Naver Map", url: "https://n", primary: true },
      ])?.url,
    ).toBe("https://n");
    expect(primaryMapLink([])).toBeUndefined();
    const cities = [city("a", 0), city("b", 2), city("c", 5)];
    expect(sortCitiesByMerchants(cities).map((item) => item.id)).toEqual(["c", "b", "a"]);
    expect(findCity([{ code: "JP", name: "日本", merchant_count: 7, cities }], "b")?.id).toBe("b");
    expect(findCity([], "b")).toBeUndefined();
  });
});
