import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoReviews } from "./admin-video-reviews";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const SLUG = "story-adapt-dolby-licensing";
const live = { slug: "ai-model-choice", title: "AI 模型怎麼挑", stage: "final", youtube_video_id: null, last_synced_at: "2026-09-25T05:00:00Z", pending: 0, checklist: [], reviews: [] };
const dropped = { ...live, slug: SLUG, title: "杜比怎麼收授權", dropped_at: "2026-10-20T05:00:00Z", dropped_note: "舊規則，重做", reviews: [] };

type Call = { method: string; url: string; body?: unknown };

/** The site for one video's page: answers the delete as `deleting` says, and records every write. */
function site(video: { slug: string } & Record<string, unknown>, deleting: Array<{ status: number; body: Record<string, unknown> }> = [{ status: 200, body: { slug: video.slug } }]) {
  const writes: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    if (method !== "GET") writes.push({ method, url, body: init?.body ? JSON.parse(String(init.body)) : undefined });
    if (method === "DELETE") {
      const { status, body } = deleting.shift() ?? { status: 200, body: {} };
      return Promise.resolve(Response.json(body, { status }));
    }
    if (url.includes("/admin/step-up")) return Promise.resolve(Response.json({ scopes: ["videos.delete"], expires_at: "2026-10-31T00:05:00Z" }));
    if (url.includes(`/admin/videos/${video.slug}`)) return Promise.resolve(Response.json(video));
    if (url.includes("/admin/videos/browse")) return Promise.resolve(Response.json({ items: [video], total: 1, page: 1, pages: 1, facets: { category: [], state: [] } }));
    if (url.includes("/admin/videos")) return Promise.resolve(Response.json([video]));
    return Promise.resolve(Response.json({}));
  }));
  return writes;
}

function open(capabilities = ["content.read", "content.manage"], slug = SLUG) {
  window.history.replaceState(null, "", `/?video=${slug}`);
  render(<AdminOperationsProvider bootstrap={bootstrap(capabilities)}><AdminVideoReviews /></AdminOperationsProvider>);
}

describe("deleting a dropped video", () => {
  afterEach(() => { cleanup(); vi.unstubAllGlobals(); window.history.replaceState(null, "", "/"); });

  it("offers no delete on a video that is not dropped", async () => {
    site(live);
    open(undefined, live.slug);
    expect(await screen.findByText("放棄這支影片", { selector: "summary" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "永久刪除" })).toBeNull();
  });

  it("offers no delete to someone who can only read", async () => {
    site(dropped);
    open(["content.read"]);
    expect(await screen.findByText("舊規則，重做")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "永久刪除" })).toBeNull();
  });

  it("deletes only once the slug is typed out, and goes back to the list", async () => {
    const writes = site(dropped);
    open();
    fireEvent.click(await screen.findByRole("button", { name: "永久刪除" }));
    const dialog = screen.getByRole("dialog", { name: "永久刪除這支影片？" });
    const confirm = within(dialog).getByRole("button", { name: "永久刪除" });
    expect(confirm).toHaveProperty("disabled", true);
    expect(within(dialog).queryByRole("note"), "no YouTube warning without a YouTube id").toBeNull();
    fireEvent.change(within(dialog).getByRole("textbox"), { target: { value: "story-adapt" } });
    expect(confirm).toHaveProperty("disabled", true);
    fireEvent.change(within(dialog).getByRole("textbox"), { target: { value: SLUG } });
    expect(confirm).toHaveProperty("disabled", false);
    fireEvent.click(confirm);
    await waitFor(() => expect(writes).toHaveLength(1));
    expect(writes[0].method).toBe("DELETE");
    expect(writes[0].url).toContain(`/admin/videos/${SLUG}`);
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    expect(new URLSearchParams(window.location.search).get("video")).toBeNull();
  });

  it("says plainly that YouTube keeps its copy", async () => {
    site({ ...dropped, youtube_video_id: "uv-CQOKDMOI" });
    open();
    fireEvent.click(await screen.findByRole("button", { name: "永久刪除" }));
    const warning = within(screen.getByRole("dialog")).getByRole("note");
    expect(warning.textContent).toContain("uv-CQOKDMOI");
    expect(warning.textContent).toContain("YouTube 上的影片不會被刪");
  });

  it("asks for the password only when the site wants it, then deletes", async () => {
    const writes = site(dropped, [
      { status: 401, body: { code: "admin_step_up_required", detail: "請重新輸入密碼後再執行此操作" } },
      { status: 200, body: { slug: SLUG } },
    ]);
    open();
    fireEvent.click(await screen.findByRole("button", { name: "永久刪除" }));
    const dialog = screen.getByRole("dialog");
    expect(within(dialog).queryByLabelText("目前密碼")).toBeNull();
    fireEvent.change(within(dialog).getByRole("textbox"), { target: { value: SLUG } });
    const confirm = within(dialog).getByRole("button", { name: "永久刪除" });
    fireEvent.click(confirm);
    const password = await within(dialog).findByLabelText(/目前密碼/);
    expect(writes.map((write) => write.method)).toEqual(["DELETE"]);
    expect(confirm).toHaveProperty("disabled", true);
    fireEvent.change(password, { target: { value: "correct-password" } });
    fireEvent.click(confirm);
    await waitFor(() => expect(writes).toHaveLength(3));
    expect(writes[1].url).toContain("/admin/step-up");
    expect(writes[1].body).toEqual({ password: "correct-password", scopes: ["videos.delete"] });
    expect(writes[2].method).toBe("DELETE");
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
  });

  it("keeps the dialog open and says why when the site refuses", async () => {
    site(dropped, [{ status: 409, body: { code: "video_project_not_dropped", detail: "只有已放棄的影片能刪除" } }]);
    open();
    fireEvent.click(await screen.findByRole("button", { name: "永久刪除" }));
    const dialog = screen.getByRole("dialog");
    fireEvent.change(within(dialog).getByRole("textbox"), { target: { value: SLUG } });
    fireEvent.click(within(dialog).getByRole("button", { name: "永久刪除" }));
    expect((await within(dialog).findByRole("alert")).textContent).toContain("刪除失敗");
    expect(screen.getByRole("dialog")).toBeTruthy();
  });

  it("offers the delete on a dropped row of the catalog", async () => {
    const writes = site(dropped);
    window.history.replaceState(null, "", "/");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: "永久刪除" }));
    const dialog = screen.getByRole("dialog");
    fireEvent.change(within(dialog).getByRole("textbox"), { target: { value: SLUG } });
    fireEvent.click(within(dialog).getByRole("button", { name: "永久刪除" }));
    await waitFor(() => expect(writes.map((write) => write.method)).toEqual(["DELETE"]));
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
  });
});
