import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { needsOwner, type Project, publishState } from "./admin-video-review-card";
import { AdminVideoReviews } from "./admin-video-reviews";
import { AdminVideoShorts, BATCH_URL } from "./admin-video-shorts";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const slot = (fields: Record<string, unknown>) => ({
  id: "11111111-1111-4111-8111-111111111111", starts_at: "2026-10-05T11:30:00Z", local_date: "2026-10-05", local_time: "19:30", phase: 1, line: null, series: null,
  topic_slug: null, project_slug: null, project_title: null, project_line: null, youtube_video_id: null, status: "open", locked_at: null, note: null, ...fields,
});
const overview = {
  autopublish: "on", autopublish_problem: null, consent_expires_at: "2026-12-30T03:00:00Z", paused_at: null, timezone: "Asia/Taipei",
  today: [slot({ status: "locked", project_slug: "receipt-total", project_title: "AI 真的可以算對發票嗎", project_line: "lab" })],
  tomorrow: [
    slot({ id: "44444444-4444-4444-8444-444444444444", local_date: "2026-10-06", local_time: "12:30", starts_at: "2026-10-06T04:30:00Z", status: "skipped" }),
    slot({ id: "22222222-2222-4222-8222-222222222222", local_date: "2026-10-06", starts_at: "2026-10-06T11:30:00Z" }),
  ],
  stock: { count: 4, days: 3, wanted_days: 5 },
  budget: { period_start: "2026-10-04T16:00:00Z", period_end: "2026-11-03T16:00:00Z", spent_ntd: 312.4, reserved_ntd: 40, unknown: 0, limit_ntd: 3000, soft_ntd: 2400, total_start: "2026-10-04T16:00:00Z", total_spent_ntd: 312.4, total_limit_ntd: 9000, paid_work_allowed: true, reason: null },
  channel: { linked: true, title: "Mokaair", audited: false, problem: null },
  worker_seen_at: "2026-10-05T03:00:00Z",
  campaign: { start: "2026-10-05", last_day: "2027-01-02", slots: 120, published: 0, missed: 0 },
  needs: [
    { kind: "upload", detail: "接下來 10 天有 2 支等你上傳到 YouTube Studio", count: 2 },
    { kind: "review", detail: "「掃描發票」的自動品管沒有全過，等你決定", slug: "invoice-scan", count: 1 },
    { kind: "worker", detail: "主機工人已經 42 分鐘沒有回報" },
    { kind: "budget", detail: "這 30 天已經花了 NT$2,400" },
  ],
  needs_count: 4,
};
const uploads = {
  ahead_days: 10,
  items: [
    { slug: "receipt-total", title: "AI 真的可以算對發票嗎", line: "lab", slot_at: "2026-10-05T11:30:00Z", file_name: "mokaair-short-receipt-total.mp4", size: 6_400_000, seconds: 35.2 },
    { slug: "menu-photo", title: "菜單翻譯", line: "cut", slot_at: "2026-10-06T11:30:00Z", file_name: "mokaair-short-menu-photo.mp4", size: null, seconds: null },
  ],
};
const short = (slug: string, title: string, state: string, fields: Record<string, unknown> = {}) => ({
  slug, title, stage: "publish", checklist: [], youtube_video_id: null, last_synced_at: "2026-10-01T00:00:00Z", pending: 0, format: "shorts", shorts_line: "lab", shorts_series: "daily",
  shorts_state: state, slot_at: null, ...fields,
});
const shorts = [
  short("in-library", "片庫裡的", "library"),
  short("invoice-scan", "掃描發票", "needs_you", { pending: 1, stage: "final" }),
  short("receipt-total", "AI 真的可以算對發票嗎", "slotted", { slot_at: "2026-10-05T11:30:00Z" }),
  short("missed-one", "錯過的", "missed"),
  short("episode-cut", "第三集的短篇", "making", { format: "drama", shorts_line: "drama", shorts_series: "wenjian", source_slug: "wenjian-e03", stage: "final" }),
];
const SHA = { final: "c".repeat(64), cover: "d".repeat(64), evidence: "e".repeat(64) };
const finalReview = {
  id: "33333333-3333-4333-8333-333333333333", gate: "final", content_sha256: SHA.final, summary: "Shorts 35.2 秒，Shorts 自動品管 12 項全過",
  payload: {
    duration_seconds: 35.2, titles: ["AI 真的可以算對發票嗎", "三張發票，AI 算對幾張"],
    qa: { ok: true, kind: "shorts", final_sha256: SHA.final, items: ["profile", "loudness", "layout", "narration", "evidence", "facts", "policy", "metadata", "captions", "links", "variety", "disclosure"].map((id) => ({ id, ok: true, detail: "" })) },
  },
  files: [
    { role: "preview", sha256: SHA.final, size: 6_400_000, content_type: "video/mp4" },
    { role: "thumbnail", sha256: SHA.cover, size: 120_000, content_type: "image/png" },
    { role: "evidence_result", sha256: SHA.evidence, size: 2048, content_type: "application/json" },
  ],
  status: "approved", choice: null, note: "Shorts 自動品管 12 項全過，依設定自動核准", decided_at: "2026-10-01T00:00:00Z", created_at: "2026-10-01T00:00:00Z",
};

