import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { siteUrl } from "@/lib/seo";
import VideoWatchPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({
  getVideo: vi.fn(),
  getGuideArticle: vi.fn(),
  notFound: vi.fn(() => {
    throw new Error("NEXT_NOT_FOUND");
  }),
}));

vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("next/navigation", () => ({ notFound: mocks.notFound }));
vi.mock("@/lib/videos.server", () => ({ getVideo: mocks.getVideo }));
vi.mock("@/lib/guides.server", () => ({ getGuideArticle: mocks.getGuideArticle }));

const sampleVideo = {
  slug: "gemini-cli-demo",
  title: "Gemini CLI 實測教學",
  youtube_video_id: "abcdefghijk",
  category: "tutorial",
  kind: "long" as const,
  source_guide: "gemini-cli-guide",
  source_guide_kind: "life" as const,
  published_at: "2026-11-18T12:00:00Z",
};

const relatedVideo = {
  slug: "claude-code-tips",
  title: "Claude Code 工作流",
  youtube_video_id: "12345678901",
  category: "tutorial",
  kind: "long" as const,
  source_guide: null,
  source_guide_kind: null,
  published_at: "2026-11-17T12:00:00Z",
};

beforeEach(() => {
  mocks.getVideo.mockReset().mockResolvedValue({
    status: "found",
    video: sampleVideo,
    related: [relatedVideo],
  });
  mocks.getGuideArticle.mockReset().mockResolvedValue({
    status: "published",
    document: {
      title: "Gemini CLI 完整攻略",
      description: "從安裝到免費額度與 MCP 設定一次看懂。",
    },
  });
  mocks.notFound.mockClear();
});

describe("/videos/[slug]", () => {
  it("renders dedicated watch page with high-priority thumbnail, companion article, related videos, and VideoObject JSON-LD", async () => {
    const { container } = render(
      await VideoWatchPage({
        params: Promise.resolve({ locale: "zh-TW" as const, slug: "gemini-cli-demo" }),
      }),
    );

    expect(screen.getByRole("heading", { level: 1, name: "Gemini CLI 實測教學" })).toBeTruthy();
    const img = screen.getByRole("img", { name: "Gemini CLI 實測教學" });
    expect(img.getAttribute("fetchpriority")).toBe("high");
    expect(container.querySelector("iframe")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "播放「Gemini CLI 實測教學」" }));
    expect(container.querySelector("iframe")?.getAttribute("src")).toBe(
      "https://www.youtube-nocookie.com/embed/abcdefghijk?autoplay=1&rel=0",
    );

    expect(screen.getByRole("link", { name: "Gemini CLI 完整攻略" }).getAttribute("href")).toBe(
      "/life/gemini-cli-guide",
    );
    expect(screen.getByRole("link", { name: "Claude Code 工作流" }).getAttribute("href")).toBe(
      "/videos/claude-code-tips",
    );

    const scripts = Array.from(container.querySelectorAll('script[type="application/ld+json"]')).map(
      (node) => node.textContent || "",
    );
    const joined = scripts.join("\n");
    expect(joined).toContain('"@type":"VideoObject"');
    expect(joined).toContain(`${siteUrl}/zh-TW/videos/gemini-cli-demo#video-gemini-cli-demo`);
    expect(joined).toContain('"@type":"BreadcrumbList"');
    expect(joined).toContain('"@type":"ItemList"');
  });

  it("emits Discover robots, video OpenGraph metadata, and companion description", async () => {
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "zh-TW" as const, slug: "gemini-cli-demo" }),
    });

    expect(meta.title).toBe("Gemini CLI 實測教學 | Mokaair");
    expect(meta.description).toBe("從安裝到免費額度與 MCP 設定一次看懂。");
    expect(meta.robots).toMatchObject({
      index: true,
      follow: true,
      googleBot: { "max-image-preview": "large", "max-snippet": -1, "max-video-preview": -1 },
    });
    expect(meta.alternates?.canonical).toBe(`${siteUrl}/zh-TW/videos/gemini-cli-demo`);
  });

  it("calls notFound when the video is missing or unpublished, and returns noindex on API outage", async () => {
    mocks.getVideo.mockResolvedValueOnce({ status: "not_found" });
    await expect(
      generateMetadata({ params: Promise.resolve({ locale: "zh-TW" as const, slug: "missing" }) }),
    ).rejects.toThrow("NEXT_NOT_FOUND");

    mocks.getVideo.mockResolvedValueOnce({ status: "unavailable" });
    const outage = await generateMetadata({
      params: Promise.resolve({ locale: "zh-TW" as const, slug: "gemini-cli-demo" }),
    });
    expect(outage.robots).toEqual({ index: false, follow: true });
  });
});
