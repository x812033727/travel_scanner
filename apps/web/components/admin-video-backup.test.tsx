import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { type BackupSettingsView, type BackupStatusView, drivePath, sizeText, VideoBackupCard } from "./admin-video-backup";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { fill, videoBackupCopy } from "@/lib/video-backup-copy";

const copy = videoBackupCopy("zh-TW");
const settingsEndpoint = "/api/travel/admin/video-backup/settings";
const saved: BackupSettingsView = {
  enabled: true, path: "AI/備份", lock_path: "AI/備份", lock_reported_at: "2026-10-19T10:00:00Z", problem: null,
  tiers: {}, folder_names: {}, default_folder_names: { curio: "奇聞檔案局", story: "品牌故事", other: "其他" },
  full_categories: ["anime", "drama", "long-drama"], updated_at: "2026-10-19T10:00:00Z",
  test: { pending_id: null, requested_at: null, status: null, message: null, tested_at: null },
  space: { free_bytes: null, total_bytes: null, at: null },
};
const counts = { done: 0, stale: 0, pending: 0, failed: 0, blocked_quota: 0, partial: 0, not_queued: 0, off: 0 };
const video = (slug: string, extra: Partial<BackupStatusView["videos"][number]> = {}) => ({
  slug, title: slug, youtube_video_id: "dQw4w9WgXcQ", series_key: "curio", folder: `奇聞檔案局/${slug}`, tier: "basic" as const,
  state: "pending" as const, complete: false, bytes: null, at: null, error: null, missing: [], overdue: false, ...extra,
});
const behind: BackupStatusView = {
  enabled: true, path: "AI/備份", uploaded: 3, counts: { ...counts, done: 1, partial: 1, pending: 1 }, all_backed_up: false, overdue_hours: 24,
  videos: [video("curio-h01", { state: "partial", missing: ["dubs/en"] }), video("curio-h02", { overdue: true })],
};
const complete: BackupStatusView = { ...behind, counts: { ...counts, done: 3 }, all_backed_up: true, videos: [] };

