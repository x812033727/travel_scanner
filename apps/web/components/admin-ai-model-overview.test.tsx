import { describe, expect, it } from "vitest";
import { overviewRows, type OverviewSources } from "./admin-ai-model-overview";
import type { VideoSettingsView } from "./admin-video-settings";
import type { NewsSettings } from "@/lib/admin-news";

// Echo the key and values so each assertion names the rule it checks.
const t = (key: string, values?: Record<string, string>) => values ? `${key}(${Object.values(values).join(",")})` : key;
const stage = (name: string) => name;

const card = (provider: string, config: Record<string, string | null>, field_options: Record<string, { value: string; label: string }[]> = {}) => ({ provider, config, field_options });
const providers = (vendors: Record<string, string | null> = {}) => ({
  providers: [
    card("ai_vendors", vendors),
    card("ai_planner", { ai_planner_mode: "auto", ai_planner_priority: "openai,minimax", openai_model: "gpt-6-sol", anthropic_model: "claude-sonnet-5", minimax_model: "MiniMax-M3", gemini_model: "gemini-3.8-flash" },
      { openai_model: [{ value: "gpt-6-sol", label: "GPT-6 Sol" }] }),
    card("ai_guide_search", { hotspot_guide_ai_default_provider: "anthropic", hotspot_guide_ai_anthropic_model: null, hotspot_guide_ai_openai_model: "gpt-6-luna" }),
    card("hotspot_intros", { hotspot_intro_ai_default_provider: "openai", hotspot_intro_ai_openai_model: null }),
    card("gemini_guides", { hotspot_guide_gemini_model: "gemini-3.8-flash" }),
  ],
});
const news = {
  writer_provider: "anthropic", writer_model: null, verifier_provider: "minimax", verifier_model: "MiniMax-M3",
  model_options: { anthropic: [{ value: "claude-opus-5-5", label: "Claude Opus 5.5", description: null, status: "stable" }] },
  default_models: { anthropic: "claude-opus-5-5", minimax: "MiniMax-M3" },
} as unknown as NewsSettings;
const video = {
  stage_models: { planner: { provider: "claude_code", model: "claude-sonnet-5" }, writer: { provider: "openai", model: "gpt-6-sol" }, verifier: { provider: "claude_code", model: "claude-opus-5-5" }, listener: { provider: "claude_code", model: "claude-opus-5-5" }, translator: { provider: "gemini", model: "gemini-3.8-flash" }, caption_reviewer: { provider: "claude_code", model: "claude-opus-5-5" } },
  model_options: { claude_code: [], anthropic: [], openai: [{ value: "gpt-6-sol", label: "GPT-6 Sol", description: null, status: "stable" }], gemini: [], minimax: [] },
} as unknown as VideoSettingsView;

const row = (sources: OverviewSources, key: string) => overviewRows(sources, t, stage).find((item) => item.key === key)!;

describe("overviewRows", () => {
  it("resolves every empty model to the one it inherits", () => {
    const sources = { providers: providers(), news };
    expect(row(sources, "planner")).toMatchObject({ vendor: "overview.plannerAuto", model: "OpenAI GPT-6 Sol → MiniMax MiniMax-M3" });
    expect(row(sources, "guideSearch")).toMatchObject({ vendor: "Anthropic Claude", model: "claude-sonnet-5", inherited: "overview.features.planner" });
    // Introductions inherit guide search first, the planner only when guide search is empty too.
    expect(row(sources, "intros")).toMatchObject({ model: "gpt-6-luna", inherited: "overview.features.guideSearch" });
    expect(row(sources, "news-writer")).toMatchObject({ model: "Claude Opus 5.5", inherited: "overview.features.guideSearch" });
    expect(row(sources, "news-verifier")).toMatchObject({ model: "MiniMax-M3", inherited: undefined });
  });

  it("marks the features that can only run on an API key", () => {
    const rows = overviewRows({ providers: providers(), news, video }, t, stage);
    const support = Object.fromEntries(rows.map((item) => [item.key, item.support]));
    expect(support).toMatchObject({ planner: "apiKeyOnly", geminiSearch: "geminiApiKeyOnly", guideSearch: "apiKeyOnly", "news-writer": "apiKeyOnly", "video-writer": "claudeCode" });
    expect(rows.filter((item) => item.connection === "subscription").map((item) => item.key)).toEqual(["video-planner", "video-verifier", "video-listener", "video-caption_reviewer"]);
    expect(rows.every((item) => item.key.startsWith("video-") || item.connection === "apiKey")).toBe(true);
  });

  it("shows Claude on the subscription once the site can and the owner switched it on", () => {
    const sources = { providers: providers({ anthropic_connection: "subscription" }), news };
    expect(row(sources, "guideSearch")).toMatchObject({ support: "claudeSubscription", connection: "subscriptionFallback" });
    expect(row(sources, "news-writer")).toMatchObject({ connection: "subscriptionFallback" });
    // Not Claude, so still the API key; the planner never takes the subscription.
    expect(row(sources, "intros")).toMatchObject({ support: "claudeSubscription", connection: "apiKey" });
    expect(row(sources, "planner")).toMatchObject({ support: "apiKeyOnly", connection: "apiKey" });
    expect(row({ providers: providers({ anthropic_connection: "api_key" }) }, "guideSearch").connection).toBe("apiKey");
  });

  it("keeps every row that runs on Gemini on the API key, whatever the feature allows", () => {
    const rows = overviewRows({ providers: providers(), news, video }, t, stage);
    const gemini = rows.filter((item) => item.support === "geminiApiKeyOnly").map((item) => item.key);
    expect(gemini).toEqual(["geminiSearch", "video-translator"]);
    expect(rows.filter((item) => item.support === "geminiApiKeyOnly").every((item) => item.connection === "apiKey")).toBe(true);
    const onGemini = providers({ anthropic_connection: "subscription" });
    onGemini.providers[3].config.hotspot_intro_ai_default_provider = "gemini";
    expect(row({ providers: onGemini }, "intros")).toMatchObject({ support: "geminiApiKeyOnly", connection: "apiKey" });
  });

  it("links every row to where it is changed and to its feature", () => {
    const rows = overviewRows({ providers: providers(), news, video }, t, stage);
    expect(row({ providers: providers() }, "planner").edit).toBe("/admin/ai-accounts?tab=models&provider=ai_planner&field=ai_planner_mode");
    expect(rows.find((item) => item.key === "news-writer")).toMatchObject({ edit: "#ai-models-news", open: "/admin/news?tab=settings" });
    expect(rows.find((item) => item.key === "video-writer")).toMatchObject({ edit: "#ai-models-video", open: "/admin/videos?tab=settings", model: "GPT-6 Sol", feature: "overview.features.video(writer)" });
    expect(rows.every((item) => item.open)).toBe(true);
  });

  it("leaves out what a reader cannot load and a planner that calls no AI", () => {
    expect(overviewRows({ news }, t, stage).map((item) => item.key)).toEqual(["news-writer", "news-verifier"]);
    const off = providers();
    off.providers[1].config.ai_planner_mode = "disabled";
    expect(row({ providers: off }, "planner")).toMatchObject({ vendor: "overview.plannerDisabled", connection: "none" });
  });
});
