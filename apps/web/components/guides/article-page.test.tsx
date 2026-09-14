import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { renderGuideArticle } from "./article-page";
import type { LearningEntry } from "@/lib/codex-learning";

const mocks = vi.hoisted(() => ({ article: vi.fn(), series: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: async () => ({ enabled: false }) }));
vi.mock("@/lib/guides.server", () => ({
  getGuideArticle: mocks.article, getGuideSeries: mocks.series,
  getGuideList: async () => ({ articles: [], next_cursor: null }),
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
