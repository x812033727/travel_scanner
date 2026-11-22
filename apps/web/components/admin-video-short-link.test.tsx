import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import type { Project, Review, YoutubeSync } from "./admin-video-review-card";
import { AdminVideoReviews } from "./admin-video-reviews";
import { canRecordShortUpload, handPushedShort } from "./admin-video-short-link";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

const SLUG = "shechu-hell-e01";
const ID = "ShortVid001";
const FORM = "記錄手動上架的影片";
const NOTE = "影片在 YouTube 還是私人或未公開、也沒有排程，沒有公開時間；公開後再貼一次網址";
const hash = (n: number) => String(n).repeat(64);
const final: Review = {
  id: "short-final", gate: "final", status: "approved", content_sha256: hash(2), summary: "Shorts 10.4 秒",
  payload: { line: "drama", hand_pushed: true },
  files: [{ role: "preview", sha256: hash(2), size: 9000, content_type: "video/mp4" }],
  choice: null, note: null, created_at: "2026-11-21T00:00:00Z", decided_at: "2026-11-22T00:00:00Z",
};
const byWorker: Review = { ...final, payload: { line: "drama" } };
const publish: Review = {
  id: "short-package", gate: "publish", status: "approved", content_sha256: hash(5), summary: "Shorts 上傳包",
  payload: { final_review_id: final.id, zh: { title: "準時下班" }, locales: [] },
  files: [{ role: "final", sha256: hash(2), size: 9000, content_type: "video/mp4" }],
  choice: null, note: null, created_at: "2026-11-22T00:10:00Z", decided_at: "2026-11-22T00:20:00Z",
};
const short: Project = {
  slug: SLUG, title: "準時下班", stage: "final", format: "drama", shorts_line: "drama", shorts_series: "shechu-hell",
  checklist: [], youtube_video_id: null, youtube_publish_at: null, publish_approved_at: null, ready_to_upload: false,
  pending: 0, last_synced_at: "2026-11-22T00:00:00Z", reviews: [final],
};
const packaged: Project = { ...short, publish_approved_at: "2026-11-22T00:20:00Z", ready_to_upload: true, reviews: [publish, final] };

describe("who records a hand upload", () => {
  it("is a Short whose cut is approved, with no publish time and outside the site's route", () => {
    expect(canRecordShortUpload(short), "no package").toBe(true);
    expect(canRecordShortUpload({ ...short, reviews: [byWorker] }), "the worker's, before its package is approved").toBe(true);
    expect(canRecordShortUpload(packaged), "pushed by hand, package or not").toBe(true);
    expect(canRecordShortUpload({ ...short, youtube_video_id: ID }), "linked without a time").toBe(true);
    expect(canRecordShortUpload({ ...packaged, reviews: [publish, byWorker] }), "the worker's with a package").toBe(false);
    expect(canRecordShortUpload({ ...short, reviews: [{ ...final, status: "pending" }] }), "cut not approved").toBe(false);
    expect(canRecordShortUpload({ ...short, youtube_video_id: ID, youtube_publish_at: "2026-11-23T11:30:00Z" })).toBe(false);
    expect(canRecordShortUpload({ ...short, dropped_at: "2026-11-22T01:00:00Z" })).toBe(false);
    expect(canRecordShortUpload({ ...short, youtube_sync: { status: "running", interrupted: false } as YoutubeSync })).toBe(false);
    expect(canRecordShortUpload({ ...short, shorts_line: null })).toBe(false);
  });

  it("counts only a live review's true as pushed by hand", () => {
    expect(handPushedShort(short)).toBe(true);
    expect(handPushedShort({ ...short, reviews: [byWorker, { ...publish, status: "pending", payload: { hand_pushed: true } }] })).toBe(true);
    expect(handPushedShort({ ...short, reviews: [{ ...final, status: "superseded" }] })).toBe(false);
    expect(handPushedShort({ ...short, reviews: [{ ...final, payload: { hand_pushed: "true" } }] })).toBe(false);
    expect(handPushedShort({ ...short, shorts_line: null })).toBe(false);
  });
});

