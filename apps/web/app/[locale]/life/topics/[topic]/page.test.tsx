import { describe, expect, it, vi } from "vitest";
import LifeTopicHubPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({
  render: vi.fn(async () => null), metadata: vi.fn(async () => ({ title: "t" })),
  redirect: vi.fn((url: string) => { throw new Error(`NEXT_REDIRECT ${url}`); }),
}));
vi.mock("next/navigation", () => ({ permanentRedirect: mocks.redirect }));
vi.mock("@/components/guides/topic-hub-page", () => ({ renderTopicHub: mocks.render, topicHubMetadata: mocks.metadata }));

const params = Promise.resolve({ locale: "zh-TW" as const, topic: "ai-terms" });

describe("/life/topics/[topic]", () => {
  it("hands the lifestyle section and the topic to the shared screen", async () => {
    await LifeTopicHubPage({ params, searchParams: Promise.resolve({}) });
    expect(mocks.render).toHaveBeenCalledWith({ locale: "zh-TW", section: "life", topic: "ai-terms", cursor: undefined });
    await generateMetadata({ params, searchParams: Promise.resolve({ cursor: "abc" }) });
    expect(mocks.metadata).toHaveBeenCalledWith({ locale: "zh-TW", section: "life", topic: "ai-terms", cursor: "abc" });
  });

  it("sends the AI family to its own hub permanently, keeping the query", async () => {
    const ai = Promise.resolve({ locale: "en" as const, topic: "ai" });
    await expect(LifeTopicHubPage({ params: ai, searchParams: Promise.resolve({}) })).rejects.toThrow("NEXT_REDIRECT /en/ai");
    await expect(LifeTopicHubPage({ params: ai, searchParams: Promise.resolve({ sort: "curated", cursor: "c1" }) }))
      .rejects.toThrow("NEXT_REDIRECT /en/ai?sort=curated&cursor=c1");
    // Its sub-topics stay where they are.
    await LifeTopicHubPage({ params: Promise.resolve({ locale: "en" as const, topic: "ai-news" }), searchParams: Promise.resolve({}) });
    expect(mocks.redirect).toHaveBeenCalledTimes(2);
  });
});
