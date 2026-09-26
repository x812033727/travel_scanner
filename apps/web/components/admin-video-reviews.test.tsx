import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { youtubeVideoId } from "./admin-video-review-card";
import { AdminVideoReviews } from "./admin-video-reviews";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const summary = {
  slug: "ai-model-choice", title: "AI 模型怎麼挑", stage: "final", youtube_video_id: null,
  last_synced_at: "2026-09-25T05:00:00Z", pending: 2,
  checklist: [{ key: "brief", label: "企劃", done: true }, { key: "final", label: "成片", done: false }],
};
const outline = {
  id: "11111111-1111-4111-8111-111111111111", gate: "outline", content_sha256: "a".repeat(64), summary: "三個大綱",
  payload: { brief: "# 企劃", options: [{ key: "A", title: "判斷方法框架" }, { key: "B", title: "從情境開始" }] },
  files: [], status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-25T05:00:00Z",
};
const final = {
  id: "22222222-2222-4222-8222-222222222222", gate: "final", content_sha256: "b".repeat(64), summary: "成片 10:00",
  payload: { checks: { ok: true, problems: [] }, chapters: [{ time: "0:00", title: "開場" }] },
  files: [{ role: "preview", sha256: "c".repeat(64), size: 10, content_type: "video/mp4" }],
  status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-25T05:00:00Z",
};

function stubFetch() {
  const posts: Array<{ url: string; body: unknown }> = [];
  const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (init?.method === "POST") {
      posts.push({ url, body: JSON.parse(String(init.body)) });
      return Promise.resolve(Response.json({ ...outline, status: "approved" }));
    }
    const body = url.endsWith("/admin/videos") ? [summary] : { ...summary, reviews: [outline, final] };
    return Promise.resolve(Response.json(body));
  });
  vi.stubGlobal("fetch", fetchMock);
  return posts;
}

afterEach(() => {
  vi.unstubAllGlobals();
  // jsdom has no clipboard; a test that defines one must not leak it into the fallback test.
  delete (navigator as { clipboard?: unknown }).clipboard;
  window.history.replaceState(null, "", "/");
});

