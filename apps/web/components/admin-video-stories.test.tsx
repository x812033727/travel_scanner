import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoSeries } from "./admin-video-series";
import { nextFreeSlot, planSlots, STORY_IMPORT_MAX_BYTES } from "./admin-video-stories";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[], roles: string[] = []): AdminBootstrap {
  return { admin_roles: roles, admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}
const MANAGER = ["content.read", "content.manage"];
const READER = ["content.read"];

// Monday 28 September 2026, 13:30 in Taipei: today's noon slot has gone, tonight's 20:00 is free.
const NOW = Date.parse("2026-09-28T05:30:00Z");
const CHAPTERS = ["hook", "origin", "idea", "engine", "turn", "now"];

// A story's plan as the import leaves it in the episode's beats (docs/videos/STORY.md).
function plan(id: string, category: string, region: string, day: number, slot: string) {
  return {
    id, category, region, subject: `${id} 主題`, question: `${id} 為什麼等了那麼久才賣得起來？`,
    chapters: CHAPTERS.map((key) => ({ key, point: `${id} 的 ${key} 要點` })),
    takeaway: `${id} 留給觀眾的觀察`,
    must_verify: [
      { claim: `${id} 的專利在 1970 年申請`, sources: [0, 1], core: true },
      { claim: `${id} 的主管說百貨公司都拒絕他`, sources: [1], attributed: true },
      { claim: `${id} 的營收只在年報裡`, sources: [2], reviewer_only: true },
    ],
    sources: [
      { url: `https://patents.example.org/${id}`, publisher: "專利資料庫", kind: "official", supports: "申請與核准日期", checked: "2026-09-28" },
      { url: `https://news.example.org/${id}`, publisher: "報紙專訪", kind: "news", supports: "主管自己的說法", checked: "2026-09-27" },
      { url: `http://reports.example.org/${id}.pdf`, publisher: "年報", kind: "archive", supports: "營收", checked: "2026-09-26" },
    ],
    names: ["Example"], cast: [], image_notes: "", sensitivity: "none", related_guide: null,
    thumbnail: { headline: "標題字", idea: "畫面構想" }, caveats: `${id}：某個軼事查不到出處，不要講。`,
    publish: { day, slot },
  };
}

type Row = Record<string, unknown>;
function video(slug: string, number: number, extra: Row = {}): Row {
  return {
    slug, title: `${slug} 影片`, format: "drama", stage: "done", checklist: [{ key: "final_video_approved", label: "成片核准", done: true }],
    youtube_video_id: null, last_synced_at: "2026-09-28T03:00:00Z", pending: 0, media_usd: 9.1, clip_seconds: 0, series_slug: "brand-stories", episode_number: number, ...extra,
  };
}
// Cleared for upload with its languages made: what the "ready to upload" card shows.
const cleared = (slug: string, number: number) => video(slug, number, { publish_approved_at: "2026-09-28T02:00:00Z", locales_decided_at: "2026-09-28T01:00:00Z", ready_to_upload: true });

function story(number: number, id: string, category: string, region: string, day: number, slot: string, status: string, extra: Row = {}) {
  return { number, chapter_number: 1, title: `${id} 的故事`, logline: `${id} 一句話說完`, beats: plan(id, category, region, day, slot), status, slug: `story-${id.toLowerCase()}`, recap: null, started_at: null as string | null, finished_at: null, video: null as Row | null, ...extra };
}

const stories = [
  story(1, "A01", "everyday", "global", 1, "12:00", "done", { title: "人類先登上月球，輪子行李箱才賣得起來", started_at: "2026-09-25T01:00:00Z", video: cleared("story-a01", 1) }),
  story(2, "B18", "asia-brand", "jp", 1, "20:00", "done", { started_at: "2026-09-25T02:00:00Z", video: cleared("story-b18", 2) }),
  story(3, "A03", "everyday", "global", 2, "12:00", "done", { started_at: "2026-09-26T01:00:00Z", video: cleared("story-a03", 3) }),
  // On YouTube, scheduled for tomorrow's noon slot: the slot is taken.
  story(4, "C20", "asia-brand", "tw", 2, "20:00", "done", { started_at: "2026-09-26T02:00:00Z", video: video("story-c20", 4, { youtube_video_id: "abcdefghijk", youtube_publish_at: "2026-09-29T04:00:00Z", publish_approved_at: "2026-09-27T02:00:00Z", locales_decided_at: "2026-09-27T01:00:00Z", ready_to_upload: true }) }),
  story(5, "T01", "tech", "global", 3, "12:00", "started", { started_at: "2026-09-28T01:00:00Z", video: video("story-t01", 5, { stage: "keyframes", checklist: [{ key: "keyframes", label: "分鏡", done: false }] }) }),
  story(6, "K04", "asia-brand", "kr", 3, "20:00", "ready"),
  story(7, "A05", "everyday", "global", 4, "12:00", "skipped"),
  // Started, then its video was dropped: skipped for good.
  story(8, "T02", "tech", "global", 4, "20:00", "skipped", { started_at: "2026-09-27T01:00:00Z", video: video("story-t02", 8, { dropped_at: "2026-09-27T09:00:00Z" }) }),
];

const quota = { day: "2026-09-28", started_today: 1, episodes_per_day: 2, in_flight: 1, max_in_flight: 2, started_this_month: 12, episodes_per_month: 70, awaiting_upload: 3, upload_buffer: 6, ready: 1, hold: null, hold_detail: null };
const summary = {
  id: "0f0e0d0c-0b0a-4908-8706-050403020100", slug: "brand-stories", kind: "story", title: "品牌故事：日常背後的生意", premise: "每一集講一個品牌、一件日用品或一個標準。",
  aspects: [], tone: "dual-male-leads-subtext", style_preset: "custom", target_minutes: 13, planned_episodes: 100, episodes_per_chapter: 10, chapters: 1, open_ended: false,
  status: "active", note: null, requested_chapter: null, force_next: false, episodes_done: 4, episodes_started: 1, episodes_ready: 1, docs_pending: 0, messages_pending: 0,
  media_usd: 27.3, clip_seconds: 0, hands_off: true, compilation: false, visual_tier: "stills", episodes_per_day: 2, image_model: "gemini-3.1-flash-image",
  look: { style: "flat 2D cartoon", negative: "text, logo" }, quota, created_at: "2026-09-20T00:00:00Z", updated_at: "2026-09-28T00:00:00Z",
};
const confirmation = {
  id: "7a7a7a7a-7a7a-4a7a-8a7a-7a7a7a7a7a7a", gate: "publish", content_sha256: "7".repeat(64), summary: "上傳包",
  payload: { zh: { title: "輪子行李箱的故事", description: "參考資料見說明欄。", tags: ["品牌故事"] }, minutes: 13 },
  files: [{ role: "final", sha256: "8".repeat(64), size: 250_000_000, content_type: "video/mp4" }],
  status: "approved", choice: null, note: null, decided_at: "2026-09-28T02:00:00Z", created_at: "2026-09-28T02:00:00Z",
};
const connection = (linked: boolean) => ({
  client_id: linked ? "123456789012-abcdefghijklmnop.apps.googleusercontent.com" : null, client_secret_set: linked, redirect_uri: "https://mokaair.com/api/admin-video-youtube/callback",
  scope: "https://www.googleapis.com/auth/youtube.force-ssl", configured: linked, linked, channel_id: linked ? "UCfixturechannel0000000" : null, channel_title: linked ? "Mokaair" : null,
  channel_url: null, linked_at: null, verified_at: null, problem: null, audited: false,
});
// The file the owner imports: the first three stories of the plan.
const storyFile = { schema_version: 1, series: { slug: "brand-stories", title: summary.title, kind: "story" }, stories: stories.slice(0, 3).map((each) => ({ number: each.number, slug: each.slug, title: each.title, logline: each.logline, ...each.beats })) };
function importReport(overrides: Row = {}) {
  return {
    series: "brand-stories", dry_run: true, accepted: true, written: false, series_exists: false, series_created: true, stories_in_file: 3, stories_imported: 2,
    create: 2, update: 0, leave_alone: 0, refuse: 0, rows: { create: ["A01", "B18"], update: [], renumbered: [], unchanged: [], started: [], refused: [] },
    series_differs: {}, problems: [], notes: ["series.youtube_category_id is not kept by the server"], ...overrides,
  };
}

type Call = { url: string; method: string; body?: Row };
type Story = (typeof stories)[number];
// What ?beats=summary keeps of a story's beats (SUMMARY_BEAT_KEYS in the API's series.py).
const SUMMARY_KEYS = ["id", "category", "region", "subject", "publish"];
const light = (each: Story) => ({ ...each, beats: Object.fromEntries(Object.entries(each.beats).filter(([key]) => SUMMARY_KEYS.includes(key))) });
type StubOptions = { series?: Row; listed?: unknown[]; linked?: boolean; importAnswer?: (body: Row) => Response; restoreRefused?: boolean; planRefused?: boolean };
/**
 * The site as the story pages see it: the story list, the series (whole, or each story's list
 * fields only at ?beats=summary), one story's whole episode, the videos, the import. A skip or a
 * restore changes the story's status, as the server does; options may be changed between steps.
 */
function stubFetch(options: StubOptions = {}) {
  const calls: Call[] = [];
  let current: Row = { ...summary, ...options.series };
  const statuses = new Map<number, string>();
  const episodes = () => stories.map((each) => (statuses.has(each.number) ? { ...each, status: statuses.get(each.number) as string } : each));
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    const body = init?.body ? JSON.parse(String(init.body)) as Row : undefined;
    calls.push({ url, method, body });
    const json = (value: unknown, status = 200) => Promise.resolve(Response.json(value, { status }));
    if (url.endsWith("/admin/video-automation/series?kind=story")) return json({ series: options.listed ?? [current] });
    if (url.includes("/admin/video-automation/series?kind=")) return json({ series: [] });
    if (url.endsWith("/stories/import")) return Promise.resolve(options.importAnswer ? options.importAnswer(body ?? {}) : Response.json(importReport({ dry_run: !body?.apply, written: Boolean(body?.apply) })));
    if (url.endsWith("/restore") && options.restoreRefused) return json({ code: "video_series_episode_was_started", detail: "第 7 個故事在 09/27 開始做過、影片已經放棄" }, 409);
    const change = /\/series\/brand-stories\/episodes\/(\d+)\/(skip|restore)$/.exec(url);
    if (change && method === "POST") {
      statuses.set(Number(change[1]), change[2] === "skip" ? "skipped" : "ready");
      return json({ ...current, docs: [], episodes: episodes() });
    }
    const one = /\/series\/brand-stories\/episodes\/(\d+)$/.exec(url);
    if (one && method === "GET") {
      if (options.planRefused) return json({ code: "internal_error", detail: "伺服器暫時無法回應" }, 503);
      return json(episodes().find((each) => each.number === Number(one[1])));
    }
    if (url.includes("/admin/video-automation/series/brand-stories")) {
      if (method === "PATCH") current = { ...current, ...body };
      return json({ ...current, docs: [], episodes: url.endsWith("?beats=summary") ? episodes().map(light) : episodes() });
    }
    if (url.endsWith("/admin/video-youtube")) return json(connection(Boolean(options.linked)));
    const detail = /\/admin\/videos\/(story-[a-z0-9]+)$/.exec(url);
    if (detail && method === "GET") return json({ ...(stories.find((each) => each.slug === detail[1])?.video ?? {}), reviews: [confirmation] });
    if (/\/admin\/videos\/story-[a-z0-9]+\/youtube$/.test(url) && method === "POST") return json({ slug: url.split("/").at(-2) });
    return json([]);
  }));
  return { calls, options };
}
const seriesReads = (calls: Call[]) => calls.filter((call) => call.method === "GET" && /\/admin\/video-automation\/series\/brand-stories(\?|$)/.test(call.url)).map((call) => call.url.split("brand-stories")[1]);
const planReads = (calls: Call[], number: number) => calls.filter((call) => call.method === "GET" && call.url.endsWith(`/series/brand-stories/episodes/${number}`)).length;
/** The opened plan once its own read came back. */
const loadedPlan = async (id: string) => {
  await waitFor(() => expect(screen.getByRole("region", { name: `${id} 的企劃` }).textContent).toContain(`${id} 為什麼等了那麼久才賣得起來？`));
  return screen.getByRole("region", { name: `${id} 的企劃` });
};

