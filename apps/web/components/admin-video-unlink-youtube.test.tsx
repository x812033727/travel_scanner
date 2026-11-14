import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoReviews } from "./admin-video-reviews";
import { canUnlinkYoutube } from "./admin-video-unlink-youtube";
import type { ProjectSummary } from "./admin-video-review-card";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const SLUG = "curio-remade";
const OLD = "dQw4w9WgXcQ";
const linked = { slug: SLUG, title: "重做的一集", stage: "done", youtube_video_id: OLD, youtube_publish_at: null, last_synced_at: "2026-11-14T05:00:00Z", pending: 0, checklist: [], reviews: [] };
const unlinked = { ...linked, youtube_video_id: null };

type Call = { method: string; url: string };

/** The site for one video's page; the DELETE answers `answer` and the page then reads `after`. */
function site(video: Record<string, unknown>, answer: { status: number; body: Record<string, unknown> } = { status: 200, body: unlinked }, after: Record<string, unknown> = unlinked) {
  const writes: Call[] = [];
  let current = video;
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    if (method !== "GET") writes.push({ method, url });
    if (method === "DELETE") {
      if (answer.status < 400) current = after;
      return Promise.resolve(Response.json(answer.body, { status: answer.status }));
    }
    if (url.includes(`/admin/videos/${SLUG}`)) return Promise.resolve(Response.json(current));
    if (url.includes("/admin/videos/browse")) return Promise.resolve(Response.json({ items: [current], total: 1, page: 1, pages: 1, facets: { category: [], state: [] } }));
    if (url.includes("/admin/videos")) return Promise.resolve(Response.json([current]));
    return Promise.resolve(Response.json({}));
  }));
  return writes;
}

function open(capabilities = ["content.read", "content.manage"]) {
  window.history.replaceState(null, "", `/?video=${SLUG}`);
  render(<AdminOperationsProvider bootstrap={bootstrap(capabilities)}><AdminVideoReviews /></AdminOperationsProvider>);
}

describe("unlinking a YouTube upload", () => {
  afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); window.history.replaceState(null, "", "/"); });

  it("is offered only while the video is linked with no publish time and no send running", () => {
    const base = linked as unknown as ProjectSummary;
    expect(canUnlinkYoutube(base)).toBe(true);
    expect(canUnlinkYoutube({ ...base, youtube_publish_at: "2099-01-01T00:00:00Z" })).toBe(false);
    expect(canUnlinkYoutube({ ...base, youtube_publish_at: "2026-01-01T00:00:00Z" })).toBe(false);
    expect(canUnlinkYoutube({ ...base, youtube_video_id: null })).toBe(false);
    expect(canUnlinkYoutube({ ...base, dropped_at: "2026-11-01T00:00:00Z" })).toBe(false);
    expect(canUnlinkYoutube({ ...base, youtube_sync: { status: "running", lease_until: "2099-01-01T00:00:00Z" } } as unknown as ProjectSummary)).toBe(false);
  });

  it("asks first, unlinks, and reads the video again", async () => {
    const writes = site(linked);
    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    open();
    fireEvent.click(await screen.findByRole("button", { name: "解除連結" }));
    expect(confirm).toHaveBeenCalledWith(expect.stringContaining(OLD));
    await waitFor(() => expect(writes).toEqual([{ method: "DELETE", url: `/api/travel/admin/videos/${SLUG}/youtube` }]));
    await waitFor(() => expect(screen.queryByRole("button", { name: "解除連結" })).toBeNull());
  });

  it("sends nothing when the owner cancels", async () => {
    const writes = site(linked);
    vi.spyOn(window, "confirm").mockReturnValue(false);
    open();
    fireEvent.click(await screen.findByRole("button", { name: "解除連結" }));
    expect(writes).toEqual([]);
  });

  it("shows why the site refused", async () => {
    site(linked, { status: 409, body: { code: "video_youtube_unlink_scheduled", detail: "這支影片已記錄公開時間" } }, linked);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    open();
    fireEvent.click(await screen.findByRole("button", { name: "解除連結" }));
    expect((await screen.findByRole("alert")).textContent).toContain("沒有解除：這支影片已記錄公開時間");
  });

  it("is not offered to a reader or on a scheduled video", async () => {
    site(linked);
    open(["content.read"]);
    expect(await screen.findByText("重做的一集", { selector: "h2" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "解除連結" })).toBeNull();
    cleanup();
    site({ ...linked, youtube_publish_at: "2099-01-01T00:00:00Z" });
    open();
    expect(await screen.findByText("重做的一集", { selector: "h2" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "解除連結" })).toBeNull();
  });
});
