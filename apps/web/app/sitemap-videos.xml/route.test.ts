import { beforeEach, describe, expect, it, vi } from "vitest";
import { siteUrl } from "@/lib/seo";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  getAllPublishedVideos: vi.fn(),
}));

vi.mock("@/lib/videos.server", () => ({
  getAllPublishedVideos: mocks.getAllPublishedVideos,
}));

beforeEach(() => {
  mocks.getAllPublishedVideos.mockReset();
});

describe("/sitemap-videos.xml", () => {
  it("renders Google Video Sitemap XML pointing at canonical watch pages", async () => {
    mocks.getAllPublishedVideos.mockResolvedValue({
      available: true,
      videos: [
        {
          slug: "gemini-cli-demo",
          title: "Gemini CLI & MCP <Demo>",
          youtube_video_id: "abcdefghijk",
          category: "tutorial",
          kind: "long",
          source_guide: "gemini-cli-guide",
          source_guide_kind: "life",
          published_at: "2026-11-18T12:00:00Z",
        },
      ],
    });

    const response = await GET();
    const body = await response.text();
    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("application/xml; charset=utf-8");
    expect(body).toContain('xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"');
    expect(body).toContain(`<loc>${siteUrl}/zh-TW/videos/gemini-cli-demo</loc>`);
    expect(body).toContain("<video:thumbnail_loc>https://i.ytimg.com/vi/abcdefghijk/hqdefault.jpg</video:thumbnail_loc>");
    expect(body).toContain("<video:title>Gemini CLI &amp; MCP &lt;Demo&gt;</video:title>");
    expect(body).toContain("<video:player_loc>https://www.youtube-nocookie.com/embed/abcdefghijk</video:player_loc>");
    expect(body).toContain("<video:publication_date>2026-11-18T12:00:00.000Z</video:publication_date>");
    expect(body).toContain("<video:family_friendly>yes</video:family_friendly>");
  });

  it("answers 503 with Retry-After when the video API is unreachable", async () => {
    mocks.getAllPublishedVideos.mockResolvedValue({ available: false, videos: [] });
    const response = await GET();
    expect(response.status).toBe(503);
    expect(response.headers.get("Retry-After")).toBe("600");
  });
});
