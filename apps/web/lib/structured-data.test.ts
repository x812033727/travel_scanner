import { describe, expect, it } from "vitest";
import { siteUrl } from "@/lib/seo";
import { breadcrumbs, guideArticle, itemList, organization, touristDestination, webSite } from "@/lib/structured-data";

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

describe("guideArticle", () => {
  const article = {
    path: "/guides/howto/seoul-subway-t-money-guide",
    title: "首爾地鐵與 T-money 全攻略",
    description: "成人基本票價 1,550 韓元，30 分鐘內免費轉乘。",
    publishedAt: "2026-09-13T00:00:00Z",
    section: "How-to guides",
  };

  it("describes the article at its own locale-prefixed URL", () => {
    const data = parse(guideArticle("zh-TW", article)) as Record<string, string>;
    expect(data["@type"]).toBe("Article");
    expect(data.headline).toBe(article.title);
    // `name` as well as `headline`: the five documents whose title runs past Google's 110
    // characters warn on `headline`, and truncating it would contradict the visible <h1>.
    expect(data.name).toBe(article.title);
    expect(data.url).toBe(`${siteUrl}/zh-TW/guides/howto/seoul-subway-t-money-guide`);
    expect(data.inLanguage).toBe("zh-TW");
    expect(data.articleSection).toBe("How-to guides");
    expect(data.isAccessibleForFree).toBe(true);
  });

  it("falls back to the publication date when nothing has been republished", () => {
    expect(parse(guideArticle("en", article)).dateModified).toBe(article.publishedAt);
    const moved = parse(guideArticle("en", { ...article, modifiedAt: "2026-09-14T00:00:00Z" }));
    expect(moved.dateModified).toBe("2026-09-14T00:00:00Z");
  });

  it("carries the sources the page lists, and no claim about when they were written", () => {
    const data = parse(guideArticle("en", {
      ...article,
      references: [
        { title: "Seoul Metro fares", url: "https://www.seoulmetro.co.kr/fares", checkedOn: "2026-09-13" },
        { title: "T-money notices", url: "https://www.t-money.co.kr/notice", checkedOn: "2026-09-14" },
      ],
    }));
    expect(data.citation).toEqual([
      { "@type": "CreativeWork", name: "Seoul Metro fares", url: "https://www.seoulmetro.co.kr/fares" },
      { "@type": "CreativeWork", name: "T-money notices", url: "https://www.t-money.co.kr/notice" },
    ]);
    // `checked_on` says when we read the source, so it belongs to this page's review date and
    // never to the cited work -- which is also why there is no `dateAccessed`, a property
    // schema.org does not define.
    expect(data.citation.every((row: Record<string, unknown>) => !("dateAccessed" in row))).toBe(true);
    expect(data.mainEntityOfPage).toEqual({
      "@type": "WebPage",
      "@id": `${siteUrl}/en/guides/howto/seoul-subway-t-money-guide`,
      lastReviewed: "2026-09-14",
      reviewedBy: { "@type": "Organization", name: "Mokaair", url: siteUrl, logo: `${siteUrl}/brand/mokaair-monogram.png` },
    });
  });

  it("reviews on the newest check, and says nothing when no source carries one", () => {
    const undated = parse(guideArticle("en", {
      ...article,
      references: [{ title: "A source", url: "https://example.com/a", checkedOn: null }],
    }));
    expect(undated.mainEntityOfPage).not.toHaveProperty("lastReviewed");
    expect(undated.citation).toHaveLength(1);
    // Out of order on purpose: the newest wins, not the last one listed.
    const mixed = parse(guideArticle("en", {
      ...article,
      references: [
        { title: "Newer", url: "https://example.com/b", checkedOn: "2026-09-14" },
        { title: "Older", url: "https://example.com/c", checkedOn: "2026-09-01" },
      ],
    }));
    expect(mixed.mainEntityOfPage.lastReviewed).toBe("2026-09-14");
  });

  it("omits every optional field rather than emitting an empty one", () => {
    const data = parse(guideArticle("en", { ...article, references: [], keywords: [] }));
    for (const key of ["citation", "keywords", "about", "image", "timeRequired", "expires", "mainEntity"]) {
      expect(data).not.toHaveProperty(key);
    }
  });

  it("joins topic labels into keywords and points `about` at the destination's own page", () => {
    const data = parse(guideArticle("ja", {
      ...article,
      keywords: ["交通", "予算"],
      destination: { name: "ソウル", path: "/destinations/seoul" },
    }));
    // Text, not a list: schema.org types `keywords` as Text.
    expect(data.keywords).toBe("交通, 予算");
    expect(data.about).toEqual({
      "@type": "TouristDestination", name: "ソウル", url: `${siteUrl}/ja/destinations/seoul`,
    });
  });

  it("gives the hero its dimensions, and states the reading time as a duration", () => {
    const data = parse(guideArticle("en", {
      ...article,
      hero: { src: "/guides/seoul-subway-t-money-guide/hero.jpg", width: 1600, height: 900 },
      minutes: 8,
    }));
    expect(data.image).toEqual({
      "@type": "ImageObject",
      url: `${siteUrl}/guides/seoul-subway-t-money-guide/hero.jpg`,
      width: 1600,
      height: 900,
    });
    expect(data.timeRequired).toBe("PT8M");
  });

  it("becomes a CollectionPage listing its members when it is a series hub", () => {
    const data = parse(guideArticle("zh-TW", {
      ...article,
      collection: true,
      entries: [
        { name: "第一課", path: "/life/gemini-lesson-1" },
        { name: "第二課", path: "/life/gemini-lesson-2" },
      ],
    }));
    expect(data["@type"]).toBe("CollectionPage");
    expect(data.mainEntity).toEqual({
      "@type": "ItemList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "第一課", url: `${siteUrl}/zh-TW/life/gemini-lesson-1` },
        { "@type": "ListItem", position: 2, name: "第二課", url: `${siteUrl}/zh-TW/life/gemini-lesson-2` },
      ],
    });
  });

  it("stays a CollectionPage with no list when the series listing did not resolve", () => {
    const data = parse(guideArticle("zh-TW", { ...article, collection: true, entries: null }));
    expect(data["@type"]).toBe("CollectionPage");
    expect(data).not.toHaveProperty("mainEntity");
  });
});
