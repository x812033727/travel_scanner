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
// A one-off is a series of one episode whose only document is its story bible (docs/videos/DRAMA-FLOW.md, section 2).
const oneOff = {
  ...summary, id: "7c2e3d4f-5a6b-4c7d-8e9f-0a1b2c3d4e5f", slug: "one-off-1a2b3c4d", kind: "one-off", title: "精衛填海", premise: "炎帝最小的女兒在東海溺水。", planned_episodes: 1, episodes_per_chapter: 1, chapters: 1,
  episodes_done: 0, episodes_started: 1, episodes_ready: 0, docs_pending: 0, messages_pending: 2, media_usd: 12.5, clip_seconds: 96, note: null,
};
const beats = (number: number) => ({ number, title: `第 ${number} 集`, logline: `L${number}`, hook: "鐘聲", conflict: "誰敲的", turn: "鐘自己響", cliffhanger: { type: "reveal", text: "鐘下有字" }, setups: ["m1"], payoffs: [], tension: [2, 3, 3, 4, 5] });
type Doc = Record<string, unknown>;
const docs: Doc[] = [
  { id: "d1", kind: "setting", chapter_number: 0, version: 2, body_md: "# 設定集\n世界。", body_json: { characters: [] }, status: "approved", note: null, decided_at: "2026-09-27T00:30:00Z", created_at: "2026-09-27T00:20:00Z" },
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

type Line = { id: string; subject: string; author: string; body_md: string; refers_to: string | null; answered_at: string | null; created_at: string; created_by_user_id: string | null };
type Call = { url: string; method: string; body?: Record<string, unknown> };

/**
 * The site as the page sees it: the series lists by kind, one series with its documents, the
 * threads by subject (an owner's line posted here shows up on the next read), the requests.
 * `answer` plays the model: it answers every waiting line and, when given, files the new documents.
 */
function stubFetch(options: { docs?: Doc[]; threads?: Record<string, Line[]>; oneOffs?: (typeof oneOff)[] } = {}) {
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
    if (url.includes("/admin/video-automation/series/one-off-1a2b3c4d")) return Promise.resolve(Response.json({ ...oneOff, docs: [bible], episodes: oneOffEpisodes }));
    if (url.includes("/admin/video-automation/series/wenjian")) return Promise.resolve(Response.json({ ...summary, docs: currentDocs, episodes }));
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
    expect(screen.queryByText("新的作品")).toBeNull();
    expect(screen.queryByRole("textbox", { name: "給模型的話" })).toBeNull();
    expect(screen.queryByRole("button", { name: "送出" })).toBeNull();
  });
});
