import { render, screen } from "@testing-library/react";
import type { ResolvingMetadata } from "next";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GuideArticlePage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({ article: vi.fn(), list: vi.fn(), notFound: vi.fn(() => { throw new Error("NEXT_NOT_FOUND"); }) }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: async () => ({ enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false }) }));
vi.mock("@/lib/guides.server", () => ({ getGuideArticle: mocks.article, getGuideList: mocks.list, getGuideTopics: async () => [] }));
vi.mock("next/navigation", () => ({ notFound: mocks.notFound }));
vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: { destinationId: string; modules?: string[] }) => (
    <div data-testid="affiliate" data-destination={props.destinationId} data-modules={(props.modules ?? []).join(",")} />
  ),
}));

const document = {
  title: "成田機場到東京車站怎麼走",
  description: "三種交通方式的時間與票價比較",
  version: 2,
  published_at: "2026-09-01T00:00:00Z",
  blocks: [{ type: "paragraph" as const, text: "Skyliner 最快。" }],
  sources: [{ title: "京成電鐵時刻表", url: "https://www.keisei.co.jp/", checked_on: "2026-09-01" }],
};

const hero = {
  src: "/guides/narita-to-tokyo/hero.jpg", alt: "Skyliner 停在成田機場月台", width: 1600, height: 900,
  credit: { author: "Mokaair", license: "© Mokaair", source_url: null },
};

const published = {
  slug: "narita-to-tokyo", kind: "howto" as const, locale: "zh-TW", status: "published" as const,
  destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], valid_until: null, expired: false,
  document, published_locales: ["zh-TW" as const, "ja" as const],
};

const summary = (slug: string, title: string) => ({
  slug, kind: "howto" as const, destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title, description: "…",
  published_at: "2026-09-02T00:00:00Z", valid_until: null, featured: false,
});

const emptyParent = Promise.resolve({}) as ResolvingMetadata;

const params = (over: Record<string, string> = {}) =>
  Promise.resolve({ locale: "zh-TW" as const, kind: "howto", slug: "narita-to-tokyo", ...over });

/** What the locale layout resolves to, as far as this page reads it. */
const parent = Promise.resolve({
  openGraph: { siteName: "Mokaair", locale: "zh_TW", alternateLocale: ["en_US", "ja_JP"], images: [{ url: "/og.png" }] },
}) as unknown as ResolvingMetadata;

function jsonLd(container: HTMLElement): Record<string, unknown>[] {
  return [...container.querySelectorAll("script[type='application/ld+json']")]
    .flatMap((script) => JSON.parse(script.textContent ?? "[]") as Record<string, unknown>[]);
}

beforeEach(() => {
  vi.clearAllMocks();
  mocks.article.mockResolvedValue(published);
  mocks.list.mockResolvedValue({ articles: [], next_cursor: null });
});

describe("an unknown section", () => {
  it("answers 404 rather than rendering an empty page", async () => {
    await expect(GuideArticlePage({ params: params({ kind: "recipes" }) })).rejects.toThrow("NEXT_NOT_FOUND");
    expect(mocks.notFound).toHaveBeenCalled();
    expect(mocks.article).not.toHaveBeenCalled();
  });
});

