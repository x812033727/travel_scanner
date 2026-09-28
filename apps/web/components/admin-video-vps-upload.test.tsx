import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { YoutubeVpsUpload } from "./admin-video-vps-upload";

const path = "/api/travel/admin/videos/test-video/youtube/vps";
const id = "abcdefghijk";
const job = {
  id: "a".repeat(64), state: "staging", code: null, video_id: null, upload_started: false,
  steps: [{ id: "video", done: false }, { id: "captions_zh-TW", done: false }, { id: "verify", done: false }],
  files: [{ role: "final", size: 2048, received: 0 }],
};
const view = (overrides = {}) => ({ configured: true, linked: false, job: { ...job, ...overrides } });
async function open() {
  fireEvent.click(screen.getByRole("button", { name: "VPS 獨立上傳" }));
  await screen.findByRole("region", { name: "VPS · YouTube Studio" });
}
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("VPS Studio mode", () => {
  it("is opt-in, preserves the original form and explains an unconfigured service", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(Response.json({ configured: false, linked: false, job: null }))));
    render(<YoutubeVpsUpload slug="test-video"><p>原來的上傳表單</p></YoutubeVpsUpload>);
    expect(fetch).not.toHaveBeenCalled();
    expect(screen.getByText("原來的上傳表單")).toBeTruthy();
    await open();
    await screen.findByText(/VPS 服務尚未設定/);
    expect(screen.queryByText("原來的上傳表單")).toBeNull();
    expect(screen.queryByRole("button", { name: "送到 VPS（私人）" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "返回其他上傳模式" }));
    expect(screen.getByText("原來的上傳表單")).toBeTruthy();
    expect(vi.mocked(fetch).mock.calls.every(([, init]) => !init?.method)).toBe(true);
  });

  it("sends draft text and the existing video, transfers chunks and stops after queue acknowledgement", async () => {
    let current: ReturnType<typeof view> | { configured: boolean; linked: boolean; job: null } = { configured: true, linked: false, job: null };
    let stages = 0;
    const mock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (String(input) === path && init?.method === "POST") current = view();
      if (String(input) === path + "/stage") {
        stages++;
        current = view(stages === 1 ? { files: [{ role: "final", size: 2048, received: 2048 }] } : { state: "queued" });
      }
      return Promise.resolve(Response.json(current));
    });
    vi.stubGlobal("fetch", mock);
    render(<YoutubeVpsUpload slug="test-video" draft={{ title: "編輯後的標題", description: "說明\n00:00 開場", video_id: id }} />);
    await open();
    fireEvent.click(await screen.findByRole("button", { name: "送到 VPS（私人）" }));
    await screen.findByText("VPS 已排入佇列");
    expect(stages).toBe(2);
    const start = mock.mock.calls.find(([input, init]) => String(input) === path && init?.method === "POST");
    expect(JSON.parse(String(start?.[1]?.body))).toEqual({ title: "編輯後的標題", description: "說明\n00:00 開場", url: id });
    expect(screen.getByText(/現在可關閉這個頁面/)).toBeTruthy();
  });

  it("resumes a partially transferred package and does not create a new job", async () => {
    let current = view({ files: [{ role: "final", size: 2048, received: 1024 }] });
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") {
        expect(String(input)).toBe(path + "/stage");
        current = view({ state: "queued" });
      }
      return Promise.resolve(Response.json(current));
    }));
    render(<YoutubeVpsUpload slug="test-video" />);
    await open();
    fireEvent.click(await screen.findByRole("button", { name: "繼續傳送到 VPS" }));
    await screen.findByText("VPS 已排入佇列");
    expect(vi.mocked(fetch).mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(1);
  });

  it("requires an existing URL after an uncertain upload and preserves owner control of login", async () => {
    let current = view({ state: "needs_action", code: "video_id_required", upload_started: true });
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") {
        expect(String(input)).toBe(path + "/resume");
        expect(JSON.parse(String(init.body))).toEqual({ url: "https://youtu.be/" + id });
        current = view({ state: "queued", video_id: id });
      }
      return Promise.resolve(Response.json(current));
    }));
    render(<YoutubeVpsUpload slug="test-video" />);
    await open();
    const resume = await screen.findByRole("button", { name: "已處理，繼續工作" });
    expect(resume).toHaveProperty("disabled", true);
    expect(screen.queryByRole("button", { name: "取消等待中的工作" })).toBeNull();
    expect(screen.getByText(/登入與驗證由你操作/)).toBeTruthy();
    fireEvent.change(screen.getByLabelText("核對後的 YouTube 影片網址"), { target: { value: "https://youtu.be/" + id } });
    fireEvent.click(resume);
    await screen.findByText("VPS 已排入佇列");
  });

  it("records a completed private result before refreshing the parent", async () => {
    const changed = vi.fn();
    const mock = vi.fn((input: RequestInfo | URL) => Promise.resolve(Response.json(
      String(input).endsWith("/record") ? { ...view({ state: "done", video_id: id }), linked: true } : view({ state: "done", video_id: id })
    )));
    vi.stubGlobal("fetch", mock);
    render(<YoutubeVpsUpload slug="test-video" onChange={changed} />);
    await open();
    await screen.findByText(/私人影片連結已記錄到網站/);
    expect(changed).toHaveBeenCalled();
    expect(mock.mock.calls.some(([input]) => String(input) === path + "/record")).toBe(true);
    expect(screen.getByRole("link", { name: "在 Studio 查看影片" }).getAttribute("href")).toBe("https://studio.youtube.com/video/" + id + "/edit");
  });

  it("shows failed submission without claiming a queued upload", async () => {
    vi.stubGlobal("fetch", vi.fn((_input: RequestInfo | URL, init?: RequestInit) => Promise.resolve(
      init?.method === "POST" ? Response.json({ detail: "VPS 暫時無法連線", code: "vps_unavailable" }, { status: 503 }) : Response.json({ configured: true, linked: false, job: null })
    )));
    render(<YoutubeVpsUpload slug="test-video" />);
    await open();
    fireEvent.click(await screen.findByRole("button", { name: "送到 VPS（私人）" }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("VPS 暫時無法連線"));
    expect(screen.queryByText("VPS 已排入佇列")).toBeNull();
    expect(screen.getByRole("button", { name: "送到 VPS（私人）" })).toHaveProperty("disabled", false);
  });

  it("lets an owner choose a project without a site OAuth connection", async () => {
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => Promise.resolve(Response.json(
      String(input).endsWith("/admin/videos") ? [{ slug: "test-video", title: "我的影片" }, { slug: "dropped", title: "已放棄", dropped_at: "2026-09-28" }] : { configured: true, linked: false, job: null }
    ))));
    render(<YoutubeVpsUpload />);
    fireEvent.click(screen.getByRole("button", { name: "VPS 獨立上傳" }));
    await screen.findByRole("option", { name: "我的影片" });
    expect(screen.queryByRole("option", { name: "已放棄" })).toBeNull();
    fireEvent.change(screen.getByRole("combobox"), { target: { value: "test-video" } });
    await screen.findByRole("button", { name: "送到 VPS（私人）" });
  });
});
