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
  { id: "d1", kind: "setting", chapter_number: 0, version: 2, body_md: "# 設定集\n世界。", body_json: { characters: [] }, status: "approved", note: "查核：世界觀一致，角色聲音有辨識度", decided_at: "2026-09-27T00:30:00Z", created_at: "2026-09-27T00:20:00Z" },
  { id: "d2", kind: "outline", chapter_number: 0, version: 1, body_md: "# 總綱", body_json: { chapters: [] }, status: "approved", note: null, decided_at: "2026-09-27T00:40:00Z", created_at: "2026-09-27T00:35:00Z" },
  { id: "d3", kind: "chapter", chapter_number: 2, version: 1, body_md: "# 第二篇", body_json: { chapter: 2, episodes: [beats(11), beats(12)] }, status: "review", note: null, decided_at: null, created_at: "2026-09-27T00:50:00Z" },
];
const episodes = [
  { number: 1, chapter_number: 1, title: "鐘", logline: "L1", beats: beats(1), status: "done", slug: "wenjian-e001", recap: "鐘響了", started_at: "2026-09-27T00:00:00Z", finished_at: "2026-09-27T00:50:00Z", video: { slug: "wenjian-e001", title: "問劍 第 1 集 鐘", format: "drama", stage: "done", checklist: [{ key: "brief", label: "企劃", done: true }], youtube_video_id: "abcdefg", last_synced_at: "2026-09-27T00:50:00Z", pending: 0, media_usd: 41.2, clip_seconds: 300 } },
  { number: 2, chapter_number: 1, title: "字", logline: "L2", beats: beats(2), status: "started", slug: "wenjian-e002", recap: null, started_at: "2026-09-27T00:55:00Z", finished_at: null, video: { slug: "wenjian-e002", title: "問劍 第 2 集 字", format: "drama", stage: "script approved", checklist: [{ key: "brief", label: "企劃", done: true }, { key: "script", label: "劇本核准", done: false }], youtube_video_id: null, last_synced_at: "2026-09-27T01:00:00Z", pending: 1, media_usd: 0, clip_seconds: 0 } },
  { number: 3, chapter_number: 1, title: "山", logline: "L3", beats: beats(3), status: "ready", slug: null, recap: null, started_at: null, finished_at: null, video: null },
];

// What the server quotes for the form's defaults (120 minutes of 3-minute hybrid episodes) against a
// month whose clip, image and episode budgets are too small for it; only the judge budget fits.
const quote = {
  episodes: 40, chapters: 4, episodes_per_chapter: 10, clip_seconds: 4320, images: 1578, judge_calls: 1698, usd: 950.5,
  budgets: {
    clip_seconds: { needed: 4320, monthly: 3000, ok: false }, images: { needed: 1578, monthly: 1500, ok: false },
    judge_calls: { needed: 1698, monthly: 3000, ok: true }, episodes_per_month: { needed: 40, monthly: 30, ok: false },
  },
  ok: false,
};
// The compilation of a finished binge series: the series' one video without an episode number.
const compilationVideo = {
  slug: "wenjian-full", title: "問劍 合集", format: "drama", stage: "done", checklist: [{ key: "brief", label: "企劃", done: true }], youtube_video_id: null,
  last_synced_at: "2026-09-27T03:00:00Z", pending: 0, media_usd: 0, clip_seconds: 0, series_slug: "wenjian", episode_number: null, compilation: true, download_available: true,
};

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