type Call = { url: string; method: string; body: unknown };
type Answers = { overview?: unknown | (() => unknown); uploads?: unknown; shorts?: unknown; tutorials?: unknown; project?: unknown; write?: (call: Call) => Response | undefined };

function stubFetch(answers: Answers = {}) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const call = { url: String(input), method: init?.method ?? "GET", body: init?.body ? JSON.parse(String(init.body)) : undefined };
    calls.push(call);
    const path = call.url.replace(/^.*\/api\/travel/, "");
    if (call.method !== "GET") return Promise.resolve(answers.write?.(call) ?? Response.json({ recalled: 0, items: [] }));
    if (path === "/admin/video-shorts/overview") return Promise.resolve(Response.json(typeof answers.overview === "function" ? answers.overview() : answers.overview ?? overview));
    if (path === "/admin/video-shorts/uploads") return Promise.resolve(Response.json(answers.uploads ?? uploads));
    if (path.startsWith("/admin/video-shorts/slots")) return Promise.resolve(Response.json({ timezone: "Asia/Taipei", slots: [] }));
    if (path === "/admin/video-shorts/metrics") return Promise.resolve(Response.json({ items: [] }));
    if (path === "/admin/video-shorts/costs") return Promise.resolve(Response.json({ items: [], budget: overview.budget, periods: [] }));
    if (path === "/admin/videos?shorts=only") return Promise.resolve(Response.json(answers.shorts ?? shorts));
    if (path.startsWith("/admin/videos?")) return Promise.resolve(Response.json(answers.tutorials ?? []));
    if (path.startsWith("/admin/videos/browse")) return Promise.resolve(Response.json({ items: [], total: 0, page: 1, pages: 0, facets: { category: [], state: [] } }));
    if (path.startsWith("/admin/videos/")) return Promise.resolve(Response.json(answers.project ?? { ...shorts[2], reviews: [finalReview] }));
    return Promise.resolve(Response.json({}, { status: 404 }));
  }));
  return calls;
}

