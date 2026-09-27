import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoSeries } from "./admin-video-series";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const summary = {
  id: "5e1a2b3c-4d5e-4f60-8a7b-9c0d1e2f3a4b", slug: "wenjian", title: "問劍", premise: "兩個少年在正道與魔道之間。", aspects: ["world", "bonds"], tone: "dual-male-leads-subtext",
  style_preset: "cinematic-3d", target_minutes: 3, planned_episodes: 25, episodes_per_chapter: 10, chapters: 3, open_ended: true, status: "active", note: "旁白慢一點",
  requested_chapter: null, force_next: false, episodes_done: 1, episodes_started: 1, episodes_ready: 8, docs_pending: 1, media_usd: 41.2, clip_seconds: 300,
  created_at: "2026-09-27T00:00:00Z", updated_at: "2026-09-27T01:00:00Z",
};
const beats = (number: number) => ({ number, title: `第 ${number} 集`, logline: `L${number}`, hook: "鐘聲", conflict: "誰敲的", turn: "鐘自己響", cliffhanger: { type: "reveal", text: "鐘下有字" }, setups: ["m1"], payoffs: [], tension: [2, 3, 3, 4, 5] });
const docs = [
  { id: "d1", kind: "setting", chapter_number: 0, version: 2, body_md: "# 設定集\n世界。", body_json: { characters: [] }, status: "approved", note: null, decided_at: "2026-09-27T00:30:00Z", created_at: "2026-09-27T00:20:00Z" },
  { id: "d2", kind: "outline", chapter_number: 0, version: 1, body_md: "# 總綱", body_json: { chapters: [] }, status: "approved", note: null, decided_at: "2026-09-27T00:40:00Z", created_at: "2026-09-27T00:35:00Z" },
  { id: "d3", kind: "chapter", chapter_number: 2, version: 1, body_md: "# 第二篇", body_json: { chapter: 2, episodes: [beats(11), beats(12)] }, status: "review", note: null, decided_at: null, created_at: "2026-09-27T00:50:00Z" },
];
const episodes = [
  { number: 1, chapter_number: 1, title: "鐘", logline: "L1", beats: beats(1), status: "done", slug: "wenjian-e001", recap: "鐘響了", started_at: "2026-09-27T00:00:00Z", finished_at: "2026-09-27T00:50:00Z", video: { slug: "wenjian-e001", title: "問劍 第 1 集 鐘", format: "drama", stage: "done", checklist: [{ key: "brief", label: "企劃", done: true }], youtube_video_id: "abcdefg", last_synced_at: "2026-09-27T00:50:00Z", pending: 0, media_usd: 41.2, clip_seconds: 300 } },
  { number: 2, chapter_number: 1, title: "字", logline: "L2", beats: beats(2), status: "started", slug: "wenjian-e002", recap: null, started_at: "2026-09-27T00:55:00Z", finished_at: null, video: { slug: "wenjian-e002", title: "問劍 第 2 集 字", format: "drama", stage: "script approved", checklist: [{ key: "brief", label: "企劃", done: true }, { key: "script", label: "劇本核准", done: false }], youtube_video_id: null, last_synced_at: "2026-09-27T01:00:00Z", pending: 1, media_usd: 0, clip_seconds: 0 } },
  { number: 3, chapter_number: 1, title: "山", logline: "L3", beats: beats(3), status: "ready", slug: null, recap: null, started_at: null, finished_at: null, video: null },
];

// The video settings the drama tab reads once for its banner and its settings section. The media
// catalog is left empty: the drama settings form itself is covered in admin-video-drama-settings.test.tsx.
function videoSettings(dramaEnabled: boolean) {
  return {
    enabled: false, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3, topic_scope: ["AI"], topic_avoid: [], topic_from_site: true, topic_from_search: true,
    stage_models: {}, voice: { provider: "gemini", name: "Sulafat", style: null, model: null, rate: "+0%" }, target_minutes_min: 8, target_minutes_max: 12,
    caption_locales: ["en"], max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true,
    stage_instructions: {}, channel_stance: "", auto_pick_outline: true, auto_approve_final: true,
    drama: {
      drama_enabled: dramaEnabled, image_provider: "gemini", image_model: "gemini-3-pro-image", clip_provider: "gemini", clip_model: "gemini-omni-1.1-flash",
      music_provider: "gemini", music_model: "lyria-3.5", clip_resolution: "1080p", clip_seconds_default: 8, clip_native_audio: false, drama_aspect: "16:9",
      max_clips_per_video: 40, max_retakes_per_shot: 2, monthly_clip_seconds_budget: 3000, monthly_images_budget: 1500, monthly_judge_calls_budget: 3000,
      monthly_music_budget: 60, max_usd_per_video: 200, judge_min_score: 7, auto_approve_storyboard: false, auto_pick_look: false, character_voice_pool: [],
      music_enabled: true, subtitle_burn_in: true, style_preset: "cinematic-3d", drama_topic_scope: ["山海經"],
    },
    media_options: { images: {}, clips: {}, music: {} }, style_presets: ["cinematic-3d"], model_options: {}, configured_providers: ["gemini"],
    voice_options: { gemini: ["Kore"], gemini_models: [], azure: [] }, usage: null, updated_at: "2026-09-27T08:00:00Z",
  };
}