const renderTab = (capabilities = MANAGER, roles: string[] = [], opened: string[] = []) => render(<AdminOperationsProvider bootstrap={bootstrap(capabilities, roles)}>
  <AdminVideoSeries onOpenVideo={(slug) => opened.push(slug)} />
</AdminOperationsProvider>);
const openStories = () => window.history.replaceState(null, "", "/?tab=drama&series=brand-stories");
/** The story rows, not the lists nested in an opened plan. */
const rows = () => [...screen.getByRole("list", { name: "故事清單" }).querySelectorAll(":scope > li")] as HTMLElement[];
const row = (id: string) => rows().find((item) => item.textContent?.startsWith(id)) as HTMLElement;
// What the page shows for a slot and what the upload form holds, in this machine's zone.
const slotText = (iso: string) => new Intl.DateTimeFormat("zh-TW", { timeZone: "Asia/Taipei", month: "numeric", day: "numeric", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).format(Date.parse(iso));
const wallClock = (iso: string) => {
  const value = new Date(iso);
  const pad = (part: number) => String(part).padStart(2, "0");
  return `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}T${pad(value.getHours())}:${pad(value.getMinutes())}`;
};

beforeEach(() => {
  vi.useFakeTimers({ now: NOW, toFake: ["Date"] });
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  window.history.replaceState(null, "", "/");
});

describe("the next free publishing slot", () => {
  it("is the story's own time of day, ahead of now by an hour, and not one a scheduled video holds", () => {
    // 13:30 in Taipei: today's noon has gone, tonight's eight o'clock is free.
    expect(new Date(nextFreeSlot("12:00", [], NOW)).toISOString()).toBe("2026-09-29T04:00:00.000Z");
    expect(new Date(nextFreeSlot("20:00", [], NOW)).toISOString()).toBe("2026-09-28T12:00:00.000Z");
    expect(new Date(nextFreeSlot("", [], NOW)).toISOString()).toBe("2026-09-28T12:00:00.000Z");
    // Half an hour before noon is too close to upload for noon.
    expect(new Date(nextFreeSlot("12:00", [], Date.parse("2026-09-28T03:30:00Z"))).toISOString()).toBe("2026-09-29T04:00:00.000Z");
    // A minute before midnight in Taipei (15:59 UTC), the next noon is the next Taipei day's.
    expect(new Date(nextFreeSlot("12:00", [], Date.parse("2026-09-28T15:59:00Z"))).toISOString()).toBe("2026-09-29T04:00:00.000Z");
    expect(new Date(nextFreeSlot("20:00", [], Date.parse("2026-09-28T16:00:00Z"))).toISOString()).toBe("2026-09-29T12:00:00.000Z");
    // A video scheduled within the hour of a slot holds it; one further away does not.
    expect(new Date(nextFreeSlot("12:00", [Date.parse("2026-09-29T04:30:00Z")], NOW)).toISOString()).toBe("2026-09-30T04:00:00.000Z");
    expect(new Date(nextFreeSlot("12:00", [Date.parse("2026-09-29T05:00:00Z")], NOW)).toISOString()).toBe("2026-09-29T04:00:00.000Z");
  });

  it("gives every story ready to upload its own slot in the plan's order, after what is already scheduled", () => {
    const slots = planSlots(stories as never, NOW);
    const iso = (number: number) => new Date(slots.get(number) as number).toISOString();
    expect([...slots.keys()].sort()).toEqual([1, 2, 3]);
    // Tomorrow's noon is C20's, so A01 takes the day after and A03, the next noon story, the one after that.
    expect(iso(1)).toBe("2026-09-30T04:00:00.000Z");
    expect(iso(2)).toBe("2026-09-28T12:00:00.000Z");
    expect(iso(3)).toBe("2026-10-01T04:00:00.000Z");
    // A run to YouTube that is being sent holds its time too.
    const sending = stories.map((each) => (each.number === 5 ? { ...each, video: { ...(each.video as Row), youtube_sync: { status: "running", interrupted: false, request: { visibility: "scheduled", publish_at: "2026-09-28T12:00:00Z" }, steps: [], progress: null, error: null, started_at: null, finished_at: null } } } : each));
    expect(new Date(planSlots(sending as never, NOW).get(2) as number).toISOString()).toBe("2026-09-29T12:00:00.000Z");
  });
});

describe("AdminVideoStorySeries and StorySeriesPage", () => {
  it("shows a story series on the drama tab with today's count, what is in the making and waiting for upload, and why no story starts", async () => {
    const held = { quota: { ...quota, started_today: 2, hold: "per_day", hold_detail: "今天（台北時間 09/28）已經開始 2 支，每日上限 2 支" } };
    const { calls } = stubFetch({ series: held });
    renderTab();
    const section = await screen.findByRole("region", { name: "品牌故事" });
    const card = await within(section).findByRole("button", { name: /品牌故事：日常背後的生意/ });
    expect(card.textContent).toContain("今天 2／2 支（台北 9/28） · 同時進行 1／2 · 可以上架 3／6 · 待做 1");
    expect(card.textContent).toContain("現在不開新故事：");
    expect(card.textContent).toContain("今天（台北 9/28）已經開始 2 支，到了每日上限 2 支；台北時間過午夜才開始下一個。");
    expect(calls.some((call) => call.url.endsWith("/admin/video-automation/series?kind=story"))).toBe(true);

    fireEvent.click(card);
    await waitFor(() => expect(window.location.search).toContain("series=brand-stories"));
    const heading = await screen.findByRole("heading", { name: /品牌故事：日常背後的生意/ });
    expect(heading.textContent).toContain("製作中");
    expect(screen.getByText(/8 個故事 · 完成 4 · 每支約 13 分鐘/).textContent).toContain("圖片模型 gemini-3.1-flash-image");
    const panel = screen.getByRole("region", { name: "工人現在能不能開新故事" });
    expect(panel.textContent).toContain("今天已開始2／2 支（台北 9/28）");
    expect(panel.textContent).toContain("同時進行1／2");
    expect(panel.textContent).toContain("可以上架、還沒上傳3／6");
    expect(panel.textContent).toContain("本月已開始12／70");
    expect(within(panel).getByRole("status").textContent).toContain("到了每日上限 2 支");
    // None of a long series' planning: no documents, no chapters, no "start the next one now".
    expect(screen.queryByRole("region", { name: "文件" })).toBeNull();
    expect(screen.queryByRole("button", { name: "現在開始下一集" })).toBeNull();
    expect(screen.queryByRole("checkbox", { name: "免關卡" })).toBeNull();
  });

  it("lists every story from one read, filters by category and status, and opens one plan read-only", async () => {
    const { calls } = stubFetch();
    const opened: string[] = [];
    openStories();
    renderTab(MANAGER, [], opened);
    await screen.findByRole("list", { name: "故事清單" });
    expect(rows().map((item) => item.textContent?.slice(0, 3))).toEqual(["A01", "B18", "A03", "C20", "T01", "K04", "A05", "T02"]);
    expect(row("A01").textContent).toContain("人類先登上月球，輪子行李箱才賣得起來");
    expect(row("A01").textContent).toContain("日常用品與隱形標準 · 全球 · 第 1 天 12:00 · 第 1 個");
    expect(row("A01").textContent).toContain("可以上架");
    expect(row("C20").textContent).toContain("已排程");
    expect(within(row("C20")).getByRole("link", { name: /YouTube/ }).getAttribute("href")).toBe("https://www.youtube.com/watch?v=abcdefghijk");
    expect(row("T01").textContent).toContain("製作中");
    expect(row("K04").textContent).toContain("待做");
    expect(within(row("K04")).queryByRole("button", { name: "打開影片" })).toBeNull();
    expect(row("T02").textContent).toContain("已略過");
    // One read of the series carries every story; the only per-story reads are the few cards ready to upload.
    expect(calls.filter((call) => call.url.includes("/admin/video-automation/series/brand-stories"))).toHaveLength(1);
    await waitFor(() => expect(calls.filter((call) => /\/admin\/videos\/story-/.test(call.url)).map((call) => call.url.split("/").at(-1)).sort()).toEqual(["story-a01", "story-a03", "story-b18"]));
    fireEvent.click(within(row("T01")).getByRole("button", { name: "打開影片" }));
    expect(opened).toEqual(["story-t01"]);

    fireEvent.change(screen.getByRole("combobox", { name: "分類" }), { target: { value: "asia-brand" } });
    await waitFor(() => expect(rows().map((item) => item.textContent?.slice(0, 3))).toEqual(["B18", "C20", "K04"]));
    expect(window.location.search).toContain("story_category=asia-brand");
    const status = screen.getByRole("combobox", { name: "狀態" });
    expect([...status.querySelectorAll("option")].map((option) => option.textContent)).toContain("可以上架（1）");
    fireEvent.change(status, { target: { value: "scheduled" } });
    await waitFor(() => expect(rows().map((item) => item.textContent?.slice(0, 3))).toEqual(["C20"]));
    fireEvent.change(screen.getByRole("combobox", { name: "分類" }), { target: { value: "" } });
    fireEvent.change(screen.getByRole("combobox", { name: "狀態" }), { target: { value: "" } });
    await waitFor(() => expect(rows()).toHaveLength(8));

    fireEvent.click(within(row("A01")).getByRole("button", { name: "看企劃" }));
    expect((await screen.findByRole("region", { name: "A01 的企劃" })).textContent).toBe("正在讀企劃…");
    const plan = await loadedPlan("A01");
    expect(window.location.search).toContain("story=A01");
    // The plan is read from its own episode, once; the series is not read again for it.
    expect(planReads(calls, 1)).toBe(1);
    expect(seriesReads(calls)).toEqual([""]);
    expect([...plan.querySelectorAll("ol")[0].querySelectorAll("li")].map((item) => item.querySelector("span")?.textContent)).toEqual(["鉤子", "起點與人物", "關鍵點子", "生意怎麼運作", "代價或反轉", "現況與一句觀察"]);
    expect(plan.textContent).toContain("A01 留給觀眾的觀察");
    expect(plan.textContent).toContain("必查事實（3 條）");
    expect(plan.textContent).toContain("A01 的專利在 1970 年申請來源 1, 2標題靠這條");
    expect(plan.textContent).toContain("要說是誰的說法");
    expect(plan.textContent).toContain("只有查核者讀得到證據");
    expect(within(plan).getByRole("link", { name: "專利資料庫" }).getAttribute("href")).toBe("https://patents.example.org/A01");
    // Only an https source is a link.
    expect(within(plan).queryByRole("link", { name: "年報" })).toBeNull();
    expect(plan.textContent).toContain("典藏 · 2026-09-26 查過");
    expect(plan.textContent).toContain("A01：某個軼事查不到出處，不要講。");
    expect(within(plan).queryByRole("button")).toBeNull();
    expect(within(plan).queryByRole("textbox")).toBeNull();
  });

  it("reads the series with each story's list fields only once it knows it is a story series, and each opened plan on its own", async () => {
    const { calls } = stubFetch();
    vi.spyOn(window, "confirm").mockReturnValue(true);
    openStories();
    renderTab();
    await screen.findByRole("list", { name: "故事清單" });
    // The first read cannot know the kind, so it is whole.
    expect(seriesReads(calls)).toEqual([""]);

    // A skip reads the series again, now with the list's fields only; the list looks the same.
    fireEvent.click(within(row("K04")).getByRole("button", { name: "略過" }));
    await waitFor(() => expect(row("K04").textContent).toContain("已略過"));
    expect(seriesReads(calls)).toEqual(["", "?beats=summary"]);
    expect(rows().map((item) => item.textContent?.slice(0, 3))).toEqual(["A01", "B18", "A03", "C20", "T01", "K04", "A05", "T02"]);
    expect(row("A01").textContent).toContain("日常用品與隱形標準 · 全球 · 第 1 天 12:00 · 第 1 個");
    expect(row("A01").textContent).toContain("可以上架");
    expect(row("C20").textContent).toContain("已排程");
    const ready = screen.getByRole("region", { name: "可以上架" });
    expect(within(ready).getAllByRole("article").map((item) => item.getAttribute("aria-label")?.slice(0, 3))).toEqual(["A01", "B18", "A03"]);
    expect(within(ready).getAllByRole("article")[0].textContent).toContain(`下一個空的時段：${slotText("2026-09-30T04:00:00Z")}（台北時間）`);
    fireEvent.change(screen.getByRole("combobox", { name: "分類" }), { target: { value: "tech" } });
    await waitFor(() => expect(rows().map((item) => item.textContent?.slice(0, 3))).toEqual(["T01", "T02"]));
    fireEvent.change(screen.getByRole("combobox", { name: "分類" }), { target: { value: "" } });
    await waitFor(() => expect(rows()).toHaveLength(8));

    // The whole plan comes from the story's own read, though the list no longer carries it.
    fireEvent.click(within(row("A01")).getByRole("button", { name: "看企劃" }));
    const plan = await loadedPlan("A01");
    expect(plan.textContent).toContain("鉤子");
    expect(plan.textContent).toContain("必查事實（3 條）");
    expect(plan.textContent).toContain("A01：某個軼事查不到出處，不要講。");
    expect(planReads(calls, 1)).toBe(1);
    // Closed and opened again, it is shown at once without another read.
    fireEvent.click(within(row("A01")).getByRole("button", { name: "收起企劃" }));
    await waitFor(() => expect(screen.queryByRole("region", { name: "A01 的企劃" })).toBeNull());
    fireEvent.click(within(row("A01")).getByRole("button", { name: "看企劃" }));
    expect(screen.getByRole("region", { name: "A01 的企劃" }).textContent).toContain("A01 為什麼等了那麼久才賣得起來？");
    expect(planReads(calls, 1)).toBe(1);

    // A story whose row changed in the list is read again when it opens.
    fireEvent.click(within(row("A01")).getByRole("button", { name: "收起企劃" }));
    fireEvent.click(within(row("K04")).getByRole("button", { name: "看企劃" }));
    await loadedPlan("K04");
    expect(planReads(calls, 6)).toBe(1);
    fireEvent.click(within(row("K04")).getByRole("button", { name: "收起企劃" }));
    fireEvent.click(within(row("K04")).getByRole("button", { name: "恢復" }));
    await waitFor(() => expect(row("K04").textContent).toContain("待做"));
    fireEvent.click(within(row("K04")).getByRole("button", { name: "看企劃" }));
    await loadedPlan("K04");
    expect(planReads(calls, 6)).toBe(2);
    expect(seriesReads(calls)).toEqual(["", "?beats=summary", "?beats=summary"]);
  });

  it("says why a plan could not be read and reads it again on request", async () => {
    const { calls, options } = stubFetch({ planRefused: true });
    openStories();
    renderTab();
    await screen.findByRole("list", { name: "故事清單" });
    fireEvent.click(within(row("B18")).getByRole("button", { name: "看企劃" }));
    const failed = await screen.findByRole("region", { name: "B18 的企劃" });
    expect((await within(failed).findByRole("alert")).textContent).toBe("企劃讀不到：伺服器暫時無法回應");
    options.planRefused = false;
    fireEvent.click(within(failed).getByRole("button", { name: "再試一次" }));
    const plan = await loadedPlan("B18");
    expect(within(plan).queryByRole("alert")).toBeNull();
    expect(planReads(calls, 2)).toBe(2);
  });

  it("keeps a drama series' whole read: its beats are the chapter outlines the page shows", async () => {
    const { calls } = stubFetch({ series: { kind: "long" } });
    openStories();
    renderTab();
    fireEvent.click(await screen.findByRole("button", { name: "暫停" }));
    await waitFor(() => expect(seriesReads(calls)).toHaveLength(2));
    expect(seriesReads(calls)).toEqual(["", ""]);
    expect(calls.some((call) => call.url.includes("/episodes/") && call.method === "GET")).toBe(false);
  });

  it("lets a manager change the daily count, pause the series, skip a story that has not started and bring a skipped one back", async () => {
    const { calls } = stubFetch();
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    openStories();
    renderTab();
    await screen.findByRole("list", { name: "故事清單" });
    const perDay = screen.getByRole("combobox", { name: "每天幾支" }) as HTMLSelectElement;
    expect(perDay.value).toBe("2");
    const save = screen.getByRole("button", { name: "改每日支數" });
    expect(save).toHaveProperty("disabled", true);
    fireEvent.change(perDay, { target: { value: "1" } });
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);
    await waitFor(() => expect(calls.some((call) => call.method === "PATCH")).toBe(true));
    expect(calls.find((call) => call.method === "PATCH")?.body).toEqual({ episodes_per_day: 1 });
    // The server's answer comes back and the select follows it.
    await waitFor(() => expect(screen.getByRole("button", { name: "改每日支數" })).toHaveProperty("disabled", true));
    expect((screen.getByRole("combobox", { name: "每天幾支" }) as HTMLSelectElement).value).toBe("1");
    fireEvent.change(screen.getByRole("combobox", { name: "每天幾支" }), { target: { value: "" } });
    fireEvent.click(screen.getByRole("button", { name: "改每日支數" }));
    await waitFor(() => expect(calls.filter((call) => call.method === "PATCH")).toHaveLength(2));
    expect(calls.filter((call) => call.method === "PATCH")[1].body).toEqual({ episodes_per_day: null });

    fireEvent.click(screen.getByRole("button", { name: "暫停" }));
    await waitFor(() => expect(calls.filter((call) => call.method === "PATCH")).toHaveLength(3));
    expect(calls.filter((call) => call.method === "PATCH")[2].body).toEqual({ status: "paused" });
    expect(await screen.findByRole("button", { name: "繼續" })).toBeTruthy();

    // Only a story that has not started may be skipped, and only one that never started comes back.
    expect(within(row("T01")).queryByRole("button", { name: "略過" })).toBeNull();
    expect(within(row("A01")).queryByRole("button", { name: "略過" })).toBeNull();
    fireEvent.click(within(row("K04")).getByRole("button", { name: "略過" }));
    await waitFor(() => expect(calls.some((call) => call.url.endsWith("/admin/video-automation/series/brand-stories/episodes/6/skip") && call.method === "POST")).toBe(true));
    expect(confirm.mock.calls[0][0]).toContain("K04「K04 的故事」");
    fireEvent.click(within(row("A05")).getByRole("button", { name: "恢復" }));
    await waitFor(() => expect(calls.some((call) => call.url.endsWith("/admin/video-automation/series/brand-stories/episodes/7/restore") && call.method === "POST")).toBe(true));
    expect(within(row("T02")).queryByRole("button", { name: "恢復" })).toBeNull();
    expect(row("T02").textContent).toContain("開始做過、影片已放棄，不能恢復");
    // A story series has no compilation: after the first read, the page stops asking for one.
    expect(calls.filter((call) => call.url.includes("/admin/videos?series=")).length).toBe(1);
  });

  it("says why the server refused to bring a story back", async () => {
    stubFetch({ restoreRefused: true });
    openStories();
    renderTab();
    await screen.findByRole("list", { name: "故事清單" });
    fireEvent.click(within(row("A05")).getByRole("button", { name: "恢復" }));
    expect((await screen.findByRole("alert")).textContent).toContain("第 7 個故事在 09/27 開始做過、影片已經放棄");
  });

  it("shows a reader everything, changes nothing, and names the permission and the roles that can", async () => {
    stubFetch();
    openStories();
    renderTab(READER, ["viewer"]);
    await screen.findByRole("list", { name: "故事清單" });
    const note = screen.getByRole("note");
    expect(note.textContent).toContain("你可以查看故事，但不能修改。");
    expect(note.textContent).toContain("都需要 content.manage 權限，「內容」與「Owner」角色有這個權限");
    expect(note.textContent).toContain("你目前的角色：唯讀。");
    expect(screen.getByRole("region", { name: "工人現在能不能開新故事" })).toBeTruthy();
    expect(screen.queryByRole("combobox", { name: "每天幾支" })).toBeNull();
    expect(screen.queryByRole("button", { name: "暫停" })).toBeNull();
    expect(screen.queryByRole("button", { name: "略過" })).toBeNull();
    expect(screen.queryByRole("button", { name: "恢復" })).toBeNull();
    // The ready cards show the package but no form to record an upload.
    const ready = screen.getByRole("region", { name: "可以上架" });
    await waitFor(() => expect(within(ready).getAllByLabelText("上傳包")).toHaveLength(3));
    expect(within(ready).queryByRole("form", { name: "已上傳到 YouTube" })).toBeNull();
    // A reader may dry-run an import but not write it.
    fireEvent.click(screen.getByText("再匯入一次企劃清單", { selector: "summary" }));
    fireEvent.change(screen.getByRole("textbox", { name: "或貼上檔案內容" }), { target: { value: JSON.stringify(storyFile) } });
    fireEvent.click(screen.getByRole("button", { name: "試跑" }));
    expect(await screen.findByText("試跑結果：什麼都沒有寫入")).toBeTruthy();
    expect(screen.queryByRole("button", { name: /確認寫入/ })).toBeNull();
    expect(screen.getByText("寫入需要 content.manage 權限（「內容」或「Owner」角色）。")).toBeTruthy();
  });

  it("imports a story plan: a dry run first, then the write, only for the file and choices the dry run answered", async () => {
    const { calls } = stubFetch({ listed: [] });
    renderTab();
    const form = await screen.findByRole("form", { name: "匯入企劃清單" });
    const check = within(form).getByRole("button", { name: "試跑" });
    expect(check).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByRole("textbox", { name: "或貼上檔案內容" }), { target: { value: "{ not json" } });
    expect(form.textContent).toContain("這不是有效的 JSON：");
    expect(check).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByRole("textbox", { name: "或貼上檔案內容" }), { target: { value: JSON.stringify(storyFile, null, 2) } });
    expect(form.textContent).toContain("3 個故事，作品 brand-stories。");
    fireEvent.change(within(form).getByRole("spinbutton", { name: "只匯入前幾個故事" }), { target: { value: "2" } });
    fireEvent.change(within(form).getByRole("combobox", { name: "建立作品時的每日支數" }), { target: { value: "1" } });
    fireEvent.click(check);
    const report = await within(form).findByRole("region", { name: "匯入結果" });
    const posts = () => calls.filter((call) => call.method === "POST");
    expect(posts()).toHaveLength(1);
    expect(posts()[0].url).toBe("/api/travel/admin/video-automation/series/brand-stories/stories/import");
    expect(posts()[0].body).toEqual({ file: storyFile, apply: false, limit: 2, episodes_per_day: 1 });
    expect(report.textContent).toContain("試跑結果：什麼都沒有寫入");
    expect(report.textContent).toContain("會照檔案建立作品 brand-stories。");
    expect(report.textContent).toContain("檔案有 3 個故事，這次匯入 2 個：新增 2、更新 0、不動 0、拒絕 0。");
    expect(report.textContent).toContain("新增（2） A01, B18");
    expect(report.textContent).toContain("series.youtube_category_id is not kept by the server");

    // A choice changed after the dry run: its answer no longer covers what would be written.
    fireEvent.change(within(form).getByRole("spinbutton", { name: "只匯入前幾個故事" }), { target: { value: "3" } });
    expect(within(form).queryByRole("button", { name: /確認寫入/ })).toBeNull();
    expect(report.textContent).toContain("試跑之後，檔案或選項改過了");
    fireEvent.change(within(form).getByRole("spinbutton", { name: "只匯入前幾個故事" }), { target: { value: "2" } });
    const write = within(form).getByRole("button", { name: "確認寫入（新增 2、更新 0）" });
    expect(posts()).toHaveLength(1);
    fireEvent.click(write);
    await waitFor(() => expect(posts()).toHaveLength(2));
    expect(posts()[1].body).toEqual({ file: storyFile, apply: true, limit: 2, episodes_per_day: 1 });
    // Written, the page opens the series the import created.
    await waitFor(() => expect(window.location.search).toContain("series=brand-stories"));
    expect(await screen.findByRole("heading", { name: /品牌故事：日常背後的生意/ })).toBeTruthy();
  });

  it("lists every problem of a refused file from the 422's body and offers no write", async () => {
    const refused = importReport({
      accepted: false, series_exists: true, series_created: false, create: 1, refuse: 1,
      rows: { create: ["B18"], update: [], renumbered: [], unchanged: [], started: [], refused: ["A01"] },
      problems: ["A01: title is 3 characters, at least 8", "A01: sources[2].url must be https"], notes: [],
    });
    stubFetch({ importAnswer: () => Response.json({ title: "請求未完成", status: 422, code: "video_story_import_refused", detail: "企劃清單有 2 個問題，整份都沒有寫入。第一個：A01: title is 3 characters, at least 8", ...refused }, { status: 422 }) });
    openStories();
    renderTab();
    await screen.findByRole("list", { name: "故事清單" });
    fireEvent.click(screen.getByText("再匯入一次企劃清單", { selector: "summary" }));
    const form = screen.getByRole("form", { name: "匯入企劃清單" });
    expect(form.textContent).toContain("檔案要是 brand-stories 的。");
    expect(within(form).queryByRole("combobox", { name: "建立作品時的每日支數" })).toBeNull();
    fireEvent.change(within(form).getByRole("textbox", { name: "或貼上檔案內容" }), { target: { value: JSON.stringify(storyFile) } });
    fireEvent.click(within(form).getByRole("button", { name: "試跑" }));
    const problems = await within(form).findByRole("alert");
    expect(problems.textContent).toContain("問題（2 個）：什麼都沒有寫入");
    expect([...problems.querySelectorAll("li")].map((item) => item.textContent)).toEqual(["A01: title is 3 characters, at least 8", "A01: sources[2].url must be https"]);
    expect(form.textContent).toContain("拒絕（1） A01");
    expect(form.textContent).toContain("作品 brand-stories 已經有了；匯入不會改作品本身。");
    expect(within(form).queryByRole("button", { name: /確認寫入/ })).toBeNull();
  });

  it("refuses a file over the import's limit before sending it", async () => {
    const { calls } = stubFetch({ listed: [] });
    renderTab();
    const form = await screen.findByRole("form", { name: "匯入企劃清單" });
    const huge = JSON.stringify({ ...storyFile, padding: "x".repeat(STORY_IMPORT_MAX_BYTES) });
    fireEvent.change(within(form).getByRole("textbox", { name: "或貼上檔案內容" }), { target: { value: huge } });
    fireEvent.click(within(form).getByRole("button", { name: "試跑" }));
    // Rounded up: a request just over the cap never reads as 4.00 MB.
    expect((await within(form).findByRole("alert")).textContent).toMatch(/^這次要送 4\.(0[1-9]|[1-9]\d) MB，匯入最多 4\.00 MB。$/);
    expect(calls.some((call) => call.method === "POST")).toBe(false);
  });

  it("reads a chosen stories.json file", async () => {
    const { calls } = stubFetch({ listed: [] });
    renderTab();
    const form = await screen.findByRole("form", { name: "匯入企劃清單" });
    const chosen = new File([JSON.stringify(storyFile)], "stories.json", { type: "application/json" });
    fireEvent.change(within(form).getByLabelText("stories.json 檔案"), { target: { files: [chosen] } });
    await waitFor(() => expect(form.textContent).toContain("3 個故事，作品 brand-stories。"));
    expect(form.textContent).toContain("已選 stories.json");
    fireEvent.click(within(form).getByRole("button", { name: "試跑" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    expect(calls.find((call) => call.method === "POST")?.body).toEqual({ file: storyFile, apply: false, limit: null, episodes_per_day: null });
  });

  it("offers each story ready to upload its next free slot, filled into the form that records the upload", async () => {
    const { calls } = stubFetch();
    openStories();
    renderTab();
    const ready = await screen.findByRole("region", { name: "可以上架" });
    const card = (id: string) => within(ready).getAllByRole("article").find((item) => item.getAttribute("aria-label")?.startsWith(id)) as HTMLElement;
    expect(within(ready).getAllByRole("article").map((item) => item.getAttribute("aria-label")?.slice(0, 3))).toEqual(["A01", "B18", "A03"]);
    expect(card("A01").textContent).toContain(`下一個空的時段：${slotText("2026-09-30T04:00:00Z")}（台北時間）`);
    expect(card("A01").textContent).toContain("企劃排在第 1 天 12:00。");
    expect(card("B18").textContent).toContain(`下一個空的時段：${slotText("2026-09-28T12:00:00Z")}（台北時間）`);
    expect(card("A03").textContent).toContain(`下一個空的時段：${slotText("2026-10-01T04:00:00Z")}（台北時間）`);
    const form = await within(card("A01")).findByRole("form", { name: "已上傳到 YouTube" });
    const when = within(form).getByLabelText("上架時間（選填）") as HTMLInputElement;
    expect(when.value).toBe(wallClock("2026-09-30T04:00:00Z"));
    fireEvent.change(within(form).getByRole("textbox", { name: "YouTube 網址或影片 id" }), { target: { value: "https://youtu.be/dQw4w9WgXcQ" } });
    fireEvent.click(within(form).getByRole("button", { name: "已上傳" }));
    await waitFor(() => expect(calls.some((call) => call.method === "POST" && call.url.endsWith("/admin/videos/story-a01/youtube"))).toBe(true));
    expect(calls.find((call) => call.method === "POST" && call.url.endsWith("/admin/videos/story-a01/youtube"))?.body).toEqual({ url: "https://youtu.be/dQw4w9WgXcQ", publish_at: "2026-09-30T04:00:00.000Z" });
  });

  it("fills the slot into the form that sends the video to a linked channel", async () => {
    stubFetch({ linked: true });
    openStories();
    renderTab();
    const ready = await screen.findByRole("region", { name: "可以上架" });
    const b18 = within(ready).getAllByRole("article").find((item) => item.getAttribute("aria-label")?.startsWith("B18")) as HTMLElement;
    const form = await within(b18).findByRole("form", { name: "送到 YouTube" });
    expect((within(form).getByLabelText("公開時間") as HTMLInputElement).value).toBe(wallClock("2026-09-28T12:00:00Z"));
  });
});
