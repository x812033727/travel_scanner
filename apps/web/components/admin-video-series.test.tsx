import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { REFRESH_MS } from "./admin-video-review-card";
import { AdminVideoSeries, DocPanel, type SeriesDoc } from "./admin-video-series";
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
// A one-off is a series of one episode whose only document is its story bible (docs/videos/DRAMA-FLOW.md, section 2).
const oneOff = {
  ...summary, id: "7c2e3d4f-5a6b-4c7d-8e9f-0a1b2c3d4e5f", slug: "one-off-1a2b3c4d", kind: "one-off", title: "精衛填海", premise: "炎帝最小的女兒在東海溺水。", planned_episodes: 1, episodes_per_chapter: 1, chapters: 1,
  episodes_done: 0, episodes_started: 1, episodes_ready: 0, docs_pending: 0, messages_pending: 2, media_usd: 12.5, clip_seconds: 96, note: null,
};
const beats = (number: number) => ({ number, title: `第 ${number} 集`, logline: `L${number}`, hook: "鐘聲", conflict: "誰敲的", turn: "鐘自己響", cliffhanger: { type: "reveal", text: "鐘下有字" }, setups: ["m1"], payoffs: [], tension: [2, 3, 3, 4, 5] });
type Doc = Record<string, unknown>;
const docs: Doc[] = [
  { id: "d1", kind: "setting", chapter_number: 0, version: 2, body_md: "# 設定集\n世界。", body_json: { characters: [] }, status: "approved", note: "查核：世界觀一致，角色聲音有辨識度", decided_at: "2026-09-27T00:30:00Z", created_at: "2026-09-27T00:20:00Z" },
  { id: "d2", kind: "outline", chapter_number: 0, version: 1, body_md: "# 總綱", body_json: { chapters: [] }, status: "approved", note: null, decided_at: "2026-09-27T00:40:00Z", created_at: "2026-09-27T00:35:00Z" },
  { id: "d3", kind: "chapter", chapter_number: 2, version: 1, body_md: "# 第二篇", body_json: { chapter: 2, episodes: [beats(11), beats(12)] }, status: "review", note: null, decided_at: null, created_at: "2026-09-27T00:50:00Z" },
];
const bible = { id: "b1", kind: "bible", chapter_number: 0, version: 1, body_md: "# 故事聖經\n精衛。", body_json: { characters: [] }, status: "approved", note: null, decided_at: "2026-09-27T02:00:00Z", created_at: "2026-09-27T01:50:00Z", unanswered: 0 };
const episodes = [
  { number: 1, chapter_number: 1, title: "鐘", logline: "L1", beats: beats(1), status: "done", slug: "wenjian-e001", recap: "鐘響了", started_at: "2026-09-27T00:00:00Z", finished_at: "2026-09-27T00:50:00Z", video: { slug: "wenjian-e001", title: "問劍 第 1 集 鐘", format: "drama", stage: "done", checklist: [{ key: "brief", label: "企劃", done: true }], youtube_video_id: "abcdefg", last_synced_at: "2026-09-27T00:50:00Z", pending: 0, media_usd: 41.2, clip_seconds: 300 } },
  { number: 2, chapter_number: 1, title: "字", logline: "L2", beats: beats(2), status: "started", slug: "wenjian-e002", recap: null, started_at: "2026-09-27T00:55:00Z", finished_at: null, video: { slug: "wenjian-e002", title: "問劍 第 2 集 字", format: "drama", stage: "script approved", checklist: [{ key: "brief", label: "企劃", done: true }, { key: "script", label: "劇本核准", done: false }], youtube_video_id: null, last_synced_at: "2026-09-27T01:00:00Z", pending: 1, media_usd: 0, clip_seconds: 0 } },
  { number: 3, chapter_number: 1, title: "山", logline: "L3", beats: beats(3), status: "ready", slug: null, recap: null, started_at: null, finished_at: null, video: null },
];
const oneOffEpisodes = [
  { number: 1, chapter_number: 1, title: "精衛填海", logline: "L1", beats: beats(1), status: "started", slug: "one-off-1a2b3c4d-e001", recap: null, started_at: "2026-09-27T02:05:00Z", finished_at: null, video: { slug: "one-off-1a2b3c4d-e001", title: "精衛填海", format: "drama", stage: "script", checklist: [{ key: "script", label: "劇本核准", done: false }], youtube_video_id: null, last_synced_at: "2026-09-27T02:10:00Z", pending: 1, media_usd: 12.5, clip_seconds: 96 } },
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
    stage_models: Object.fromEntries(["planner", "writer", "verifier", "listener", "translator", "caption_reviewer"].map((stage) => [stage, { provider: "anthropic", model: "claude-sonnet-5" }])),
    voice: { provider: "gemini", name: "Sulafat", style: null, model: null, rate: "+0%" }, target_minutes_min: 8, target_minutes_max: 12,
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

type Line = { id: string; subject: string; author: string; body_md: string; refers_to: string | null; answered_at: string | null; created_at: string; created_by_user_id: string | null };
type Call = { url: string; method: string; body?: Record<string, unknown> };

/**
 * The site as the page sees it: the series lists by kind, one series with its documents, the
 * threads by subject (an owner's line posted here shows up on the next read), the requests.
 * `answer` plays the model: it answers every waiting line and, when given, files the new documents.
 */
function stubFetch(options: { docs?: Doc[]; threads?: Record<string, Line[]>; oneOffs?: (typeof oneOff)[]; withdrawRefused?: boolean ; settings?: Record<string, unknown>; series?: Record<string, unknown>; seriesVideos?: unknown[] } = {}) {
  const calls: Call[] = [];
  let currentDocs = options.docs ?? docs;
  const threads = options.threads ?? {};
  let counter = 0;
  const newOne = { ...summary, slug: "new-one", title: "新作", status: "setting", docs: [], episodes: [] };
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    const body = init?.body ? JSON.parse(String(init.body)) as Record<string, unknown> : undefined;
    calls.push({ url, method, body });
    if (options.settings && url.endsWith("/admin/video-automation/settings")) {
      if (method === "PUT") return Promise.resolve(Response.json({ ...options.settings, ...body, updated_at: "2026-09-27T09:00:00Z" }));
      return Promise.resolve(Response.json(options.settings));
    }
    if (url.includes("/admin/videos?series=")) return Promise.resolve(Response.json(options.seriesVideos ?? []));
    if (url.includes("/admin/video-automation/series/binge-quote")) return Promise.resolve(Response.json(quote));
    if (method === "DELETE" && url.includes("/admin/video-automation/series/")) {
      if (options.withdrawRefused) return Promise.resolve(Response.json({ code: "video_series_started", detail: "第 1 集已經開始做了，不能撤回" }, { status: 409 }));
      return Promise.resolve(Response.json({ slug: url.split("/").pop(), requests_cancelled: 1 }));
    }
    if (url.endsWith("/admin/video-automation/series") && method === "POST") return Promise.resolve(Response.json(newOne, { status: 201 }));
    if (url.endsWith("/admin/video-automation/series?kind=series")) return Promise.resolve(Response.json({ series: [summary] }));
    if (url.endsWith("/admin/video-automation/series?kind=one-off")) return Promise.resolve(Response.json({ series: options.oneOffs ?? [] }));
    if (url.endsWith("/messages") && method === "POST") {
      const subject = String(body?.subject);
      const line: Line = { id: `m${++counter}`, subject, author: "owner", body_md: String(body?.body), refers_to: "v1", answered_at: null, created_at: `2026-09-27T03:0${counter}:00Z`, created_by_user_id: "u1" };
      (threads[subject] ??= []).push(line);
      return Promise.resolve(Response.json(line, { status: 201 }));
    }
    if (url.includes("/messages?subject=")) {
      const subject = new URL(url, "http://test").searchParams.get("subject") ?? "";
      return Promise.resolve(Response.json({ messages: threads[subject] ?? [] }));
    }
    if (url.includes("/admin/video-automation/series/new-one")) return Promise.resolve(Response.json(newOne));
    if (url.includes("/admin/video-automation/series/one-off-9f8e7d6c")) return Promise.resolve(Response.json({ ...oneOff, slug: "one-off-9f8e7d6c", title: "大禹治水", status: "setting", episodes_started: 0, docs: [], episodes: [{ ...oneOffEpisodes[0], status: "planned", slug: null, started_at: null, video: null }] }));
    if (url.includes("/admin/video-automation/series/one-off-1a2b3c4d")) return Promise.resolve(Response.json({ ...oneOff, docs: [bible], episodes: oneOffEpisodes }));
    if (url.includes("/admin/video-automation/series/wenjian")) return Promise.resolve(Response.json({ ...summary, ...options.series, docs: currentDocs, episodes }));
    if (url.endsWith("/drama-requests") && method === "POST") return Promise.resolve(Response.json({ id: "r1", premise: body?.premise, title: null, source_guide: null, style_preset: body?.style_preset, target_minutes: body?.target_minutes, note: null, status: "queued", slug: null, series_slug: "one-off-1a2b3c4d", episode_number: 1, created_at: "2026-09-27T04:00:00Z", started_at: null, finished_at: null, cancelled_at: null }, { status: 201 }));
    if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests: [] }));
    return Promise.resolve(Response.json([]));
  }));
  const answer = (subject: string, reply: string, refersTo: string, newDocs?: Doc[]) => {
    for (const line of threads[subject] ?? []) line.answered_at ??= "2026-09-27T03:10:00Z";
    (threads[subject] ??= []).push({ id: `m${++counter}`, subject, author: "planner", body_md: reply, refers_to: refersTo, answered_at: "2026-09-27T03:10:00Z", created_at: "2026-09-27T03:10:00Z", created_by_user_id: null });
    if (newDocs) currentDocs = newDocs;
  };
  return { calls, answer };
}