describe("AdminVideoReviews", () => {
  it("lists videos, opens one, and approves an outline only once an option is chosen", async () => {
    const posts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: /AI 模型怎麼挑/ }));
    const approve = await screen.findByRole("button", { name: "用這個大綱" });
    expect(approve).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("radio", { name: /選項 B/ }));
    expect(approve).toHaveProperty("disabled", false);
    fireEvent.click(approve);
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(posts[0].url).toContain(`/admin/videos/ai-model-choice/reviews/${outline.id}/decision`);
    expect(posts[0].body).toEqual({ decision: "approve", choice: "B" });
    expect(window.location.search).toContain("video=ai-model-choice");
  });

  it("plays the preview through the admin file route and needs a reason to send a cut back", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    const { container } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "成片" });
    expect(container.querySelector("video")?.getAttribute("src")).toBe(`/api/admin-video-files/ai-model-choice/${"c".repeat(64)}`);
    const sendBack = card.querySelector("button:last-of-type") as HTMLButtonElement;
    expect(sendBack.textContent).toBe("退回");
    expect(sendBack.disabled).toBe(true);
    fireEvent.change(card.querySelector("textarea") as HTMLTextAreaElement, { target: { value: "片頭太長" } });
    expect(sendBack.disabled).toBe(false);
  });

  it("lets a reader look but not decide", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const approve = await screen.findByRole("button", { name: "核准" });
    expect(approve).toHaveProperty("disabled", true);
    expect(screen.queryByText("放棄這支影片")).toBeNull();
  });

  it("drops a video with a reason once confirmed, then shows it as dropped", async () => {
    let dropped = false;
    const posts: Array<{ url: string; body: unknown }> = [];
    const droppedFields = () => (dropped ? { dropped_at: "2026-09-25T13:00:00Z", dropped_note: "第二批做過了" } : {});
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST") {
        posts.push({ url, body: JSON.parse(String(init.body)) });
        dropped = true;
      }
      if (url.endsWith("/admin/videos")) return Promise.resolve(Response.json([{ ...summary, ...droppedFields() }]));
      const reviews = dropped ? [{ ...outline, status: "superseded" }] : [outline];
      return Promise.resolve(Response.json({ ...summary, ...droppedFields(), reviews }));
    }));
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByText("放棄這支影片", { selector: "summary" }));
    const button = screen.getByRole("button", { name: "放棄這支影片" });
    expect(button).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "放棄的原因（必填）" }), { target: { value: "第二批做過了" } });
    fireEvent.click(button);
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(confirm).toHaveBeenCalledOnce();
    expect(posts[0].url).toContain("/admin/videos/ai-model-choice/drop");
    expect(posts[0].body).toEqual({ note: "第二批做過了" });
    expect((await screen.findByRole("status")).textContent).toContain("第二批做過了");
    expect(screen.queryByText("放棄這支影片", { selector: "summary" })).toBeNull();
    confirm.mockRestore();
  });

  it("shows a character's sheets as radio cards and approves only once one is chosen", async () => {
    const look = {
      id: "33333333-3333-4333-8333-333333333333", gate: "look", subject: "jingwei", content_sha256: "d".repeat(64), summary: "精衛 的設定圖 2 張，judge 建議 B",
      payload: { subject: "jingwei", character: { name: "精衛", description: "a girl of about twelve", voice: "gemini:Kore" }, suggested: "B", options: [{ key: "A", index: 1, file_role: "candidate_a", judge: { overall: 6, problems: ["six fingers"] } }, { key: "B", index: 2, file_role: "candidate_b", judge: { overall: 9, problems: [] } }] },
      files: [{ role: "candidate_a", sha256: "e".repeat(64), size: 10, content_type: "image/png" }, { role: "candidate_b", sha256: "f".repeat(64), size: 10, content_type: "image/png" }],
      status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-26T05:00:00Z",
    };
    const board = {
      id: "44444444-4444-4444-8444-444444444444", gate: "storyboard", content_sha256: "1".repeat(64), summary: "分鏡 2 鏡，judge 最低 5/10，1 鏡待修",
      payload: { shots: [{ id: "opening", chapter: "發鳩山", prompt: "wide shot", seconds: 9.5, file_role: "shot_01", needs_review: false, judge: { overall: 8, problems: [] } }, { id: "bird", chapter: null, prompt: "close-up of a bird", seconds: 8, file_role: "shot_02", needs_review: true, judge: { overall: 5, problems: ["no bird"] } }], judge: { overall: 5, problems: ["no bird"] }, duplicates: [{ a: "opening", b: "bird", distance: 3 }] },
      files: [{ role: "shot_01", sha256: "2".repeat(64), size: 10, content_type: "image/png" }, { role: "shot_02", sha256: "3".repeat(64), size: 10, content_type: "image/png" }, { role: "contact_sheet", sha256: "4".repeat(64), size: 10, content_type: "image/png" }],
      status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-26T05:10:00Z",
    };
    const posts: Array<{ url: string; body: unknown }> = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST") {
        posts.push({ url, body: JSON.parse(String(init.body)) });
        return Promise.resolve(Response.json({ ...look, status: "approved", choice: "B" }));
      }
      if (url.endsWith("/admin/videos")) return Promise.resolve(Response.json([{ ...summary, format: "drama", media_usd: 12.5, clip_seconds: 96 }]));
      return Promise.resolve(Response.json({ ...summary, format: "drama", reviews: [look, board] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    const { container } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "角色設定圖：精衛" });
    expect(card.textContent).toContain("聲音 gemini:Kore");
    const images = [...card.querySelectorAll("img")].map((image) => image.getAttribute("src"));
    expect(images).toEqual([`/api/admin-video-files/ai-model-choice/${"e".repeat(64)}`, `/api/admin-video-files/ai-model-choice/${"f".repeat(64)}`]);
    expect(card.textContent).toContain("judge 建議");
    expect(card.textContent).toContain("judge 6/10：six fingers");
    const approve = screen.getByRole("button", { name: "用這張" });
    expect(approve).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("radio", { name: /設定圖 B/ }));
    expect(approve).toHaveProperty("disabled", false);
    fireEvent.click(approve);
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(posts[0].url).toContain(`/reviews/${look.id}/decision`);
    expect(posts[0].body).toEqual({ decision: "approve", choice: "B" });

    const storyboard = screen.getByRole("article", { name: "分鏡" });
    expect(storyboard.textContent).toContain("judge 5/10：no bird");
    expect(storyboard.textContent).toContain("相鄰鏡頭太像：opening／bird");
    expect(storyboard.textContent).toContain("沒有一次通過 judge");
    expect(storyboard.textContent).toContain("9.5 秒");
    expect(storyboard.querySelectorAll("li img").length).toBe(2);
    expect(container.querySelector("details img")?.getAttribute("src")).toBe(`/api/admin-video-files/ai-model-choice/${"4".repeat(64)}`);
    expect(screen.getByRole("button", { name: "核准分鏡" })).toHaveProperty("disabled", false);
  });

  it("queues a drama episode from the form, lists the requests and withdraws a queued one", async () => {
    const calls: Array<{ url: string; method: string; body?: unknown }> = [];
    type Row = Record<string, unknown> & { id: string; status: string; created_at: string };
    let requests: Row[] = [
      { id: "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b", premise: "精衛填海：炎帝最小的女兒在東海溺水。", title: null, source_guide: null, style_preset: "cinematic-3d", target_minutes: 3, note: "旁白慢一點", status: "queued", slug: null, created_at: "2026-09-26T05:00:00Z", started_at: null, finished_at: null, cancelled_at: null },
      { id: "7a2e3d4c-5b6a-4f7e-9b8c-0d1e2f3a4b5c", premise: "夸父逐日", title: "夸父", source_guide: "shanhaijing-kuafu", style_preset: "ink-wash", target_minutes: 2, note: null, status: "started", slug: "kuafu-chases-the-sun", created_at: "2026-09-26T04:00:00Z", started_at: "2026-09-26T04:10:00Z", finished_at: null, cancelled_at: null },
    ];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = init?.method ?? "GET";
      calls.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
      if (url.endsWith("/drama-requests") && method === "POST") {
        const body = JSON.parse(String(init?.body));
        requests = [{ ...requests[0], id: "new", premise: body.premise, style_preset: body.style_preset, target_minutes: body.target_minutes, note: null, created_at: "2026-09-26T06:00:00Z" }, ...requests];
        return Promise.resolve(Response.json(requests[0], { status: 201 }));
      }
      if (method === "DELETE") {
        requests = requests.map((request) => (url.endsWith(request.id) ? { ...request, status: "cancelled", cancelled_at: "2026-09-26T06:30:00Z" } : request));
        return Promise.resolve(Response.json(requests[0]));
      }
      if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests }));
      if (url.includes("/admin/video-automation/series")) return Promise.resolve(Response.json({ series: [] }));
      return Promise.resolve(Response.json([{ ...summary, format: "drama", pending: 1, checklist: [{ key: "brief", label: "企劃", done: true }, { key: "look", label: "角色設定圖", done: false }] }]));
    }));
    window.history.replaceState(null, "", "/?tab=drama");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const queue = await screen.findByRole("region", { name: "發起的漫劇" });
    expect(queue.textContent).toContain("排隊中");
    expect(queue.textContent).toContain("製作中");
    expect(queue.textContent).toContain("改編文章 shanhaijing-kuafu");
    expect(screen.getByRole("button", { name: "打開 kuafu-chases-the-sun" })).toBeTruthy();
    expect(screen.getByText("現在：角色設定圖")).toBeTruthy();

    fireEvent.click(screen.getByText("新的漫劇", { selector: "summary" }));
    const submit = screen.getByRole("button", { name: "排進製作" });
    expect(submit).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "故事前提（必填）" }), { target: { value: "  大禹治水  " } });
    fireEvent.change(screen.getByRole("combobox", { name: "風格" }), { target: { value: "ink-wash" } });
    fireEvent.change(screen.getByRole("spinbutton", { name: "長度（分鐘，1–8）" }), { target: { value: "2" } });
    fireEvent.change(screen.getByRole("textbox", { name: "改編站上文章（slug，選填）" }), { target: { value: "Not A Slug" } });
    expect(submit).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "改編站上文章（slug，選填）" }), { target: { value: "" } });
    expect(submit).toHaveProperty("disabled", false);
    fireEvent.click(submit);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toContain("/admin/video-automation/drama-requests");
    expect(post?.body).toEqual({ premise: "大禹治水", style_preset: "ink-wash", target_minutes: 2 });
    await waitFor(() => expect(screen.getByRole("region", { name: "發起的漫劇" }).textContent).toContain("大禹治水"));

    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    fireEvent.click(screen.getAllByRole("button", { name: "取消" })[0]);
    await waitFor(() => expect(calls.some((call) => call.method === "DELETE")).toBe(true));
    expect(calls.find((call) => call.method === "DELETE")?.url).toContain("/admin/video-automation/drama-requests/new");
    await waitFor(() => expect(screen.getByRole("region", { name: "發起的漫劇" }).textContent).toContain("已取消"));
    confirm.mockRestore();
  });

  it("keeps dramas off the tutorial list and shows a one-off drama with its spend on the drama tab", async () => {
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/admin/video-automation/series")) return Promise.resolve(Response.json({ series: [] }));
      if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests: [] }));
      return Promise.resolve(Response.json([{ ...summary, pending: 0, format: "drama", media_usd: 12.5, clip_seconds: 96 }, { ...summary, slug: "a-tutorial", title: "教學片", pending: 0 }]));
    }));
    const { unmount } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByRole("button", { name: /教學片/ });
    expect(screen.queryByRole("button", { name: /AI 模型怎麼挑/ })).toBeNull();
    unmount();
    window.history.replaceState(null, "", "/?tab=drama");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const item = await screen.findByRole("button", { name: /AI 模型怎麼挑/ });
    expect(item.textContent).toContain("AI 漫劇");
    expect(item.textContent).toContain("媒體花費 US$12.50（96 片段秒）");
  });

  it("shows a screenplay's beats, the checker's verdicts and every line with its speaker", async () => {
    const script = {
      id: "55555555-5555-4555-8555-555555555555", gate: "script", content_sha256: "9".repeat(64), summary: "劇本 3 場、12 句，約 2.5 分鐘",
      payload: {
        minutes: 2.5, beats: { hook: "鐘聲在夜裡響了", conflict: "誰敲的", turn: "鐘是自己響的", cliffhanger: { type: "reveal", text: "鐘下有字" } },
        coverage: { hook: "有", conflict: "有", turn: "弱", cliffhanger: "有" }, continuity_problems: ["轉折來得太晚"],
        characters: [{ id: "shen-lan", name: "沈瀾" }],
        scenes: [
          { id: "opening", chapter: "山門", template: "shot", prompt: "wide shot of a mountain gate at night", lines: [{ id: "a1", speaker: "narrator", name: null, text: "夜裡，鐘響了。", emotion: null }, { id: "a2", speaker: "shen-lan", name: "沈瀾", text: "誰？", emotion: "警覺" }] },
          { id: "outro", chapter: null, template: "outro", prompt: null, lines: [{ id: "a3", speaker: "narrator", name: null, text: "下集待續。", emotion: null }] },
        ],
      },
      files: [], status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-27T05:00:00Z",
    };
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json({ ...summary, format: "drama", series_slug: "wenjian", episode_number: 1, reviews: [script] }))));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "劇本" });
    expect(screen.getByText("作品 wenjian 第 1 集")).toBeTruthy();
    expect(card.textContent).toContain("鉤子有");
    expect(card.textContent).toContain("轉折弱");
    expect(card.textContent).toContain("轉折來得太晚");
    expect(card.textContent).toContain("【沈瀾】");
    expect(card.textContent).toContain("（警覺）誰？");
    expect(card.textContent).toContain("旁白：夜裡，鐘響了。");
    expect(card.textContent).toContain("鐘下有字");
    expect(screen.getByRole("button", { name: "核准劇本" })).toHaveProperty("disabled", false);
  });

  it("marks a dropped video in the list", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json([{ ...summary, pending: 0, dropped_at: "2026-09-25T13:00:00Z" }]))));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const item = await screen.findByRole("button", { name: /AI 模型怎麼挑/ });
    expect(item.textContent).toContain("已放棄");
  });

  it("shows why Jev picked an outline, and the quality check items with the failed ones first", async () => {
    const picked = {
      ...outline, status: "approved", choice: "B", decided_at: "2026-09-25T05:10:00Z",
      note: "Jev 挑了 B（0.74）：符合立場 0.81、有示範 0.92、建議 0.05，依設定自動核准",
      payload: { ...outline.payload, pick: { choice: "B", probabilities: { A: 0.26, B: 0.74 }, options: { A: { stance: 0.55, demo: 0.4 }, B: { stance: 0.81, demo: 0.92 } }, advice: 0.05 } },
    };
    const checked = {
      ...final, summary: "自動品管 2 項沒過：pace、links",
      payload: { ...final.payload, qa: { ok: false, final_sha256: "b".repeat(64), items: [
        { id: "assemble", ok: true, detail: "1800 frames" },
        { id: "pace", ok: false, detail: "slide 4 stays 21 s" },
        { id: "captions", ok: true, detail: "5 locales", warnings: ["en: 18 characters per second"] },
        { id: "links", ok: false, detail: "https://example.com/x returned 404" },
      ] } },
    };
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json({ ...summary, pending: 1, reviews: [checked, picked] }))));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const cut = await screen.findByRole("article", { name: "成片" });
    const items = [...within(cut).getByLabelText("自動品管").querySelectorAll(":scope > ul > li")].map((item) => item.textContent);
    expect(items[0]).toContain("節奏 · slide 4 stays 21 s");
    expect(items[1]).toContain("連結 · https://example.com/x returned 404");
    expect(items[2]).toContain("合成 · 1800 frames");
    expect(items[3]).toContain("字幕 · 5 locales");
    expect(items[3]).toContain("注意：en: 18 characters per second");
    expect(cut.textContent).toContain("2 項沒過");

    fireEvent.click(screen.getByText("過去的決定", { selector: "summary" }));
    const chosen = screen.getByRole("article", { name: "大綱" });
    expect(chosen.textContent).toContain("Jev 挑選");
    const table = within(chosen).getByLabelText("Jev 挑選的理由");
    const rows = [...table.querySelectorAll("tbody tr")].map((row) => row.textContent);
    expect(rows[0]).toContain("選項 A");
    expect(rows[0]).toContain("0.26");
    expect(rows[1]).toContain("選項 BJev 挑的");
    expect(rows[1]).toContain("0.74");
    expect(rows[1]).toContain("0.81");
    expect(rows[1]).toContain("0.92");
    expect(table.textContent).toContain("整份企劃給了建議0.05");
    expect(table.textContent).toContain("門檻：符合立場與有示範至少 0.6，建議至多 0.3。");
    expect(chosen.textContent).toContain("依設定自動核准");
    expect(chosen.textContent).not.toContain("有項目沒過門檻");
  });

  it("puts what needs the owner first, then what is ready to upload with its package, copy buttons and the uploaded form", async () => {
    const ready = { ...summary, slug: "upload-ready", title: "上傳包影片", stage: "done", pending: 0, publish_approved_at: "2026-09-27T05:00:00Z", last_synced_at: "2026-09-27T05:00:00Z" };
    const blocked = { ...summary, slug: "stuck-video", title: "卡住的影片", stage: "blocked", pending: 0, checklist: [{ key: "blocked", label: "卡住，需要人處理：缺金鑰", done: false }] };
    const published = { ...summary, slug: "on-youtube", title: "已上架的影片", pending: 0, youtube_video_id: "abcdefghijk", youtube_publish_at: "2026-10-01T12:00:00Z", publish_approved_at: "2026-09-20T05:00:00Z" };
    const confirmation = {
      id: "66666666-6666-4666-8666-666666666666", gate: "publish", content_sha256: "5".repeat(64), summary: "上傳包 4 項齊全",
      payload: {
        package: { ok: true, final_sha256: "5".repeat(64), items: [{ id: "files", ok: true, detail: "13 files" }, { id: "descriptions", ok: true, detail: "5 locales" }, { id: "captions", ok: true, detail: "5 locales" }, { id: "disclosure", ok: true, detail: "slides and TTS" }] },
        minutes: 9.5, chapters: 6, locales: ["zh-TW", "zh-CN", "en", "ja", "ko"],
        zh: { title: "AI 模型怎麼挑：三個問題", description: "先把帳算清楚。\n\n0:00 開場", tags: ["AI", "模型"] },
        disclosure: { synthetic: false, reason: "投影片加一般 TTS，不需要勾" },
      },
      files: [
        { role: "final", sha256: "6".repeat(64), size: 95_000_000, content_type: "video/mp4" },
        { role: "thumbnail", sha256: "7".repeat(64), size: 180_000, content_type: "image/jpeg" },
        { role: "captions_zh-TW", sha256: "8".repeat(64), size: 12_000, content_type: "text/plain" },
        { role: "captions_zh_cn", sha256: "b".repeat(64), size: 11_000, content_type: "application/x-subrip" },
        { role: "description_zh-TW", sha256: "9".repeat(64), size: 2_000, content_type: "text/plain" },
        { role: "metadata", sha256: "a".repeat(64), size: 4_000, content_type: "application/json" },
      ],
      status: "approved", choice: null, note: "上傳包 4 項齊全，依設定自動核准", decided_at: "2026-09-27T05:00:00Z", created_at: "2026-09-27T05:00:00Z",
    };
    const posts: Array<{ url: string; body: unknown }> = [];
    let linked = false;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST") {
        posts.push({ url, body: JSON.parse(String(init.body)) });
        linked = true;
        return Promise.resolve(Response.json({ ...ready, youtube_video_id: "dQw4w9WgXcQ", reviews: [confirmation] }));
      }
      const current = linked ? { ...ready, youtube_video_id: "dQw4w9WgXcQ" } : ready;
      if (url.endsWith("/admin/videos")) return Promise.resolve(Response.json([published, current, blocked, summary]));
      if (url.endsWith("/admin/videos/upload-ready")) return Promise.resolve(Response.json({ ...current, reviews: [confirmation] }));
      return Promise.resolve(Response.json({ ...summary, reviews: [] }));
    }));
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "上傳包影片" });
    expect(screen.getAllByRole("region").map((region) => region.getAttribute("aria-label"))).toEqual(["需要你", "可以上架", "已上架"]);
    const needs = screen.getByRole("region", { name: "需要你" });
    expect([...needs.querySelectorAll("button")].map((button) => button.textContent)).toEqual([expect.stringContaining("卡住的影片"), expect.stringContaining("AI 模型怎麼挑")]);
    expect(needs.textContent).toContain("卡住");
    expect(screen.getByRole("region", { name: "已上架" }).textContent).toContain("YouTube 影片 abcdefghijk");

    await waitFor(() => expect(card.textContent).toContain("9.5 分鐘"));
    expect(card.textContent).toContain("6 章");
    expect(card.textContent).toContain("5 個語系");
    const downloads = [...card.querySelectorAll("a[download]")];
    expect(downloads.map((link) => link.getAttribute("download"))).toEqual(["final.mp4", "thumbnail.jpg", "zh-TW.srt", "zh-CN.srt", "description.zh-TW.txt", "metadata.json"]);
    expect(downloads[0].getAttribute("href")).toBe(`/api/admin-video-files/upload-ready/${"6".repeat(64)}`);
    expect(downloads[0].textContent).toContain("95.0 MB");
    expect(card.textContent).toContain("不用勾");
    expect(card.textContent).toContain("投影片加一般 TTS，不需要勾");
    expect((screen.getByRole("textbox", { name: "標籤" }) as HTMLTextAreaElement).value).toBe("AI, 模型");
    fireEvent.click(screen.getByRole("button", { name: "複製 中文標題" }));
    await waitFor(() => expect(writeText).toHaveBeenCalledWith("AI 模型怎麼挑：三個問題"));
    expect(screen.getByRole("button", { name: "複製 中文標題" }).textContent).toContain("已複製");

    const form = screen.getByRole("form", { name: "已上傳到 YouTube" });
    const submit = within(form).getByRole("button", { name: "已上傳" });
    expect(submit).toHaveProperty("disabled", true);
    const address = within(form).getByRole("textbox", { name: "YouTube 網址或影片 id" });
    fireEvent.change(address, { target: { value: "https://example.com/watch?v=dQw4w9WgXcQ" } });
    expect(form.textContent).toContain("看不出影片 id");
    expect(submit).toHaveProperty("disabled", true);
    fireEvent.change(address, { target: { value: " https://youtu.be/dQw4w9WgXcQ?si=share " } });
    expect(form.textContent).toContain("影片 id：dQw4w9WgXcQ");
    expect(submit).toHaveProperty("disabled", false);
    fireEvent.change(within(form).getByLabelText("上架時間（選填）"), { target: { value: "2026-10-01T20:00" } });
    fireEvent.click(submit);
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(posts[0].url).toContain("/admin/videos/upload-ready/youtube");
    expect(posts[0].body).toEqual({ url: "https://youtu.be/dQw4w9WgXcQ?si=share", publish_at: new Date("2026-10-01T20:00").toISOString() });
    await waitFor(() => expect(screen.getByRole("region", { name: "已上架" }).textContent).toContain("上傳包影片"));
    expect(screen.queryByRole("region", { name: "可以上架" })).toBeNull();
  });

  it("selects the text for Ctrl+C when the clipboard is refused, and shows the form on a ready video's page", async () => {
    const confirmation = {
      id: "66666666-6666-4666-8666-666666666666", gate: "publish", content_sha256: "5".repeat(64), summary: "上傳包",
      payload: {
        package: { ok: true, final_sha256: "5".repeat(64), items: [{ id: "files", ok: true, detail: "13 files" }, { id: "descriptions", ok: true }, { id: "captions", ok: true }, { id: "disclosure", ok: true }] },
        zh: { title: "標題", description: "說明", tags: [] },
      },
      files: [],
      status: "approved", choice: null, note: null, decided_at: "2026-09-27T05:00:00Z", created_at: "2026-09-27T05:00:00Z",
    };
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json({ ...summary, pending: 0, publish_approved_at: "2026-09-27T05:00:00Z", reviews: [confirmation] }))));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    expect(await screen.findByRole("form", { name: "已上傳到 YouTube" })).toBeTruthy();
    const confirmed = screen.getByRole("article", { name: "上架確認" });
    expect(within(confirmed).getByLabelText("上傳包檢查").textContent).toContain("4 項全過");
    expect(within(confirmed).getByLabelText("上傳包檢查").textContent).toContain("檔案 · 13 files");
    fireEvent.click(screen.getByRole("button", { name: "複製 中文說明欄" }));
    expect((await screen.findByRole("status")).textContent).toContain("沒辦法自動複製");
    const field = screen.getByRole("textbox", { name: "中文說明欄" }) as HTMLTextAreaElement;
    expect(document.activeElement).toBe(field);
    expect([field.selectionStart, field.selectionEnd]).toEqual([0, "說明".length]);
  });

  it("tells a published video's page whether its mp4 is still in the store", async () => {
    const gone = { ...summary, pending: 0, youtube_video_id: "dQw4w9WgXcQ", youtube_publish_at: "2026-09-01T12:00:00Z", publish_approved_at: "2026-08-30T00:00:00Z", reviews: [] };
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json(gone))));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    const { unmount } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByText(/YouTube 影片 dQw4w9WgXcQ/);
    expect(screen.getByText(/YouTube 影片 dQw4w9WgXcQ/).textContent).toContain("排定");
    expect(screen.getByText(/已從審核區刪除/)).toBeTruthy();
    unmount();
    const fresh = { ...gone, youtube_publish_at: new Date(Date.now() + 86_400_000).toISOString(), publish_approved_at: new Date().toISOString() };
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json(fresh))));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByText(/YouTube 影片 dQw4w9WgXcQ/);
    expect(screen.getByText(/上架滿 7 天後從審核區刪除/)).toBeTruthy();
  });

  it("reads a video id out of every address shape and nothing else", () => {
    const id = "dQw4w9WgXcQ";
    for (const pasted of [id, `https://youtu.be/${id}?si=x`, `https://www.youtube.com/watch?t=30s&v=${id}`, `https://youtube.com/shorts/${id}`, `https://studio.youtube.com/video/${id}/edit`, `youtu.be/${id}`, `m.youtube.com/watch?v=${id}`]) {
      expect(youtubeVideoId(pasted)).toBe(id);
    }
    for (const pasted of ["", "dQw4w9WgXc", `https://example.com/watch?v=${id}`, `https://youtube.com.evil.example/watch?v=${id}`, "https://www.youtube.com/channel/UCabcdefghij", "javascript:alert(1)", "https://["]) {
      expect(youtubeVideoId(pasted)).toBeNull();
    }
  });
});
