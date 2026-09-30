import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import type { Review, YoutubeSync } from "./admin-video-review-card";
import { AdminVideoReviews } from "./admin-video-reviews";
import { SYNC_POLL_MS, YoutubeChannelCard, type YoutubeConnection, YoutubePublishForm, YoutubeSyncPanel } from "./admin-video-youtube";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const CLIENT_ID = "123456789012-abcdefghijklmnop.apps.googleusercontent.com";
const empty: YoutubeConnection = {
  client_id: null, client_secret_set: false, redirect_uri: "https://mokaair.com/api/admin-video-youtube/callback",
  scope: "https://www.googleapis.com/auth/youtube.force-ssl", configured: false, linked: false,
  channel_id: null, channel_title: null, channel_url: null, linked_at: null, verified_at: null, problem: null, audited: false,
};
const linked: YoutubeConnection = {
  ...empty, client_id: CLIENT_ID, client_secret_set: true, configured: true, linked: true,
  channel_id: "UCfixturechannel0000000", channel_title: "Mokaair", channel_url: "https://www.youtube.com/channel/UCfixturechannel0000000",
  linked_at: "2026-09-27T05:00:00Z", verified_at: "2026-09-27T05:00:00Z",
};
const confirmation: Review = {
  id: "66666666-6666-4666-8666-666666666666", gate: "publish", content_sha256: "5".repeat(64), summary: "上傳包",
  payload: { zh: { title: "AI 模型怎麼挑：三個問題", description: "先把帳算清楚。", tags: ["AI"] }, locales: ["zh-TW", "en"] },
  files: [
    { role: "final", sha256: "6".repeat(64), size: 95_000_000, content_type: "video/mp4" },
    { role: "metadata", sha256: "5".repeat(64), size: 4_000, content_type: "application/json" },
  ],
  status: "approved", choice: null, note: null, decided_at: "2026-09-27T05:00:00Z", created_at: "2026-09-27T05:00:00Z",
};

type Call = { url: string; method: string; body: unknown };
function stub(answer: (url: string, method: string, body: unknown) => unknown) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    const body = init?.body ? JSON.parse(String(init.body)) : undefined;
    calls.push({ url, method, body });
    if (url.endsWith("/admin/video-youtube/vps/settings")) return Promise.resolve(Response.json({
      enabled: false, url: null, channel_id: null, desktop_url: null, secret_set: false, configured: false,
      source: "none", updated_at: null, last_test_status: null, last_test_message: null, last_tested_at: null,
    }));
    // The catalog under the groups (admin-video-browser.tsx) is not what these tests look at.
    const value = url.includes("/admin/videos/browse") ? { items: [], total: 0, page: 1, pages: 0, facets: { category: [], state: [] } } : answer(url, method, body);
    return Promise.resolve(value instanceof Response ? value : Response.json(value));
  }));
  return calls;
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  vi.useRealTimers();
  window.history.replaceState(null, "", "/");
});