const paths = (calls: Call[]) => calls.map((call) => `${call.method} ${call.url.replace(/^.*\/api\/travel/, "")}`);
const page = (capabilities = ["content.read", "content.manage"]) => render(<AdminOperationsProvider bootstrap={bootstrap(capabilities)}><AdminVideoReviews /></AdminOperationsProvider>);
const tab = (capabilities = ["content.read", "content.manage"], onOpenVideo = vi.fn()) => {
  render(<AdminOperationsProvider bootstrap={bootstrap(capabilities)}><AdminVideoShorts onOpenVideo={onOpenVideo} /></AdminOperationsProvider>);
  return onOpenVideo;
};

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("the Shorts tab of /admin/videos", () => {
  it("sits between the dramas and the settings, and follows the address", async () => {
    const calls = stubFetch();
    page();
    const tabs = within(screen.getByRole("tablist", { name: "影片審核分頁" })).getAllByRole("tab");
    expect(tabs.map((each) => each.textContent)).toEqual(["影片", "漫劇", "Shorts", "設定"]);
    fireEvent.click(tabs[2]);
    expect(await screen.findByRole("region", { name: "Shorts 現況" })).toBeTruthy();
    expect(window.location.search).toContain("tab=shorts");
    expect(paths(calls)).toContain("GET /admin/video-shorts/overview");
    // The calendar is the first view; the others are asked for by name.
    const views = within(screen.getByRole("tablist", { name: "Shorts 的畫面" })).getAllByRole("tab");
    expect(views.map((each) => each.textContent)).toEqual(["月曆", "片庫與製作中", "成效", "花費", "Shorts 設定"]);
    expect(views[0].getAttribute("aria-selected")).toBe("true");
    fireEvent.click(views[2]);
    await waitFor(() => expect(window.location.search).toContain("view=metrics"));
    expect(await screen.findByText("還沒有公開的 Shorts")).toBeTruthy();
    fireEvent.click(views[3]);
    expect(await screen.findByRole("region", { name: "這 30 天" })).toBeTruthy();
    expect(window.location.search).toContain("view=costs");
  });

  it("opens on the view the address names, and a video in the address comes first", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?tab=shorts&view=library");
    const { unmount } = page();
    expect(await screen.findByRole("region", { name: "片庫" })).toBeTruthy();
    unmount();
    window.history.replaceState(null, "", "/?tab=shorts&view=library&video=receipt-total");
    page();
    expect(await screen.findByRole("heading", { name: "AI 真的可以算對發票嗎" })).toBeTruthy();
    expect(screen.queryByRole("region", { name: "Shorts 現況" })).toBeNull();
  });

  it("asks for the tutorials without the Shorts, and for the Shorts alone", async () => {
    const tutorial = { slug: "ai-model-choice", title: "AI 模型怎麼挑", stage: "final", youtube_video_id: null, last_synced_at: "2026-09-25T05:00:00Z", pending: 1, checklist: [] };
    // A server from before the filter answers with everything: the page still leaves the Shorts out.
    const calls = stubFetch({ tutorials: [tutorial, shorts[0], { ...tutorial, slug: "a-drama", title: "一集漫劇", format: "drama" }] });
    page();
    expect(await screen.findByRole("button", { name: /AI 模型怎麼挑/ })).toBeTruthy();
    expect(paths(calls)).toContain("GET /admin/videos?shorts=exclude");
    expect(screen.queryByText("片庫裡的")).toBeNull();
    expect(screen.queryByText("一集漫劇")).toBeNull();
    fireEvent.click(screen.getByRole("tab", { name: "Shorts" }));
    fireEvent.click(await screen.findByRole("tab", { name: "片庫與製作中" }));
    expect(await screen.findByRole("button", { name: "打開 片庫裡的" })).toBeTruthy();
    expect(paths(calls)).toContain("GET /admin/videos?shorts=only");
  });
});

