import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoModelSettings } from "./admin-video-model-settings";
import { AdminVideoSettings, linesToList, mediaChoice, saveBody, settingsBody, STAGES } from "./admin-video-settings";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const sonnet = { provider: "anthropic", model: "claude-sonnet-5" };
const opus = { provider: "anthropic", model: "claude-opus-5-5" };
const view = {
  enabled: false, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3,
  topic_scope: ["AI", "Tech"], topic_avoid: ["Stocks"], topic_from_site: true, topic_from_search: true,
  stage_models: { planner: sonnet, writer: sonnet, verifier: opus, listener: opus, translator: sonnet, caption_reviewer: opus },
  voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" },
  target_minutes_min: 8, target_minutes_max: 12, caption_locales: ["en", "ja", "ko", "zh-CN"],
  max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2,
  subscription_max_usage_percent: 80, auto_approve_audio: true,
  drama: {
    drama_enabled: false, image_provider: "gemini", image_model: "gemini-3-pro-image", clip_provider: "gemini", clip_model: "gemini-omni-1.1-flash",
    music_provider: "gemini", music_model: "lyria-3.5", clip_resolution: "1080p", clip_seconds_default: 8, clip_native_audio: false, drama_aspect: "16:9",
    max_clips_per_video: 40, max_retakes_per_shot: 2, monthly_clip_seconds_budget: 3000, monthly_images_budget: 1500, monthly_judge_calls_budget: 3000,
    monthly_music_budget: 60, max_usd_per_video: 200, judge_min_score: 7, auto_approve_storyboard: false, character_voice_pool: [], music_enabled: true,
    subtitle_burn_in: true, style_preset: "cinematic-3d", drama_topic_scope: ["山海經", "民間傳說"],
  },
  media_options: {
    images: { gemini: [{ value: "gemini-3-pro-image", label: "Gemini 3 Pro Image", description: null, status: "stable", resolutions: [], durations: [], reference_images: 14, native_audio: false, usd_per_second: null, usd_per_image: 0.134, usd_per_track: null }], minimax: [] },
    clips: {
      gemini: [{ value: "gemini-omni-1.1-flash", label: "Gemini Omni 1.1 Flash", description: null, status: "stable", resolutions: ["720p", "1080p"], durations: [4, 5, 6, 7, 8, 9, 10], reference_images: 3, native_audio: true, usd_per_second: 0.15, usd_per_image: null, usd_per_track: null }],
      minimax: [{ value: "MiniMax-H3", label: "MiniMax H3", description: null, status: "stable", resolutions: ["768p", "2k"], durations: [4, 6, 8, 10], reference_images: 9, native_audio: false, usd_per_second: 0.13, usd_per_image: null, usd_per_track: null }],
    },
    music: { gemini: [{ value: "lyria-3.5", label: "Lyria 3.5", description: null, status: "stable", resolutions: [], durations: [], reference_images: 0, native_audio: false, usd_per_second: null, usd_per_image: null, usd_per_track: 0.08 }], minimax: [] },
  },
  style_presets: ["cinematic-3d", "anime-2d", "ink-wash", "custom"],
  model_options: {
    claude_code: [{ value: "claude-opus-5-5", label: "Claude Opus 5.5", description: null, status: "stable" }, { value: "claude-sonnet-5", label: "Claude Sonnet 5", description: null, status: "stable" }],
    anthropic: [{ value: "claude-opus-5-5", label: "Claude Opus 5.5", description: null, status: "stable" }, { value: "claude-sonnet-5", label: "Claude Sonnet 5", description: null, status: "stable" }],
    openai: [], minimax: [],
    gemini: [{ value: "gemini-3.8-flash", label: "Gemini 3.8 Flash", description: null, status: "stable" }],
  },
  configured_providers: ["anthropic", "gemini"],
  voice_options: { gemini: ["Sulafat", "Kore"], gemini_models: ["gemini-3.8-flash-tts"], azure: [] },
  usage: { tokens: 1500, token_budget: 20_000_000, drafts: 1, draft_budget: 8, calls: 3, failed_calls: 1 },
  updated_at: "2026-09-25T08:00:00Z",
};