describe("YoutubeChannelCard", () => {
  it("keeps VPS configuration available when the separate OAuth card cannot load", async () => {
    stub(() => Response.json({ detail: "OAuth unavailable" }, { status: 503 }));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><YoutubeChannelCard /></AdminOperationsProvider>);
    const vps = await screen.findByRole("region", { name: "VPS 上傳服務" });
    await within(vps).findByLabelText("服務密鑰");
    expect(vps.id).toBe("youtube-vps-settings");
    expect(vps.previousElementSibling?.getAttribute("aria-labelledby")).toBe("video-settings-youtube");
    expect((await screen.findByRole("alert")).textContent).toContain("OAuth unavailable");
  });

  it("walks the owner through Google Cloud, keeps the secret write-only, and only links once the client is saved", async () => {
    let current = empty;
    const calls = stub((url, method, body) => {
      if (method === "PUT") {
        current = { ...current, client_id: (body as { client_id: string }).client_id, client_secret_set: true, configured: true };
        return current;
      }
      return current;
    });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><YoutubeChannelCard /></AdminOperationsProvider>);
    const card = await screen.findByRole("region", { name: "YouTube 頻道" });
    expect(card.textContent).toContain("未連結");
    expect(card.textContent).toContain("https://mokaair.com/api/admin-video-youtube/callback");
    expect(card.textContent).toContain("youtube.force-ssl");
    expect(card.textContent).toContain("正式版");
    const link = within(card).getByRole("button", { name: "連結 YouTube 頻道" });
    expect(link).toHaveProperty("disabled", true);

    const save = within(card).getByRole("button", { name: "儲存" });
    fireEvent.change(within(card).getByLabelText("用戶端 ID"), { target: { value: "not-a-client" } });
    expect(card.textContent).toContain("看起來不像網頁應用程式的用戶端 ID");
    fireEvent.change(within(card).getByLabelText("用戶端 ID"), { target: { value: ` ${CLIENT_ID} ` } });
    expect(save).toHaveProperty("disabled", true);
    fireEvent.change(within(card).getByLabelText("用戶端密鑰"), { target: { value: "GOCSPX-secret-value" } });
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);
    await waitFor(() => expect(calls.some((call) => call.method === "PUT")).toBe(true));
    expect(calls.find((call) => call.method === "PUT")?.body).toEqual({ client_id: CLIENT_ID, client_secret: "GOCSPX-secret-value", audited: false });
    const start = await within(card).findByRole("link", { name: "連結 YouTube 頻道" });
    expect(start.getAttribute("href")).toBe("/api/admin-video-youtube/start?locale=zh-TW");
    expect((within(card).getByLabelText("用戶端密鑰") as HTMLInputElement).value).toBe("");
    expect((within(card).getByLabelText("用戶端密鑰") as HTMLInputElement).placeholder).toBe("已設定；留空就不變");
  });

  it("shows the linked channel, and unlinks after a confirmation", async () => {
    let current = linked;
    const calls = stub((url, method) => {
      if (url.endsWith("/unlink") && method === "POST") {
        current = { ...linked, linked: false, channel_id: null, channel_title: null, channel_url: null, linked_at: null, verified_at: null };
        return { revoked: true, connection: current };
      }
      return current;
    });
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><YoutubeChannelCard /></AdminOperationsProvider>);
    const card = await screen.findByRole("region", { name: "YouTube 頻道" });
    await waitFor(() => expect(card.textContent).toContain("已連結"));
    const channel = within(card).getByRole("link", { name: /Mokaair/ });
    expect(channel.getAttribute("href")).toBe("https://www.youtube.com/channel/UCfixturechannel0000000");
    expect(within(card).getByRole("link", { name: "重新連結" })).toBeTruthy();
    fireEvent.click(within(card).getByRole("button", { name: "解除連結" }));
    expect(confirm).toHaveBeenCalledOnce();
    await waitFor(() => expect(calls.some((call) => call.url.endsWith("/admin/video-youtube/unlink"))).toBe(true));
    expect(await within(card).findByText("已解除連結。")).toBeTruthy();
    expect(card.textContent).toContain("未連結");
  });

  it("reads the outcome Google's callback left in the address", async () => {
    stub(() => empty);
    window.history.replaceState(null, "", "/?tab=settings&youtube_error=video_youtube_scope_missing");
    const { unmount } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><YoutubeChannelCard /></AdminOperationsProvider>);
    expect((await screen.findByRole("alert")).textContent).toContain("沒有勾 YouTube 的權限");
    unmount();
    window.history.replaceState(null, "", "/?tab=settings&youtube=linked");
    stub(() => linked);
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><YoutubeChannelCard /></AdminOperationsProvider>);
    expect(await screen.findByText("已連結頻道。")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "知道了" }));
    expect(window.location.search).toBe("?tab=settings");
  });

  it("lets a content reviewer read the card but not change or link it", async () => {
    stub(() => ({ ...linked, linked: false }));
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><YoutubeChannelCard /></AdminOperationsProvider>);
    const card = await screen.findByRole("region", { name: "YouTube 頻道" });
    await waitFor(() => expect(within(card).getByLabelText("用戶端 ID")).toHaveProperty("disabled", true));
    expect(within(card).getByRole("button", { name: "連結 YouTube 頻道" })).toHaveProperty("disabled", true);
    expect(within(card).queryByRole("link", { name: "連結 YouTube 頻道" })).toBeNull();
  });
});