describe("the top row", () => {
  it("says where publishing stands", async () => {
    stubFetch();
    tab();
    const top = await screen.findByRole("region", { name: "Shorts 現況" });
    const tile = (label: string) => within(top).getByText(label, { selector: "dt" }).parentElement as HTMLElement;
    expect(tile("自動上架").textContent).toContain("開著");
    expect(tile("今天").textContent).toContain("19:30");
    expect(tile("今天").textContent).toContain("AI 真的可以算對發票嗎");
    expect(tile("今天").textContent).toContain("已鎖定");
    // The empty slot waits for a Short; the one that is not publishing waits for none.
    expect(tile("明天").textContent).toBe("明天12:30不發19:30還沒有排影片空格");
    expect(tile("片庫").textContent).toContain("4 支");
    expect(tile("片庫").textContent).toContain("夠 3 天，希望有 5 天");
    expect(tile("這 30 天的花費").textContent).toContain("NT$312.4，上限 NT$3,000");
    expect(tile("這 30 天的花費").textContent).toContain("另有 NT$40 已預留");
    expect(tile("YouTube 頻道").textContent).toContain("Mokaair");
    expect(tile("YouTube 頻道").textContent).toContain("API 稽核還沒通過：檔案由你上傳");
    expect(tile("這一輪").textContent).toContain("2026-10-05 到 2027-01-02");
    expect(tile("這一輪").textContent).toContain("共 120 格，已公開 0，錯過 0");
    expect(top.textContent).toContain("這是實驗目標，不是營利資格的核算");
  });

  it("pauses, resumes and recalls, and asks before a recall", async () => {
    let paused = false;
    const calls = stubFetch({
      overview: () => ({ ...overview, autopublish: paused ? "paused" : "on", paused_at: paused ? "2026-10-05T04:00:00Z" : null }),
      write: (call) => {
        paused = !call.url.endsWith("/resume");
        if (!call.url.endsWith("/recall")) return Response.json({});
        return Response.json({
          recalled: 1,
          items: [
            { slug: "receipt-total", youtube_video_id: "ShortVid001", recalled: true, detail: "已經取消排程，影片保持私人" },
            { slug: "menu-photo", youtube_video_id: "ShortVid002", recalled: false, detail: "已經公開了；要下架請在 Studio 處理" },
          ],
        });
      },
    });
    tab();
    const top = await screen.findByRole("region", { name: "Shorts 現況" });
    fireEvent.click(within(top).getByRole("button", { name: "暫停" }));
    expect(await within(top).findByRole("button", { name: "繼續" })).toBeTruthy();
    expect(top.textContent).toContain("暫停中");
    fireEvent.click(within(top).getByRole("button", { name: "繼續" }));
    expect(await within(top).findByRole("button", { name: "暫停" })).toBeTruthy();

    const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValue(true);
    fireEvent.click(within(top).getByRole("button", { name: "撤回已排程的" }));
    expect(paths(calls).filter((path) => path.startsWith("POST"))).toEqual(["POST /admin/video-shorts/pause", "POST /admin/video-shorts/resume"]);
    fireEvent.click(within(top).getByRole("button", { name: "撤回已排程的" }));
    const answer = await within(top).findByRole("status");
    expect(answer.textContent).toContain("撤回了 1 支，自動上架已暫停");
    expect(answer.textContent).toContain("已經公開了；要下架請在 Studio 處理");
    expect(paths(calls)).toContain("POST /admin/video-shorts/recall");
    confirm.mockRestore();
  });

  it("gives a reader no switch, and sends someone without a channel to link one", async () => {
    stubFetch({ overview: { ...overview, autopublish: "off", channel: { linked: false, title: null, audited: false, problem: null }, consent_expires_at: null } });
    window.history.replaceState(null, "", "/?tab=shorts&view=costs");
    tab(["content.read"]);
    const top = await screen.findByRole("region", { name: "Shorts 現況" });
    expect(within(top).queryByRole("button", { name: "暫停" })).toBeNull();
    expect(within(top).queryByRole("button", { name: "撤回已排程的" })).toBeNull();
    expect(top.textContent).toContain("沒有授權");
    expect(top.textContent).toContain("還沒有連結");
    fireEvent.click(within(top).getByRole("button", { name: "到設定分頁連結" }));
    expect(window.location.search).toContain("tab=settings");
    expect(window.location.search).not.toContain("view=");
    // With no channel there is nowhere to upload to: the files are not asked for.
    expect(screen.queryByRole("region", { name: "等你上傳" })).toBeNull();
  });
});

