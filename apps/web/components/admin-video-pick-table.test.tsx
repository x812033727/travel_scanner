import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ReviewCard, type Review } from "./admin-video-review-card";

// Ticket 2026-10-17-review-card-s-outline-pick-table: an outline pick for a video the site files
// as an explainer or a story carries demo: null on every option, since the question was not asked
// (2026-10-10-outline-pick-demo-exempts-explainers). The table says so and does not count it
// against the pick; a tutorial's score, or a score that is simply missing, reads as before.
function outline(options: Record<string, Record<string, unknown>>): Review {
  return {
    id: "6f3d1c1e-0d36-4b4e-9a54-6f1b7d2f8a10", gate: "outline", content_sha256: "a".repeat(64), summary: "兩個大綱",
    payload: {
      options: [{ key: "A", title: "從海苔受潮講起" }, { key: "B", title: "從專利講起" }],
      pick: { choice: "A", probabilities: { A: 1, B: 0 }, options, advice: 0.02 },
    },
    files: [], status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-10-17T01:00:00Z",
  };
}

function table(review: Review) {
  render(<ReviewCard slug="sothatswhy-b26" review={review} canManage={false} onDecided={vi.fn()} />);
  return screen.getByLabelText("Jev 挑選的理由");
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("the outline pick table", () => {
  it("shows a demonstration that was not asked as not applicable and does not hold the pick back for it", () => {
    const shown = table(outline({ A: { stance: 0.92, demo: null }, B: { stance: 0.7, demo: null } }));
    const rows = [...shown.querySelectorAll("tbody tr")].map((row) => row.textContent);
    expect(rows[0]).toContain("0.92");
    expect(rows[0]).toContain("不適用（解說）");
    expect(rows[1]).toContain("不適用（解說）");
    expect(screen.queryByText("有項目沒過門檻，所以還是等你決定。")).toBeNull();
  });

  it("still holds a pick back for a low score, a missing score or a low stance", () => {
    for (const options of [
      { A: { stance: 0.92, demo: 0.33 }, B: { stance: 0.7, demo: 0.2 } },
      { A: { stance: 0.92 }, B: { stance: 0.7 } },
      { A: { stance: 0.5, demo: null }, B: { stance: 0.7, demo: null } },
    ]) {
      table(outline(options));
      expect(screen.getByText("有項目沒過門檻，所以還是等你決定。")).toBeTruthy();
      cleanup();
    }
  });
});
