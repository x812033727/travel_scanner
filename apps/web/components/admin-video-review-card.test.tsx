import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ReviewCard, type Review } from "./admin-video-review-card";

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