describe("what waits for the owner", () => {
  it("is a sentence each, with the button that goes and does it", async () => {
    stubFetch();
    const onOpenVideo = tab();
    const needs = await screen.findByRole("region", { name: "需要你" });
    const items = within(needs).getAllByRole("listitem");
    expect(items.map((item) => item.textContent)).toEqual([
      "接下來 10 天有 2 支等你上傳到 YouTube Studio看要上傳的檔案",
      "「掃描發票」的自動品管沒有全過，等你決定打開這支",
      "主機工人已經 42 分鐘沒有回報",
      "這 30 天已經花了 NT$2,400看花費",
    ]);
    fireEvent.click(within(items[1]).getByRole("button", { name: "打開這支" }));
    expect(onOpenVideo).toHaveBeenCalledWith("invoice-scan");
    fireEvent.click(within(items[3]).getByRole("button", { name: "看花費" }));
    await waitFor(() => expect(window.location.search).toContain("view=costs"));
  });

  it("says so when nothing waits", async () => {
    stubFetch({ overview: { ...overview, needs: [], needs_count: 0 } });
    tab();
    expect(await screen.findByText("現在沒有等你處理的事。")).toBeTruthy();
  });
});

describe("the files the owner uploads", () => {
  it("lists them, downloads them as one archive and says what the channel had", async () => {
    const calls = stubFetch({
      write: () => Response.json({
        claimed: 1,
        items: [
          { slug: "receipt-total", file_name: "mokaair-short-receipt-total.mp4", result: "matched", detail: "對到了", youtube_video_id: "ShortVid001" },
          { slug: "menu-photo", file_name: "mokaair-short-menu-photo.mp4", result: "length_differs", detail: "上傳的那一支長 52 秒，成片是 35.2 秒：不是同一個檔", youtube_video_id: "ShortVid002" },
        ],
      }),
    });
    tab();
    const panel = await screen.findByRole("region", { name: "等你上傳" });
    const rows = within(panel).getAllByRole("row").slice(1);
    expect(rows).toHaveLength(2);
    expect(rows[0].textContent).toContain("mokaair-short-receipt-total.mp4");
    expect(rows[0].textContent).toContain("35.2 秒");
    expect(rows[0].textContent).toContain("6.4 MB");
    expect(rows[1].textContent).toContain("長片精華");
    expect(within(panel).getAllByRole("listitem")).toHaveLength(3);
    const download = within(panel).getByRole("link", { name: "下載這一批（zip）" });
    expect(download.getAttribute("href")).toBe(BATCH_URL);
    expect(BATCH_URL).toBe("/api/admin-video-shorts/batch");
    fireEvent.click(within(panel).getByRole("button", { name: "我上傳好了" }));
    const answer = await within(panel).findByRole("status");
    expect(paths(calls)).toContain("POST /admin/video-shorts/uploads/claim");
    expect(answer.textContent).toContain("找到 1 支");
    expect(answer.textContent).toContain("對到了");
    expect(answer.textContent).toContain("長度不符");
    expect(answer.textContent).toContain("上傳的那一支長 52 秒");
  });

  it("is not asked for once the API audit passed, and a reader is given no button", async () => {
    stubFetch({ overview: { ...overview, channel: { ...overview.channel, audited: true } } });
    const { unmount } = render(<AdminVideoShorts onOpenVideo={vi.fn()} />);
    await screen.findByRole("region", { name: "Shorts 現況" });
    expect(screen.queryByRole("region", { name: "等你上傳" })).toBeNull();
    unmount();
    stubFetch();
    tab(["content.read"]);
    const panel = await screen.findByRole("region", { name: "等你上傳" });
    expect(within(panel).queryByRole("link")).toBeNull();
    expect(within(panel).queryByRole("button")).toBeNull();
  });
});

