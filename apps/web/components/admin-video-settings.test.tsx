import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoModelSettings } from "./admin-video-model-settings";
import { AdminVideoSettings, dramaBody, linesToList, mediaChoice, normalizeDrama, settingsBody, sharedBody, STAGES, tutorialBody } from "./admin-video-settings";
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
  auto_approve_audio: true,
  stage_instructions: { writer: "結尾留懸念" },
  channel_stance: "", auto_pick_outline: true, auto_approve_final: true,
  drama: {
    drama_enabled: false, image_provider: "gemini", image_model: "gemini-3-pro-image", clip_provider: "gemini", clip_model: "gemini-omni-1.1-flash",
    music_provider: "gemini", music_model: "lyria-3.5", clip_resolution: "1080p", clip_seconds_default: 8, clip_native_audio: false, drama_aspect: "16:9",
    max_clips_per_video: 40, max_retakes_per_shot: 2, monthly_clip_seconds_budget: 3000, monthly_images_budget: 1500, monthly_judge_calls_budget: 3000,
    monthly_music_budget: 60, max_usd_per_video: 200, judge_min_score: 7, auto_approve_storyboard: false, auto_pick_look: false, character_voice_pool: [], music_enabled: true,
    subtitle_burn_in: true, style_preset: "cinematic-3d", drama_topic_scope: ["山海經", "民間傳說"],
    series_max_in_flight: 1, series_script_gate: true, series_auto_continue: true, series_chapter_ahead: 2, series_doc_rewrites: 2, series_episodes_per_month: 30,
    drama_stage_models: null, drama_stage_instructions: { writer: "每集結尾一個懸念" }, drama_voice: null, drama_caption_locales: [],
    drama_auto_approve_audio: true, drama_auto_approve_final: true, drama_max_verify_rounds: 3, drama_max_retake_rounds: 2,
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

const prompts = [
  { stage: "planner", format: "drama", variant: "setting", slug: "jingwei", instructions: "You are the planner.\n\n## The owner's standing instructions\n每集結尾留下一集的懸念", sent_at: "2026-09-26T15:00:00Z" },
  { stage: "writer", format: "slides", variant: "", slug: "ai-model-choice", instructions: "You are the writer.", sent_at: "2026-09-26T16:00:00Z" },
];

/** A merge the way the API answers a partial save: the sent fields over the stored ones, drama field by field. */
function merged(body: Record<string, unknown>) {
  const { drama, ...rest } = body as { drama?: Record<string, unknown> };
  return { ...view, ...rest, drama: { ...view.drama, ...(drama ?? {}) }, updated_at: "2026-09-27T08:00:00Z" };
}

function stubFetch() {
  const puts: unknown[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    if (String(input).endsWith("/api/travel/admin/video-automation/prompts")) return Promise.resolve(Response.json({ prompts }));
    expect(String(input)).toContain("/api/travel/admin/video-automation/settings");
    if (init?.method === "PUT") {
      const body = JSON.parse(String(init.body));
      puts.push(body);
      return Promise.resolve(Response.json(merged(body)));
    }
    return Promise.resolve(Response.json(view));
  }));
  return puts;
}

const settingsAt = (section: string) => window.history.replaceState(null, "", `/zh-TW/admin/videos?tab=settings&section=${section}`);
const manager = () => render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoSettings /></AdminOperationsProvider>);

beforeEach(() => window.history.replaceState(null, "", "/zh-TW/admin/videos?tab=settings"));
afterEach(() => vi.unstubAllGlobals());

