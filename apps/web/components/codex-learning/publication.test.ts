import { beforeEach, describe, expect, it, vi } from "vitest";
import { learningEntries } from "@/lib/codex-learning";
import { getLearningPublication } from "@/lib/codex-learning/server";

const mocks = vi.hoisted(() => ({ series: vi.fn() }));
vi.mock("@/lib/guides.server", () => ({ getGuideSeries: mocks.series }));
beforeEach(() => vi.clearAllMocks());

describe("shared publication boundary", () => {
  it("uses the requested locale and only published API titles", async () => {
    const row = { slug: "codex-beginner-guide", kind: "life", title: "Live title", description: "Live description" };
    mocks.series.mockResolvedValue({ entries: [row] });
    const publication = await getLearningPublication("ja");
    expect(mocks.series).toHaveBeenCalledWith("codex", "ja");
    const entries = learningEntries("ja", publication.articles);
    expect(entries.filter(entry => entry.published)).toHaveLength(1);
    expect(entries[0].title).toBe("Live title");
    expect(entries[0].description).toBe("Live description");
  });
  it("renders no published links when the shared API is unavailable", async () => {
    mocks.series.mockResolvedValue(null);
    const publication = await getLearningPublication("ko");
    expect(publication).toEqual({ articles: [], available: false });
    expect(learningEntries("ko", publication.articles).every(entry => !entry.published)).toBe(true);
  });
});
