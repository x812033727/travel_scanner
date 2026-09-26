import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
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

  it("marks a drama and its media spend in the list", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json([{ ...summary, pending: 0, format: "drama", media_usd: 12.5, clip_seconds: 96 }]))));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const item = await screen.findByRole("button", { name: /AI 模型怎麼挑/ });
    expect(item.textContent).toContain("AI 漫劇");
    expect(item.textContent).toContain("媒體花費 US$12.50（96 片段秒）");
  });

  it("marks a dropped video in the list", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json([{ ...summary, pending: 0, dropped_at: "2026-09-25T13:00:00Z" }]))));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const item = await screen.findByRole("button", { name: /AI 模型怎麼挑/ });
    expect(item.textContent).toContain("已放棄");
  });
});