describe("YoutubePublishForm", () => {
  it("defaults to a Studio upload before the audit, and an upload by the site needs the owner's yes", async () => {
    const calls = stub(() => ({}));
    const sent = vi.fn();
    render(<YoutubePublishForm slug="ai-model-choice" review={confirmation} connection={linked} canUpload onSent={sent} />);
    const form = screen.getByRole("form", { name: "送到 YouTube" });
    expect(form.textContent).toContain("Mokaair");
    expect((within(form).getByRole("radio", { name: /我已經在 Studio 上傳/ }) as HTMLInputElement).checked).toBe(true);
    expect((within(form).getByLabelText("中文標題") as HTMLInputElement).value).toBe("AI 模型怎麼挑：三個問題");
    expect((within(form).getByLabelText("中文說明欄") as HTMLTextAreaElement).value).toBe("先把帳算清楚。");
    const send = within(form).getByRole("button", { name: "送到 YouTube" });
    expect(send).toHaveProperty("disabled", true);

    fireEvent.click(within(form).getByRole("radio", { name: "由網站上傳 mp4" }));
    expect(form.textContent).toContain("鎖成私人");
    fireEvent.change(within(form).getByLabelText("公開時間"), { target: { value: "2030-01-02T20:00" } });
    expect(send).toHaveProperty("disabled", true);
    fireEvent.click(within(form).getByRole("checkbox", { name: /我知道這支會被鎖成私人/ }));
    expect(send).toHaveProperty("disabled", false);
    fireEvent.change(within(form).getByLabelText("中文標題"), { target: { value: "字".repeat(101) } });
    expect(form.textContent).toContain("標題最多 100 個字");
    expect(send).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByLabelText("中文標題"), { target: { value: "改過的標題" } });
    fireEvent.click(send);
    await waitFor(() => expect(sent).toHaveBeenCalledOnce());
    expect(calls[0].url).toContain("/api/travel/admin/videos/ai-model-choice/youtube/publish");
    expect(calls[0].body).toEqual({
      mode: "upload", url: null, visibility: "scheduled", publish_at: new Date("2030-01-02T20:00").toISOString(),
      title: "改過的標題", description: "先把帳算清楚。", accept_private_lock: true,
    });
  });

  it("sends a Studio video unlisted with no time, and shows a refusal in the owner's words", async () => {
    const calls = stub(() => Response.json({ code: "video_youtube_package_missing", detail: "審核區已經找不到這份上傳包" }, { status: 409 }));
    render(<YoutubePublishForm slug="ai-model-choice" review={confirmation} connection={{ ...linked, audited: true }} canUpload={false} onSent={vi.fn()} />);
    const form = screen.getByRole("form", { name: "送到 YouTube" });
    expect(within(form).queryByRole("radio", { name: "由網站上傳 mp4" })).toBeNull();
    fireEvent.change(within(form).getByLabelText("YouTube 網址或影片 id"), { target: { value: "https://studio.youtube.com/video/dQw4w9WgXcQ/edit" } });
    expect(form.textContent).toContain("影片 id：dQw4w9WgXcQ");
    fireEvent.click(within(form).getByRole("radio", { name: /不公開/ }));
    expect(within(form).queryByLabelText("公開時間")).toBeNull();
    fireEvent.click(within(form).getByRole("button", { name: "送到 YouTube" }));
    expect((await within(form).findByRole("alert")).textContent).toContain("審核區已經找不到這份上傳包");
    expect(calls[0].body).toMatchObject({ mode: "studio", url: "https://studio.youtube.com/video/dQw4w9WgXcQ/edit", visibility: "unlisted", publish_at: null });
  });
});

const failedSync: YoutubeSync = {
  status: "failed", interrupted: false,
  request: { mode: "studio", visibility: "scheduled", publish_at: "2030-01-02T12:00:00Z", title: "t", description: "d", video_id: "dQw4w9WgXcQ" },
  steps: [
    { id: "details", state: "done", detail: "標題、說明、5 個語系", at: "2026-09-27T05:00:00Z" },
    { id: "captions", state: "failed", detail: "今天的 YouTube API 配額用完了", at: "2026-09-27T05:00:01Z" },
    { id: "thumbnail", state: "pending", detail: "", at: null },
  ],
  progress: null, error: "今天的 YouTube API 配額用完了", queued_at: "2026-09-27T05:00:00Z", started_at: "2026-09-27T05:00:00Z", finished_at: "2026-09-27T05:00:02Z",
};

