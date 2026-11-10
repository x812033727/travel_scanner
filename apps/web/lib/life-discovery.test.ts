import { describe, expect, it } from "vitest";
import type { GuideSummary } from "./guides";
import { lifeDiscoveryCopy, selectLifeKnowledge } from "./life-discovery";

const article = (slug: string, overrides: Partial<GuideSummary> = {}): GuideSummary => ({
  slug, kind: "life", title: slug, description: "A useful explanation", topics: [],
  destination_id: null, destination_label: null, published_at: "2026-11-01T00:00:00Z",
  news_date: null, valid_until: null, featured: false, ...overrides,
});

describe("life knowledge discovery", () => {
  it("excludes news dates, every news topic even when undated, and travel articles", () => {
    const rows = [article("dated", { news_date: "2026-11-10" }),
      ...["ai-news", "crypto", "tech-news"].map(slug => article(slug, { topics: [{ slug, label: slug }] })),
      article("travel", { kind: "howto" }), article("useful")];
    expect(selectLifeKnowledge(rows).map(row => row.slug)).toEqual(["useful"]);
  });

  it("takes at most three unique articles in existing curated order, without ranking by freshness", () => {
    const first = article("first", { published_at: "2020-01-01T00:00:00Z" });
    const rows = [first, first, article("second"), article("third"), article("fourth", { featured: true })];
    expect(selectLifeKnowledge(rows).map(row => row.slug)).toEqual(["first", "second", "third"]);
    expect(rows).toHaveLength(5);
  });

  it("excludes expired and upcoming deadlines without guessing whether dated information is still useful", () => {
    const rows = [article("expired", { valid_until: "2020-01-01" }),
      article("future-deadline", { valid_until: "2099-12-31" }), article("no-expiry")];
    expect(selectLifeKnowledge(rows).map(row => row.slug)).toEqual(["no-expiry"]);
    expect(rows.map(row => row.slug)).toEqual(["expired", "future-deadline", "no-expiry"]);
  });

  it("supports older API summaries without a news date and never fills an empty rail", () => {
    expect(selectLifeKnowledge([article("old-api", { news_date: undefined })]).map(row => row.slug)).toEqual(["old-api"]);
    expect(selectLifeKnowledge([])).toEqual([]);
  });

  it.each(["en", "ja", "ko", "zh-TW", "zh-CN"])("has the same keys and one count placeholder in %s", (locale) => {
    const copy = lifeDiscoveryCopy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(lifeDiscoveryCopy("en")).sort());
    expect(copy.moreNews.match(/\{count\}/g)).toHaveLength(1);
    expect(Object.values(copy).every(value => value.trim().length > 0)).toBe(true);
    expect(Object.values(copy).flatMap(value => value.match(/\{[^}]+\}/g) ?? [])).toEqual(["{count}"]);
  });
});
