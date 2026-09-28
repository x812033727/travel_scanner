import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { YoutubeManualUpload } from "./admin-video-manual-upload";
import { type Project, type Review, type YoutubeSync } from "./admin-video-review-card";
import { type YoutubeConnection, YoutubePublishForm, YoutubeSyncPanel } from "./admin-video-youtube";

const ID = "abcdefghijk";
const hash = (n: number) => String(n).repeat(64);
const review: Review = {
  id: "approved-package", gate: "publish", status: "approved", content_sha256: hash(1), summary: "Upload",
  payload: { zh: { title: "核准標題", description: "完整說明\n00:00 開場", tags: ["AI", "測試"] }, locales: ["zh-TW", "zh-CN", "en", "ja", "ko"], disclosure: { synthetic: false } },
  files: [
    { role: "final", sha256: hash(2), size: 30000, content_type: "video/mp4" },
    { role: "preview", sha256: hash(3), size: 5000, content_type: "video/mp4" },
    { role: "thumbnail", sha256: hash(4), size: 500, content_type: "image/png" },
    { role: "metadata", sha256: hash(5), size: 800, content_type: "application/json" },
    ...["zh_tw", "zh-CN", "en", "ja", "ko"].map((locale, i) => ({ role: `captions_${locale}`, sha256: hash(i + 5), size: 100, content_type: locale === "ja" ? "text/vtt" : "text/plain" })),
    { role: "description_en", sha256: hash(9), size: 100, content_type: "text/plain" },
  ],
  choice: null, note: null, created_at: "2026-09-28T00:00:00Z", decided_at: "2026-09-28T00:00:00Z",
};
const metadata = {
  title: "核准標題", description: "完整說明\n00:00 開場", tags: ["AI", "測試"], default_language: "zh-TW",
  made_for_kids: true, contains_synthetic_media: false, category_id: 28,
  localizations: {
    en: { title: "English title", description: "Description\n00:00 Introduction\nhttps://example.com" },
    ja: { title: "日本語", description: "日本語の説明" },
    ko: { title: "한국어", description: "한국어 설명" },
    "zh-CN": { title: "简体标题", description: "简体说明" },
  },
};
const sync: YoutubeSync = {
  status: "failed", interrupted: false, request: { mode: "upload", title: "上次自訂標題", description: "上次自訂說明" },
  steps: [{ id: "upload", state: "done", detail: ID, at: null }, { id: "captions", state: "failed", detail: "quotaExceeded", at: null }],
  progress: null, error: "quotaExceeded", started_at: null, finished_at: null,
};
const project: Project = {
  slug: "test-video", title: "Test video", stage: "publish", checklist: [], youtube_video_id: null,
  pending: 0, last_synced_at: "2026-09-28T00:00:00Z", reviews: [review],
};
function stub(value: Project = project, meta: unknown = metadata) {
  return vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
    const url = String(input);
    if (url === "/api/travel/admin/videos/test-video") return Promise.resolve(Response.json(value));
    if (url === `/api/admin-video-files/test-video/${hash(5)}`) return Promise.resolve(meta instanceof Response ? meta : Response.json(meta));
    throw new Error(`Unexpected request: ${url}`);
  }));
}
async function open() {
  fireEvent.click(screen.getByRole("button", { name: "手動模式：下載檔案與複製文字" }));
  return screen.findByRole("region", { name: "1. 開啟或上傳影片" });
}
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("manual YouTube upload", () => {
  it("opens from a quota failure, targets the existing video and only reads site resources", async () => {
    stub({ ...project, youtube_video_id: ID, youtube_sync: sync });
    const writeText = vi.fn().mockResolvedValue(undefined);
    vi.stubGlobal("navigator", { clipboard: { writeText }, language: "zh-TW" });
    render(<YoutubeSyncPanel slug={project.slug} sync={sync} canManage onChange={vi.fn()} />);
    expect(fetch).not.toHaveBeenCalled();
    await open();
    expect(screen.getByRole("link", { name: "在 Studio 開啟這支影片" }).getAttribute("href")).toBe(`https://studio.youtube.com/video/${ID}/edit`);
    expect(screen.queryByRole("link", { name: /下載影片/ })).toBeNull();
    expect(screen.getByLabelText("標題")).toHaveProperty("value", "上次自訂標題");
    fireEvent.click(screen.getByRole("button", { name: "複製說明（含章節）" }));
    await screen.findByText("已複製。");
    expect(writeText).toHaveBeenCalledWith("上次自訂說明");
    expect(screen.getByRole("link", { name: "下載中文（台灣）字幕" }).getAttribute("download")).toBe("zh-TW.srt");
    expect(screen.getByRole("link", { name: "下載日文字幕" }).getAttribute("download")).toBe("ja.vtt");
    expect(screen.getByRole("link", { name: "下載縮圖" }).getAttribute("download")).toBe("thumbnail.png");
    expect(screen.getByText(/原本的「失敗／等待」可能仍保留/)).toBeTruthy();
    for (const [url, init] of vi.mocked(fetch).mock.calls) {
      expect(String(url).startsWith("/api/")).toBe(true);
      expect(init?.method ?? "GET").toBe("GET");
    }
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it("uses final.mp4, all locale text including chapters, and the package's audience setting", async () => {
    stub();
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    expect(screen.getByRole("link", { name: /下載影片/ }).getAttribute("href")).toBe(`/api/admin-video-files/test-video/${hash(2)}`);
    expect(screen.queryByRole("link", { name: /preview/ })).toBeNull();
    const writeText = vi.fn().mockResolvedValue(undefined);
    vi.stubGlobal("navigator", { clipboard: { writeText }, language: "zh-TW" });
    for (const [locale, value] of Object.entries(metadata.localizations)) {
      fireEvent.change(screen.getByRole("combobox", { name: "語言" }), { target: { value: locale } });
      expect(screen.getByLabelText("標題")).toHaveProperty("value", value.title);
      fireEvent.click(screen.getByRole("button", { name: "複製說明（含章節）" }));
      await waitFor(() => expect(writeText).toHaveBeenLastCalledWith(value.description));
    }
    expect(screen.getByText("是，這是兒童專屬的影片")).toBeTruthy();
    expect(screen.getByText("科學與技術（28）")).toBeTruthy();
    expect(screen.getByRole("link", { name: "description.en.txt" }).getAttribute("download")).toBe("description.en.txt");
  });

  it("switches the publish form to manual mode without sending and preserves edits on return", async () => {
    stub();
    const connection = { linked: true, audited: true, channel_title: "Mokaair" } as YoutubeConnection;
    render(<YoutubePublishForm slug={project.slug} review={review} connection={connection} canUpload onSent={vi.fn()} />);
    const form = screen.getByRole("form");
    fireEvent.change(within(form).getByLabelText("中文標題"), { target: { value: "正在編輯的新標題" } });
    await open();
    expect(screen.queryByRole("form")).toBeNull();
    expect(screen.getByLabelText("標題")).toHaveProperty("value", "正在編輯的新標題");
    fireEvent.click(screen.getByRole("button", { name: "返回 API 上傳" }));
    expect(within(screen.getByRole("form")).getByLabelText("中文標題")).toHaveProperty("value", "正在編輯的新標題");
    expect(vi.mocked(fetch).mock.calls.every(([, init]) => !init?.method || init.method === "GET")).toBe(true);
  });

  it("keeps available downloads and fallback text when metadata fails; copying failure is recoverable", async () => {
    stub(project, new Response("unavailable", { status: 503 }));
    vi.stubGlobal("navigator", { clipboard: { writeText: vi.fn().mockRejectedValue(new Error("denied")) }, language: "zh-TW" });
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    expect(screen.getByText(/部分文字或設定讀取失敗/)).toBeTruthy();
    expect(screen.getByLabelText("標題")).toHaveProperty("value", "核准標題");
    expect(screen.getByText("上傳包未指定，請依影片內容在 Studio 確認。")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "複製標題" }));
    await screen.findByText("無法複製，請選取文字框內的內容自行複製。");
    expect(screen.queryByText("已複製。")).toBeNull();
    fireEvent.change(screen.getByRole("combobox", { name: "語言" }), { target: { value: "en" } });
    expect(screen.getByText(/這個語言沒有可複製的說明/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "重新讀取上傳包" })).toBeTruthy();
  });

  it.each([
    ["unapproved", { ...project, reviews: [{ ...review, status: "pending" as const }] }, "這支影片還沒有已核准的上傳包"],
    ["running", { ...project, youtube_sync: { ...sync, status: "running" as const } }, "API 上傳或同步仍在進行中"],
    ["dropped", { ...project, dropped_at: "2026-09-28T00:00:00Z" }, "這支影片還沒有已核准的上傳包"],
  ])("does not offer stale uploads for %s projects", async (_name, value, message) => {
    stub(value);
    render(<YoutubeManualUpload slug={project.slug} />);
    fireEvent.click(screen.getByRole("button", { name: /手動模式/ }));
    expect((await screen.findByRole("alert")).textContent).toContain(message);
    expect(screen.queryByRole("link")).toBeNull();
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("uses the compilation download when the final file is outside the review store", async () => {
    stub({ ...project, compilation: true, download_available: true, reviews: [{ ...review, files: review.files.filter((file) => file.role !== "final") }] });
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    expect(screen.getByRole("link", { name: /下載影片/ }).getAttribute("href")).toBe("/api/admin-video-download/test-video");
  });

  it("explains missing final files and does not offer a preview as an upload", async () => {
    stub({ ...project, reviews: [{ ...review, files: review.files.filter((file) => file.role !== "final") }] });
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    expect(screen.getByText(/不要上傳預覽檔/)).toBeTruthy();
    expect(screen.queryByRole("link", { name: /下載影片/ })).toBeNull();
  });

  it("handles permission errors and hides the entry from read-only sync panels", async () => {
    const { unmount } = render(<YoutubeSyncPanel slug={project.slug} sync={sync} canManage={false} onChange={vi.fn()} />);
    expect(screen.queryByRole("button", { name: /手動模式/ })).toBeNull();
    unmount();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("denied", { status: 403 })));
    render(<YoutubeManualUpload slug={project.slug} />);
    fireEvent.click(screen.getByRole("button", { name: /手動模式/ }));
    expect((await screen.findByRole("alert")).textContent).toContain("讀取上傳包失敗");
    expect(screen.queryByRole("link")).toBeNull();
  });
});
