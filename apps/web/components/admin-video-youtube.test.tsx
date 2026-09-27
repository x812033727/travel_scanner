import { act, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import type { ProjectSummary } from "./admin-video-review-card";
import { RELOAD_AFTER_MS, type Connection, type SyncRecord, YouTubeConnectionCard, YouTubeSyncCard } from "./admin-video-youtube";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const CONNECTION = "/api/travel/admin/video-youtube/connection";
const unlinked: Connection = {
  configured: true, connected: false, channel_id: null, channel_title: null, connected_at: null,
  redirect_uri: "https://mokaair.com/api/travel/admin/video-youtube/connection/callback", scope: "https://www.googleapis.com/auth/youtube.force-ssl",
};
const linked: Connection = { ...unlinked, connected: true, channel_id: "UCabc", channel_title: "Mokaair", connected_at: "2026-09-27T09:00:00Z" };

/** A fetch that answers the connection routes and remembers what was sent. */
function stubFetch(state: Connection) {
  const calls: Array<{ url: string; method: string; body: unknown }> = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    calls.push({ url, method, body: init?.body ? JSON.parse(String(init.body)) : null });
    if (url.endsWith(`${CONNECTION}/start`)) return Promise.resolve(Response.json({ authorization_url: "https://accounts.google.com/o/oauth2/v2/auth?state=s", expires_in: 600 }));
    if (url.endsWith(CONNECTION) && method === "DELETE") return Promise.resolve(Response.json({ ...state, connected: false, channel_id: null, channel_title: null, connected_at: null }));
    if (url.endsWith(CONNECTION)) return Promise.resolve(Response.json(state));
    return Promise.resolve(Response.json({ code: "not_found" }, { status: 404 }));
  }));
  return calls;
}

const card = (capabilities: string[]) => render(<AdminOperationsProvider bootstrap={bootstrap(capabilities)}><YouTubeConnectionCard /></AdminOperationsProvider>);
const owner = ["content.read", "content.manage", "roles.manage"];

beforeEach(() => window.history.replaceState(null, "", "/zh-TW/admin/videos?tab=settings&section=shared"));
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.useRealTimers(); });

describe("YouTubeConnectionCard", () => {
  it("tells the owner to fill in the client first, and shows the redirect URI to register", async () => {
    stubFetch({ ...unlinked, configured: false });
    card(owner);
    const region = await screen.findByRole("region", { name: "YouTube 頻道" });
    await within(region).findByText("還沒連結");
    expect(within(region).getByText(/先在供應商卡填 YouTube OAuth 用戶端 ID 與密鑰/)).toBeTruthy();
    expect(within(region).getByRole("link", { name: "Azure 語音（影片旁白）卡" }).getAttribute("href")).toBe("/admin/ai-accounts");
    expect(within(region).getByText(unlinked.redirect_uri).tagName).toBe("CODE");
    expect(within(region).getByRole("button", { name: "連結 YouTube 頻道" })).toHaveProperty("disabled", true);
    expect(within(region).queryByRole("button", { name: "撤銷連結" })).toBeNull();
  });

  it("sends the owner to Google with the page to come back to, and reads the outcome from the address", async () => {
    // jsdom has no navigation: the assign is reported on the console, which this test expects.
    vi.spyOn(console, "error").mockImplementation(() => undefined);
    const calls = stubFetch(unlinked);
    card(owner);
    const connect = await screen.findByRole("button", { name: "連結 YouTube 頻道" });
    expect(connect).toHaveProperty("disabled", false);
    expect(screen.queryByText(/只有站主能連結或撤銷/)).toBeNull();
    fireEvent.click(connect);
    await vi.waitFor(() => expect(calls.some((call) => call.url.endsWith(`${CONNECTION}/start`))).toBe(true));
    const started = calls.find((call) => call.url.endsWith(`${CONNECTION}/start`));
    expect(started).toMatchObject({ method: "POST", body: { next_path: "/zh-TW/admin/videos?tab=settings&section=shared" } });
    expect(connect).toHaveProperty("disabled", true);
  });

  it("says when the consent came back, or which error Google named", async () => {
    stubFetch(linked);
    window.history.replaceState(null, "", "/zh-TW/admin/videos?tab=settings&section=shared&youtube=connected");
    const first = card(owner);
    expect((await screen.findByRole("status")).textContent).toBe("已連結完成。");
    first.unmount();
    window.history.replaceState(null, "", "/zh-TW/admin/videos?tab=settings&section=shared&youtube=access_denied");
    card(owner);
    expect((await screen.findByRole("alert")).textContent).toBe("連結沒有完成：access_denied");
  });

  it("shows the connected channel and lets the owner revoke it after confirming", async () => {
    const calls = stubFetch(linked);
    vi.spyOn(window, "confirm").mockReturnValue(false);
    card(owner);
    const region = await screen.findByRole("region", { name: "YouTube 頻道" });
    await within(region).findByText("已連結");
    expect(within(region).getByText(/Mokaair，.*連結/)).toBeTruthy();
    const revoke = within(region).getByRole("button", { name: "撤銷連結" });
    expect(within(region).queryByRole("button", { name: "連結 YouTube 頻道" })).toBeNull();
    fireEvent.click(revoke);
    expect(calls.filter((call) => call.method === "DELETE")).toHaveLength(0);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    fireEvent.click(revoke);
    await within(region).findByText("還沒連結");
    expect(calls.filter((call) => call.method === "DELETE").map((call) => call.url)).toEqual([CONNECTION]);
    expect(within(region).getByRole("button", { name: "連結 YouTube 頻道" })).toBeTruthy();
  });

  it("keeps a content manager reading: the buttons stay disabled and say why", async () => {
    stubFetch(linked);
    card(["content.read", "content.manage"]);
    const region = await screen.findByRole("region", { name: "YouTube 頻道" });
    await within(region).findByText("已連結");
    expect(within(region).getByText("只有站主能連結或撤銷：這是站主自己的 Google 帳號。")).toBeTruthy();
    expect(within(region).getByRole("button", { name: "撤銷連結" })).toHaveProperty("disabled", true);
  });
});

