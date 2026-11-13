import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { GuideSummary } from "@/lib/guides";
import { HomeGuides, type HomeGuideBlock } from "./home-guides";

const article = (
  slug: string,
  kind: GuideSummary["kind"],
  title: string,
  overrides: Partial<GuideSummary> = {},
): GuideSummary => ({
  slug,
  kind,
  destination_id: null,
  destination_label: null,
  topics: [],
  title,
  description: `${title}的描述`,
  published_at: "2026-09-16T05:00:00Z",
  valid_until: null,
  news_date: null,
  featured: false,
  ...overrides,
});

const blocks = (travel: GuideSummary[], tech: GuideSummary[], money: GuideSummary[]): HomeGuideBlock[] => [
  { key: "tech", href: "/life/topics/ai", articles: tech },
  { key: "travel", href: "/guides", articles: travel },
  { key: "money", href: "/life/topics/finance", articles: money },
];

describe("the home page's portal and guide sections", () => {
  it("says what the site is, offers inline article search and quick links, and lists each section", () => {
    const { container } = render(<HomeGuides blocks={blocks(
      [article("tokyo-first-trip", "howto", "東京第一次自由行")],
      [article("claude-code-intro", "life", "Claude Code 入門")],
      [article("credit-card-basics", "life", "信用卡入門")],
    )} />);
    expect(screen.getByRole("heading", { level: 2, name: "AI 科技快訊、軟體教學與旅遊生活攻略" })).toBeTruthy();
    const directIntro = container.querySelectorAll('section[aria-labelledby="home-guides-title"] > p');
    expect(directIntro).toHaveLength(1);
    expect(directIntro[0]?.textContent).toContain("Mokaair");
    expect(screen.getByText(/個人站長經營/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "搜尋機票與住宿" }).getAttribute("href")).toBe("/search/new");
    expect(screen.getByRole("search").getAttribute("action")).toBe("/zh-TW/search/articles");
    expect(screen.getByRole("link", { name: /RSS 訂閱/ }).getAttribute("href")).toBe("/zh-TW/life/feed.xml");

    const travel = screen.getByTestId("home-guides-travel");
    expect(within(travel).getByRole("heading", { name: "旅遊攻略" })).toBeTruthy();
    expect(within(travel).getByRole("link", { name: "看全部" }).getAttribute("href")).toBe("/guides");
    expect(within(travel).getByRole("link", { name: /東京第一次自由行/ }).getAttribute("href")).toBe("/guides/howto/tokyo-first-trip");

    expect(within(screen.getByTestId("home-guides-tech")).getByRole("link", { name: "看全部" }).getAttribute("href")).toBe("/life/topics/ai");
    expect(within(screen.getByTestId("home-guides-money")).getByRole("link", { name: /信用卡入門/ }).getAttribute("href")).toBe("/life/credit-card-basics");
  });

  it("renders the hero lead story, chronological daily news desk, trending rail, and interactive category filter tabs", () => {
    const news = [
      article("gpt-5-release-20261112", "life", "GPT-5.5 推出免費額度與 API 降價總整理", {
        news_date: "2026-11-12",
        topics: [{ slug: "ai-news", label: "AI 新聞" }],
      }),
      article("ios-27-update-20261111", "life", "iOS 27.1 更新修正電池續航與 Siri 捷徑", {
        news_date: "2026-11-11",
        topics: [{ slug: "tech-news", label: "科技新聞" }],
      }),
    ];
    const trending = [
      article("gemini-cli-guide", "life", "Gemini CLI 免費額度與安裝完整攻略", {
        topics: [{ slug: "ai", label: "AI 應用" }],
      }),
    ];
    render(
      <HomeGuides
        blocks={blocks(
          [article("tokyo-first-trip", "howto", "東京第一次自由行")],
          [article("claude-code-intro", "life", "Claude Code 入門")],
          [article("credit-card-basics", "life", "信用卡入門")],
        )}
        news={news}
        trending={trending}
      />,
    );

    const hero = screen.getByTestId("portal-hero");
    expect(within(hero).getByText("焦點頭條")).toBeTruthy();
    expect(within(hero).getByRole("link", { name: "GPT-5.5 推出免費額度與 API 降價總整理" }).getAttribute("href"))
      .toBe("/life/gpt-5-release-20261112");

    const desk = screen.getByTestId("portal-news-desk");
    expect(within(desk).getByRole("link", { name: "iOS 27.1 更新修正電池續航與 Siri 捷徑" }).getAttribute("href"))
      .toBe("/life/ios-27-update-20261111");
    expect(within(desk).getByRole("link", { name: /RSS 訂閱/ }).getAttribute("href")).toBe("/zh-TW/life/feed.xml");

    const trendingRail = screen.getByTestId("portal-trending");
    expect(within(trendingRail).getByRole("link", { name: "Gemini CLI 免費額度與安裝完整攻略" }).getAttribute("href"))
      .toBe("/life/gemini-cli-guide");

    const tabs = screen.getByTestId("portal-tabs");
    fireEvent.click(within(tabs).getByRole("button", { name: "旅遊攻略" }));
    expect(screen.getByTestId("home-guides-travel")).toBeTruthy();
    expect(screen.queryByTestId("home-guides-tech")).toBeNull();
    expect(screen.queryByTestId("portal-news-desk")).toBeNull();

    fireEvent.click(within(tabs).getByRole("button", { name: "全部總覽" }));
    expect(screen.getByTestId("portal-news-desk")).toBeTruthy();
    expect(screen.getByTestId("home-guides-tech")).toBeTruthy();
  });

  it("leaves out a block with nothing to show and keeps the introduction", () => {
    render(<HomeGuides blocks={blocks([article("tokyo-first-trip", "howto", "東京第一次自由行")], [], [])} />);
    expect(screen.getByTestId("home-guides-travel")).toBeTruthy();
    expect(screen.queryByTestId("home-guides-tech")).toBeNull();
    expect(screen.queryByTestId("home-guides-money")).toBeNull();
    expect(screen.getByText(/個人站長經營/)).toBeTruthy();
  });

  it("renders secondary editorial sub-lead cards alongside the chronological wire when 4+ news stories exist", () => {
    const news = [
      article("lead-1", "life", "頭條焦點一", { news_date: "2026-11-12", topics: [{ slug: "ai-news", label: "AI 新聞" }] }),
      article("sub-2", "life", "次焦點報導二", { news_date: "2026-11-11", topics: [{ slug: "tech-news", label: "科技新聞" }] }),
      article("sub-3", "life", "次焦點報導三", { news_date: "2026-11-10", topics: [{ slug: "ai-news", label: "AI 新聞" }] }),
      article("wire-4", "life", "即時快訊列表四", { news_date: "2026-11-09", topics: [{ slug: "crypto", label: "幣圈" }] }),
    ];
    render(<HomeGuides blocks={blocks([], [], [])} news={news} />);
    const desk = screen.getByTestId("portal-news-desk");
    expect(within(desk).getAllByRole("article")).toHaveLength(3);
    expect(within(desk).getByRole("link", { name: "次焦點報導二" }).getAttribute("href")).toBe("/life/sub-2");
    expect(within(desk).getByRole("link", { name: "次焦點報導三" }).getAttribute("href")).toBe("/life/sub-3");
    expect(within(desk).getByRole("link", { name: "即時快訊列表四" }).getAttribute("href")).toBe("/life/wire-4");
  });

  it("caps overview columns at 4 items and expands full category articles plus matching series on a category tab", () => {
    const aiArticles = [1, 2, 3, 4, 5, 6].map((n) => article(`ai-pick-${n}`, "life", `AI 精選指南 ${n}`));
    render(
      <HomeGuides
        blocks={blocks(
          [article("tokyo-1", "howto", "東京交通")],
          aiArticles,
          [article("money-1", "life", "雙幣卡比較")],
        )}
        series={[
          {
            slug: "claude-code",
            section: "life",
            topic: "ai",
            source: "api-series",
            entries: 12,
            hub: { kind: "life", slug: "claude-code-tutorials", title: "Claude Code 教學中心" },
          },
          {
            slug: "jr-rail",
            section: "travel",
            topic: "transport",
            source: "api-series",
            entries: 5,
            hub: { kind: "howto", slug: "jr-rail-hub", title: "JR 鐵路教學系列" },
          },
        ]}
      />,
    );

    // Overview ("all") keeps each category column compact at 4 items.
    const overviewTech = screen.getByTestId("home-guides-tech");
    expect(within(overviewTech).getAllByRole("listitem")).toHaveLength(4);

    // Switching to AI tab reveals all 6 AI articles and only AI series hubs.
    const tabs = screen.getByTestId("portal-tabs");
    fireEvent.click(within(tabs).getByRole("button", { name: "AI 應用" }));
    expect(within(screen.getByTestId("home-guides-tech")).getAllByRole("listitem")).toHaveLength(6);
    const catSeries = screen.getByTestId("portal-category-series");
    expect(within(catSeries).getByRole("link", { name: "Claude Code 教學中心" })).toBeTruthy();
    expect(within(catSeries).queryByText("JR 鐵路教學系列")).toBeNull();
  });
});
