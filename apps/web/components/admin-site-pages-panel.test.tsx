import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import type { SitePageDetail, SitePageDocument } from "@/lib/site-pages";
import { AdminSitePagesPanel } from "./admin-site-pages-panel";

const mock = vi.hoisted(() => ({ api: vi.fn(), allowed: true }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/lib/navigation-guard", () => ({ useNavigationGuard: vi.fn() }));
vi.mock("@/components/admin-action-guard", () => ({ useAdminActionGuard: () => ({ allowed: mock.allowed }), AdminReadOnlyNotice: () => null }));
vi.mock("@/components/community/ui", () => ({
  Button: ({ secondary, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement> & { secondary?: boolean }) => { void secondary; return <button type="button" {...props} />; },
  Dialog: ({ children, title, onClose }: { children: React.ReactNode; title: string; onClose: () => void }) => <section role="dialog" aria-label={title}><button onClick={onClose}>關閉</button>{children}</section>,
}));
const document: SitePageDocument = {
  title: "Fixture title", description: "Fixture summary", effective_date: "2026-09-09", blocks: [{ type: "paragraph", text: "Fixture body" }],
  requirements: { operator: "Fixture operator", location: "Fixture location", contact: "Fixture contact", retention: "Fixture retention", legal: "Fixture legal" },
};
function detail(): SitePageDetail {
  return { slug: "privacy", locale: "zh-TW", version: 1, draft: structuredClone(document), published: null, pending_requirements: [], revisions: [{ id: "r1", version: 1, action: "initialized", created_at: "2026-09-09T00:00:00Z", created_by_user_id: "actor" }], audit: [] };
}
beforeEach(() => { mock.api.mockReset(); mock.allowed = true; mock.api.mockResolvedValue(detail()); });
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe("managed site information", () => {
  it("loads a draft, previews it safely, and saves with its expected version without publishing", async () => {
    render(<AdminSitePagesPanel />);
    const title = await screen.findByRole("textbox", { name: "文件標題" });
    fireEvent.change(title, { target: { value: "Updated title" } });
    fireEvent.click(screen.getByRole("button", { name: "預覽" }));
    expect(within(screen.getByRole("dialog")).getByRole("heading", { name: "Updated title" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "關閉" }));
    mock.api.mockResolvedValueOnce({ ...detail(), version: 2, draft: { ...document, title: "Updated title" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存草稿" }));
    expect(await screen.findByText("草稿已儲存，公開版本未變更。")).toBeTruthy();
    const write = mock.api.mock.calls.find(([url]) => url.includes("/draft"));
    expect(write?.[0]).toBe("/admin/site-pages/privacy/draft?locale=zh-TW");
    expect(JSON.parse(write?.[1].body)).toMatchObject({ expected_version: 1, document: { title: "Updated title" } });
    expect(mock.api.mock.calls.some(([url]) => url.includes("/publish"))).toBe(false);
  });
  it("requires an explicit confirmation and reason before publication", async () => {
    render(<AdminSitePagesPanel />); await screen.findByRole("textbox", { name: "文件標題" });
    fireEvent.click(screen.getByRole("button", { name: "發布" }));
    const dialog = screen.getByRole("dialog", { name: "確認發布" });
    const publish = within(dialog).getByRole("button", { name: "確認發布" });
    expect(publish).toHaveProperty("disabled", true);
    fireEvent.change(within(dialog).getByRole("textbox", { name: "異動原因" }), { target: { value: "Checked fixture" } });
    fireEvent.click(within(dialog).getByRole("checkbox"));
    fireEvent.click(publish);
    expect(await screen.findByText("已發布正式版本。")).toBeTruthy();
    expect(mock.api).toHaveBeenCalledWith("/admin/site-pages/privacy/publish?locale=zh-TW", expect.objectContaining({ method: "POST", body: JSON.stringify({ expected_version: 1, confirmed: true, reason: "Checked fixture" }) }));
  });
  it("keeps unsaved edits when another administrator wins a version conflict", async () => {
    render(<AdminSitePagesPanel />);
    const title = await screen.findByRole("textbox", { name: "文件標題" });
    fireEvent.change(title, { target: { value: "Keep my draft" } });
    mock.api.mockRejectedValueOnce(new ApiError("Conflict", 409, "site_page_version_conflict"));
    fireEvent.click(screen.getByRole("button", { name: "儲存草稿" }));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", expect.stringContaining("其他管理員"));
    expect(title).toHaveProperty("value", "Keep my draft");
  });
  it("protects page/language changes and supports five document languages", async () => {
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
    render(<AdminSitePagesPanel />);
    fireEvent.change(await screen.findByRole("textbox", { name: "文件標題" }), { target: { value: "Unsaved" } });
    const languages = screen.getByRole("combobox", { name: "文件語言" });
    expect(within(languages).getAllByRole("option")).toHaveLength(5);
    fireEvent.change(languages, { target: { value: "ja" } });
    expect(confirm).toHaveBeenCalled(); expect(languages).toHaveProperty("value", "zh-TW");
    expect(mock.api).toHaveBeenCalledTimes(1);
  });
  it("allows readers to preview but not change or publish", async () => {
    mock.allowed = false; render(<AdminSitePagesPanel />);
    const title = await screen.findByRole("textbox", { name: "文件標題" });
    expect(title.closest("fieldset")).toHaveProperty("disabled", true);
    expect(screen.getByRole("button", { name: "發布" })).toHaveProperty("disabled", true);
    expect(screen.getByRole("button", { name: "儲存草稿" })).toHaveProperty("disabled", true);
    expect(screen.getByRole("button", { name: "預覽" })).toHaveProperty("disabled", false);
  });
  it("never initializes on a GET and only initializes missing drafts after an explicit action", async () => {
    mock.api.mockRejectedValueOnce(new ApiError("Missing", 404, "site_page_not_found"));
    render(<AdminSitePagesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "建立缺少的五語系初稿" }));
    await waitFor(() => expect(mock.api).toHaveBeenCalledWith("/admin/site-pages/initialize", { method: "POST" }));
    expect(await screen.findByText("已建立初稿，未發布任何內容。")).toBeTruthy();
  });
  it("restores a history version only as a draft with a reason and expected version", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    render(<AdminSitePagesPanel />); await screen.findByRole("textbox", { name: "文件標題" });
    fireEvent.change(screen.getByRole("textbox", { name: "異動原因" }), { target: { value: "Restore fixture" } });
    fireEvent.click(screen.getByRole("button", { name: "還原為草稿" }));
    expect(await screen.findByText("已還原為新草稿，尚未發布。")).toBeTruthy();
    expect(mock.api).toHaveBeenCalledWith("/admin/site-pages/privacy/restore?locale=zh-TW", expect.objectContaining({ body: JSON.stringify({ expected_version: 1, revision_id: "r1", reason: "Restore fixture" }) }));
  });
});
