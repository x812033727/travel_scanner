import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LifeArticlePage, { generateMetadata } from "./page";

/**
 * A lifestyle article shares the article screen with `/guides/[kind]/[slug]`, so these cases
 * cover what the section changes: its own URL and breadcrumb, the crosslinks that always end
 * it, and the partner panel that appears only when an editor named a destination.
 */

const mocks = vi.hoisted(() => ({ article: vi.fn(), list: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/guides.server", () => ({ getGuideArticle: mocks.article, getGuideList: mocks.list }));
vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: { destinationId: string; modules?: string[]; placement?: string; contextual?: boolean }) => (
    <div
      data-testid="affiliate"
      data-destination={props.destinationId}
      data-modules={(props.modules ?? []).join(",")}
      data-placement={props.placement}
      data-contextual={String(Boolean(props.contextual))}
    />
  ),
}));

const document = {
  title: "我每天在用的 AI 工具",
  description: "四個工具與各自的代價",
  version: 1,
  published_at: "2026-09-10T00:00:00Z",
  blocks: [{ type: "paragraph" as const, text: "先講結論。" }],
  sources: [],
};

const published = {
  slug: "ai-notes", kind: "life" as const, locale: "zh-TW", status: "published" as const,
  destination_id: null, destination_label: null,
  topics: [{ slug: "ai", label: "AI 工具", section: "life" as const }],
  valid_until: null, expired: false,
  document, published_locales: ["zh-TW" as const, "ja" as const],
};

const travelSummary = {
  slug: "narita-to-tokyo", kind: "howto" as const, destination_id: "tokyo",
  destination_label: "東京", topics: [{ slug: "transport", label: "交通" }],
  title: "成田到東京怎麼走", description: "三種選擇",
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: false,
};

const params = (over: Record<string, string> = {}) =>
  Promise.resolve({ locale: "zh-TW" as const, slug: "ai-notes", ...over });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.article.mockResolvedValue(published);
  mocks.list.mockResolvedValue({ articles: [travelSummary], next_cursor: null });
});

describe("a published lifestyle article", () => {
  it("loads itself by its own kind, which is fixed by the route", async () => {
    render(await LifeArticlePage({ params: params() }));
    expect(mocks.article).toHaveBeenCalledWith("life", "ai-notes", "zh-TW");
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("我每天在用的 AI 工具");
    expect(screen.getByText("先講結論。")).toBeTruthy();
  });

  it("returns the reader to the lifestyle listing, not a /guides one", async () => {
    render(await LifeArticlePage({ params: params() }));
    expect(screen.getByRole("link", { name: "生活分享" }).getAttribute("href")).toBe("/life");
  });

  it("links its other languages at the lifestyle URL", async () => {
    render(await LifeArticlePage({ params: params() }));
    const japanese = screen.getByRole("link", { name: "日本語" });
    expect(japanese.getAttribute("href")).toBe("/ja/life/ai-notes");
    expect(japanese.getAttribute("hreflang")).toBe("ja");
  });

  it("always ends with the travel crosslinks, whether or not it has a destination", async () => {
    render(await LifeArticlePage({ params: params() }));
    expect(mocks.list).toHaveBeenCalledWith("zh-TW", { section: "travel" }, 3);
    expect(screen.getByRole("heading", { name: "最新旅遊情報攻略" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "成田到東京怎麼走" }).getAttribute("href"))
      .toBe("/guides/howto/narita-to-tokyo");
    expect(screen.getByRole("heading", { name: "熱門目的地" })).toBeTruthy();
  });

  it("carries no partner buttons without a destination, which is the usual case", async () => {
    render(await LifeArticlePage({ params: params() }));
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });

  it("offers the named destination's partners once an editor sets one", async () => {
    mocks.article.mockResolvedValue({
      ...published, destination_id: "tokyo", destination_label: "東京",
    });
    render(await LifeArticlePage({ params: params() }));
    const panel = screen.getByTestId("affiliate");
    expect(panel.getAttribute("data-destination")).toBe("tokyo");
    expect(panel.getAttribute("data-placement")).toBe("life");
    expect(panel.getAttribute("data-modules")).toBe("flight,hotel,activities,transport,connectivity");
  });

  it("still renders the crosslinks when there is no travel article to show", async () => {
    mocks.list.mockResolvedValue({ articles: [], next_cursor: null });
    render(await LifeArticlePage({ params: params() }));
    expect(screen.queryByRole("heading", { name: "最新旅遊情報攻略" })).toBeNull();
    expect(screen.getByRole("heading", { name: "熱門目的地" })).toBeTruthy();
  });
});

describe("what a lifestyle article tells search engines", () => {
  it("declares only the locales it is genuinely published in", async () => {
    const metadata = await generateMetadata({ params: params() });
    const languages = metadata.alternates!.languages!;
    expect(Object.keys(languages).sort()).toEqual(["ja", "zh-TW"]);
    expect(languages["zh-TW"]).toContain("/zh-TW/life/ai-notes");
    expect(languages.ja).toContain("/ja/life/ai-notes");
    expect(metadata.alternates!.canonical).toContain("/zh-TW/life/ai-notes");
  });

  it("offers x-default only once English exists", async () => {
    mocks.article.mockResolvedValue({ ...published, published_locales: ["zh-TW", "en"] });
    const metadata = await generateMetadata({ params: params() });
    expect(metadata.alternates!.languages!["x-default"]).toContain("/en/life/ai-notes");
  });

  it("is never indexed in a language nobody wrote, so an empty page cannot outrank it", async () => {
    mocks.article.mockResolvedValue({
      ...published, status: "unpublished", document: null, published_locales: ["ja"],
    });
    const metadata = await generateMetadata({ params: params() });
    expect(metadata.robots).toEqual({ index: false });
    expect(metadata.alternates?.languages).toBeUndefined();

    render(await LifeArticlePage({ params: params() }));
    expect(screen.getByRole("status")).toBeTruthy();
    expect(screen.getByRole("link", { name: "日本語" }).getAttribute("href"))
      .toBe("/ja/life/ai-notes");
  });

  it("keeps a broken article out of the index rather than publishing a blank one", async () => {
    mocks.article.mockResolvedValue({
      ...published, status: "unavailable", document: null, published_locales: [],
    });
    const metadata = await generateMetadata({ params: params() });
    expect(metadata.robots).toEqual({ index: false });

    render(await LifeArticlePage({ params: params() }));
    expect(screen.getByRole("alert")).toBeTruthy();
  });
});