describe("the library", () => {
  it("groups the Shorts by where each stands, what waits for the owner first", async () => {
    window.history.replaceState(null, "", "/?view=library");
    stubFetch();
    const onOpenVideo = tab();
    const groups = await screen.findAllByRole("region", { name: /^(需要你|製作中|片庫|錯過時段，等下一個空格|已排時段)$/ });
    // "Needs you" is also the name of the list above the views.
    expect(groups.map((group) => group.getAttribute("aria-label")).slice(-5)).toEqual(["需要你", "製作中", "片庫", "錯過時段，等下一個空格", "已排時段"]);
    const slotted = screen.getByRole("region", { name: "已排時段" });
    const card = within(slotted).getByRole("button", { name: "打開 AI 真的可以算對發票嗎" });
    expect(card.textContent).toContain("已排時段");
    expect(card.textContent).toContain("實測");
    expect(card.textContent).toContain("系列 daily");
    expect(card.textContent).toContain("排在");
    await waitFor(() => expect(card.textContent).toContain("品管 12 項全過"));
    expect(card.textContent).toContain("35.2 秒");
    expect(within(card).getByRole("img", { name: "AI 真的可以算對發票嗎 的封面" }).getAttribute("src")).toBe(`/api/admin-video-files/receipt-total/${SHA.cover}`);
    // The cover's box has a height of its own; one sized by aspect-ratio, in a button, stopped a browser.
    const cover = within(card).getByTestId("shorts-card-cover");
    expect(cover.className).toContain("h-32");
    expect(cover.className).not.toContain("aspect-");
    const drama = screen.getByRole("button", { name: "打開 第三集的短篇" });
    expect(drama.textContent).toContain("漫劇直式短篇");
    expect(drama.textContent).toContain("來源 wenjian-e03");
    expect(drama.textContent).toContain("還沒有時段");
    fireEvent.click(card);
    expect(onOpenVideo).toHaveBeenCalledWith("receipt-total");
  });

  it("shows a dozen of a group and more on request", async () => {
    window.history.replaceState(null, "", "/?view=library");
    stubFetch({ shorts: Array.from({ length: 15 }, (_each, index) => short(`in-library-${index}`, `片庫第 ${index + 1} 支`, "library")) });
    tab();
    const library = await screen.findByRole("region", { name: "片庫" });
    expect(within(library).getAllByRole("listitem")).toHaveLength(12);
    fireEvent.click(within(library).getByRole("button", { name: "再看 3 支" }));
    expect(within(library).getAllByRole("listitem")).toHaveLength(15);
    expect(within(library).queryByRole("button", { name: /再看/ })).toBeNull();
  });

  it("says so when there is no Short yet", async () => {
    window.history.replaceState(null, "", "/?view=library");
    stubFetch({ shorts: [] });
    tab();
    expect(await screen.findByText("還沒有 Shorts")).toBeTruthy();
  });
});

