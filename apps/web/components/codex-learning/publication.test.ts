import { beforeEach, describe, expect, it, vi } from "vitest";
import { publishedSeriesLinks, lessons } from "@/lib/codex-learning";
import { getLearningPublication } from "@/lib/codex-learning/server";
import type { GuideSummary } from "@/lib/guides";

const mocks = vi.hoisted(() => ({ list: vi.fn() }));
vi.mock("@/lib/guides.server", () => ({ getGuideList: mocks.list }));
beforeEach(() => vi.clearAllMocks());
const row = { slug: lessons[0].slug, kind: "life" } as GuideSummary;
describe("publication-aware series links", () => {
  it("finds a tutorial beyond the first page", async () => {
    mocks.list.mockResolvedValueOnce({ articles: [], next_cursor: "second", available: true })
      .mockResolvedValueOnce({ articles: [row], next_cursor: null, available: true });
    expect(await getLearningPublication("en")).toEqual({ articles: [row], available: true });
    expect(mocks.list).toHaveBeenLastCalledWith("en", { kind: "life", cursor: "second" }, 50);
  });
  it("fails closed if a later page fails or a cursor loops", async () => {
    mocks.list.mockResolvedValueOnce({ articles: [row], next_cursor: "a", available: true })
      .mockResolvedValueOnce({ available: false });
    expect(await getLearningPublication("ja")).toEqual({ articles: [], available: false });
    mocks.list.mockResolvedValue({ articles: [], next_cursor: "a", available: true });
    expect(await getLearningPublication("ko")).toEqual({ articles: [], available: false });
  });
  it("keeps withdrawn inline text and external links, preserving published locale", () => {
    const blocks = publishedSeriesLinks([{ type: "rich_paragraph", spans: [
      { type: "link", text: "Read", url: `https://mokaair.com/en/life/${row.slug}` },
      { type: "link", text: "unpublished", url: "https://mokaair.com/en/life/codex-agents-md" },
      { type: "link", text: "source", url: "https://learn.chatgpt.com/docs/app" },
    ] }], "en", [row]);
    expect(blocks[0]).toMatchObject({ spans: [{ type: "link" }, { type: "text", text: "unpublished" }, { type: "link" }] });
  });
});
