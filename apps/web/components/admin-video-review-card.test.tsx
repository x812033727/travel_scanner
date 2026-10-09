import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { chosenLanguagesComplete, publishState, PublishPill, ReviewCard, UploadPackage, type ProjectSummary, type Review } from "./admin-video-review-card";

// Ticket 2026-09-28-admin-video-review-the-owner-s: three final-cut approvals did not register on
// 2026-09-28 until the owner was sent the exact titles. These pin down what the card itself does
// with a final cut, the heaviest card (preview, QA report, chapters), so the cause is looked for
// elsewhere: the decision goes to the card's own video and review, and a refused one says so.
const final: Review = {
  id: "5332abba-80a5-4400-895d-954b4ec4328f", gate: "final", content_sha256: "b".repeat(64), summary: "Synthetic final cut",
  payload: {
    checks: { ok: true, problems: [] }, chapters: [{ time: "0:00", title: "Opening" }],
    qa: { ok: false, final_sha256: "b".repeat(64), items: [{ id: "policy", ok: false, detail: "stance missing" }, { id: "render", ok: true }] },
  },
  files: [{ role: "preview", sha256: "c".repeat(64), size: 10, content_type: "video/mp4" }],
  status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-28T08:40:31Z",
};

type Post = { url: string; body: unknown };
function stubDecision(answer: () => Response) {
  const posts: Post[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    posts.push({ url: String(input), body: JSON.parse(String(init?.body)) });
    return Promise.resolve(answer());
  }));
  return posts;
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("language results and upload package readiness", () => {
  const base: ProjectSummary = {
    slug: "imported-cut", title: "Imported cut", stage: "final approved", pending: 0,
    checklist: [{ key: "final_video_approved", label: "Final approved", done: true }],
    youtube_video_id: null, last_synced_at: "2026-10-04T10:00:00Z", ready_to_upload: false,
    locales_decided_at: "2026-10-04T09:00:00Z", locales: { en: { metadata: true, captions: true, dub: true } },
    languages: { en: { metadata: { state: "ready" }, captions: { state: "ready" }, dub: { state: "working" } } },
  };

  it("does not present unreported results as an active producer", () => {
    expect(publishState(base)).toBe("making");
    expect(chosenLanguagesComplete(base)).toBe(false);
    render(<PublishPill project={base} />);
    expect(screen.getByText("語言尚未完成")).toBeTruthy();
    expect(screen.queryByText("語言製作中")).toBeNull();
    expect(publishState({ ...base, languages: {} })).toBe("making");
    expect(publishState({ ...base, languages: { en: { ...base.languages?.en, dub: { state: "unrecognized" } } } })).toBe("making");
  });

  it("identifies a missing package after all selected parts have results", () => {
    const complete = { ...base, languages: { en: { metadata: { state: "ready" }, captions: { state: "ready" }, dub: { state: "skipped", reason: "quality check failed" } } } };
    expect(chosenLanguagesComplete(complete)).toBe(true);
    expect(publishState(complete)).toBe("packaging");
    render(<PublishPill project={complete} />);
    expect(screen.getByText("上架包尚未就緒")).toBeTruthy();
    expect(publishState({ ...complete, languages: { en: { ...complete.languages.en, dub: { state: "uploaded" } } } })).toBe("packaging");
    expect(publishState({ ...base, locales: {}, languages: {} })).toBe("packaging");
    expect(publishState({ ...complete, ready_to_upload: true, publish_approved_at: "2026-10-04T10:00:00Z" })).toBe("ready");
    expect(publishState({ ...complete, dropped_at: "2026-10-04T10:00:00Z" })).toBeNull();
    expect(publishState({ ...complete, shorts_line: "cut" })).toBeNull();
    expect(publishState({ ...complete, youtube_video_id: "abcdefghijk" })).toBe("published");
    expect(publishState({ ...complete, youtube_video_id: "abcdefghijk", youtube_publish_at: "2999-01-01T00:00:00Z" })).toBe("scheduled");
  });
});

describe("a final cut's review card", () => {
  it("sends the owner's approval for its own video and review, with no choice or note, then reads the page again", async () => {
    const posts = stubDecision(() => Response.json({ ...final, status: "approved", decided_at: "2026-09-28T09:45:12Z" }));
    const onDecided = vi.fn();
    render(<ReviewCard slug="openai-agents-broke-in" review={final} canManage onDecided={onDecided} />);
    const card = screen.getByRole("article", { name: "成片" });
    const approve = within(card).getByRole("button", { name: "核准" });
    // A final cut has nothing to choose: the button is live as soon as the card is.
    expect(approve).toHaveProperty("disabled", false);
    fireEvent.click(approve);
    await waitFor(() => expect(onDecided).toHaveBeenCalledTimes(1));
    expect(posts).toEqual([{ url: `/api/travel/admin/videos/openai-agents-broke-in/reviews/${final.id}/decision`, body: { decision: "approve" } }]);
    expect(within(card).queryByRole("alert")).toBeNull();
  });

  it("keeps a refused approval on the card with the reason, and lets the owner send it again", async () => {
    let refuse = true;
    const posts = stubDecision(() => (refuse
      ? Response.json({ code: "authentication_required", detail: "Sign in again" }, { status: 401 })
      : Response.json({ ...final, status: "approved" })));
    const onDecided = vi.fn();
    render(<ReviewCard slug="openai-agents-broke-in" review={final} canManage onDecided={onDecided} />);
    const card = screen.getByRole("article", { name: "成片" });
    fireEvent.click(within(card).getByRole("button", { name: "核准" }));
    const alert = await within(card).findByRole("alert");
    expect(alert.textContent).toMatch(/^沒有送出：/);
    expect(onDecided).not.toHaveBeenCalled();
    // The card is still the pending one, and the button is back for a second try.
    const approve = within(card).getByRole("button", { name: "核准" });
    expect(approve).toHaveProperty("disabled", false);
    refuse = false;
    fireEvent.click(approve);
    await waitFor(() => expect(onDecided).toHaveBeenCalledTimes(1));
    expect(posts).toHaveLength(2);
    expect(within(card).queryByRole("alert")).toBeNull();
  });
});