function stubFetch(options: { settings?: Record<string, unknown>; videos?: unknown[] } = {}) {
  const calls: Array<{ url: string; method: string; body?: unknown }> = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    calls.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    if (options.settings && url.endsWith("/admin/video-automation/settings")) {
      if (method === "PUT") return Promise.resolve(Response.json({ ...options.settings, ...JSON.parse(String(init?.body)), updated_at: "2026-09-27T09:00:00Z" }));
      return Promise.resolve(Response.json(options.settings));
    }
    if (options.videos && url.includes("/admin/videos?format=drama")) return Promise.resolve(Response.json(options.videos));
    if (url.endsWith("/admin/video-automation/series") && method === "POST") return Promise.resolve(Response.json({ ...summary, slug: "new-one", title: "新作", status: "setting", docs: [], episodes: [] }, { status: 201 }));
    if (url.endsWith("/admin/video-automation/series")) return Promise.resolve(Response.json({ series: [summary] }));
    if (url.includes("/admin/video-automation/series/new-one")) return Promise.resolve(Response.json({ ...summary, slug: "new-one", title: "新作", status: "setting", docs: [], episodes: [] }));
    if (url.includes("/admin/video-automation/series/wenjian")) return Promise.resolve(Response.json({ ...summary, docs, episodes }));
    if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests: [] }));
    return Promise.resolve(Response.json([]));
  }));
  return calls;
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("AdminVideoSeries", () => {
  it("lists the series with their progress and starts a new one from the form", async () => {
    const calls = stubFetch();
    const opened: string[] = [];
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={(slug) => opened.push(slug)} /></AdminOperationsProvider>);
    const card = await screen.findByRole("button", { name: /問劍/ });
    expect(card.textContent).toContain("製作中");
    expect(card.textContent).toContain("1 份等你核准");
    expect(card.textContent).toContain("1/25 集 · 3 篇");
    expect(card.textContent).toContain("US$41.20");

    fireEvent.click(screen.getByText("新的作品", { selector: "summary" }));
    const create = screen.getByRole("button", { name: "建立作品" });
    expect(create).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "作品名稱" }), { target: { value: "新作" } });
    fireEvent.change(screen.getByRole("textbox", { name: "代號（小寫英數與連字號）" }), { target: { value: "New One" } });
    fireEvent.change(screen.getByRole("textbox", { name: "故事前提" }), { target: { value: "  一把劍  " } });
    expect(create).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "代號（小寫英數與連字號）" }), { target: { value: "new-one" } });
    fireEvent.click(screen.getByRole("checkbox", { name: /敘事結構/ }));
    fireEvent.change(screen.getByRole("combobox", { name: "情感線" }), { target: { value: "no-romance" } });
    fireEvent.change(screen.getByRole("spinbutton", { name: "預計集數" }), { target: { value: "60" } });
    expect(create).toHaveProperty("disabled", false);
    fireEvent.click(create);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toContain("/admin/video-automation/series");
    expect(post?.body).toEqual({ slug: "new-one", title: "新作", premise: "一把劍", aspects: ["world", "bonds", "mood"], tone: "no-romance", style_preset: "cinematic-3d", target_minutes: 3, planned_episodes: 60, episodes_per_chapter: 10, open_ended: true });
    await waitFor(() => expect(window.location.search).toContain("series=new-one"));
  });

  it("opens a series: the chapter outline waiting for the owner, its beats table, and the episode table", async () => {
    const calls = stubFetch();
    const opened: string[] = [];
    window.history.replaceState(null, "", "/?tab=drama&series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={(slug) => opened.push(slug)} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /問劍/ });
    const docsRegion = screen.getByRole("region", { name: "文件" });
    expect(docsRegion.textContent).toContain("設定集");
    expect(docsRegion.textContent).toContain("第 2 版");
    expect(docsRegion.textContent).toContain("第 2 篇細綱");
    expect(docsRegion.textContent).toContain("等你決定");
    expect(screen.getAllByRole("row").some((row) => row.textContent?.includes("鐘聲") && row.textContent?.includes("鐘下有字") && row.textContent?.includes("2-3-3-4-5"))).toBe(true);

    const reject = screen.getByRole("button", { name: "退回" });
    expect(reject).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "備註" }), { target: { value: "第 12 集再緊一點" } });
    fireEvent.click(reject);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const decision = calls.find((call) => call.method === "POST");
    expect(decision?.url).toContain("/admin/video-automation/series/wenjian/docs/chapter/2/decision");
    expect(decision?.body).toEqual({ decision: "reject", note: "第 12 集再緊一點" });

    const table = screen.getByRole("region", { name: "集數" });
    expect(table.textContent).toContain("完成");
    expect(table.textContent).toContain("劇本核准");
    expect(table.textContent).toContain("1 項等你");
    expect(table.textContent).toContain("US$41.20");
    fireEvent.click(screen.getAllByRole("button", { name: "打開" })[1]);
    expect(opened).toEqual(["wenjian-e002"]);
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    fireEvent.click(screen.getByRole("button", { name: "跳過" }));
    await waitFor(() => expect(calls.some((call) => call.url.endsWith("/episodes/3/skip"))).toBe(true));
    confirm.mockRestore();
    fireEvent.click(screen.getByRole("button", { name: "先規劃下一篇" }));
    await waitFor(() => expect(calls.some((call) => call.url.endsWith("/actions/plan-next-chapter"))).toBe(true));
  });

  it("lets a reader look but not decide", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /問劍/ });
    expect(screen.queryByRole("button", { name: "核准" })).toBeNull();
    expect(screen.queryByRole("button", { name: "跳過" })).toBeNull();
    expect(screen.queryByText("新的作品")).toBeNull();
  });

  it("says the drama route is off, opens its settings first, and says it is on once saved", async () => {
    const calls = stubFetch({ settings: videoSettings(false) });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage", "settings.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    expect(await screen.findByText("漫劇目前是關閉的。")).toBeTruthy();
    expect(screen.getByText("工人不會製作任何漫劇，你發起的單集漫劇與作品會等到開啟後才開始。在下方「漫劇設定」勾選「開啟 AI 漫劇」，再按儲存。")).toBeTruthy();
    expect((screen.getByText("漫劇設定", { selector: "summary" }).closest("details") as HTMLDetailsElement).open).toBe(true);
    fireEvent.click(screen.getByRole("checkbox", { name: "開啟 AI 漫劇" }));
    fireEvent.click(screen.getByRole("button", { name: "儲存漫劇設定" }));
    expect(await screen.findByText("漫劇已開啟：工人會依序製作發起的單集漫劇與作品。")).toBeTruthy();
    expect(screen.queryByText("漫劇目前是關閉的。")).toBeNull();
    const put = calls.find((call) => call.method === "PUT");
    expect((put?.body as { drama: { drama_enabled: boolean } }).drama.drama_enabled).toBe(true);
  });

  it("keeps the drama settings closed once the route is on", async () => {
    stubFetch({ settings: videoSettings(true) });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    expect(await screen.findByText("漫劇已開啟：工人會依序製作發起的單集漫劇與作品。")).toBeTruthy();
    expect((screen.getByText("漫劇設定", { selector: "summary" }).closest("details") as HTMLDetailsElement).open).toBe(false);
  });

  it("lists the one-off episodes that wait for the owner first, and marks one that stopped", async () => {
    const oneOff = (slug: string, extra: Record<string, unknown> = {}) => ({
      slug, title: slug, format: "drama", stage: "clips", checklist: [{ key: "brief", label: "企劃", done: true }], youtube_video_id: null,
      last_synced_at: "2026-09-27T01:00:00Z", pending: 0, media_usd: 0, clip_seconds: 0, ...extra,
    });
    stubFetch({ videos: [oneOff("quiet-one"), oneOff("waiting-one", { pending: 1 }), oneOff("stopped-one", { stage: "blocked" })] });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const region = await screen.findByRole("region", { name: "單集漫劇" });
    const rows = within(region).getAllByRole("button").map((button) => button.textContent ?? "");
    expect(rows.map((row) => row.split("AI 漫劇")[0])).toEqual(["waiting-one", "stopped-one", "quiet-one"]);
    expect(rows[1]).toContain("卡住");
    expect(rows[0]).not.toContain("卡住");
  });
});
