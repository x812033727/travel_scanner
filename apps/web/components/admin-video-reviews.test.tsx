import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { BROWSE_STATES } from "./admin-video-browser";
import { VIDEO_CATEGORIES, youtubeVideoId } from "./admin-video-review-card";
import { AdminVideoReviews, REFRESH_MS } from "./admin-video-reviews";
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

// One page of the catalog under the groups (admin-video-browser.tsx), with the counts the server
// would put on the pills, worked out from the items the way the server does.
type Item = { slug: string; category?: string | null; dropped_at?: string | null; youtube_video_id?: string | null } & Record<string, unknown>;
const browseState = (item: Item) => (item.dropped_at ? "dropped" : item.youtube_video_id ? "published" : "working");
function pageOf(items: Item[], extra: Record<string, unknown> = {}) {
  return {
    items, total: items.length, page: 1, pages: items.length ? 1 : 0,
    facets: {
      category: [...VIDEO_CATEGORIES, "none"].map((code) => ({ code, count: items.filter((item) => (item.category ?? "none") === code).length })),
      state: BROWSE_STATES.map((code) => ({ code, count: items.filter((item) => browseState(item) === code).length })),
    },
    ...extra,
  };
}
/** A fetch stub that answers the catalog from `items` (read at call time) and everything else from `answer`. */
const withBrowse = (answer: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>, items: Item[] | (() => Item[]) = []) =>
  vi.fn((input: RequestInfo | URL, init?: RequestInit) => (String(input).includes("/admin/videos/browse")
    ? Promise.resolve(Response.json(pageOf(typeof items === "function" ? items() : items)))
    : answer(input, init)));
const tableRows = (table: HTMLElement) => [...table.querySelectorAll("tbody tr")].map((row) => row.textContent ?? "");

