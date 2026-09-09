import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { CreatorInvitations } from "./creator-invitations";
import { PostEditor } from "./editor";
const mock = vi.hoisted(() => ({ api: vi.fn(), canPublish: false }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: { id: "reader" }, status: "authenticated", sessionIdentity: null }) }));
vi.mock("./provider", () => ({ useCommunity: () => ({ flags: { enabled: true, posting_enabled: true }, me: { can_publish: mock.canPublish, invitation_required: true } }) }));
beforeEach(() => {
  mock.api.mockReset(); mock.canPublish = false;
  mock.api.mockImplementation(async (path: string) => path === "/trips" ? [] : { items: [] });
  HTMLDialogElement.prototype.showModal = vi.fn(function (this: HTMLDialogElement) { this.setAttribute("open", ""); });
});
afterEach(cleanup);
describe("creator eligibility and reference-only video editing", () => {
  it("allows an uninvited creator to save a draft but never bypasses publishing eligibility", async () => {
    mock.api.mockImplementation(async (path: string) => path === "/trips" ? [] : { id: "post-1", version: 1, media: [] });
    render(<PostEditor />);
    const video = screen.getByLabelText("YouTube 連結（每行一個，最多 5 個）");
    fireEvent.change(video, { target: { value: "https://youtu.be/dQw4w9WgXcQ?si=not-stored" } });
    const publish = screen.getByRole("button", { name: "發佈" }) as HTMLButtonElement;
    expect(publish.disabled).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "儲存草稿" }));
    await waitFor(() => expect(mock.api.mock.calls.some(([path, init]) => path === "/community/posts" && init?.method === "POST")).toBe(true));
    const payload = JSON.parse(mock.api.mock.calls.find(([path]) => path === "/community/posts")![1].body);
    expect(payload.video_refs).toEqual([{ provider: "youtube", video_id: "dQw4w9WgXcQ" }]);
    expect(JSON.stringify(payload)).not.toContain("not-stored");
  });
  it("rejects unsafe or duplicate video references without sending them to the API", () => {
    render(<PostEditor />);
    fireEvent.change(screen.getByLabelText("YouTube 連結（每行一個，最多 5 個）"), { target: { value: "https://example.org/video" } });
    expect(screen.getByRole("alert").textContent).toContain("有效且不重複");
    expect((screen.getByRole("button", { name: "儲存草稿" }) as HTMLButtonElement).disabled).toBe(true);
    expect(mock.api.mock.calls.some(([path]) => path === "/community/posts")).toBe(false);
  });
  it("updates only the looked-up invitation with its captured version and review reason", async () => {
    const id = "10000000-0000-4000-8000-000000000001";
    mock.api.mockImplementation(async (_path: string, init?: RequestInit) => init?.method === "PUT" ? {} : { items: [{ user_id: id, invited: false, version: 4, updated_at: null }] });
    render(<CreatorInvitations />);
    fireEvent.change(screen.getByLabelText("使用者 ID"), { target: { value: id } }); fireEvent.click(screen.getByRole("button", { name: "查詢" }));
    fireEvent.click(await screen.findByLabelText("已邀請的創作者"));
    fireEvent.change(screen.getByLabelText("原因"), { target: { value: "Editorial pilot invitation" } });
    fireEvent.click(screen.getByRole("button", { name: "更新邀請" }));
    await waitFor(() => expect(mock.api.mock.calls.some(([path, init]) => path === `/admin/community/creator-invitations/${id}` && init?.method === "PUT")).toBe(true));
    const call = mock.api.mock.calls.find(([, init]) => init?.method === "PUT");
    expect(JSON.parse(call![1].body)).toEqual({ version: 4, invited: true, reason: "Editorial pilot invitation" });
  });
});
