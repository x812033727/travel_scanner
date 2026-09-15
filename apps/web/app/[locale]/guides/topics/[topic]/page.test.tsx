import { describe, expect, it, vi } from "vitest";
import TravelTopicHubPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({ render: vi.fn(async () => null), metadata: vi.fn(async () => ({ title: "t" })) }));
vi.mock("@/components/guides/topic-hub-page", () => ({ renderTopicHub: mocks.render, topicHubMetadata: mocks.metadata }));

const params = Promise.resolve({ locale: "zh-TW" as const, topic: "transport" });

describe("/guides/topics/[topic]", () => {
  it("hands the travel section and the topic to the shared screen", async () => {
    await TravelTopicHubPage({ params, searchParams: Promise.resolve({ cursor: "abc" }) });
    expect(mocks.render).toHaveBeenCalledWith({ locale: "zh-TW", section: "travel", topic: "transport", cursor: "abc" });
    await generateMetadata({ params, searchParams: Promise.resolve({}) });
    expect(mocks.metadata).toHaveBeenCalledWith({ locale: "zh-TW", section: "travel", topic: "transport", cursor: undefined });
  });
});
