import { act, render, screen, within } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import type { AnchorHTMLAttributes } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./page";
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
vi.mock("@/lib/guides.server", () => ({ getGuideList: state.guides }));

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
    expect(screen.getByRole("heading", { level: 2, name: "旅行與生活的實用指南" })).toBeTruthy();
    expect(screen.getByText(/個人站長經營/)).toBeTruthy();
    const introduction = screen.getByRole("region", { name: "旅行與生活的實用指南" });
    expect(introduction.compareDocumentPosition(document.getElementById("trip-search")!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
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
    const introduction = within(parsed).getByRole("region", { name: "旅行與生活的實用指南" });
    const followingBody = parsed.querySelector("main");
    expect(followingBody).toBeTruthy();
    expect(introduction.compareDocumentPosition(followingBody!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(within(introduction).getByText(/個人站長經營/)).toBeTruthy();
    for (const article of Object.values(articleGroups).flat()) {
      const href = article.kind === "howto" ? `/guides/howto/${article.slug}` : `/life/${article.slug}`;
      expect(within(introduction).getByRole("link", { name: article.title }).getAttribute("href")).toBe(href);
      expect(within(introduction).getByText(article.description)).toBeTruthy();
    }
    expect(introduction.querySelectorAll("li[data-variant=compact]")).toHaveLength(12);
    expect(within(introduction).getByRole("link", { name: "搜尋機票與住宿" }).getAttribute("href")).toBe("/search/new");
    if (feed) {
      expect(parsed.querySelectorAll("article[id^='guide:discovery-']")).toHaveLength(20);
    } else {
      expect(parsed.querySelector("#trip-search")).toBeTruthy();
      expect(within(parsed).getByRole("link", { name: "東京" }).getAttribute("href")).toBe("/destinations/tokyo");
    }
  });
});