describe("one Short's page", () => {
  it("plays the cut whole at nine to sixteen, with what the Shorts interface covers on request", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?tab=shorts&video=receipt-total");
    const { container } = page();
    const frame = await screen.findByTestId("shorts-frame");
    expect(frame.className).toContain("aspect-[9/16]");
    expect(frame.className).toContain("max-w-[min(22.5rem,45vh)]");
    const video = frame.querySelector("video") as HTMLVideoElement;
    expect(video.getAttribute("src")).toBe(`/api/admin-video-files/receipt-total/${SHA.final}`);
    expect(video.className).toContain("object-contain");
    expect(container.querySelector("video.aspect-video")).toBeNull();
    expect(screen.queryByTestId("shorts-cover")).toBeNull();
    fireEvent.click(screen.getByLabelText("顯示 Shorts 介面會蓋住的範圍"));
    const cover = screen.getByTestId("shorts-cover");
    const insets = [...cover.querySelectorAll("span")].map((part) => [part.style.left, part.style.top, part.style.right, part.style.bottom]);
    // The buttons right of x 902, the titles below y 1600, the cards inside x 78 to 902 above y 1380.
    expect(insets).toEqual([["83.519%", "0%", "0%", "0%"], ["0%", "83.333%", "0%", "0%"], ["7.222%", "0%", "16.481%", "28.125%"]]);
  });

  it("names the line, the state and the slot, the two titles, the twelve checks and the evidence", async () => {
    stubFetch({ project: { ...shorts[2], reviews: [{ ...finalReview, status: "pending", decided_at: null, note: null }] } });
    window.history.replaceState(null, "", "/?tab=shorts&video=receipt-total");
    page();
    const facts = await screen.findByLabelText("這支 Shorts");
    expect(facts.textContent).toContain("實測");
    expect(facts.textContent).toContain("已排時段");
    expect(facts.textContent).toContain("系列 daily");
    const card = screen.getByRole("article", { name: "成片" });
    expect(card.textContent).toContain("三張發票，AI 算對幾張");
    expect(card.textContent).toContain("使用中");
    expect(card.textContent).toContain("備案");
    expect(card.textContent).toContain("12 項全過");
    for (const label of ["規格", "響度", "版面", "證據", "多樣性", "揭露"]) expect(card.textContent).toContain(label);
    fireEvent.click(within(card).getByText(/原始證據/, { selector: "summary" }));
    const evidence = within(card).getByRole("row", { name: /result/ });
    expect(evidence.textContent).toContain(SHA.evidence);
    expect(within(evidence).getByRole("link", { name: "下載" }).getAttribute("href")).toBe(`/api/admin-video-files/receipt-total/${SHA.evidence}`);
    // A Short's languages are the Shorts settings', so the page does not ask for them here.
    expect(screen.queryByRole("region", { name: "這支影片的語言" })).toBeNull();
  });

  it("says where a Short stands once, in the Shorts' own words, and asks for no languages", async () => {
    const approved = { ...shorts[0], locales: {}, locales_decided_at: null, languages: {}, ready_to_upload: false, reviews: [finalReview] } as unknown as Project;
    const ready: Project = { ...approved, publish_approved_at: "2026-10-01T00:00:00Z", ready_to_upload: true };
    const scheduled: Project = { ...ready, shorts_state: "scheduled", youtube_video_id: "ShortVid001", youtube_publish_at: "2999-01-01T00:00:00Z", ready_to_upload: false };
    for (const each of [approved, ready, scheduled, { ...scheduled, youtube_publish_at: "2026-01-01T00:00:00Z" }]) expect(publishState(each)).toBeNull();
    expect(needsOwner(approved)).toBe(false);
    // A tutorial in the same places has the publish flow's states.
    expect(publishState({ ...approved, shorts_line: null })).toBe("deciding");
    expect(publishState({ ...ready, shorts_line: null, locales_decided_at: "2026-10-01T00:00:00Z" })).toBe("ready");
    expect(publishState({ ...scheduled, shorts_line: null })).toBe("scheduled");

    stubFetch({ project: scheduled });
    window.history.replaceState(null, "", "/?tab=shorts&video=in-library");
    page();
    const facts = await screen.findByLabelText("這支 Shorts");
    expect(facts.textContent).toContain("已排程");
    for (const pill of ["等你決定語言", "語言製作中", "可以上架", "已排定", "已上架"]) expect(screen.queryByText(pill)).toBeNull();
  });

  it("opens the video a highlight or a vertical short was cut from", async () => {
    stubFetch({ project: { ...shorts[4], reviews: [] } });
    window.history.replaceState(null, "", "/?tab=shorts&video=episode-cut");
    page();
    fireEvent.click(await screen.findByRole("button", { name: "打開 wenjian-e03" }));
    await waitFor(() => expect(window.location.search).toContain("video=wenjian-e03"));
  });

  it("leaves a tutorial's player at sixteen to nine", async () => {
    const tutorial = { slug: "ai-model-choice", title: "AI 模型怎麼挑", stage: "final", youtube_video_id: null, last_synced_at: "2026-09-25T05:00:00Z", pending: 1, checklist: [] };
    stubFetch({ project: { ...tutorial, reviews: [{ ...finalReview, payload: {}, status: "pending" }] } });
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    const { container } = page();
    await screen.findByRole("article", { name: "成片" });
    expect(container.querySelector("video")?.className).toContain("aspect-video");
    expect(screen.queryByTestId("shorts-frame")).toBeNull();
    expect(screen.queryByLabelText("這支 Shorts")).toBeNull();
    expect(screen.getByRole("region", { name: "這支影片的語言" })).toBeTruthy();
  });
});