const panelOf = (title: string) => screen.getByText(title).closest("details") as HTMLElement;

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
  window.history.replaceState(null, "", "/");
});

describe("AdminVideoSeries", () => {
  it("lists the series with their progress and starts a new one from the form", async () => {
    const { calls } = stubFetch();
    const opened: string[] = [];
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={(slug) => opened.push(slug)} /></AdminOperationsProvider>);
    const card = await screen.findByRole("button", { name: /問劍/ });
    expect(card.textContent).toContain("製作中");
    expect(card.textContent).toContain("1 份等你核准");
    expect(card.textContent).toContain("1/25 集 · 3 篇");
    expect(card.textContent).toContain("US$41.20");
    expect(card.textContent).not.toContain("等模型回覆");
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

  it("lists one-off episodes apart with what waits on them, and opens the one the form files", async () => {
    // The server starts a one-off at "setting" while the worker writes its story bible.
    const { calls } = stubFetch({ oneOffs: [{ ...oneOff, status: "setting" }] });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const oneOffs = await screen.findByRole("region", { name: "單集漫劇" });
    const card = within(oneOffs).getByRole("button", { name: /精衛填海/ });
    expect(card.textContent).toContain("單集");
    expect(card.textContent).toContain("故事聖經");
    expect(card.textContent).not.toContain("設定集");
    expect(card.textContent).toContain("2 則等模型回覆");
    expect(card.textContent).toContain("US$12.50 · 片段 96 秒");
    expect(card.textContent).not.toContain("集 · ");
    expect(screen.getByRole("list", { name: "作品" }).textContent).not.toContain("精衛填海");
    expect(calls.some((call) => call.url.includes("/admin/videos"))).toBe(false);

    fireEvent.click(screen.getByText("新的漫劇", { selector: "summary" }));
    fireEvent.change(screen.getByRole("textbox", { name: "故事前提（必填）" }), { target: { value: "大禹治水" } });
    fireEvent.click(screen.getByRole("button", { name: "排進製作" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    expect(calls.find((call) => call.method === "POST")?.url).toContain("/admin/video-automation/drama-requests");
    await waitFor(() => expect(window.location.search).toContain("series=one-off-1a2b3c4d"));
    // The one-off's page: its bible, its one episode, and none of a long series' planning controls.
    const heading = await screen.findByRole("heading", { name: /精衛填海/ });
    expect(heading.textContent).toContain("單集");
    expect(heading.textContent).toContain("2 則等模型回覆");
    expect(screen.getByRole("region", { name: "文件" }).textContent).toContain("故事聖經");
    expect(screen.getByRole("region", { name: "集數" }).textContent).toContain("劇本核准");
    expect(screen.queryByRole("button", { name: "先規劃下一篇" })).toBeNull();
    expect(screen.getByRole("button", { name: "現在開始下一集" })).toBeTruthy();
    expect(screen.queryByText(/\/1 集/)).toBeNull();
    expect(screen.queryByRole("button", { name: "撤回" }), "its episode has started").toBeNull();
  });

  it("withdraws a one-off the worker has not started, from its card or its page, and says why when refused", async () => {
    const waiting = { ...oneOff, slug: "one-off-9f8e7d6c", title: "大禹治水", status: "setting", episodes_started: 0 };
    const { calls } = stubFetch({ oneOffs: [waiting, oneOff] });
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const oneOffs = await screen.findByRole("region", { name: "單集漫劇" });
    const withdraws = within(oneOffs).getAllByRole("button", { name: "撤回" });
    expect(withdraws, "only the one still at its bible").toHaveLength(1);
    expect(withdraws[0].closest("li")?.textContent).toContain("大禹治水");
    const listed = calls.filter((call) => call.url.endsWith("?kind=one-off")).length;
    fireEvent.click(withdraws[0]);
    await waitFor(() => expect(calls.some((call) => call.method === "DELETE")).toBe(true));
    expect(confirm.mock.calls[0][0]).toContain("大禹治水");
    expect(calls.find((call) => call.method === "DELETE")?.url).toMatch(/\/admin\/video-automation\/series\/one-off-9f8e7d6c$/);
    await waitFor(() => expect(calls.filter((call) => call.url.endsWith("?kind=one-off")).length).toBeGreaterThan(listed));

    // From its page: withdrawn, the page goes back to the list.
    fireEvent.click(within(oneOffs).getByRole("button", { name: /大禹治水/ }));
    await screen.findByRole("heading", { name: /大禹治水/ });
    const deletes = calls.filter((call) => call.method === "DELETE").length;
    fireEvent.click(screen.getByRole("button", { name: "撤回" }));
    await waitFor(() => expect(calls.filter((call) => call.method === "DELETE").length).toBe(deletes + 1));
    await waitFor(() => expect(window.location.search).not.toContain("series="));
    confirm.mockRestore();
  });

  it("keeps a one-off whose withdrawal the server refused and shows the reason", async () => {
    const waiting = { ...oneOff, slug: "one-off-9f8e7d6c", title: "大禹治水", status: "setting", episodes_started: 0 };
    stubFetch({ oneOffs: [waiting], withdrawRefused: true });
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    window.history.replaceState(null, "", "/?series=one-off-9f8e7d6c");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /大禹治水/ });
    fireEvent.click(screen.getByRole("button", { name: "撤回" }));
    expect((await screen.findByRole("alert")).textContent).toContain("第 1 集已經開始做了");
    expect(window.location.search).toContain("series=one-off-9f8e7d6c");
    expect(screen.getByRole("button", { name: "撤回" })).toHaveProperty("disabled", false);
    confirm.mockRestore();
  });

  it("opens a series: the chapter outline waiting for the owner, its beats table, and the episode table", async () => {
    const { calls } = stubFetch();
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
    expect(decision?.body).toEqual({ decision: "reject", note: "第 12 集再緊一點", expected_version: 1 });

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

  it("discusses a chapter outline: the owner's line waits for the model, and the thread stays when the model answers with a new version", async () => {
    const { calls, answer } = stubFetch();
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /問劍/ });
    const panel = panelOf("第 2 篇細綱");
    const thread = within(panel).getByRole("region", { name: "討論" });
    await waitFor(() => expect(thread.textContent).toContain("還沒有討論"));
    // Every document reads its own thread, by the subject the API names it.
    expect(calls.filter((call) => call.url.includes("/messages?subject=")).map((call) => decodeURIComponent(call.url.split("subject=")[1])).sort()).toEqual(["chapter:2", "outline", "setting"]);
    expect(within(thread).queryByText("等模型回覆")).toBeNull();

    const send = within(thread).getByRole("button", { name: "送出" });
    expect(send).toHaveProperty("disabled", true);
    fireEvent.change(within(thread).getByRole("textbox", { name: "給模型的話" }), { target: { value: " 第二幕為什麼要死一個人？ " } });
    fireEvent.click(send);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toContain("/admin/video-automation/series/wenjian/messages");
    expect(post?.body).toEqual({ subject: "chapter:2", body: "第二幕為什麼要死一個人？" });
    // The thread is read again: the line, who said it, about which version, and that it waits.
    await waitFor(() => expect(thread.textContent).toContain("第二幕為什麼要死一個人？"));
    expect(thread.textContent).toContain("站主");
    expect(thread.textContent).toContain("對第 1 版");
    // The thread's header pill and the pill on the unanswered line.
    expect(within(thread).getAllByText("等模型回覆")).toHaveLength(2);
    expect((within(thread).getByRole("textbox", { name: "給模型的話" }) as HTMLTextAreaElement).value).toBe("");
    // The approve and send back controls are untouched by the discussion.
    expect(within(panel).getByRole("button", { name: "核准" })).toBeTruthy();
    expect(within(panel).getByRole("button", { name: "退回" })).toHaveProperty("disabled", true);

    // The model answers and files version 2; the owner's next line brings both to the page.
    answer("chapter:2", "因為要讓師兄的選擇有代價；我把第 12 集改成他先開口。", "v2", [docs[0], docs[1], { ...docs[2], status: "rejected", note: "依討論改寫" }, { ...docs[2], id: "d4", version: 2, body_md: "# 第二篇 v2", created_at: "2026-09-27T03:10:00Z" }].filter((doc) => doc.id !== "d3"));
    fireEvent.change(within(thread).getByRole("textbox", { name: "給模型的話" }), { target: { value: "把師兄改成沉默寡言" } });
    fireEvent.click(within(thread).getByRole("button", { name: "送出" }));
    await waitFor(() => expect(panelOf("第 2 篇細綱").textContent).toContain("第 2 版"));
    const renewed = within(panelOf("第 2 篇細綱")).getByRole("region", { name: "討論" });
    await waitFor(() => expect(renewed.textContent).toContain("把師兄改成沉默寡言"));
    expect(renewed.textContent).toContain("第二幕為什麼要死一個人？");
    expect(renewed.textContent).toContain("企劃");
    expect(renewed.textContent).toContain("因為要讓師兄的選擇有代價");
    expect(renewed.textContent).toContain("對第 2 版");
    expect(within(renewed).getAllByText("等模型回覆")).toHaveLength(2);
    expect(within(panelOf("第 2 篇細綱")).getByRole("button", { name: "核准" })).toBeTruthy();
  });

  it("keeps an approved document's thread as a record and takes no new line on it", async () => {
    const said: Line[] = [
      { id: "m1", subject: "setting", author: "owner", body_md: "門派再多一個。", refers_to: "v1", answered_at: "2026-09-27T00:15:00Z", created_at: "2026-09-27T00:10:00Z", created_by_user_id: "u1" },
      { id: "m2", subject: "setting", author: "planner", body_md: "加了「聽雨樓」，見第 2 版。", refers_to: "v2", answered_at: "2026-09-27T00:15:00Z", created_at: "2026-09-27T00:15:00Z", created_by_user_id: null },
    ];
    stubFetch({ threads: { setting: said }, docs: [docs[0], docs[1], { ...docs[2], unanswered: 1 }] });
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /問劍/ });
    const approved = panelOf("設定集");
    const record = await within(approved).findByRole("region", { name: "討論" });
    await waitFor(() => expect(record.textContent).toContain("聽雨樓"));
    expect(record.textContent).toContain("站主");
    expect(record.textContent).toContain("企劃");
    expect(record.textContent).toContain("對第 2 版");
    expect(record.textContent).toContain("只留紀錄");
    expect(within(record).queryByRole("textbox")).toBeNull();
    expect(within(record).queryByRole("button", { name: "送出" })).toBeNull();
    // The server's count marks a document whose thread waits: on the panel's summary line, and in
    // the thread header once its (here empty) lines are read; no line of its own carries one.
    const waiting = panelOf("第 2 篇細綱");
    expect(within(waiting.querySelector("summary") as HTMLElement).getByText("等模型回覆")).toBeTruthy();
    expect(within(waiting).getAllByText("等模型回覆")).toHaveLength(2);
    expect(within(approved).queryByText("等模型回覆")).toBeNull();
  });

  it("lets a reader look but not decide", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /問劍/ });
    expect(screen.queryByRole("button", { name: "核准" })).toBeNull();
    expect(screen.queryByRole("button", { name: "跳過" })).toBeNull();
    expect(screen.queryByRole("button", { name: "撤回" })).toBeNull();
    expect(screen.queryByText("新的作品")).toBeNull();
    expect(screen.queryByRole("textbox", { name: "給模型的話" })).toBeNull();
    expect(screen.queryByRole("button", { name: "送出" })).toBeNull();
  });

  it("quotes a binge series as the numbers change, warns about each budget it overruns, and starts it with the derived payload and no slug", async () => {
    const { calls } = stubFetch();
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
    const { calls } = stubFetch({ series: finished, seriesVideos: [compilationVideo, { ...episodes[0].video, series_slug: "wenjian", episode_number: 1 }] });
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
    // A series has the one compilation the worker named <series>-full, so there is no second
    // 做合集; a finished series has nothing else to push along either.
    expect(screen.queryByRole("button", { name: "現在開始下一集" })).toBeNull();
    expect(screen.queryByRole("button", { name: "做合集" })).toBeNull();
    fireEvent.click(screen.getByRole("checkbox", { name: "免關卡" }));
    await waitFor(() => expect(calls.some((call) => call.method === "PATCH")).toBe(true));
    const patch = calls.find((call) => call.method === "PATCH");
    expect(patch?.url).toContain("/admin/video-automation/series/wenjian");
    expect(patch?.body).toEqual({ hands_off: false });
  });

  it("offers 做合集 on a finished series that was not set up to make one, and posts the action", async () => {
    const finished = { status: "finished", episodes_done: 25, compilation: false, compilation_slug: null, compilation_started_at: null, compilation_finished_at: null };
    const { calls } = stubFetch({ series: finished, seriesVideos: [] });
    window.history.replaceState(null, "", "/?tab=drama&series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const block = await screen.findByRole("region", { name: "合集" });
    expect(block.textContent).toContain("沒有設定要做合集");
    fireEvent.click(screen.getByRole("button", { name: "做合集" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST" && call.url.endsWith("/admin/video-automation/series/wenjian/actions/compile"))).toBe(true));
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

  it("shows a reader the finished compilation but not the download the API would refuse", async () => {
    const finished = {
      status: "finished", episodes_done: 25, genre: "rebirth-revenge", lead: "female", hands_off: true, compilation: true, visual_tier: "hybrid", total_minutes: 75,
      compilation_slug: "wenjian-full", compilation_started_at: "2026-09-27T02:00:00Z", compilation_finished_at: "2026-09-27T03:00:00Z",
    };
    stubFetch({ series: finished, seriesVideos: [compilationVideo] });
    window.history.replaceState(null, "", "/?tab=drama&series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const block = await screen.findByRole("region", { name: "合集" });
    await waitFor(() => expect(block.textContent).toContain("問劍 合集"));
    expect(within(block).queryByRole("link", { name: "下載 1080p 成片" })).toBeNull();
    expect(screen.queryByRole("checkbox", { name: "免關卡" })).toBeNull();
  });

  it("says the drama route is off, opens its settings first, and says it is on once saved", async () => {
    const { calls } = stubFetch({ settings: videoSettings(false) });
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
});


describe("document revision safeguards", () => {
  it("saves text as an unapproved draft and only synchronizes after an explicit request", async () => {
    const { calls } = stubFetch();
    const original = { ...docs[0], status: "review", needs_reconciliation: false } as SeriesDoc;
    const changed = vi.fn();
    const view = render(<DocPanel slug="wenjian" doc={original} canManage onChanged={changed} />);
    fireEvent.click(screen.getByText("自己改", { selector: "summary" }));
    fireEvent.change(screen.getByRole("textbox", { name: "自己改" }), { target: { value: "# 設定集\n主角改名為沈知芸。" } });
    expect(screen.queryByRole("button", { name: "儲存並核准" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "儲存文字草稿" }));
    await waitFor(() => expect(changed).toHaveBeenCalledOnce());
    expect(calls.find((call) => call.method === "PUT")?.body).toEqual({ body_md: "# 設定集\n主角改名為沈知芸。", approve: false });
    expect(calls.filter((call) => call.method === "POST")).toHaveLength(0);
    view.rerender(<DocPanel slug="wenjian" doc={{ ...original, body_json: {}, needs_reconciliation: true, version: 3 }} canManage onChanged={changed} />);
    expect(screen.getByRole("button", { name: "核准" })).toHaveProperty("disabled", true);
    expect(screen.getByText(/模型呼叫可能產生費用/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "請 AI 同步製作資料" }));
    await waitFor(() => expect(calls.filter((call) => call.method === "POST")).toHaveLength(1));
    const request = calls.find((call) => call.method === "POST");
    expect(request?.url).toMatch(/\/wenjian\/messages$/);
    expect(request?.body?.subject).toBe("setting");
    expect(request?.body?.body).toContain("最新文字草稿");
  });

  it("blocks later imported documents until their latest prerequisites are approved", async () => {
    const pending = docs.map((doc) => ({ ...doc, status: "review" }));
    stubFetch({ docs: pending });
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    await screen.findByRole("heading", { name: /問劍/ });
    expect(within(panelOf("設定集")).getByRole("button", { name: "核准" })).toHaveProperty("disabled", false);
    const approvals = within(screen.getByRole("region", { name: "文件" })).getAllByRole("button", { name: "核准" });
    expect(approvals.filter((button) => !(button as HTMLButtonElement).disabled)).toHaveLength(1);
  });

  it.each([false, true])("does not resubmit AI synchronization while the document refresh is delayed (refresh fails: %s)", async (refreshFails) => {
    const revisionDocs = [{ ...docs[0], status: "review", needs_reconciliation: true, unanswered: 0 }];
    const { calls } = stubFetch({ docs: revisionDocs });
    const baseFetch = globalThis.fetch;
    let holdRefresh = false;
    let releaseRefresh!: (response: Response) => void;
    let markRefreshStarted!: () => void;
    const refreshResponse = new Promise<Response>((resolve) => { releaseRefresh = resolve; });
    const refreshStarted = new Promise<void>((resolve) => { markRefreshStarted = resolve; });
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (holdRefresh && String(input).endsWith("/admin/video-automation/series/wenjian") && (init?.method ?? "GET") === "GET") {
        holdRefresh = false;
        markRefreshStarted();
        return refreshResponse;
      }
      return baseFetch(input, init);
    }));
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const synchronize = await screen.findByRole("button", { name: "請 AI 同步製作資料" });
    holdRefresh = true;
    await act(async () => {
      fireEvent.click(synchronize);
      await refreshStarted;
    });
    expect(synchronize).toHaveProperty("disabled", true);
    fireEvent.click(synchronize);
    expect(calls.filter((call) => call.method === "POST" && call.url.endsWith("/messages"))).toHaveLength(1);

    await act(async () => {
      releaseRefresh(refreshFails
        ? Response.json({ detail: "refresh failed" }, { status: 503 })
        : Response.json({ ...summary, docs: revisionDocs, episodes }));
    });
    // Neither a failed GET nor a still-stale unanswered=0 response cancels the accepted POST.
    expect(synchronize).toHaveProperty("disabled", true);
    fireEvent.click(synchronize);
    expect(calls.filter((call) => call.method === "POST" && call.url.endsWith("/messages"))).toHaveLength(1);
    if (refreshFails) {
      expect(screen.getByText("refresh failed")).toBeTruthy();
      revisionDocs[0] = { ...revisionDocs[0], unanswered: 1 };
      fireEvent.click(screen.getByRole("button", { name: "再試一次" }));
      await waitFor(() => expect(screen.queryByText("refresh failed")).toBeNull());
      expect(synchronize).toHaveProperty("disabled", true);
      expect(calls.filter((call) => call.method === "POST" && call.url.endsWith("/messages"))).toHaveLength(1);
    }
  });

  it("allows retry after a rejected synchronization POST and keeps an accepted request locked until it is answered or revised", async () => {
    stubFetch();
    const baseFetch = globalThis.fetch;
    let attempts = 0;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (String(input).endsWith("/messages") && init?.method === "POST" && ++attempts === 1) {
        return Promise.resolve(Response.json({ detail: "synchronization rejected" }, { status: 503 }));
      }
      return baseFetch(input, init);
    }));
    const original = { ...docs[0], status: "review", needs_reconciliation: true, unanswered: 0 } as SeriesDoc;
    const changed = vi.fn();
    const view = render(<DocPanel slug="wenjian" doc={original} canManage onChanged={changed} />);
    const synchronize = screen.getByRole("button", { name: "請 AI 同步製作資料" });
    fireEvent.click(synchronize);
    expect((await screen.findByRole("alert")).textContent).toContain("synchronization rejected");
    expect(synchronize).toHaveProperty("disabled", false);
    expect(changed).not.toHaveBeenCalled();
    fireEvent.click(synchronize);
    await waitFor(() => expect(changed).toHaveBeenCalledOnce());
    expect(attempts).toBe(2);
    expect(synchronize).toHaveProperty("disabled", true);
    view.rerender(<DocPanel slug="wenjian" doc={{ ...original, unanswered: 1 }} canManage onChanged={changed} />);
    expect(synchronize).toHaveProperty("disabled", true);
    view.rerender(<DocPanel slug="wenjian" doc={original} canManage onChanged={changed} />);
    expect(synchronize).toHaveProperty("disabled", true);
    view.rerender(<DocPanel slug="wenjian" doc={{ ...original, version: 3 }} canManage onChanged={changed} />);
    expect(synchronize).toHaveProperty("disabled", false);
  });

  it("unlocks an answered synchronization without a new revision or ever observing an unanswered count", async () => {
    vi.useFakeTimers({ toFake: ["setInterval", "clearInterval"] });
    const revisionDocs = [{ ...docs[0], status: "review", needs_reconciliation: true, unanswered: 0 }];
    const { calls, answer } = stubFetch({ docs: revisionDocs });
    const baseFetch = globalThis.fetch;
    let posted = false;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/messages") && init?.method === "POST") posted = true;
      if (posted && url.endsWith("/admin/video-automation/series/wenjian") && (init?.method ?? "GET") === "GET") {
        return Promise.resolve(Response.json({ detail: "refresh failed" }, { status: 503 }));
      }
      return baseFetch(input, init);
    }));
    window.history.replaceState(null, "", "/?series=wenjian");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
    const synchronize = await screen.findByRole("button", { name: "請 AI 同步製作資料" });
    fireEvent.click(synchronize);
    await screen.findByText("refresh failed");
    expect(synchronize).toHaveProperty("disabled", true);
    // The model answers the exact owner message, but does not write a document. The parent's
    // GET keeps failing, so the displayed version and unanswered=0 can never acknowledge it.
    answer("setting", "請先補充主角的本名。", "v2");
    await act(async () => { await vi.advanceTimersByTimeAsync(REFRESH_MS); });
    expect(screen.getByText("請先補充主角的本名。")).toBeTruthy();
    expect(synchronize).toHaveProperty("disabled", false);
    fireEvent.click(synchronize);
    await waitFor(() => expect(calls.filter((call) => call.method === "POST" && call.url.endsWith("/messages"))).toHaveLength(2));
  });

  it("submits the version actually reviewed and reports a stale approval without claiming success", async () => {
    const { calls } = stubFetch();
    const baseFetch = globalThis.fetch;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (String(input).endsWith("/decision") && init?.method === "POST") {
        void baseFetch(input, init);
        return Promise.resolve(Response.json({ code: "video_series_doc_stale", detail: "文件已有新版本，請重新載入並審閱後再決定" }, { status: 409 }));
      }
      return baseFetch(input, init);
    }));
    const original = { ...docs[0], status: "review", needs_reconciliation: false, version: 2 } as SeriesDoc;
    const changed = vi.fn();
    render(<DocPanel slug="wenjian" doc={original} canManage onChanged={changed} />);
    fireEvent.click(screen.getByRole("button", { name: "核准" }));
    expect((await screen.findByRole("alert")).textContent).toContain("文件已有新版本，請重新載入並審閱後再決定");
    expect(calls.find((call) => call.method === "POST")?.body).toEqual({ decision: "approve", expected_version: 2 });
    expect(changed).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "核准" })).toHaveProperty("disabled", false);
  });
});
