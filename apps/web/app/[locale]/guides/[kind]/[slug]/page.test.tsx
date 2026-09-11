import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import GuideArticlePage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({ article: vi.fn(), notFound: vi.fn(() => { throw new Error("NEXT_NOT_FOUND"); }) }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/guides.server", () => ({ getGuideArticle: mocks.article }));
vi.mock("next/navigation", () => ({ notFound: mocks.notFound }));

const document = {
  title: "成田機場到東京車站怎麼走",
  description: "三種交通方式的時間與票價比較",
  version: 2,
  published_at: "2026-09-01T00:00:00Z",
  blocks: [{ type: "paragraph" as const, text: "Skyliner 最快。" }],
  sources: [{ title: "京成電鐵時刻表", url: "https://www.keisei.co.jp/", checked_on: "2026-09-01" }],
};

const published = {
  slug: "narita-to-tokyo", kind: "howto" as const, locale: "zh-TW", status: "published" as const,
  destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], valid_until: null, expired: false,
  document, published_locales: ["zh-TW" as const, "ja" as const],
};

const params = (over: Record<string, string> = {}) =>
  Promise.resolve({ locale: "zh-TW" as const, kind: "howto", slug: "narita-to-tokyo", ...over });

beforeEach(() => {
  vi.clearAllMocks();
  mocks.article.mockResolvedValue(published);
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
    expect(screen.getByRole("link", { name: "交通" })).toBeTruthy();
  });

  it("declares only the locales that are genuinely published", async () => {
    const metadata = await generateMetadata({ params: params() });
    expect(metadata.title).toBe("成田機場到東京車站怎麼走");
    expect(Object.keys(metadata.alternates!.languages!).sort()).toEqual(["ja", "zh-TW"]);
    expect(metadata.robots).toBeUndefined();
  });

  it("offers x-default only when the English version exists", async () => {
    mocks.article.mockResolvedValue({ ...published, published_locales: ["zh-TW", "en"] });
    const metadata = await generateMetadata({ params: params() });
    expect(metadata.alternates!.languages!["x-default"]).toContain("/en/guides/howto/narita-to-tokyo");
  });

  it("links the other languages from the page itself, not only from the head", async () => {
    render(await GuideArticlePage({ params: params() }));
    const link = screen.getByRole("link", { name: "日本語" });
    expect(link.getAttribute("href")).toBe("/ja/guides/howto/narita-to-tokyo");
    expect(link.getAttribute("hreflang")).toBe("ja");
  });
});

describe("an expired notice", () => {
  const expired = {
    ...published, kind: "intel" as const, expired: true, valid_until: "2026-08-01",
  };

  it("keeps its page and says what date it applied until", async () => {
    mocks.article.mockResolvedValue(expired);
    render(await GuideArticlePage({ params: params({ kind: "intel" }) }));
    expect(screen.getByRole("heading", { level: 1 })).toBeTruthy();
    expect(screen.getByRole("status").textContent).toContain("2026-08-01");
  });

  it("stays indexable, because withdrawing the URL would break existing links", async () => {
    mocks.article.mockResolvedValue(expired);
    const metadata = await generateMetadata({ params: params({ kind: "intel" }) });
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
    const metadata = await generateMetadata({ params: params({ locale: "ko" }) });
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
    expect((await generateMetadata({ params: params() })).robots).toEqual({ index: false });
  });
});
