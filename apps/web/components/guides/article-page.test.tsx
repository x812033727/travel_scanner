import { cleanup, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { guideArticleMetadata, renderGuideArticle } from "./article-page";
import type { LearningEntry } from "@/lib/codex-learning";

const mocks = vi.hoisted(() => ({
  article: vi.fn(), series: vi.fn(),
  list: vi.fn<(locale: string, filters: Record<string, string>, limit: number) => Promise<{ articles: Record<string, unknown>[]; next_cursor: null }>>(
    async () => ({ articles: [], next_cursor: null }),
  ),
  topics: vi.fn(async (): Promise<Record<string, unknown>[]> => []),
  trending: vi.fn(async () => ({ articles: [] as Record<string, unknown>[], next_cursor: null, available: true })),
  permanentRedirect: vi.fn((url: string) => { throw new Error(`NEXT_REDIRECT ${url}`); }),
  headers: vi.fn(async () => new Headers()),
}));
vi.mock("next/navigation", async (original) => ({
  ...await original<typeof import("next/navigation")>(), permanentRedirect: mocks.permanentRedirect,
}));
vi.mock("next/headers", () => ({ headers: mocks.headers }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: async () => ({ enabled: false }) }));
vi.mock("@/lib/guides.server", () => ({
  getGuideArticle: mocks.article, getGuideSeries: mocks.series,
  getGuideList: mocks.list,
  getGuideTopics: mocks.topics,
  getTrendingGuides: mocks.trending,
}));
vi.mock("@/components/codex-learning/hub", () => ({ LearningHub: ({ entries, available }: { entries: LearningEntry[]; available: boolean }) =>
  <section aria-label="Learning directory" data-available={available}>
    {entries.filter(entry => entry.published).map(entry => <a key={entry.slug} href={`/life/${entry.slug}`}>{entry.title}</a>)}
  </section>,
}));

const reference = { kind: "life", slug: "codex-learning-hub", title: "Codex hub" };
const current = { kind: "life", slug: "codex-agents-md", title: "Project rules", description: "Rules",
  number: 20, group: "D", level: "beginner", platforms: ["cli"], aliases: ["AGENTS.md"], minutes: 12, operation_minutes: 20 };
const document = {
  title: "Codex hub", description: "Find a lesson", version: 1,
  published_at: "2026-09-14T00:00:00Z", modified_at: "2026-09-14T00:00:00Z", sources: [],
  blocks: [1, 2, 3].map(number => ({ type: "heading", level: 2, text: `Step ${number}` })),
};
const state = { ...reference, locale: "en", status: "published", destination_id: null,
  destination_label: null, topics: [], published_locales: ["en", "ja"], expired: false, document,
  series: { slug: "codex", hub: reference, current: null, previous: null, next: null, prerequisites: [], related: [] }, article_links: [] };

beforeEach(() => { vi.clearAllMocks(); mocks.headers.mockResolvedValue(new Headers()); mocks.article.mockResolvedValue(state); mocks.series.mockResolvedValue({
  slug: "codex", locale: "en", hub: reference, groups: [], paths: [], entries: [current],
}); });

describe("a capitalised slug", () => {
  it("is sent to the canonical lowercase address for good, before anything is fetched", async () => {
    const route = { locale: "en" as const, kind: "howto" as const, slug: "Narita-To-Tokyo" };
    await expect(renderGuideArticle(route)).rejects.toThrow("NEXT_REDIRECT /en/guides/howto/narita-to-tokyo");
    await expect(guideArticleMetadata(route)).rejects.toThrow("NEXT_REDIRECT /en/guides/howto/narita-to-tokyo");
    expect(mocks.permanentRedirect).toHaveBeenCalledTimes(2);
    expect(mocks.article).not.toHaveBeenCalled();
    // A lifestyle slug lands under /life, and a lowercase slug is left alone.
    await expect(renderGuideArticle({ locale: "zh-TW", kind: "life", slug: "AI-Notes" })).rejects.toThrow("/zh-TW/life/ai-notes");
    mocks.permanentRedirect.mockClear();
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: "codex-learning-hub" }));
    expect(mocks.permanentRedirect).not.toHaveBeenCalled();
  });

  it("keeps the query string, so a campaign-tagged link does not lose its tags", async () => {
    const query = "?utm_source=youtube&utm_medium=video&utm_campaign=ai-notes";
    mocks.headers.mockResolvedValue(new Headers({ "x-travel-pathname": `/zh-TW/life/AI-Notes${query}` }));
    const route = { locale: "zh-TW" as const, kind: "life" as const, slug: "AI-Notes" };
    await expect(renderGuideArticle(route)).rejects.toThrow(`NEXT_REDIRECT /zh-TW/life/ai-notes${query}`);
    await expect(guideArticleMetadata(route)).rejects.toThrow(`NEXT_REDIRECT /zh-TW/life/ai-notes${query}`);
  });
});

