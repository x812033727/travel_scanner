import { describe, expect, it, vi } from "vitest";
import LifeTopicHubPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({ render: vi.fn(async () => null), metadata: vi.fn(async () => ({ title: "t" })) }));
vi.mock("@/components/guides/topic-hub-page", () => ({ renderTopicHub: mocks.render, topicHubMetadata: mocks.metadata }));

const params = Promise.resolve({ locale: "zh-TW" as const, topic: "ai-terms" });

describe("/life/topics/[topic]", () => {
  it("hands the lifestyle section and the topic to the shared screen", async () => {
    await LifeTopicHubPage({ params, searchParams: Promise.resolve({}) });
    expect(mocks.render).toHaveBeenCalledWith({ locale: "zh-TW", section: "life", topic: "ai-terms", cursor: undefined });
    await generateMetadata({ params, searchParams: Promise.resolve({ cursor: "abc" }) });
    expect(mocks.metadata).toHaveBeenCalledWith({ locale: "zh-TW", section: "life", topic: "ai-terms", cursor: "abc" });
  });
});