function stubFetch(options: { settings?: Record<string, unknown>; videos?: unknown[]; series?: Record<string, unknown>; seriesVideos?: unknown[] } = {}) {
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
    if (url.includes("/admin/videos?series=")) return Promise.resolve(Response.json(options.seriesVideos ?? []));
    if (url.includes("/admin/video-automation/series/binge-quote")) return Promise.resolve(Response.json(quote));
    if (url.endsWith("/admin/video-automation/series") && method === "POST") return Promise.resolve(Response.json({ ...summary, slug: "new-one", title: "新作", status: "setting", docs: [], episodes: [] }, { status: 201 }));
    if (url.endsWith("/admin/video-automation/series")) return Promise.resolve(Response.json({ series: [summary] }));
    if (url.includes("/admin/video-automation/series/new-one")) return Promise.resolve(Response.json({ ...summary, slug: "new-one", title: "新作", status: "setting", docs: [], episodes: [] }));
    if (url.includes("/admin/video-automation/series/wenjian")) return Promise.resolve(Response.json({ ...summary, ...options.series, docs, episodes }));
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
    // A series from before the binge columns reads as the classic xianxia series made of clips.
    expect(card.textContent).toContain("仙俠羈絆");
    expect(card.textContent).toContain("全片段");
    expect(card.textContent).not.toContain("免關卡");

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

  it("quotes a binge series as the numbers change, warns about each budget it overruns, and starts it with the derived payload and no slug", async () => {
    const calls = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const form = await screen.findByRole("form", { name: "一鍵開拍" });
    // The quote for the defaults (120 minutes of 3-minute hybrid episodes) arrives after the debounce.
    await waitFor(() => expect(form.textContent).toContain("40 集，4 篇（每篇 10 集）"));
    expect(form.textContent).toContain("片段 4320 秒 · 圖片 1578 張 · 約 US$950.50");
    expect(calls.find((call) => call.url.includes("binge-quote"))?.url).toContain("binge-quote?total_minutes=120&episode_minutes=3&visual_tier=hybrid");
    const lines = [...form.querySelectorAll("li")].map((line) => line.textContent);
    expect(lines).toEqual([
      "本月片段預算 3000 秒，這部要 4320 秒：先到設定分頁調高",
      "本月圖片預算 1500 張，這部要 1578 張：先到設定分頁調高",
      "本月 judge 預算 3000 次，這部要 1698 次",
      "每月集數上限 30 集，這部要 40 集：先到設定分頁調高",
    ]);
    expect(form.textContent).toContain("預算不夠時工人會停在那裡等");
    // An overrun budget is a warning, not a stop: the owner raises it on the settings tab and the worker waits.
    const start = within(form).getByRole("button", { name: "一鍵開拍" });
    expect(start).toHaveProperty("disabled", false);
    // A custom genre is the one that needs a premise.
    fireEvent.click(within(form).getByRole("radio", { name: /自訂/ }));
    expect(start).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByRole("textbox", { name: "故事前提（自訂題材必填）" }), { target: { value: "一把劍" } });
    expect(start).toHaveProperty("disabled", false);
    fireEvent.change(within(form).getByRole("textbox", { name: "故事前提（自訂題材必填）" }), { target: { value: "" } });
    fireEvent.click(within(form).getByRole("radio", { name: /重生復仇/ }));
    expect(start).toHaveProperty("disabled", false);
    fireEvent.click(within(form).getByRole("radio", { name: "女主" }));
    fireEvent.click(within(form).getByRole("radio", { name: /^靜圖/ }));
    fireEvent.change(within(form).getByRole("spinbutton", { name: "總長度（分鐘，30–480）" }), { target: { value: "30" } });
    fireEvent.change(within(form).getByRole("spinbutton", { name: "每集分鐘（2–4）" }), { target: { value: "2" } });
    await waitFor(() => expect(calls.filter((call) => call.url.includes("binge-quote")).at(-1)?.url).toContain("total_minutes=30&episode_minutes=2&visual_tier=stills"));
    fireEvent.change(within(form).getByRole("textbox", { name: "給企劃的常設備註" }), { target: { value: " 旁白慢一點 " } });
    fireEvent.click(start);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toContain("/admin/video-automation/series");
    expect(post?.body).toEqual({
      genre: "rebirth-revenge", lead: "female", total_minutes: 30, target_minutes: 2, visual_tier: "stills", style_preset: "cinematic-3d",
      hands_off: true, compilation: true, open_ended: false, note: "旁白慢一點",
    });
    await waitFor(() => expect(window.location.search).toContain("series=new-one"));
  });

  it("shows a finished binge series' compilation with its download, offers another cut, and lets the owner take the series back", async () => {
    const finished = {
      status: "finished", episodes_done: 25, genre: "rebirth-revenge", lead: "female", hands_off: true, compilation: true, visual_tier: "hybrid", total_minutes: 75,
      compilation_slug: "wenjian-full", compilation_started_at: "2026-09-27T02:00:00Z", compilation_finished_at: "2026-09-27T03:00:00Z",
    };
    const calls = stubFetch({ series: finished, seriesVideos: [compilationVideo, { ...episodes[0].video, series_slug: "wenjian", episode_number: 1 }] });
    const opened: string[] = [];
    window.history.replaceState(null, "", "/?tab=drama&series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={(slug) => opened.push(slug)} /></AdminOperationsProvider>);
    const heading = await screen.findByRole("heading", { name: /問劍/ });
    for (const pill of ["已完結", "重生復仇", "混合", "免關卡", "合集完成"]) expect(heading.textContent).toContain(pill);
    expect(screen.getByText(/共 75 分鐘/).textContent).toContain("女主");
    const block = screen.getByRole("region", { name: "合集" });
    await waitFor(() => expect(block.textContent).toContain("問劍 合集"));
    const link = within(block).getByRole("link", { name: "下載 1080p 成片" });
    expect(link.getAttribute("href")).toBe("/api/admin-video-download/wenjian-full");
    expect(link.getAttribute("download")).toBe("wenjian-full.mp4");
    fireEvent.click(within(block).getByRole("button", { name: "打開" }));
    expect(opened).toEqual(["wenjian-full"]);
    // A finished compilation may be made again; a finished series has nothing else to push along.
    expect(screen.queryByRole("button", { name: "現在開始下一集" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "做合集" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST" && call.url.endsWith("/admin/video-automation/series/wenjian/actions/compile"))).toBe(true));
    fireEvent.click(screen.getByRole("checkbox", { name: "免關卡" }));
    await waitFor(() => expect(calls.some((call) => call.method === "PATCH")).toBe(true));
    const patch = calls.find((call) => call.method === "PATCH");
    expect(patch?.url).toContain("/admin/video-automation/series/wenjian");
    expect(patch?.body).toEqual({ hands_off: false });
  });

  it("says the cut is still in the worker's workspace while the compilation is being made", async () => {
    const making = { status: "finished", compilation: true, compilation_slug: "wenjian-full", compilation_started_at: "2026-09-27T02:00:00Z", compilation_finished_at: null };
    const cutting = { ...compilationVideo, stage: "clips", download_available: false, checklist: [{ key: "brief", label: "企劃", done: true }, { key: "clips", label: "片段生成", done: false }] };
    stubFetch({ series: making, seriesVideos: [cutting] });
    window.history.replaceState(null, "", "/?tab=drama&series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const block = await screen.findByRole("region", { name: "合集" });
    await waitFor(() => expect(block.textContent).toContain("成片還在工人的工作區"));
    expect(block.textContent).toContain("合集製作中");
    expect(block.textContent).toContain("片段生成");
    expect(within(block).queryByRole("link")).toBeNull();
    expect(screen.queryByRole("button", { name: "做合集" })).toBeNull();
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
    expect(docsRegion.textContent).toContain("備註：");
    expect(docsRegion.textContent).toContain("查核：世界觀一致，角色聲音有辨識度");
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
    expect(screen.queryByRole("form", { name: "一鍵開拍" })).toBeNull();
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