describe("Codex articles on the shared page", () => {
  it("renders the Codex directory and CollectionPage from current locale publication", async () => {
    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(mocks.series).toHaveBeenCalledWith("codex", "en");
    expect(screen.getByRole("link", { name: "Project rules" }).getAttribute("href")).toBe("/life/codex-agents-md");
    const json = [...container.querySelectorAll('script[type="application/ld+json"]')].flatMap(script => JSON.parse(script.textContent!));
    const collection = json.find(item => item["@type"] === "CollectionPage");
    expect(collection.mainEntity.itemListElement).toEqual([{ "@type": "ListItem", position: 1, name: "Project rules", url: expect.stringContaining("/en/life/codex-agents-md") }]);
  });
  it("keeps the directory visible but links and ItemList absent when publication lookup fails", async () => {
    mocks.article.mockResolvedValue({ ...state, series: null });
    mocks.series.mockResolvedValue(null);
    const { container } = render(await renderGuideArticle({ locale: "ja", kind: "life", slug: reference.slug }));
    expect(screen.getByRole("region", { name: "Learning directory" }).getAttribute("data-available")).toBe("false");
    expect(screen.queryByRole("link", { name: "Project rules" })).toBeNull();
    expect(container.querySelector('script[type="application/ld+json"]')?.textContent).not.toContain("ItemList");
  });
  it("shows shared chapter navigation and separate practice time on a lesson", async () => {
    mocks.article.mockResolvedValue({ ...state, slug: current.slug, document: { ...document, title: current.title }, series: { ...state.series, current } });
    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: current.slug }));
    expect(mocks.series).not.toHaveBeenCalled();
    expect(container.textContent).toContain("Practice 20 min");
    expect(container.querySelector("details.lg\\:hidden")).not.toBeNull();
    expect(container.querySelector("aside nav.sticky")).not.toBeNull();
    expect(container.querySelectorAll('a[href="/en/life/codex-learning-hub"]').length).toBeGreaterThanOrEqual(2);
  });
  it("does not fetch a series when the hub translation is unpublished", async () => {
    mocks.article.mockResolvedValue({ ...state, status: "unpublished", document: null });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(mocks.series).not.toHaveBeenCalled();
    expect(screen.queryByRole("region", { name: "Learning directory" })).toBeNull();
  });
});