describe("AdminVideoSettings", () => {
  it("builds each part's body from the whole, one topic per line, without the options or the other parts", () => {
    expect(linesToList(" AI \n\nAI 工具教學\r\n")).toEqual(["AI", "AI 工具教學"]);
    const body = settingsBody(view as never);
    expect(Object.keys(body)).not.toContain("model_options");
    expect(Object.keys(body)).not.toContain("updated_at");
    expect(Object.keys(body.stage_models)).toEqual([...STAGES]);
    const tutorial = tutorialBody(body, "AI\n工具");
    expect(tutorial.topic_scope).toEqual(["AI", "工具"]);
    expect(tutorial).not.toHaveProperty("stage_models");
    expect(tutorial).not.toHaveProperty("drama");
    expect(tutorial).not.toHaveProperty("channel_stance");
    expect(tutorial).not.toHaveProperty("topic_avoid");
    expect(Object.keys(sharedBody(body, "Stocks\n"))).toEqual(["channel_stance", "topic_avoid", "monthly_token_budget_millions"]);
    expect(Object.keys(dramaBody(body.drama, "山海經"))).toEqual(["drama"]);
    // An older site's drama object lacks the series and the split's fields; the defaults fill them.
    const older = normalizeDrama({ drama_enabled: true } as never);
    expect(older).toMatchObject({ drama_enabled: true, drama_stage_models: null, drama_voice: null, drama_stage_instructions: {}, drama_caption_locales: [], series_script_gate: true, drama_max_verify_rounds: 3 });
  });

  it("opens on the tutorial part, saves only its fields, and keeps the drama's and the shared ones out of the body", async () => {
    const puts = stubFetch();
    manager();
    const enabled = await screen.findByRole("checkbox", { name: "自動產生草稿" });
    expect(screen.getByRole("tab", { name: "教學影片", selected: true })).toBeTruthy();
    fireEvent.click(enabled);
    fireEvent.change(screen.getByRole("spinbutton", { name: "多久產生一次新草稿（小時）" }), { target: { value: "48" } });
    expect(screen.queryByRole("textbox", { name: "要避開的題材" })).toBeNull();
    expect(screen.queryByRole("textbox", { name: "頻道立場" })).toBeNull();
    expect(screen.queryByRole("checkbox", { name: "開啟 AI 漫劇" })).toBeNull();
    expect(screen.getAllByText(/Anthropic Claude API · Claude Opus 5\.5/, { selector: "dd" })).toHaveLength(3);
    expect(screen.getByRole("link", { name: "到 AI 設定修改" }).getAttribute("href")).toContain("/admin/ai-accounts?tab=models&section=video");
    const writer = screen.getByRole("textbox", { name: "撰稿的常設指示" });
    expect(writer).toHaveProperty("value", "結尾留懸念");
    fireEvent.change(writer, { target: { value: "" } });
    fireEvent.click(screen.getByRole("checkbox", { name: "英文" }));
    // Only the slides prompts show here; the drama's are on the drama part.
    expect(screen.getByText(/撰稿 · ai-model-choice · /).tagName).toBe("SUMMARY");
    expect(screen.queryByText(/企劃（選題與大綱） · setting · jingwei/)).toBeNull();
    expect(screen.getByText(/產生 1 \/ 8 支草稿/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "儲存教學設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as Record<string, unknown>;
    expect(body).toMatchObject({ enabled: true, draft_interval_hours: 48, topic_scope: ["AI", "Tech"], stage_instructions: { writer: "" }, caption_locales: ["ja", "ko", "zh-CN"] });
    expect(Object.keys(body).sort()).toEqual([
      "auto_approve_audio", "auto_approve_final", "auto_pick_outline", "caption_locales", "draft_interval_hours", "enabled", "max_drafts_per_month",
      "max_retake_rounds", "max_verify_rounds", "max_waiting_drafts", "stage_instructions", "target_minutes_max", "target_minutes_min", "topic_from_search",
      "topic_from_site", "topic_scope", "topics_per_run", "voice",
    ]);
    expect((await screen.findByRole("status")).textContent).toBe("已儲存");
    expect(vi.mocked(fetch).mock.calls.at(-1)?.[0]).toBe("/api/travel/admin/video-automation/settings");
  });

  it("saves the shared part on its own: the stance, the topics to avoid and the token budget", async () => {
    const puts = stubFetch();
    manager();
    fireEvent.click(await screen.findByRole("tab", { name: "共用" }));
    const stance = await screen.findByRole("textbox", { name: "頻道立場" });
    expect(stance).toHaveProperty("value", "");
    fireEvent.change(stance, { target: { value: "1. 先把帳算清楚再花錢" } });
    fireEvent.change(screen.getByRole("textbox", { name: "要避開的題材" }), { target: { value: "Stocks\n  Elections  \n" } });
    fireEvent.change(screen.getByRole("spinbutton", { name: "每月模型 token 上限（百萬）" }), { target: { value: "30" } });
    expect(screen.getByText(/API 已用 1,500 \/ 20,000,000 個 token/)).toBeTruthy();
    expect(screen.getByText(/呼叫模型 3 次（其中 1 次失敗）/)).toBeTruthy();
    expect(screen.queryByRole("checkbox", { name: "自動產生草稿" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "儲存共用設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0]).toEqual({ channel_stance: "1. 先把帳算清楚再花錢", topic_avoid: ["Stocks", "Elections"], monthly_token_budget_millions: 30 });
    expect((await screen.findByRole("status")).textContent).toBe("已儲存");
  });

  it("deep-links to the drama part, follows the clip model's resolutions and lengths, and saves the drama object alone", async () => {
    settingsAt("drama");
    const puts = stubFetch();
    manager();
    fireEvent.click(await screen.findByRole("checkbox", { name: "開啟 AI 漫劇" }));
    expect(screen.getByRole("tab", { name: "漫劇", selected: true })).toBeTruthy();
    expect(screen.queryByRole("checkbox", { name: "自動產生草稿" })).toBeNull();
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
    fireEvent.change(screen.getByRole("spinbutton", { name: "同時最多幾集在做（1–2）" }), { target: { value: "2" } });
    fireEvent.click(screen.getByRole("checkbox", { name: /劇本先給我看/ }));
    fireEvent.click(screen.getByRole("checkbox", { name: /設定圖自動選/ }));
    // The drama's prompts, with the series document's variant, and only those.
    expect(screen.getByText(/企劃（選題與大綱） · setting · jingwei · /).tagName).toBe("SUMMARY");
    expect(screen.queryByText(/撰稿 · ai-model-choice/)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "儲存漫劇設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as { drama: Record<string, unknown> };
    expect(Object.keys(body)).toEqual(["drama"]);
    expect(body.drama).toMatchObject({
      drama_enabled: true, clip_provider: "minimax", clip_model: "MiniMax-H3", clip_resolution: "768p", clip_seconds_default: 8, max_usd_per_video: 120,
      drama_topic_scope: ["山海經", "原創玄幻"], series_max_in_flight: 2, series_script_gate: false, auto_pick_look: true, drama_stage_models: null, drama_voice: null,
    });
    expect(body.drama.character_voice_pool).toEqual([{ provider: "gemini", name: "Kore" }]);
    expect(mediaChoice(view.media_options as never, "clips", "minimax", "MiniMax-H3")?.usd_per_second).toBe(0.13);
    expect(mediaChoice(view.media_options as never, "clips", "gemini", "nope")).toBeNull();
    expect((await screen.findByRole("status")).textContent).toBe("已儲存");
  });

  it("gives the drama its own narrator voice, standing instructions and language defaults, or follows the tutorial's", async () => {
    settingsAt("drama");
    const puts = stubFetch();
    manager();
    const follows = await screen.findByRole("checkbox", { name: "旁白聲音跟教學一樣（頻道聲音）" });
    expect(follows).toHaveProperty("checked", true);
    expect(screen.queryByRole("combobox", { name: "聲音" })).toBeNull();
    fireEvent.click(follows);
    // The drama's voice starts from the channel voice, then differs.
    const name = screen.getByRole("combobox", { name: "聲音" }) as HTMLSelectElement;
    expect(name.value).toBe("Sulafat");
    fireEvent.change(name, { target: { value: "Kore" } });
    const writer = screen.getByRole("textbox", { name: "撰稿的常設指示" });
    expect(writer).toHaveProperty("value", "每集結尾一個懸念");
    fireEvent.change(screen.getByRole("textbox", { name: "查核的常設指示" }), { target: { value: "對照設定集" } });
    fireEvent.click(screen.getByRole("checkbox", { name: "日文" }));
    fireEvent.click(screen.getByRole("checkbox", { name: "旁白由 Jev 判斷每一句都唸對時，自動核准" }));
    expect(screen.getByText(/漫劇的各階段跟教學影片用同樣的模型/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "儲存漫劇設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as { drama: Record<string, unknown> };
    expect(body.drama).toMatchObject({
      drama_voice: { provider: "gemini", name: "Kore", style: "Relaxed", model: null, rate: "+0%" },
      drama_stage_instructions: { writer: "每集結尾一個懸念", verifier: "對照設定集" },
      drama_caption_locales: ["ja"], drama_auto_approve_audio: false, drama_auto_approve_final: true,
    });
    expect(body).not.toHaveProperty("voice");
    expect(body).not.toHaveProperty("stage_instructions");
  });

  it("picks the tutorial's and the drama's stage models on the AI settings page, null when the drama follows", async () => {
    const puts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoModelSettings /></AdminOperationsProvider>);
    const writer = await screen.findByRole("group", { name: "撰稿" });
    fireEvent.change(writer.querySelectorAll("select")[1], { target: { value: "claude-opus-5-5" } });
    const follows = screen.getByRole("checkbox", { name: "各階段模型跟教學一樣" });
    expect(follows).toHaveProperty("checked", true);
    expect(screen.queryByRole("group", { name: "漫劇：撰稿" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "儲存影片模型" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0]).toEqual({ stage_models: { ...view.stage_models, writer: opus }, drama_stage_models: null });
    expect(vi.mocked(fetch).mock.calls.at(-1)?.[0]).toBe("/api/travel/admin/video-automation/settings/models");

    fireEvent.click(follows);
    const dramaWriter = screen.getByRole("group", { name: "漫劇：撰稿" });
    fireEvent.change(within(dramaWriter).getAllByRole("combobox")[0], { target: { value: "claude_code" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存影片模型" }));
    await waitFor(() => expect(puts).toHaveLength(2));
    const second = puts[1] as { drama_stage_models: Record<string, unknown> };
    // The drama's choices start as a copy of the tutorial's (the writer was just set to Opus there).
    expect(second.drama_stage_models.writer).toEqual({ provider: "claude_code", model: "claude-opus-5-5" });
    expect(second.drama_stage_models.planner).toEqual(sonnet);
  });

  it("shows a vendor without a key and keeps a reader from saving on every part", async () => {
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoSettings /><AdminVideoModelSettings /></AdminOperationsProvider>);
    expect(await screen.findByText(/要有「管理設定」權限才能修改/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "儲存教學設定" })).toHaveProperty("disabled", true);
    expect(await screen.findByRole("button", { name: "儲存影片模型" })).toHaveProperty("disabled", true);
    expect(screen.getAllByRole("option", { name: "OpenAI API (沒有金鑰)" }).length).toBe(STAGES.length);
    expect(screen.getAllByRole("option", { name: "Claude Code (訂閱帳號) (主機代理未設定)" }).length).toBe(STAGES.length);
    fireEvent.click(screen.getByRole("tab", { name: "共用" }));
    expect(await screen.findByRole("button", { name: "儲存共用設定" })).toHaveProperty("disabled", true);
    expect(screen.getByText(/用滿才換下一個，最後一個用滿再回到 A/)).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: "漫劇" }));
    expect(await screen.findByRole("button", { name: "儲存漫劇設定" })).toHaveProperty("disabled", true);
  });
});