function stubFetch() {
  const posts: Array<{ url: string; method: string; body: unknown }> = [];
  let category: string | null = null;
  const fetchMock = withBrowse((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (init?.method === "POST" || init?.method === "PUT") {
      const body = JSON.parse(String(init.body)) as Record<string, unknown>;
      posts.push({ url, method: init.method, body });
      if (init.method === "PUT") {
        if (url.endsWith("/category")) category = body.category as string | null;
        return Promise.resolve(Response.json({ ...summary, category, reviews: [outline, final] }));
      }
      return Promise.resolve(Response.json({ ...outline, status: "approved" }));
    }
    const body = url.endsWith("/admin/videos?shorts=exclude") ? [summary] : { ...summary, category, reviews: [outline, final] };
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
    // Only a drama's script gate has a discussion; a tutorial's outline and final cut have none.
    expect(within(card).queryByRole("region", { name: "討論" })).toBeNull();
    expect(within(screen.getByRole("article", { name: "大綱" })).queryByRole("region", { name: "討論" })).toBeNull();
  });

  it("lets a reader look but not decide", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const approve = await screen.findByRole("button", { name: "核准" });
    expect(approve).toHaveProperty("disabled", true);
    expect(screen.queryByText("放棄這支影片")).toBeNull();
  });

  it("lets a content manager request one retry for a blocked video", async () => {
    const blocked = { ...summary, stage: "blocked", pending: 0, checklist: [{ key: "blocked", label: "卡住，需要人處理：writer failed twice", done: false }] };
    const request = "2b06f60f-1026-477a-9d40-28683b00a22e";
    let pending = false;
    const posts: string[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST") { posts.push(url); pending = true; }
      const value = { ...blocked, retry_request_id: pending ? request : null, retry_acknowledged_id: null };
      return Promise.resolve(Response.json(url.endsWith("/admin/videos?shorts=exclude") ? [value] : { ...value, reviews: [] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: "重試這支影片" }));
    await waitFor(() => expect(posts).toEqual([expect.stringContaining("/admin/videos/ai-model-choice/retry")]));
    expect(await screen.findByText("已提出重試，工人下一輪會接手。")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "重試這支影片" })).toBeNull();
  });

  it("shows a blocked video's reason to a reader without the retry action", async () => {
    const blocked = { ...summary, stage: "blocked", pending: 0, checklist: [{ key: "blocked", label: "卡住，需要人處理：缺金鑰", done: false }] };
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => Promise.resolve(Response.json(String(input).endsWith("/admin/videos?shorts=exclude") ? [blocked] : { ...blocked, reviews: [] }))));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    expect(await screen.findByText("卡住，需要人處理：缺金鑰")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "重試這支影片" })).toBeNull();
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
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json([{ ...summary, ...droppedFields() }]));
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
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json([{ ...summary, format: "drama", media_usd: 12.5, clip_seconds: 96 }]));
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
      return Promise.resolve(Response.json([]));
    }));
    window.history.replaceState(null, "", "/?tab=drama");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    // Requests from before one-offs were series (no series_slug) still show as a queue.
    const queue = await screen.findByRole("region", { name: "發起的漫劇" });
    expect(queue.textContent).toContain("排隊中");
    expect(queue.textContent).toContain("製作中");
    expect(queue.textContent).toContain("改編文章 shanhaijing-kuafu");
    expect(screen.getByRole("button", { name: "打開 kuafu-chases-the-sun" })).toBeTruthy();

    fireEvent.click(screen.getByText("新的漫劇", { selector: "summary" }));
    const submit = screen.getByRole("button", { name: "排進製作" });
    expect(submit).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "故事前提（必填）" }), { target: { value: "  大禹治水  " } });
    expect(screen.getByRole("option", { name: "扁平插畫解說" })).toHaveProperty("value", "flat-explainer");
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

  it("shows a languages batch with each part's state and file and the Studio steps, and approves it as uploaded", async () => {
    // The payload and files are what the worker sends (docs/videos/LANGUAGES.md): a state per part
    // per language, the worker's reason when it gave one up, and a file per finished part.
    const languages = {
      id: "55555555-5555-4555-8555-555555555555", gate: "languages", content_sha256: "7".repeat(64), summary: "語言：en 三項完成、ja 配音跳過",
      payload: { locales: { ja: { metadata: "ready", captions: "ready", dub: { status: "skipped", reason: "1.15 倍還塞不下" } }, en: { metadata: "ready", captions: "ready", dub: "ready" } } },
      files: [
        { role: "description_en", sha256: "8".repeat(64), size: 10, content_type: "text/plain" },
        { role: "captions_en", sha256: "9".repeat(64), size: 10, content_type: "application/x-subrip" },
        { role: "dub_en", sha256: "1".repeat(64), size: 10, content_type: "audio/mp4" },
        { role: "description_ja", sha256: "2".repeat(64), size: 10, content_type: "text/plain" },
        { role: "captions_ja", sha256: "3".repeat(64), size: 10, content_type: "application/x-subrip" },
      ],
      status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-27T05:00:00Z",
    };
    const posts: Array<{ url: string; body: unknown }> = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST") {
        posts.push({ url, body: JSON.parse(String(init.body)) });
        return Promise.resolve(Response.json({ ...languages, status: "approved" }));
      }
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json([summary]));
      return Promise.resolve(Response.json({ ...summary, ready_to_upload: false, locales_decided_at: "2026-09-27T04:30:00Z", locales: { en: { metadata: true, captions: true, dub: true }, ja: { metadata: true, captions: true, dub: true } }, reviews: [languages] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "語言" });
    expect(card.textContent).toContain("語言：en 三項完成、ja 配音跳過");
    // English first whatever the payload's order, every part with its state and its file.
    const rows = [...card.querySelectorAll("li")].map((row) => row.textContent);
    expect(rows[0]).toContain("英文");
    expect(rows[0]).toContain("配音已完成");
    expect(rows[1]).toContain("日文");
    expect(rows[1]).toContain("配音跳過（1.15 倍還塞不下）");
    expect(within(card).getByRole("link", { name: "下載 en.m4a" }).getAttribute("href")).toContain(`/api/admin-video-files/${summary.slug}/${"1".repeat(64)}`);
    expect(within(card).getByRole("link", { name: "下載 description.en.txt" }).getAttribute("href")).toContain("8".repeat(64));
    expect(within(card).getByRole("link", { name: "下載 ja.srt" }).getAttribute("href")).toContain("3".repeat(64));
    expect(within(card).queryByRole("link", { name: "下載 ja.m4a" })).toBeNull();
    // A dub track is the one part only the owner can upload, so the Studio steps are there.
    expect(card.textContent).toContain("配音要在 Studio 上傳");
    expect(card.textContent).toContain("「新增語言」");
    const approve = screen.getByRole("button", { name: "已在 Studio 上傳配音" });
    expect(approve).toHaveProperty("disabled", false);
    fireEvent.click(approve);
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(posts[0].url).toContain(`/reviews/${languages.id}/decision`);
    expect(posts[0].body).toEqual({ decision: "approve" });
  });

  it("still reads a dubs review from before the languages gate", async () => {
    const dubs = {
      id: "55555555-5555-4555-8555-555555555555", gate: "dubs", content_sha256: "7".repeat(64), summary: "配音：en 完成、ja 跳過",
      payload: { locales: { en: { file: "en.m4a", file_role: "dub_en", status: "ready" }, ja: { status: "skipped", reason: "1.15 倍還塞不下" } } },
      files: [{ role: "dub_en", sha256: "8".repeat(64), size: 10, content_type: "audio/mp4" }],
      status: "approved", choice: null, note: null, decided_at: "2026-09-27T06:00:00Z", created_at: "2026-09-27T05:00:00Z",
    };
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json([summary]));
      return Promise.resolve(Response.json({ ...summary, pending: 0, reviews: [dubs] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByText("過去的決定", { selector: "summary" }));
    const card = screen.getByRole("article", { name: "配音音軌" });
    expect(within(card).getByRole("link", { name: "下載 en.m4a" }).getAttribute("href")).toContain("8".repeat(64));
    expect(card.textContent).toContain("英文配音已完成");
    expect(card.textContent).toContain("日文配音跳過（1.15 倍還塞不下）");
  });

  it("lets the owner choose each language's parts after the final cut, ticks the captions with a dub, and saves in the page's order", async () => {
    const puts: Array<{ url: string; body: unknown }> = [];
    let locales: Record<string, unknown> = { en: { metadata: true, captions: true, dub: false } };
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "PUT") {
        const body = JSON.parse(String(init.body)) as { locales: Record<string, unknown> };
        puts.push({ url, body });
        locales = body.locales;
        return Promise.resolve(Response.json({ ...summary, locales, reviews: [] }));
      }
      if (url.includes("/admin/video-automation/settings")) return Promise.resolve(Response.json({ caption_locales: ["ja", "zh-CN"], drama: { drama_caption_locales: ["en"] } }));
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json([summary]));
      return Promise.resolve(Response.json({
        ...summary, ready_to_upload: false, locales, locales_decided_at: "2026-09-27T04:30:00Z",
        languages: { en: { metadata: { state: "ready" }, captions: { state: "working" } } }, reviews: [{ ...final, status: "approved", decided_at: "2026-09-27T04:00:00Z" }],
      }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const panel = await screen.findByRole("region", { name: "這支影片的語言" });
    const box = (name: string) => within(panel).getByRole("checkbox", { name }) as HTMLInputElement;
    expect(box("英文 標題與說明").checked).toBe(true);
    expect(box("英文 CC 字幕").checked).toBe(true);
    expect(box("英文 配音").checked).toBe(false);
    expect(box("韓文 配音").disabled).toBe(false);
    // Where the saved parts stand, next to their boxes; the unsaved dub has no state yet.
    const cells = [...panel.querySelectorAll("tbody tr")][0].textContent;
    expect(cells).toContain("已完成");
    expect(cells).toContain("製作中");
    const save = within(panel).getByRole("button", { name: "儲存" });
    expect(save).toHaveProperty("disabled", true);
    fireEvent.click(box("韓文 配音"));
    expect(box("韓文 CC 字幕").checked).toBe(true);
    fireEvent.click(box("英文 CC 字幕"));
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0].url).toContain("/admin/videos/ai-model-choice/languages");
    expect(puts[0].body).toEqual({ locales: { en: { metadata: true, captions: false, dub: false }, ko: { metadata: false, captions: true, dub: true } } });
    expect((await within(panel).findByRole("status")).textContent).toBe("已儲存");
    await waitFor(() => expect(box("韓文 配音").checked).toBe(true));
    expect(save).toHaveProperty("disabled", true);

    fireEvent.click(within(panel).getByRole("button", { name: "照預設勾選" }));
    await waitFor(() => expect(box("日文 CC 字幕").checked).toBe(true));
    expect(box("日文 標題與說明").checked).toBe(true);
    expect(box("簡體中文 CC 字幕").checked).toBe(true);
    expect(box("英文 標題與說明").checked).toBe(false);
    expect(box("韓文 配音").checked).toBe(false);
    expect(save).toHaveProperty("disabled", false);

    fireEvent.click(within(panel).getByRole("button", { name: "只出繁體中文" }));
    await waitFor(() => expect(puts).toHaveLength(2));
    expect(puts[1].body).toEqual({ locales: {} });
    await waitFor(() => expect(box("日文 CC 字幕").checked).toBe(false));
    expect(within(panel).getByRole("button", { name: "只出繁體中文" })).toHaveProperty("disabled", true);
  });

  it("waits for the final cut before offering languages, greys out a drama's dub, and lets a reader only look", async () => {
    const detail = (fields: Record<string, unknown>) => vi.fn((input: RequestInfo | URL) => Promise.resolve(Response.json(String(input).endsWith("/admin/videos?shorts=exclude") ? [summary] : { ...summary, ready_to_upload: false, ...fields })));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    vi.stubGlobal("fetch", detail({ reviews: [outline] }));
    const first = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const early = await screen.findByRole("region", { name: "這支影片的語言" });
    expect(early.textContent).toContain("成片核准後可以選語言");
    expect(within(early).queryAllByRole("checkbox")).toHaveLength(0);
    expect(screen.queryByText("等你決定語言")).toBeNull();
    first.unmount();

    vi.stubGlobal("fetch", detail({ format: "drama", pending: 0, locales_decided_at: null, reviews: [{ ...final, status: "approved", decided_at: "2026-09-27T04:00:00Z" }] }));
    const second = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const drama = await screen.findByRole("region", { name: "這支影片的語言" });
    expect(within(drama).getByRole("checkbox", { name: "英文 配音" })).toHaveProperty("disabled", true);
    expect(within(drama).getByRole("checkbox", { name: "英文 CC 字幕" })).toHaveProperty("disabled", false);
    // Nothing decided yet: the page says so, and saving nothing is a decision too.
    expect(screen.getByText("等你決定語言")).toBeTruthy();
    expect(within(drama).getByRole("button", { name: "儲存" })).toHaveProperty("disabled", false);
    second.unmount();

    vi.stubGlobal("fetch", detail({ pending: 0, locales_decided_at: null, reviews: [{ ...final, status: "approved", decided_at: "2026-09-27T04:00:00Z" }] }));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const reader = await screen.findByRole("region", { name: "這支影片的語言" });
    expect(within(reader).getByRole("checkbox", { name: "日文 配音" })).toHaveProperty("disabled", true);
    for (const name of ["照預設勾選", "只出繁體中文", "儲存"]) expect(within(reader).getByRole("button", { name })).toHaveProperty("disabled", true);
  });

  it("tells each finished video where it is on its way to YouTube, and lists one waiting for its languages under needs you", async () => {
    const done = { key: "final_video_approved", label: "成片核准", done: true };
    const base = { ...summary, pending: 0, checklist: [done], ready_to_upload: false, locales: {}, locales_decided_at: null, languages: {} };
    const deciding = { ...base, slug: "pick-languages", title: "等語言的影片", stage: "languages" };
    const making = {
      ...base, slug: "making-languages", title: "做語言的影片", publish_approved_at: "2026-09-27T05:00:00Z", locales_decided_at: "2026-09-27T04:30:00Z",
      locales: { en: { metadata: true, captions: true, dub: true } }, languages: { en: { metadata: { state: "ready" }, captions: { state: "ready" }, dub: { state: "working" } } },
    };
    const ready = { ...base, slug: "upload-ready", title: "可上架的影片", publish_approved_at: "2026-09-27T05:00:00Z", locales_decided_at: "2026-09-27T04:30:00Z", ready_to_upload: true };
    const scheduled = { ...base, slug: "scheduled-video", title: "排定的影片", youtube_video_id: "abcdefghijk", youtube_publish_at: "2999-01-01T00:00:00Z", publish_approved_at: "2026-09-27T05:00:00Z" };
    const published = { ...base, slug: "public-video", title: "公開的影片", youtube_video_id: "abcdefghijl", youtube_publish_at: "2026-09-01T00:00:00Z", publish_approved_at: "2026-08-27T05:00:00Z" };
    const all = [deciding, making, ready, scheduled, published];
    vi.stubGlobal("fetch", withBrowse((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json(all));
      const project = all.find((each) => url.endsWith(`/admin/videos/${each.slug}`)) ?? making;
      return Promise.resolve(Response.json({ ...project, reviews: [] }));
    }, all));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByRole("article", { name: "可上架的影片" });
    // The two groups that wait for the owner, then the catalog of every tutorial.
    expect(screen.getAllByRole("region").map((region) => region.getAttribute("aria-label"))).toEqual(["需要你", "可以上架", "全部影片"]);
    const needs = screen.getByRole("region", { name: "需要你" });
    expect(needs.textContent).toContain("等語言的影片");
    expect(needs.textContent).toContain("等你決定語言");
    const rows = tableRows(await screen.findByRole("table", { name: "全部影片" }));
    expect(rows).toHaveLength(5);
    const rowOf = (title: string) => rows.find((row) => row.includes(title)) ?? "";
    expect(rowOf("等語言的影片")).toContain("等你決定語言");
    expect(rowOf("做語言的影片")).toContain("語言製作中");
    expect(rowOf("可上架的影片")).toContain("可以上架");
    expect(rowOf("排定的影片")).toContain("已排定");
    expect(rowOf("公開的影片")).toContain("已上架");
    expect(rowOf("公開的影片")).toContain("YouTube 影片 abcdefghijl");

    fireEvent.click(screen.getByRole("button", { name: /做語言的影片/ }));
    await screen.findByRole("heading", { name: "做語言的影片" });
    expect(screen.getByText("語言製作中")).toBeTruthy();
    expect(screen.getByText("語言做好後才能送到 YouTube，那時上傳包裡才有這些語言。")).toBeTruthy();
    // The site sends the video from the upload package, languages included, so nothing goes to YouTube before they are made.
    expect(screen.queryByRole("form", { name: "已上傳到 YouTube" })).toBeNull();
    const panel = screen.getByRole("region", { name: "這支影片的語言" });
    const row = [...panel.querySelectorAll("tbody tr")][0].textContent ?? "";
    expect(row.match(/已完成/g)).toHaveLength(2);
    expect(row).toContain("製作中");
  });

  it("keeps dramas out of the needs-you group but lists them in the catalog, and shows a one-off drama as a one-episode series on the drama tab", async () => {
    const oneOff = {
      id: "7c2e3d4f-5a6b-4c7d-8e9f-0a1b2c3d4e5f", slug: "one-off-1a2b3c4d", kind: "one-off", title: "精衛填海", premise: "炎帝最小的女兒在東海溺水。", aspects: [], tone: "no-romance", style_preset: "ink-wash",
      target_minutes: 2, planned_episodes: 1, episodes_per_chapter: 1, chapters: 1, open_ended: false, status: "setting", note: null, requested_chapter: null, force_next: false,
      episodes_done: 0, episodes_started: 0, episodes_ready: 0, docs_pending: 1, messages_pending: 0, media_usd: 12.5, clip_seconds: 96, created_at: "2026-09-27T00:00:00Z", updated_at: "2026-09-27T01:00:00Z",
    };
    const tutorial = { ...summary, slug: "a-tutorial", title: "教學片", pending: 0 };
    const episode = { ...summary, pending: 0, format: "drama", category: "drama", series_slug: "one-off-1a2b3c4d", episode_number: 1, media_usd: 12.5, clip_seconds: 96 };
    vi.stubGlobal("fetch", withBrowse((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/admin/video-automation/series?kind=one-off")) return Promise.resolve(Response.json({ series: [oneOff] }));
      if (url.includes("/admin/video-automation/series")) return Promise.resolve(Response.json({ series: [] }));
      if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests: [] }));
      return Promise.resolve(Response.json([{ ...episode, pending: 2 }, tutorial]));
    }, [episode, tutorial]));
    const { unmount } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByRole("button", { name: /教學片/ });
    // The drama waits for the owner on the drama tab, not in the tutorials' needs-you group; the catalog records it.
    expect(screen.queryByRole("region", { name: "需要你" })).toBeNull();
    const rows = tableRows(screen.getByRole("table", { name: "全部影片" }));
    expect(rows).toHaveLength(2);
    expect(rows.find((row) => row.includes("AI 模型怎麼挑"))).toContain("漫劇");
    expect(rows.find((row) => row.includes("AI 模型怎麼挑"))).toContain("作品 one-off-1a2b3c4d 第 1 集");
    unmount();
    window.history.replaceState(null, "", "/?tab=drama");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const item = await screen.findByRole("button", { name: /精衛填海/ });
    expect(screen.getByRole("region", { name: "單集漫劇" }).contains(item)).toBe(true);
    expect(item.textContent).toContain("單集");
    expect(item.textContent).toContain("1 份等你核准");
    expect(item.textContent).toContain("US$12.50 · 片段 96 秒");
    expect(item.textContent).toContain("水墨");
    fireEvent.click(item);
    expect(window.location.search).toContain("series=one-off-1a2b3c4d");
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
    const said = [
      { id: "m1", subject: "script:1", author: "owner", body_md: "鐘聲太早。", refers_to: "9".repeat(12), answered_at: "2026-09-27T05:10:00Z", created_at: "2026-09-27T05:05:00Z", created_by_user_id: "u1" },
      { id: "m2", subject: "script:1", author: "writer", body_md: "移到沈瀾開口之後了。", refers_to: "9".repeat(12), answered_at: "2026-09-27T05:10:00Z", created_at: "2026-09-27T05:10:00Z", created_by_user_id: null },
    ];
    const calls: Array<{ url: string; method: string; body?: unknown }> = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = init?.method ?? "GET";
      calls.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
      if (url.endsWith("/messages") && method === "POST") return Promise.resolve(Response.json({ ...said[0], id: "m3", answered_at: null }, { status: 201 }));
      if (url.includes("/messages?subject=")) return Promise.resolve(Response.json({ messages: said }));
      return Promise.resolve(Response.json({ ...summary, format: "drama", series_slug: "wenjian", episode_number: 1, reviews: [script] }));
    }));
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
    // The episode's thread on its series, read by the subject script:<episode>, sits in the card.
    const thread = within(card).getByRole("region", { name: "討論" });
    await waitFor(() => expect(thread.textContent).toContain("移到沈瀾開口之後了。"));
    expect(calls.some((call) => call.url.endsWith("/admin/video-automation/series/wenjian/messages?subject=script%3A1"))).toBe(true);
    expect(thread.textContent).toContain("撰稿");
    expect(thread.textContent).toContain(`對劇本 ${"9".repeat(12)}`);
    fireEvent.change(within(thread).getByRole("textbox", { name: "給模型的話" }), { target: { value: "結尾多一句旁白" } });
    fireEvent.click(within(thread).getByRole("button", { name: "送出" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toContain("/admin/video-automation/series/wenjian/messages");
    expect(post?.body).toEqual({ subject: "script:1", body: "結尾多一句旁白" });
    // The gate card's own note is still the one the decision reads.
    expect(within(card).getByRole("textbox", { name: "意見（退回時必填）" })).toBeTruthy();
  });

  it("shows a one-off episode's story bible with its thread above the gates, and approves it on its series", async () => {
    const script = {
      id: "55555555-5555-4555-8555-555555555555", gate: "script", content_sha256: "9".repeat(64), summary: "劇本 1 場", payload: { minutes: 2, scenes: [] },
      files: [], status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-27T05:00:00Z",
    };
    const bible = { id: "b1", kind: "bible", chapter_number: 0, version: 1, body_md: "# 故事聖經\n精衛。", body_json: {}, status: "review", note: null, decided_at: null, created_at: "2026-09-27T02:00:00Z", unanswered: 1 };
    const series = {
      id: "7c2e3d4f-5a6b-4c7d-8e9f-0a1b2c3d4e5f", slug: "one-off-1a2b3c4d", kind: "one-off", title: "精衛填海", premise: "炎帝最小的女兒在東海溺水。", aspects: [], tone: "no-romance", style_preset: "ink-wash",
      target_minutes: 2, planned_episodes: 1, episodes_per_chapter: 1, chapters: 1, open_ended: false, status: "setting", note: null, requested_chapter: null, force_next: false,
      episodes_done: 0, episodes_started: 1, episodes_ready: 0, docs_pending: 1, messages_pending: 1, media_usd: 0, clip_seconds: 0, created_at: "2026-09-27T00:00:00Z", updated_at: "2026-09-27T01:00:00Z",
      docs: [bible], episodes: [],
    };
    const line = { id: "m1", subject: "bible", author: "owner", body_md: "第二幕為什麼要死一個人？", refers_to: "v1", answered_at: null, created_at: "2026-09-27T02:30:00Z", created_by_user_id: "u1" };
    const calls: Array<{ url: string; method: string; body?: unknown }> = [];
    let approved = false;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = init?.method ?? "GET";
      calls.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : undefined });
      if (method === "POST") { approved = true; return Promise.resolve(Response.json({ ...bible, status: "approved", decided_at: "2026-09-27T06:00:00Z" })); }
      if (url.includes("/messages?subject=bible")) return Promise.resolve(Response.json({ messages: [line] }));
      if (url.includes("/messages?subject=")) return Promise.resolve(Response.json({ messages: [] }));
      if (url.endsWith("/admin/video-automation/series/one-off-1a2b3c4d")) return Promise.resolve(Response.json({ ...series, docs: [{ ...bible, status: approved ? "approved" : "review" }] }));
      return Promise.resolve(Response.json({ ...summary, title: "精衛填海", format: "drama", series_slug: "one-off-1a2b3c4d", episode_number: 1, reviews: [script] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "劇本" });
    const panel = (await screen.findByText("故事聖經")).closest("details") as HTMLElement;
    // The bible comes first on the page, the gate cards after it.
    expect(panel.compareDocumentPosition(card) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(panel.textContent).toContain("等你決定");
    expect(panel.textContent).toContain("第 1 版");
    const thread = within(panel).getByRole("region", { name: "討論" });
    await waitFor(() => expect(thread.textContent).toContain("第二幕為什麼要死一個人？"));
    // The panel's summary pill (from the server's count), the thread header's, and the unanswered line's.
    expect(within(panel).getAllByText("等模型回覆")).toHaveLength(3);
    expect(within(panel).getByRole("textbox", { name: "給模型的話" })).toBeTruthy();
    // The script card's thread is the episode's own subject.
    expect(calls.some((call) => call.url.endsWith("/series/one-off-1a2b3c4d/messages?subject=script%3A1"))).toBe(true);

    fireEvent.click(within(panel).getByRole("button", { name: "核准" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const postIndex = calls.findIndex((call) => call.method === "POST");
    const post = calls[postIndex];
    expect(post?.url).toContain("/admin/video-automation/series/one-off-1a2b3c4d/docs/bible/decision");
    // The decision names the version the owner read, so the site can refuse one given on an older version.
    expect(post?.body).toEqual({ decision: "approve", expected_version: 1 });
    // The panel reads its series again and shows the approved bible, whose thread stays as a record;
    // the video page reloads too, so the episode's gates follow the approval.
    await waitFor(() => expect(within(panel.querySelector("summary") as HTMLElement).getByText("已核准")).toBeTruthy());
    await waitFor(() => expect(within(panel).getByRole("region", { name: "討論" }).textContent).toContain("只留紀錄"));
    expect(within(panel).queryByRole("textbox", { name: "給模型的話" })).toBeNull();
    expect(within(panel).queryByRole("button", { name: "核准" })).toBeNull();
    expect(calls.slice(postIndex + 1).some((call) => call.method === "GET" && call.url.endsWith("/admin/videos/ai-model-choice"))).toBe(true);
  });

  it("knows a one-off by its series' kind, so an owner-named one-off gets its bible on the episode page too", async () => {
    const script = {
      id: "55555555-5555-4555-8555-555555555555", gate: "script", content_sha256: "9".repeat(64), summary: "劇本 1 場", payload: { minutes: 2, scenes: [] },
      files: [], status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-27T05:00:00Z",
    };
    const bible = { id: "b1", kind: "bible", chapter_number: 0, version: 1, body_md: "# 故事聖經\n精衛。", body_json: {}, status: "review", note: null, decided_at: null, created_at: "2026-09-27T02:00:00Z", unanswered: 0 };
    const series = {
      id: "7c2e3d4f-5a6b-4c7d-8e9f-0a1b2c3d4e5f", slug: "jingwei", kind: "one-off", title: "精衛填海", premise: "炎帝最小的女兒在東海溺水。", aspects: [], tone: "no-romance", style_preset: "ink-wash",
      target_minutes: 2, planned_episodes: 1, episodes_per_chapter: 1, chapters: 1, open_ended: false, status: "setting", note: null, requested_chapter: null, force_next: false,
      episodes_done: 0, episodes_started: 1, episodes_ready: 0, docs_pending: 1, messages_pending: 0, media_usd: 0, clip_seconds: 0, created_at: "2026-09-27T00:00:00Z", updated_at: "2026-09-27T01:00:00Z",
      episodes: [],
    };
    let written = true;
    const calls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      calls.push(url);
      if (url.includes("/messages?subject=")) return Promise.resolve(Response.json({ messages: [] }));
      if (url.endsWith("/admin/video-automation/series/jingwei")) return Promise.resolve(Response.json({ ...series, docs: written ? [bible] : [] }));
      return Promise.resolve(Response.json({ ...summary, title: "精衛填海", format: "drama", series_slug: "jingwei", episode_number: 1, reviews: [script] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    const first = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "劇本" });
    const panel = (await screen.findByText("故事聖經")).closest("details") as HTMLElement;
    expect(panel.compareDocumentPosition(card) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(panel.textContent).toContain("等你決定");
    expect(within(panel).getByRole("button", { name: "核准" })).toBeTruthy();
    expect(calls.some((url) => url.endsWith("/admin/video-automation/series/jingwei"))).toBe(true);
    first.unmount();

    // Before the worker has written the bible, the page says so instead of showing nothing.
    written = false;
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByRole("article", { name: "劇本" });
    expect(await screen.findByText("工人下一輪會寫故事聖經。")).toBeTruthy();
    expect(screen.queryByText("故事聖經")).toBeNull();
  });

  it("reads a long series or a brand story once for the episode page, and keeps refreshing a one-off's bible", async () => {
    const bible = { id: "b1", kind: "bible", chapter_number: 0, version: 1, body_md: "# 故事聖經\n精衛。", body_json: {}, status: "review", note: null, decided_at: null, created_at: "2026-09-27T02:00:00Z", unanswered: 0 };
    const setting = { ...bible, id: "s1", kind: "setting", body_md: "# 設定集", status: "approved" };
    const base = {
      id: "7c2e3d4f-5a6b-4c7d-8e9f-0a1b2c3d4e5f", title: "作品", premise: "前提", aspects: [], tone: "no-romance", style_preset: "ink-wash",
      target_minutes: 2, planned_episodes: 100, episodes_per_chapter: 10, chapters: 10, open_ended: false, status: "running", note: null, requested_chapter: null, force_next: false,
      episodes_done: 0, episodes_started: 1, episodes_ready: 0, docs_pending: 0, messages_pending: 0, media_usd: 0, clip_seconds: 0, created_at: "2026-09-27T00:00:00Z", updated_at: "2026-09-27T01:00:00Z",
      episodes: [],
    };
    // A long drama, a brand story, and a response from an API without the kind (no bible, so not a one-off).
    const long = [
      { slug: "long-drama", series: { ...base, slug: "long-drama", kind: "series", docs: [setting] } },
      { slug: "brand-story", series: { ...base, slug: "brand-story", kind: "story", docs: [] } },
      { slug: "old-api", series: { ...base, slug: "old-api", docs: [setting] } },
    ];
    const oneOff = { slug: "jingwei", series: { ...base, slug: "jingwei", kind: "one-off", planned_episodes: 1, status: "setting", docs: [bible] } };
    vi.useFakeTimers({ shouldAdvanceTime: true });
    try {
      for (const { slug, series } of [...long, oneOff]) {
        const calls: string[] = [];
        vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
          const url = String(input);
          calls.push(url);
          if (url.includes("/messages?subject=")) return Promise.resolve(Response.json({ messages: [] }));
          if (url.endsWith(`/admin/video-automation/series/${slug}`)) return Promise.resolve(Response.json(series));
          return Promise.resolve(Response.json({ ...summary, format: "drama", series_slug: slug, episode_number: 1, reviews: [] }));
        }));
        window.history.replaceState(null, "", "/?video=ai-model-choice");
        const view = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
        await screen.findByText(`作品 ${slug} 第 1 集`);
        const seriesReads = () => calls.filter((url) => url.endsWith(`/admin/video-automation/series/${slug}`)).length;
        await waitFor(() => expect(seriesReads()).toBe(1));
        const pageReads = () => calls.filter((url) => url.endsWith("/admin/videos/ai-model-choice")).length;
        const pageBefore = pageReads();
        await act(async () => { await vi.advanceTimersByTimeAsync(REFRESH_MS * 3 + 100); });
        // The video page itself keeps refreshing every minute either way.
        expect(pageReads()).toBeGreaterThanOrEqual(pageBefore + 3);
        if (slug === oneOff.slug) {
          // The one-off's bible is still read every minute, so the worker's new version and its thread show up.
          expect(seriesReads()).toBe(4);
          expect(screen.getByText("故事聖經")).toBeTruthy();
        } else {
          expect(seriesReads()).toBe(1);
          expect(screen.queryByText("故事聖經")).toBeNull();
          expect(screen.queryByText("工人下一輪會寫故事聖經。")).toBeNull();
        }
        view.unmount();
      }
    } finally {
      vi.useRealTimers();
    }
  });

  it("keeps an approved screenplay's thread as a record in the history, and gives a rejected one none", async () => {
    const base = { gate: "script", content_sha256: "9".repeat(64), summary: "劇本 1 場", payload: { minutes: 2, scenes: [] }, files: [], choice: null, created_at: "2026-09-27T05:00:00Z" };
    const approved = { ...base, id: "55555555-5555-4555-8555-555555555555", status: "approved", note: null, decided_at: "2026-09-27T06:00:00Z" };
    const rejected = { ...base, id: "66666666-6666-4666-8666-666666666666", content_sha256: "8".repeat(64), status: "rejected", note: "太短", decided_at: "2026-09-27T05:30:00Z", created_at: "2026-09-27T04:00:00Z" };
    const said = [
      { id: "m1", subject: "script:1", author: "owner", body_md: "鐘聲太早。", refers_to: "9".repeat(12), answered_at: "2026-09-27T05:10:00Z", created_at: "2026-09-27T05:05:00Z", created_by_user_id: "u1" },
      { id: "m2", subject: "script:1", author: "writer", body_md: "移到沈瀾開口之後了。", refers_to: "9".repeat(12), answered_at: "2026-09-27T05:10:00Z", created_at: "2026-09-27T05:10:00Z", created_by_user_id: null },
    ];
    const calls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      calls.push(url);
      if (url.includes("/messages?subject=")) return Promise.resolve(Response.json({ messages: said }));
      return Promise.resolve(Response.json({ ...summary, pending: 1, format: "drama", series_slug: "wenjian", episode_number: 1, reviews: [outline, approved, rejected] }));
    }));
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const live = await screen.findByRole("article", { name: "大綱" });
    expect(within(live).queryByRole("region", { name: "討論" })).toBeNull();
    fireEvent.click(screen.getByText("過去的決定", { selector: "summary" }));
    const scripts = screen.getAllByRole("article", { name: "劇本" });
    expect(scripts).toHaveLength(2);
    const record = scripts.find((card) => card.textContent?.includes("已核准")) as HTMLElement;
    const sentBack = scripts.find((card) => card.textContent?.includes("已退回")) as HTMLElement;
    // The approved screenplay keeps its lines as a record without an input, even for a manager.
    const thread = await within(record).findByRole("region", { name: "討論" });
    await waitFor(() => expect(thread.textContent).toContain("移到沈瀾開口之後了。"));
    expect(thread.textContent).toContain("只留紀錄");
    expect(within(record).queryByRole("textbox", { name: "給模型的話" })).toBeNull();
    expect(within(record).queryByRole("button", { name: "送出" })).toBeNull();
    // The rejected one is superseded by a rewrite the worker discusses on the same subject; it shows no thread.
    expect(within(sentBack).queryByRole("region", { name: "討論" })).toBeNull();
    expect(calls.filter((url) => url.includes("/messages?subject="))).toHaveLength(1);
  });

  it("marks a dropped video in the catalog, and a video nobody filed as uncategorized", async () => {
    const dropped = { ...summary, pending: 0, dropped_at: "2026-09-25T13:00:00Z" };
    vi.stubGlobal("fetch", withBrowse(() => Promise.resolve(Response.json([dropped])), [dropped]));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const item = await screen.findByRole("button", { name: "AI 模型怎麼挑" });
    const row = item.closest("tr")?.textContent ?? "";
    expect(row).toContain("已放棄");
    expect(row).toContain("未分類");
    expect(row).toContain("尚未上架");
    expect(screen.queryByRole("region", { name: "需要你" })).toBeNull();
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
    const listed = () => [published, linked ? { ...ready, youtube_video_id: "dQw4w9WgXcQ" } : ready, blocked, summary];
    vi.stubGlobal("fetch", withBrowse((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (init?.method === "POST") {
        posts.push({ url, body: JSON.parse(String(init.body)) });
        linked = true;
        return Promise.resolve(Response.json({ ...ready, youtube_video_id: "dQw4w9WgXcQ", reviews: [confirmation] }));
      }
      const current = listed()[1];
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json(listed()));
      if (url.endsWith("/admin/videos/upload-ready")) return Promise.resolve(Response.json({ ...current, reviews: [confirmation] }));
      return Promise.resolve(Response.json({ ...summary, reviews: [] }));
    }, listed));
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "上傳包影片" });
    expect(screen.getAllByRole("region").map((region) => region.getAttribute("aria-label"))).toEqual(["需要你", "可以上架", "全部影片"]);
    const needs = screen.getByRole("region", { name: "需要你" });
    expect([...needs.querySelectorAll("button")].map((button) => button.textContent)).toEqual([expect.stringContaining("卡住的影片"), expect.stringContaining("AI 模型怎麼挑")]);
    expect(needs.textContent).toContain("卡住");
    expect(tableRows(await screen.findByRole("table", { name: "全部影片" })).find((row) => row.includes("已上架的影片"))).toContain("YouTube 影片 abcdefghijk");

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
    // Linking the video reads the groups and the catalog again: the card goes, its line says it is on YouTube.
    await waitFor(() => expect(screen.queryByRole("region", { name: "可以上架" })).toBeNull());
    await waitFor(() => expect(tableRows(screen.getByRole("table", { name: "全部影片" })).find((row) => row.includes("上傳包影片"))).toContain("YouTube 影片 dQw4w9WgXcQ"));
  });

  it("filters the catalog by category and state, searches it, and keeps the typed search across reloads", async () => {
    const news = { ...summary, slug: "gemini-student", title: "Gemini 學生方案", pending: 0, category: "ai-news" };
    const unfiled = { ...summary, pending: 0 };
    const gone = { ...summary, slug: "old-tutorial", title: "舊教學", pending: 0, category: "tutorial", dropped_at: "2026-09-25T13:00:00Z" };
    const items: Item[] = [news, unfiled, gone];
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/admin/videos/browse")) {
        urls.push(url);
        const query = new URL(url, "http://test").searchParams;
        const matches = (item: Item, skip: string) => (skip === "category" || !query.get("category") || (item.category ?? "none") === query.get("category"))
          && (skip === "state" || !query.get("state") || browseState(item) === query.get("state"))
          && (!query.get("q") || String(item.title).includes(query.get("q") ?? ""));
        const shown = items.filter((item) => matches(item, ""));
        // Each facet is counted with the other filters kept and its own dropped, as the server does.
        const facets = { category: pageOf(items.filter((item) => matches(item, "category"))).facets.category, state: pageOf(items.filter((item) => matches(item, "state"))).facets.state };
        return Promise.resolve(Response.json({ ...pageOf(shown), facets }));
      }
      return Promise.resolve(Response.json(url.endsWith("/admin/videos?shorts=exclude") ? items : { ...unfiled, reviews: [] }));
    }));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const table = await screen.findByRole("table", { name: "全部影片" });
    expect(tableRows(table)).toHaveLength(3);
    expect(tableRows(table).find((row) => row.includes("Gemini 學生方案"))).toContain("AI／科技時事");
    expect(tableRows(table).find((row) => row.includes("AI 模型怎麼挑"))).toContain("未分類");
    expect(screen.getByText("共 3 支")).toBeTruthy();
    expect(urls[0]).toContain("/admin/videos/browse?page=1&limit=30");

    // The pills carry the server's counts; a category with none is not clickable.
    const categories = screen.getByRole("group", { name: "分類" });
    expect(within(categories).getByRole("button", { name: /^全部分類/ }).textContent).toBe("全部分類3");
    expect(within(categories).getByRole("button", { name: /^AI／科技時事/ }).textContent).toBe("AI／科技時事1");
    expect(within(categories).getByRole("button", { name: /^觀念解說/ })).toHaveProperty("disabled", true);
    fireEvent.click(within(categories).getByRole("button", { name: /^AI／科技時事/ }));
    expect(window.location.search).toBe("?category=ai-news");
    await waitFor(() => expect(urls.at(-1)).toContain("category=ai-news"));
    await waitFor(() => expect(tableRows(screen.getByRole("table", { name: "全部影片" }))).toHaveLength(1));
    fireEvent.click(within(categories).getByRole("button", { name: /^未分類/ }));
    expect(window.location.search).toBe("?category=none");
    await waitFor(() => expect(urls.at(-1)).toContain("category=none"));
    fireEvent.click(within(categories).getByRole("button", { name: /^全部分類/ }));
    expect(window.location.search).toBe("");

    const states = screen.getByRole("group", { name: "狀態" });
    fireEvent.click(within(states).getByRole("button", { name: /^已放棄/ }));
    expect(window.location.search).toBe("?state=dropped");
    await waitFor(() => expect(tableRows(screen.getByRole("table", { name: "全部影片" }))).toEqual([expect.stringContaining("舊教學")]));

    // What is typed stays through a reload for another filter; Enter sends it as q and resets the page.
    const box = screen.getByRole("searchbox", { name: "搜尋" });
    fireEvent.change(box, { target: { value: "學生" } });
    fireEvent.click(within(states).getByRole("button", { name: /^全部/ }));
    await waitFor(() => expect(urls.at(-1)).not.toContain("state="));
    expect((screen.getByRole("searchbox", { name: "搜尋" }) as HTMLInputElement).value).toBe("學生");
    fireEvent.submit(box.closest("form") as HTMLFormElement);
    expect(window.location.search).toBe(`?q=${encodeURIComponent("學生")}`);
    await waitFor(() => expect(urls.at(-1)).toContain(`q=${encodeURIComponent("學生")}`));
    await waitFor(() => expect(tableRows(screen.getByRole("table", { name: "全部影片" }))).toEqual([expect.stringContaining("Gemini 學生方案")]));
    fireEvent.change(screen.getByRole("searchbox", { name: "搜尋" }), { target: { value: "沒有這支" } });
    fireEvent.submit(box.closest("form") as HTMLFormElement);
    await screen.findByText("沒有符合條件的影片。");
  });

  it("pages through the catalog and falls back to the last page when the URL is past it", async () => {
    const urls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes("/admin/videos/browse")) {
        urls.push(url);
        const page = Number(new URL(url, "http://test").searchParams.get("page") ?? "1");
        return Promise.resolve(Response.json(pageOf([{ ...summary, pending: 0 }], { total: 40, page: Math.min(page, 2), pages: 2 })));
      }
      return Promise.resolve(Response.json(url.endsWith("/admin/videos?shorts=exclude") ? [] : { ...summary, reviews: [] }));
    }));
    window.history.replaceState(null, "", "/?page=7");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    await screen.findByRole("table", { name: "全部影片" });
    expect(urls[0]).toContain("page=7");
    await waitFor(() => expect(window.location.search).toBe("?page=2"));
    await waitFor(() => expect(urls.at(-1)).toContain("page=2&"));
    const paging = await screen.findByRole("navigation", { name: "第 2／2 頁" });
    expect(within(paging).getByRole("button", { name: "下一頁" })).toHaveProperty("disabled", true);
    fireEvent.click(within(paging).getByRole("button", { name: "上一頁" }));
    expect(window.location.search).toBe("");
    await waitFor(() => expect(urls.at(-1)).toContain("page=1&"));
    fireEvent.click(screen.getByRole("button", { name: "下一頁" }));
    expect(window.location.search).toBe("?page=2");
  });

  it("lets a content manager file the video under a category on its page, and a reader only see it", async () => {
    const posts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: /AI 模型怎麼挑/ }));
    const form = await screen.findByRole("form", { name: "分類" });
    const select = within(form).getByRole("combobox") as HTMLSelectElement;
    expect(select.value).toBe("");
    expect([...select.options].map((option) => option.textContent)).toEqual(["未分類", "AI 名詞解釋", "AI／科技時事", "教學實作", "比較評測", "觀念解說", "品牌故事", "漫劇", "長篇劇", "動漫", "旅遊", "其他"]);
    const save = within(form).getByRole("button", { name: "儲存" });
    expect(save).toHaveProperty("disabled", true);
    fireEvent.change(select, { target: { value: "tutorial" } });
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);
    await waitFor(() => expect(posts.filter((post) => post.method === "PUT")).toHaveLength(1));
    expect(posts.at(-1)?.url).toContain("/admin/videos/ai-model-choice/category");
    expect(posts.at(-1)?.body).toEqual({ category: "tutorial" });
    await within(form).findByRole("status");
    expect(within(form).getByRole("status").textContent).toBe("分類已儲存");
    // Back to none is a choice too, sent as null.
    fireEvent.change(select, { target: { value: "" } });
    fireEvent.click(within(form).getByRole("button", { name: "儲存" }));
    await waitFor(() => expect(posts.filter((post) => post.method === "PUT")).toHaveLength(2));
    expect(posts.at(-1)?.body).toEqual({ category: null });
  });

  it("shows a reader the category without a save", async () => {
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: /AI 模型怎麼挑/ }));
    const form = await screen.findByRole("form", { name: "分類" });
    expect(within(form).getByRole("combobox")).toHaveProperty("disabled", true);
    expect(within(form).queryByRole("button")).toBeNull();
  });

  it("offers a compilation's 1080p cut on its ready card and its page, says when it is still being cut, and nothing for an ordinary video", async () => {
    const ready = { ...summary, slug: "upload-ready", title: "上傳包影片", stage: "done", pending: 0, publish_approved_at: "2026-09-27T05:00:00Z" };
    const compilation = { ...ready, slug: "wenjian-full", title: "問劍 合集", series_slug: "wenjian", episode_number: null, compilation: true, download_available: true };
    const cutting = { ...compilation, slug: "wenjian-cut", title: "問劍 合集（剪接中）", download_available: false };
    const projects = [ready, compilation, cutting];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/admin/videos?shorts=exclude")) return Promise.resolve(Response.json(projects));
      const project = projects.find((each) => url.endsWith(`/admin/videos/${each.slug}`)) ?? ready;
      return Promise.resolve(Response.json({ ...project, reviews: [] }));
    }));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const full = await screen.findByRole("article", { name: "問劍 合集" });
    const link = within(full).getByRole("link", { name: "下載 1080p 成片" });
    expect(link.getAttribute("href")).toBe("/api/admin-video-download/wenjian-full");
    expect(link.getAttribute("download")).toBe("wenjian-full.mp4");
    const cut = screen.getByRole("article", { name: "問劍 合集（剪接中）" });
    expect(cut.textContent).toContain("成片還在工人的工作區");
    expect(within(cut).queryByRole("link")).toBeNull();
    const plain = screen.getByRole("article", { name: "上傳包影片" });
    expect(plain.textContent).not.toContain("1080p");
    expect(plain.textContent).not.toContain("工作區");
    // The video page says whose compilation it is and offers the same download.
    fireEvent.click(within(full).getByRole("button", { name: "打開 wenjian-full" }));
    await screen.findByText("作品 wenjian 的合集");
    expect(screen.getByRole("link", { name: "下載 1080p 成片" }).getAttribute("href")).toBe("/api/admin-video-download/wenjian-full");
    expect(screen.queryByText(/第 0 集/)).toBeNull();
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