describe("a published article", () => {
  it("renders the body, its sources and its topics", async () => {
    render(await GuideArticlePage({ params: params() }));
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("成田機場到東京車站怎麼走");
    expect(screen.getByText("Skyliner 最快。")).toBeTruthy();
    expect(screen.getByRole("link", { name: "京成電鐵時刻表" }).getAttribute("href")).toBe("https://www.keisei.co.jp/");
    // The topic chip under the body, and the breadcrumb's topic crumb above it.
    expect(screen.getAllByRole("link", { name: "交通" }).map((link) => link.getAttribute("href"))).toEqual([
      "/guides/topics/transport", "/guides/howto?topic=transport",
    ]);
  });

  it("declares only the locales that are genuinely published", async () => {
    const metadata = await generateMetadata({ params: params() }, emptyParent);
    expect(metadata.title).toBe("成田機場到東京車站怎麼走");
    expect(Object.keys(metadata.alternates!.languages!).sort()).toEqual(["ja", "zh-TW"]);
    expect(metadata.robots).toBeUndefined();
  });

  it("offers x-default only when the English version exists", async () => {
    mocks.article.mockResolvedValue({ ...published, published_locales: ["zh-TW", "en"] });
    const metadata = await generateMetadata({ params: params() }, emptyParent);
    expect(metadata.alternates!.languages!["x-default"]).toContain("/en/guides/howto/narita-to-tokyo");
  });

  it("leaves the other languages to the head, listing none under the article", async () => {
    const metadata = await generateMetadata({ params: params() }, emptyParent);
    expect(metadata.alternates!.languages!.ja).toContain("/ja/guides/howto/narita-to-tokyo");
    const { container } = render(await GuideArticlePage({ params: params() }));
    expect(screen.queryByRole("link", { name: "日本語" })).toBeNull();
    expect(container.querySelector("a[hreflang]")).toBeNull();
  });

  it("claims no image and leaves the site's share card alone when it has no hero", async () => {
    const metadata = await generateMetadata({ params: params() }, parent);
    expect(metadata.openGraph).toBeUndefined();
    expect(metadata.twitter).toBeUndefined();
    const { container } = render(await GuideArticlePage({ params: params() }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    expect(article.image).toBeUndefined();
    expect(article.dateModified).toBe("2026-09-01T00:00:00Z");
  });

  it("tells the reader how long it takes", async () => {
    render(await GuideArticlePage({ params: params() }));
    expect(screen.getByText("閱讀時間約 1 分鐘")).toBeTruthy();
  });
});

describe("an article with a hero", () => {
  const illustrated = {
    ...published,
    document: { ...document, hero, modified_at: "2026-09-12T09:00:00Z" },
  };

  beforeEach(() => {
    mocks.article.mockResolvedValue(illustrated);
  });

  it("puts the hero on the share card without losing the layout's locales", async () => {
    const metadata = await generateMetadata({ params: params() }, parent);
    expect(metadata.openGraph).toMatchObject({
      type: "article",
      siteName: "Mokaair",
      locale: "zh_TW",
      alternateLocale: ["en_US", "ja_JP"],
      publishedTime: "2026-09-01T00:00:00Z",
      modifiedTime: "2026-09-12T09:00:00Z",
      images: [{ url: "/guides/narita-to-tokyo/hero.jpg", width: 1600, height: 900, alt: hero.alt }],
    });
    expect(metadata.twitter).toEqual({ card: "summary_large_image", images: ["/guides/narita-to-tokyo/hero.jpg"] });
  });

  it("still builds the card when the parent metadata is empty", async () => {
    const metadata = await generateMetadata({ params: params() }, emptyParent);
    expect(metadata.openGraph).toMatchObject({ type: "article", images: [{ url: "/guides/narita-to-tokyo/hero.jpg" }] });
  });

  it("claims the image and the correction date in the structured data", async () => {
    const { container } = render(await GuideArticlePage({ params: params() }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    // An ImageObject rather than a bare URL, so the dimensions the hero already carries are
    // not thrown away between the page and the graph.
    expect(article.image).toEqual({
      "@type": "ImageObject",
      url: "http://localhost:3000/guides/narita-to-tokyo/hero.jpg",
      width: 1600,
      height: 900,
    });
    expect(article.dateModified).toBe("2026-09-12T09:00:00Z");
    expect(article.datePublished).toBe("2026-09-01T00:00:00Z");
    expect(screen.getByRole("img", { name: hero.alt })).toBeTruthy();
  });
});

describe("what the article graph tells an answer engine", () => {
  it("cites the sources the page lists, and dates its own review from them", async () => {
    const { container } = render(await GuideArticlePage({ params: params() }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    // The same source the body renders as a link, further up this file.
    expect(article.citation).toEqual([
      { "@type": "CreativeWork", name: "京成電鐵時刻表", url: "https://www.keisei.co.jp/" },
    ]);
    expect(article.mainEntityOfPage).toMatchObject({
      "@type": "WebPage",
      "@id": "http://localhost:3000/zh-TW/guides/howto/narita-to-tokyo",
      lastReviewed: "2026-09-01",
    });
  });

  it("never cites a source the page itself refused to draw", async () => {
    mocks.article.mockResolvedValue({
      ...published,
      document: { ...document, sources: [
        { title: "京成電鐵時刻表", url: "https://www.keisei.co.jp/", checked_on: "2026-09-01" },
        { title: "壞掉的來源", url: "javascript:alert(1)", checked_on: "2026-09-02" },
      ] },
    });
    const { container } = render(await GuideArticlePage({ params: params() }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    expect(screen.queryByRole("link", { name: "壞掉的來源" })).toBeNull();
    expect(article.citation).toHaveLength(1);
    // The rejected source takes its checked_on with it: the page never showed that date either.
    expect((article.mainEntityOfPage as Record<string, unknown>).lastReviewed).toBe("2026-09-01");
  });

  it("names the section, the topics and the destination the page shows", async () => {
    const { container } = render(await GuideArticlePage({ params: params() }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    expect(article.articleSection).toBe("旅遊攻略");
    expect(article.keywords).toBe("交通");
    expect(article.about).toEqual({
      "@type": "TouristDestination", name: "東京", url: "http://localhost:3000/zh-TW/destinations/tokyo",
    });
    // The same figure the page prints as "閱讀時間約 1 分鐘".
    expect(article.timeRequired).toBe("PT1M");
    expect(article.isAccessibleForFree).toBe(true);
  });

  it("says nothing about a destination with no page behind it", async () => {
    mocks.article.mockResolvedValue({ ...published, destination_id: "atlantis", destination_label: "亞特蘭提斯" });
    const { container } = render(await GuideArticlePage({ params: params() }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    expect(article.about).toBeUndefined();
  });

  it("does not publish an intel notice's expiry, which the page deliberately withholds", async () => {
    mocks.article.mockResolvedValue({ ...published, kind: "intel", valid_until: "2026-12-15" });
    const { container } = render(await GuideArticlePage({ params: params({ kind: "intel" }) }));
    const article = jsonLd(container).find((graph) => graph["@type"] === "Article")!;
    // schema.org reads `expires` as "stop serving this", and the notice keeps its URL on purpose.
    expect(article.expires).toBeUndefined();
  });
});

describe("related reading", () => {
  it("ends with other travel articles about the same city, never the article itself", async () => {
    mocks.list.mockResolvedValue({
      articles: [summary("narita-to-tokyo", "成田機場到東京車站怎麼走"), summary("tokyo-transit-passes", "東京交通票券怎麼選")],
      next_cursor: null,
    });
    render(await GuideArticlePage({ params: params() }));
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", { section: "travel", destination: "tokyo" }, 4);
    expect(screen.getByRole("heading", { name: "延伸閱讀" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "東京交通票券怎麼選" }).getAttribute("href")).toBe("/guides/howto/tokyo-transit-passes");
    // The article is on the page as the h1 and as the breadcrumb's current step, not as a card.
    expect(screen.queryByRole("link", { name: "成田機場到東京車站怎麼走" })).toBeNull();
    expect(screen.getAllByText("成田機場到東京車站怎麼走")).toHaveLength(2);
  });

  it("tops up from the first topic when the city has too few", async () => {
    mocks.list
      .mockResolvedValueOnce({ articles: [], next_cursor: null })
      .mockResolvedValueOnce({ articles: [summary("incheon-airport-to-seoul", "仁川機場到首爾")], next_cursor: null });
    render(await GuideArticlePage({ params: params() }));
    expect(mocks.list).toHaveBeenLastCalledWith("zh-TW", { section: "travel", topic: "transport" }, 4);
    expect(screen.getByRole("link", { name: "仁川機場到首爾" })).toBeTruthy();
  });

  it("shows no related section at all when there is nothing to show", async () => {
    render(await GuideArticlePage({ params: params() }));
    expect(screen.queryByRole("heading", { name: "延伸閱讀" })).toBeNull();
  });
});

describe("an expired notice", () => {
  const expired = {
    ...published, kind: "intel" as const, expired: true, valid_until: "2026-08-01",
  };

  it("keeps its page, and shows neither the date it applied until nor a banner", async () => {
    mocks.article.mockResolvedValue(expired);
    render(await GuideArticlePage({ params: params({ kind: "intel" }) }));
    expect(screen.getByRole("heading", { level: 1 })).toBeTruthy();
    expect(screen.queryByRole("status")).toBeNull();
    expect(screen.queryByText(/2026-08-01/)).toBeNull();
  });

  it("stays indexable, because withdrawing the URL would break existing links", async () => {
    mocks.article.mockResolvedValue(expired);
    const metadata = await generateMetadata({ params: params({ kind: "intel" }) }, emptyParent);
    expect(metadata.robots).toBeUndefined();
  });
});

describe("a locale the article was never written in", () => {
  const untranslated = {
    ...published, locale: "ko", status: "unpublished" as const, document: null,
  };

  it("says so and offers the languages that do exist", async () => {
    mocks.article.mockResolvedValue(untranslated);
    render(await GuideArticlePage({ params: params({ locale: "ko" }) }));
    expect(screen.getByRole("status").textContent).toBe("這篇文章還沒有你選擇語言的版本。");
    expect(screen.getByRole("link", { name: "繁體中文" }).getAttribute("href")).toBe("/zh-TW/guides/howto/narita-to-tokyo");
  });

  it("is never indexed, so an empty page cannot outrank the real one", async () => {
    mocks.article.mockResolvedValue(untranslated);
    const metadata = await generateMetadata({ params: params({ locale: "ko" }) }, emptyParent);
    expect(metadata.robots).toEqual({ index: false });
    expect(metadata.alternates!.languages).toBeUndefined();
  });
});

describe("a backend fault", () => {
  const broken = { ...published, status: "unavailable" as const, document: null, published_locales: [] };

  it("reports a failure instead of a blank article", async () => {
    mocks.article.mockResolvedValue(broken);
    render(await GuideArticlePage({ params: params() }));
    expect(screen.getByRole("alert").textContent).toBe("暫時無法取得這篇文章，請稍後再試。");
  });

  it("keeps the broken page out of the index", async () => {
    mocks.article.mockResolvedValue(broken);
    expect((await generateMetadata({ params: params() }, emptyParent)).robots).toEqual({ index: false });
  });
});
