import { act, render, screen, within } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import type { AnchorHTMLAttributes } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./page";
import { loadHomeGuides } from "@/components/home-guides";
import { ThemeProvider } from "@/components/theme-provider";
import type { DiscoveryItem } from "@/lib/discovery";
import type { InitialDiscoveryFeed } from "@/lib/discovery.server";
import type { GuideSummary } from "@/lib/guides";

const state = vi.hoisted(() => ({ enabled: false, loading: false, feed: null as InitialDiscoveryFeed, guides: vi.fn() }));

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn(), refresh: vi.fn() }), useSearchParams: () => new URLSearchParams() }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, scroll, ...props }: AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; scroll?: boolean }) => {
    void scroll; return <a href={href} {...props}>{children}</a>;
  },
  usePathname: () => "/",
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), refresh: vi.fn() }),
}));
vi.mock("@/lib/discovery", async (original) => ({ ...await original<typeof import("@/lib/discovery")>(), useDiscoveryStatus: () => ({ enabled: state.enabled, loading: state.loading }) }));
vi.mock("@/lib/discovery-status.server", () => ({ getDiscoveryStatus: async () => ({ enabled: state.enabled }) }));
vi.mock("@/lib/discovery.server", async (original) => ({
  ...await original<typeof import("@/lib/discovery.server")>(), getInitialDiscoveryFeed: async () => state.feed,
}));
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(),
  getGuideList: state.guides,
  getTrendingGuides: vi.fn(async () => ({ articles: [], next_cursor: null, available: false })),
  getSeriesIndex: vi.fn(async () => []),
}));

const articles = (group: string, kind: GuideSummary["kind"]): GuideSummary[] => Array.from({ length: 4 }, (_, index) => ({
  slug: `${group}-article-${index}`, kind, destination_id: null, destination_label: null, topics: [],
  title: `${group} article ${index}`, description: `${group} article ${index} explains an actual reader decision`,
  published_at: "2026-09-16T05:00:00Z", valid_until: null, news_date: null, featured: false,
}));
const articleGroups = { travel: articles("travel", "howto"), tech: articles("tech", "life"), money: articles("money", "life") };
const discoveryItems: DiscoveryItem[] = Array.from({ length: 20 }, (_, index) => ({
  id: `guide:discovery-${index}`, kind: "article", title: `Discovery card ${index}`, summary: "A recently published item",
  locale: "zh-TW", href: `/life/discovery-${index}`, destination: null,
  source: { label: "Mokaair", url: null, kind: "editorial" },
  published_at: "2026-09-16T05:00:00Z", updated_at: null, thumbnail_url: null,
}));
const seededFeed: InitialDiscoveryFeed = {
  path: "/discovery/feed?mode=recommended",
  page: { enabled: true, items: discoveryItems, next_cursor: null, query: "", filters: { kinds: [], destinations: [], topics: [] } },
};

