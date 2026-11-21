// @vitest-environment node
import { beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  getGuideTopicList: vi.fn(),
  loadSubsetFont: vi.fn(),
}));

vi.mock("@/lib/guides.server", () => ({
  getGuideTopicList: mocks.getGuideTopicList,
}));
vi.mock("next-intl/server", () => ({
  getTranslations: async ({ namespace }: { namespace: string }) => (key: string, values?: Record<string, string>) => {
    if (namespace === "metadata" && key === "topicHubTitle") return `${values?.topic ?? ""} Guides | Mokaair`;
    if (namespace === "metadata" && key === "topicHubDescription") return `Guides on ${values?.topic ?? ""}.`;
    if (namespace === "common" && key === "guides.lifeHubTitle") return "Life & Tech";
    return key;
  },
}));
vi.mock("@/lib/article-og", async (original) => ({
  ...await original<typeof import("@/lib/article-og")>(),
  loadSubsetFont: mocks.loadSubsetFont,
}));

beforeEach(() => {
  mocks.getGuideTopicList.mockReset();
  mocks.loadSubsetFont.mockReset().mockResolvedValue(null);
});

describe("/og/[locale]/topics/[section]/[topic]/card.png", () => {
  it("renders a PNG card for a published topic hub", async () => {
    mocks.getGuideTopicList.mockResolvedValue({
      available: true,
      topics: [{ slug: "claude-code", label: "Claude Code", description: "CLI coding workflows.", count: 12 }],
    });

    const response = await GET(new Request("https://mokaair.com/og/en/topics/life/claude-code/card.png"), {
      params: Promise.resolve({ locale: "en", section: "life", topic: "claude-code" }),
    });

    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toContain("image/png");
    const bytes = new Uint8Array(await response.arrayBuffer());
    expect(bytes.slice(0, 4)).toEqual(new Uint8Array([0x89, 0x50, 0x4e, 0x47]));
  });

  it("returns 404 for unknown sections, empty topics, or unknown slugs", async () => {
    mocks.getGuideTopicList.mockResolvedValue({
      available: true,
      topics: [{ slug: "empty-topic", label: "Empty", count: 0 }],
    });

    const empty = await GET(new Request("https://mokaair.com/og/en/topics/life/empty-topic/card.png"), {
      params: Promise.resolve({ locale: "en", section: "life", topic: "empty-topic" }),
    });
    expect(empty.status).toBe(404);

    const badSection = await GET(new Request("https://mokaair.com/og/en/topics/invalid/ai/card.png"), {
      params: Promise.resolve({ locale: "en", section: "invalid", topic: "ai" }),
    });
    expect(badSection.status).toBe(404);
  });
});