const project: ProjectSummary = {
  slug: "ai-model-choice", title: "AI 模型怎麼挑", stage: "done", youtube_video_id: "dQw4w9WgXcQ",
  last_synced_at: "2026-09-27T05:00:00Z", pending: 0, checklist: [],
};
const record: SyncRecord = {
  at: "2026-09-27T09:30:00Z", video_id: "dQw4w9WgXcQ", reason: "linked", ok: false,
  steps: [
    { id: "video", ok: true, detail: "標題與說明：zh-TW、en；不用揭露" },
    { id: "schedule", ok: false, detail: "影片現在是 public，不是私人" },
    { id: "captions", ok: true, detail: "字幕：新上傳 en；已有 zh-TW" },
    { id: "mystery", ok: true, detail: "an id this page does not know" },
  ],
  localizations: ["en"], captions: ["zh-TW", "en"], scheduled_at: null, thumbnail_sha256: null,
};

describe("YouTubeSyncCard", () => {
  it("lists what was sent and how each step went, and names the steps it knows", () => {
    render(<YouTubeSyncCard slug="ai-model-choice" project={{ ...project, youtube_sync: record }} canManage onSynced={vi.fn()} />);
    const region = screen.getByRole("region", { name: "送到 YouTube 的東西" });
    expect(within(region).getByText("沒有全部送成")).toBeTruthy();
    expect(within(region).getByText(/上次送出 .*（貼上網址後）/)).toBeTruthy();
    const items = [...region.querySelectorAll("li")].map((item) => item.textContent);
    expect(items).toEqual([
      "標題與說明 標題與說明：zh-TW、en；不用揭露",
      "上架時間 影片現在是 public，不是私人",
      "字幕 字幕：新上傳 en；已有 zh-TW",
      "mystery an id this page does not know",
    ]);
    expect(within(region).queryByText(/已在 YouTube 排定/)).toBeNull();
  });

  it("says when nothing was sent yet, and when the video is scheduled", () => {
    const { unmount } = render(<YouTubeSyncCard slug="ai-model-choice" project={project} canManage={false} onSynced={vi.fn()} />);
    expect(screen.getByText("還沒送過。")).toBeTruthy();
    expect(screen.getByRole("button", { name: "重送到 YouTube" })).toHaveProperty("disabled", true);
    unmount();
    const scheduled = { ...record, ok: true, reason: "languages", steps: [{ id: "schedule", ok: true, detail: "排定" }], scheduled_at: "2026-10-01T12:00:00Z" };
    render(<YouTubeSyncCard slug="ai-model-choice" project={{ ...project, youtube_sync: scheduled }} canManage onSynced={vi.fn()} />);
    expect(screen.getByText("已送出")).toBeTruthy();
    expect(screen.getByText(/（語言批次送到後）/)).toBeTruthy();
    expect(screen.getByText(/已在 YouTube 排定 .* 公開/)).toBeTruthy();
  });

  it("queues a send again and reads the page once the queue has had its seconds", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    const posts: string[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      posts.push(`${init?.method} ${String(input)}`);
      return Promise.resolve(Response.json({ ...project, youtube_sync: record }, { status: 202 }));
    }));
    const onSynced = vi.fn();
    render(<YouTubeSyncCard slug="ai-model-choice" project={{ ...project, youtube_sync: record }} canManage onSynced={onSynced} />);
    fireEvent.click(screen.getByRole("button", { name: "重送到 YouTube" }));
    expect((await screen.findByRole("status")).textContent).toBe("已排入，幾秒後這頁會更新。");
    expect(posts).toEqual(["POST /api/travel/admin/video-youtube/ai-model-choice/sync"]);
    expect(onSynced).not.toHaveBeenCalled();
    await act(async () => { await vi.advanceTimersByTimeAsync(RELOAD_AFTER_MS); });
    expect(onSynced).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("status")).toBeNull();
  });

  it("shows why a send was refused", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json({ code: "video_youtube_not_linked", detail: "還沒有 YouTube 影片 id" }, { status: 409 }))));
    render(<YouTubeSyncCard slug="ai-model-choice" project={project} canManage onSynced={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "重送到 YouTube" }));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("沒有排入：");
    expect(alert.textContent).toContain("還沒有 YouTube 影片 id");
  });
});
