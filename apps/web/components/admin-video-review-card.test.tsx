import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ReviewCard, UploadPackage, type Review } from "./admin-video-review-card";

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
