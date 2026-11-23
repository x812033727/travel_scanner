// @vitest-environment node
import { beforeEach, describe, expect, it, vi } from "vitest";
import { getGuideArticle } from "@/lib/guides.server";
import { loadSubsetFont } from "@/lib/article-og";
import { GET } from "./route";

vi.mock("@/lib/guides.server", () => ({
  getGuideArticle: vi.fn(),
}));

vi.mock("@/lib/article-og", async (original) => ({
  ...(await original<typeof import("@/lib/article-og")>()),
  loadSubsetFont: vi.fn(),
}));

const publishedEn = {
  slug: "claude-api-pricing-2026",
  kind: "life" as const,
  locale: "en" as const,
  status: "published" as const,
  destination_id: null,
  destination_label: null,
  topics: [{ slug: "ai-news", label: "AI News" }],
  valid_until: null,
  news_date: "2026-11-20",
  expired: false,
  published_locales: ["en" as const],
  document: {
    title: "Claude API pricing update and context limits",
    description: "What changed across input tokens, prompt caching, and batch tiers.",
    version: 1,
    published_at: "2026-11-20T01:00:00Z",
    modified_at: "2026-11-20T01:00:00Z",
    blocks: [{ type: "paragraph" as const, text: "Details." }],
    sources: [],
  },
};

const req = () => new Request("https://mokaair.com/og/en/life/claude-api-pricing-2026/card.png");

beforeEach(() => {
  vi.clearAllMocks();
  vi.mocked(getGuideArticle).mockResolvedValue(publishedEn);
  vi.mocked(loadSubsetFont).mockResolvedValue(null);
});

describe("/og/[locale]/[kind]/[slug]/card.png", () => {
  it("returns 404 for unknown locales, unknown kinds, invalid slugs, or unpublished articles", async () => {
    const badLocale = await GET(req(), { params: Promise.resolve({ locale: "fr", kind: "life", slug: "valid-slug" }) });
    expect(badLocale.status).toBe(404);
    const badKind = await GET(req(), { params: Promise.resolve({ locale: "en", kind: "recipes", slug: "valid-slug" }) });
    expect(badKind.status).toBe(404);
    const badSlug = await GET(req(), { params: Promise.resolve({ locale: "en", kind: "life", slug: "Invalid_Slug" }) });
    expect(badSlug.status).toBe(404);
    expect(getGuideArticle).not.toHaveBeenCalled();

    vi.mocked(getGuideArticle).mockResolvedValueOnce({ ...publishedEn, status: "unpublished", document: null });
    const unpublished = await GET(req(), { params: Promise.resolve({ locale: "en", kind: "life", slug: "claude-api-pricing-2026" }) });
    expect(unpublished.status).toBe(404);
  });

  it("renders a cached PNG card for an English published article without needing an external font fetch", async () => {
    const response = await GET(req(), {
      params: Promise.resolve({ locale: "en", kind: "life", slug: "claude-api-pricing-2026" }),
    });
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toContain("image/png");
    expect(response.headers.get("cache-control")).toContain("max-age=3600");
    const bytes = new Uint8Array(await response.arrayBuffer());
    // PNG magic header: 89 50 4E 47
    expect(Array.from(bytes.slice(0, 4))).toEqual([0x89, 0x50, 0x4e, 0x47]);
    expect(loadSubsetFont).not.toHaveBeenCalled();
  });

  it("falls back to static /og.png rather than rendering tofu when CJK font loading fails", async () => {
    vi.mocked(getGuideArticle).mockResolvedValueOnce({
      ...publishedEn,
      locale: "zh-TW",
      topics: [{ slug: "ai-news", label: "AI 新聞" }],
      document: {
        ...publishedEn.document,
        title: "Claude API 價格與上下文上限調整",
        description: "整理輸入輸出計費與快取折扣的實際變動。",
      },
    });
    vi.mocked(loadSubsetFont).mockResolvedValueOnce(null);

    const response = await GET(req(), {
      params: Promise.resolve({ locale: "zh-TW", kind: "life", slug: "claude-api-pricing-2026" }),
    });
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toBe("image/png");
    expect(response.headers.get("cache-control")).toBe("public, max-age=300");
    const bytes = new Uint8Array(await response.arrayBuffer());
    expect(Array.from(bytes.slice(0, 4))).toEqual([0x89, 0x50, 0x4e, 0x47]);
    expect(loadSubsetFont).toHaveBeenCalledTimes(1);
  });
});
