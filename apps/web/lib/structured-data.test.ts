import { describe, expect, it } from "vitest";
import { siteUrl } from "@/lib/seo";
import { breadcrumbs, organization, webSite } from "@/lib/structured-data";

const parse = (value: object) => JSON.parse(JSON.stringify(value));

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
