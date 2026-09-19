import { describe, expect, it } from "vitest";
import { siteUrl } from "@/lib/seo";
import {
  definedTerm, faqPage, breadcrumbs, foodEstablishment, foodEstablishments, guideArticle, itemList, organization,
  touristDestination, webSite, type MerchantCard,
} from "@/lib/structured-data";

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
    for (const key of ["citation", "keywords", "about", "image", "timeRequired", "expires", "mainEntity", "abstract", "speakable"]) {
      expect(data).not.toHaveProperty(key);
    }
  });

  it("carries the editor's summary as the abstract and names its card as the speakable passage", () => {
    const data = parse(guideArticle("zh-TW", { ...article, abstract: ["先買 eSIM。", "落地就能上網。"] }));
    expect(data.abstract).toBe("先買 eSIM。 落地就能上網。");
    expect(data.speakable).toEqual({ "@type": "SpeakableSpecification", cssSelector: ["#article-summary"] });
    expect(parse(guideArticle("zh-TW", { ...article, abstract: [] }))).not.toHaveProperty("abstract");
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

describe("faqPage", () => {
  it("lists the editor's questions with their answers, and nothing without any", () => {
    const data = parse(faqPage("zh-TW", "/life/tokyo-esim", [
      { question: "要實體 SIM 嗎？", answer: "不用。" }, { question: " ", answer: "空的問題不算" },
    ]));
    expect(data["@type"]).toBe("FAQPage");
    expect(data["@id"]).toBe(`${siteUrl}/zh-TW/life/tokyo-esim#faq`);
    expect(data.mainEntity).toEqual([
      { "@type": "Question", name: "要實體 SIM 嗎？", acceptedAnswer: { "@type": "Answer", text: "不用。" } },
    ]);
    expect(faqPage("zh-TW", "/life/tokyo-esim", [{ question: "", answer: "" }])).toBeNull();
  });
});

describe("definedTerm", () => {
  it("names the term, its other names and the glossary it belongs to", () => {
    const data = parse(definedTerm("zh-TW", {
      path: "/life/ai-term-machine-learning", name: "機器學習", description: "讓電腦從資料學規則。",
      aliases: ["ML", " 機器學習 ", "Machine Learning"], set: { name: "AI 名詞總索引", path: "/life/ai-terms-index" },
    }));
    expect(data["@type"]).toBe("DefinedTerm");
    expect(data["@id"]).toBe(`${siteUrl}/zh-TW/life/ai-term-machine-learning#term`);
    expect(data.name).toBe("機器學習");
    // The term's own name is not one of its other names.
    expect(data.alternateName).toEqual(["ML", "Machine Learning"]);
    expect(data.inDefinedTermSet).toEqual({ "@type": "DefinedTermSet", name: "AI 名詞總索引", url: `${siteUrl}/zh-TW/life/ai-terms-index` });
    expect(parse(definedTerm("zh-TW", { path: "/life/x", name: "X", description: "d", set: { name: "S", path: "/life/s" } })))
      .not.toHaveProperty("alternateName");
  });
});

describe("foodEstablishment", () => {
  // The labels the card can badge, as the page resolves them for the reader's language.
  const awards = { bib_gourmand: "必比登推介", one_star: "米其林一星" };
  const hankook: MerchantCard = {
    id: "merchant-1",
    name: "Hankook Jib",
    local_name: "한국집",
    destination_name: "首爾",
    address: "Seoul, Jung-gu",
    sources: [
      { title: "Michelin Guide Seoul", url: "https://guide.michelin.example/hankook-jib", distinction: "bib_gourmand" },
      // The card prints this title as text: `safeExternalHref` refuses the scheme, so no link.
      { title: "Visit Seoul listing", url: "javascript:alert(1)", distinction: null },
    ],
  };

  it("describes the card: name, original-script name, address line, city, badge and sources", () => {
    const data = parse(foodEstablishment("zh-TW", hankook, awards));
    expect(data["@context"]).toBe("https://schema.org");
    expect(data["@type"]).toBe("FoodEstablishment");
    // The card's own anchor, which the share button hands out.
    expect(data["@id"]).toBe(`${siteUrl}/zh-TW/foods#merchant-merchant-1`);
    expect(data.name).toBe("Hankook Jib");
    expect(data.alternateName).toBe("한국집");
    expect(data.address).toEqual({ "@type": "PostalAddress", streetAddress: "Seoul, Jung-gu", addressLocality: "首爾" });
    expect(data.award).toBe("必比登推介");
    expect(data.citation).toEqual([
      { "@type": "CreativeWork", name: "Michelin Guide Seoul", url: "https://guide.michelin.example/hankook-jib" },
      { "@type": "CreativeWork", name: "Visit Seoul listing" },
    ]);
  });

  it("badges the first source the card would badge, and nothing when no source carries a known one", () => {
    const first = parse(foodEstablishment("en", {
      ...hankook,
      sources: [
        { title: "Guide", url: "https://a.example/", distinction: "one_star" },
        { title: "Guide, later edition", url: "https://b.example/", distinction: "bib_gourmand" },
      ],
    }, awards));
    expect(first.award).toBe("米其林一星");
    // A distinction the card has no label for stays off the graph as it stays off the card.
    const unknown = parse(foodEstablishment("en", {
      ...hankook, sources: [{ title: "Guide", url: "https://a.example/", distinction: "plate" }],
    }, awards));
    expect(unknown).not.toHaveProperty("award");
    const none = parse(foodEstablishment("en", { ...hankook, sources: [{ ...hankook.sources[0], distinction: null }] }, awards));
    expect(none).not.toHaveProperty("award");
    expect(none.citation).toHaveLength(1);
  });

  it("omits what the card has no value for rather than emitting an empty field", () => {
    const data = parse(foodEstablishment("en", { ...hankook, local_name: "Hankook Jib", address: null, sources: [] }, awards));
    expect(data).not.toHaveProperty("alternateName");
    expect(data.address).toEqual({ "@type": "PostalAddress", addressLocality: "首爾" });
    expect(data).not.toHaveProperty("citation");
    expect(data).not.toHaveProperty("award");
  });

  it("claims nothing the card does not show: no rating, review, hours, coordinates or website", () => {
    const data = parse(foodEstablishment("en", hankook, awards));
    expect(Object.keys(data).sort()).toEqual(["@context", "@id", "@type", "address", "alternateName", "award", "citation", "name"]);
    // Nothing on this site collects a rating; the interest score is Mokaair's own signal.
    const text = JSON.stringify(data);
    for (const forbidden of ["aggregateRating", "\"review\"", "Review", "Rating", "openingHours", "geo", "sameAs", "servesCuisine"]) {
      expect(text).not.toContain(forbidden);
    }
  });
});

describe("foodEstablishments", () => {
  const awards = { bib_gourmand: "Bib Gourmand" };
  const card: MerchantCard = {
    id: "a", name: "A", local_name: "A", destination_name: "Tokyo", address: "東京都中央区築地5-2-1",
    sources: [{ title: "Tokyo tourism", url: "https://www.gotokyo.org/a", distinction: null }],
  };

  it("marks up the seed's items, one FoodEstablishment each, in the order the cards render", () => {
    const seed = { total: 2, has_more: false, next_cursor: null, items: [card, { ...card, id: "b", name: "B" }], facets: {} };
    const data = foodEstablishments("ja", seed, awards).map(parse);
    expect(data.map((node) => node["@type"])).toEqual(["FoodEstablishment", "FoodEstablishment"]);
    expect(data.map((node) => node["@id"])).toEqual([`${siteUrl}/ja/foods#merchant-a`, `${siteUrl}/ja/foods#merchant-b`]);
  });

  it("describes no merchant the server did not draw: a seed that never arrived, or is not a merchant list", () => {
    // The API withholds moderated and unverified merchants before they reach `items`; what is
    // left for the page is the seed that failed to load, when the browser renders after hydration.
    expect(foodEstablishments("en", null, awards)).toEqual([]);
    expect(foodEstablishments("en", undefined, awards)).toEqual([]);
    expect(foodEstablishments("en", { countries: [] }, awards)).toEqual([]);
    expect(foodEstablishments("en", { items: [] }, awards)).toEqual([]);
    expect(foodEstablishments("en", "not a list", awards)).toEqual([]);
  });
});
