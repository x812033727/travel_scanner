import { describe, expect, it } from "vitest";
import { siteUrl } from "@/lib/seo";
import { breadcrumbs, itemList, organization, touristDestination, webSite } from "@/lib/structured-data";

const parse = (value: object | null) => JSON.parse(JSON.stringify(value));

describe("organization", () => {
  it("names the brand and an absolute logo", () => {
    const data = parse(organization()) as Record<string, string>;
    expect(data["@context"]).toBe("https://schema.org");
    expect(data["@type"]).toBe("Organization");
    expect(data.name).toBe("Mokaair");
    expect(data.url).toBe(siteUrl);
    expect(data.logo.startsWith(`${siteUrl}/`)).toBe(true);
  });
});

describe("webSite", () => {
  it("omits a search action when its destination feature is closed or unavailable", () => {
    expect(parse(webSite("en", false))).not.toHaveProperty("potentialAction");
    expect(parse(webSite("en", false)).name).toBe("Mokaair");
  });
  it("describes this locale's tree, not the bare origin", () => {
    const data = parse(webSite("ja")) as Record<string, string>;
    expect(data.url).toBe(`${siteUrl}/ja`);
    expect(data.inLanguage).toBe("ja");
  });

  it("points the search action at a URL that really filters", () => {
    // /hotspots reads `q` and passes it to the ranking query, so this is an endpoint a reader
    // can land on rather than a shape invented to earn a sitelinks search box.
    const action = parse(webSite("en")).potentialAction;
    expect(action["@type"]).toBe("SearchAction");
    expect(action.target.urlTemplate).toBe(`${siteUrl}/en/hotspots?q={search_term_string}`);
    expect(action["query-input"]).toBe("required name=search_term_string");
  });
});

describe("breadcrumbs", () => {
  it("numbers the trail from one and resolves each step for the locale", () => {
    const data = parse(breadcrumbs("zh-TW", [
      { name: "首頁", path: "/" },
      { name: "熱門景點", path: "/hotspots" },
    ]));
    expect(data["@type"]).toBe("BreadcrumbList");
    expect(data.itemListElement).toEqual([
      { "@type": "ListItem", position: 1, name: "首頁", item: `${siteUrl}/zh-TW` },
      { "@type": "ListItem", position: 2, name: "熱門景點", item: `${siteUrl}/zh-TW/hotspots` },
    ]);
  });
});

describe("itemList", () => {
  it("numbers entries from one and resolves each URL for the locale", () => {
    const data = parse(itemList("ja", [
      { name: "東京", path: "/destinations/tokyo" },
      { name: "ソウル", path: "/destinations/seoul" },
    ]));
    expect(data["@type"]).toBe("ItemList");
    expect(data.itemListElement).toEqual([
      { "@type": "ListItem", position: 1, name: "東京", url: `${siteUrl}/ja/destinations/tokyo` },
      { "@type": "ListItem", position: 2, name: "ソウル", url: `${siteUrl}/ja/destinations/seoul` },
    ]);
  });
});

describe("touristDestination", () => {
  const tokyo = {
    name: "Tokyo", path: "/destinations/tokyo", description: "A dense, legible first trip to Japan.",
    country: "Japan", alternateName: ["東京", "Tokyo"], center: { latitude: 35.6812, longitude: 139.7671 },
  };

  it("describes the place, its country and its coordinates", () => {
    const data = parse(touristDestination("en", tokyo));
    expect(data["@type"]).toBe("TouristDestination");
    expect(data.url).toBe(`${siteUrl}/en/destinations/tokyo`);
    expect(data.containedInPlace).toEqual({ "@type": "Country", name: "Japan" });
    expect(data.geo).toEqual({ "@type": "GeoCoordinates", latitude: 35.6812, longitude: 139.7671 });
  });

  it("does not repeat the heading as an alternate name", () => {
    // english_name matches `name` on the English page; the original script is the useful half.
    expect(parse(touristDestination("en", tokyo)).alternateName).toEqual(["東京"]);
  });

  it("leaves out fields the catalog has no value for, rather than emitting empty ones", () => {
    const data = parse(touristDestination("ko", {
      name: "가마쿠라", path: "/destinations/kamakura", description: "", country: "", center: null,
    }));
    expect(data).not.toHaveProperty("description");
    expect(data).not.toHaveProperty("containedInPlace");
    expect(data).not.toHaveProperty("geo");
    expect(data).not.toHaveProperty("alternateName");
    expect(data.name).toBe("가마쿠라");
  });
});

describe("empty graphs", () => {
  it("returns null rather than an empty BreadcrumbList or ItemList", () => {
    // Rich Results treats an empty itemListElement as an invalid object, so there is nothing
    // useful to emit. The component drops nulls instead of writing them into the document.
    expect(breadcrumbs("en", [])).toBeNull();
    expect(itemList("en", [])).toBeNull();
  });
});

describe("touristDestination language", () => {
  it("does not claim inLanguage, which is not a Place property", () => {
    const data = parse(touristDestination("ja", {
      name: "東京", path: "/destinations/tokyo", description: "", country: "", center: null,
    }));
    expect(data).not.toHaveProperty("inLanguage");
  });
});
