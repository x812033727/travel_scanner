import { cleanup, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { renderGuideArticle } from "./article-page";
import type { LearningEntry } from "@/lib/codex-learning";

const mocks = vi.hoisted(() => ({
  article: vi.fn(), series: vi.fn(), topics: vi.fn(async (): Promise<Record<string, unknown>[]> => []),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: async () => ({ enabled: false }) }));
vi.mock("@/lib/guides.server", () => ({
  getGuideArticle: mocks.article, getGuideSeries: mocks.series,
  getGuideList: async () => ({ articles: [], next_cursor: null }),
  getGuideTopics: mocks.topics,
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

beforeEach(() => { vi.clearAllMocks(); mocks.article.mockResolvedValue(state); mocks.series.mockResolvedValue({
  slug: "codex", locale: "en", hub: reference, groups: [], paths: [], entries: [current],
}); });

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
    // The lifestyle handover to the travel section still follows.
    expect(screen.getByTestId("travel-crosslinks")).toBeTruthy();
    const order = [screen.getByTestId("related-grid"), screen.getByTestId("backlinks"), screen.getByTestId("travel-crosslinks")];
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
      "/life", "/life/topics/ai", "/life/topics/ai-terms",
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
      .toEqual(["/life", "/life/topics/ai"]);
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
});