function stubFetch() {
  const puts: unknown[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    expect(String(input)).toContain("/api/travel/admin/video-automation/settings");
    if (init?.method === "PUT") {
      const body = JSON.parse(String(init.body));
      puts.push(body);
      return Promise.resolve(Response.json({ ...view, ...body }));
    }
    return Promise.resolve(Response.json(view));
  }));
  return puts;
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminVideoSettings", () => {
  it("keeps one topic per line and sends only what the API stores", () => {
    expect(linesToList(" AI \n\nAI 工具教學\r\n")).toEqual(["AI", "AI 工具教學"]);
    const body = settingsBody(view as never);
    expect(Object.keys(body)).not.toContain("model_options");
    expect(Object.keys(body)).not.toContain("updated_at");
    expect(Object.keys(body.stage_models)).toEqual([...STAGES]);
    expect(saveBody(body, "AI", "")).not.toHaveProperty("stage_models");
  });

  it("lets a settings manager turn drafts on and save without touching the stage models", async () => {
    const puts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoSettings /></AdminOperationsProvider>);
    const enabled = await screen.findByRole("checkbox", { name: "自動產生草稿" });
    fireEvent.click(enabled);
    fireEvent.change(screen.getByRole("spinbutton", { name: "多久產生一次新草稿（小時）" }), { target: { value: "48" } });
    expect(screen.queryByRole("group", { name: "撰稿" })).toBeNull();
    expect(screen.getAllByText(/Anthropic Claude API · Claude Opus 5\.5/, { selector: "dd" })).toHaveLength(3);
    expect(screen.getByRole("link", { name: "到 AI 設定修改" }).getAttribute("href")).toContain("/admin/ai-accounts?tab=models&section=video");
    fireEvent.change(screen.getByRole("textbox", { name: "要避開的題材" }), { target: { value: "Stocks\n  Elections  \n" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as Record<string, unknown>;
    expect(body).toMatchObject({ enabled: true, draft_interval_hours: 48, topic_avoid: ["Stocks", "Elections"] });
    expect(body).not.toHaveProperty("stage_models");
    expect(body).not.toHaveProperty("model_options");
    expect((await screen.findByRole("status")).textContent).toBe("已儲存");
  });

  it("picks a stage model on the AI settings page and saves only the models", async () => {
    const puts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoModelSettings /></AdminOperationsProvider>);
    const writer = await screen.findByRole("group", { name: "撰稿" });
    fireEvent.change(writer.querySelectorAll("select")[1], { target: { value: "claude-opus-5-5" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存影片模型" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as { stage_models: Record<string, unknown> };
    expect(Object.keys(body)).toEqual(["stage_models"]);
    expect(body.stage_models.writer).toEqual(opus);
    expect(vi.mocked(fetch).mock.calls.at(-1)?.[0]).toBe("/api/travel/admin/video-automation/settings/models");
  });

  it("turns the drama route on, follows the clip model's resolutions and lengths, and saves the drama block", async () => {
    const puts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoSettings /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("checkbox", { name: "開啟 AI 漫劇" }));
    const resolution = screen.getByRole("combobox", { name: "片段解析度" }) as HTMLSelectElement;
    expect([...resolution.options].map((option) => option.value)).toEqual(["720p", "1080p"]);
    expect(screen.getAllByRole("option", { name: /MiniMax API \(沒有金鑰\)/ })).toHaveLength(3);
    fireEvent.change(screen.getByRole("combobox", { name: "片段廠商（圖生影片）" }), { target: { value: "minimax" } });
    expect((screen.getByRole("combobox", { name: "片段模型" }) as HTMLSelectElement).value).toBe("MiniMax-H3");
    expect([...(screen.getByRole("combobox", { name: "片段解析度" }) as HTMLSelectElement).options].map((option) => option.value)).toEqual(["768p", "2k"]);
    expect((screen.getByRole("combobox", { name: "片段預設秒數" }) as HTMLSelectElement).value).toBe("8");
    fireEvent.click(screen.getByRole("checkbox", { name: "Kore" }));
    fireEvent.change(screen.getByRole("spinbutton", { name: "單支最多花費（美元）" }), { target: { value: "120" } });
    fireEvent.change(screen.getByRole("textbox", { name: "漫劇題材（每行一個）" }), { target: { value: "山海經\n原創玄幻\n" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as { drama: Record<string, unknown> };
    expect(body.drama).toMatchObject({ drama_enabled: true, clip_provider: "minimax", clip_model: "MiniMax-H3", clip_resolution: "768p", clip_seconds_default: 8, max_usd_per_video: 120, drama_topic_scope: ["山海經", "原創玄幻"] });
    expect(body.drama.character_voice_pool).toEqual([{ provider: "gemini", name: "Kore" }]);
    expect(mediaChoice(view.media_options as never, "clips", "minimax", "MiniMax-H3")?.usd_per_second).toBe(0.13);
    expect(mediaChoice(view.media_options as never, "clips", "gemini", "nope")).toBeNull();
  });

  it("shows a vendor without a key and keeps a reader from saving", async () => {
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoSettings /><AdminVideoModelSettings /></AdminOperationsProvider>);
    expect(await screen.findByText(/要有「管理設定」權限才能修改/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "儲存設定" })).toHaveProperty("disabled", true);
    expect(await screen.findByRole("button", { name: "儲存影片模型" })).toHaveProperty("disabled", true);
    expect(screen.getAllByRole("option", { name: "OpenAI API (沒有金鑰)" }).length).toBe(STAGES.length);
    expect(screen.getAllByRole("option", { name: "Claude Code (訂閱帳號) (主機代理未設定)" }).length).toBe(STAGES.length);
    expect(screen.getByText(/1 \/ 8 支草稿，呼叫模型 3 次（其中 1 次失敗）/)).toBeTruthy();
    expect(screen.getByRole("spinbutton", { name: /訂閱帳號用到幾 %/ })).toHaveProperty("value", "80");
  });
});