// Ticket 2026-10-02-show-thumbnail-variants-b-and-c: Test & compare thumbnails B and C.
const jpeg = (role: string, char: string) => ({ role, sha256: char.repeat(64), size: 2048, content_type: "image/jpeg" });

describe("thumbnail variants B and C", () => {
  it("shows A, B and C side by side on a final cut that has them", () => {
    const review = { ...final, files: [...final.files, jpeg("thumbnail", "d"), jpeg("thumbnail-b", "e"), jpeg("thumbnail-c", "f")] };
    render(<ReviewCard slug="why-ice-floats" review={review} canManage={false} onDecided={vi.fn()} />);
    const card = screen.getByRole("article", { name: "成片" });
    const pictures = ["A", "B", "C"].map((letter) => within(card).getByRole("img", { name: `縮圖 ${letter}` }));
    expect(pictures.map((picture) => picture.getAttribute("src"))).toEqual(["d", "e", "f"].map((char) => `/api/admin-video-files/why-ice-floats/${char.repeat(64)}`));
  });

  it("leaves a final cut without variants as it was", () => {
    const review = { ...final, files: [...final.files, jpeg("thumbnail", "d")] };
    render(<ReviewCard slug="why-ice-floats" review={review} canManage={false} onDecided={vi.fn()} />);
    expect(within(screen.getByRole("article", { name: "成片" })).queryByRole("img", { name: /^縮圖 / })).toBeNull();
  });

  it("offers B and C as their own downloads on the publish card, not as languages", () => {
    const review: Review = { ...final, gate: "publish", payload: { locales: ["zh-TW", "en"] }, files: [jpeg("thumbnail", "d"), jpeg("thumbnail-b", "e"), jpeg("thumbnail-c", "f"), jpeg("thumbnail_en", "a")] };
    render(<UploadPackage slug="why-ice-floats" review={review} />);
    const links = screen.getAllByRole("link").map((link) => [link.textContent?.replace(/\d.*$/, "").trim(), link.getAttribute("download")]);
    expect(links).toEqual([["縮圖 thumbnail.jpg", "thumbnail.jpg"], ["縮圖 B", "thumbnail-b.jpg"], ["縮圖 C", "thumbnail-c.jpg"], ["縮圖 en", "thumbnail.en.jpg"]]);
  });
});

// Ticket 2026-10-09-languages-card-says-the-site-cannot: sixteen batches with a ready dub track
// were approved and none of the tracks reached YouTube, because the owner read the button as
// an order to the site. The site cannot upload an audio track (YouTube has no API for it), so
// the card says so first, the button reads as the owner's own statement, and an approved
// batch still offers the track and the steps, since approving never uploaded anything.
describe("a languages card with a dub track", () => {
  const languages: Review = {
    id: "c2a1d0e9-5d8a-4f03-9b8e-1f2a3b4c5d6e", gate: "languages", content_sha256: "a".repeat(64), summary: "語言：en 三項完成",
    payload: { locales: { en: { metadata: "ready", captions: "ready", dub: "ready", file: "en.m4a", format: "m4a", file_role: "dub_en" } } },
    files: [{ role: "dub_en", sha256: "1".repeat(64), size: 25_000_000, content_type: "audio/mp4" }],
    status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-10-09T10:00:00Z",
  };

  it("says the site cannot upload the track before the steps, and the button is the owner's statement", () => {
    render(<ReviewCard slug="meta-anti-scam-2fa-passkey" review={languages} canManage onDecided={vi.fn()} />);
    const card = screen.getByRole("article", { name: "語言" });
    expect(card.textContent).toContain("網站沒辦法替你上傳音軌：YouTube 沒有這個 API，只有你能在 Studio 傳。");
    expect(card.textContent).toContain("開啟「進階功能」");
    expect(card.textContent).toContain("按了網站不會替你傳");
    expect(within(card).getByRole("button", { name: "我已經在 Studio 傳好這些配音" })).toHaveProperty("disabled", false);
    expect(within(card).queryByRole("button", { name: "已在 Studio 上傳配音" })).toBeNull();
  });

  it("keeps the track and the Studio steps on an approved batch, so the owner can still upload it", () => {
    const approved: Review = { ...languages, status: "approved", decided_at: "2026-10-09T10:05:00Z" };
    render(<ReviewCard slug="meta-anti-scam-2fa-passkey" review={approved} canManage onDecided={vi.fn()} />);
    const card = screen.getByRole("article", { name: "語言" });
    expect(within(card).getByRole("link", { name: "下載 en.m4a" }).getAttribute("href")).toContain("1".repeat(64));
    expect(card.textContent).toContain("「新增語言」");
    expect(within(card).queryByRole("button", { name: "我已經在 Studio 傳好這些配音" })).toBeNull();
  });
});
