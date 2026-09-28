import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { ReviewCard, type Review, type ReviewFile } from "./admin-video-review-card";

const image = (role: string, n: number): ReviewFile => ({ role, sha256: String(n).padStart(64, "0"), size: 100, content_type: "image/png" });
const url = (file: ReviewFile) => `/api/admin-video-files/story/${file.sha256}`;
const review = (payload: Review["payload"], files: ReviewFile[]): Review => ({
  id: "storyboard-review", gate: "storyboard", content_sha256: "a".repeat(64),
  summary: "Synthetic storyboard", payload, files, status: "pending", choice: null,
  note: null, decided_at: null, created_at: "2026-09-28T07:00:00Z",
});
const show = (value: Review) => render(<ReviewCard slug="story" review={value} canManage={false} onDecided={() => {}} />);

afterEach(cleanup);

describe("storyboard contact sheets", () => {
  it("shows all four pages for 95 shots and links omitted keyframes to the correct uploaded page", () => {
    const pages = Array.from({ length: 4 }, (_, i) => image(`contact_sheet_0${i + 1}`, i + 1));
    const keyframe = image("shot_01", 5);
    const shots = Array.from({ length: 95 }, (_, i) => ({ id: `shot-${i + 1}`, prompt: "Synthetic shot", file_role: i === 0 ? "shot_01" : null }));
    const sheets = pages.map((file, i) => ({ role: file.role, shots: shots.slice(i * 24, (i + 1) * 24).map(shot => shot.id) }));
    const { container } = show(review({ shots, sheets, omitted: 94 }, [...pages].reverse().concat(keyframe)));
    expect(Array.from(container.querySelectorAll("details img")).map(img => img.getAttribute("src"))).toEqual(pages.map(url));
    expect(screen.getByRole("img", { name: "shot-1" }).getAttribute("src")).toBe(url(keyframe));
    expect(screen.getAllByRole("link", { name: "聯絡表 4 / 4" })).toHaveLength(23);
    for (const link of screen.getAllByRole("link", { name: "聯絡表 4 / 4" })) expect(link.getAttribute("href")).toBe(url(pages[3]));
    expect(container.querySelectorAll("li")).toHaveLength(95);
    expect(screen.getByRole("button", { name: "分鏡可以，做片段" }).hasAttribute("disabled")).toBe(true);
  });

  it("keeps the legacy single-sheet review and individual keyframe", () => {
    const sheet = image("contact_sheet", 1);
    const shot = image("shot_01", 2);
    const { container } = show(review({ shots: [{ id: "one", file_role: shot.role }] }, [shot, sheet]));
    expect(container.querySelector("details summary")?.textContent).toBe("聯絡表");
    expect(container.querySelector("details img")?.getAttribute("src")).toBe(url(sheet));
    expect(screen.getByRole("img", { name: "one" }).getAttribute("src")).toBe(url(shot));
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("reads available numbered files even if optional sheet metadata is absent", () => {
    const second = image("contact_sheet_02", 2);
    const tenth = image("contact_sheet_10", 10);
    const { container } = show(review({ shots: [] }, [tenth, second]));
    expect(Array.from(container.querySelectorAll("details img")).map(img => img.getAttribute("src"))).toEqual([url(second), url(tenth)]);
  });

  it("ignores missing or malformed file references and does not duplicate an uploaded page", () => {
    const sheet = image("contact_sheet_01", 1);
    const other = image("thumbnail", 2);
    const { container } = show(review({ shots: [{ id: "one", file_role: null }], sheets: [
      null, { role: "missing", shots: ["one"] }, { role: "thumbnail", shots: ["one"] },
      { role: sheet.role, shots: ["one"] }, { role: sheet.role, shots: ["one"] },
    ] }, [other, sheet, sheet]));
    expect(container.querySelectorAll("details img")).toHaveLength(1);
    expect(screen.getByRole("link", { name: "聯絡表" }).getAttribute("href")).toBe(url(sheet));
    expect(container.querySelector(`img[src="${url(other)}"]`)).toBeNull();
  });
});
