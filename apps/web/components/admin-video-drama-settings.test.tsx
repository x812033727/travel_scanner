import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoDramaSettings, missingMediaKeys } from "./admin-video-drama-settings";
import { mediaChoice, type VideoSettingsView } from "./admin-video-settings";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[], roles: string[] = []): AdminBootstrap {
  return { admin_roles: roles, admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const sonnet = { provider: "anthropic", model: "claude-sonnet-5" };
const opus = { provider: "anthropic", model: "claude-opus-5-5" };
const view = {
  enabled: false, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3,
  topic_scope: ["AI", "Tech"], topic_avoid: ["Stocks"], topic_from_site: true, topic_from_search: true,
  stage_models: { planner: sonnet, writer: sonnet, verifier: opus, listener: opus, translator: sonnet, caption_reviewer: opus },
  voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" },
  target_minutes_min: 8, target_minutes_max: 12, caption_locales: ["en", "ja", "ko"],
  max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2,
  auto_approve_audio: true, stage_instructions: {}, channel_stance: "", auto_pick_outline: true, auto_approve_final: true,
  drama: {
    drama_enabled: false, image_provider: "gemini", image_model: "gemini-3-pro-image", clip_provider: "gemini", clip_model: "gemini-omni-1.1-flash",
    music_provider: "gemini", music_model: "lyria-3.5", clip_resolution: "1080p", clip_seconds_default: 8, clip_native_audio: false, drama_aspect: "16:9",
    max_clips_per_video: 40, max_retakes_per_shot: 2, monthly_clip_seconds_budget: 3000, monthly_images_budget: 1500, monthly_judge_calls_budget: 3000,
    monthly_music_budget: 60, max_usd_per_video: 200, judge_min_score: 7, auto_approve_storyboard: false, auto_pick_look: false, character_voice_pool: [], music_enabled: true,
    subtitle_burn_in: true, style_preset: "cinematic-3d", drama_topic_scope: ["山海經", "民間傳說"],
    // Fields the tab does not edit: they must go back exactly as they came.
    series_max_in_flight: 1, series_script_gate: true, series_auto_continue: true, series_chapter_ahead: 2, series_doc_rewrites: 2, series_episodes_per_month: 30,
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
  model_options: { claude_code: [], anthropic: [], openai: [], minimax: [], gemini: [] },
  configured_providers: ["anthropic", "gemini"],
  voice_options: { gemini: ["Sulafat", "Kore"], gemini_models: ["gemini-3.8-flash-tts"], azure: [] },
  usage: null,
  updated_at: "2026-09-25T08:00:00Z",
} as unknown as VideoSettingsView;

// What the API holds when the drama tab saves: someone changed the draft interval meanwhile.
const stored = { ...view, draft_interval_hours: 48 };

/** The API as the tab sees it: a partial save lands over the stored settings, the drama block field by field. */
function stubFetch() {
  const puts: Array<Record<string, unknown>> = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    if (String(input).endsWith("/api/travel/admin/video-automation/prompts")) return Promise.resolve(Response.json({ prompts: [] }));
    expect(String(input)).toBe("/api/travel/admin/video-automation/settings");
    if (init?.method === "PUT") {
      const body = JSON.parse(String(init.body)) as { drama?: Record<string, unknown> };
      puts.push(body);
      return Promise.resolve(Response.json({ ...stored, ...body, drama: { ...stored.drama, ...(body.drama ?? {}) }, updated_at: "2026-09-27T09:00:00Z" }));
    }
    return Promise.resolve(Response.json(stored));
  }));
  return puts;
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminVideoDramaSettings", () => {
  it("names the media vendors a turned-on route still needs a key for", () => {
    expect(missingMediaKeys({ image_provider: "gemini", clip_provider: "minimax", music_provider: "gemini" }, ["gemini"])).toEqual(["minimax"]);
    expect(missingMediaKeys({ image_provider: "gemini", clip_provider: "gemini", music_provider: "gemini" }, ["gemini", "anthropic"])).toEqual([]);
    expect(missingMediaKeys({ image_provider: "minimax", clip_provider: "minimax", music_provider: "gemini" }, [])).toEqual(["gemini", "minimax"]);
    expect(mediaChoice(view.media_options, "clips", "minimax", "MiniMax-H3")?.usd_per_second).toBe(0.13);
    expect(mediaChoice(view.media_options, "clips", "gemini", "nope")).toBeNull();
  });

  it("turns the route on, follows the clip model, warns about a vendor without a key and saves only the drama block", async () => {
    const puts = stubFetch();
    const saved: VideoSettingsView[] = [];
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoDramaSettings view={view} onSaved={(next) => saved.push(next)} /></AdminOperationsProvider>);
    // The route is off, so the section opens with its switch in view.
    expect((screen.getByText("漫劇設定").closest("details") as HTMLDetailsElement).open).toBe(true);
    fireEvent.click(screen.getByRole("checkbox", { name: "開啟 AI 漫劇" }));
    // Every chosen vendor is Gemini, which has a key: nothing to warn about yet.
    expect(screen.queryByRole("alert")).toBeNull();
    const resolution = screen.getByRole("combobox", { name: "片段解析度" }) as HTMLSelectElement;
    expect([...resolution.options].map((option) => option.value)).toEqual(["720p", "1080p"]);
    expect(screen.getAllByRole("option", { name: /MiniMax API \(沒有金鑰\)/ })).toHaveLength(3);
    fireEvent.change(screen.getByRole("combobox", { name: "片段廠商（圖生影片）" }), { target: { value: "minimax" } });
    expect((screen.getByRole("combobox", { name: "片段模型" }) as HTMLSelectElement).value).toBe("MiniMax-H3");
    expect([...(screen.getByRole("combobox", { name: "片段解析度" }) as HTMLSelectElement).options].map((option) => option.value)).toEqual(["768p", "2k"]);
    expect((screen.getByRole("combobox", { name: "片段預設秒數" }) as HTMLSelectElement).value).toBe("8");
    expect(screen.getByRole("alert").textContent).toContain("網站還沒有 MiniMax API 的金鑰");
    expect(screen.getByRole("link", { name: "到 AI 設定填金鑰" }).getAttribute("href")).toContain("/admin/ai-accounts?tab=api&provider=ai_vendors");
    fireEvent.click(screen.getByRole("checkbox", { name: "Kore" }));
    fireEvent.click(screen.getByRole("checkbox", { name: /設定圖自動選/ }));
    fireEvent.change(screen.getByRole("spinbutton", { name: "單支最多花費（美元）" }), { target: { value: "120" } });
    fireEvent.change(screen.getByRole("textbox", { name: "漫劇題材（每行一個）" }), { target: { value: "山海經\n原創玄幻\n" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存漫劇設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0];
    expect(body.drama).toMatchObject({
      drama_enabled: true, clip_provider: "minimax", clip_model: "MiniMax-H3", clip_resolution: "768p", clip_seconds_default: 8,
      max_usd_per_video: 120, auto_pick_look: true, drama_topic_scope: ["山海經", "原創玄幻"],
      series_episodes_per_month: 30, series_script_gate: true,
    });
    expect((body.drama as { character_voice_pool: unknown }).character_voice_pool).toEqual([{ provider: "gemini", name: "Kore" }]);
    // The drama block alone: the API keeps everything else as it holds it now.
    expect(Object.keys(body)).toEqual(["drama"]);
    expect((await screen.findByRole("status")).textContent).toBe("已儲存");
    expect(saved.map((next) => next.updated_at)).toEqual(["2026-09-27T09:00:00Z"]);
  });

  it("lets the worker keep up to six episodes in the making and sends the limit back with the drama block", async () => {
    const puts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoDramaSettings view={view} onSaved={() => undefined} /></AdminOperationsProvider>);
    const inFlight = screen.getByRole("spinbutton", { name: "同時最多幾集在做（1–6）" }) as HTMLInputElement;
    expect(inFlight.value).toBe("1");
    expect(inFlight.getAttribute("min")).toBe("1");
    expect(inFlight.getAttribute("max")).toBe("6");
    fireEvent.change(inFlight, { target: { value: "6" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存漫劇設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0].drama).toMatchObject({ series_max_in_flight: 6, series_episodes_per_month: 30, drama_enabled: false });
  });

  it("tells a content reviewer why the drama settings are read-only", () => {
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"], ["content"])}><AdminVideoDramaSettings view={view} onSaved={() => undefined} /></AdminOperationsProvider>);
    expect(screen.getByText("你目前登入的帳號，後台角色是：內容。")).toBeTruthy();
    expect(screen.getByRole("checkbox", { name: "開啟 AI 漫劇" })).toHaveProperty("disabled", true);
    expect(screen.getByRole("button", { name: "儲存漫劇設定" })).toHaveProperty("disabled", true);
  });
});