describe("YoutubeSyncPanel", () => {
  it("lists each step and retries a failed run", async () => {
    const calls = stub(() => ({}));
    const changed = vi.fn();
    render(<YoutubeSyncPanel slug="ai-model-choice" sync={failedSync} canManage onChange={changed} />);
    const panel = screen.getByRole("region", { name: "YouTube 同步" });
    expect(panel.textContent).toContain("失敗");
    expect(panel.textContent).toContain("標題、說明與排程 · 完成");
    expect(panel.textContent).toContain("字幕 · 失敗");
    expect(panel.textContent).toContain("縮圖 · 等待");
    expect(within(panel).getByRole("alert").textContent).toContain("配額用完");
    fireEvent.click(within(panel).getByRole("button", { name: "重試" }));
    await waitFor(() => expect(changed).toHaveBeenCalledOnce());
    expect(calls[0]).toMatchObject({ method: "POST" });
    expect(calls[0].url).toContain("/admin/videos/ai-model-choice/youtube/retry");
  });

  it("reads a running upload again every few seconds and shows its progress", () => {
    vi.useFakeTimers();
    const changed = vi.fn();
    const running: YoutubeSync = {
      ...failedSync, status: "running", error: null, finished_at: null,
      request: { ...failedSync.request, mode: "upload" },
      steps: [{ id: "upload", state: "running", detail: "", at: null }, ...failedSync.steps.map((step) => ({ ...step, state: "pending" as const }))],
      progress: { sent: 40_000_000, total: 95_000_000 },
    };
    render(<YoutubeSyncPanel slug="ai-model-choice" sync={running} canManage onChange={changed} />);
    expect(screen.getByRole("region", { name: "YouTube 同步" }).textContent).toContain("已上傳 40.0／95.0 MB（42%）");
    expect(screen.queryByRole("button", { name: "重試" })).toBeNull();
    act(() => { vi.advanceTimersByTime(SYNC_POLL_MS * 2); });
    expect(changed).toHaveBeenCalledTimes(2);
  });
});

describe("the ready card and the list with a linked channel", () => {
  it("offers the send form instead of the paste form, and lists a failed run under needs-you", async () => {
    const ready = { slug: "upload-ready", title: "上傳包影片", stage: "done", checklist: [], youtube_video_id: null, last_synced_at: "2026-09-27T05:00:00Z", pending: 0, publish_approved_at: "2026-09-27T05:00:00Z" };
    const stuck = { ...ready, slug: "stuck-sync", title: "送到一半的影片", youtube_video_id: "dQw4w9WgXcQ", youtube_sync: failedSync };
    stub((url) => {
      if (url.endsWith("/admin/video-youtube")) return linked;
      if (url.endsWith("/admin/videos?shorts=exclude")) return [ready, stuck];
      if (url.endsWith("/admin/videos/upload-ready")) return { ...ready, reviews: [confirmation] };
      return { ...stuck, reviews: [] };
    });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "上傳包影片" });
    const form = await within(card).findByRole("form", { name: "送到 YouTube" });
    expect(within(card).queryByRole("form", { name: "已上傳到 YouTube" })).toBeNull();
    // The card reads the package after the list; the form fills itself from it only once loaded.
    expect((within(form).getByLabelText("中文標題") as HTMLInputElement).value).toBe("AI 模型怎麼挑：三個問題");
    expect((within(form).getByLabelText("中文說明欄") as HTMLTextAreaElement).value).toBe("先把帳算清楚。");
    const needs = screen.getByRole("region", { name: "需要你" });
    expect(needs.textContent).toContain("送到一半的影片");
    expect(needs.textContent).toContain("YouTube 同步失敗");
  });

  it("keeps the paste form, with a pointer to the settings tab, while no channel is linked", async () => {
    const ready = { slug: "upload-ready", title: "上傳包影片", stage: "done", checklist: [], youtube_video_id: null, last_synced_at: "2026-09-27T05:00:00Z", pending: 0, publish_approved_at: "2026-09-27T05:00:00Z" };
    stub((url) => {
      if (url.endsWith("/admin/video-youtube")) return empty;
      if (url.endsWith("/admin/videos?shorts=exclude")) return [ready];
      // The settings tab's own form is not what this test reads.
      if (url.includes("/admin/video-automation/")) return new Response(null, { status: 404 });
      return { ...ready, reviews: [confirmation] };
    });
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "上傳包影片" });
    expect(await within(card).findByRole("form", { name: "已上傳到 YouTube" })).toBeTruthy();
    fireEvent.click(within(card).getByRole("button", { name: "到設定分頁連結" }));
    await waitFor(() => expect(window.location.search).toBe("?tab=settings"));
    expect(await screen.findByRole("region", { name: "YouTube 頻道" })).toBeTruthy();
  });
});