describe("home", () => {
  beforeEach(() => {
    state.enabled = false; state.loading = false; state.feed = null;
    state.guides.mockReset().mockResolvedValue({ articles: [], next_cursor: null });
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(
      JSON.stringify({ detail: "not signed in" }),
      { status: 401 },
    )));
  });

  it("keeps the original primary trip search when discovery is resolved off", async () => {
    const home = await Home();
    await act(async () => { render(home, { wrapper: ThemeProvider }); });
    expect(screen.getByRole("heading", { name: /不用寫完整句子/ })).toBeTruthy();
    expect(screen.getByRole("button", { name: /下一步/ })).toBeTruthy();
    expect(document.getElementById("trip-search")).toBeTruthy();
  });

  it("says what the site is before the search, even when every article read fails", async () => {
    const home = await Home();
    await act(async () => { render(home, { wrapper: ThemeProvider }); });
    expect(screen.getByRole("heading", { level: 1, name: "AI 科技快訊、軟體教學與旅遊生活攻略" })).toBeTruthy();
    expect(screen.getByText(/個人站長經營/)).toBeTruthy();
    const introduction = screen.getByRole("region", { name: "AI 科技快訊、軟體教學與旅遊生活攻略" });
    expect(introduction.compareDocumentPosition(document.getElementById("trip-search")!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it("server-renders the newest dated story and links to every populated news channel before the desk cutoff", async () => {
    const aiTopic = { slug: "ai-news", label: "AI 新聞與趨勢" };
    const [template] = articleGroups.tech;
    const aiNews = Array.from({ length: 11 }, (_, index) => ({
      ...template, slug: `daily-ai-${index}`, title: `AI daily ${index}`,
      topics: [{ slug: "ai", label: "AI 應用" }, aiTopic], news_date: `2026-11-${String(18 - index).padStart(2, "0")}`,
    }));
    const olderTech = { ...template, slug: "older-tech", news_date: "2026-11-07", topics: [{ slug: "tech-news", label: "科技新聞" }] };
    const lists: Record<string, GuideSummary[]> = {
      ai: [aiNews[0]],
      "ai-news": aiNews,
      "tech-news": [olderTech],
      crypto: [{ ...template, topics: [{ slug: "crypto", label: "加密貨幣" }] }],
    };
    state.guides.mockImplementation(async (_locale: string, filters: { topic?: string }, limit: number) => ({
      articles: (lists[filters.topic ?? ""] ?? []).slice(0, limit), next_cursor: null,
    }));
    const html = renderToStaticMarkup(<ThemeProvider>{await Home()}</ThemeProvider>);
    const { container } = render(<div dangerouslySetInnerHTML={{ __html: html }} />);
    const desk = within(container).getByTestId("portal-news-desk");
    expect(within(desk).getByRole("heading", { level: 2, name: "每日即時快訊" })).toBeTruthy();
    const hero = within(desk).getByTestId("portal-hero");
    expect(within(hero).getByRole("heading", { level: 3, name: aiNews[0].title })).toBeTruthy();
    expect(within(hero).getByRole("link", { name: aiNews[0].title })).toBeTruthy();
    expect(within(hero).getByText(aiTopic.label)).toBeTruthy();
    expect(within(hero).queryByText("AI 應用")).toBeNull();
    expect(Array.from(desk.querySelectorAll("time"), (time) => time.dateTime)).toEqual(aiNews.map((story) => story.news_date));
    expect(container.querySelectorAll('a[href="/life/daily-ai-0"]')).toHaveLength(1);
    const links = within(desk);
    expect(links.getByRole("link", { name: "AI 新聞" }).getAttribute("href")).toBe("/life/topics/ai-news");
    expect(links.getByRole("link", { name: "科技新聞" }).getAttribute("href")).toBe("/life/topics/tech-news");
    expect(desk.querySelector('a[href="/life/older-tech"]')).toBeNull();
    expect(desk.querySelector('a[href="/life/topics/crypto"]')).toBeNull();
    expect(links.getByRole("link", { name: "看全部" }).getAttribute("href")).toBe("/life#life-news-heading");
    expect(links.getByRole("link", { name: "RSS 訂閱" }).getAttribute("href")).toBe("/zh-TW/life/feed.xml");
  });

  it("merges news channels by event date and lists a cross-tagged story once", async () => {
    const [template] = articleGroups.tech;
    const shared = { ...template, slug: "two-channels", news_date: "2026-11-15" };
    const newest = { ...template, slug: "newest", news_date: "2026-11-17" };
    const middle = { ...template, slug: "middle", news_date: "2026-11-16" };
    const lists: Record<string, GuideSummary[]> = {
      "ai-news": [shared], crypto: [newest, shared], "tech-news": [middle],
    };
    state.guides.mockImplementation(async (_locale: string, filters: { topic?: string }) => ({
      articles: lists[filters.topic ?? ""] ?? [], next_cursor: null,
    }));
    const { news, newsTopics } = await loadHomeGuides("zh-TW");
    expect(news.map((article) => article.slug)).toEqual(["newest", "middle", "two-channels"]);
    expect(newsTopics).toEqual(["ai-news", "crypto", "tech-news"]);
  });

  it.each([
    { label: "discovery off", enabled: false, feed: null },
    { label: "discovery on", enabled: true, feed: seededFeed },
    { label: "an unavailable discovery feed", enabled: true, feed: null },
  ])("server-renders the introduction and twelve article links before $label, keeping a direct search entrance", async ({ enabled, feed }) => {
    state.enabled = enabled; state.loading = true; state.feed = feed;
    state.guides.mockImplementation(async (_locale: string, filters: { kind: string; topic?: string }) => ({
      articles: filters.kind === "howto" ? articleGroups.travel : filters.topic === "ai" ? articleGroups.tech : articleGroups.money,
      next_cursor: null,
    }));
    const html = renderToStaticMarkup(<ThemeProvider>{await Home()}</ThemeProvider>);
    // Mount only the server's HTML; the page components are not hydrated here.
    const { container: parsed } = render(<div dangerouslySetInnerHTML={{ __html: html }} />);
    const introduction = within(parsed).getByRole("region", { name: "AI 科技快訊、軟體教學與旅遊生活攻略" });
    expect(within(parsed).getAllByRole("heading", { level: 1 })).toEqual([
      within(introduction).getByRole("heading", { level: 1, name: "AI 科技快訊、軟體教學與旅遊生活攻略" }),
    ]);
    const main = within(parsed).getByRole("main");
    expect(main.contains(introduction)).toBe(true);
    expect(within(introduction).getByText(/個人站長經營/)).toBeTruthy();
    for (const article of Object.values(articleGroups).flat()) {
      const href = article.kind === "howto" ? `/guides/howto/${article.slug}` : `/life/${article.slug}`;
      expect(within(introduction).getByRole("link", { name: article.title }).getAttribute("href")).toBe(href);
      expect(within(introduction).getByText(article.description)).toBeTruthy();
    }
    expect(introduction.querySelectorAll("li[data-variant=compact]")).toHaveLength(12);
    expect(within(introduction).getByRole("link", { name: "搜尋機票與住宿" }).getAttribute("href")).toBe("/search/new");
    const followingBody = main.querySelector(feed ? "article[id^='guide:discovery-']" : "#trip-search");
    expect(followingBody).toBeTruthy();
    expect(introduction.compareDocumentPosition(followingBody!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    if (feed) {
      expect(parsed.querySelectorAll("article[id^='guide:discovery-']")).toHaveLength(20);
    } else {
      expect(parsed.querySelector("#trip-search")).toBeTruthy();
      expect(within(parsed).getByRole("link", { name: "東京" }).getAttribute("href")).toBe("/destinations/tokyo");
    }
  });
});