function bootstrap(manage: boolean): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: ["content.read", ...(manage ? ["settings.manage"] : [])], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}
/** The site's backup routes: GETs answer `settings` and `status`; PUT and POST answer `answer` or the settings. */
function site({ settings = saved, status = behind, answer }: { settings?: BackupSettingsView; status?: BackupStatusView; answer?: (url: string, init: RequestInit) => Response } = {}) {
  const fetchMock = vi.fn((input: RequestInfo | URL, init: RequestInit = {}) => {
    const url = String(input);
    if (init.method && init.method !== "GET") return Promise.resolve(answer ? answer(url, init) : Response.json(settings));
    return Promise.resolve(Response.json(url.includes("/status") ? status : settings));
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}
async function mount(manage = true) {
  render(<AdminOperationsProvider bootstrap={bootstrap(manage)}><VideoBackupCard /></AdminOperationsProvider>);
  const card = await screen.findByRole("region", { name: copy.title });
  await within(card).findByLabelText(copy.path);
  await waitFor(() => expect(within(card).getByRole("button", { name: copy.refresh })).toHaveProperty("disabled", false));
  return within(card);
}
const sent = (fetchMock: ReturnType<typeof site>, method: string) => fetchMock.mock.calls.filter(([, init]) => init?.method === method);
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("video backup card", () => {
  it("keeps the five catalogs aligned", () => {
    const keys = Object.keys(videoBackupCopy("en")).sort();
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) expect(Object.keys(videoBackupCopy(locale)).sort()).toEqual(keys);
    for (const locale of ["en", "zh-TW", "zh-CN", "ja", "ko"]) {
      const names = (text: string) => [...text.matchAll(/\{(\w+)\}/g)].map((match) => match[1]).sort();
      const catalog = videoBackupCopy(locale) as Record<string, string>;
      for (const [key, text] of Object.entries(videoBackupCopy("en"))) expect(names(catalog[key]), `${locale}.${key}`).toEqual(names(text));
    }
  });

  it("reads a pasted folder the way the site saves it", () => {
    expect(drivePath("G:\\我的雲端硬碟\\AI\\備份\\")).toBe("AI/備份");
    expect(drivePath("G:\\My Drive\\AI\\備份")).toBe("AI/備份");
    expect(drivePath("/AI/備份/")).toBe("AI/備份");
    for (const bad of ["", "G:\\", "AI/../系統", "AI/備份?", "AI/備份."]) expect(drivePath(bad), bad).toBeNull();
    expect(sizeText(1536)).toBe("1.5 KB");
    expect(sizeText(535_000_000)).toBe("510 MB");
  });

  it("says how many uploaded videos are not backed up yet, and lists them with what is missing", async () => {
    site();
    const card = await mount();
    expect(card.getByText(fill(copy.notAllDone, { count: 3, left: 2 }))).toBeTruthy();
    const rows = card.getAllByRole("row");
    expect(rows.some((row) => row.textContent?.includes("curio-h01") && row.textContent.includes(copy.statePartial) && row.textContent.includes("dubs/en"))).toBe(true);
    expect(rows.some((row) => row.textContent?.includes("curio-h02") && row.textContent.includes(fill(copy.overdue, { hours: 24 })))).toBe(true);
    expect(card.getByText("AI/備份/奇聞檔案局/curio-h01")).toBeTruthy();
  });

  it("says so plainly when every uploaded video is in Drive, and lists them all on request", async () => {
    const fetchMock = site({ status: complete });
    const card = await mount();
    expect(card.getByText(fill(copy.allDone, { count: 3, path: "AI/備份" }))).toBeTruthy();
    fireEvent.click(card.getByRole("button", { name: copy.showAll }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("/admin/video-backup/status?all=true"))).toBe(true));
  });

  it("shows a reviewer the status but no way to change or test it", async () => {
    const fetchMock = site();
    const card = await mount(false);
    expect(card.getByRole("note").textContent).toBe(copy.readOnly);
    expect(card.getByLabelText(copy.path)).toHaveProperty("disabled", true);
    expect(card.getByRole("button", { name: copy.save })).toHaveProperty("disabled", true);
    expect(card.getByRole("button", { name: copy.test })).toHaveProperty("disabled", true);
    fireEvent.submit(card.getByRole("form"));
    expect(sent(fetchMock, "PUT")).toHaveLength(0);
  });

  it("previews the pasted PC folder and sends only what changed, with the saved stamp", async () => {
    const fetchMock = site({ answer: () => Response.json({ ...saved, tiers: { curio: "full" }, folder_names: { curio: "奇聞" }, updated_at: "2026-10-19T11:00:00Z" }) });
    const card = await mount();
    fireEvent.change(card.getByLabelText(copy.path), { target: { value: "G:\\My Drive\\AI\\備份\\" } });
    expect(card.getByText(fill(copy.pathPreview, { path: "AI/備份" }))).toBeTruthy();
    fireEvent.change(card.getByLabelText(`${copy.tiersTitle} curio`), { target: { value: "full" } });
    fireEvent.change(card.getByLabelText(`${copy.folderName} curio`), { target: { value: " 奇聞 " } });
    expect(card.getByRole("button", { name: copy.test })).toHaveProperty("disabled", true);
    fireEvent.click(card.getByRole("button", { name: copy.save }));
    await card.findByText(copy.saved);
    const [[url, init]] = sent(fetchMock, "PUT");
    expect(url).toBe(settingsEndpoint);
    expect(JSON.parse(String(init?.body))).toEqual({
      path: "G:\\My Drive\\AI\\備份\\", tiers: { curio: "full" }, folder_names: { curio: "奇聞" }, expected_updated_at: saved.updated_at,
    });
  });

  it("will not save a folder that cannot be one, and adds a series by a valid key only", async () => {
    site();
    const card = await mount();
    fireEvent.change(card.getByLabelText(copy.path), { target: { value: "AI/../系統" } });
    expect(card.getByText(copy.pathInvalid)).toBeTruthy();
    expect(card.getByRole("button", { name: copy.save })).toHaveProperty("disabled", true);
    fireEvent.change(card.getByLabelText(copy.newSeries), { target: { value: "ou de" } });
    expect(card.getByText(copy.newSeriesInvalid)).toBeTruthy();
    expect(card.getByRole("button", { name: copy.addSeries })).toHaveProperty("disabled", true);
    fireEvent.change(card.getByLabelText(copy.newSeries), { target: { value: "ou-de-jianghu" } });
    fireEvent.click(card.getByRole("button", { name: copy.addSeries }));
    expect(card.getByLabelText(`${copy.folderName} ou-de-jianghu`)).toBeTruthy();
  });

  it("keeps the edits on a conflict and shows the site's refusal as it is", async () => {
    site({ answer: () => Response.json({ detail: "x", code: "video_backup_settings_conflict" }, { status: 409 }) });
    const card = await mount();
    fireEvent.click(card.getByLabelText(copy.enabled));
    fireEvent.click(card.getByRole("button", { name: copy.save }));
    expect(await card.findByText(copy.conflict)).toBeTruthy();
    expect(card.getByLabelText(copy.enabled)).toHaveProperty("checked", false);
    cleanup();
    const outside = "主機的 rclone 只能寫入 AI/備份 和它底下的資料夾";
    site({ answer: () => Response.json({ detail: outside, code: "video_backup_path_outside_lock" }, { status: 422 }) });
    const again = await mount();
    fireEvent.change(again.getByLabelText(copy.path), { target: { value: "AI/別的" } });
    fireEvent.click(again.getByRole("button", { name: copy.save }));
    expect((await again.findByRole("alert")).textContent).toContain(outside);
  });

  it("asks the worker for a test and shows it waiting, then the answer and the free space", async () => {
    const pending = { ...saved, test: { ...saved.test, pending_id: "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b", requested_at: "2026-10-19T12:00:00Z" } };
    const fetchMock = site({ answer: () => Response.json(pending) });
    const card = await mount();
    fireEvent.click(card.getByRole("button", { name: copy.test }));
    await waitFor(() => expect(sent(fetchMock, "POST")).toHaveLength(1));
    expect(String(sent(fetchMock, "POST")[0][0])).toBe("/api/travel/admin/video-backup/test");
    expect(await card.findByText((text) => text.startsWith(copy.testPending.split("{time}")[0]))).toBeTruthy();
    cleanup();
    site({ settings: { ...saved, test: { pending_id: null, requested_at: null, status: "success", message: "ok", tested_at: "2026-10-19T12:05:00Z" }, space: { free_bytes: 10 * 1024 ** 3, total_bytes: 15 * 1024 ** 3, at: null } } });
    const answered = await mount();
    expect(answered.getByText(fill(copy.space, { free: "10 GB", total: "15 GB" }))).toBeTruthy();
    expect(answered.getByText((text) => text.startsWith(copy.testSuccess))).toBeTruthy();
  });
});
