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
    { role: "thumbnail-b", sha256: "b".repeat(64), size: 500, content_type: "image/jpeg" },
    ...["en", "ja"].map((locale) => ({ role: `thumbnail_${locale}`, sha256: (locale === "en" ? "e" : "f").repeat(64), size: 500, content_type: "image/jpeg" })),
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
    expect(screen.getByRole("link", { name: "縮圖 英文" }).getAttribute("download")).toBe("thumbnail.en.jpg");
    expect(screen.getByRole("link", { name: "縮圖 日文" }).getAttribute("href")).toBe(`/api/admin-video-files/test-video/${"f".repeat(64)}`);
    expect(screen.queryByRole("link", { name: /縮圖 B/ })).toBeNull();
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

  it("offers one zip of every listed file under the names the single downloads use", async () => {
    stub();
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    const link = screen.getByRole("link", { name: "下載整包 zip（11 個檔案）" });
    expect(link.getAttribute("download")).toBe("test-video-upload.zip");
    const url = new URL(link.getAttribute("href") ?? "", "https://mokaair.com");
    expect(url.pathname).toBe("/api/admin-video-package/test-video");
    expect(url.searchParams.getAll("file")).toEqual([
      `${hash(2)}:final.mp4`, `${hash(4)}:thumbnail.png`, `${"e".repeat(64)}:thumbnail.en.jpg`, `${"f".repeat(64)}:thumbnail.ja.jpg`,
      `${hash(5)}:zh-TW.srt`, `${hash(6)}:zh-CN.srt`, `${hash(7)}:en.srt`, `${hash(8)}:ja.vtt`, `${hash(9)}:ko.srt`,
      `${hash(9)}:description.en.txt`, `${hash(5)}:metadata.json`,
    ]);
    expect(screen.queryByText(/不在審核區/)).toBeNull();
  });

  it("offers the dub tracks of the newest card not sent back, pending included, and puts them in the zip", async () => {
    const later = (seconds: number) => new Date(Date.parse(review.created_at) + seconds * 1000).toISOString();
    const card = (id: string, status: Review["status"], seconds: number, files: Review["files"]): Review => ({
      ...review, id, gate: "languages", status, created_at: later(seconds), decided_at: status === "pending" ? null : later(seconds), payload: { locales: {} }, files,
    });
    const pending = card("waiting-for-studio", "pending", 60, [
      { role: "dub_en", sha256: "1a".repeat(32), size: 9000, content_type: "audio/mp4" },
      { role: "dub_unchecked_ja", sha256: "2b".repeat(32), size: 9000, content_type: "audio/wav" },
      { role: "captions_th", sha256: "3c".repeat(32), size: 100, content_type: "text/plain" },
    ]);
    const rejected = card("sent-back", "rejected", 120, [{ role: "dub_ko", sha256: "4d".repeat(32), size: 9000, content_type: "audio/mpeg" }]);
    stub({ ...project, reviews: [rejected, pending, review] });
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    const step = screen.getByRole("region", { name: "6. 逐語言上傳配音音軌" });
    expect(within(step).getByRole("link", { name: "下載英文配音" }).getAttribute("download")).toBe("dub.en.m4a");
    expect(within(step).getByRole("link", { name: "下載日文配音（沒過自動檢查）" }).getAttribute("download")).toBe("dub.ja.unchecked.wav");
    expect(within(step).getByText(/上傳前請整條聽一遍/)).toBeTruthy();
    expect(screen.queryByRole("link", { name: /韓文配音/ })).toBeNull();
    expect(screen.queryByRole("link", { name: "下載泰文字幕" })).toBeNull();
    const zip = new URL(screen.getByRole("link", { name: "下載整包 zip（13 個檔案）" }).getAttribute("href") ?? "", "https://mokaair.com");
    expect(zip.searchParams.getAll("file").slice(-3)).toEqual([`${"1a".repeat(32)}:dub.en.m4a`, `${"2b".repeat(32)}:dub.ja.unchecked.wav`, `${hash(5)}:metadata.json`]);
  });

  it("has no dub step when the package has no dub track", async () => {
    stub();
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    expect(screen.queryByRole("region", { name: /配音音軌/ })).toBeNull();
  });

  it("says the compilation video is outside the zip", async () => {
    stub({ ...project, compilation: true, download_available: true, reviews: [{ ...review, files: review.files.filter((file) => file.role !== "final") }] });
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    expect(screen.getByRole("link", { name: "下載整包 zip（10 個檔案）" })).toBeTruthy();
    expect(screen.getByText(/1080p 影片不在審核區/)).toBeTruthy();
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

  it("reads a language added after the upload from the newest approved language batch, and never an older batch", async () => {
    const later = (seconds: number) => new Date(Date.parse(review.created_at) + seconds * 1000).toISOString();
    const batch = (id: string, created: string, metadataHash: string, locale: string): Review => ({
      ...review, id, gate: "languages", created_at: created, decided_at: created, payload: { locales: { [locale]: { metadata: "ready", captions: "ready" } } },
      files: [
        { role: `description_${locale}`, sha256: hash(6), size: 100, content_type: "text/plain" },
        { role: `captions_${locale}`, sha256: "a".repeat(64), size: 100, content_type: "text/plain" },
        { role: `thumbnail_${locale}`, sha256: "c".repeat(64), size: 500, content_type: "image/jpeg" },
        { role: "metadata", sha256: metadataHash, size: 900, content_type: "application/json" },
      ],
    });
    const translated = { ...metadata, localizations: { ...metadata.localizations, th: { title: "ชื่อไทย", description: "คำอธิบาย" } } };
    // Newest first, as the API orders them: the Thai batch, then the publish review, then a batch older than it.
    const value = { ...project, reviews: [batch("thai", later(60), "d".repeat(64), "th"), review, batch("older", later(-60), hash(7), "vi")] };
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url === "/api/travel/admin/videos/test-video") return Promise.resolve(Response.json(value));
      if (url === `/api/admin-video-files/test-video/${"d".repeat(64)}`) return Promise.resolve(Response.json(translated));
      throw new Error(`Unexpected request: ${url}`);
    }));
    render(<YoutubeManualUpload slug={project.slug} />);
    await open();
    fireEvent.change(screen.getByRole("combobox", { name: "語言" }), { target: { value: "th" } });
    expect(screen.getByLabelText("標題")).toHaveProperty("value", "ชื่อไทย");
    expect(screen.getByRole("link", { name: "縮圖 泰文" }).getAttribute("download")).toBe("thumbnail.th.jpg");
    expect(screen.getByRole("link", { name: "下載泰文字幕" }).getAttribute("href")).toBe(`/api/admin-video-files/test-video/${"a".repeat(64)}`);
    expect(screen.getByRole("link", { name: "下載日文字幕" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "縮圖 越南文" })).toBeNull();
    expect(screen.queryByRole("option", { name: "越南文" })).toBeNull();
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