/** The site for one Short's page, with a linked channel; a POST answers and the page reads `after`. */
function site(video: Project, after: Project = video) {
  const posts: { url: string; body: unknown }[] = [];
  let current = video;
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (init?.method === "POST") {
      posts.push({ url, body: JSON.parse(String(init.body)) });
      current = after;
      return Promise.resolve(Response.json({ ...after, youtube_publish_note: after.youtube_publish_at ? null : NOTE }));
    }
    if (url.endsWith("/admin/video-youtube")) return Promise.resolve(Response.json({ linked: true, channel_title: "Mokaair", audited: false }));
    if (url.includes(`/admin/videos/${SLUG}`)) return Promise.resolve(Response.json(current));
    if (url.includes("/admin/videos/browse")) return Promise.resolve(Response.json({ items: [], total: 0, page: 1, pages: 1, facets: { category: [], state: [] } }));
    if (url.includes("/admin/videos")) return Promise.resolve(Response.json([]));
    return Promise.resolve(Response.json({}));
  }));
  return posts;
}

function open(capabilities = ["content.read", "content.manage"]) {
  window.history.replaceState(null, "", `/?video=${SLUG}`);
  const bootstrap: AdminBootstrap = { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
  render(<AdminOperationsProvider bootstrap={bootstrap}><AdminVideoReviews /></AdminOperationsProvider>);
}

describe("a Short's page", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    window.history.replaceState(null, "", "/");
  });

  it("records the Studio link with no package, says why there is no time, then takes the time", async () => {
    const linked = { ...short, youtube_video_id: ID };
    const posts = site(short, linked);
    open();
    const form = within(await screen.findByRole("form", { name: FORM }));
    fireEvent.change(form.getByLabelText("YouTube 網址或影片 id"), { target: { value: `https://youtube.com/shorts/${ID}` } });
    fireEvent.click(form.getByRole("button", { name: "記錄連結" }));

    expect(await form.findByText(NOTE)).toBeTruthy();
    expect(posts[0]).toEqual({ url: `/api/travel/admin/videos/${SLUG}/youtube`, body: { url: `https://youtube.com/shorts/${ID}`, publish_at: null } });
    await waitFor(() => expect(form.getByText(/還沒有公開時間。在 Studio/)).toBeTruthy());

    fireEvent.change(form.getByLabelText("上架時間（選填）"), { target: { value: "2026-11-23T19:30" } });
    fireEvent.click(form.getByRole("button", { name: "記錄連結" }));
    await waitFor(() => expect(posts).toHaveLength(2));
    expect(posts[1].body).toEqual({ url: `https://youtube.com/shorts/${ID}`, publish_at: new Date("2026-11-23T19:30").toISOString() });
  });

  it("starts from the recorded video when only the time is missing", async () => {
    site({ ...short, youtube_video_id: ID });
    open();
    const form = within(await screen.findByRole("form", { name: FORM }));
    expect(form.getByLabelText("YouTube 網址或影片 id")).toHaveProperty("value", ID);
  });

  it("offers the link instead of a send to YouTube for a Short pushed by hand", async () => {
    site(packaged);
    open();
    expect(await screen.findByRole("form", { name: FORM })).toBeTruthy();
    expect(screen.getAllByRole("form")).toHaveLength(1);
  });

  it("keeps the send to YouTube for the worker's Short with an approved package", async () => {
    site({ ...packaged, reviews: [publish, byWorker] });
    open();
    await waitFor(() => expect(screen.getAllByRole("form").length).toBeGreaterThan(0));
    expect(screen.queryByRole("form", { name: FORM })).toBeNull();
  });

  it("shows the form only to someone who manages content", async () => {
    site(short);
    open(["content.read"]);
    await screen.findByRole("heading", { name: "準時下班" });
    expect(screen.queryByRole("form", { name: FORM })).toBeNull();
  });
});
