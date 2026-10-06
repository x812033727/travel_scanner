import { fireEvent, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import VideosPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({
  videos: vi.fn(),
  redirect: vi.fn((url: string) => { throw new Error(`NEXT_REDIRECT ${url}`); }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("next/navigation", () => ({ redirect: mocks.redirect }));
vi.mock("@/lib/videos.server", () => ({ getVideos: mocks.videos }));

const video = (slug: string, over: Record<string, unknown> = {}) => ({
  slug, title: `影片 ${slug}`, youtube_video_id: "abcdefghijk", category: "tutorial", kind: "long",
  source_guide: "cursor-editor-guide", source_guide_kind: "life", published_at: "2026-10-01T00:00:00Z", ...over,
});
const page = (over: Record<string, unknown> = {}) => ({ videos: [video("a")], next_cursor: null, categories: ["tutorial", "comparison"], available: true, ...over });
const open = async (search: Record<string, string> = {}) =>
  render(await VideosPage({ params: Promise.resolve({ locale: "zh-TW" as const }), searchParams: Promise.resolve(search) }));

beforeEach(() => {
  mocks.videos.mockReset().mockResolvedValue(page());
  mocks.redirect.mockClear();
});

describe("/videos", () => {
  it("lists each video with its article and plays it in place only when asked", async () => {
    await open();
    const card = screen.getByRole("listitem");
    expect(within(card).getByRole("heading", { name: "影片 a" })).toBeTruthy();
    expect(within(card).getByText("教學")).toBeTruthy();
    expect(within(card).getByRole("link", { name: "看文章版" }).getAttribute("href")).toBe("/life/cursor-editor-guide");
    expect(card.querySelector("iframe")).toBeNull();
    fireEvent.click(within(card).getByRole("button", { name: "播放「影片 a」" }));
    expect(card.querySelector("iframe")?.getAttribute("src")).toBe("https://www.youtube-nocookie.com/embed/abcdefghijk?autoplay=1&rel=0");
  });

  it("filters by length and category through plain links", async () => {
    await open({ kind: "shorts" });
    expect(mocks.videos).toHaveBeenCalledWith("zh-TW", { category: undefined, kind: "shorts", cursor: undefined });
    const lengths = screen.getByRole("navigation", { name: "影片長度" });
    expect(within(lengths).getByRole("link", { name: "Shorts" }).getAttribute("aria-current")).toBe("page");
    const categories = screen.getByRole("navigation", { name: "影片分類" });
    expect(within(categories).getByRole("link", { name: "比較實測" }).getAttribute("href")).toBe("/videos?kind=shorts&category=comparison");
  });

  it("says the list is unavailable rather than empty when the API does not answer", async () => {
    mocks.videos.mockResolvedValue(page({ videos: [], categories: [], available: false }));
    await open();
    expect(screen.getByText("暫時無法取得影片清單，請稍後再試。")).toBeTruthy();
  });

  it("pages with a cursor and restarts when the cursor is stale", async () => {
    mocks.videos.mockResolvedValue(page({ next_cursor: "c2" }));
    await open();
    expect(screen.getByRole("link", { name: "看更多影片" }).getAttribute("href")).toBe("/videos?cursor=c2");
    mocks.videos.mockResolvedValue(page({ videos: [] }));
    await expect(open({ cursor: "old", kind: "long" })).rejects.toThrow("NEXT_REDIRECT /zh-TW/videos?kind=long");
  });

  it("keeps filtered views out of the index", async () => {
    const plain = await generateMetadata({ params: Promise.resolve({ locale: "zh-TW" as const }), searchParams: Promise.resolve({}) });
    expect(plain.robots).toBeUndefined();
    const filtered = await generateMetadata({ params: Promise.resolve({ locale: "zh-TW" as const }), searchParams: Promise.resolve({ kind: "shorts" }) });
    expect(filtered.robots).toEqual({ index: false, follow: true });
  });
});