describe("further reading", () => {
  const ref = (slug: string, title: string, kind: "life" | "howto" = "life") =>
    ({ kind, slug, title, description: `${title} 的描述` });

  it("shows the API's ranked list, minus what the series navigation already lists, then who cites the article", async () => {
    mocks.article.mockResolvedValue({
      ...state,
      series: { ...state.series, related: [ref("already", "已列")] },
      related: [ref("already", "已列"), ref("next", "接著讀"), ref("guide", "旅遊攻略", "howto")],
      backlinks: [ref("citing", "引用者")],
    });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    const grid = screen.getByRole("region", { name: "同主題延伸閱讀" });
    expect(within(grid).getAllByRole("listitem").map((item) => item.textContent)).toEqual([
      expect.stringContaining("接著讀"), expect.stringContaining("旅遊攻略"),
    ]);
    expect(within(grid).queryByRole("link", { name: "已列" })).toBeNull();
    expect(within(grid).getByRole("link", { name: "旅遊攻略" }).getAttribute("href")).toBe("/guides/howto/guide");
    expect(screen.getByRole("region", { name: "引用本文的文章" }).textContent).toContain("引用者");
    const order = [screen.getByTestId("related-grid"), screen.getByTestId("backlinks")];
    expect(order[0].compareDocumentPosition(order[1]) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it("ends an article that names no destination without travel cards or city chips", async () => {
    // What an AI, tech or finance article looks like: topical related reading, no destination.
    // The site's newest travel guides used to follow every one of them, whatever it was about.
    mocks.list.mockResolvedValue({ articles: [{ ...ref("okinawa-lodging-tax-2027", "沖繩住宿稅", "howto"), kind: "intel", destination_label: null, hero: null, topics: [] }], next_cursor: null });
    mocks.article.mockResolvedValue({ ...state, related: [ref("next", "接著讀")] });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(screen.getByTestId("related-grid")).toBeTruthy();
    expect(screen.queryByTestId("travel-crosslinks")).toBeNull();
    expect(screen.queryByText("沖繩住宿稅")).toBeNull();
    expect(mocks.list).not.toHaveBeenCalledWith("en", { section: "travel" }, expect.anything());
  });

  it("hands an article that names a destination over to that destination's travel guides, after its own lists", async () => {
    mocks.list.mockImplementation(async (_locale, filters) => ({
      articles: filters.destination === "tokyo"
        ? [{ ...ref("tokyo-transit-passes", "東京交通票券", "howto"), destination_label: "Tokyo", hero: null, topics: [] }]
        : [],
      next_cursor: null,
    }));
    mocks.article.mockResolvedValue({
      ...state, destination_id: "tokyo", related: [ref("next", "接著讀")], backlinks: [ref("citing", "引用者")],
    });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(mocks.list).toHaveBeenCalledWith("en", { section: "travel", destination: "tokyo" }, 3);
    const handover = screen.getByTestId("travel-crosslinks");
    expect(within(handover).getByRole("link", { name: "東京交通票券" }).getAttribute("href")).toBe("/guides/howto/tokyo-transit-passes");
    // The chips are that country's cities, not one city of every country.
    const chips = within(handover).getAllByRole("link").map((link) => link.getAttribute("href")).filter((href) => href?.startsWith("/destinations/"));
    expect(chips).toContain("/destinations/tokyo");
    expect(chips).not.toContain("/destinations/seoul");
    const order = [screen.getByTestId("related-grid"), screen.getByTestId("backlinks"), handover];
    expect(order[0].compareDocumentPosition(order[1]) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(order[1].compareDocumentPosition(order[2]) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it("draws neither section for an article the API sent without them", async () => {
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(screen.queryByTestId("related-grid")).toBeNull();
    expect(screen.queryByTestId("backlinks")).toBeNull();
  });

  it("hands the definition-card words to the body, so a term link can show its target's description", async () => {
    mocks.article.mockResolvedValue({
      ...state,
      document: { ...document, blocks: [{ type: "rich_paragraph", inlines: [{ type: "article", kind: "life", slug: "term", text: "the term" }] }] },
      article_links: [ref("term", "Term")],
    });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(screen.getByRole("link", { name: "the term" }).getAttribute("aria-expanded")).toBe("false");
  });
});

describe("breadcrumb, summary, FAQ and glossary markup", () => {
  it("shows a breadcrumb on every article, through the topic's parent hub when the vocabulary knows it", async () => {
    mocks.topics.mockResolvedValue([
      { slug: "ai", label: "AI", section: "life", parent: null },
      { slug: "ai-terms", label: "AI 名詞解釋", section: "life", parent: "ai" },
    ]);
    mocks.article.mockResolvedValue({ ...state, series: null, topics: [{ slug: "ai-terms", label: "AI 名詞解釋", parent: "ai" }] });
    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    const nav = screen.getByRole("navigation", { name: "頁面路徑" });
    expect(within(nav).getAllByRole("link").map((link) => link.getAttribute("href"))).toEqual([
      "/life", "/ai", "/life/topics/ai-terms",
    ]);
    expect(mocks.topics).toHaveBeenCalledWith("en", "life");
    const json = [...container.querySelectorAll('script[type="application/ld+json"]')].flatMap(script => JSON.parse(script.textContent!));
    const crumbs = json.find(item => item["@type"] === "BreadcrumbList");
    expect(crumbs.itemListElement.map((item: { name: string }) => item.name)).toEqual(["首頁", "生活分享", "AI", "AI 名詞解釋", "Codex hub"]);
  });

  it("keeps the topic crumb when the vocabulary is unavailable, and skips it for an article without topics", async () => {
    mocks.article.mockResolvedValue({ ...state, series: null, topics: [{ slug: "ai", label: "AI" }] });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(within(screen.getByRole("navigation", { name: "頁面路徑" })).getAllByRole("link").map((link) => link.getAttribute("href")))
      .toEqual(["/life", "/ai"]);
    cleanup();
    mocks.article.mockResolvedValue({ ...state, series: null, topics: [] });
    render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    expect(within(screen.getByRole("navigation", { name: "頁面路徑" })).getAllByRole("link").map((link) => link.getAttribute("href")))
      .toEqual(["/life"]);
  });

  it("emits the abstract, the FAQ and the glossary entry exactly when the page shows them", async () => {
    mocks.article.mockResolvedValue({
      ...state,
      series: null,
      document: { ...document, blocks: [
        { type: "summary", items: ["先讀這句。", "再讀那句。"] },
        ...document.blocks,
        { type: "faq", items: [{ question: "要多久？", answer: "十分鐘。" }, { question: "要錢嗎？", answer: "不用。" }] },
      ] },
      aliases: ["ML"],
      term_set: { kind: "life", slug: "ai-terms-index", title: "AI 名詞總索引", description: "全部名詞" },
    });
    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    const json = [...container.querySelectorAll('script[type="application/ld+json"]')].flatMap(script => JSON.parse(script.textContent!));
    // The fixture is the Codex hub, so its graph is a CollectionPage; the fields are the same.
    const article = json.find(item => item["@type"] === "CollectionPage" || item["@type"] === "Article");
    expect(article.abstract).toBe("先讀這句。 再讀那句。");
    expect(article.speakable.cssSelector).toEqual(["#article-summary"]);
    expect(container.querySelector("#article-summary")).not.toBeNull();
    const faq = json.find(item => item["@type"] === "FAQPage");
    expect(faq.mainEntity.map((item: { name: string }) => item.name)).toEqual(["要多久？", "要錢嗎？"]);
    expect(container.querySelectorAll("#article-faq details")).toHaveLength(2);
    const term = json.find(item => item["@type"] === "DefinedTerm");
    expect(term.name).toBe(document.title);
    expect(term.alternateName).toEqual(["ML"]);
    expect(term.inDefinedTermSet.url).toContain("/en/life/ai-terms-index");
    cleanup();
    mocks.article.mockResolvedValue({ ...state, series: null });
    const plain = render(await renderGuideArticle({ locale: "en", kind: "life", slug: reference.slug }));
    const graphs = [...plain.container.querySelectorAll('script[type="application/ld+json"]')].flatMap(script => JSON.parse(script.textContent!));
    expect(graphs.map(item => item["@type"])).not.toEqual(expect.arrayContaining(["FAQPage", "DefinedTerm"]));
    expect(graphs.find(item => item["@type"] === "CollectionPage" || item["@type"] === "Article")).not.toHaveProperty("abstract");
  });

  it("emits NewsArticle JSON-LD and renders news_date when the article is a dated news item", async () => {
    mocks.article.mockResolvedValue({
      ...state,
      slug: "claude-code-news-2026-11-12",
      series: null,
      news_date: "2026-11-12",
      topics: [{ slug: "ai-news", label: "AI 新聞" }],
    });
    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: "claude-code-news-2026-11-12" }));
    const graphs = [...container.querySelectorAll('script[type="application/ld+json"]')].flatMap(script => JSON.parse(script.textContent!));
    expect(graphs.find(item => item["@type"] === "NewsArticle")).toBeTruthy();
    expect(container.querySelector('time[datetime="2026-11-12"]')?.textContent).toBe("2026-11-12");
    expect(container.querySelector("details.lg\\:hidden")).not.toBeNull();
    expect(container.querySelector("aside nav.sticky")).not.toBeNull();
  });

  it("omits synthetic news-assets placeholder artwork from OpenGraph, Twitter and NewsArticle JSON-LD", async () => {
    const syntheticHero = {
      src: "/guides/news-assets/deadbeef1234567890abcdef-hero.webp",
      alt: "Placeholder",
      width: 1600,
      height: 900,
      credit: { author: "Mokaair", license: "Original editorial artwork", source_url: null },
    };
    mocks.article.mockResolvedValue({
      ...state,
      slug: "claude-code-news-2026-11-12",
      series: null,
      news_date: "2026-11-12",
      topics: [{ slug: "ai-news", label: "AI 新聞" }],
      document: { ...document, hero: syntheticHero },
    });
    const meta = await guideArticleMetadata({ locale: "en", kind: "life", slug: "claude-code-news-2026-11-12" });
    expect(meta.openGraph).toBeUndefined();
    expect(meta.twitter).toBeUndefined();

    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: "claude-code-news-2026-11-12" }));
    const graphs = [...container.querySelectorAll('script[type="application/ld+json"]')].flatMap(script => JSON.parse(script.textContent!));
    const newsGraph = graphs.find(item => item["@type"] === "NewsArticle");
    expect(newsGraph).not.toHaveProperty("image");
    expect(container.querySelector("img")).toBeNull();
  });

  it("emits Discover max-image-preview:large metadata and renders share actions plus right-rail trending recirculation", async () => {
    mocks.article.mockResolvedValue({
      ...state,
      slug: "short-news-20261113",
      series: null,
      news_date: "2026-11-13",
      topics: [{ slug: "ai-news", label: "AI 新聞" }],
      document: {
        ...document,
        blocks: [{ type: "heading", level: 2, text: "重點" }],
      },
    });
    mocks.trending.mockResolvedValueOnce({
      articles: [
        {
          slug: "short-news-20261113",
          kind: "life",
          destination_id: null,
          destination_label: null,
          topics: [{ slug: "ai-news", label: "AI 新聞" }],
          title: "Self article should be excluded",
          description: "D",
          published_at: "2026-11-13T00:00:00Z",
          valid_until: null,
          featured: false,
        },
        {
          slug: "tokyo-esim-pick",
          kind: "howto",
          destination_id: "tokyo",
          destination_label: "東京",
          topics: [{ slug: "connectivity", label: "網路" }],
          title: "日本 eSIM 實測比較",
          description: "D",
          published_at: "2026-11-13T01:00:00Z",
          valid_until: null,
          featured: true,
        },
      ],
      next_cursor: null,
      available: true,
    });

    const meta = await guideArticleMetadata({ locale: "en", kind: "life", slug: "short-news-20261113" });
    expect(meta.robots).toMatchObject({
      index: true,
      follow: true,
      googleBot: { "max-image-preview": "large", "max-snippet": -1 },
    });

    const { container } = render(await renderGuideArticle({ locale: "en", kind: "life", slug: "short-news-20261113" }));
    const headerShare = screen.getByRole("group", { name: "分享文章" });
    expect(within(headerShare).getByRole("button", { name: "複製連結" })).toBeTruthy();
    expect(within(headerShare).getByRole("link", { name: "LINE 分享" }).getAttribute("href")).toContain("social-plugins.line.me/lineit/share");
    const footerShare = screen.getByTestId("article-share-footer");
    expect(within(footerShare).getByText("覺得這篇整理實用嗎？分享給需要的朋友")).toBeTruthy();
    expect(within(footerShare).getByRole("button", { name: "複製連結" })).toBeTruthy();
    expect(container.querySelector("div.fixed.inset-x-0.lg\\:hidden")).not.toBeNull();
    const trendingSection = screen.getByRole("region", { name: "熱門閱讀" });
    expect(trendingSection.closest("aside")?.className).not.toContain("hidden");
    expect(within(trendingSection).getByRole("link", { name: "日本 eSIM 實測比較" })).toBeTruthy();
    expect(within(trendingSection).queryByText("Self article should be excluded")).toBeNull();
  });

  it("opens a mobile TOC quick-jump bottom sheet once scrolled past 28% on multi-section articles", async () => {
    const { fireEvent } = await import("@testing-library/react");
    const { ArticleMobileProgress } = await import("@/components/guides/article-toc-rail");

    Object.defineProperty(window.document.documentElement, "scrollHeight", { configurable: true, value: 2000 });
    Object.defineProperty(window.document.documentElement, "clientHeight", { configurable: true, value: 800 });
    Object.defineProperty(window, "scrollY", { configurable: true, value: 600 });

    render(
      <ArticleMobileProgress
        backToTopLabel="回到頂部"
        contentsLabel="本篇目錄"
        closeLabel="關閉目錄"
        headings={[
          { id: "section-1", text: "重點比較" },
          { id: "section-2", text: "常見問題" },
        ]}
      />,
    );
    fireEvent.scroll(window);

    const trigger = screen.getByRole("button", { name: "本篇目錄" });
    fireEvent.click(trigger);

    const dialog = screen.getByRole("dialog", { name: "本篇目錄" });
    expect(within(dialog).getByText("50%")).toBeTruthy();
    const firstJump = within(dialog).getByRole("link", { name: /重點比較/ });
    expect(firstJump.getAttribute("href")).toBe("#section-1");
    fireEvent.click(firstJump);
    expect(screen.queryByRole("dialog", { name: "本篇目錄" })).toBeNull();

    Object.defineProperty(window, "scrollY", { configurable: true, value: 0 });
  });
});

